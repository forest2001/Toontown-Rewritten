from StreetAI import StreetAI
from toontown.toonbase import ToontownGlobals
from toontown.dna.DNAParser import DNAStorage

class MMStreetAI(StreetAI):
    def __init__(self, air, zoneId):
        StreetAI.__init__(self, air, zoneId)
        self.dnaStore = DNAStorage()
        self.dnaData = simbase.air.loadDNAFileAI(self.dnaStore, 'phase_6/dna/minnies_melody_land_%i.dna' % self.zoneId)
        self.pondNpcs = {ToontownGlobals.AltoAvenue: 4141, ToontownGlobals.BaritoneBoulevard: 4235, ToontownGlobals.TenorTerrace: 4335}
        self.createObjects(self.dnaData)