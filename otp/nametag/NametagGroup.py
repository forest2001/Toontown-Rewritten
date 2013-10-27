from pandac.PandaModules import *
from NametagConstants import *
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
        self.nametag2d = Nametag2d()
        self.nametag3d = Nametag3d()
        self.icon = PandaNode('icon')

        self.chatTimeoutTask = None

        self.font = None
        self.name = ''
        self.displayName = ''
        self.qtColor = VBase4(1,1,1,1)

        self.chatString = ''
        self.chatFlags = 0

        self.nametags = []
        self.addNametag(self.nametag2d)
        self.addNametag(self.nametag3d)

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
        return self.chatString

    def getStompText(self):
        return ''

    def getUniqueId(self):
        return 'foo'

    def setActive(self, active):
        pass

    def setAvatar(self, avatar):
        pass

    def setFont(self, font):
        self.font = font

    def setColorCode(self, cc):
        pass

    def setName(self, name):
        self.name = name
        self.updateTags()

    def setDisplayName(self, name):
        self.displayName = name
        self.updateTags()

    def setQtColor(self, color):
        self.qtColor = color

    def setChat(self, chatString, chatFlags):
        self.chatString = chatString
        self.chatFlags = chatFlags
        self.updateTags()

        if chatFlags&CFTimeout:
            self._startChatTimeout()
        else:
            self._stopChatTimeout()

    def _startChatTimeout(self):
        self.chatTimeoutTask = taskMgr.doMethodLater(5, self.__doChatTimeout,
                                                     'ChatTimeout-%d' % id(self))

    def __doChatTimeout(self, task):
        self.setChat('', 0)
        return task.done

    def _stopChatTimeout(self):
        if self.chatTimeoutTask:
            taskMgr.remove(self.chatTimeoutTask)

    def clearShadow(self):
        pass

    def clearChat(self):
        self.setChat('', 0)

    def updateNametag(self, tag):
        tag.font = self.font
        tag.name = self.name
        tag.displayName = self.displayName
        tag.qtColor = self.qtColor
        tag.chatString = self.chatString
        tag.chatFlags = self.chatFlags

        tag.update()

    def updateTags(self):
        for nametag in self.nametags:
            self.updateNametag(nametag)

    def addNametag(self, nametag):
        self.nametags.append(nametag)
        self.updateNametag(nametag)

    def removeNametag(self, nametag):
        self.nametags.remove(nametag)

    def manage(self, manager):
        pass

    def unmanage(self, manager):
        pass
