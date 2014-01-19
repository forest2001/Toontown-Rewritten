from toontown.hood import HoodAI
from toontown.dna.DNAParser import DNAData
from toontown.racing.DistributedRacePadAI import DistributedRacePadAI
from toontown.racing.DistributedViewPadAI import DistributedViewPadAI
from toontown.racing.DistributedStartingBlockAI import DistributedStartingBlockAI, DistributedViewingBlockAI
from toontown.building.DistributedDoorAI import DistributedDoorAI
from toontown.building.DistributedKartShopInteriorAI import DistributedKartShopInteriorAI
from toontown.toon import NPCToons
from toontown.building import DoorTypes
from toontown.racing import RaceGlobals
from otp.ai.MagicWordGlobal import *

class GSHoodAI(HoodAI.HoodAI):
    HOOD = 8000

    def __init__(self, air):
        HoodAI.HoodAI.__init__(self, air)
        self.racepads = []
        self.viewpads = []
        
    def createSafeZone(self):
        self.spawnObjects()
