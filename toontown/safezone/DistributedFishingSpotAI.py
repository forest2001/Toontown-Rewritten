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
        self.acceptOnce(self.air.getAvatarExitEvent(avId), self.removeFromPier, extraArgs=[avId])
        taskMgr.remove('cancel%d' % self.doId)
        self.sendUpdate('setOccupied', [avId])
        self.sendUpdate('setMovie', [FishGlobals.EnterMovie, 0, 0, 0, 0, 0, 0])
        taskMgr.doMethodLater(2, DistributedFishingSpotAI.cancelAnimation, 'cancel %d' % self.doId, [self])
        self.avId = avId
            

    def rejectEnter(self):
        pass

    def requestExit(self):
        avId = self.air.getAvatarIdFromSender()
        if self.avId != avId:
            self.air.writeServerEvent('suspicious', avId, 'Toon requested to exit a pier they\'re not on!')
            return
        taskMgr.remove('cancel%d' % self.doId)
        self.sendUpdate('setMovie', [FishGlobals.ExitMovie, 0, 0, 0, 0, 0, 0])
        taskMgr.doMethodLater(1, DistributedFishingSpotAI.removeFromPier, 'Exit from %d' % self.doId, [self])
        self.ignore(self.air.getAvatarExitEvent(avId))

    def setOccupied(self, avId):
        pass

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
        taskMgr.remove('cancel %d' % self.doId)
        self.sendUpdate('setMovie', [FishGlobals.CastMovie, 0, 0, 0, 0, p, h])
        taskMgr.doMethodLater(2, DistributedFishingSpotAI.cancelAnimation, 'cancelAnimation%d' % self.doId, [self])
        
    def sellFish(self):
        pass

    def sellFishComplete(self, todo0, todo1):
        pass

    def setMovie(self, todo0, todo1, todo2, todo3, todo4, todo5, todo6):
        pass

    def removeFromPier(self):
        self.cancelAnimation()
        self.sendUpdate('setOccupied', [0])
        self.avId = None
	
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
        self.sendUpdate('setMovie', [FishGlobals.PullInMovie, itemType, fish.getGenus(), fish.getSpecies(), fish.getWeight(), 0, 0])
        
	
    def cancelAnimation(self):
        self.sendUpdate('setMovie', [FishGlobals.NoMovie, 0, 0, 0, 0, 0, 0])