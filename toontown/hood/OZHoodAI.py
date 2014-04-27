from SZHoodAI import SZHoodAI
from toontown.toonbase import ToontownGlobals
from toontown.distributed.DistributedTimerAI import DistributedTimerAI

class OZHoodAI(SZHoodAI):
    HOOD = ToontownGlobals.OutdoorZone
    
    def createZone(self):
        SZHoodAI.createTreasurePlanner(self)
        self.timer = DistributedTimerAI(self.air)
        self.timer.generateWithRequired(self.HOOD)
