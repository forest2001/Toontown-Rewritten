from StreetAI import StreetAI
from toontown.toonbase import ToontownGlobals
from toontown.dna.DNAParser import DNAStorage

class DGStreetAI(StreetAI):
    def __init__(self, air, zoneId):
        StreetAI.__init__(self, air, zoneId)
        self.dnaStore = DNAStorage()
        self.dnaData = simbase.air.loadDNAFileAI(self.dnaStore, 'phase_8/dna/daisys_garden_%i.dna' % self.zoneId)
        self.pondNpcs = {ToontownGlobals.ElmStreet: 5129, ToontownGlobals.MapleStreet: 5229, ToontownGlobals.OakStreet: 5322}
        self.createObjects(self.dnaData)