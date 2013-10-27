from NametagConstants import *
import NametagGlobals
from otp.margins.ClickablePopup import ClickablePopup
from pandac.PandaModules import *

class Nametag(ClickablePopup):
    CName = 1
    CSpeech = 2
    CThought = 4

    def __init__(self):
        ClickablePopup.__init__(self)
        self.contents = (self.CName|self.CSpeech|self.CThought)

        self.innerNP = NodePath.anyPath(self).attachNewNode('nametag_contents')

        self.wordWrap = 10

        self.font = None
        self.name = ''
        self.displayName = ''
        self.qtColor = VBase4(1,1,1,1)

        self.chatString = ''
        self.chatFlags = 0

    def setContents(self, contents):
        self.contents = contents

    def update(self):
        self.innerNP.node().removeAllChildren()
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
        if not self.font:
            # If no font is set, we can't actually display a name yet...
            return

        # Create text node:
        t = self.innerNP.attachNewNode(TextNode('name'))
        t.node().setFont(self.font)
        t.node().setAlign(TextNode.ACenter)
        t.node().setWordwrap(self.wordWrap)
        t.node().setText(self.displayName)
        t.node().setTextColor(VBase4(0,0,0,1))

        width, height = t.node().getWidth(), t.node().getHeight()

        t.setDepthOffset(1)

        # Apply panel behind the text:
        panel = NametagGlobals.nametagCardModel.copyTo(self.innerNP)
        panel.setPos((t.node().getLeft()+t.node().getRight())/2.0, 0,
                     (t.node().getTop()+t.node().getBottom())/2.0)
        panel.setScale(width, 1, height)
