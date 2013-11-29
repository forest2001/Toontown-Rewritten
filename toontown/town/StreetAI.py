from toontown.dna.DNAParser import DNAVisGroup
from toontown.fishing.DistributedFishingPondAI import DistributedFishingPondAI
from toontown.safezone.DistributedFishingSpotAI import DistributedFishingSpotAI
from toontown.fishing.DistributedFishingTargetAI import DistributedFishingTargetAI
from toontown.fishing.DistributedPondBingoManagerAI import DistributedPondBingoManagerAI
from toontown.fishing import FishingTargetGlobals
from toontown.toon import NPCToons

class StreetAI:
    """
    AI-side representation of everything in a single street.

    One subclass of this class exists for every neighborhood in the game.
    StreetAIs are responsible for spawning all SuitPlanners,ponds, and other
    street objects, etc.
    """
    
    def __init__(self, air, zoneId):
        self.air = air
        self.zoneId = zoneId
        self.ponds = {}
        self.pondNpcs = {}
    
    def createObjects(self, group):
        if group.getName()[:13] == 'fishing_pond_':
            visGroup = group.getVisGroup()
            pondZone = 0
            if visGroup is None:
                pondZone = self.zoneId
            else:
                pondZone = int(visGroup.getName())

            pondIndex = int(group.getName()[13:])
            pond = DistributedFishingPondAI(self.air)
            pond.setArea(self.zoneId)
            pond.generateWithRequired(pondZone)
            self.ponds[pondIndex] = pond
            
            bingoManager = DistributedPondBingoManagerAI(self.air)
            bingoManager.setPondDoId(pond.getDoId())
            bingoManager.generateWithRequired(pondZone)
            #temporary, until we have scheduled stuff
            bingoManager.createGame()
            pond.bingoMgr = bingoManager
            self.air.fishManager.ponds[self.zoneId] = pond

            for i in range(FishingTargetGlobals.getNumTargets(self.zoneId)):
                target = DistributedFishingTargetAI(self.air)
                target.setPondDoId(pond.getDoId())
                target.generateWithRequired(pondZone)

            for i in range(group.getNumChildren()):
                posSpot = group.at(i)
                if posSpot.getName()[:13] == 'fishing_spot_':
                    spot = DistributedFishingSpotAI(self.air)
                    spot.setPondDoId(pond.getDoId())
                    x, y, z = posSpot.getPos()
                    h, p, r = posSpot.getHpr()
                    spot.setPosHpr(x, y, z, h, p, r)
                    spot.generateWithRequired(pondZone)
                elif posSpot.getName()[:21] == 'npc_fisherman_origin_':
                    NPCToons.createNPC(self.air, self.pondNpcs[self.zoneId], NPCToons.NPCToonDict.get(self.pondNpcs[self.zoneId]), pondZone, posIndex=int(posSpot.getName()[21:]))
            return
        for i in range(group.getNumChildren()):
            self.createObjects(group.at(i))