from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

class DistributedTargetAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedTargetAI")

    def setPosition(self, todo0, todo1, todo2):
        pass

    def setState(self, todo0, todo1, todo2):
        pass

    def setReward(self, todo0):
        pass

    def setResult(self, todo0):
        pass

    def setBonus(self, todo0):
        pass

    def setCurPinballScore(self, todo0, todo1, todo2):
        pass

    def setPinballHiScorer(self, todo0):
        pass

    def setPinballHiScore(self, todo0):
        pass

