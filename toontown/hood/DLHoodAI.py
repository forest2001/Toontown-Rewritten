from toontown.toonbase import ToontownGlobals
from SZHoodAI import SZHoodAI
from toontown.toon import NPCToons

class DLHoodAI(SZHoodAI):
    HOOD = ToontownGlobals.DonaldsDreamland
    
    def createZone(self):
        SZHoodAI.createZone(self)
        
        self.spawnObjects()
