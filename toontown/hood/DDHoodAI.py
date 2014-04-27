from toontown.toonbase import ToontownGlobals
from toontown.safezone.DistributedFishingSpotAI import DistributedFishingSpotAI
from toontown.safezone.DistributedBoatAI import DistributedBoatAI
from toontown.toon import NPCToons
from SZHoodAI import SZHoodAI

class DDHoodAI(SZHoodAI):
    HOOD = ToontownGlobals.DonaldsDock

    def createZone(self):
        SZHoodAI.createZone(self)

        self.spawnObjects()

        self.boat = DistributedBoatAI(self.air)
        self.boat.generateWithRequired(self.safezone)
