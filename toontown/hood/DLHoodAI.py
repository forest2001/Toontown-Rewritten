from toontown.toonbase import ToontownGlobals
from HoodAI import HoodAI
from toontown.dna.DNAParser import DNAStorage
from toontown.toon import NPCToons
from toontown.town.DLStreetAI import DLStreetAI

class DLHoodAI(HoodAI):
    HOOD = ToontownGlobals.DonaldsDreamland
    
    def createSafeZone(self):
        HoodAI.createSafeZone(self)

        self.dnaStore = DNAStorage()
        self.dnaData = simbase.air.loadDNAFileAI(self.dnaStore, 'phase_8/dna/donalds_dreamland_sz.dna')
        
        self.createPond(self.dnaData)
        
        NPCToons.createNPC(self.air, 9011, NPCToons.NPCToonDict.get(9011), self.HOOD, posIndex=0)
        
        self.createHQ(9505,5)

        
    def createStreets(self):
        branchIds = ToontownGlobals.HoodHierarchy.get(self.HOOD, [])
        for branch in branchIds:
            street = DLStreetAI(self.air, branch)
            self.streets[branch] = street
