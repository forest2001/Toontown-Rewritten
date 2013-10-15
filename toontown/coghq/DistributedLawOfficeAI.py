from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

class DistributedLawOfficeAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedLawOfficeAI")

    def setLawOfficeId(self, todo0):
        pass

    def startSignal(self):
        pass

    def readyForNextFloor(self):
        pass

