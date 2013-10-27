from Nametag import *
import NametagGlobals
from pandac.PandaModules import *

class Nametag3d(Nametag):
    CONTENTS_SCALE = 0.33

    def __init__(self):
        Nametag.__init__(self)
        self.innerNP.setBillboardAxis()
        self.innerNP.setScale(self.CONTENTS_SCALE)

    def showSpeech(self):
        bubble = NametagGlobals.speechBalloon3d.generate(self.chatString, self.font)
        bubble.reparentTo(self.innerNP)

    def showThought(self):
        bubble = NametagGlobals.thoughtBalloon3d.generate(self.chatString, self.font)
        bubble.reparentTo(self.innerNP)
