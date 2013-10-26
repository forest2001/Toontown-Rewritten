from Nametag import *
import NametagGlobals
from pandac.PandaModules import *

class Nametag3d(Nametag, PandaNode):
    def __init__(self):
        Nametag.__init__(self)

    def showSpeech(self):
        bubble = NametagGlobals.speechBalloon3d.generate(self.chatString, self.font)
        bubble.reparentTo(NodePath(self))
