from direct.directnotify import DirectNotifyGlobal
from otp.level.DistributedEntityAI import DistributedEntityAI

class DistributedMoverAI(DistributedEntityAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedMoverAI")

    def startMove(self, todo0):
        pass

