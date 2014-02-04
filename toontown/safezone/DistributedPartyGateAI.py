from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from toontown.parties import PartyGlobals

class DistributedPartyGateAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedPartyGateAI")

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.area = None

    def setArea(self, area):
        self.area = area

    def getArea(self):
        return self.area

    def getPartyList(self, avId):
        partyManager = simbase.air.partyManager
        self.sendUpdateToAvatarId(avId, 'listAllPublicParties', [partyManager.getPublicParties()])

    def partyChoiceRequest(self, avId, shardId, zoneId):
        # Try to get a spot for them in the party
        # find partyId
        party = None
        pid = 0
        for partyId in self.air.partyManager.pubPartyInfo:
            p = self.air.partyManager.pubPartyInfo[partyId]
            if p.get('shardId', 0) == shardId and p.get('zoneId', 0) == zoneId:
                party = p
                pid = partyId
                break
        if not party:
            self.sendUpdateToAvatarId(self.air.getAvatarIdFromSender(), 'partyRequestDenied', [PartyGlobals.PartyGateDenialReasons.Unavailable])
            return #dafuq
        self.air.globalPartyMgr.requestPartySlot(pid, self.air.getAvatarIdFromSender(), self.doId)