from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from toontown.fishing import FishGlobals
from toontown.fishing.FishBase import FishBase
from direct.task import Task


class DistributedFishingSpotAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedFishingSpotAI")
	
    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.avId = None
        self.pondDoId = None
        self.posHpr = [None, None, None, None, None, None]
	
    def generate(self):
        DistributedObjectAI.generate(self)
        pond = self.air.doId2do[self.pondDoId]
        pond.addSpot(self)

    
    def setPondDoId(self, pondDoId):
        self.pondDoId = pondDoId
	
    def getPondDoId(self):
        return self.pondDoId
	
    def setPosHpr(self, x, y, z, h, p, r):
        self.posHpr = [x, y, z, h, p, r]
	
    def getPosHpr(self):
        return self.posHpr
	
    def requestEnter(self):
        avId = self.air.getAvatarIdFromSender()
        if self.avId != None:
            if self.avId == avId:
                self.air.writeServerEvent('suspicious', avId, 'Toon requested to enter a pier twice!')
            self.sendUpdateToAvatarId(avId, 'rejectEnter', [])
            return
        self.acceptOnce(self.air.getAvatarExitEvent(avId), self.removeFromPier)
        self.b_setOccupied(avId)
        self.d_setMovie(FishGlobals.EnterMovie, 0, 0, 0, 0, 0, 0)
        taskMgr.remove('cancelAnimation%d' % self.doId)
        taskMgr.doMethodLater(2, DistributedFishingSpotAI.cancelAnimation, 'cancelAnimation%d' % self.doId, [self])
        taskMgr.remove('timeOut%d' % self.doId)
        taskMgr.doMethodLater(45, DistributedFishingSpotAI.removeFromPierWithAnim, 'timeOut%d' % self.doId, [self])
            

    def rejectEnter(self):
        pass

    def requestExit(self):
        avId = self.air.getAvatarIdFromSender()
        if self.avId != avId:
            self.air.writeServerEvent('suspicious', avId, 'Toon requested to exit a pier they\'re not on!')
            return
        taskMgr.doMethodLater(1, DistributedFishingSpotAI.removeFromPier, 'Exit from %d' % self.doId, [self])
        self.ignore(self.air.getAvatarExitEvent(avId))

    def setOccupied(self, avId):
        self.avId = avId
        
    def d_setOccupied(self, avId):
        self.sendUpdate('setOccupied', [avId])
    
    def b_setOccupied(self, avId):
        self.setOccupied(avId)
        self.d_setOccupied(avId)

    def doCast(self, p, h):
        avId = self.air.getAvatarIdFromSender()
        if self.avId != avId:
            self.air.writeServerEvent('suspicious', avId, 'Toon tried to cast from a pier they\'re not on!')
            return
        av = self.air.doId2do[avId]
        money = av.getMoney()
        cost = FishGlobals.getCastCost(av.getFishingRod())
        if money < cost:
            self.air.writeServerEvent('suspicious', avId, 'Toon tried to cast without enough jellybeans!')
            return
        av.takeMoney(cost, False)
        self.d_setMovie(FishGlobals.CastMovie, 0, 0, 0, 0, p, h)
        taskMgr.remove('cancelAnimation%d' % self.doId)
        taskMgr.doMethodLater(2, DistributedFishingSpotAI.cancelAnimation, 'cancelAnimation%d' % self.doId, [self])
        taskMgr.remove('timeOut%d' % self.doId)
        taskMgr.doMethodLater(45, DistributedFishingSpotAI.removeFromPierWithAnim, 'timeOut%d' % self.doId, [self])
        
    def sellFish(self):
        avId = self.air.getAvatarIdFromSender()
        if self.avId != avId:
            self.air.writeServerEvent('suspicious', avId, 'Toon tried to sell fish at a pier they\'re not using!')
            return
        av = self.air.doId2do[avId]
        totalFish = av.fishCollection.__len__()
        trophies = int(totalFish / 10)
        curTrophies = len(av.fishingTrophies)
        result = False
        if trophies > curTrophies:
            av.b_setMaxHp(av.getMaxHp() + trophies - curTrophies)
            av.b_setHp(av.getMaxHp())
            av.b_setFishingTrophies(range(trophies))
            result = True
        av.addMoney(av.fishTank.getTotalValue())
        av.b_setFishTank([], [], [])
        self.sendUpdateToAvatarId(avId, 'sellFishComplete', [result, totalFish])
        taskMgr.remove('timeOut%d' % self.doId)
        taskMgr.doMethodLater(45, DistributedFishingSpotAI.removeFromPierWithAnim, 'timeOut%d' % self.doId, [self])   

    def sellFishComplete(self, todo0, todo1):
        pass

    def setMovie(self, todo0, todo1, todo2, todo3, todo4, todo5, todo6):
        pass
        
    def d_setMovie(self, mode, code, genus, species, weight, p, h):
        self.sendUpdate('setMovie', [mode, code, genus, species, weight, p, h])

    def removeFromPier(self):
        taskMgr.remove('timeOut%d' % self.doId)
        taskMgr.doMethodLater(45, DistributedFishingSpotAI.removeFromPierWithAnim, 'timeOut%d' % self.doId, [self])   
        self.cancelAnimation()
        self.b_setOccupied(0)
        
    def removeFromPierWithAnim(self):
        taskMgr.remove('cancelAnimation%d' % self.doId)
        self.d_setMovie(FishGlobals.ExitMovie, 0, 0, 0, 0, 0, 0)
        taskMgr.doMethodLater(1, DistributedFishingSpotAI.removeFromPier, 'remove%d' % self.doId, [self])
	
    def rewardIfValid(self, target):
        av = self.air.doId2do[self.avId]
        f = FishGlobals.getRandomFishVitals(self.air.doId2do[self.pondDoId].getArea(), av.getFishingRod())
        fish = FishBase(f[1], f[2], f[3])      
        fishType = av.fishCollection.collectFish(fish)
        if fishType == FishGlobals.COLLECT_NEW_ENTRY:
            itemType = FishGlobals.FishItemNewEntry
        elif fishType == FishGlobals.COLLECT_NEW_RECORD:
            itemType = FishGlobals.FishItemNewRecord
        else:
            itemType = FishGlobals.FishItem
        netlist = av.fishCollection.getNetLists()
        av.d_setFishCollection(netlist[0], netlist[1], netlist[2])
        
        av.fishTank.addFish(fish)
        netlist = av.fishTank.getNetLists()
        av.d_setFishTank(netlist[0], netlist[1], netlist[2])
        self.d_setMovie(FishGlobals.PullInMovie, itemType, fish.getGenus(), fish.getSpecies(), fish.getWeight(), 0, 0)
        
        
	
    def cancelAnimation(self):
        self.d_setMovie(FishGlobals.NoMovie, 0, 0, 0, 0, 0, 0)