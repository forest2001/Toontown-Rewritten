from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from toontown.estate.DistributedEstateAI import DistributedEstateAI
from toontown.estate.DistributedHouseAI import DistributedHouseAI
import functools

class EstateManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("EstateManagerAI")
    
    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.air = air
        
        self.senderIds = {}
        self.estateZone = {}
        self.accountFields = {}
        self.houseIds = {}
        self.estateId = {}
        
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
            # For if we're creating a blank house. We still need an index, however.
            'setName' : [''],
            'setAvatarId' : [0],
        }
        
    def getEstateZone(self):
        senderId = self.air.getAvatarIdFromSender()
        accId = self.air.getAccountIdFromSender()
        
        if accId in self.estateZone:
            # Account already has an estate generated, just tell the sender the zone.
            self.sendUpdateToAccountId(accId, 'setEstateZone', [self.senderIds[accId], self.estateZone[accId]])
            return
            
        self.senderIds[accId] = senderId
        
        # Begin checking if the account has an estate.
        self.air.dbInterface.queryObject(
            self.air.dbId,
            accId,
            functools.partial(self.__checkEstateExists, accId=accId)
        )
            
    def __checkEstateExists(self, dclass, fields, accId):
        if dclass != self.air.dclassesByName['AccountAI']:
            return

        self.accountFields[accId] = fields
        
        if self.accountFields[accId]['ESTATE_ID'] != 0:
            # An estate exists for this account! Let's generate it.
            self.houseIds[accId] = self.accountFields[accId]['HOUSE_ID_SET']
            self.estateId[accId] = self.accountFields[accId]['ESTATE_ID']
            self.__spawnEstateAndHouses(accId)
        else:
            # This account has no estate, we need to create it.
            # This also implies that the Avatar's on the account have no houses.
            # This should only ever happen once per account, when the first toon visits their estate for the first time.
            self.__createEstateAndHouses(accId)
    
    def __createEstateAndHouses(self, accId):
        estateFields = self.defaultEstate.copy()
        for index in enumerate(self.accountFields[accId]['ACCOUNT_AV_SET']):
            # Set each estate toonId slot to mimic the account's toon slots.
            avIndex = index[0]
            avId = index[1]
            estateFields['setSlot%dToonId' % avIndex] = [avId]
        
        # Create the object on the database
        self.air.dbInterface.createObject(
            self.air.dbId, 
            self.air.dclassesByName['DistributedEstateAI'],
            estateFields,
            functools.partial(self.__handleEstateCreation, accId=accId)
        )
        
    def __handleEstateCreation(self, estateId, accId):
        if not estateId:
            self.notify.warning('Failed to create estate for account %d' % accId)
            return
        
        # Update the account's estateId to our newly generated estate.
        dg = self.air.dclassesByName['AccountAI'].aiFormatUpdate(
            'ESTATE_ID',
            accId, accId,
            self.air.ourChannel,
            estateId
        )
        self.air.send(dg)
        self.air.writeServerEvent('estateCreated', 'New estate %d for the account %d' % (estateId, accId))
        
        # Update our stuff so it contains the new estateId.
        self.accountFields[accId]['ESTATE_ID'] = estateId
        self.estateId[accId] = estateId
        
        # Create 6 new houses for our newly generated estate.
        # We will always be creating 6 houses, regardless of if an avatar exists or not.
        self.houseIds[accId] = [0, 0, 0, 0, 0, 0]
        for houseIndex in range(6):
            avId = self.accountFields[accId]['ACCOUNT_AV_SET'][houseIndex]
            if avId != 0:
                # Create a house for a specific toon.
                self.air.dbInterface.queryObject(
                    self.air.dbId,
                    avId,
                    functools.partial(self.__handleGetToonFields, accId=accId, avId=avId, houseIndex=houseIndex)
                )
            else:
                # We only need a blank house
                houseFields = self.defaultHouse.copy()
                houseFields['setGardenPos'] = [houseIndex]
                houseFields['setColor'] = [houseIndex]
                self.air.dbInterface.createObject(
                    self.air.dbId,
                    self.air.dclassesByName['DistributedHouseAI'],
                    houseFields,
                    functools.partial(self.__handleHouseCreation, accId=accId, houseIndex=houseIndex)
                )
                
    def __handleGetToonFields(self, dclass, fields, accId, avId, houseIndex):
        if dclass != self.air.dclassesByName['DistributedToonAI']:
            # Reset and spawn a blank house instead.
            fields['setName'] = ['']
            avId = 0
        houseFields = self.defaultHouse.copy()
        houseFields['setName'] = [fields['setName'][0]]
        houseFields['setAvatarId'] = [avId]
        houseFields['setColor'] = [houseIndex]
        houseFields['setGardenPos'] = [houseIndex]
        self.air.dbInterface.createObject(
            self.air.dbId,
            self.air.dclassesByName['DistributedHouseAI'],
            houseFields,
            functools.partial(self.__handleHouseCreation, accId=accId, avId=avId, houseIndex=houseIndex)
        )
    
    def __handleHouseCreation(self, houseId, accId, houseIndex, avId=0):
        if not houseId:
            self.notify.warning('Failed to create a house for avId %d on account %d' % (avId, accId))
            return
        
        # Update the avatar's houseId
        if avId != 0:
            self.air.dbInterface.updateObject(
                self.air.dbId,
                avId,
                self.air.dclassesByName['DistributedToonAI'],
                { 'setHouseId' : [houseId] }
            )
        
        self.houseIds[accId][houseIndex] = houseId
        if 0 not in self.houseIds[accId]:
            # Now that we have all 6 houses, update the account too.
            self.air.dbInterface.updateObject(
                self.air.dbId,
                accId,
                self.air.dclassesByName['AccountAI'],
                { 'HOUSE_ID_SET' : self.houseIds[accId] }
            )
            
            # Update our dict so it contains the new houseIds
            self.accountFields[accId]['HOUSE_ID_SET'] = self.houseIds[accId]
            
            # Now finally, lets spawn everything! Woo!
            self.__spawnEstateAndHouses(accId)
            
    def __spawnEstateAndHouses(self, accId):
        # Allocate a zone for the DistributedEstateAI and DistributedHouseAI's.
        self.estateZone[accId] = self.air.allocateZone()
        
        # Spawn the estate
        if self.accountFields[accId]['ESTATE_ID'] in self.air.doId2do:
            # We want to respawn it in another zone, so if it still exists for whatever reason,
            # we delete it.
            self.air.doId2do[self.accountFields[accId]['ESTATE_ID']].requestDelete()
         
        self.air.sendActivate(
            self.accountFields[accId]['ESTATE_ID'],
            self.air.districtId,
            self.estateZone[accId],
            self.air.dclassesByName['DistributedEstateAI'],
            {}
        )
        
        # Spawn the houses
        for house in enumerate(self.accountFields[accId]['HOUSE_ID_SET']):
            houseIndex = house[0]
            houseId = house[1]
            
            if houseId in self.air.doId2do:
                # Same as estates, we want to respawn it elsewhere.
                self.air.doId2do[houseId].requestDelete()
                
            self.air.sendActivate(
                houseId,
                self.air.districtId,
                self.estateZone[accId],
                self.air.dclassesByName['DistributedHouseAI'],
                { 'setHousePos' : [houseIndex] }
            )
            
        # Tell the client where to find everything :D
        self.sendUpdateToAccountId(accId, 'setEstateZone', [self.senderIds[accId], self.estateZone[accId]])
        
        # Clean up everything that we no longer need.
        del self.senderIds[accId]
        del self.accountFields[accId]

    def exitEstate(self):
        accId = self.air.getAccountIdFromSender()
        # Delete houses (which also deletes doors and interiors).
        for houseId in self.houseIds[accId]:
            self.air.doId2do[houseId].requestDelete()
        # Delete the estate
        self.air.doId2do[self.estateId[accId]].requestDelete()
        # Deallocate zone
        self.air.deallocateZone(self.estateZone[accId])
        # Clear the crap that the estate needed
        del self.estateZone[accId]
        del self.houseIds[accId]
        del self.estateId[accId]
        
    def setAvHouseId(self, todo0, todo1):
        pass
        
    def sendAvToPlayground(self, todo0, todo1):
        pass
        
    def startAprilFools(self):
        pass
        
    def stopAprilFools(self):
        pass
