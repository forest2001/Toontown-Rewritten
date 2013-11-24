from direct.directnotify import DirectNotifyGlobal
from toontown.racing.DistributedKartPadAI import DistributedKartPadAI
from direct.distributed.ClockDelta import *

class DistributedViewPadAI(DistributedKartPadAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedViewPadAI")
    
    def __init__(self, air):
        DistributedKartPadAI.__init__(self, air)
        self.timestamp = globalClockDelta.getRealNetworkTime()
    
    def setLastEntered(self, timestamp):
        self.timestamp = timestamp
        
    def d_setLastEntered(self, timestamp):
        self.sendUpdate('setLastEntered', [timestamp])
        
    def b_setLastEntered(self, timestamp):
        self.setLastEntered(timestamp)
        self.d_setLastEntered(timestamp)
        
    def getLastEntered(self):
        return self.timestamp
        
    def updateTimer(self):
        self.b_setLastEntered(globalClockDelta.getRealNetworkTime())

