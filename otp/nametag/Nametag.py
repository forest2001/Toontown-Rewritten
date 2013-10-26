from NametagConstants import *
import NametagGlobals
from otp.margins.ClickablePopup import ClickablePopup

class Nametag(ClickablePopup):
    CName = 1
    CSpeech = 2
    CThought = 4

    def __init__(self):
        ClickablePopup.__init__(self)
        self.contents = 0

        self.font = None
        self.name = ''
        self.displayName = ''

        self.chatString = ''
        self.chatFlags = 0

    def setContents(self, contents):
        self.contents = contents

    def update(self):
        self.removeAllChildren()
        if self.contents&self.CThought and self.chatFlags&CFThought:
            self.showThought()
        elif self.contents&self.CSpeech and self.chatFlags&CFSpeech:
            self.showSpeech()
        elif self.contents&self.CName:
            self.showName()

    def showThought(self):
        pass

    def showSpeech(self):
        pass

    def showName(self):
        pass
