from direct.directnotify import DirectNotifyGlobal
from toontown.coghq.DistributedCrushableEntityAI import DistributedCrushableEntityAI

class DistributedGoonAI(DistributedCrushableEntityAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedGoonAI")

    def requestBattle(self, todo0):
        pass

    def requestStunned(self, todo0):
        pass

    def requestResync(self):
        pass

    def setParameterize(self, todo0, todo1, todo2, todo3):
        pass

    def setMovie(self, todo0, todo1, todo2, todo3):
        pass

