from NametagConstants import *
import NametagGlobals
from otp.margins.ClickablePopup import ClickablePopup
from pandac.PandaModules import *

class Nametag(ClickablePopup):
    CName = 1
    CSpeech = 2
    CThought = 4

    NAME_PADDING = 0.2
    CHAT_ALPHA = 1.0

    DEFAULT_CHAT_WORDWRAP = 10.0

    IS_3D = False # 3D variants will set this to True.

    def __init__(self):
        if self.IS_3D:
            ClickablePopup.__init__(self, NametagGlobals.camera)
        else:
            ClickablePopup.__init__(self)

        self.contents = 0 # To be set by subclass.

        self.innerNP = NodePath.anyPath(self).attachNewNode('nametag_contents')

        self.wordWrap = 7.5
        self.chatWordWrap = None

        self.font = None
        self.name = ''
        self.displayName = ''
        self.qtColor = VBase4(1,1,1,1)
        self.colorCode = CCNormal
        self.avatar = None
        self.icon = NodePath('icon')

        self.frame = (0, 0, 0, 0)

        self.nameFg = (0,0,0,1)
        self.nameBg = (1,1,1,1)
        self.chatFg = (0,0,0,1)
        self.chatBg = (1,1,1,1)

        self.chatString = ''
        self.chatFlags = 0

    def destroy(self):
        ClickablePopup.destroy(self)

    def setContents(self, contents):
        self.contents = contents
        self.update()

    def setAvatar(self, avatar):
        self.avatar = avatar

    def setChatWordwrap(self, chatWordWrap):
        self.chatWordWrap = chatWordWrap

    def tick(self):
        pass # Does nothing by default.

    def clickStateChanged(self):
        self.update()

    def getButton(self):
        cs = self.getClickState()
        if self.buttons is None:
            return None
        elif cs in self.buttons:
            return self.buttons[cs]
        else:
            return self.buttons.get(0)

    def update(self):
        if self.colorCode in NAMETAG_COLORS:
            cc = self.colorCode
        else:
            cc = CCNormal

        self.nameFg, self.nameBg, self.chatFg, self.chatBg = NAMETAG_COLORS[cc][self.getClickState()]

        self.innerNP.node().removeAllChildren()
        if self.contents&self.CThought and self.chatFlags&CFThought:
            self.showThought()
        elif self.contents&self.CSpeech and self.chatFlags&CFSpeech:
            self.showSpeech()
        elif self.contents&self.CName and self.displayName:
            self.showName()

    def showBalloon(self, balloon, text):
        color = self.qtColor if (self.chatFlags&CFQuicktalker) else self.chatBg
        if color[3] > self.CHAT_ALPHA:
            color = (color[0], color[1], color[2], self.CHAT_ALPHA)

        reversed = (self.IS_3D and (self.chatFlags&CFReversed))

        balloon, frame = balloon.generate(text, self.font, textColor=self.chatFg,
                                          balloonColor=color,
                                          wordWrap=self.chatWordWrap or \
                                            self.DEFAULT_CHAT_WORDWRAP,
                                          button=self.getButton(),
                                          reversed=reversed)
        balloon.reparentTo(self.innerNP)
        self.frame = frame

    def showThought(self):
        self.showBalloon(self.getThoughtBalloon(), self.chatString)

    def showSpeech(self):
        self.showBalloon(self.getSpeechBalloon(), self.chatString)

    def showName(self):
        if not self.font:
            # If no font is set, we can't actually display a name yet...
            return

        # Create text node:
        self.innerNP.attachNewNode(self.icon)
        t = self.innerNP.attachNewNode(TextNode('name'), 1)
        t.node().setFont(self.font)
        t.node().setAlign(TextNode.ACenter)
        t.node().setWordwrap(self.wordWrap)
        t.node().setText(self.displayName)
        t.setColor(self.nameFg)
        t.setTransparency(self.nameFg[3] < 1.0)

        width, height = t.node().getWidth(), t.node().getHeight()

        # Put the actual written name a little in front of the nametag and
        # disable depth write so the text appears nice and clear, free from
        # z-fighting and bizarre artifacts. The text renders *after* the tag
        # behind it, due to both being in the transparency bin,
        # so there's really no problem with doing this.
        t.setY(-0.05)
        t.setAttrib(DepthWriteAttrib.make(0))

        # Apply panel behind the text:
        panel = NametagGlobals.nametagCardModel.copyTo(self.innerNP, 0)
        panel.setPos((t.node().getLeft()+t.node().getRight())/2.0, 0,
                     (t.node().getTop()+t.node().getBottom())/2.0)
        panel.setScale(width + self.NAME_PADDING, 1, height + self.NAME_PADDING)
        panel.setColor(self.nameBg)
        panel.setTransparency(self.nameBg[3] < 1.0)

        self.frame = (t.node().getLeft()-self.NAME_PADDING/2.0,
                      t.node().getRight()+self.NAME_PADDING/2.0,
                      t.node().getBottom()-self.NAME_PADDING/2.0,
                      t.node().getTop()+self.NAME_PADDING/2.0)
