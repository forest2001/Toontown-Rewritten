# 2013.08.22 22:25:08 Pacific Daylight Time
# Embedded file name: toontown.speedchat.TTSCCogMenu
from otp.speedchat.SCMenu import SCMenu
from otp.speedchat.SCStaticTextTerminal import SCStaticTextTerminal

class TTSCCogMenu(SCMenu):
    __module__ = __name__

    def __init__(self, indices):
        SCMenu.__init__(self)
        for index in indices:
            term = SCStaticTextTerminal(index)
            self.append(term)

    def destroy(self):
        SCMenu.destroy(self)
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\speedchat\TTSCCogMenu.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:25:08 Pacific Daylight Time
