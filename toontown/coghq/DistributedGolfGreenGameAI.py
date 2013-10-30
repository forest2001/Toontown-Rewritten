from direct.directnotify import DirectNotifyGlobal
from toontown.coghq.BattleBlockerAI import BattleBlockerAI

class DistributedGolfGreenGameAI(BattleBlockerAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedGolfGreenGameAI")

    def requestJoin(self):
        pass

    def leaveGame(self):
        pass

    def acceptJoin(self, todo0, todo1, todo2):
        pass

    def requestBoard(self, todo0):
        pass

    def startBoard(self, todo0, todo1):
        pass

    def signalDone(self, todo0):
        pass

    def boardCleared(self, todo0):
        pass

    def scoreData(self, todo0, todo1, todo2):
        pass

    def informGag(self, todo0, todo1):
        pass

    def helpOthers(self, todo0):
        pass

    def setTimerStart(self, todo0, todo1):
        pass

