from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

class SafeZoneManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("SafeZoneManagerAI")

    def enterSafeZone(self):
        pass

    def exitSafeZone(self):
        pass

