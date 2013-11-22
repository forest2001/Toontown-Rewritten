from Nametag import *
from otp.margins.MarginPopup import *
from pandac.PandaModules import *

class Nametag2d(Nametag, MarginPopup):
    SCALE_2D = 0.3

    def __init__(self):
        Nametag.__init__(self)
        MarginPopup.__init__(self)

        self.contents = self.CName|self.CSpeech

        self.innerNP.setScale(self.SCALE_2D)

    def showBalloon(self, balloon, text):
        text = '%s: %s' % (self.displayName, text)
        Nametag.showBalloon(self, balloon, text)

    def getSpeechBalloon(self):
        return NametagGlobals.speechBalloon2d

    def getThoughtBalloon(self):
        return NametagGlobals.thoughtBalloon2d
