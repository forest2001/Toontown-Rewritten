from HoodAI import HoodAI
from toontown.toonbase import ToontownGlobals
from toontown.distributed import DistributedTimerAI

class OZHoodAI(HoodAI):
    HOOD = ToontownGlobals.OutdoorZone
    
    def createSafeZone(self):
        HoodAI.createTreasurePlanner(self)
        self.timer = DistributedTimerAI.DistributedTimerAI(self.air)
        self.timer.generateWithRequired(ToontownGlobals.OutdoorZone)
