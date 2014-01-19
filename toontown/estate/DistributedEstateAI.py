from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
import HouseGlobals
import time

class DistributedEstateAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedEstateAI")
    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.toons = [0, 0, 0, 0, 0, 0]
        self.items = [[], [], [], [], [], []]
        self.decorData = []
        self.estateType = 0 # NOT SURE IF THIS HAS ANY USE BUT THANKS DISNEY
        self.cloudType = 0
        self.dawnTime = 0
        self.lastEpochTimestamp = 0
        self.rentalTimestamp = 0
        self.houses = [None] * 6

        self.owner = None

    def destroy(self):
        for house in self.houses:
            if house:
                house.requestDelete()
        self.requestDelete()

    def setEstateReady(self):
        pass

    def setClientReady(self):
        self.sendUpdate('setEstateReady', [])

    def setEstateType(self, type):
        self.estateType = type
        
    def d_setEstateType(self, type):
        self.sendUpdate('setEstateType', [type])
        
    def b_setEstateType(self, type):
        self.setEstateType(type)
        self.d_setEstateType(type)

    def getEstateType(self):
        return self.estateType
        
    def setClosestHouse(self, todo0):
        pass

    def setTreasureIds(self, todo0):
        pass

    def requestServerTime(self):
        avId = self.air.getAvatarIdFromSender()
        self.sendUpdateToAvatarId(avId, 'setServerTime', [time.time() % HouseGlobals.DAY_NIGHT_PERIOD])

    def setServerTime(self, todo0):
        pass

    def setDawnTime(self, dawnTime):
        self.dawnTime = dawnTime
        
    def d_setDawnTime(self, dawnTime):
        self.sendUpdate('setDawnTime', [dawnTime])
        
    def b_setDawnTime(self, dawnTime):
        self.setDawnTime(dawnTime)
        self.d_setDawnTime(dawnTime)
        
    def getDawnTime(self):
        return self.dawnTime

    def placeOnGround(self, todo0):
        pass

    def setDecorData(self, decorData):
        self.decorData = decorData
        
    def d_setDecorData(self, decorData):
        self.sendUpdate('setDecorData', [decorData])
        
    def b_setDecorData(self, decorData):
        self.setDecorData(decorData)
        self.d_setDecorData(decorData)
        
    def getDecorData(self):
        return self.decorData

    def setLastEpochTimeStamp(self, last): #how do I do this
        self.lastEpochTimestamp = last
        
    def d_setLastEpochTimeStamp(self, last):
        self.sendUpdate('setLastEpochTimeStamp', [last])
        
    def b_setLastEpochTimeStamp(self, last):
        self.setLastEpochTimeStamp(last)
        self.d_setLastEpochTimeStamp(last)
        
    def getLastEpochTimeStamp(self):
        return self.lastEpochTimestamp

    def setRentalTimeStamp(self, rental):
        self.rentalTimestamp = rental
        
    def d_setRentalTimeStamp(self, rental):
        self.sendUpdate('setRentalTimeStamp', [rental])
        
    def b_setRentalTimeStamp(self, rental):
        self.setRentalTimeStamp(self, rental)
        self.b_setRentalTimeStamp(self, rental)
        
    def getRentalTimeStamp(self):
        return self.rentalTimestamp

    def setRentalType(self, todo0):
        pass
        
    def getRentalType(self):
        return 0

    def setSlot0ToonId(self, id):
        self.toons[0] = id
        
    def d_setSlot0ToonId(self, id):
        self.sendUpdate('setSlot0ToonId', [id])
        
    def b_setSlot0ToonId(self, id):
        self.setSlot0ToonId(id)
        self.d_setSlot0ToonId(id)
        
    def getSlot0ToonId(self):
        return self.toons[0]

    def setSlot0Items(self, items):
        self.items[0] = items

    def d_setSlot0Items(self, items):
        self.sendUpdate('setSlot5Items', [items])
        
    def b_setSlot0Items(self, items):
        self.setSlot0Items(items)
        self.d_setSlot0Items(items)
        
    def getSlot0Items(self):
        return self.items[0]
        
    def setSlot1ToonId(self, id):
        self.toons[1] = id

    def d_setSlot1ToonId(self, id):
        self.sendUpdate('setSlot1ToonId', [id])
        
    def b_setSlot1ToonId(self, id):
        self.setSlot1ToonId(id)
        self.d_setSlot1ToonId(id)
        
    def getSlot1ToonId(self):
        return self.toons[1]
        
    def setSlot1Items(self, items):
        self.items[1] = items
        
    def d_setSlot1Items(self, items):
        self.sendUpdate('setSlot2Items', [items])
        
    def b_setSlot1Items(self, items):
        self.setSlot2Items(items)
        self.d_setSlot2Items(items)
        
    def getSlot1Items(self):
        return self.items[1]

    def setSlot2ToonId(self, id):
        self.toons[2] = id

    def d_setSlot2ToonId(self, id):
        self.sendUpdate('setSlot2ToonId', [id])
        
    def b_setSlot2ToonId(self, id):
        self.setSlot2ToonId(id)
        self.d_setSlot2ToonId(id)
        
    def getSlot2ToonId(self):
        return self.toons[2]

    def setSlot2Items(self, items):
        self.items[2] = items

    def d_setSlot2Items(self, items):
        self.sendUpdate('setSlot2Items', [items])
        
    def b_setSlot2Items(self, items):
        self.setSlot2Items(items)
        self.d_setSlot2Items(items)
        
    def getSlot2Items(self):
        return self.items[2]

    def setSlot3ToonId(self, id):
        self.toons[3] = id
        
    def d_setSlot3ToonId(self, id):
        self.sendUpdate('setSlot3ToonId', [id])
        
    def b_setSlot3ToonId(self, id):
        self.setSlot3ToonId(id)
        self.d_setSlot3ToonId(id)
        
    def getSlot3ToonId(self):
        return self.toons[3]

    def setSlot3Items(self, items):
        self.items[3] = items
        
    def d_setSlot3Items(self, items):
        self.sendUpdate('setSlot3Items', [items])
        
    def b_setSlot3Items(self, items):
        self.setSlot3Items(items)
        self.d_setSlot3Items(items)
        
    def getSlot3Items(self):
        return self.items[3]

    def setSlot4ToonId(self, id):
        self.toons[4] = id
        
    def d_setSlot4ToonId(self, id):
        self.sendUpdate('setSlot4ToonId', [id])
        
    def b_setSlot5ToonId(self, id):
        self.setSlot4ToonId(id)
        self.d_setSlot4ToonId(id)
        
    def getSlot4ToonId(self):
        return self.toons[4]


    def setSlot4Items(self, items):
        self.items[4] = items
        
    def d_setSlot4Items(self, items):
        self.sendUpdate('setSlot4Items', [items])
        
    def b_setSlot4Items(self, items):
        self.setSlot4Items(items)
        self.d_setSlot4Items(items)
        
    def getSlot4Items(self):
        return self.items[4]

    def setSlot5ToonId(self, id):
        self.toons[5] = id
        
    def d_setSlot5ToonId(self, id):
        self.sendUpdate('setSlot5ToonId', [id])
        
    def b_setSlot5ToonId(self, id):
        self.setSlot5ToonId(id)
        self.d_setSlot5ToonId(id)
        
    def getSlot5ToonId(self):
        return self.toons[5]

    def setSlot5Items(self, items):
        self.items[5] = items
        
    def d_setSlot5Items(self, items):
        self.sendUpdate('setSlot5Items', [items])
        
    def b_setSlot5Items(self, items):
        self.setSlot5Items(items)
        self.d_setSlot5Items(items)
        
    def getSlot5Items(self):
        return self.items[5]

    def setIdList(self, idList):
        for i in range(len(idList)):
            if i >= 6:
                return
            self.toons[i] = idList[i]
        
    def d_setIdList(self, idList):
        self.sendUpdate('setIdList', [idList])
    
    def b_setIdList(self, idList):
        self.setIdList(idList)
        self.d_setIdLst(idList)
        
    def completeFlowerSale(self, todo0):
        pass

    def awardedTrophy(self, todo0):
        pass

    def setClouds(self, clouds):
        self.cloudType = clouds
        
    def d_setClouds(self, clouds):
        self.sendUpdate('setClouds', [clouds])
        
    def b_setClouds(self, clouds):
        self.setClouds(clouds)
        self.d_setClouds(clouds)
        
    def getClouds(self):
        return self.cloudType

    def cannonsOver(self):
        pass

    def gameTableOver(self):
        pass

