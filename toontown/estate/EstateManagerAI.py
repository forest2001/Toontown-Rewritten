from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from toontown.ai.DatabaseObject import DatabaseObject
from toontown.estate.DistributedEstateAI import DistributedEstateAI
from toontown.estate.DistributedHouseAI import DistributedHouseAI
from toontown.estate.DistributedHouseInteriorAI import DistributedHouseInteriorAI
from toontown.estate.DistributedHouseDoorAI import DistributedHouseDoorAI
from toontown.building import DoorTypes
import functools

class EstateManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("EstateManagerAI")
    
    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.air = air
        self.estateZones = {}
        self.otherToons = {}

    def startAprilFools(self):
        pass

    def stopAprilFools(self):
        pass

    def getEstateZone(self, avId, name):
        self.setEstateZone(avId, name)

    def setEstateZone(self, avId, name):
        if not avId in self.estateZones:
            self.estateZones[avId] = []
            self.estateZones[avId].append(self.air.allocateZone())
            self.__loadEstate(avId)
        self.sendUpdateToAvatarId(avId, 'setEstateZone', [avId, self.estateZones[avId][0]])
                    
    def __loadEstate(self, avId):
        estate = DistributedEstateAI(self.air)
        estate.generateWithRequired(self.estateZones[avId][0])
        
        def getAvIdName(dclass, fields, avIndex=0):
            name = fields['setName'][0]
            self.otherToons[avId][avIndex].append(name)
            createHouse(self.otherToons[avId][avIndex][0], name, avIndex)
        
        def getEstateHouseDetails(dclass, fields):
            self.otherToons[avId] = []
            for avIndex in enumerate(fields['ACCOUNT_AV_SET']):
                toonAvId = avIndex[1]
                self.otherToons[avId].append([ toonAvId ])
                if toonAvId != 0:
                    self.air.dbInterface.queryObject(self.air.dbId, toonAvId, functools.partial(getAvIdName, avIndex=avIndex[0]))
                else:
                    self.otherToons[avId][avIndex[0]].append('')
                    createHouse(0, '', avIndex[0])
                
        self.air.dbInterface.queryObject(self.air.dbId, self.air.doId2do[avId].DISLid, getEstateHouseDetails)
        
        def createHouse(avIdOfToon, name, avIndex):
            house = DistributedHouseAI(self.air)
            house.setName(name)
            house.setAvatarId(avIdOfToon)
            house.setHousePos(avIndex)
            house.setColor(avIndex)
            house.setHouseType(0)
            house.generateWithRequired(self.estateZones[avId][0])
            
            self.estateZones[avId].append(self.air.allocateZone())
            interiorZone = self.estateZones[avId][-1]
            
            door = DistributedHouseDoorAI(simbase.air)
            door.setZoneIdAndBlock(self.estateZones[avId][0], house.getDoId())
            door.setDoorType(DoorTypes.EXT_STANDARD)
            door.setSwing(3)
            door.generateWithRequired(self.estateZones[avId][0])

            interiorDoor = DistributedHouseDoorAI(simbase.air)
            interiorDoor.setZoneIdAndBlock(interiorZone, house.getDoId())
            interiorDoor.setSwing(3)
            interiorDoor.setDoorType(DoorTypes.INT_STANDARD)
            interiorDoor.setOtherZoneIdAndDoId(self.estateZones[avId][0], door.getDoId())
            interiorDoor.generateWithRequired(interiorZone)

            door.setOtherZoneIdAndDoId(interiorZone, interiorDoor.getDoId())
            
            interior = DistributedHouseInteriorAI(self.air)
            interior.setHouseIndex(avIndex)
            interior.setHouseId(house.getDoId())
            interior.generateWithRequired(interiorZone)

    def setAvHouseId(self, todo0, todo1):
        pass

    def sendAvToPlayground(self, todo0, todo1):
        pass

    def exitEstate(self):
        avId = self.air.getAvatarIdFromSender()
        for zoneId in self.estateZones[avId]:
            self.air.deallocateZone(zoneId)
            print "deallocated zoneId %d from %d" % ( zoneId, avId )
        del self.estateZones[avId]

    def removeFriend(self, todo0, todo1):
        pass

