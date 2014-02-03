from toontown.toonbase import ToontownGlobals
from HoodAI import HoodAI
from toontown.dna.DNAParser import DNAStorage
from toontown.toon import NPCToons

class BRHoodAI(HoodAI):
    HOOD = ToontownGlobals.TheBrrrgh

    def createSafeZone(self):
        HoodAI.createSafeZone(self)
        
        self.spawnObjects()
