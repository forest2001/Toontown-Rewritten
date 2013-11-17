from toontown.safezone.DistributedTrolleyAI import DistributedTrolleyAI
from toontown.fishing.DistributedFishingPondAI import DistributedFishingPondAI
from toontown.safezone.DistributedFishingSpotAI import DistributedFishingSpotAI
from toontown.fishing.DistributedFishingTargetAI import DistributedFishingTargetAI
from toontown.fishing.DistributedPondBingoManagerAI import DistributedPondBingoManagerAI
from toontown.building.DistributedDoorAI import DistributedDoorAI
from toontown.building.DistributedHQInteriorAI import DistributedHQInteriorAI
from toontown.building import DoorTypes
from toontown.fishing import FishingTargetGlobals
from toontown.safezone import TreasureGlobals
from toontown.safezone.SZTreasurePlannerAI import SZTreasurePlannerAI

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

    def createTreasurePlanner(self):
        treasureType, healAmount, spawnPoints, spawnRate, maxTreasures = TreasureGlobals.SafeZoneTreasureSpawns[self.safezone]
        self.treasurePlanner = SZTreasurePlannerAI(self.safezone, treasureType, healAmount, spawnPoints, spawnRate, maxTreasures)
        self.treasurePlanner.start()

    def createHQ(self, zone, block):
        hqDoor = DistributedDoorAI(self.air)
        hqDoor.setZoneIdAndBlock(self.safezone, block)
        hqDoor.setDoorType(DoorTypes.EXT_HQ)
        hqDoor.setSwing(3)
        hqDoor.generateWithRequired(self.safezone)
        
        hqDoor2 = DistributedDoorAI(self.air)
        hqDoor2.setZoneIdAndBlock(self.safezone, block)
        hqDoor2.setDoorType(DoorTypes.EXT_HQ)
        hqDoor2.setSwing(3)
        hqDoor2.setDoorIndex(1)
        hqDoor2.generateWithRequired(self.safezone)

        hqDoorInt = DistributedDoorAI(self.air)
        hqDoorInt.setZoneIdAndBlock(zone, 0)
        hqDoorInt.setDoorType(DoorTypes.INT_HQ)
        hqDoorInt.setOtherZoneIdAndDoId(self.safezone, hqDoor.getDoId())
        hqDoorInt.generateWithRequired(zone)

        hqDoorInt2 = DistributedDoorAI(self.air)
        hqDoorInt2.setZoneIdAndBlock(zone, 0)
        hqDoorInt2.setDoorType(DoorTypes.INT_HQ)
        hqDoorInt2.setOtherZoneIdAndDoId(self.safezone, hqDoor2.getDoId())
        hqDoorInt2.setDoorIndex(1)
        hqDoorInt2.generateWithRequired(zone)

        hqDoor.setOtherZoneIdAndDoId(zone, hqDoorInt.getDoId())
        hqDoor2.setOtherZoneIdAndDoId(zone, hqDoorInt2.getDoId())

        hqInterior = DistributedHQInteriorAI(self.air)
        hqInterior.setZoneIdAndBlock(zone, 0)
        hqInterior.generateWithRequired(zone)

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
