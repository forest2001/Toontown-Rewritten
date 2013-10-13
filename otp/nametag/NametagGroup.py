from pandac.PandaModules import *
from Nametag3d import *
from Nametag2d import *

class NametagGroup:
    CCNormal = 0
    CCNoChat = 1
    CCNonPlayer = 2
    CCSuit = 3
    CCToonBuilding = 4
    CCSuitBuilding = 5
    CCHouseBuilding = 6
    CCSpeedChat = 7
    CCFreeChat = 8

    def __init__(self):
        self.nametag2d = Nametag2d('')
        self.nametag3d = Nametag3d('')
        self.icon = PandaNode('icon')

    def getNametag2d(self):
        return self.nametag2d

    def getNametag3d(self):
        return self.nametag3d

    def getNameIcon(self):
        return self.icon

    def setActive(self, active):
        pass

    def setAvatar(self, avatar):
        pass

    def setFont(self, font):
        pass

    def setColorCode(self, cc):
        pass
