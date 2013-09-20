# 2013.08.22 22:15:47 Pacific Daylight Time
# Embedded file name: otp.speedchat.SCCustomMenu
from SCMenu import SCMenu
from SCCustomTerminal import SCCustomTerminal
from otp.otpbase.OTPLocalizer import CustomSCStrings

class SCCustomMenu(SCMenu):
    __module__ = __name__

    def __init__(self):
        SCMenu.__init__(self)
        self.accept('customMessagesChanged', self.__customMessagesChanged)
        self.__customMessagesChanged()

    def destroy(self):
        SCMenu.destroy(self)

    def __customMessagesChanged(self):
        self.clearMenu()
        try:
            lt = base.localAvatar
        except:
            return

        for msgIndex in lt.customMessages:
            if CustomSCStrings.has_key(msgIndex):
                self.append(SCCustomTerminal(msgIndex))
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\otp\speedchat\SCCustomMenu.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:15:47 Pacific Daylight Time
