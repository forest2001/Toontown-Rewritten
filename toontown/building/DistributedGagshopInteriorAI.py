from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

class DistributedGagshopInteriorAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedGagshopInteriorAI")

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.zoneId = 0
        self.block = 0
    
    def setZoneIdAndBlock(self, zoneId, block):
        self.zoneId = zoneId
        self.block = block
    
    def getZoneIdAndBlock(self):
        return [self.zoneId, self.block]