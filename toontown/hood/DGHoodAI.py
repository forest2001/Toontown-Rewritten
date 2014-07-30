from toontown.toonbase import ToontownGlobals
from toontown.safezone.DistributedDGFlowerAI import DistributedDGFlowerAI
from SZHoodAI import SZHoodAI
from toontown.toon import NPCToons
from toontown.safezone import ButterflyGlobals
from toontown.safezone.DistributedButterflyAI import DistributedButterflyAI

class DGHoodAI(SZHoodAI):
    HOOD = ToontownGlobals.DaisyGardens

    def createZone(self):
        SZHoodAI.createZone(self)
        self.butterflies = []
        self.spawnObjects()

        self.flower = DistributedDGFlowerAI(self.air)
        self.flower.generateWithRequired(self.HOOD)
        self.createButterflies()

    def createButterflies(self):
        playground = ButterflyGlobals.DG
        for area in range(ButterflyGlobals.NUM_BUTTERFLY_AREAS[playground]):
            for b in range(ButterflyGlobals.NUM_BUTTERFLIES[playground]):
                butterfly = DistributedButterflyAI(self.air)
                butterfly.setArea(playground, area)
                butterfly.setState(0, 0, 0, 1, 1)
                butterfly.generateWithRequired(self.HOOD)
                self.butterflies.append(butterfly)
