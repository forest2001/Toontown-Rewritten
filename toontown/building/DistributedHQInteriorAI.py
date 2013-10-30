from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

class DistributedHQInteriorAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedHQInteriorAI")

    def setZoneIdAndBlock(self, todo0, todo1):
        pass

    def setLeaderBoard(self, todo0):
        pass

    def setTutorial(self, todo0):
        pass

