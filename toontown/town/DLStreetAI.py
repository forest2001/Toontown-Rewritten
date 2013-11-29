from StreetAI import StreetAI
from toontown.toonbase import ToontownGlobals
from toontown.dna.DNAParser import DNAStorage

class DLStreetAI(StreetAI):
    def __init__(self, air, zoneId):
        StreetAI.__init__(self, air, zoneId)
        self.dnaStore = DNAStorage()
        self.dnaData = simbase.air.loadDNAFileAI(self.dnaStore, 'phase_8/dna/donalds_dreamland_%i.dna' % self.zoneId)
        self.pondNpcs = {ToontownGlobals.PajamaPlace: 9237, ToontownGlobals.LullabyLane: 9136}
        self.createObjects(self.dnaData)