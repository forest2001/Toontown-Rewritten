from toontown.toonbase import ToontownGlobals
from toontown.town.TTStreetAI import TTStreetAI
from HoodAI import HoodAI
from toontown.safezone import ButterflyGlobals
from toontown.safezone.DistributedButterflyAI import DistributedButterflyAI
from toontown.ai.DistributedPolarBearMgrAI import DistributedPolarBearMgrAI
from toontown.toon.DistributedNPCToonBaseAI import DistributedNPCToonBaseAI
from toontown.toon.ToonDNA import ToonDNA

class TTHoodAI(HoodAI):
    HOOD = ToontownGlobals.ToontownCentral
    
    def createSafeZone(self):
        HoodAI.createSafeZone(self)
        HoodAI.spawnObjects(self, 'phase_4/dna/toontown_central_sz.dna')
        
        # Polar Bear Slappy!
        self.createSlappy()
        polarBearMgr = DistributedPolarBearMgrAI(self.air)
        polarBearMgr.generateWithRequired(self.HOOD)
        
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
                
    def createSlappy(self):
        npc = DistributedNPCToonBaseAI(self.air, 9001)
        dna = ToonDNA()
        dna.newToonFromProperties('fls', 'ms', 'l', 'm', 14, 0, 14, 14, 152, 27, 139, 27, 59, 27)
        npc.setName('Slappy')
        npc.setDNAString(dna.makeNetString())
        npc.setHp(15)
        npc.setMaxHp(15)
        npc.setPositionIndex(12)
        npc.generateWithRequired(self.HOOD)
