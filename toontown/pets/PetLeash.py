# 2013.08.22 22:23:54 Pacific Daylight Time
# Embedded file name: toontown.pets.PetLeash
from pandac.PandaModules import *
from otp.movement import Impulse

class PetLeash(Impulse.Impulse):
    __module__ = __name__

    def __init__(self, origin, length):
        Impulse.Impulse.__init__(self)
        self.origin = origin
        self.length = length

    def _process(self, dt):
        Impulse.Impulse._process(self, dt)
        myPos = self.nodePath.getPos()
        myDist = self.VecType(myPos - self.origin.getPos()).length()
        if myDist > self.length:
            excess = myDist - self.length
            shove = self.VecType(myPos)
            shove.normalize()
            shove *= -excess
            self.mover.addShove(shove)
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\pets\PetLeash.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:23:54 Pacific Daylight Time
