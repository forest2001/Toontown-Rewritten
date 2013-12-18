from toontown.dna.DNASpawnerAI import DNASpawnerAI

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
    
    def spawnObjects(self, filename):
        DNASpawnerAI().spawnObjects(filename, self.zoneId)
