from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

class DistributedMailboxAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedMailboxAI")

    def setHouseId(self, todo0):
        pass

    def setHousePos(self, todo0):
        pass

    def setName(self, todo0):
        pass

    def setFullIndicator(self, todo0):
        pass

    def avatarEnter(self):
        pass

    def avatarExit(self):
        pass

    def freeAvatar(self):
        pass

    def setMovie(self, todo0, todo1):
        pass

    def acceptItemMessage(self, todo0, todo1, todo2, todo3):
        pass

    def acceptItemResponse(self, todo0, todo1):
        pass

    def discardItemMessage(self, todo0, todo1, todo2, todo3):
        pass

    def discardItemResponse(self, todo0, todo1):
        pass

    def acceptInviteMessage(self, todo0, todo1):
        pass

    def rejectInviteMessage(self, todo0, todo1):
        pass

    def markInviteReadButNotReplied(self, todo0):
        pass

