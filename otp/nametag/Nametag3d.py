from Nametag import *
import NametagGlobals
from NametagConstants import *
from pandac.PandaModules import *

class Nametag3d(Nametag):
    CONTENTS_SCALE = 0.33

    def __init__(self):
        Nametag.__init__(self)

        self.contents = self.CName|self.CSpeech|self.CThought

        self.innerNP.setBillboardPointWorld()
        self.innerNP.setScale(self.CONTENTS_SCALE)

    def showSpeech(self):
        color = self.qtColor if (self.chatFlags&CFQuicktalker) else VBase4(1,1,1,1)
        bubble = NametagGlobals.speechBalloon3d.generate(self.chatString, self.font,
                                                         balloonColor=color)
        bubble.reparentTo(self.innerNP)

    def showThought(self):
        color = self.qtColor if (self.chatFlags&CFQuicktalker) else VBase4(1,1,1,1)
        bubble = NametagGlobals.thoughtBalloon3d.generate(self.chatString, self.font,
                                                          balloonColor=color)
        bubble.reparentTo(self.innerNP)
