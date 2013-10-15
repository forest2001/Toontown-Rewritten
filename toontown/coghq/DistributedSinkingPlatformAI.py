from direct.directnotify import DirectNotifyGlobal
from otp.level.DistributedEntityAI import DistributedEntityAI

class DistributedSinkingPlatformAI(DistributedEntityAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedSinkingPlatformAI")

    def setOnOff(self, todo0, todo1):
        pass

    def setSinkMode(self, todo0, todo1, todo2):
        pass

