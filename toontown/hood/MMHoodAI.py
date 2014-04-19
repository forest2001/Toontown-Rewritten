from toontown.toonbase import ToontownGlobals
from SZHoodAI import SZHoodAI
from toontown.toon import NPCToons

class MMHoodAI(SZHoodAI):
    HOOD = ToontownGlobals.MinniesMelodyland
    
    def createZone(self):
        SZHoodAI.createZone(self)
        
        self.spawnObjects()
