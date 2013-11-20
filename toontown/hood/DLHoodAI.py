from toontown.toonbase import ToontownGlobals
from HoodAI import HoodAI

class DLHoodAI(HoodAI):
    HOOD = ToontownGlobals.DonaldsDreamland
    
    def createSelfZone(self):
        HoodAI.createSelfZone(self)
        
        self.createHQ(9505,5)
