from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedNodeAI import DistributedNodeAI

class DistributedLawnDecorAI(DistributedNodeAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedLawnDecorAI")
    
    def __init__(self, air):
        DistributedNodeAI.__init__(self, air)
        self.plot = 0
        self.h = 0
        self.pos = (0, 0, 0)
        self.ownerIndex = 0

    def setPlot(self, plot):
        self.plot = plot

    def getPlot(self):
        return self.plot
        
    def setHeading(self, h):
        self.setH(h)
        self.h = h
        
    def getHeading(self):
        return self.h
        
    def setPosition(self, x, y, z):
        self.setPos(x, y, z)
        self.pos = (x, y, z)
        
    def d_setPosition(self, x, y, z):
        self.sendUpdate('setPos', [x, y, z])
        self.sendUpdate('setPosition', [x, y, z])
        
    def b_setPosition(self, x, y, z):
        self.setPosition(x, y, z)
        self.d_setPosition(x, y, z)
    
    def getPosition(self):
        return self.pos
        
    def getOwnerIndex(self):
        return self.ownerIndex

    def setOwnerIndex(self, index):
        self.ownerIndex = index

    def plotEntered(self):
        pass

    def removeItem(self):
        pass

    def setMovie(self, todo0, todo1):
        pass

    def movieDone(self):
        pass

    def interactionDenied(self, todo0):
        pass

