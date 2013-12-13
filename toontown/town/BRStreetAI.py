from StreetAI import StreetAI
from toontown.toonbase import ToontownGlobals
from toontown.dna.DNAParser import DNAStorage

class BRStreetAI(StreetAI):
    def __init__(self, air, zoneId):
        StreetAI.__init__(self, air, zoneId)
        self.dnaStore = DNAStorage()
        self.dnaData = simbase.air.loadDNAFileAI(self.dnaStore, 'phase_8/dna/the_burrrgh_%i.dna' % self.zoneId)
        self.pondNpcs = {ToontownGlobals.PolarPlace: 3307, ToontownGlobals.SleetStreet: 3232, ToontownGlobals.WalrusWay: 3140}
        self.createObjects(self.dnaData)