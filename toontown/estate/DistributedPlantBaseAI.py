from direct.directnotify import DirectNotifyGlobal
from toontown.estate.DistributedLawnDecorAI import DistributedLawnDecorAI

class DistributedPlantBaseAI(DistributedLawnDecorAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedPlantBaseAI")

    def setTypeIndex(self, todo0):
        pass

    def setWaterLevel(self, todo0):
        pass

    def setGrowthLevel(self, todo0):
        pass

    def waterPlant(self):
        pass

    def waterPlantDone(self):
        pass

