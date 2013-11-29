from StreetAI import StreetAI
from toontown.toonbase import ToontownGlobals
from toontown.dna.DNAParser import DNAStorage

class DDStreetAI(StreetAI):
    def __init__(self, air, zoneId):
        StreetAI.__init__(self, air, zoneId)
        self.dnaStore = DNAStorage()
        self.dnaData = simbase.air.loadDNAFileAI(self.dnaStore, 'phase_6/dna/donalds_dock_%i.dna' % self.zoneId)
        self.pondNpcs = {ToontownGlobals.BarnacleBoulevard: 1126, ToontownGlobals.LighthouseLane: 1332, ToontownGlobals.SeaweedStreet: 1228}
        self.createObjects(self.dnaData)