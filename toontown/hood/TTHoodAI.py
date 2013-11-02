from toontown.toonbase import ToontownGlobals
from toontown.safezone.DistributedFishingSpotAI import DistributedFishingSpotAI
from toontown.toon import NPCToons
from HoodAI import HoodAI

class TTHoodAI(HoodAI):
    SAFEZONE = ToontownGlobals.ToontownCentral

    def __init__(self, air):
        HoodAI.__init__(self, air)

        self.createTrolley()

        #this is messier than it needs to be
        self.createPond()
        self.createSpot(-63.5335, 41.648, -3.36708, 120, 0, 0)
        self.createSpot(-90.2253, 42.5202, -3.3105, -135, 0, 0)
        self.createSpot( -94.9218, 31.4153, -3.20083, -105, 0, 0)
        self.createSpot(-77.5199, 46.9817, -3.28456, -180, 0, 0)

        # Create Fisherman Freddy:
        NPCToons.createNPC(air, 2012, NPCToons.NPCToonDict.get(2012), 2000, posIndex=0)
