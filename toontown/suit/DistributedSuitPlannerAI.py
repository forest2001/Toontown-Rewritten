from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

class DistributedSuitPlannerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedSuitPlannerAI")

    def setZoneId(self, todo0):
        pass

    def suitListQuery(self):
        pass

    def suitListResponse(self, todo0):
        pass

    def buildingListQuery(self):
        pass

    def buildingListResponse(self, todo0):
        pass

