from direct.directnotify import DirectNotifyGlobal
from toontown.estate.DistributedPlantBaseAI import DistributedPlantBaseAI

class DistributedFlowerAI(DistributedPlantBaseAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedFlowerAI")

    def setTypeIndex(self, todo0):
        pass

    def setVariety(self, todo0):
        pass

