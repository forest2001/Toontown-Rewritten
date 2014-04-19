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

        self.spawnObjects()
