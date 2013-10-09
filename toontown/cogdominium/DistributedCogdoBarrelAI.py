from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

class DistributedCogdoBarrelAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedCogdoBarrelAI")

    def requestGrab(self):
        pass

    def setIndex(self, todo0):
        pass

    def setState(self, todo0):
        pass

    def setGrab(self, todo0):
        pass

    def setReject(self):
        pass

