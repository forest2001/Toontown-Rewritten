from toontown.toonbase import ToontownGlobals
from HoodAI import HoodAI
from toontown.building.DistributedBuildingMgrAI import DistributedBuildingMgrAI
from toontown.safezone.DistributedTrolleyAI import DistributedTrolleyAI
from toontown.building.DistributedDoorAI import DistributedDoorAI
from toontown.building.DistributedHQInteriorAI import DistributedHQInteriorAI
from toontown.safezone import TreasureGlobals
from toontown.town.StreetAI import StreetAI
from toontown.safezone.SZTreasurePlannerAI import SZTreasurePlannerAI
from toontown.toon import NPCToons

class SZHoodAI(HoodAI):
    """
    AI-side representation of everything in a single safezone neighborhood.

    One subclass of this class exists for every neighborhood in the game.
    HoodAIs are responsible for spawning all TreasurePlanners, ponds, 
    and other hood objects, etc.
    """
    
    def __init__(self, air):
        HoodAI.__init__(self, air)

        self.safezone = self.HOOD
        self.streets = {}
        
        self.trolley = None
        self.pond = None
        self.buildingMgr = None

        self.createZone()
        self.createStreets()

    def createZone(self):
        HoodAI.createZone(self)
        self.air.dnaStoreMap[self.HOOD] = self.air.loadDNA(self.air.genDNAFileName(self.HOOD)).generateData()
        self.createTrolley()
        self.createTreasurePlanner()
        self.buildingMgr = DistributedBuildingMgrAI(self.air, self.HOOD, self.air.dnaStoreMap[self.HOOD], self.air.trophyMgr)
        NPCToons.createNpcsInZone(self.air, self.HOOD)

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
        filename = self.air.genDNAFileName(self.safezone)
        self.air.dnaSpawner.spawnObjects(filename, self.safezone)
