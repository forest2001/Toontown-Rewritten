from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

class DistributedCashbotBossSafeAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedCashbotBossSafeAI")

    def setIndex(self, todo0):
        pass

    def requestInitial(self):
        pass

