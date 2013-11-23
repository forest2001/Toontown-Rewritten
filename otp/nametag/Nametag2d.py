from Nametag import *
from otp.margins.MarginPopup import *
from pandac.PandaModules import *

class Nametag2d(Nametag, MarginPopup):
    SCALE_2D = 0.25
    CHAT_ALPHA = 0.5

    def __init__(self):
        Nametag.__init__(self)
        MarginPopup.__init__(self)

        self.contents = self.CName|self.CSpeech

        self.chatWordWrap = 7.5

        self.innerNP.setScale(self.SCALE_2D)

    def showBalloon(self, balloon, text):
        text = '%s: %s' % (self.displayName, text)
        Nametag.showBalloon(self, balloon, text)

        # Next, center the balloon in the cell:
        balloon = NodePath.anyPath(self).find('*/balloon')

        # Calculate the center of the TextNode.
        text = balloon.find('**/+TextNode')
        t = text.node()
        left, right, bottom, top = t.getLeft(), t.getRight(), t.getBottom(), t.getTop()
        center = self.innerNP.getRelativePoint(text,
                                               ((left+right)/2., 0, (bottom+top)/2.))

        # Next translate the balloon along the inverse.
        balloon.setPos(balloon, -center)

    def getSpeechBalloon(self):
        return NametagGlobals.speechBalloon2d

    def getThoughtBalloon(self):
        return NametagGlobals.thoughtBalloon2d
