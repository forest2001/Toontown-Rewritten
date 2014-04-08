from toontown.suit.DistributedSuitPlannerAI import DistributedSuitPlannerAI

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
        
        self.sp = DistributedSuitPlannerAI(self.air, self.zoneId)
        self.sp.generateWithRequired(self.zoneId)
        self.sp.d_setZoneId(self.zoneId)
        self.sp.initTasks()

        self.spawnObjects()
    
    def spawnObjects(self):
        filename = self.air.genDNAFileName(self.zoneId)

        self.air.dnaSpawner.spawnObjects(filename, self.zoneId)
