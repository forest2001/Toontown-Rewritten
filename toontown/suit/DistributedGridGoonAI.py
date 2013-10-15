from direct.directnotify import DirectNotifyGlobal
from toontown.suit.DistributedGoonAI import DistributedGoonAI

class DistributedGridGoonAI(DistributedGoonAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedGridGoonAI")

    def setPathPts(self, todo0, todo1, todo2, todo3, todo4, todo5):
        pass

