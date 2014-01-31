from direct.distributed.DistributedObjectGlobalAI import DistributedObjectGlobalAI
from direct.distributed.PyDatagram import *
from direct.directnotify.DirectNotifyGlobal import directNotify

class GlobalPartyManagerAI(DistributedObjectGlobalAI):
    notify = directNotify.newCategory('GlobalPartyManagerAI')
    
    def announceGenerate(self):
        DistributedObjectGlobalAI.announceGenerate(self)
        # Inform the UD that we as an AI have started up, and tell him the doId of our partymanager, so they can talk
        self.sendUpdate('partyManagerAIHello', [simbase.air.partyManager.doId])

    def sendAddParty(self, avId, partyId, start, end, isPrivate, inviteTheme, activities, decorations, inviteeIds):
        self.sendUpdate('addParty', [avId, partyId, start, end, isPrivate, inviteTheme, activities, decorations, inviteeIds])
        
    def queryPartyForHost(self, hostId):
        self.sendUpdate('queryParty', [hostId])

    def partyStarted(self, partyId, shardId, zoneId, hostName):
        self.sendUpdate('partyHasStarted', [partyId, shardId, zoneId, hostName])

    def toonJoinedParty(self, partyId, avId):
        self.sendUpdate('toonJoinedParty', [partyId, avId])

    def toonLeftParty(self, partyId, avId):
        self.sendUpdate('toonLeftParty', [partyId, avId])