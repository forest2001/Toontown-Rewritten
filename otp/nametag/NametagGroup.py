from pandac.PandaModules import *
from NametagConstants import *
from Nametag3d import *
from Nametag2d import *

class NametagGroup:
    CCNormal = CCNormal
    CCNoChat = CCNoChat
    CCNonPlayer = CCNonPlayer
    CCSuit = CCSuit
    CCToonBuilding = CCToonBuilding
    CCSuitBuilding = CCSuitBuilding
    CCHouseBuilding = CCHouseBuilding
    CCSpeedChat = CCSpeedChat
    CCFreeChat = CCFreeChat

    CHAT_TIMEOUT_MAX = 12.0
    CHAT_TIMEOUT_MIN = 4.0
    CHAT_TIMEOUT_PROP = 0.5

    def __init__(self):
        self.nametag2d = Nametag2d()
        self.nametag3d = Nametag3d()
        self.icon = PandaNode('icon')

        self.chatTimeoutTask = None

        self.font = None
        self.name = ''
        self.displayName = ''
        self.qtColor = VBase4(1,1,1,1)
        self.colorCode = CCNormal
        self.avatar = None
        self.active = True

        self.chatString = ''
        self.chatFlags = 0

        self.objectCode = None

        self.manager = None

        self.nametags = []
        self.addNametag(self.nametag2d)
        self.addNametag(self.nametag3d)

        self.visible3d = True # Is a 3D nametag visible, or do we need a 2D popup?

        self.tickTask = taskMgr.add(self.__tickTask, self.getUniqueId(), sort=45)

    def destroy(self):
        taskMgr.remove(self.tickTask)
        if self.manager is not None:
            self.unmanage(self.manager)
        for nametag in list(self.nametags):
            self.removeNametag(nametag)

    def getNametag2d(self):
        return self.nametag2d

    def getNametag3d(self):
        return self.nametag3d

    def getNameIcon(self):
        return self.icon

    def getNumChatPages(self):
        return 1 if self.chatString and self.chatFlags else 0

    def getChatStomp(self):
        return 0

    def getChat(self):
        return self.chatString

    def getStompText(self):
        return ''

    def getStompDelay(self):
        return 0.0

    def getUniqueId(self):
        return 'Nametag-%d' % id(self)

    def hasButton(self):
        return False # TODO: Support buttons

    def setActive(self, active):
        self.active = active

    def isActive(self):
        return self.active

    def setAvatar(self, avatar):
        self.avatar = avatar

    def setFont(self, font):
        self.font = font
        self.updateTags()

    def setColorCode(self, cc):
        self.colorCode = cc
        self.updateTags()

    def setName(self, name):
        self.name = name
        self.updateTags()

    def setDisplayName(self, name):
        self.displayName = name
        self.updateTags()

    def setQtColor(self, color):
        self.qtColor = color
        self.updateTags()

    def setChat(self, chatString, chatFlags):
        self.chatString = chatString
        self.chatFlags = chatFlags
        self.updateTags()

        self._stopChatTimeout()
        if chatFlags&CFTimeout:
            self._startChatTimeout()

    def setContents(self, contents):
        # This function is a little unique, it's meant to override contents on
        # EXISTING nametags only:
        for tag in self.nametags:
            tag.setContents(contents)

    def setObjectCode(self, objectCode):
        self.objectCode = objectCode

    def getObjectCode(self):
        return self.objectCode

    def _startChatTimeout(self):
        length = len(self.chatString)
        timeout = min(max(length*self.CHAT_TIMEOUT_PROP, self.CHAT_TIMEOUT_MIN), self.CHAT_TIMEOUT_MAX)
        self.chatTimeoutTask = taskMgr.doMethodLater(timeout, self.__doChatTimeout,
                                                     'ChatTimeout-' + self.getUniqueId())

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
        tag.displayName = self.displayName or self.name
        tag.qtColor = self.qtColor
        tag.colorCode = self.colorCode
        tag.chatString = self.chatString
        tag.chatFlags = self.chatFlags
        tag.avatar = self.avatar
        tag.icon = self.icon

        if self.active:
            tag.setClickRegionEvent(self.getUniqueId())
        else:
            tag.setClickRegionEvent(None)

        tag.update()

    def __tickTask(self, task):
        for nametag in self.nametags:
            nametag.tick()

        if self.avatar is None: return
        pos = self.avatar.getPos(NametagGlobals.camera)
        visible3d = NametagGlobals.camera.node().getLens().project(pos, Point2())

        if self.avatar.isHidden():
            visible3d = False

        if NametagGlobals.onscreenChatForced and self.chatFlags & CFSpeech:
            visible3d = False

        if visible3d ^ self.visible3d:
            self.visible3d = visible3d
            for nametag in self.nametags:
                if isinstance(nametag, MarginPopup):
                    nametag.setVisible(not visible3d)

        return task.cont

    def updateTags(self):
        for nametag in self.nametags:
            self.updateNametag(nametag)

    def addNametag(self, nametag):
        self.nametags.append(nametag)
        self.updateNametag(nametag)
        if self.manager is not None and isinstance(nametag, MarginPopup):
            nametag.manage(manager)

    def removeNametag(self, nametag):
        self.nametags.remove(nametag)
        if self.manager is not None and isinstance(nametag, MarginPopup):
            nametag.unmanage(manager)
        nametag.destroy()

    def manage(self, manager):
        self.manager = manager
        for tag in self.nametags:
            if isinstance(tag, MarginPopup):
                tag.manage(manager)

    def unmanage(self, manager):
        self.manager = None
        for tag in self.nametags:
            if isinstance(tag, MarginPopup):
                tag.unmanage(manager)
                
    def setNameWordwrap(self, wrap):
        pass
