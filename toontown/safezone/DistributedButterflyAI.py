from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
import ButterflyGlobals

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

    def avatarEnter(self):
        pass

