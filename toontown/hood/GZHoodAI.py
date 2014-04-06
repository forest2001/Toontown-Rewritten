from toontown.hood.HoodAI import *
from toontown.toonbase import ToontownGlobals
from toontown.safezone.DistributedGolfKartAI import DistributedGolfKartAI
from toontown.golf import GolfGlobals

class GZHoodAI(HoodAI):
    HOOD = ToontownGlobals.GolfZone
    
    def __init__(self, air):
        HoodAI.__init__(self, air)
        
        self.golfKarts = []
        
    def createSafeZone(self):
        self.spawnObjects()
