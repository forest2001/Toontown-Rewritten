from StreetAI import StreetAI
from toontown.toonbase import ToontownGlobals

class MMStreetAI(StreetAI):
    def __init__(self, air, zoneId):
        StreetAI.__init__(self, air, zoneId)
        self.spawnObjects('phase_6/dna/minnies_melody_land_%i.dna' % zoneId)
