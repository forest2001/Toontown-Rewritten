from toontown.toonbase import ToontownGlobals
from HoodAI import HoodAI
from toontown.toon import NPCToons

class MMHoodAI(HoodAI):
    HOOD = ToontownGlobals.MinniesMelodyland
    
    def createSafeZone(self):
        HoodAI.createSafeZone(self)
        
        self.spawnObjects()
