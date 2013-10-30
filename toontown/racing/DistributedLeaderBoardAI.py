from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

class DistributedLeaderBoardAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedLeaderBoardAI")

    def setPosHpr(self, todo0, todo1, todo2, todo3, todo4, todo5):
        pass

    def setDisplay(self, todo0):
        pass

