from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

class DistributedHouseInteriorAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedHouseInteriorAI")
    
    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.houseId = 0
        self.houseIndex = 0
        self.wallpaper = ''
        self.windows = ''

    def setHouseId(self, houseId):
        self.houseId = houseId
        
    def getHouseId(self):
        return self.houseId

    def setHouseIndex(self, index):
        self.houseIndex = index

    def getHouseIndex(self):
        return self.houseIndex
    
    def setWallpaper(self, todo0):
        pass
        
    def getWallpaper(self):
        return self.wallpaper

    def setWindows(self, todo0):
        pass
        
    def getWindows(self):
        return self.windows

