from Nametag import *
import NametagGlobals
from NametagConstants import *
from pandac.PandaModules import *

class Nametag3d(Nametag):
    SCALING_FACTOR = 0.02
    SCALING_MINDIST = 1
    SCALING_MAXDIST = 50

    BILLBOARD_OFFSET = 3.0
    SHOULD_BILLBOARD = True

    def __init__(self):
        Nametag.__init__(self)

        self.contents = self.CName|self.CSpeech|self.CThought

        self.bbOffset = self.BILLBOARD_OFFSET
        self._doBillboard()

    def _doBillboard(self):
        if self.SHOULD_BILLBOARD:
            self.innerNP.setEffect(BillboardEffect.make(
                Vec3(0,0,1),
                True,
                False,
                self.bbOffset,
                NametagGlobals.camera,
                Point3(0,0,0)))

    def setBillboardOffset(self, bbOffset):
        self.bbOffset = bbOffset
        self._doBillboard()

    def tick(self):
        # Attempt to maintain the same on-screen size.
        distance = self.innerNP.getPos(base.cam).length()
        distance = max(min(distance, self.SCALING_MAXDIST), self.SCALING_MINDIST)

        self.innerNP.setScale(distance*self.SCALING_FACTOR)

    def getSpeechBalloon(self):
        return NametagGlobals.speechBalloon3d

    def getThoughtBalloon(self):
        return NametagGlobals.thoughtBalloon3d

    def setChatWordwrap(self, todo1):
        pass
