from toontown.toonbase import ToontownGlobals
from HoodAI import HoodAI
from toontown.safezone import ButterflyGlobals
from toontown.safezone.DistributedButterflyAI import DistributedButterflyAI
from toontown.toon import NPCToons

class TTHoodAI(HoodAI):
    HOOD = ToontownGlobals.ToontownCentral
    
    def createSafeZone(self):
        HoodAI.createSafeZone(self)
        self.spawnObjects()
        
        self.createButterflies()
            
    def createButterflies(self):
        playground = ButterflyGlobals.TTC
        for area in range(ButterflyGlobals.NUM_BUTTERFLY_AREAS[playground]):
            for b in range(ButterflyGlobals.NUM_BUTTERFLIES[playground]):
                butterfly = DistributedButterflyAI(self.air)
                butterfly.setArea(playground, area)
                butterfly.setState(0, 0, 0, 1, 1)
                butterfly.generateWithRequired(self.HOOD)
