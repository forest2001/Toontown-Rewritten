from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

class DistributedHouseAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedHouseAI")
    
    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.houseType = 0
        self.gardenPos = 0
        self.avatarId = 0
        self.name = ''
        self.color = 0
        self.housePos = 0
        
    def announceGenerate(self):
        DistributedObjectAI.announceGenerate(self)
        self.sendUpdate('setHouseReady', [])

    def setHousePos(self, pos):
        self.housePos = pos
        
    def d_setHousePos(self, pos):
        self.sendUpdate('setHousePos', [pos])
        
    def b_setHousePos(self, pos):
        self.setHousePos(pos)
        self.d_setHousePos(pos)
        
    def getHousePos(self):
        return self.housePos

    def setHouseType(self, type):
        self.houseType = houseType
        
    def d_setHouseType(self, type):
        self.sendUpdate('setHouseType', [type])
    
    def b_setHouseType(self, type):
        self.setHouseType(type)
        self.d_setHouseType(type)
        
    def getHouseType(self):
        return self.houseType

    def setGardenPos(self, pos):
        self.gardenPos = pos
        
    def d_setGardenPos(self, pos):
        self.sendUpdate('setGardenPos', [pos])
        
    def b_setGardenPos(self, pos):
        self.setGardenPow(pos)
        self.d_setGardenPos(pos)
        
    def getGardenPos(self):
        return self.gardenPos

    def setAvatarId(self, avId):
        self.avatarId = avId
        
    def d_setAvatarId(self, avId):
        self.sendUpdate('setAvatarId', [avId])
        
    def b_setAvatarId(self, avId):
        self.setAvatarId(avId)
        self.d_setAvatarId(avId)
        
    def getAvatarId(self):
        return self.avatarId

    def setName(self, name):
        self.name = name
        
    def d_setName(self, name):
        self.sendUpdate('setName', [name])
        
    def b_setName(self, name):
        self.setName(name)
        self.d_setName(name)
        
    def getName(self):
        return self.name

    def setColor(self, color):
        self.color = color
        
    def d_setColor(self, color):
        self.sendUpdate('setColor', [color])
        
    def b_setColor(self, color):
        self.setColor(color)
        self.d_setColor(color)
        
    def getColor(self):
        return self.color

    def setAtticItems(self, todo0):
        pass
        
    def getAtticItems(self):
        return '' #TODO

    def setInteriorItems(self, todo0):
        pass
        
    def getInteriorItems(self):
        return '' #TODO

    def setAtticWallpaper(self, todo0):
        pass
        
    def getAtticWallpaper(self):
        return '' #TODO

    def setInteriorWallpaper(self, todo0):
        pass
        
    def getInteriorWallpaper(self):
        return '' #TODO

    def setAtticWindows(self, todo0):
        pass

    def getAtticWindows(self):
        return ''
        
    def setInteriorWindows(self, todo0):
        pass
        
    def getInteriorWindows(self):
        return ''

    def setDeletedItems(self, todo0):
        pass
        
    def getDeletedItems(self):
        return ''

    def setCannonEnabled(self, todo0):
        pass
        
    def getCannonEnabled(self):
        return 0

    def setHouseReady(self):
        pass

