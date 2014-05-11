from Nametag import *
import NametagGlobals
from NametagConstants import *
from pandac.PandaModules import *
import math

class Nametag3d(Nametag):
    WANT_DYNAMIC_SCALING = True
    SCALING_FACTOR = 0.055
    SCALING_MINDIST = 1
    SCALING_MAXDIST = 50

    BILLBOARD_OFFSET = 3.0
    SHOULD_BILLBOARD = True

    IS_3D = True

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
                NodePath(), # Empty; look at scene camera
                Point3(0,0,0)))

    def setBillboardOffset(self, bbOffset):
        self.bbOffset = bbOffset
        self._doBillboard()

    def tick(self):
        if not self.WANT_DYNAMIC_SCALING:
            self.innerNP.setScale(self.SCALING_FACTOR)
            return

        # Attempt to maintain the same on-screen size.
        distance = self.innerNP.getPos(NametagGlobals.camera).length()
        distance = max(min(distance, self.SCALING_MAXDIST), self.SCALING_MINDIST)

        scale = math.sqrt(distance)*self.SCALING_FACTOR
        self.innerNP.setScale(scale)

        # As 3D nametags can move around on their own, we need to update the
        # click frame constantly:
        path = NodePath.anyPath(self)
        if path.isHidden() or path.getTop() != NametagGlobals.camera.getTop():
            self.stashClickRegion()
        else:
            left, right, bottom, top = self.frame
            self.updateClickRegion(left*scale, right*scale,
                                   bottom*scale, top*scale,
                                   self.bbOffset)

    def getSpeechBalloon(self):
        return NametagGlobals.speechBalloon3d

    def getThoughtBalloon(self):
        return NametagGlobals.thoughtBalloon3d
