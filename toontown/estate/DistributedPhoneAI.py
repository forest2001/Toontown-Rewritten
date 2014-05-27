from direct.directnotify import DirectNotifyGlobal
from toontown.estate.DistributedFurnitureItemAI import DistributedFurnitureItemAI
from toontown.toonbase import ToontownGlobals
from direct.distributed.ClockDelta import *
import PhoneGlobals

class DistributedPhoneAI(DistributedFurnitureItemAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedPhoneAI")
    
    def __init__(self, air, furnitureMgr, item):
        DistributedFurnitureItemAI.__init__(self, air, furnitureMgr, item)
        self.avId = None
        
    def setInitialScale(self, sx, sy, sz):
        pass
        
    def getInitialScale(self):
        return (1, 1, 1)

    def setNewScale(self, sx, sy, sz):
        if sx + sy + sz < 5:
            return
        self.sendUpdate('setInitialScale', [sx, sy, sz])

    def avatarEnter(self):
        avId = self.air.getAvatarIdFromSender()
        
        if self.avId:
            if self.avId == avId:
                self.air.writeServerEvent('suspicious', avId=avId, issue='Tried to use a phone twice!')
                return
            self.sendUpdateToAvatarId(avId, 'freeAvatar', [])
            return
        
        av = self.air.doId2do.get(avId)
        if not av:
            return
        if len(av.monthlyCatalog) == 0 and len(av.weeklyCatalog) == 0 and len(av.backCatalog) == 0:
            self.d_setMovie(PhoneGlobals.PHONE_MOVIE_EMPTY, avId, globalClockDelta.getRealNetworkTime())
            taskMgr.doMethodLater(1, self.__resetMovie, 'resetMovie-%d' % self.getDoId(), extraArgs=[])
            return
        self.avId = avId
        self.d_setMovie(PhoneGlobals.PHONE_MOVIE_PICKUP, avId, globalClockDelta.getRealNetworkTime())
        self.sendUpdateToAvatarId(avId, 'setLimits', [20]) # TODO - what is the correct number here
        av.b_setCatalogNotify(ToontownGlobals.NoItems, av.mailboxNotify)

    def avatarExit(self):
        avId = self.air.getAvatarIdFromSender()
        if avId != self.avId:
            self.air.writeServerEvent('suspicious', avId=avId, issue='Tried to exit a phone they weren\'t using!')
            return
        self.avId = None
        self.d_setMovie(PhoneGlobals.PHONE_MOVIE_HANGUP, avId, globalClockDelta.getRealNetworkTime())
        taskMgr.doMethodLater(1, self.__resetMovie, 'resetMovie-%d' % self.getDoId(), extraArgs=[])

    def freeAvatar(self):
        pass

    def setLimits(self, todo0):
        pass

    def setMovie(self, todo0, todo1, todo2):
        pass
        
    def d_setMovie(self, mode, avId, time):
        self.sendUpdate('setMovie', [mode, avId, time])
        
    def __resetMovie(self):
        self.d_setMovie(PhoneGlobals.PHONE_MOVIE_CLEAR, 0, globalClockDelta.getRealNetworkTime())

    def requestPurchaseMessage(self, todo0, todo1, todo2):
        pass

    def requestPurchaseResponse(self, todo0, todo1):
        pass

    def requestGiftPurchaseMessage(self, todo0, todo1, todo2, todo3):
        pass

    def requestGiftPurchaseResponse(self, todo0, todo1):
        pass

