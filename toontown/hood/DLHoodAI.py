from toontown.toonbase import ToontownGlobals
from HoodAI import HoodAI
from toontown.dna.DNAParser import DNAStorage
from toontown.toon import NPCToons
from toontown.town.DLStreetAI import DLStreetAI

class DLHoodAI(HoodAI):
    HOOD = ToontownGlobals.DonaldsDreamland
    
    def createSafeZone(self):
        HoodAI.createSafeZone(self)
        
        HoodAI.spawnObjects(self, 'phase_8/dna/donalds_dreamland_sz.dna')
        
    def createStreets(self):
        branchIds = ToontownGlobals.HoodHierarchy.get(self.HOOD, [])
        for branch in branchIds:
            street = DLStreetAI(self.air, branch)
            self.streets[branch] = street
