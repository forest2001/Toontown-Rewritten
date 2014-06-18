from MarginPopup import *
from ClickablePopup import *
from otp.nametag import NametagGlobals
from otp.nametag.NametagConstants import *

class WhisperPopup(MarginPopup, ClickablePopup):
    WTNormal = WTNormal
    WTQuickTalker = WTQuickTalker
    WTSystem = WTSystem
    WTBattleSOS = WTBattleSOS
    WTEmote = WTEmote
    WTToontownBoardingGroup = WTToontownBoardingGroup

    WORDWRAP = 7.5
    SCALE_2D = 0.25

    def __init__(self, text, font, whisperType, timeout=10.0):
        ClickablePopup.__init__(self)
        MarginPopup.__init__(self)

        self.innerNP = NodePath.anyPath(self).attachNewNode('innerNP')
        self.innerNP.setScale(self.SCALE_2D)

        self.text = text
        self.font = font
        self.whisperType = whisperType
        self.timeout = timeout

        self.active = False
        self.fromId = 0

        self.left = 0.0
        self.right = 0.0
        self.bottom = 0.0
        self.top = 0.0

        self.updateContents()

        self.setPriority(2)
        self.setVisible(True)

    def updateContents(self):
        if self.whisperType in WHISPER_COLORS:
            cc = self.whisperType
        else:
            cc = WTSystem

        # This line litterly makes me sick
        clickState = 0
        if self.active:
            clickState = self.getClickState()

        fgColor, bgColor = WHISPER_COLORS[cc][clickState]

        balloon, frame = NametagGlobals.speechBalloon2d.generate(
            self.text, self.font, textColor=fgColor, balloonColor=bgColor,
            wordWrap=self.WORDWRAP)
        balloon.reparentTo(self.innerNP)

        # Calculate the center of the TextNode.
        text = balloon.find('**/+TextNode')
        t = text.node()

        # Get the frame of the textNode
        self.left, self.right, self.bottom, self.top = t.getFrameActual()
        center = self.innerNP.getRelativePoint(text, ((self.left + self.right) / 2.0, 0, (self.bottom + self.top) / 2.0))

        # Next translate the balloon along the inverse.
        balloon.setPos(balloon, -center)

        # Now lets check if the popup is active and if
        # it's from an avatar
        if self.active and self.fromId:
            self.setClickRegionEvent('clickedWhisper', clickArgs=[self.fromId])
        else:
            self.setClickRegionEvent(None)

    def setClickable(self, senderName, fromId, isPlayer=0):
        self.active = True
        self.fromId = fromId

        self.updateContents()
        self.__updateClickRegion()

    def marginVisibilityChanged(self):
        self.__updateClickRegion()

    def __updateClickRegion(self):
        if self.isDisplayed() and self.active:
            self.updateClickRegion(self.left, self.right, self.bottom, self.top)

    def clickStateChanged(self):
        self.updateContents()

    def manage(self, manager):
        MarginPopup.manage(self, manager)

        taskMgr.doMethodLater(self.timeout, self.unmanage, 'whisper-timeout-%d' % id(self), [manager])

    # Manually cleanup
    def unmanage(self, manager):
        MarginPopup.unmanage(self, manager)

        ClickablePopup.destroy(self)
        self.innerNP.removeNode()
