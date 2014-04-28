from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

class DistributedKartShopInteriorAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedKartShopInteriorAI")
    
    def __init__(self, blockNumber, air, interiorZone):
        DistributedObjectAI.__init__(self, air)
        self.zone = interiorZone
        self.block = blockNumber
    
    def setZoneIdAndBlock(self, zone, block):
        self.zone = zone
        self.block = block
        
    def getZoneIdAndBlock(self):
       return [self.zone, self.block]
