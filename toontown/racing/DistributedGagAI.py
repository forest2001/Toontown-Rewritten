from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

class DistributedGagAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedGagAI")
    
    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.owner = 0

    def setInitTime(self, initTime):
        self.initTime = initTime
        
    def getInitTime(self):
        return self.initTime

    def setActivateTime(self, activateTime):
        self.activateTime = activateTime
        
    def getActivateTime(self):
        return self.activateTime

    def setPos(self, x, y, z):
        self.pos = [x, y, z]
        
    def getPos(self):
        return self.pos

    def setRace(self, raceId):
        self.race = self.air.doId2do[raceId]
        
    def getRace(self):
        return self.race.getDoId()

    def setOwnerId(self, ownerId):
        self.owner = ownerId
        
    def getOwnerId(self):
        return self.owner

    def setType(self, type):
        self.type = type
        
    def getType(self):
        return self.type

    def hitSomebody(self, avId, timestamp):
        self.requestDelete()

