from direct.directnotify import DirectNotifyGlobal
from otp.level.DistributedLevelAI import DistributedLevelAI

class DistributedLawOfficeFloorAI(DistributedLevelAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedLawOfficeFloorAI")

    def setLawOfficeId(self, todo0):
        pass

    def setSuits(self, todo0, todo1):
        pass

    def readyForNextFloor(self):
        pass

    def setForemanConfronted(self, todo0):
        pass

    def setDefeated(self):
        pass

