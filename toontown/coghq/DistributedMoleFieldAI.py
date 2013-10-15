from direct.directnotify import DirectNotifyGlobal
from otp.level.DistributedEntityAI import DistributedEntityAI

class DistributedMoleFieldAI(DistributedEntityAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedMoleFieldAI")

    def setGameStart(self, todo0, todo1, todo2):
        pass

    def setClientTriggered(self):
        pass

    def whackedMole(self, todo0, todo1):
        pass

    def whackedBomb(self, todo0, todo1, todo2):
        pass

    def updateMole(self, todo0, todo1):
        pass

    def reportToonHitByBomb(self, todo0, todo1, todo2):
        pass

    def setScore(self, todo0):
        pass

    def damageMe(self):
        pass

    def setPityWin(self):
        pass

