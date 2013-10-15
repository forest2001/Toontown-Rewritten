from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

class DistributedTutorialInteriorAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedTutorialInteriorAI")

    def setZoneIdAndBlock(self, todo0, todo1):
        pass

    def setTutorialNpcId(self, todo0):
        pass

