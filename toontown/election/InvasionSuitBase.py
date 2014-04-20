from pandac.PandaModules import *
from toontown.toonbase import ToontownGlobals

class InvasionSuitBase:
    # Primarily, this class implements the variety of 2D lerp that we use to
    # move the invading suits around.

    def __init__(self):
        self.walkSpeed = ToontownGlobals.SuitWalkSpeed

        # This is a fine way to reset all values to defaults:
        self.freezeLerp(0, 0)

    def setLerpPoints(self, x1, y1, x2, y2):
        # This sets the points in the lerp and precalculates everything.
        self._originPoint = Point2(x1, y1)
        endPoint = Point2(x2, y2)
        self._lerpVector = endPoint - self._originPoint

        # We can get our ideal heading as long as the lerpVector has a length:
        self._idealH = -self._lerpVector.signedAngleDeg(Vec2(0,1))

        # Calculate how long it takes the suit to march along this lerp:
        vectorLength = self._lerpVector.length()
        self._lerpDelay = vectorLength / self.walkSpeed

        # Avoid divisions by zero:
        self._lerpDelay = max(self._lerpDelay, 0.01)

    def freezeLerp(self, x, y):
        # This creates a "lerp" that is actually frozen. No movement occurs.
        self.setLerpPoints(x, y, x, y)

    def getPosAt(self, t):
        # Where are we at time (in seconds) t? (Where t=0 is when the lerp began.)
        vecScale = min(max(t / self._lerpDelay, 0.0), 1.0)

        return self._originPoint + (self._lerpVector * vecScale)

    def freezeLerpAt(self, t):
        x, y = self.getPosAt(t)
        self.freezeLerp(x, y)
