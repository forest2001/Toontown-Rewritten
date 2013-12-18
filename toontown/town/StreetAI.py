from toontown.dna.DNAParser import DNAVisGroup, DNALandmarkBuilding
from toontown.fishing.DistributedFishingPondAI import DistributedFishingPondAI
from toontown.safezone.DistributedFishingSpotAI import DistributedFishingSpotAI
from toontown.fishing.DistributedFishingTargetAI import DistributedFishingTargetAI
from toontown.fishing.DistributedPondBingoManagerAI import DistributedPondBingoManagerAI
from toontown.building.DistributedToonInteriorAI import DistributedToonInteriorAI
from toontown.building.DistributedHQInteriorAI import DistributedHQInteriorAI
from toontown.fishing import FishingTargetGlobals
from toontown.building import DoorTypes
from toontown.building.DistributedDoorAI import DistributedDoorAI
from toontown.toon import NPCToons
from toontown.hood import ZoneUtil

from toontown.dna.DNASpawnerAI import DNASpawnerAI

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
        self.spawnInteriorsIn = [1000, 2000, 5000]
        self.spawnNpcsIn = [1000, 2000]
    
    def spawnObjects(self, filename):
        DNASpawnerAI().spawnObjects(filename, self.zoneId)
    
    def createObjects(self, group):
        if isinstance(group, DNALandmarkBuilding):
            if group.getName()[:2] == 'tb' and ZoneUtil.getCanonicalHoodId(self.zoneId) in self.spawnInteriorsIn:
                visGroup = group.getVisGroup()
                buildingZone = 0
                if visGroup is None:
                    buildingZone = self.zoneId
                else:
                    buildingZone = int(visGroup.getName())
                index = int(group.getName()[2:].split(':')[0])
                interiorZone = self.zoneId + 500 + index
                type = group.getBuildingType()
                if type == 'hq':
                    pass
                else:                    
                    extDoor = DistributedDoorAI(self.air)
                    extDoor.setZoneIdAndBlock(buildingZone, index)
                    extDoor.setDoorType(DoorTypes.EXT_STANDARD)
                    extDoor.setSwing(3)
                    extDoor.setDoorIndex(1)
                    extDoor.generateWithRequired(buildingZone)
                    
                    intDoor = DistributedDoorAI(self.air)
                    intDoor.setZoneIdAndBlock(interiorZone, 0)
                    intDoor.setDoorType(DoorTypes.INT_STANDARD)
                    intDoor.setSwing(3)
                    intDoor.setDoorIndex(1)
                    intDoor.generateWithRequired(interiorZone)
                    
                    extDoor.setOtherZoneIdAndDoId(interiorZone, intDoor.getDoId())
                    intDoor.setOtherZoneIdAndDoId(buildingZone, extDoor.getDoId())
                    
                    interior = DistributedToonInteriorAI(self.air)
                    interior.setZoneIdAndBlock(interiorZone, 0)
                    interior.setState('toon')
                    interior.generateWithRequired(interiorZone)
                    
                    if ZoneUtil.getCanonicalHoodId(interiorZone) in self.spawnNpcsIn:
                        NPCToons.createNpcsInZone(self.air, interiorZone)

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
        for i in range(group.getNumChildren()):
            self.createObjects(group.at(i))