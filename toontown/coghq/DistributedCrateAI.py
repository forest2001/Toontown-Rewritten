from direct.directnotify import DirectNotifyGlobal
from toontown.coghq.DistributedCrushableEntityAI import DistributedCrushableEntityAI

class DistributedCrateAI(DistributedCrushableEntityAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedCrateAI")

    def requestPush(self, todo0):
        pass

    def setReject(self):
        pass

    def setAccept(self):
        pass

    def setMoveTo(self, todo0, todo1, todo2, todo3, todo4, todo5, todo6):
        pass

    def setDone(self):
        pass

