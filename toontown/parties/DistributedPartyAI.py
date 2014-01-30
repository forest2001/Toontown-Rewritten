from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from PartyGlobals import *
import time
# ugh all these activities
from toontown.parties.DistributedPartyJukeboxActivityAI import DistributedPartyJukeboxActivityAI
from toontown.parties.DistributedPartyDanceActivityAI import DistributedPartyDanceActivityAI
from toontown.parties.DistributedPartyJukebox40ActivityAI import DistributedPartyJukebox40ActivityAI
from toontown.parties.DistributedPartyDance20ActivityAI import DistributedPartyDance20ActivityAI
from toontown.parties.DistributedPartyCogActivityAI import DistributedPartyCogActivityAI
from toontown.parties.DistributedPartyTrampolineActivityAI import DistributedPartyTrampolineActivityAI
from toontown.parties.DistributedPartyVictoryTrampolineActivityAI import DistributedPartyVictoryTrampolineActivityAI
from toontown.parties.DistributedPartyCatchActivityAI import DistributedPartyCatchActivityAI
from toontown.parties.DistributedPartyTugOfWarActivityAI import DistributedPartyTugOfWarActivityAI
from toontown.parties.DistributedPartyCannonActivityAI import DistributedPartyCannonActivityAI
from toontown.parties.DistributedPartyFireworksActivityAI import DistributedPartyFireworksActivityAI

"""
dclass DistributedParty : DistributedObject {
  setPartyClockInfo(uint8, uint8, uint8) required broadcast;
  setInviteeIds(uint32array) required broadcast;
  setPartyState(bool) required broadcast;
  setPartyInfoTuple(party) required broadcast;
  setAvIdsAtParty(uint32 []) required broadcast;
  setPartyStartedTime(string) required broadcast;
  setHostName(string) required broadcast;
  avIdEnteredParty(uint32) clsend airecv;
};
"""
class DistributedPartyAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedPartyAI")

    def __init__(self, air, hostId, zoneId, info):
        DistributedObjectAI.__init__(self, air)
        self.hostId = hostId
        self.zoneId = zoneId
        self.info = info
        # buncha required crap
        PARTY_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
        self.startedAt = time.strftime(PARTY_TIME_FORMAT)
        self.partyState = 0
        self.avIdsAtParty = []

        # apparently 'partyclockinfo' is the xyz on the party grid
        for activity in self.info['activities']:
            if activity[0] == ActivityIds.PartyClock:
                self.partyClockInfo = (activity[1], activity[2], activity[3])

        # We'll need to inform the UD later of the host's name so other public parties know the host. Maybe we know who he is..
        self.hostName = ''
        host = self.air.doId2do.get(self.hostId, None)
        if host:
            self.hostName = host.getName()

    def generate(self):
        DistributedObjectAI.generate(self)
        # make stuff
        actId2Class = {
            ActivityIds.PartyJukebox: DistributedPartyJukeboxActivityAI,
            ActivityIds.PartyCannon: DistributedPartyCannonActivityAI,
            ActivityIds.PartyTrampoline: DistributedPartyTrampolineActivityAI,
            ActivityIds.PartyVictoryTrampoline: DistributedPartyVictoryTrampolineActivityAI,
            ActivityIds.PartyCatch: DistributedPartyCatchActivityAI,
            ActivityIds.PartyDance: DistributedPartyDanceActivityAI, 
            ActivityIds.PartyTugOfWar: DistributedPartyTugOfWarActivityAI,
            ActivityIds.PartyFireworks: DistributedPartyFireworksActivityAI,
            ActivityIds.PartyJukebox40: DistributedPartyJukebox40ActivityAI,
            ActivityIds.PartyDance20: DistributedPartyDance20ActivityAI,
            ActivityIds.PartyCog: DistributedPartyCogActivityAI,
        }
        for activity in self.info['activities']:
            actId = activity[0]
            if actId in actId2Class:
                act = actId2Class[actId](self.air, self.doId, activity)
                act.generateWithRequired(self.zoneId)

    def getPartyClockInfo(self):
        return self.partyClockInfo

    def getInviteeIds(self):
        return self.info.get('inviteeIds', [])

    def getPartyState(self):
        return self.partyState

    def b_setPartyState(self, partyState):
        self.partyState = partyState
        self.sendUpdate('setPartyState', [partyState])

    def _formatParty(self, partyDict, status=PartyStatus.Started):
        start = partyDict['start']
        end = partyDict['end']
        return [partyDict['partyId'],
                partyDict['hostId'],
                start.year,
                start.month,
                start.day,
                start.hour,
                start.minute,
                end.year,
                end.month,
                end.day,
                end.hour,
                end.minute,
                partyDict['isPrivate'],
                partyDict['inviteTheme'],
                partyDict['activities'],
                partyDict['decorations'],
                status]
    def getPartyInfoTuple(self):
        return self._formatParty(self.info)

    def getAvIdsAtParty(self):
        return self.avIdsAtParty

    def getPartyStartedTime(self):
        return self.startedAt

    def getHostName(self):
        return self.hostName

    def avIdEnteredParty(self, avId):
        # Sent as the client DistributedParty announces generate
        pass

