from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedNodeAI import DistributedNodeAI

class DistributedPicnicTableAI(DistributedNodeAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedPicnicTableAI")

    def fillSlot(self, todo0, todo1, todo2, todo3, todo4, todo5, todo6, todo7, todo8, todo9):
        pass

    def emptySlot(self, todo0, todo1, todo2):
        pass

    def requestTableState(self):
        pass

    def setTableState(self, todo0, todo1):
        pass

    def setGameZone(self, todo0, todo1):
        pass

    def setIsPlaying(self, todo0):
        pass

    def requestJoin(self, todo0, todo1, todo2, todo3, todo4, todo5, todo6):
        pass

    def rejectJoin(self):
        pass

    def requestObserve(self):
        pass

    def leaveObserve(self):
        pass

    def requestGameZone(self):
        pass

    def requestPickedGame(self, todo0):
        pass

    def requestExit(self):
        pass

    def requestZone(self):
        pass

    def announceWinner(self, todo0, todo1):
        pass

    def allowObserve(self):
        pass

    def allowPick(self):
        pass

    def setZone(self, todo0):
        pass

