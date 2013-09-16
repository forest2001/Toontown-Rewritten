# 2013.08.22 22:13:46 Pacific Daylight Time
# Embedded file name: direct.controls.ControlManager
from direct.showbase.InputStateGlobal import inputState
from direct.directnotify import DirectNotifyGlobal
from direct.task import Task
CollisionHandlerRayStart = 4000.0

class ControlManager():
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('ControlManager')
    wantAvatarPhysicsIndicator = config.GetBool('want-avatar-physics-indicator', 0)
    wantAvatarPhysicsDebug = config.GetBool('want-avatar-physics-debug', 0)
    wantWASD = config.GetBool('want-WASD', 0)

    def __init__(self, enable = True, passMessagesThrough = False):
        self.passMessagesThrough = passMessagesThrough
        self.inputStateTokens = []
        self.WASDTurnTokens = []
        self.__WASDTurn = True
        self.controls = {}
        self.currentControls = None
        self.currentControlsName = None
        self.isEnabled = 0
        if enable:
            self.enable()
        self.forceAvJumpToken = None
        if self.passMessagesThrough:
            ist = self.inputStateTokens
            ist.append(inputState.watchWithModifiers('forward', 'arrow_up', inputSource=inputState.ArrowKeys))
            ist.append(inputState.watchWithModifiers('reverse', 'arrow_down', inputSource=inputState.ArrowKeys))
            ist.append(inputState.watchWithModifiers('turnLeft', 'arrow_left', inputSource=inputState.ArrowKeys))
            ist.append(inputState.watchWithModifiers('turnRight', 'arrow_right', inputSource=inputState.ArrowKeys))
        return

    def __str__(self):
        return "ControlManager: using '%s'" % self.currentControlsName

    def add(self, controls, name = 'basic'):
        oldControls = self.controls.get(name)
        if oldControls is not None:
            oldControls.disableAvatarControls()
            oldControls.setCollisionsActive(0)
            oldControls.delete()
        controls.disableAvatarControls()
        controls.setCollisionsActive(0)
        self.controls[name] = controls
        return

    def get(self, name):
        return self.controls.get(name)

    def remove(self, name):
        oldControls = self.controls.pop(name, None)
        if oldControls is not None:
            oldControls.disableAvatarControls()
            oldControls.setCollisionsActive(0)
        return

    def use(self, name, avatar):
        if __debug__ and hasattr(self, 'ignoreUse'):
            return
        controls = self.controls.get(name)
        if controls is not None:
            if controls is not self.currentControls:
                if self.currentControls is not None:
                    self.currentControls.disableAvatarControls()
                    self.currentControls.setCollisionsActive(0)
                    self.currentControls.setAvatar(None)
                self.currentControls = controls
                self.currentControlsName = name
                self.currentControls.setAvatar(avatar)
                self.currentControls.setCollisionsActive(1)
                if self.isEnabled:
                    self.currentControls.enableAvatarControls()
                messenger.send('use-%s-controls' % (name,), [avatar])
        return

    def setSpeeds(self, forwardSpeed, jumpForce, reverseSpeed, rotateSpeed, strafeLeft = 0, strafeRight = 0):
        for controls in self.controls.values():
            controls.setWalkSpeed(forwardSpeed, jumpForce, reverseSpeed, rotateSpeed)

    def delete(self):
        self.disable()
        for controls in self.controls.keys():
            self.remove(controls)

        del self.controls
        del self.currentControls
        for token in self.inputStateTokens:
            token.release()

        for token in self.WASDTurnTokens:
            token.release()

        self.WASDTurnTokens = []

    def getSpeeds(self):
        if self.currentControls:
            return self.currentControls.getSpeeds()
        return None

    def getIsAirborne(self):
        if self.currentControls:
            return self.currentControls.getIsAirborne()
        return False

    def setTag(self, key, value):
        for controls in self.controls.values():
            controls.setTag(key, value)

    def deleteCollisions(self):
        for controls in self.controls.values():
            controls.deleteCollisions()

    def collisionsOn(self):
        if self.currentControls:
            self.currentControls.setCollisionsActive(1)

    def collisionsOff(self):
        if self.currentControls:
            self.currentControls.setCollisionsActive(0)

    def placeOnFloor(self):
        if self.currentControls:
            self.currentControls.placeOnFloor()

    def enable(self):
        if self.isEnabled:
            return
        self.isEnabled = 1
        ist = self.inputStateTokens
        ist.append(inputState.watch('run', 'runningEvent', 'running-on', 'running-off'))
        ist.append(inputState.watchWithModifiers('forward', 'arrow_up', inputSource=inputState.ArrowKeys))
        ist.append(inputState.watch('forward', 'force-forward', 'force-forward-stop'))
        ist.append(inputState.watchWithModifiers('reverse', 'arrow_down', inputSource=inputState.ArrowKeys))
        ist.append(inputState.watchWithModifiers('reverse', 'mouse4', inputSource=inputState.Mouse))
        if self.wantWASD:
            ist.append(inputState.watchWithModifiers('turnLeft', 'arrow_left', inputSource=inputState.ArrowKeys))
            ist.append(inputState.watch('turnLeft', 'mouse-look_left', 'mouse-look_left-done'))
            ist.append(inputState.watch('turnLeft', 'force-turnLeft', 'force-turnLeft-stop'))
            ist.append(inputState.watchWithModifiers('turnRight', 'arrow_right', inputSource=inputState.ArrowKeys))
            ist.append(inputState.watch('turnRight', 'mouse-look_right', 'mouse-look_right-done'))
            ist.append(inputState.watch('turnRight', 'force-turnRight', 'force-turnRight-stop'))
            ist.append(inputState.watchWithModifiers('forward', 'w', inputSource=inputState.WASD))
            ist.append(inputState.watchWithModifiers('reverse', 's', inputSource=inputState.WASD))
            ist.append(inputState.watchWithModifiers('slideLeft', 'q', inputSource=inputState.QE))
            ist.append(inputState.watchWithModifiers('slideRight', 'e', inputSource=inputState.QE))
            self.setWASDTurn(self.__WASDTurn)
        else:
            ist.append(inputState.watchWithModifiers('turnLeft', 'arrow_left', inputSource=inputState.ArrowKeys))
            ist.append(inputState.watch('turnLeft', 'mouse-look_left', 'mouse-look_left-done'))
            ist.append(inputState.watch('turnLeft', 'force-turnLeft', 'force-turnLeft-stop'))
            ist.append(inputState.watchWithModifiers('turnRight', 'arrow_right', inputSource=inputState.ArrowKeys))
            ist.append(inputState.watch('turnRight', 'mouse-look_right', 'mouse-look_right-done'))
            ist.append(inputState.watch('turnRight', 'force-turnRight', 'force-turnRight-stop'))
        if self.wantWASD:
            ist.append(inputState.watchWithModifiers('jump', 'space'))
        else:
            ist.append(inputState.watch('jump', 'control', 'control-up'))
        if self.currentControls:
            self.currentControls.enableAvatarControls()

    def disable(self):
        self.isEnabled = 0
        for token in self.inputStateTokens:
            token.release()

        self.inputStateTokens = []
        for token in self.WASDTurnTokens:
            token.release()

        self.WASDTurnTokens = []
        if self.currentControls:
            self.currentControls.disableAvatarControls()
        if self.passMessagesThrough:
            ist = self.inputStateTokens
            ist.append(inputState.watchWithModifiers('forward', 'arrow_up', inputSource=inputState.ArrowKeys))
            ist.append(inputState.watchWithModifiers('reverse', 'arrow_down', inputSource=inputState.ArrowKeys))
            ist.append(inputState.watchWithModifiers('turnLeft', 'arrow_left', inputSource=inputState.ArrowKeys))
            ist.append(inputState.watchWithModifiers('turnRight', 'arrow_right', inputSource=inputState.ArrowKeys))

    def stop(self):
        self.disable()
        if self.currentControls:
            self.currentControls.setCollisionsActive(0)
            self.currentControls.setAvatar(None)
        self.currentControls = None
        return

    def disableAvatarJump(self):
        self.forceAvJumpToken = inputState.force('jump', 0, 'ControlManager.disableAvatarJump')

    def enableAvatarJump(self):
        self.forceAvJumpToken.release()
        self.forceAvJumpToken = None
        return

    def monitor(self, foo):
        return Task.cont

    def setWASDTurn(self, turn):
        self.__WASDTurn = turn
        if not self.isEnabled:
            return
        turnLeftWASDSet = inputState.isSet('turnLeft', inputSource=inputState.WASD)
        turnRightWASDSet = inputState.isSet('turnRight', inputSource=inputState.WASD)
        slideLeftWASDSet = inputState.isSet('slideLeft', inputSource=inputState.WASD)
        slideRightWASDSet = inputState.isSet('slideRight', inputSource=inputState.WASD)
        for token in self.WASDTurnTokens:
            token.release()

        if turn:
            self.WASDTurnTokens = (inputState.watchWithModifiers('turnLeft', 'a', inputSource=inputState.WASD), inputState.watchWithModifiers('turnRight', 'd', inputSource=inputState.WASD))
            inputState.set('turnLeft', slideLeftWASDSet, inputSource=inputState.WASD)
            inputState.set('turnRight', slideRightWASDSet, inputSource=inputState.WASD)
            inputState.set('slideLeft', False, inputSource=inputState.WASD)
            inputState.set('slideRight', False, inputSource=inputState.WASD)
        else:
            self.WASDTurnTokens = (inputState.watchWithModifiers('slideLeft', 'a', inputSource=inputState.WASD), inputState.watchWithModifiers('slideRight', 'd', inputSource=inputState.WASD))
            inputState.set('slideLeft', turnLeftWASDSet, inputSource=inputState.WASD)
            inputState.set('slideRight', turnRightWASDSet, inputSource=inputState.WASD)
            inputState.set('turnLeft', False, inputSource=inputState.WASD)
            inputState.set('turnRight', False, inputSource=inputState.WASD)
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\controls\ControlManager.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:13:46 Pacific Daylight Time
