# 2013.08.22 22:15:47 Pacific Daylight Time
# Embedded file name: otp.speedchat.SCEmoteMenu
from SCMenu import SCMenu
from SCEmoteTerminal import SCEmoteTerminal

class SCEmoteMenu(SCMenu):
    __module__ = __name__

    def __init__(self):
        SCMenu.__init__(self)
        self.accept('emotesChanged', self.__emoteAccessChanged)
        self.__emoteAccessChanged()

    def destroy(self):
        SCMenu.destroy(self)

    def __emoteAccessChanged(self):
        self.clearMenu()
        try:
            lt = base.localAvatar
        except:
            return

        for i in range(len(lt.emoteAccess)):
            if lt.emoteAccess[i]:
                self.append(SCEmoteTerminal(i))
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\otp\speedchat\SCEmoteMenu.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:15:47 Pacific Daylight Time
