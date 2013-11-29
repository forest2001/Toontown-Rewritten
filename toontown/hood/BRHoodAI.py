from toontown.toonbase import ToontownGlobals
from HoodAI import HoodAI
from toontown.dna.DNAParser import DNAStorage
from toontown.toon import NPCToons
from toontown.town.BRStreetAI import BRStreetAI

class BRHoodAI(HoodAI):
    HOOD = ToontownGlobals.TheBrrrgh

    def createSafeZone(self):
        HoodAI.createSafeZone(self)
        
        self.dnaStore = DNAStorage()
        self.dnaData = simbase.air.loadDNAFileAI(self.dnaStore, 'phase_8/dna/the_burrrgh_sz.dna')

        self.createPond(self.dnaData)
        
        NPCToons.createNPC(self.air, 3009, NPCToons.NPCToonDict.get(3009), self.HOOD, posIndex=0)
        
        self.createHQ(3508, 8)

        
        
    def createStreets(self):
        branchIds = ToontownGlobals.HoodHierarchy.get(self.HOOD, [])
        for branch in branchIds:
            street = BRStreetAI(self.air, branch)
            self.streets[branch] = street
