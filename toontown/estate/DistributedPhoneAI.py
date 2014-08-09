from direct.directnotify import DirectNotifyGlobal
from toontown.estate.DistributedFurnitureItemAI import DistributedFurnitureItemAI
from toontown.toonbase import ToontownGlobals
from toontown.catalog import CatalogItem
from direct.distributed.ClockDelta import *
import time
import PhoneGlobals

class DistributedPhoneAI(DistributedFurnitureItemAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedPhoneAI")
    
    def __init__(self, air, furnitureMgr, item):
        DistributedFurnitureItemAI.__init__(self, air, furnitureMgr, item)
        self.avId = None
        self.movie = PhoneGlobals.PHONE_MOVIE_CLEAR
        
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
        self.sendUpdateToAvatarId(avId, 'setLimits', [ToontownGlobals.MaxHouseItems]) # TODO - what is the correct number here
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

    def setMovie(self, mode, avId, timestamp):
        self.movie = mode
        if self.movie != PhoneGlobals.PHONE_MOVIE_CLEAR:
            taskMgr.doMethodLater(2.0, self.clearMovie, 'clear-movie-%d' % self.getDoId())
        
    def d_setMovie(self, mode, avId, time):
        self.sendUpdate('setMovie', [mode, avId, time])
        
    def __resetMovie(self):
        self.d_setMovie(PhoneGlobals.PHONE_MOVIE_CLEAR, 0, globalClockDelta.getRealNetworkTime())

    def requestPurchaseMessage(self, context, item, optional):
        avId = self.air.getAvatarIdFromSender()
        if avId != self.avId:
            self.air.writeServerEvent('suspicious', avId=avId, issue='Tried to purchase while not using the phone!')
            return
        av = self.air.doId2do.get(avId)
        if not av:
            self.air.writeServerEvent('suspicious', avId=avId, issue='Used phone from other shard!')
            return
        item = CatalogItem.getItem(item)
        if item in av.backCatalog:
            price = item.getPrice(CatalogItem.CatalogTypeBackorder)
        elif item in av.weeklyCatalog or item in av.monthlyCatalog:
            price = item.getPrice(0)
        else:
            return
        if item.getDeliveryTime():
            if len(av.onOrder) > 3: #TODO correct number
                self.sendUpdateToAvatarId(avId, 'requestPurchaseResponse', [context, ToontownGlobals.ToontownGlobals.P_OnOrderListFull])
                return
            if len(av.mailboxContents) + len(av.onOrder) >= ToontownGlobals.MaxMailboxContents:
                self.sendUpdateToAvatarId(avId, 'requestPurchaseResponse', [context, ToontownGlobals.P_MailboxFull])
            if not av.takeMoney(price):
                return
            item.deliveryDate = int(time.time()/60) + 1#item.getDeliveryTime()
            av.onOrder.append(item)
            av.b_setDeliverySchedule(av.onOrder)
            self.sendUpdateToAvatarId(avId, 'requestPurchaseResponse', [context, ToontownGlobals.P_ItemOnOrder])
        else:
            if not av.takeMoney(price):
                #u wot m8
                return
            self.sendUpdateToAvatarId(avId, 'requestPurchaseResponse', [context, item.recordPurchase(av, optional)])
        

    def requestPurchaseResponse(self, todo0, todo1):
        pass

    def requestGiftPurchaseMessage(self, todo0, todo1, todo2, todo3):
        pass

    def requestGiftPurchaseResponse(self, todo0, todo1):
        pass

