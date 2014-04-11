from toontown.toonbase import ToontownGlobals
from HoodAI import HoodAI
from toontown.safezone import ButterflyGlobals
from toontown.safezone.DistributedButterflyAI import DistributedButterflyAI
from toontown.toon import NPCToons
from toontown.election.DistributedElectionEventAI import DistributedElectionEventAI
from toontown.building.HQBuildingAI import HQBuildingAI
from toontown.toon import NPCToons
from toontown.toonbase import TTLocalizer
from otp.ai.MagicWordGlobal import *

class TTHoodAI(HoodAI):
    HOOD = ToontownGlobals.ToontownCentral
    
    def createSafeZone(self):
        HoodAI.createSafeZone(self)
        self.spawnObjects()
        self.butterflies = []
        # TODO: Re-enable butterflies. RIP, you will be missed.
        #self.createButterflies()
        
        #beginhack disable election props
        #self.spawnElection()
        #endhack

        #TODO: in reality this should be done by the buildingMgr
        hqBlock = 20
        hqZone = self.HOOD - self.HOOD % 100 + 500 + hqBlock
        self.hqBuilding = HQBuildingAI(self.air, self.HOOD, hqZone, hqBlock)
        #beginhack NPC IN TTC
        self.npc = NPCToons.createNPC(self.air, 2001, NPCToons.NPCToonDict[2001], self.HOOD, 3)
        #endhack
    
    def spawnElection(self):
        event = self.air.doFind('ElectionEvent')
        if event is None:
            event = DistributedElectionEventAI(self.air)
            event.generateWithRequired(self.HOOD)
        event.b_setState('Intro')
    
    def createButterflies(self):
        playground = ButterflyGlobals.TTC
        for area in range(ButterflyGlobals.NUM_BUTTERFLY_AREAS[playground]):
            for b in range(ButterflyGlobals.NUM_BUTTERFLIES[playground]):
                butterfly = DistributedButterflyAI(self.air)
                butterfly.setArea(playground, area)
                butterfly.setState(0, 0, 0, 1, 1)
                butterfly.generateWithRequired(self.HOOD)
                self.butterflies.append(butterfly)

@magicWord(category=CATEGORY_OVERRIDE, types=[str])
def gibnpc(npcName):
    hood = simbase.air.hoods[0]
    npcId = 0
    for id, name in TTLocalizer.NPCToonNames.items():
        if npcName.lower() == name.lower():
            hood.npc.requestDelete()
            hood.npc = NPCToons.createNPC(simbase.air, id, NPCToons.NPCToonDict[id], hood.HOOD, 3)
            return "Found match {0}({1})".format(name, id)
    return "No match found"

@magicWord(category=CATEGORY_OVERRIDE, types=[int])
def gibnpcid(npcId):
    hood = simbase.air.hoods[0]
    hood.npc.requestDelete()
    hood.npc = NPCToons.createNPC(simbase.air, npcId, NPCToons.NPCToonDict[npcId], hood.HOOD, 3)
    return "swapped"

