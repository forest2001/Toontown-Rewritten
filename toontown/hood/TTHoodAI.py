from toontown.toonbase import ToontownGlobals
from toontown.safezone.DistributedFishingSpotAI import DistributedFishingSpotAI
from toontown.toon import NPCToons
from toontown.dna.DNAParser import DNAStorage
from toontown.town.TTStreetAI import TTStreetAI
from HoodAI import HoodAI
from toontown.safezone.DistributedButterflyAI import DistributedButterflyAI

class TTHoodAI(HoodAI):
    HOOD = ToontownGlobals.ToontownCentral
    
    def createSafeZone(self):
        HoodAI.createSafeZone(self)
        
        self.dnaStore = DNAStorage()
        self.dnaData = simbase.air.loadDNAFileAI(self.dnaStore, 'phase_4/dna/toontown_central_sz.dna')

        #this is messier than it needs to be
        self.createPond(self.dnaData)

        # Create Fisherman Freddy: 
        NPCToons.createNPC(self.air, 2012, NPCToons.NPCToonDict.get(2012), 2000, posIndex=0)

        self.createHQ(2520, 20)
        
        self.createButterflies()

    def createStreets(self):
        branchIds = ToontownGlobals.HoodHierarchy.get(self.HOOD, [])
        for branch in branchIds:
            street = TTStreetAI(self.air, branch)
            self.streets[branch] = street
            
    def createButterflies(self):
        for i in range(1, 20):
            butterfly = DistributedButterflyAI(self.air)
            butterfly.setArea(self.HOOD, self.HOOD)
            butterfly.setState(1, 1, 1, 1, 1)
