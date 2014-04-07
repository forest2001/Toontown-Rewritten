from toontown.toonbase import ToontownGlobals
from toontown.safezone.DistributedTrolleyAI import DistributedTrolleyAI
from toontown.building.DistributedDoorAI import DistributedDoorAI
from toontown.building.DistributedHQInteriorAI import DistributedHQInteriorAI
from toontown.safezone import TreasureGlobals
from toontown.town.StreetAI import StreetAI
from toontown.safezone.SZTreasurePlannerAI import SZTreasurePlannerAI

#from toontown.dna.DNASpawnerAI import DNASpawnerAI

class HoodAI:
    """
    AI-side representation of everything in a single neighborhood.

    One subclass of this class exists for every neighborhood in the game.
    HoodAIs are responsible for spawning all TreasurePlanners, SuitPlanners,
    ponds, and other safezone objects, etc.
    """

    HOOD = None

    def __init__(self, air):
        self.air = air
        
        self.spawnNpcsIn = [2000]

        self.safezone = self.HOOD
        self.streets = {}
        
        self.trolley = None
        self.pond = None

        self.createSafeZone()
        self.createStreets()

    def createSafeZone(self):
        self.createTrolley()
        self.createTreasurePlanner()

    def createStreets(self):
        branchIds = ToontownGlobals.HoodHierarchy.get(self.HOOD, [])
        for branch in branchIds:
            street = StreetAI(self.air, branch)
            self.streets[branch] = street

    def createTrolley(self):
        self.trolley = DistributedTrolleyAI(self.air)
        self.trolley.generateWithRequired(self.safezone)

    def createTreasurePlanner(self):
        treasureType, healAmount, spawnPoints, spawnRate, maxTreasures = TreasureGlobals.SafeZoneTreasureSpawns[self.HOOD]
        self.treasurePlanner = SZTreasurePlannerAI(self.safezone, treasureType, healAmount, spawnPoints, spawnRate, maxTreasures)
        self.treasurePlanner.start()

    def spawnObjects(self):
        return
        filename = self.air.genDNAFileName(self.safezone)

        DNASpawnerAI().spawnObjects(filename, self.safezone)
