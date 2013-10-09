from direct.directnotify import DirectNotifyGlobal
from otp.level.DistributedEntityAI import DistributedEntityAI

class DistributedLiftAI(DistributedEntityAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedLiftAI")

    def setStateTransition(self, todo0, todo1, todo2):
        pass

    def setAvatarEnter(self):
        pass

    def setAvatarLeave(self):
        pass

