from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

class DistributedKartShopInteriorAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedKartShopInteriorAI")
    
    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.zone = None
        self.block = None
    
    def setZoneIdAndBlock(self, zone, block):
        self.zone = zone
        self.block = block
        
    def getZoneIdAndBlock(self):
       return [self.zone, self.block]
