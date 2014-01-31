from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

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

    def partyChoiceRequest(self, todo0, todo1, todo2):
        pass

    def partyRequestDenied(self, todo0):
        pass

    def setParty(self, todo0):
        pass

