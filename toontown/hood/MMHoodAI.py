from toontown.toonbase import ToontownGlobals
from HoodAI import HoodAI

class MMHoodAI(HoodAI):
    HOOD = ToontownGlobals.MinniesMelodyland
    
    def createSafeZone(self):
        HoodAI.createSafeZone(self)
        
        self.createHQ(4504, 4)
