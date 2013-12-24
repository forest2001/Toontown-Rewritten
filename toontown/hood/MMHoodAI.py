from toontown.toonbase import ToontownGlobals
from HoodAI import HoodAI
from toontown.dna.DNAParser import DNAStorage
from toontown.toon import NPCToons
from toontown.town.MMStreetAI import MMStreetAI


class MMHoodAI(HoodAI):
    HOOD = ToontownGlobals.MinniesMelodyland
    
    def createSafeZone(self):
        HoodAI.createSafeZone(self)
        
        HoodAI.spawnObjects(self, 'phase_6/dna/minnies_melody_land_sz.dna')
        
    def createStreets(self):
        branchIds = ToontownGlobals.HoodHierarchy.get(self.HOOD, [])
        for branch in branchIds:
            street = MMStreetAI(self.air, branch)
            self.streets[branch] = street
