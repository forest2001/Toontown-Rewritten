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
        self.wordWrap = None
        self.qtColor = VBase4(1,1,1,1)
        self.colorCode = CCNormal
        self.avatar = None
        self.active = True

        self.chatPages = []
        self.chatPage = 0
        self.chatFlags = 0

        self.objectCode = None

        self.manager = None

        self.nametags = []
        self.addNametag(self.nametag2d)
        self.addNametag(self.nametag3d)

        self.visible3d = True # Is a 3D nametag visible, or do we need a 2D popup?

        self.tickTask = taskMgr.add(self.__tickTask, self.getUniqueId(), sort=45)

        self.stompTask = None
        self.stompText = None
        self.stompFlags = 0

    def destroy(self):
        taskMgr.remove(self.tickTask)
        if self.manager is not None:
            self.unmanage(self.manager)
        for nametag in list(self.nametags):
            self.removeNametag(nametag)
        if self.stompTask:
            self.stompTask.remove()

    def getNametag2d(self):
        return self.nametag2d

    def getNametag3d(self):
        return self.nametag3d

    def getNameIcon(self):
        return self.icon

    def getNumChatPages(self):
        if not self.chatFlags & (CFSpeech|CFThought):
            return 0

        return len(self.chatPages)

    def setPageNumber(self, page):
        self.chatPage = page
        self.updateTags()

    def getChatStomp(self):
        return bool(self.stompTask)

    def getChat(self):
        if self.chatPage >= len(self.chatPages):
            return ''
        else:
            return self.chatPages[self.chatPage]

    def getStompText(self):
        return self.stompText

    def getStompDelay(self):
        return 0.2

    def getUniqueId(self):
        return 'Nametag-%d' % id(self)

    def hasButton(self):
        return bool(self.getButtons())

    def getButtons(self):
        if self.getNumChatPages() < 2:
            # Either only one page or no pages displayed. This means no button,
            # unless the game code specifically requests one.
            if self.chatFlags & CFPageButton:
                return NametagGlobals.pageButtons
            elif self.chatFlags & CFQuitButton:
                return NametagGlobals.quitButtons
            else:
                return None
        elif self.chatPage == self.getNumChatPages()-1:
            # Last page of a multiple-page chat. This calls for a quit button,
            # unless the game says otherwise.
            if not self.chatFlags & CFNoQuitButton:
                return NametagGlobals.quitButtons
            else:
                return None
        else:
            # Non-last page of a multiple-page chat. This calls for a page
            # button, but only if the game requests it:
            if self.chatFlags & CFPageButton:
                return NametagGlobals.pageButtons
            else:
                return None

    def setActive(self, active):
        self.active = active

    def isActive(self):
        return self.active

    def setAvatar(self, avatar):
        self.avatar = avatar

    def setFont(self, font):
        self.font = font
        self.updateTags()

    def setWordwrap(self, wrap):
        self.wordWrap = wrap
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
        if not self.chatFlags&CFSpeech:
            # We aren't already displaying some chat. Therefore, we don't have
            # to stomp.
            self._setChat(chatString, chatFlags)
        else:
            # Stomp!
            self.clearChat()
            self.stompText = chatString
            self.stompFlags = chatFlags
            self.stompTask = taskMgr.doMethodLater(self.getStompDelay(), self.__updateStomp,
                                                   'ChatStomp-' + self.getUniqueId())

    def _setChat(self, chatString, chatFlags):
        if chatString:
            self.chatPages = chatString.split('\x07')
            self.chatFlags = chatFlags
        else:
            self.chatPages = []
            self.chatFlags = 0
        self.setPageNumber(0) # Calls updateTags() for us.

        self._stopChatTimeout()
        if chatFlags&CFTimeout:
            self._startChatTimeout()

    def __updateStomp(self, task):
        self._setChat(self.stompText, self.stompFlags)
        self.stompTask = None

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
        length = len(self.getChat())
        timeout = min(max(length*self.CHAT_TIMEOUT_PROP, self.CHAT_TIMEOUT_MIN), self.CHAT_TIMEOUT_MAX)
        self.chatTimeoutTask = taskMgr.doMethodLater(timeout, self.__doChatTimeout,
                                                     'ChatTimeout-' + self.getUniqueId())

    def __doChatTimeout(self, task):
        self._setChat('', 0)
        return task.done

    def _stopChatTimeout(self):
        if self.chatTimeoutTask:
            taskMgr.remove(self.chatTimeoutTask)

    def clearShadow(self):
        pass

    def clearChat(self):
        self._setChat('', 0)
        if self.stompTask:
            self.stompTask.remove()

    def updateNametag(self, tag):
        tag.font = self.font
        tag.name = self.name
        tag.wordWrap = self.wordWrap or DEFAULT_WORDWRAPS[self.colorCode]
        tag.displayName = self.displayName or self.name
        tag.qtColor = self.qtColor
        tag.colorCode = self.colorCode
        tag.chatString = self.getChat()
        tag.buttons = self.getButtons()
        tag.chatFlags = self.chatFlags
        tag.avatar = self.avatar
        tag.icon = self.icon

        tag.update()

    def __testVisible3D(self):
        # We must determine if a 3D nametag is visible or not, since this
        # affects the visibility state of 2D nametags.

        # Next, we iterate over all of our nametags until we find a visible
        # one:
        for nametag in self.nametags:
            if not isinstance(nametag, Nametag3d):
                continue # It's not in the 3D system, disqualified.

            if nametag.isOnScreen():
                return True

        # If we got here, none of the tags were a match...
        return False


    def __tickTask(self, task):
        for nametag in self.nametags:
            nametag.tick()
            if (NametagGlobals.masterNametagsActive and self.active) or self.hasButton():
                nametag.setClickRegionEvent(self.getUniqueId())
            else:
                nametag.setClickRegionEvent(None)

        if NametagGlobals.onscreenChatForced and self.chatFlags & CFSpeech:
            # Because we're *forcing* chat onscreen, we skip the visible3d test
            # and go ahead and display it anyway.
            visible3d = False
        elif not NametagGlobals.masterArrowsOn:
            # We're forcing margins offscreen; therefore, we should pretend
            # that the 3D nametag is always visible.
            visible3d = True
        else:
            visible3d = self.__testVisible3D()

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
