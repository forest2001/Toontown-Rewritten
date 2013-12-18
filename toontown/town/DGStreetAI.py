from StreetAI import StreetAI
from toontown.toonbase import ToontownGlobals

class DGStreetAI(StreetAI):
    def __init__(self, air, zoneId):
        StreetAI.__init__(self, air, zoneId)
        self.spawnObjects('phase_8/dna/daisys_garden_%i.dna' % zoneId)
