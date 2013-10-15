from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

class DistributedBossbotBossAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedBossbotBossAI")

    def setState(self, todo0):
        pass

    def setBattleDifficulty(self, todo0):
        pass

    def requestGetFood(self, todo0, todo1, todo2):
        pass

    def toonGotFood(self, todo0, todo1, todo2, todo3):
        pass

    def requestServeFood(self, todo0, todo1):
        pass

    def toonServeFood(self, todo0, todo1, todo2):
        pass

    def hitBoss(self, todo0):
        pass

    def hitToon(self, todo0):
        pass

    def ballHitBoss(self, todo0):
        pass

    def setBossDamage(self, todo0, todo1, todo2):
        pass

    def setSpeedDamage(self, todo0, todo1, todo2):
        pass

    def reachedTable(self, todo0):
        pass

    def hitTable(self, todo0):
        pass

    def awayFromTable(self, todo0):
        pass

    def toonGotHealed(self, todo0):
        pass

    def requestGetToonup(self, todo0, todo1, todo2):
        pass

    def toonGotToonup(self, todo0, todo1, todo2, todo3):
        pass

