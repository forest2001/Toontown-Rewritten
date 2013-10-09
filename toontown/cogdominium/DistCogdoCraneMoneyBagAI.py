from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

class DistCogdoCraneMoneyBagAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistCogdoCraneMoneyBagAI")

    def setIndex(self, todo0):
        pass

    def requestInitial(self):
        pass

