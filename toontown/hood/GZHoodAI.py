from toontown.hood.HoodAI import *
from toontown.dna.DNAParser import DNAData
from toontown.toonbase import ToontownGlobals
from toontown.safezone.DistributedGolfKartAI import DistributedGolfKartAI
from toontown.golf import GolfGlobals

class GZHoodAI(HoodAI):
    HOOD = ToontownGlobals.GolfZone
    
    def __init__(self, air):
        HoodAI.__init__(self, air)
        
        self.golfKarts = []
        
    def createSafeZone(self):
        return False # Golf is currently broken. :)
        HoodAI.spawnObjects(self, 'phase_6/dna/golf_zone_sz.dna')
        
    def createObjects(self, group):
        if group.getName()[:9] == 'golf_kart':
            index, dest = group.getName()[10:].split('_', 2)
            try:
                index = int(index)
            except: #incase something goes wrong.. better safe than sorry.
                index = 1
            
            kart = DistributedGolfKartAI(self.air)
            kart.setGolfZone(self.HOOD)
            kart.nameType = dest
            kart.index = index
            kart.setGolfCourse(1)
            for i in range(group.getNumChildren()):
                posSpot = group.at(i)
                if posSpot.getName()[:14] == 'starting_block':
                    spotIndex = int(posSpot.getName()[15:])
                    x, y, z = posSpot.getPos()
                    h, p, r = posSpot.getHpr()
                    kart.setPosHpr(x, y, z, h, p, r)
                    kart.setColor(GolfGlobals.KartColors[index][0][1], GolfGlobals.KartColors[index][1][1], GolfGlobals.KartColors[index][2][1])
                    kart.generateWithRequired(self.HOOD)
                    self.golfKarts.append(kart)
        for i in range(group.getNumChildren()):
            self.createObjects(group.at(i)) #hmm
