from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedNodeAI import DistributedNodeAI

class DistributedFindFourAI(DistributedNodeAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedFindFourAI")

    def requestExit(self):
        pass

    def requestBegin(self):
        pass

    def requestMove(self, todo0):
        pass

    def requestTimer(self):
        pass

    def requestWin(self, todo0):
        pass

    def startBeginTimer(self, todo0, todo1):
        pass

    def setTableDoId(self, todo0):
        pass

    def setGameState(self, todo0, todo1, todo2, todo3):
        pass

    def setTimer(self, todo0):
        pass

    def setTurnTimer(self, todo0):
        pass

    def gameStart(self, todo0):
        pass

    def sendTurn(self, todo0):
        pass

    def announceWin(self, todo0):
        pass

    def announceWinLocation(self, todo0, todo1, todo2, todo3):
        pass

    def announceWinnerPosition(self, todo0, todo1, todo2, todo3):
        pass

    def illegalMove(self):
        pass

    def tie(self):
        pass

