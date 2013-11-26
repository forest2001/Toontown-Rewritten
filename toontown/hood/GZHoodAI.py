from toontown.hood import HoodAI
from toontown.dna.DNAParser import DNAData
from toontown.toonbase import ToontownGlobals

class GZHoodAI(HoodAI):
    HOOD = ToontownGlobals.GolfZone
    
    def __init__(self, air):
        HoodAI.HoodAI.__init(self, air)
        
        self.dnaData = DNAData('gz_data')
        self.dnaData.read(open('resources/phase_6/dna/golf_zone.dna'))
        
    def createSafeZone():
        #self.createObjects(dnaData)
        pass
