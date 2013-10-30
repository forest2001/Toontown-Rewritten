from direct.directnotify import DirectNotifyGlobal
from otp.level.DistributedEntityAI import DistributedEntityAI

class DistributedSecurityCameraAI(DistributedEntityAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedSecurityCameraAI")

    def trapFire(self):
        pass

    def setTarget(self, todo0):
        pass

