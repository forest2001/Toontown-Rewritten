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

        self.updateContents()

        self.setPriority(2)
        self.setVisible(True)

    def updateContents(self):
        if self.whisperType in WHISPER_COLORS:
            cc = self.whisperType
        else:
            cc = WTSystem
        fgColor, bgColor = WHISPER_COLORS[cc][0]

        balloon = NametagGlobals.speechBalloon2d.generate(
            self.text, self.font, textColor=fgColor, balloonColor=bgColor,
            wordWrap=self.WORDWRAP)
        balloon.reparentTo(self.innerNP)

        # Calculate the center of the TextNode.
        text = balloon.find('**/+TextNode')
        t = text.node()
        left, right, bottom, top = t.getFrameActual()
        center = self.innerNP.getRelativePoint(text,
                                               ((left+right)/2., 0, (bottom+top)/2.))

        # Next translate the balloon along the inverse.
        balloon.setPos(balloon, -center)

    def setClickable(self, senderName, fromId, todo=0):
        pass

    def manage(self, manager):
        MarginPopup.manage(self, manager)

        taskMgr.doMethodLater(self.timeout, self.unmanage,
                              'whisper-timeout-%d' % id(self), [manager])
