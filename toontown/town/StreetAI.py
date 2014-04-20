from toontown.suit.DistributedSuitPlannerAI import DistributedSuitPlannerAI
from toontown.building.DistributedBuildingMgrAI import DistributedBuildingMgrAI

class StreetAI:
    """
    AI-side representation of everything in a single street.

    One subclass of this class exists for every neighborhood in the game.
    StreetAIs are responsible for spawning all SuitPlanners,ponds, and other
    street objects, etc.
    """
    
    def __init__(self, air, zoneId):
        self.air = air
        self.zoneId = zoneId
        
        self.air.dnaStoreMap[self.zoneId] = self.air.loadDNA(self.air.genDNAFileName(self.zoneId)).generateData()
        self.spawnObjects()

    def spawnObjects(self):
        filename = self.air.genDNAFileName(self.zoneId)
        self.air.dnaSpawner.spawnObjects(filename, self.zoneId)
        self.buildingMgr = DistributedBuildingMgrAI(self.air, self.zoneId, self.air.dnaStoreMap[self.zoneId], self.air.trophyMgr)
        self.sp = DistributedSuitPlannerAI(self.air, self.zoneId)
        self.sp.generateWithRequired(self.zoneId)
        self.sp.d_setZoneId(self.zoneId)
        self.sp.initTasks()
