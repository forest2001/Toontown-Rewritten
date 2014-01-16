# cfsworks, send help


from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from toontown.ai.DatabaseObject import DatabaseObject
from toontown.estate.DistributedEstateAI import DistributedEstateAI
from toontown.estate.DistributedHouseAI import DistributedHouseAI
import functools

class EstateManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("EstateManagerAI")
    
    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.air = air
        self.estateZones = {}
        self.otherToons = {}
        self.houseIds = {}
        self.estates = {}
        self.target = {}
        
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

    def getEstateZone(self, requestedAv, name):
        accId = self.air.getAccountIdFromSender()
        # completely ignore client request lol
        self.target[accId] = requestedAv
        self.setEstateZone(accId, name)

    def setEstateZone(self, accId, name):
        if not accId in self.estateZones:
            self.estateZones[accId] = []
            self.__loadEstate(accId)
        else:
            self.sendUpdateToAccountId(accId, 'setEstateZone', [self.target[accId], self.estateZones[accId]])
            del self.target[accId]
        
        
    def handleEstateCreate(self, estateId, accId):
        if not estateId:
            self.notify.warning('Failed to create estate for accId %d' % accId)
            return
        
        self.houseIds[accId] = []
        for i in range(len(self.otherToons[accId])):
            toonId = self.otherToons[accId][i][0]
            if toonId == 0:
                houseFields = self.defaultHouse.copy()
                houseFields['setName'] = ['']
                houseFields['setColor'] = [i]
                houseFields['setGardenPos'] = [i]
                houseFields['setAvatarId'] = [0]
                self.air.dbInterface.createObject( self.air.dbId, self.air.dclassesByName['DistributedHouseAI'], houseFields, functools.partial(self.handleHouseCreate, index=i, accId=accId))
            else:
                self.air.dbInterface.queryObject(self.air.dbId, toonId, functools.partial(self.handleQueryToon, accId=accId, estateId=estateId, index=i))
            
        
        dg = self.air.dclassesByName['AccountAI'].aiFormatUpdate('ESTATE_ID', accId, accId, self.air.ourChannel, estateId)
        self.air.send(dg)
        
        
        self.air.writeServerEvent('estateCreated', '%d for accountId %d' % (estateId, accId)) 
        self.spawnEstate(estateId, accId)
        
    def handleQueryToon(self, dclass, fields, accId, estateId, index):
        houseFields = self.defaultHouse.copy()
        houseFields['setName'] = [fields['setName'][0]]
        houseFields['setColor'] = [index]
        houseFields['setGardenPos'] = [index]
        houseFields['setAvatarId'] = [self.otherToons[accId][index][0]]
        self.air.dbInterface.createObject( self.air.dbId, self.air.dclassesByName['DistributedHouseAI'], houseFields, functools.partial(self.handleHouseCreate, index=index, accId=accId))
        
    def handleHouseCreate(self, houseId, index, accId):
        if not houseId:
            self.houseIds[accId].append(0)
            self.notify.warning('Could not create house!')
            return
            
        if self.otherToons[accId][index][0] != 0:
            self.air.dbInterface.updateObject(self.air.dbId, self.otherToons[accId][index][0], self.air.dclassesByName['DistributedToonAI'], { 'setHouseId' : [houseId] })
            
        self.houseIds[accId].append(houseId)
        if len(self.houseIds[accId]) == 6:
            dg = self.air.dclassesByName['AccountAI'].aiFormatUpdate('HOUSE_ID_SET', accId, accId, self.air.ourChannel, self.houseIds[accId])
            self.air.send(dg)
        self.spawnHouse(houseId, accId, index)
            
        
    def spawnEstate(self, estateId, accId):
        self.sendUpdateToAccountId(accId, 'setEstateZone', [self.target[accId], self.estateZones[accId][0]])
        del self.target[accId]
        self.air.sendActivate(
            estateId,
            self.air.districtId,
            self.estateZones[accId][0], 
            self.air.dclassesByName['DistributedEstateAI'],
            {}
        )
        
    def spawnHouse(self, houseId, accId, index):
        if houseId == 0:
            return
        self.air.sendActivate(
            houseId,
            self.air.districtId,
            self.estateZones[accId][0], 
            self.air.dclassesByName['DistributedHouseAI'],
            {'setHousePos' : [index] }
        ) 
        
    def __loadEstate(self, accId):        
        def getEstateHouseDetails(dclass, fields):
            self.otherToons[accId] = []    
            self.estateZones[accId].append(self.air.allocateZone())
            
            if fields['ESTATE_ID'] == 0:
                estateFields = self.defaultEstate.copy()
                for avIndex in enumerate(fields['ACCOUNT_AV_SET']):
                    toonAvId = avIndex[1]
                    estateFields['setSlot%dToonId' % avIndex[0]] = [toonAvId]
                    self.otherToons[accId].append([ toonAvId ])
                    
                self.air.dbInterface.createObject(
                    self.air.dbId,
                    self.air.dclassesByName['DistributedEstateAI'],
                    estateFields,
                    functools.partial(self.handleEstateCreate, accId=accId)
                )
            else:
                self.spawnEstate(fields['ESTATE_ID'], accId)
                for house in enumerate(fields['HOUSE_ID_SET']):
                    self.spawnHouse(house[1], accId, house[0])                
        self.air.dbInterface.queryObject(self.air.dbId, accId, getEstateHouseDetails)
        
    def setAvHouseId(self, todo0, todo1):
        pass

    def sendAvToPlayground(self, todo0, todo1):
        pass

    def exitEstate(self):
        accId = self.air.getAccountIdFromSender()
        for zoneId in self.estateZones[accId]:
            self.air.deallocateZone(zoneId)
        del self.estateZones[accId]

    def removeFriend(self, todo0, todo1):
        pass

