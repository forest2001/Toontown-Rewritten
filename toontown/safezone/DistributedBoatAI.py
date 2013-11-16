from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.distributed.ClockDelta import *

class DistributedBoatAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedBoatAI")
    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.state = 'DockedEast'
    def setState(self, state, timestamp):
        self.sendUpdate('setState', [self.state, globalClockDelta.getRealNetworkTime()])
    def getState(self):
        return (self.state, globalClockDelta.getRealNetworkTime())
