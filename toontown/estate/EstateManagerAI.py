# cfsworks, send help


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
        self.houseIds = {}
        
        self.defaultEstate = {
            'setEstateType' : [0],
            'setDecorData' : [[]],
            'setLastEpochTimeStamp' : [0],
            'setRentalTimeStamp' : [0],
            'setRentalType' : [0],
            'setSlot0Items' : [[]],
            'setSlot1Items' : [[]],
            'setSlot2Items' : [[]],
            'setSlot3Items' : [[]],
            'setSlot4Items' : [[]],
            'setSlot5Items' : [[]],
        }
        
        self.defaultHouse = {
            'setHouseType' : [0],
            'setGardenPos' : [0],
            'setAtticItems' : [''],
            'setInteriorItems' : [''],
            'setAtticWallpaper' : [''],
            'setInteriorWallpaper' : [''],
            'setAtticWindows' : [''],
            'setInteriorWindows' : [''],
            'setDeletedItems' : [''],
        }

    def startAprilFools(self):
        pass

    def stopAprilFools(self):
        pass

    def getEstateZone(self, avId, name):
        self.setEstateZone(avId, name)

    def setEstateZone(self, avId, name):
        if not avId in self.estateZones:
            self.estateZones[avId] = []
            self.__loadEstate(avId)
        
        
    def handleEstateCreate(self, estateId, avId):
        if not estateId:
            self.notify.warning('Failed to create estate for avId %d' % avId)
            return
            
        for toon in self.otherToons[avId]:
            toonId = toon[0]
            self.air.dbInterface.queryObject(self.air.dbId, toonId, functools.partial(self.handleQueryToon, avId=avId, estateId=estateId, index=self.otherToons[avId].index(toon)))
            
        
        accId = self.air.doId2do[avId].DISLid
        dg = self.air.dclassesByName['AccountAI'].aiFormatUpdate('ESTATE_ID', accId, accId, self.air.ourChannel, estateId)
        self.air.send(dg)
        
        
        self.air.writeServerEvent('estateCreated', '%d for accountId %d' % (estateId, self.air.doId2do[avId].DISLid)) 
        self.spawnEstate(estateId, avId)
        
    def handleQueryToon(self, dclass, fields, avId, estateId, index):
        houseFields = self.defaultHouse.copy()
        houseFields['setName'] = fields['setName'][0]
        houseFields['setColor'] = index
        houseFields['setGardenPos'] = index
        houseFields['setAvatarId'] = self.otherToons[avId][index][0]
        self.air.dbInterface.createObject( self.air.dbId, self.air.dclassesByName['DistributedHouseAI'], houseFields, functools.partial(self.handleHouseCreate, estateId=estateId, index=index, avId=avId))
        
    def handleHouseCreate(self, houseId, estateId, index, avId):
        if not houseId:
            self.notify.warning('FUCK, I COULDN\'T BUILD A HOUSE!!!!!')
            return
            
        self.houseIds[avId].append(houseId)
        if len(self.houseIds[avId]) == 6:
            accId = self.air.doId2do[avId].DISLid
            dg = self.air.dclassesByName['AccountAI'].aiFormatUpdate('HOUSE_ID_SET', accId, accId, self.air.ourChannel, self.houseIds[avId])
            self.air.send(dg)
            
        
    def spawnEstate(self, estateId, avId):
        self.estateZones[avId].append(self.air.allocateZone())
        self.sendUpdateToAvatarId(avId, 'setEstateZone', [avId, self.estateZones[avId][0]])
        self.air.sendActivate(
            estateId,
            self.air.districtId,
            self.estateZones[avId][0], 
            self.air.dclassesByName['DistributedEstateAI'],
            {}
        )
        
    def __loadEstate(self, avId):
        
        def getAvIdName(dclass, fields, avIndex=0):
            name = fields['setName'][0]
            self.otherToons[avId][avIndex].append(name)
            createHouse(self.otherToons[avId][avIndex][0], name, avIndex)       
        
        def getEstateHouseDetails(dclass, fields):
            self.otherToons[avId] = []
            self.houseIds[avId] = []
            estateFields = self.defaultEstate.copy()
            
            
            if fields['ESTATE_ID'] == 0:
                for avIndex in enumerate(fields['ACCOUNT_AV_SET']):
                    toonAvId = avIndex[1]
                    estateFields['setSlot%dToonId' % avIndex[0]] = [toonAvId]
                    self.otherToons[avId].append([ toonAvId ])
                    
                self.air.dbInterface.createObject(
                    self.air.dbId,
                    self.air.dclassesByName['DistributedEstateAI'],
                    estateFields,
                    functools.partial(self.handleEstateCreate, avId=avId)
                )
            else:
                self.spawnEstate(fields['ESTATE_ID'], avId)
                #if toonAvId != 0:
                    #self.air.dbInterface.queryObject(self.air.dbId, toonAvId, functools.partial(getAvIdName, avIndex=avIndex[0]))
                #else:
                    #self.otherToons[avId][avIndex[0]].append('')
                    #createHouse(0, '', avIndex[0])
                
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

