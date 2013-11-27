from toontown.toonbase import ToontownGlobals
from HoodAI import HoodAI

class DLHoodAI(HoodAI):
    HOOD = ToontownGlobals.DonaldsDreamland
    
    def createSafeZone(self):
        HoodAI.createSafeZone(self)
        
        self.createHQ(9505,5)
