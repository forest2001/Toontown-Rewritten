from DNAParser import DNAVisGroup, DNALandmarkBuilding, DNAStorage

from toontown.building.DistributedToonInteriorAI import DistributedToonInteriorAI
from toontown.building.DistributedDoorAI import DistributedDoorAI
from toontown.building.DistributedHQInteriorAI import DistributedHQInteriorAI
from toontown.building.DistributedPetshopInteriorAI import DistributedPetshopInteriorAI
from toontown.building.DistributedGagshopInteriorAI import DistributedGagshopInteriorAI
from toontown.building.DistributedKartShopInteriorAI import DistributedKartShopInteriorAI
from toontown.building import DoorTypes

from toontown.racing.DistributedRacePadAI import DistributedRacePadAI
from toontown.racing.DistributedViewPadAI import DistributedViewPadAI
from toontown.racing.DistributedStartingBlockAI import DistributedStartingBlockAI, DistributedViewingBlockAI
from toontown.racing import RaceGlobals


from toontown.fishing.DistributedFishingPondAI import DistributedFishingPondAI
from toontown.fishing.DistributedFishingTargetAI import DistributedFishingTargetAI
from toontown.fishing.DistributedPondBingoManagerAI import DistributedPondBingoManagerAI

from toontown.fishing import FishingTargetGlobals

from toontown.safezone.DistributedFishingSpotAI import DistributedFishingSpotAI

from toontown.toon import NPCToons

#alfa only
from toontown.hood import ZoneUtil

