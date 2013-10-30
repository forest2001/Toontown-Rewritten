from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

class DistributedBuildingAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedBuildingAI")

    def setBlock(self, todo0, todo1):
        pass

    def setSuitData(self, todo0, todo1, todo2):
        pass

    def setVictorList(self, todo0):
        pass

    def setState(self, todo0, todo1):
        pass

    def setVictorReady(self):
        pass

