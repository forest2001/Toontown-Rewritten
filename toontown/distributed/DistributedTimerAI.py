from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.distributed.ClockDelta import *
import time

class DistributedTimerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedTimerAI")

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.setStartTime(globalClockDelta.getRealNetworkTime(bits = 32))

    def setStartTime(self, time):
        self.startTime = time

    def getStartTime(self):
        return self.startTime

