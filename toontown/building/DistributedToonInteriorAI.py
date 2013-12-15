from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.distributed.ClockDelta import *
import cPickle

class DistributedToonInteriorAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedToonInteriorAI")
    
    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
    
    
    def setZoneIdAndBlock(self, zoneId, block):
        self.zoneId = zoneId
        self.block = block
        
    def d_setZoneIdAndBlock(self, zoneId, block):
        self.sendUpdate('setZoneIdAndBlock', [zoneId, block])
    
    def b_setZoneIdAndBlock(self, zoneId, block):
        self.setZoneIdAndBlock(zoneId, block)
        self.d_setZoneIdAndBlock(zoneId, block)
        
    def getZoneIdAndBlock(self):
        return [self.zoneId, self.block]

    def setToonData(self, toonData):
        pass
        
    def getToonData(self):
        return cPickle.dumps(None)

    def setState(self, state):
        self.timeStamp = globalClockDelta.getRealNetworkTime()
        self.state = state
    
    def getState(self):
        return [self.state, self.timeStamp]
