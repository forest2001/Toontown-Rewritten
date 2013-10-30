from direct.directnotify import DirectNotifyGlobal
from toontown.coghq.DistributedCrusherEntityAI import DistributedCrusherEntityAI

class DistributedStomperAI(DistributedCrusherEntityAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedStomperAI")

    def setMovie(self, todo0, todo1, todo2):
        pass

