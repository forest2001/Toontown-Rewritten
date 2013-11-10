from toontown.safezone.DistributedTrolleyAI import DistributedTrolleyAI
from toontown.fishing.DistributedFishingPondAI import DistributedFishingPondAI
from toontown.safezone.DistributedFishingSpotAI import DistributedFishingSpotAI
from toontown.fishing.DistributedFishingTargetAI import DistributedFishingTargetAI
from toontown.fishing.DistributedPondBingoManagerAI import DistributedPondBingoManagerAI
from toontown.fishing import FishingTargetGlobals

class HoodAI:
    """
    AI-side representation of everything in a single neighborhood.

    One subclass of this class exists for every neighborhood in the game.
    HoodAIs are responsible for spawning all TreasurePlanners, SuitPlanners,
    ponds, and other safezone objects, etc.
    """

    SAFEZONE = None

    def __init__(self, air):
        self.air = air

        self.safezone = self.SAFEZONE

        self.trolley = None
        self.pond = None

    def createTrolley(self):
        self.trolley = DistributedTrolleyAI(self.air)
        self.trolley.generateWithRequired(self.safezone)

    def createPond(self):
        self.pond = DistributedFishingPondAI(self.air)
        self.pond.setArea(self.safezone)
        self.pond.generateWithRequired(self.safezone)
        
        bingoManager = DistributedPondBingoManagerAI(self.air)
        bingoManager.setPondDoId(self.pond.getDoId())
        bingoManager.generateWithRequired(self.safezone)
        #temporary, until we have scheduled stuff
        bingoManager.createGame()
        
        self.pond.bingoMgr = bingoManager

        for i in range(FishingTargetGlobals.getNumTargets(self.safezone)):
            target = DistributedFishingTargetAI(self.air)
            target.setPondDoId(self.pond.getDoId())
            target.generateWithRequired(self.safezone)

    def createSpot(self, x, y, z, h, p, r):
        spot = DistributedFishingSpotAI(self.air)
        spot.setPondDoId(self.pond.getDoId())
        spot.setPosHpr(x, y, z, h, p, r)
        spot.generateWithRequired(self.safezone)
