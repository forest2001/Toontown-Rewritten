from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

class DistributedSuitBaseAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedSuitBaseAI")

    def denyBattle(self):
        pass

    def setDNAString(self, todo0):
        pass

    def setLevelDist(self, todo0):
        pass

    def setBrushOff(self, todo0):
        pass

    def setSkelecog(self, todo0):
        pass

    def setSkeleRevives(self, todo0):
        pass

    def setHP(self, todo0):
        pass

