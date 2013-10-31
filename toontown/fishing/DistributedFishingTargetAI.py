from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedNodeAI import DistributedNodeAI
from direct.distributed.ClockDelta import *
from toontown.fishing import FishingTargetGlobals
from direct.task import Task
import random

class DistributedFishingTargetAI(DistributedNodeAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedFishingTargetAI")
	
    def __init__(self, air):
        DistributedNodeAI.__init__(self, air)
        self.pondId = 0
        self.angle = 0
        self.targetRadius = 0
        self.time = 0
        self.stateIndex = 0
    
    def generate(self):
        DistributedNodeAI.generate(self)
        self.updateState()
        pond = self.air.doId2do[self.pondId]
        pond.addTarget(self)
    def setPondDoId(self, pondId):
        self.pondId = pondId
        
    def getPondDoId(self):
        return self.pondId
        
    def setState(self, stateIndex, angle, radius, time, timeStamp):
        self.angle = angle
        self.targetRadius = radius
        self.time = time
        
    def getState(self):
        return [self.stateIndex, self.angle, self.targetRadius, self.time, globalClockDelta.getRealNetworkTime()]
        
    def updateState(self):
        self.stateIndex += 1
        self.angle = random.randrange(359)
        self.targetRadius = random.uniform(FishingTargetGlobals.getTargetRadius(self.air.doId2do[self.pondId].getArea()), 0)
        self.time = random.uniform(10.0, 5.0)
        self.sendUpdate('setState', [self.stateIndex, self.angle, self.targetRadius, self.time, globalClockDelta.getRealNetworkTime()])
        taskMgr.doMethodLater(self.time + random.uniform(5, 2.5), DistributedFishingTargetAI.updateState, 'updateFishingTarget', [self])
        
        