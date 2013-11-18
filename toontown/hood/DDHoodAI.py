from toontown.toonbase import ToontownGlobals
from toontown.safezone.DistributedFishingSpotAI import DistributedFishingSpotAI
from toontown.safezone.DistributedBoatAI import DistributedBoatAI
from toontown.toon import NPCToons
from HoodAI import HoodAI


class DDHoodAI(HoodAI):
    HOOD = ToontownGlobals.DonaldsDock

    def createSafeZone(self):
        HoodAI.createSafeZone(self)

        #TODO: make this better
        self.createPond()
        self.createSpot(-1.79822, 139.984, 3.59855, 135, 0, 0)
        self.createSpot(-11.6229, 148.498, 3.64751, 165, 0, 0)
        self.createSpot(-23.6427, 149.15, 3.59725, -165, 0, 0)
        self.createSpot(-31.3754, 141.368, 3.56653, -135, 0, 0)

        NPCToons.createNPC(self.air, 1008, NPCToons.NPCToonDict.get(1008), 1000, posIndex=0)

        self.createHQ(1507, 7)

        self.boat = DistributedBoatAI(self.air)
        self.boat.generateWithRequired(self.safezone)
