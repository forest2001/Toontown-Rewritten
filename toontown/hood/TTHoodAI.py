from toontown.toonbase import ToontownGlobals
from toontown.safezone.DistributedFishingSpotAI import DistributedFishingSpotAI
from toontown.toon import NPCToons
from toontown.dna.DNAParser import DNAStorage
from toontown.town.TTStreetAI import TTStreetAI
from toontown.toon.DistributedNPCToonBaseAI import DistributedNPCToonBaseAI
from toontown.toon.ToonDNA import ToonDNA
from toontown.ai.DistributedBlackCatMgrAI import DistributedBlackCatMgrAI
from HoodAI import HoodAI
from toontown.safezone import ButterflyGlobals
from toontown.safezone.DistributedButterflyAI import DistributedButterflyAI

class TTHoodAI(HoodAI):
    HOOD = ToontownGlobals.ToontownCentral
    
    def createSafeZone(self):
        HoodAI.createSafeZone(self)
        
        self.dnaStore = DNAStorage()
        self.dnaData = simbase.air.loadDNAFileAI(self.dnaStore, 'phase_4/dna/toontown_central_sz.dna')

        #this is messier than it needs to be
        self.createPond(self.dnaData)

        # Black Cat Flippy!
        self.createFlippy()
        blackCatMgr = DistributedBlackCatMgrAI(self.air)
        blackCatMgr.generateWithRequired(self.HOOD)

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
        playground = ButterflyGlobals.TTC
        for area in range(ButterflyGlobals.NUM_BUTTERFLY_AREAS[playground]):
            for b in range(ButterflyGlobals.NUM_BUTTERFLIES[playground]):
                butterfly = DistributedButterflyAI(self.air)
                butterfly.setArea(playground, area)
                butterfly.setState(0, 0, 0, 1, 1)
                butterfly.generateWithRequired(self.HOOD)
                
    def createFlippy(self):
        # NPCToons requires questManager for Flippy, so do this instead :D.
        npc = DistributedNPCToonBaseAI(self.air, 9001)
        dna = ToonDNA()
        dna.newToonFromProperties('dss', 'ms', 'm', 'm', 17, 0, 17, 17, 3, 3, 3, 3, 7, 2)
        npc.setName('Flippy')
        npc.setDNAString(dna.makeNetString())
        npc.setHp(15)
        npc.setMaxHp(15)
        npc.setPositionIndex(12)
        npc.generateWithRequired(self.SAFEZONE)
