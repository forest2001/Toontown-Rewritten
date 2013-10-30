from direct.directnotify import DirectNotifyGlobal
from toontown.estate.DistributedLawnDecorAI import DistributedLawnDecorAI

class DistributedStatuaryAI(DistributedLawnDecorAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedStatuaryAI")

    def setTypeIndex(self, todo0):
        pass

    def setWaterLevel(self, todo0):
        pass

    def setGrowthLevel(self, todo0):
        pass

