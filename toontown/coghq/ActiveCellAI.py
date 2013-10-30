from direct.directnotify import DirectNotifyGlobal
from otp.level.DistributedEntityAI import DistributedEntityAI

class ActiveCellAI(DistributedEntityAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("ActiveCellAI")

    def setState(self, todo0, todo1):
        pass

