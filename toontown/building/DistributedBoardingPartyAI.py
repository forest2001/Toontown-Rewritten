from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

class DistributedBoardingPartyAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedBoardingPartyAI")

    def postGroupInfo(self, todo0, todo1, todo2, todo3):
        pass

    def informDestinationInfo(self, todo0):
        pass

    def postDestinationInfo(self, todo0):
        pass

    def postInvite(self, todo0, todo1):
        pass

    def postInviteCanceled(self):
        pass

    def postKick(self, todo0):
        pass

    def postKickReject(self, todo0, todo1, todo2):
        pass

    def postSizeReject(self, todo0, todo1, todo2):
        pass

    def postInviteAccepted(self, todo0):
        pass

    def postInviteDelcined(self, todo0):
        pass

    def postInviteNotQualify(self, todo0, todo1, todo2):
        pass

    def postAlreadyInGroup(self):
        pass

    def postGroupDissolve(self, todo0, todo1, todo2, todo3):
        pass

    def postMessageAcceptanceFailed(self, todo0, todo1):
        pass

    def postGroupAlreadyFull(self):
        pass

    def postSomethingMissing(self):
        pass

    def postRejectBoard(self, todo0, todo1, todo2, todo3):
        pass

    def postRejectGoto(self, todo0, todo1, todo2, todo3):
        pass

    def postMessageInvited(self, todo0, todo1):
        pass

    def postMessageInvitationFailed(self, todo0):
        pass

    def acceptGoToFirstTime(self, todo0):
        pass

    def acceptGoToSecondTime(self, todo0):
        pass

    def rejectGoToRequest(self, todo0, todo1, todo2, todo3):
        pass

    def requestInvite(self, todo0):
        pass

    def requestCancelInvite(self, todo0):
        pass

    def requestAcceptInvite(self, todo0, todo1):
        pass

    def requestRejectInvite(self, todo0, todo1):
        pass

    def requestKick(self, todo0):
        pass

    def requestLeave(self, todo0):
        pass

    def requestBoard(self, todo0):
        pass

    def requestGoToFirstTime(self, todo0):
        pass

    def requestGoToSecondTime(self, todo0):
        pass

    def setElevatorIdList(self, todo0):
        pass

    def setGroupSize(self, todo0):
        pass

