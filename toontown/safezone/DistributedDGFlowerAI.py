from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

class DistributedDGFlowerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedDGFlowerAI")

    def avatarEnter(self):
        pass

    def avatarExit(self):
        pass

    def setHeight(self, todo0):
        pass

