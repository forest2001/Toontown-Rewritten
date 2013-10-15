from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

class DistributedDoorAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedDoorAI")

    def setZoneIdAndBlock(self, todo0, todo1):
        pass

    def setSwing(self, todo0):
        pass

    def setDoorType(self, todo0):
        pass

    def setDoorIndex(self, todo0):
        pass

    def setOtherZoneIdAndDoId(self, todo0, todo1):
        pass

    def requestEnter(self):
        pass

    def requestExit(self):
        pass

    def rejectEnter(self, todo0):
        pass

    def avatarEnter(self, todo0):
        pass

    def avatarExit(self, todo0):
        pass

    def setState(self, todo0, todo1):
        pass

    def setExitDoorState(self, todo0, todo1):
        pass

