from StreetAI import StreetAI
from toontown.toonbase import ToontownGlobals

class DDStreetAI(StreetAI):
    def __init__(self, air, zoneId):
        StreetAI.__init__(self, air, zoneId)
        self.spawnObjects('phase_6/dna/donalds_dock_%i.dna' % zoneId)
