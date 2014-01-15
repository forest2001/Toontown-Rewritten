from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from toontown.ai.DatabaseObject import DatabaseObject
from toontown.estate.DistributedEstateAI import DistributedEstateAI
from toontown.estate.DistributedHouseAI import DistributedHouseAI
from toontown.estate.DistributedHouseInteriorAI import DistributedHouseInteriorAI
from toontown.estate.DistributedHouseDoorAI import DistributedHouseDoorAI
from toontown.building import DoorTypes


class EstateManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("EstateManagerAI")
    
    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.air = air
        self.estateZones = {}

    def startAprilFools(self):
        pass

    def stopAprilFools(self):
        pass

    def getEstateZone(self, avId, name):
        self.setEstateZone(avId, name)

    def setEstateZone(self, avId, name):
        if not avId in self.estateZones:
            self.estateZones[avId] = self.air.allocateZone()
            self.__loadEstate(avId)
        self.sendUpdateToAvatarId(avId, 'setEstateZone', [avId, self.estateZones[avId]])
                    
    def __loadEstate(self, avId):
        estate = DistributedEstateAI(self.air)
        estate.generateWithRequired(self.estateZones[avId])
        for i in range(6):
            house = DistributedHouseAI(self.air)
            house.setName('Hawkheart') #best name
            house.setAvatarId(0) # :D
            house.setHousePos(i)
            house.setColor(i)
            house.setHouseType(1)
            house.generateWithRequired(self.estateZones[avId])
            
            interiorZone = self.air.allocateZone()
            
            door = DistributedHouseDoorAI(simbase.air)
            door.setZoneIdAndBlock(self.estateZones[avId], house.getDoId())
            door.setDoorType(DoorTypes.EXT_STANDARD)
            door.setSwing(3)
            door.generateWithRequired(self.estateZones[avId])

            interiorDoor = DistributedHouseDoorAI(simbase.air)
            interiorDoor.setZoneIdAndBlock(interiorZone, house.getDoId())
            interiorDoor.setSwing(3)
            interiorDoor.setDoorType(DoorTypes.INT_STANDARD)
            interiorDoor.setOtherZoneIdAndDoId(self.estateZones[avId], door.getDoId())
            interiorDoor.generateWithRequired(interiorZone)


            door.setOtherZoneIdAndDoId(interiorZone, interiorDoor.getDoId())
            
            interior = DistributedHouseInteriorAI(self.air)
            interior.setHouseIndex(i)
            interior.setHouseId(house.getDoId())
            interior.generateWithRequired(interiorZone)

    def setAvHouseId(self, todo0, todo1):
        pass

    def sendAvToPlayground(self, todo0, todo1):
        pass

    def exitEstate(self):
        avId = self.air.getAvatarIdFromSender()
        self.air.deallocateZone(self.estateZones[avId])
        del self.estateZones[avId]

    def removeFriend(self, todo0, todo1):
        pass

