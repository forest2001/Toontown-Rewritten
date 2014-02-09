from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.task import Task
import PartyGlobals

class DistributedPartyCannonAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedPartyCannonAI")
    
    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.actId = 0
        self.posHpr = [0, 0, 0, 0, 0, 0]
        self.avId = 0

        
    def delete(self):
        taskMgr.remove('removeToon%d' % self.doId)
        DistributedObjectAI.delete(self)
        
    def setActivityDoId(self, actId):
        self.actId = actId
        
    def getActivityDoId(self):
        return self.actId

    def setPosHpr(self, x, y, z, h, p, r):
        self.posHpr = [x, y, z, h, p, r]
        
    def getPosHpr(self):
        return self.posHpr

    def requestEnter(self):
        if not self.avId:
            self.avId = self.air.getAvatarIdFromSender()
            self.d_setMovie(PartyGlobals.CANNON_MOVIE_LOAD, self.avId)

    def requestExit(self):
        avId = self.air.getAvatarIdFromSender()
        if self.avId == avId:
            self.sendUpdate('setCannonExit', [avId])
            self.avId = 0

    def d_setMovie(self, movie, avId):
        self.sendUpdate('setMovie', [movie, avId])

    def setCannonPosition(self, rot, angle):
        avId = self.air.getAvatarIdFromSender()
        if avId == self.avId:
            self.sendUpdate('updateCannonPosition', [avId, rot, angle])

    def setCannonLit(self, rot, angle):
        avId = self.air.getAvatarIdFromSender()
        if avId == self.avId:
            activity = self.air.doId2do[self.actId]
            activity.b_setCannonWillFire(self.doId, rot, angle, avId)
            self.d_setMovie(PartyGlobals.CANNON_MOVIE_CLEAR, avId)
            self.sendUpdate('setCannonExit', [avId])
            self.avId = 0

    def setFired(self):
        self.air.writeServerEvent('suspicious',self.air.getAvatarIdFromSender(),'Toon tried to call unused setFired!')

    def setLanded(self, toonId):
        avId = self.air.getAvatarIdFromSender()
        if toonId != avId:
            self.air.writeServerEvent('suspicious',avId,'Toon claimed to be another toon in cannon!')
            return
        self.d_setMovie(PartyGlobals.CANNON_MOVIE_LANDED, avId)

    def setTimeout(self):
        avId = self.air.getAvatarIdFromSender()
        if avId != self.avId:
            self.air.writeServerEvent('suspicious',avId,'Toon tried to start timer for someone else!')
        taskMgr.doMethodLater(PartyGlobals.CANNON_TIMEOUT, self.__removeToon, 'removeToon%d' % self.doId, extraArgs=[avId])
        
        
    def __removeToon(self, avId):
        if avId != self.avId:
            return
        self.avId = 0
        self.d_setMovie(PartyGlobals.CANNON_MOVIE_FORCE_EXIT, avId)
        self.sendUpdate('setCannonExit', [avId])
