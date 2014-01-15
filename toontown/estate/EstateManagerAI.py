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
        self.estateAvIdsAndNames = {}
        self.otherToons = []
        self.otherToonsNames = []

    def startAprilFools(self):
        pass

    def stopAprilFools(self):
        pass

    def getEstateZone(self, avId, name):
        self.setEstateZone(avId, name)

    def setEstateZone(self, avId, name):
        if not avId in self.estateZones:
            self.estateZones[avId] = []
            self.otherToons = []
            self.otherToonsNames = []
            self.estateZones[avId].append(self.air.allocateZone())
            self.__loadEstate(avId)
        self.sendUpdateToAvatarId(avId, 'setEstateZone', [avId, self.estateZones[avId][0]])
                    
    def __loadEstate(self, avId):
        estate = DistributedEstateAI(self.air)
        estate.generateWithRequired(self.estateZones[avId][0])
        
        def storeAvIdsAndNames2(dclass, fields):
            name = fields['setName'][0]
            self.otherToonsNames.append(name)
            index = len(self.otherToonsNames) - 1
            createHouse(self.otherToons[index], self.otherToonsNames[index])
            if index < 5:
                index += 1
                while self.otherToons[index] == 0:
                    print "created empty house!"
                    self.otherToonsNames.append('hack %d' % index)
                    createHouse(0, 'hack %d' % index)
                    if index < 5:
                        index += 1
                    else:
                        del self.otherToons
                        del self.otherToonsNames
                        for zoneId in self.estateZones[avId]:
                            print "allocated zoneId %d to %d" % ( zoneId, avId)
                        return
                self.air.dbInterface.queryObject(self.air.dbId, self.otherToons[index], storeAvIdsAndNames2)
            else:
                del self.otherToons
                del self.otherToonsNames
                for zoneId in self.estateZones[avId]:
                    print "allocated zoneId %d to %d" % ( zoneId, avId)
        
        def storeAvIdsAndNames(dclass, fields):
            self.otherToons = fields['ACCOUNT_AV_SET']
            index = 0
            while self.otherToons[index] == 0:
                print "created empty house!"
                self.otherToonsNames.append('hack %d' % index)
                createHouse(0, 'hack %d' % index)
                index += 1
            self.air.dbInterface.queryObject(self.air.dbId, self.otherToons[index], storeAvIdsAndNames2)
        self.air.dbInterface.queryObject(self.air.dbId, self.air.doId2do[avId].DISLid, storeAvIdsAndNames)
        
        def createHouse(avIdOfToon, name):
            house = DistributedHouseAI(self.air)
            house.setName(name) #best name
            house.setAvatarId(avIdOfToon) # :D
            house.setHousePos(self.otherToonsNames.index(name))
            house.setColor(self.otherToonsNames.index(name))
            house.setHouseType(0)
            house.generateWithRequired(self.estateZones[avId][0])
            
            self.estateZones[avId].append(self.air.allocateZone())
            interiorZone = self.estateZones[avId][self.otherToonsNames.index(name)+1]
            
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
            interior.setHouseIndex(self.otherToonsNames.index(name))
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

