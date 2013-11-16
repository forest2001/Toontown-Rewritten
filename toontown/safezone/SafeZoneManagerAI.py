from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

class SafeZoneManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("SafeZoneManagerAI")

    def enterSafeZone(self):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)
        if not av is None:
            zone = av.zoneId
            av.b_setDefaultZone(zone)
            hoodsVisited = av.getHoodsVisited()
            if not zone in hoodsVisited:
                hoodsVisited.append(zone)
                av.b_setHoodsVisited(hoodsVisited)

    def exitSafeZone(self):
        pass