# 2013.08.22 22:15:40 Pacific Daylight Time
# Embedded file name: otp.movement.Impulse
from pandac.PandaModules import *
from direct.showbase import DirectObject

class Impulse(DirectObject.DirectObject):
    __module__ = __name__

    def __init__(self):
        self.mover = None
        self.nodePath = None
        return

    def destroy(self):
        pass

    def _process(self, dt):
        pass

    def _setMover(self, mover):
        self.mover = mover
        self.nodePath = self.mover.getNodePath()
        self.VecType = self.mover.VecType

    def _clearMover(self, mover):
        if self.mover == mover:
            self.mover = None
            self.nodePath = None
        return

    def isCpp(self):
        return 0
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\otp\movement\Impulse.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:15:40 Pacific Daylight Time
