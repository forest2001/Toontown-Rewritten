from direct.directnotify import DirectNotifyGlobal
from toontown.estate.DistributedFurnitureItemAI import DistributedFurnitureItemAI
from toontown.toon.ToonDNA import ToonDNA
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
        self.removedBottoms = []
        self.removedTops = []
        
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
        self.botList = fields['setClothesBottomsList'][0]
        self.topList = fields['setClothesTopsList'][0]
        dna = ToonDNA(str=fields['setDNAString'][0])
        self.gender = dna.gender
    
    def getOwnerId(self):
        return self.furnitureMgr.ownerId
        
    def __verifyAvatarInMyZone(self, av):
        return av.getLocation() == self.getLocation()

    def enterAvatar(self):
        avId = self.air.getAvatarIdFromSender()
        if self.avId:
            if self.avId == avId:
                self.air.writeServerEvent('suspicious', avId=avId, issue='Tried to use closet twice!')
            self.sendUpdateToAvatarId(avId, 'freeAvatar', [])
            return
        av = self.air.doId2do.get(avId)
        if not av:
            self.air.writeServerEvent('suspicious', avId=avId, issue='Not in same shard as closet!')
            return
        if not self.__verifyAvatarInMyZone(av):
            self.air.writeServerEvent('suspicious', avId=avId, issue='Not in same zone as closet!')
            return
        self.customerDNA = av.dna
        self.avId = avId
        self.d_setState(ClosetGlobals.OPEN, avId, self.furnitureMgr.ownerId, self.gender, self.topList, self.botList)
        

    def removeItem(self, item, topOrBottom):
        avId = self.air.getAvatarIdFromSender()
        if avId != self.furnitureMgr.ownerId:
            self.air.writeServerEvent('suspicious', avId=avId, issue='Tried to remove item from someone else\'s closet!')
            return
        if avId != self.avId:
            self.air.writeServerEvent('suspicious', avId=avId, issue='Tried to remove item while not interacting with closet!')
            return
        av = self.air.doId2do.get(avId)
        if not av:
            self.air.writeServerEvent('suspicious', avId=avId, issue='Tried to interact with a closet from another shard!')
            return
        tempDna = ToonDNA()
        if not tempDna.isValidNetString(item):
            self.air.writeServerEvent('suspicious', avId=avId, issue='Sent an invalid DNA string!')
            return
        tempDna.makeFromNetString(item)
        if topOrBottom == ClosetGlobals.SHIRT:
            self.removedTops.append([tempDna.topTex, tempDna.topTexColor, tempDna.sleeveTex, tempDna.sleeveTexColor])
        elif topOrBottom == ClosetGlobals.SHORTS:
            self.removedBottoms.append([tempDna.botTex, tempDna.botTexColor])
        else:
            self.air.writeServerEvent('suspicious', avId=avId, issue='Set an invalid topOrBottom value!')
            return
        
    def __checkValidDNAChange(self, av, testDNA):
        # verify they aren't trying to change anything other than their clothing.
        # FML this took some time to write...
        if testDNA.head != av.dna.head:
            return False
        if testDNA.torso != av.dna.torso:
            if av.dna.gender == 'm':
                return False
            elif testDNA.torso[0] != av.dna.torso[0]: #first character of torso ('size') must remain the same, otherwise you are hacker scum.
                return False
        if testDNA.legs != av.dna.legs:
            return False
        if testDNA.gender != av.dna.gender:
            return False
        if testDNA.armColor != av.dna.armColor:
            return False
        if testDNA.gloveColor != av.dna.gloveColor:
            # wtf u little hackin' shit.
            return False
        if testDNA.legColor != av.dna.legColor:
            return False
        if testDNA.headColor != av.dna.headColor:
            return False
        return True

    def setDNA(self, dnaString, finished, whichItem):
        avId = self.air.getAvatarIdFromSender()
        if avId != self.avId:
            self.air.writeServerEvent('suspicious', avId=avId, issue='Tried to set DNA from closet while not using it!')
            return
        av = self.air.doId2do.get(avId)
        if not av:
            self.air.writeServerEvent('suspicious', avId=avId, issue='Interacted with a closet from another shard!')
            return
        if not self.__verifyAvatarInMyZone(av):
            self.air.writeServerEvent('suspicious', avId=avId, issue='Tried to setDNA while in another zone!')
            return
        testDna = ToonDNA()
        if not testDna.isValidNetString(dnaString):
            self.air.writeServerEvent('suspicious', avId=avId, issue='Tried to set invalid DNA at a closet!')
            return
        if not finished:
            testDna.makeFromNetString(dnaString)
            if not self.__checkValidDNAChange(av, testDna):
                    self.air.writeServerEvent('suspicious', avId=avId, issue='Tried to change their DNA temporarily!')
                    return
            self.sendUpdate('setCustomerDNA', [avId, dnaString])
            return
        elif finished == 1:
            self.d_setMovie(ClosetGlobals.CLOSET_MOVIE_COMPLETE, avId, globalClockDelta.getRealNetworkTime())
            taskMgr.doMethodLater(1, self.__resetMovie, 'resetMovie-%d' % self.getDoId(), extraArgs=[])
            self.d_setState(ClosetGlobals.CLOSED, 0, self.furnitureMgr.ownerId, self.gender, self.topList, self.botList)
            av.b_setDNAString(self.customerDNA.makeNetString())
            self.removedBottoms = []
            self.removedTops = []
            self.customerDNA = None
            self.avId = None
        elif finished == 2:
            if avId != self.furnitureMgr.ownerId:
                self.air.writeServerEvent('suspicious', avId=avId, issue='Tried to set their clothes from somebody else\'s closet!')
                return
            testDna.makeFromNetString(dnaString)
            if whichItem & ClosetGlobals.SHIRT:
                success = av.replaceItemInClothesTopsList(testDna.topTex, testDna.topTexColor, testDna.sleeveTex, testDna.sleeveTexColor, self.customerDNA.topTex, self.customerDNA.topTexColor, self.customerDNA.sleeveTex, self.customerDNA.sleeveTexColor)
                if success:
                    self.customerDNA.topTex = testDna.topTex
                    self.customerDNA.topTexColor = testDna.topTexColor
                    self.customerDNA.sleeveTex = testDna.sleeveTex
                    self.customerDNA.sleeveTexColor = testDna.sleeveTexColor
                else:
                    self.air.writeServerEvent('suspicious', avId=avId, issue='Tried to set their shirt to a shirt they don\'t own!')
            if whichItem & ClosetGlobals.SHORTS:
                success = av.replaceItemInClothesBottomsList(testDna.botTex, testDna.botTexColor, self.customerDNA.botTex, self.customerDNA.botTexColor)
                if success:
                    self.customerDNA.botTex = testDna.botTex
                    self.customerDNA.botTexColor = testDna.botTexColor
                    if self.customerDNA.torso != testDna.torso:
                            if self.customerDNA.gender == 'm':
                                self.air.writeServerEvent('suspicious', avId=avId, issue='Tried to change their torso size!')
                                return
                            elif self.customerDNA.torso[0] != testDna.torso[0]:
                                self.air.writeServerEvent('suspicious', avId=avId, issue='Tried to change their torso size!')
                                return
                    self.customerDNA.torso = testDna.torso
                else:
                    self.air.writeServerEvent('suspicious', avId=avId, issue='Tried to set their shorts to a pair they don\'t own!')
            for bottom in self.removedBottoms:
                botTex, botTexColor = bottom
                success = av.removeItemInClothesBottomsList(botTex, botTexColor)
                if not success:
                    self.air.writeServerEvent('suspicious', avId=avId, issue='Tried to remove a bottom they didn\'t have!')
            for top in self.removedTops:
                topTex, topTexColor, sleeveTex, sleeveTexColor = top
                success = av.removeItemInClothesTopsList(topTex, topTexColor, sleeveTex, sleeveTexColor)
                if not success:
                    self.air.writeServerEvent('suspicious', avId=avId, issue='Tried to remove a top they didn\'t have!')
            av.b_setDNAString(self.customerDNA.makeNetString())
            av.b_setClothesTopsList(av.getClothesTopsList())
            av.b_setClothesBottomsList(av.getClothesBottomsList())
            self.topList = av.getClothesTopsList()
            self.botList = av.getClothesBottomsList()
            self.removedBottoms = []
            self.removedTops = []
            self.d_setMovie(ClosetGlobals.CLOSET_MOVIE_COMPLETE, avId, globalClockDelta.getRealNetworkTime())
            taskMgr.doMethodLater(1, self.__resetMovie, 'resetMovie-%d' % self.getDoId(), extraArgs=[])
            self.d_setState(ClosetGlobals.CLOSED, 0, self.furnitureMgr.ownerId, self.gender, self.topList, self.botList)
            self.customerDNA = None
            self.avId = None

    def setState(self, todo0, todo1, todo2, todo3, todo4, todo5):
        pass
        
    def d_setState(self, mode, avId, ownerId, gender, topList, botList):
        self.sendUpdate('setState', [mode, avId, ownerId, gender, topList, botList])
        
    def d_setMovie(self, movie, avId, time):
        self.sendUpdate('setMovie', [movie, avId, time])
        
    def __resetMovie(self):
        self.d_setMovie(ClosetGlobals.CLOSET_MOVIE_CLEAR, 0, globalClockDelta.getRealNetworkTime())

    def setMovie(self, todo0, todo1, todo2):
        pass

    def resetItemLists(self):
        pass

    def setCustomerDNA(self, todo0, todo1):
        pass

