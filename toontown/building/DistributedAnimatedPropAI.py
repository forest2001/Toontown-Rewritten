from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

class DistributedAnimatedPropAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedAnimatedPropAI")

    def setPropId(self, todo0):
        pass

    def setAvatarInteract(self, todo0):
        pass

    def requestInteract(self):
        pass

    def rejectInteract(self):
        pass

    def requestExit(self):
        pass

    def avatarExit(self, todo0):
        pass

    def setState(self, todo0, todo1):
        pass

