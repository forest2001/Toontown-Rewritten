# 2013.08.22 22:25:09 Pacific Daylight Time
# Embedded file name: toontown.speedchat.TTSCResistanceMenu
from direct.showbase import PythonUtil
from otp.speedchat.SCMenu import SCMenu
from otp.speedchat.SCMenuHolder import SCMenuHolder
from toontown.chat import ResistanceChat
from TTSCResistanceTerminal import TTSCResistanceTerminal

class TTSCResistanceMenu(SCMenu):
    __module__ = __name__

    def __init__(self):
        SCMenu.__init__(self)
        self.accept('resistanceMessagesChanged', self.__resistanceMessagesChanged)
        self.__resistanceMessagesChanged()
        submenus = []

    def destroy(self):
        SCMenu.destroy(self)

    def clearMenu(self):
        SCMenu.clearMenu(self)

    def __resistanceMessagesChanged(self):
        self.clearMenu()
        try:
            lt = base.localAvatar
        except:
            return

        phrases = lt.resistanceMessages
        for menuIndex in ResistanceChat.resistanceMenu:
            menu = SCMenu()
            for itemIndex in ResistanceChat.getItems(menuIndex):
                textId = ResistanceChat.encodeId(menuIndex, itemIndex)
                charges = lt.getResistanceMessageCharges(textId)
                if charges > 0:
                    menu.append(TTSCResistanceTerminal(textId, charges))

            textId = ResistanceChat.encodeId(menuIndex, 0)
            menuName = ResistanceChat.getMenuName(textId)
            self.append(SCMenuHolder(menuName, menu))
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\speedchat\TTSCResistanceMenu.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:25:09 Pacific Daylight Time
