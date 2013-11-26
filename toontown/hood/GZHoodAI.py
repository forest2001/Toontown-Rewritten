from toontown.hood.HoodAI import *
from toontown.dna.DNAParser import DNAData
from toontown.toonbase import ToontownGlobals

class GZHoodAI(HoodAI):
    HOOD = ToontownGlobals.GolfZone
    
    def __init__(self, air):
        HoodAI.__init__(self, air)
        
        self.dnaData = DNAData('gz_data')
        self.dnaData.read(open('resources/phase_6/dna/golf_zone_sz.dna'))
        
    def createSafeZone(self):
        #self.createObjects(dnaData)
        pass
