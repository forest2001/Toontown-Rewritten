from StreetAI import StreetAI
from toontown.toonbase import ToontownGlobals

class DLStreetAI(StreetAI):
    def __init__(self, air, zoneId):
        StreetAI.__init__(self, air, zoneId)
        self.spawnObjects('phase_8/dna/donalds_dreamland_%i.dna' % zoneId)
