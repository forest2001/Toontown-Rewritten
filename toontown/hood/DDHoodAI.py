from toontown.toonbase import ToontownGlobals
from toontown.safezone.DistributedFishingSpotAI import DistributedFishingSpotAI
from toontown.safezone.DistributedBoatAI import DistributedBoatAI
from toontown.toon import NPCToons
from HoodAI import HoodAI
from toontown.dna.DNAParser import DNAStorage

class DDHoodAI(HoodAI):
    HOOD = ToontownGlobals.DonaldsDock

    def createSafeZone(self):
        HoodAI.createSafeZone(self)

        self.spawnObjects()

        self.boat = DistributedBoatAI(self.air)
        self.boat.generateWithRequired(self.safezone)
