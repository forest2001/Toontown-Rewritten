from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

class FriendManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("FriendManagerAI")

    def friendQuery(self, todo0):
        pass

    def cancelFriendQuery(self, todo0):
        pass

    def inviteeFriendConsidering(self, todo0, todo1):
        pass

    def inviteeFriendResponse(self, todo0, todo1):
        pass

    def inviteeAcknowledgeCancel(self, todo0):
        pass

    def friendConsidering(self, todo0, todo1):
        pass

    def friendResponse(self, todo0, todo1):
        pass

    def inviteeFriendQuery(self, todo0, todo1, todo2, todo3):
        pass

    def inviteeCancelFriendQuery(self, todo0):
        pass

    def requestSecret(self):
        pass

    def requestSecretResponse(self, todo0, todo1):
        pass

    def submitSecret(self, todo0):
        pass

    def submitSecretResponse(self, todo0, todo1):
        pass

