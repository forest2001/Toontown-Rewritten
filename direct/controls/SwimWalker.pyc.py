# 2013.08.22 22:13:49 Pacific Daylight Time
# Embedded file name: direct.controls.SwimWalker
from direct.showbase.InputStateGlobal import inputState
from direct.directnotify import DirectNotifyGlobal
from direct.controls import NonPhysicsWalker

class SwimWalker(NonPhysicsWalker.NonPhysicsWalker):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('SwimWalker')

    def _calcSpeeds(self):
        forward = inputState.isSet('forward')
        reverse = inputState.isSet('reverse')
        if not inputState.isSet('turnLeft'):
            turnLeft = inputState.isSet('slideLeft')
            turnRight = inputState.isSet('turnRight') or inputState.isSet('slideRight')
            forward = base.localAvatar.getAutoRun() and 1
            reverse = 0
        self.speed = forward and self.avatarControlForwardSpeed or reverse and -self.avatarControlReverseSpeed
        self.slideSpeed = 0.0
        self.rotationSpeed = turnLeft and self.avatarControlRotateSpeed or turnRight and -self.avatarControlRotateSpeed
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\controls\SwimWalker.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:13:49 Pacific Daylight Time
