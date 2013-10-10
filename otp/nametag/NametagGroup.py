from pandac.PandaModules import *
from Nametag3d import *

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
        self.nametag2d = None
        self.nametag3d = Nametag3d('')
        self.icon = PandaNode('icon')

    def getNametag3d(self):
        return self.nametag3d

    def getNameIcon(self):
        return self.icon

    def setAvatar(self, avatar):
        pass

    def setFont(self, font):
        pass

    def setColorCode(self, cc):
        pass
