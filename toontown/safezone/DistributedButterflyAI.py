from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.distributed.ClockDelta import *
import ButterflyGlobals
import random

class DistributedButterflyAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedButterflyAI")

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.area = 0
        self.playground = 0
        self.stateIndex = 0
        self.curIndex = 0
        self.destIndex = 0
        self.time = 0
        self.timestamp = 0
    
    def generate(self):
        fr = ButterflyGlobals.getFirstRoute(self.playground, self.area, self.doId)
        self.b_setState(ButterflyGlobals.FLYING, fr[1], fr[3], fr[4], globalClockDelta.getRealNetworkTime())
        taskMgr.doMethodLater(fr[4], self.__land, 'landButterfly%i' % self.doId, [])
    
    def __land(self):
        ttl = random.uniform(0, ButterflyGlobals.MAX_LANDED_TIME)
        self.b_setState(ButterflyGlobals.LANDED, self.curIndex, self.destIndex, ttl, globalClockDelta.getRealNetworkTime())
        taskMgr.doMethodLater(ttl, self.__fly, 'flyButterfly%i' % self.doId, [])
        
    def __fly(self):
        next = ButterflyGlobals.getNextPos(ButterflyGlobals.ButterflyPoints[self.playground][self.area][self.destIndex], self.playground, self.area, self.doId)
        self.b_setState(ButterflyGlobals.FLYING, self.destIndex, next[1], next[2], globalClockDelta.getRealNetworkTime())
        taskMgr.doMethodLater(next[2], self.__land, 'landButterfly%i' % self.doId, [])
    
    def setArea(self, playground, area):
        self.area = area
        self.playground = playground
        
    def d_setArea(self, playground, area):
        self.sendUpdate('setArea', [playground, area])
        
    def b_setArea(self, playground, area):
        self.setArea(playground, area)
        self.d_setArea(playground, area)
        
    def getArea(self):
        return [self.playground, self.area]

    def setState(self, stateIndex, curIndex, destIndex, time, timestamp):
        self.stateIndex = stateIndex
        self.curIndex = curIndex
        self.destIndex = destIndex
        self.time = time
        self.timestamp = timestamp
        
    def d_setState(self, stateIndex, curIndex, destIndex, time, timestamp):
        self.sendUpdate('setState', [stateIndex, curIndex, destIndex, time, timestamp])
        
    def b_setState(self, stateIndex, curIndex, destIndex, time, timestamp):
        self.setState(stateIndex, curIndex, destIndex, time, timestamp)
        self.d_setState(stateIndex, curIndex, destIndex, time, timestamp)
        
    def getState(self):
        return [self.stateIndex, self.curIndex, self.destIndex, self.time, self.timestamp]

    def avatarEnter(self):
        pass

