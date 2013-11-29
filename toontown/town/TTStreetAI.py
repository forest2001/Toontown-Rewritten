from StreetAI import StreetAI
from toontown.toonbase import ToontownGlobals
from toontown.dna.DNAParser import DNAStorage

class TTStreetAI(StreetAI):
    def __init__(self, air, zoneId):
        StreetAI.__init__(self, air, zoneId)
        self.dnaStore = DNAStorage()
        self.dnaData = simbase.air.loadDNAFileAI(self.dnaStore, 'phase_5/dna/toontown_central_%i.dna' % self.zoneId)
        self.pondNpcs = {ToontownGlobals.SillyStreet: 2140, ToontownGlobals.LoopyLane: 2225, ToontownGlobals.PunchlinePlace: 2321}
        self.createObjects(self.dnaData)