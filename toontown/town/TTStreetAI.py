from StreetAI import StreetAI
from toontown.toonbase import ToontownGlobals

class TTStreetAI(StreetAI):
    def __init__(self, air, zoneId):
        StreetAI.__init__(self, air, zoneId)
        self.spawnObjects('phase_5/dna/toontown_central_%i.dna' % zoneId)
