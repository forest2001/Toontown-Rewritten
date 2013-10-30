from direct.directnotify import DirectNotifyGlobal
from toontown.suit.DistributedSuitBaseAI import DistributedSuitBaseAI

class DistributedSuitAI(DistributedSuitBaseAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedSuitAI")

    def requestBattle(self, todo0, todo1, todo2, todo3, todo4, todo5):
        pass

    def setSPDoId(self, todo0):
        pass

    def setPathEndpoints(self, todo0, todo1, todo2, todo3):
        pass

    def setPathPosition(self, todo0, todo1):
        pass

    def setPathState(self, todo0):
        pass

    def debugSuitPosition(self, todo0, todo1, todo2, todo3, todo4):
        pass

