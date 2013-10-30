from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

class DistributedCCharBaseAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedCCharBaseAI")

    def setChat(self, todo0, todo1, todo2):
        pass

    def fadeAway(self):
        pass

    def setWalk(self, todo0, todo1, todo2):
        pass

    def avatarEnter(self):
        pass

    def avatarExit(self):
        pass

    def setNearbyAvatarChat(self, todo0):
        pass

    def setNearbyAvatarSC(self, todo0):
        pass

    def setNearbyAvatarSCCustom(self, todo0):
        pass

    def setNearbyAvatarSCToontask(self, todo0, todo1, todo2, todo3):
        pass

