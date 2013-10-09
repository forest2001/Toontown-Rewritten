from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedNodeAI import DistributedNodeAI

class DistributedChineseCheckersAI(DistributedNodeAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedChineseCheckersAI")

    def requestExit(self):
        pass

    def requestBegin(self):
        pass

    def requestMove(self, todo0):
        pass

    def requestTimer(self):
        pass

    def requestSeatPositions(self):
        pass

    def startBeginTimer(self, todo0, todo1):
        pass

    def gameStart(self, todo0):
        pass

    def setTableDoId(self, todo0):
        pass

    def setGameState(self, todo0, todo1):
        pass

    def setTimer(self, todo0):
        pass

    def setTurnTimer(self, todo0):
        pass

    def sendTurn(self, todo0):
        pass

    def requestWin(self):
        pass

    def announceWin(self, todo0):
        pass

    def announceSeatPositions(self, todo0):
        pass

