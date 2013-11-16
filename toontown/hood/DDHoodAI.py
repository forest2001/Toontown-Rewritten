from toontown.toonbase import ToontownGlobals
from toontown.safezone.DistributedFishingSpotAI import DistributedFishingSpotAI
from toontown.safezone.DistributedBoatAI import DistributedBoatAI
from toontown.toon import NPCToons
from HoodAI import HoodAI


class DDHoodAI(HoodAI):
    SAFEZONE = ToontownGlobals.DonaldsDock

    def __init__(self, air):
        HoodAI.__init__(self, air)
        
        self.createTrolley()

        self.boat = DistributedBoatAI(self.air)
        self.boat.generateWithRequired(self.safezone)