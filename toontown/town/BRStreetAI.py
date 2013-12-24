from StreetAI import StreetAI
from toontown.toonbase import ToontownGlobals

class BRStreetAI(StreetAI):
    def __init__(self, air, zoneId):
        StreetAI.__init__(self, air, zoneId)
        self.spawnObjects('phase_8/dna/the_burrrgh_%i.dna' % zoneId)
