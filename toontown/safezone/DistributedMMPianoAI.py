from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

class DistributedMMPianoAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedMMPianoAI")

    def requestSpeedUp(self):
        pass

    def requestChangeDirection(self):
        pass

    def setSpeed(self, todo0, todo1, todo2):
        pass

    def playSpeedUp(self, todo0):
        pass

    def playChangeDirection(self, todo0):
        pass

