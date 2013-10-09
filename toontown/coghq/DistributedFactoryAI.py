from direct.directnotify import DirectNotifyGlobal
from otp.level.DistributedLevelAI import DistributedLevelAI

class DistributedFactoryAI(DistributedLevelAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedFactoryAI")

    def setFactoryId(self, todo0):
        pass

    def setSuits(self, todo0, todo1):
        pass

    def setForemanConfronted(self, todo0):
        pass

    def setDefeated(self):
        pass

