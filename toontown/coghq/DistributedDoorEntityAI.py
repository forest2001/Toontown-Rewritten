from direct.directnotify import DirectNotifyGlobal
from otp.level.DistributedEntityAI import DistributedEntityAI

class DistributedDoorEntityAI(DistributedEntityAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedDoorEntityAI")

    def setLocksState(self, todo0):
        pass

    def setDoorState(self, todo0, todo1):
        pass

    def requestOpen(self):
        pass

