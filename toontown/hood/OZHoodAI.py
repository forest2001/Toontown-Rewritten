from toontown.toonbase import ToontownGlobals
from HoodAI import HoodAI

class OZHoodAI(HoodAI):
    HOOD = ToontownGlobals.OutdoorZone
    
    def createSafeZone(self):
        HoodAI.createTreasurePlanner()
