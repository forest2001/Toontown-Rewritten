from direct.directnotify import DirectNotifyGlobal
from toontown.estate.DistributedLawnDecorAI import DistributedLawnDecorAI

class DistributedGardenBoxAI(DistributedLawnDecorAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedGardenBoxAI")
    
    def __init__(self, air):
        DistributedLawnDecorAI.__init__(self, air)
        self.typeIndex = 0

    def setTypeIndex(self, index):
        self.typeIndex = index
        
    def getTypeIndex(self):
        return self.typeIndex

