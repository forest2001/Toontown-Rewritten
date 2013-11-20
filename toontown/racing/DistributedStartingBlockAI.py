from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from toontown.racing.KartShopGlobals import KartGlobals
from toontown.racing import RaceGlobals

class DistributedStartingBlockAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedStartingBlockAI")
    
    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.air = air
        self.pad = None
        self.currentMovie = False
        self.avId = 0
        self.posHpr = [0, 0, 0, 0, 0, 0]

    def setPadDoId(self, padDoId):
        self.pad = self.air.doId2do[padDoId]
        
    def getPadDoId(self):
        return self.pad.getDoId()

    def setPosHpr(self, x, y, z, h, p, r):
        self.posHpr = [x, y, z, h, p, r]
    
    def getPosHpr(self):
        return self.posHpr
    
    def setPadLocationId(self, padLocationId):
        self.padLocationId = padLocationId
        
    def getPadLocationId(self):
        return self.padLocationId

    def requestEnter(self, isPaid):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do[avId]
        if not av.hasKart():
            self.sendUpdateToAvatarId(avId, 'rejectEnter', [KartGlobals.ERROR_CODE.eNoKart])
            return
        if av.getTickets() < RaceGlobals.getEntryFee(self.pad.trackId, self.pad.trackType):
            self.sendUpdateToAvatarId(avId, 'rejectEnter', [KartGlobals.ERROR_CODE.eTickets])
            return        
        if self.pad.state == 'AllAboard' or self.pad.state == 'WaitBoarding' :
            self.sendUpdateToAvatarId(avId, 'rejectEnter', [KartGlobals.ERROR_CODE.eBoardOver])
            return
        if self.avId != 0:
            if self.avId == avId:
                self.air.writeServerEvent('suspicious', avId, 'Toon tried to board the same starting block twice!')
            self.sendUpdateToAvatarId(avId, 'rejectEnter', [KartGlobals.ERROR_CODE.eOccupied])
            return
        self.b_setOccupied(avId)
        self.b_setMovie(KartGlobals.ENTER_MOVIE)
    def rejectEnter(self, errCode):
        pass

    def requestExit(self):
        avId = self.air.getAvatarIdFromSender()
        if avId != self.avId:
            self.air.writeServerEvent('suspicious', avId, 'Toon tried to get off a starting block they\'re not on!')
        self.b_setMovie(KartGlobals.EXIT_MOVIE)

    def setOccupied(self, avId):
        self.avId = avId
        self.pad.updateTimer()
        
    def d_setOccupied(self, avId):
        self.sendUpdate('setOccupied', [avId])
        
    def b_setOccupied(self, avId):
        self.setOccupied(avId)
        self.d_setOccupied(avId)
        
    def setMovie(self, movie):
        self.currentMovie = movie
    
    def d_setMovie(self, movie):
        self.sendUpdate('setMovie', [movie])
    
    def b_setMovie(self, movie):
        self.setMovie(movie)
        self.d_setMovie(movie)

    def movieFinished(self):
        avId = self.air.getAvatarIdFromSender()
        if self.avId != avId:
            self.air.writeServerEvent('suspicious', avId, 'Toon tried to end movie of another toon!')
            return
        if not self.currentMovie:
            self.air.writeServerEvent('suspicious', avId, 'Toon tried to end non-existent movie!')
            return
        if self.currentMovie == KartGlobals.EXIT_MOVIE:
            self.b_setOccupied(0)
        self.b_setMovie(0)

class DistributedViewingBlockAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedViewingBlockAI")
