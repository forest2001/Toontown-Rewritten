# 2013.08.22 22:13:49 Pacific Daylight Time
# Embedded file name: direct.controls.TwoDWalker
from GravityWalker import *

class TwoDWalker(GravityWalker):
    __module__ = __name__
    notify = directNotify.newCategory('TwoDWalker')
    wantDebugIndicator = base.config.GetBool('want-avatar-physics-indicator', 0)
    wantFloorSphere = base.config.GetBool('want-floor-sphere', 0)
    earlyEventSphere = base.config.GetBool('early-event-sphere', 0)

    def __init__(self, gravity = -32.174, standableGround = 0.707, hardLandingForce = 16.0):
        self.notify.debug('Constructing TwoDWalker')
        GravityWalker.__init__(self)

    def handleAvatarControls(self, task):
        jump = inputState.isSet('forward')
        if self.lifter.isOnGround():
            if self.isAirborne:
                self.isAirborne = 0
                impact = self.lifter.getImpactVelocity()
                messenger.send('jumpLand')
            self.priorParent = Vec3.zero()
        else:
            if self.isAirborne == 0:
                pass
            self.isAirborne = 1
        return Task.cont

    def jumpPressed(self):
        if self.lifter.isOnGround():
            if self.isAirborne == 0:
                if self.mayJump:
                    self.lifter.addVelocity(self.avatarControlJumpForce)
                    messenger.send('jumpStart')
                    self.isAirborne = 1
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\controls\TwoDWalker.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:13:49 Pacific Daylight Time
