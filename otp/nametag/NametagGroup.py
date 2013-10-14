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

    def getNumChatPages(self):
        return 0

    def getChatStomp(self):
        return 0

    def getChat(self):
        return ''

    def getStompText(self):
        return ''

    def getUniqueId(self):
        return 'foo'

    def setActive(self, active):
        pass

    def setAvatar(self, avatar):
        pass

    def setFont(self, font):
        pass

    def setColorCode(self, cc):
        pass

    def setName(self, name):
        pass

    def setDisplayName(self, name):
        pass

    def setQtColor(self, color):
        pass

    def setChat(self, chatString, chatFlags):
        pass

    def clearShadow(self):
        pass

    def manage(self, manager):
        pass
