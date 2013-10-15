from direct.directnotify import DirectNotifyGlobal
from otp.level.DistributedEntityAI import DistributedEntityAI

class DistributedCrushableEntityAI(DistributedEntityAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedCrushableEntityAI")

    def setPosition(self, todo0, todo1, todo2):
        pass

    def setCrushed(self, todo0, todo1):
        pass

