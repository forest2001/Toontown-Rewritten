from toontown.toonbase import ToontownGlobals
from HoodAI import HoodAI
from toontown.dna.DNAParser import DNAStorage
from toontown.toon import NPCToons
from toontown.town.MMStreetAI import MMStreetAI


class MMHoodAI(HoodAI):
    HOOD = ToontownGlobals.MinniesMelodyland
    
    def createSafeZone(self):
        HoodAI.createSafeZone(self)
        
        self.dnaStore = DNAStorage()
        self.dnaData = simbase.air.loadDNAFileAI(self.dnaStore, 'phase_6/dna/minnies_melody_land_sz.dna')

        self.createPond(self.dnaData)
        
        NPCToons.createNPC(self.air, 4009, NPCToons.NPCToonDict.get(4009), self.HOOD, posIndex=0)
        
        self.createHQ(4504, 4)

        
    def createStreets(self):
        branchIds = ToontownGlobals.HoodHierarchy.get(self.HOOD, [])
        for branch in branchIds:
            street = MMStreetAI(self.air, branch)
            self.streets[branch] = street
