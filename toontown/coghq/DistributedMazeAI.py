from direct.directnotify import DirectNotifyGlobal
from otp.level.DistributedEntityAI import DistributedEntityAI

class DistributedMazeAI(DistributedEntityAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedMazeAI")

    def setRoomDoId(self, todo0):
        pass

    def setGameStart(self, todo0):
        pass

    def setClientTriggered(self):
        pass

    def setFinishedMaze(self):
        pass

    def setGameOver(self):
        pass

    def toonFinished(self, todo0, todo1, todo2):
        pass

    def damageMe(self):
        pass

