from toontown.toonbase import ToontownGlobals
from toontown.safezone.DistributedDGFlowerAI import DistributedDGFlowerAI
from HoodAI import HoodAI
from toontown.dna.DNAParser import DNAStorage
from toontown.toon import NPCToons
from toontown.safezone import ButterflyGlobals
from toontown.safezone.DistributedButterflyAI import DistributedButterflyAI

class DGHoodAI(HoodAI):
    HOOD = ToontownGlobals.DaisyGardens

    def createSafeZone(self):
        HoodAI.createSafeZone(self)

        self.spawnObjects()