class DNASpawnerAI:
        
    def spawnObjects(self, filename, baseZone):
        # This is strictly for buildings during alpha release
        self.spawnInteriorsIn = [1000, 2000, 3000 8000] # 8000 = GSW... and kart shop was already open ;D
        self.spawnNPCsIn = [1000, 2000] # GSW works differently to normal buildings.
        
        dnaStore = DNAStorage()
        dnaData = simbase.air.loadDNAFileAI(dnaStore, filename)
        self._createObjects(dnaData, baseZone)
        
    def _createObjects(self, group, zone):
        if group.getName()[:12] == 'fishing_pond':
            visGroup = group.getVisGroup()
            pondZone = 0
            if visGroup is None:
                pondZone = zone
            else:
                pondZone = int(visGroup.getName().split(':')[0])
            pond = DistributedFishingPondAI(simbase.air)
            pond.setArea(pondZone)
            pond.generateWithRequired(pondZone)
            for i in range(group.getNumChildren()):
                posSpot = group.at(i)
                if posSpot.getName()[:12] == 'fishing_spot':
                    x, y, z = posSpot.getPos()
                    h, p, r = posSpot.getHpr()
                    spot = DistributedFishingSpotAI(simbase.air)
                    spot.setPondDoId(pond.getDoId())
                    spot.setPosHpr(x, y, z, h, p, r)
                    spot.generateWithRequired(pondZone)
            bingoManager = DistributedPondBingoManagerAI(simbase.air)
            bingoManager.setPondDoId(pond.getDoId())
            bingoManager.generateWithRequired(pondZone)
            #temporary, until we have scheduled stuff
            bingoManager.createGame()   
            pond.bingoMgr = bingoManager
            simbase.air.fishManager.ponds[pondZone] = pond
            for i in range(FishingTargetGlobals.getNumTargets(pondZone)):
                target = DistributedFishingTargetAI(simbase.air)
                target.setPondDoId(pond.getDoId())
                target.generateWithRequired(pondZone)
            NPCToons.createNpcsInZone(simbase.air, pondZone)
        
        elif isinstance(group, DNALandmarkBuilding) and ZoneUtil.getCanonicalHoodId(zone) in self.spawnInteriorsIn:
            if group.getName()[:2] == 'tb' or group.getName()[:2] == 'sz':
                visGroup = group.getVisGroup()
                buildingZone = 0
                if visGroup is None:
                    buildingZone = zone
                else:
                    buildingZone = int(visGroup.getName().split(':')[0])
                index = int(group.getName()[2:].split(':')[0])
                interiorZone = zone + 500 + index
                type = group.getBuildingType()
                if type == 'hq':
                    hqDoor = DistributedDoorAI(simbase.air)
                    hqDoor.setZoneIdAndBlock(buildingZone, index)
                    hqDoor.setDoorType(DoorTypes.EXT_HQ)
                    hqDoor.setSwing(3)
                    hqDoor.generateWithRequired(buildingZone)
                    
                    hqDoor2 = DistributedDoorAI(simbase.air)
                    hqDoor2.setZoneIdAndBlock(buildingZone, index)
                    hqDoor2.setDoorType(DoorTypes.EXT_HQ)
                    hqDoor2.setSwing(3)
                    hqDoor2.setDoorIndex(1)
                    hqDoor2.generateWithRequired(buildingZone)

                    hqDoorInt = DistributedDoorAI(simbase.air)
                    hqDoorInt.setZoneIdAndBlock(interiorZone, 0)
                    hqDoorInt.setSwing(3)
                    hqDoorInt.setDoorType(DoorTypes.INT_HQ)
                    hqDoorInt.setOtherZoneIdAndDoId(buildingZone, hqDoor.getDoId())
                    hqDoorInt.generateWithRequired(interiorZone)

                    hqDoorInt2 = DistributedDoorAI(simbase.air)
                    hqDoorInt2.setZoneIdAndBlock(interiorZone, 0)
                    hqDoorInt2.setSwing(3)
                    hqDoorInt2.setDoorType(DoorTypes.INT_HQ)
                    hqDoorInt2.setOtherZoneIdAndDoId(buildingZone, hqDoor2.getDoId())
                    hqDoorInt2.setDoorIndex(1)
                    hqDoorInt2.generateWithRequired(interiorZone)

                    hqDoor.setOtherZoneIdAndDoId(interiorZone, hqDoorInt.getDoId())
                    hqDoor2.setOtherZoneIdAndDoId(interiorZone, hqDoorInt2.getDoId())

                    hqInterior = DistributedHQInteriorAI(simbase.air)
                    hqInterior.setZoneIdAndBlock(interiorZone, index)
                    hqInterior.generateWithRequired(interiorZone)
                elif type == 'kartshop':
                    ksInterior = DistributedKartShopInteriorAI(simbase.air)
                    ksInterior.setZoneIdAndBlock(interiorZone, 0)
                    ksInterior.generateWithRequired(interiorZone)
                
                    ksDoor = DistributedDoorAI(simbase.air)
                    ksDoor.setZoneIdAndBlock(buildingZone, 1)
                    ksDoor.setDoorType(DoorTypes.EXT_KS)
                    ksDoor.setSwing(3)
                    ksDoor.setDoorIndex(1)
                    ksDoor.generateWithRequired(buildingZone)
                    
                    ksDoor2 = DistributedDoorAI(simbase.air)
                    ksDoor2.setZoneIdAndBlock(buildingZone, 1)
                    ksDoor2.setDoorType(DoorTypes.EXT_KS)
                    ksDoor2.setSwing(3)
                    ksDoor2.setDoorIndex(2)
                    ksDoor2.generateWithRequired(buildingZone)
                    
                    ksDoorInt = DistributedDoorAI(simbase.air)
                    ksDoorInt.setZoneIdAndBlock(interiorZone, 0)
                    ksDoorInt.setSwing(3)
                    ksDoorInt.setDoorType(DoorTypes.INT_KS)
                    ksDoorInt.setDoorIndex(1)
                    ksDoorInt.setOtherZoneIdAndDoId(buildingZone, ksDoor.getDoId())
                    ksDoorInt.generateWithRequired(interiorZone)

                    ksDoorInt2 = DistributedDoorAI(simbase.air)
                    ksDoorInt2.setZoneIdAndBlock(interiorZone, 0)
                    ksDoorInt2.setSwing(3)
                    ksDoorInt2.setDoorType(DoorTypes.INT_KS)
                    ksDoorInt2.setOtherZoneIdAndDoId(buildingZone, ksDoor2.getDoId())
                    ksDoorInt2.setDoorIndex(2)
                    ksDoorInt2.generateWithRequired(interiorZone)
                    
                    ksDoor.setOtherZoneIdAndDoId(interiorZone, ksDoorInt.getDoId())
                    ksDoor2.setOtherZoneIdAndDoId(interiorZone, ksDoorInt2.getDoId())
                    
                    NPCToons.createNpcsInZone(simbase.air, interiorZone)
                elif type == 'clotheshop':
                    pass
                elif type == 'petshop':
                    interior = DistributedPetshopInteriorAI(simbase.air)
                    interior.setZoneIdAndBlock(interiorZone, 0)
                    interior.generateWithRequired(interiorZone)
                    
                    extDoor = DistributedDoorAI(simbase.air)
                    extDoor.setZoneIdAndBlock(buildingZone, index)
                    extDoor.setDoorType(DoorTypes.EXT_STANDARD)
                    extDoor.setSwing(3)
                    extDoor.setDoorIndex(1)
                    extDoor.generateWithRequired(buildingZone)
                    
                    intDoor = DistributedDoorAI(simbase.air)
                    intDoor.setZoneIdAndBlock(interiorZone, index)
                    intDoor.setDoorType(DoorTypes.INT_STANDARD)
                    intDoor.setSwing(3)
                    intDoor.setDoorIndex(0)
                    intDoor.setOtherZoneIdAndDoId(buildingZone, extDoor.getDoId())
                    intDoor.generateWithRequired(interiorZone)
                    
                    extDoor.setOtherZoneIdAndDoId(interiorZone, intDoor.getDoId())
                    
                    NPCToons.createNpcsInZone(simbase.air, interiorZone)

                elif type == 'gagshop':
                    interior = DistributedGagshopInteriorAI(simbase.air)
                    interior.setZoneIdAndBlock(interiorZone, 0)
                    interior.generateWithRequired(interiorZone)
                    
                    extDoor = DistributedDoorAI(simbase.air)
                    extDoor.setZoneIdAndBlock(buildingZone, index)
                    extDoor.setDoorType(DoorTypes.EXT_STANDARD)
                    extDoor.setSwing(3)
                    extDoor.setDoorIndex(1)
                    extDoor.generateWithRequired(buildingZone)
                    
                    intDoor = DistributedDoorAI(simbase.air)
                    intDoor.setZoneIdAndBlock(interiorZone, 0)
                    intDoor.setDoorType(DoorTypes.INT_STANDARD)
                    intDoor.setSwing(3)
                    intDoor.setDoorIndex(0)
                    intDoor.setOtherZoneIdAndDoId(buildingZone, extDoor.getDoId())
                    intDoor.generateWithRequired(interiorZone)
                    
                    extDoor.setOtherZoneIdAndDoId(interiorZone, intDoor.getDoId())
                    
                    NPCToons.createNpcsInZone(simbase.air, interiorZone)
                else:
                    if group.getName() == 'sz13:toon_landmark_TT_toonhall_DNARoot':
                        pass # We don't want Toon Hall just yet.
                    else:
                        interior = DistributedToonInteriorAI(simbase.air)
                        interior.setZoneIdAndBlock(interiorZone, 0)
                        interior.setState('toon')
                        interior.generateWithRequired(interiorZone)
                        
                        extDoor = DistributedDoorAI(simbase.air)
                        extDoor.setZoneIdAndBlock(buildingZone, index)
                        extDoor.setDoorType(DoorTypes.EXT_STANDARD)
                        extDoor.setSwing(3)
                        extDoor.setDoorIndex(1)
                        extDoor.generateWithRequired(buildingZone)
                        
                        intDoor = DistributedDoorAI(simbase.air)
                        intDoor.setZoneIdAndBlock(interiorZone, 0)
                        intDoor.setDoorType(DoorTypes.INT_STANDARD)
                        intDoor.setSwing(3)
                        intDoor.setDoorIndex(0)
                        intDoor.setOtherZoneIdAndDoId(zone, extDoor.getDoId())
                        intDoor.generateWithRequired(interiorZone)
                        
                        extDoor.setOtherZoneIdAndDoId(interiorZone, intDoor.getDoId())
                        
                        if ZoneUtil.getCanonicalHoodId(zone) in self.spawnNPCsIn:
                            NPCToons.createNpcsInZone(simbase.air, interiorZone)
        
        elif group.getName()[:10] == 'racing_pad':
            index, dest = group.getName()[11:].split('_', 2)
            index = int(index)
            
            pad = DistributedRacePadAI(simbase.air)
            pad.setArea(zone)
            pad.nameType = dest
            pad.index = index
            nri = RaceGlobals.getNextRaceInfo(-1, dest, index)
            pad.setTrackInfo([nri[0], nri[1]])
            pad.generateWithRequired(zone)
            for i in range(group.getNumChildren()):
                posSpot = group.at(i)
                if posSpot.getName()[:14] == 'starting_block':
                    spotIndex = int(posSpot.getName()[15:])
                    x, y, z = posSpot.getPos()
                    h, p, r = posSpot.getHpr()
                    startingBlock = DistributedStartingBlockAI(simbase.air)
                    startingBlock.setPosHpr(x, y, z, h, p, r)
                    startingBlock.setPadDoId(pad.getDoId())
                    startingBlock.setPadLocationId(index)
                    startingBlock.generateWithRequired(zone)
                    pad.addStartingBlock(startingBlock)
        elif group.getName()[:11] == 'viewing_pad':
            pad = DistributedViewPadAI(simbase.air)
            pad.setArea(zone)
            pad.generateWithRequired(zone)
            for i in range(group.getNumChildren()):
                posSpot = group.at(i)
                if posSpot.getName()[:14] == 'starting_block':
                    spotIndex = int(posSpot.getName()[15:])
                    x, y, z = posSpot.getPos()
                    h, p, r = posSpot.getHpr()
                    startingBlock = DistributedViewingBlockAI(simbase.air)
                    startingBlock.setPosHpr(x, y, z, h, p, r)
                    startingBlock.setPadDoId(pad.getDoId())
                    startingBlock.setPadLocationId(0)
                    startingBlock.generateWithRequired(zone)
                    pad.addStartingBlock(startingBlock)
        for i in range(group.getNumChildren()):
            self._createObjects(group.at(i), zone)
