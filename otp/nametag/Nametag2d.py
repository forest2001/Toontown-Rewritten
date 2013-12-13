from Nametag import *
from otp.margins.MarginPopup import *
from pandac.PandaModules import *
import math

class Nametag2d(Nametag, MarginPopup):
    SCALE_2D = 0.25
    CHAT_ALPHA = 0.5
    ARROW_OFFSET = -1.0
    ARROW_SCALE = 1.5

    def __init__(self):
        Nametag.__init__(self)
        MarginPopup.__init__(self)

        self.contents = self.CName|self.CSpeech
        self.chatWordWrap = 7.5

        self.arrow = None

        self.innerNP.setScale(self.SCALE_2D)

    def showBalloon(self, balloon, text):
        text = '%s: %s' % (self.displayName, text)
        Nametag.showBalloon(self, balloon, text)

        # Next, center the balloon in the cell:
        balloon = NodePath.anyPath(self).find('*/balloon')

        # Calculate the center of the TextNode.
        text = balloon.find('**/+TextNode')
        t = text.node()
        left, right, bottom, top = t.getFrameActual()
        center = self.innerNP.getRelativePoint(text,
                                               ((left+right)/2., 0, (bottom+top)/2.))

        # Next translate the balloon along the inverse.
        balloon.setPos(balloon, -center)

        # When a balloon is active, we need to be somewhat higher-priority in the
        # popup system:
        self.setPriority(1)

        # Remove our pointer arrow:
        if self.arrow is not None:
            self.arrow.removeNode()
        self.arrow = None

    def showName(self):
        Nametag.showName(self)

        # Revert our priority back to basic:
        self.setPriority(0)

        # Tack on an arrow:
        t = self.innerNP.find('**/+TextNode')
        arrowZ = self.ARROW_OFFSET + t.node().getBottom()

        self.arrow = NametagGlobals.arrowModel.copyTo(self.innerNP)
        self.arrow.setZ(arrowZ)
        self.arrow.setScale(self.ARROW_SCALE)
        self.arrow.setColor(self.nameFg)

    def tick(self):
        # Update the arrow's pointing.
        if not self.isDisplayed() or self.arrow is None:
            return # No arrow or not onscreen.

        if self.avatar is None:
            return # No avatar, can't be done.

        # Get points needed in calculation:
        cam = NametagGlobals.camera or base.cam
        toon = NametagGlobals.toon or cam

        # libotp calculates this using the offset from localToon->avatar, but
        # the orientation from cam. Therefore, we duplicate it like so:
        location = self.avatar.getPos(toon)
        rotation = toon.getQuat(cam)

        camSpacePos = rotation.xform(location)
        arrowRadians = math.atan2(camSpacePos[0], camSpacePos[1])
        arrowDegrees = arrowRadians/math.pi*180

        self.arrow.setR(arrowDegrees - 90)

    def getSpeechBalloon(self):
        return NametagGlobals.speechBalloon2d

    def getThoughtBalloon(self):
        return NametagGlobals.thoughtBalloon2d
