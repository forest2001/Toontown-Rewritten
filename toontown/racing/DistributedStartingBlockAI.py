from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

class DistributedStartingBlockAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedStartingBlockAI")

    def setPadDoId(self, todo0):
        pass

    def setPosHpr(self, todo0, todo1, todo2, todo3, todo4, todo5):
        pass

    def setPadLocationId(self, todo0):
        pass

    def requestEnter(self, todo0):
        pass

    def rejectEnter(self, todo0):
        pass

    def requestExit(self):
        pass

    def setOccupied(self, todo0):
        pass

    def setMovie(self, todo0):
        pass

    def movieFinished(self):
        pass

class DistributedViewingBlockAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedViewingBlockAI")
