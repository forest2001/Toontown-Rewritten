from direct.directnotify import DirectNotifyGlobal
from toontown.estate.DistributedFurnitureItemAI import DistributedFurnitureItemAI
from direct.distributed.ClockDelta import *
import ClosetGlobals

class DistributedClosetAI(DistributedFurnitureItemAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedClosetAI")

    def __init__(self, air, furnitureMgr, itemType):
        DistributedFurnitureItemAI.__init__(self, air, furnitureMgr, itemType)
        self.avId = None
        self.customerDNA = None
        self.topList = []
        self.botList = []
        self.gender = 'm'
        
    def generate(self):
        if self.furnitureMgr.ownerId:
            owner = self.air.doId2do.get(self.furnitureMgr.ownerId)
            if owner:
                self.topList = owner.clothesTopsList
                self.botList = owner.clothesBottomsList
                self.gender = owner.dna.gender
            else:
                self.air.dbInterface.queryObject(self.air.dbId, self.furnitureMgr.ownerId, self.__gotOwner)

    def __gotOwner(self, dclass, fields):
        if dclass != self.air.dclassesByName['DistributedToonAI']:
            self.notify.warning('Got object of wrong type!')
            return
    
    def getOwnerId(self):
        return self.furnitureMgr.ownerId

    def enterAvatar(self):
        avId = self.air.getAvatarIdFromSender()
        if self.avId:
            if self.avId == avId:
                self.air.writeServerUpdate('suspicious', avId=avId, issue='Tried to use closet twice!')
            self.sendUpdateToAvatarId(avId, 'freeAvatar', [])
            return
        self.d_setState(ClosetGlobals.OPEN, avId, self.furnitureMgr.ownerId, self.gender, self.topList, self.botList)
        

    def removeItem(self, todo0, todo1):
        pass

    def setDNA(self, dnaString, finished, whichItem):
        avId = self.air.getAvatarIdFromSender()
        self.sendUpdate('setCustomerDNA', [avId, dnaString])
        if finished:
            self.d_setMovie(ClosetGlobals.CLOSET_MOVIE_COMPLETE, avId, globalClockDelta.getRealNetworkTime())
            self.d_setState(ClosetGlobals.CLOSED, 0, self.furnitureMgr.ownerId, self.gender, self.topList, self.botList)

    def setState(self, todo0, todo1, todo2, todo3, todo4, todo5):
        pass
        
    def d_setState(self, mode, avId, ownerId, gender, topList, botList):
        self.sendUpdate('setState', [mode, avId, ownerId, gender, topList, botList])
        
    def d_setMovie(self, movie, avId, time):
        self.sendUpdate('setMovie', [movie, avId, time])

    def setMovie(self, todo0, todo1, todo2):
        pass

    def resetItemLists(self):
        pass

    def setCustomerDNA(self, todo0, todo1):
        pass

