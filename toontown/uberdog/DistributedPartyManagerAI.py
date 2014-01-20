from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from otp.distributed.OtpDoGlobals import *
from pandac.PandaModules import *
from toontown.parties.DistributedPartyAI import DistributedPartyAI
import time

class DistributedPartyManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedPartyManagerAI")

    def announceGenerate(self):
        DistributedObjectAI.announceGenerate(self)
        self.partyId2Zone = {}
        self.partyId2PlanningZone = {}
        self.partyId2Host = {}
        self.host2PartyId = {}
        self.partyId2Party = {}
        self.partyInfo = {}
        self.partyAllocator = UniqueIdAllocator(0, 1000000)
        print 'DPMAI - my doid: %s' % self.doId

        self.sendUpdate('partyManagerAIStartingUp', [simbase.air.districtId, 0]) # the 0 is a uint32

    def _makePartyDict(self, struct):
        PARTY_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
        party = {}
        party['partyId'] = struct[0]
        party['hostId'] = struct[1]
        start = '%s-%s-%s %s:%s:00' % (struct[2], struct[3], struct[4], struct[5], struct[6])
        party['start'] = time.strptime(start, PARTY_TIME_FORMAT)
        end = '%s-%s-%s %s:%s:00' % (struct[7], struct[8], struct[9], struct[10], struct[11])
        party['end'] = time.strptime(end, PARTY_TIME_FORMAT)
        party['isPrivate'] = struct[12]
        party['inviteTheme'] = struct[13]
        party['activities'] = struct[14]
        party['decorations'] = struct[15]
        # struct[16] = partystatus
        return party

    # Management stuff
    def partyManagerUdStartingUp(self):
        # This is sent in reply to the GPMAI's hello
        print 'uberdog has come up'

    def partyManagerUdLost(self):
        # well fuck. ud died.
        print 'uberdog died'

    def canBuyParties(self):
        return True

    def addParty(self, todo0, todo1, todo2, todo3, todo4, todo5, todo6, todo7, todo8, todo9):
        pass

    def addPartyRequest(self, hostId, startTime, endTime, isPrivate, inviteTheme, activities, decorations, inviteeIds):
        if hostId != simbase.air.getAvatarIdFromSender():
            # todo: a suspicious
            return
        print 'party requested: host %s, start %s, end %s, private %s, invitetheme %s, activities omitted, decor omitted, invitees %s' % (hostId, startTime, endTime, isPrivate, inviteTheme, inviteeIds)
        simbase.air.globalPartyMgr.sendAddParty(hostId, self.host2PartyId[hostId], startTime, endTime, isPrivate, inviteTheme, activities, decorations, inviteeIds)

    def addPartyResponse(self, hostId, errorCode):
        pass

    def addPartyResponseUdToAi(self, partyId, errorCode):
        avId = self.partyId2Host[partyId]
        print 'responding to client now that ud got back to us'
        self.sendUpdateToAvatarId(avId, 'addPartyResponse', [avId, errorCode])
        pass

    def markInviteAsReadButNotReplied(self, todo0, todo1):
        pass

    def respondToInvite(self, todo0, todo1, todo2, todo3, todo4):
        pass

    def respondToInviteResponse(self, todo0, todo1, todo2, todo3, todo4):
        pass

    def changePrivateRequest(self, todo0, todo1):
        pass

    def changePrivateRequestAiToUd(self, todo0, todo1, todo2):
        pass

    def changePrivateResponseUdToAi(self, todo0, todo1, todo2, todo3):
        pass

    def changePrivateResponse(self, todo0, todo1, todo2):
        pass

    def changePartyStatusRequest(self, partyId, newPartyStatus):
        pass

    def changePartyStatusRequestAiToUd(self, todo0, todo1, todo2):
        pass

    def changePartyStatusResponseUdToAi(self, todo0, todo1, todo2, todo3):
        pass

    def changePartyStatusResponse(self, todo0, todo1, todo2, todo3):
        pass

    def partyInfoOfHostRequestAiToUd(self, todo0, todo1):
        pass

    def partyInfoOfHostFailedResponseUdToAi(self, todo0):
        pass

    def givePartyRefundResponse(self, todo0, todo1, todo2, todo3, todo4):
        pass

    def getPartyZone(self, hostId, zoneId, isAvAboutToPlanParty):
        avId = self.air.getAvatarIdFromSender()
        if isAvAboutToPlanParty:
            partyId = self.partyAllocator.allocate() + (simbase.air.ourChannel << 32) # high 32 bits are the AI's id, low 32 up to AI
            print 'pid %s' % partyId
            self.partyId2Host[partyId] = hostId
            self.partyId2PlanningZone[partyId] = zoneId
            self.host2PartyId[hostId] = partyId
            print 'Responding to a get party zone when planning, av,party,zone: %s %s %s' % (avId, partyId, zoneId)
        else:
            if hostId not in self.host2PartyId:
                # Uhh, we don't know if the host even has a party. Better ask the ud
                self.air.globalPartyMgr.queryPartyForHost(hostId)
                return
            partyId = self.host2PartyId[hostId]
            # Is the party already running?
            if partyId in self.partyId2Zone:
                # Yep!
                zoneId = self.partyId2Zone[partyId]
            elif avId == hostId:
                # Time to start party
                pass
                
        self.sendUpdateToAvatarId(avId, 'receivePartyZone', [hostId, partyId, zoneId])

    def partyInfoOfHostResponseUdToAi(self, partyStruct, inviteeIds):
        party = self._makePartyDict(partyStruct)
        party['inviteeIds'] = inviteeIds
        partyId = party['partyId']
        # This is issued in response to a request for the party to start, essentially. So let's alloc a zone
        zoneId = self.air.allocateZone()
        self.partyId2Zone[partyId] = zoneId
        self.host2PartyId[party['hostId']] = partyId
        
        # We need to setup the party itself on our end, so make an ai party
        partyAI = DistributedPartyAI(self.air, party['hostId'], zoneId, party)
        partyAI.generateWithRequiredAndId(self.air.allocateChannel(), self.air.districtId, zoneId)
        
        # Don't forget this was initially started by a getPartyZone, so we better tell the host the partyzone
        self.sendUpdateToAvatarId(party['hostId'], 'receivePartyZone', [party['hostId'], partyId, zoneId])

    def freeZoneIdFromPlannedParty(self, hostId, zoneId):
        sender = self.air.getAvatarIdFromSender()
        # Only the host of a party can free its zone
        if sender != hostId:
            return # TODO suspicious
        partyId = self.host2PartyId[hostId]
        if partyId in self.partyId2PlanningZone:
            print 'freeing zone'
            self.air.deallocateZone(self.partyId2PlanningZone[partyId])
            del self.partyId2PlanningZone[partyId]
        return

    def sendAvToPlayground(self, todo0, todo1):
        pass

    def exitParty(self, zoneIdOfAv):
        pass

    def removeGuest(self, ownerId, avId):
        pass

    def partyManagerAIStartingUp(self, todo0, todo1):
        pass

    def partyManagerAIGoingDown(self, todo0, todo1):
        pass

    def partyHasStartedAiToUd(self, todo0, todo1, todo2, todo3, todo4):
        pass

    def toonHasEnteredPartyAiToUd(self, todo0):
        pass

    def toonHasExitedPartyAiToUd(self, todo0):
        pass

    def partyHasFinishedUdToAllAi(self, todo0):
        pass

    def updateToPublicPartyInfoUdToAllAi(self, shardId, partyId, hostId, numGuests, maxGuests, hostName, activities):
        self.partyInfo[partyId] = {
          'shardId': shardId,
          'partyId': partyId,
          'hostId': hostId,
          'numGuests': numGuests,
          'maxGuests': maxGuests,
          'hostName': hostName,
          'activities': activities }

    def updateToPublicPartyCountUdToAllAi(self, partyCount, partyId):
        # Update the number of guests at a party
        pass

    def getPublicParties(self):
        p = []
        for party in self.partyInfo:
            print party.get('activities')
            p.append([simbase.air.ourChannel, self.partyId2HostZone[party.get('partyId')][1], 1, "Fat McStink", [1], 10])
        return p

    def requestShardIdZoneIdForHostId(self, todo0):
        pass

    def sendShardIdZoneIdToAvatar(self, todo0, todo1):
        pass

    def updateAllPartyInfoToUd(self, todo0, todo1, todo2, todo3, todo4, todo5, todo6, todo7, todo8):
        pass

    def forceCheckStart(self):
        pass

    def requestMw(self, todo0, todo1, todo2, todo3):
        pass

    def mwResponseUdToAllAi(self, todo0, todo1, todo2, todo3):
        pass

