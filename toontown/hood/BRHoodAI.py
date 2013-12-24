from toontown.toonbase import ToontownGlobals
from HoodAI import HoodAI
from toontown.dna.DNAParser import DNAStorage
from toontown.toon import NPCToons
from toontown.town.BRStreetAI import BRStreetAI

class BRHoodAI(HoodAI):
    HOOD = ToontownGlobals.TheBrrrgh

    def createSafeZone(self):
        HoodAI.createSafeZone(self)
        
        HoodAI.spawnObjects(self, 'phase_8/dna/the_burrrgh_sz.dna') 
        
    def createStreets(self):
        branchIds = ToontownGlobals.HoodHierarchy.get(self.HOOD, [])
        for branch in branchIds:
            street = BRStreetAI(self.air, branch)
            self.streets[branch] = street
