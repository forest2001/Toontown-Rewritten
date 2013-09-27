from pandac.PandaModules import *
from libotp import Nametag, WhisperPopup
from direct.gui.DirectGui import *
from direct.showbase.PythonUtil import *
from direct.interval.IntervalGlobal import *
from direct.showbase.InputStateGlobal import inputState
from pandac.PandaModules import *
import Avatar
from direct.controls import ControlManager
import DistributedAvatar
from direct.task import Task
import PositionExaminer
from otp.otpbase import OTPGlobals
from otp.otpbase import OTPRender
import math, string, random
from direct.directnotify import DirectNotifyGlobal
from direct.distributed import DistributedSmoothNode
from direct.gui import DirectGuiGlobals
from otp.otpbase import OTPLocalizer
from direct.controls.GhostWalker import GhostWalker
from direct.controls.GravityWalker import GravityWalker
from direct.controls.ObserverWalker import ObserverWalker
from direct.controls.PhysicsWalker import PhysicsWalker
from direct.controls.SwimWalker import SwimWalker
from direct.controls.TwoDWalker import TwoDWalker

class LocalAvatar(DistributedAvatar.DistributedAvatar, DistributedSmoothNode.DistributedSmoothNode):
    notify = DirectNotifyGlobal.directNotify.newCategory('LocalAvatar')
    wantDevCameraPositions = base.config.GetBool('want-dev-camera-positions', 0)
    wantMouse = base.config.GetBool('want-mouse', 0)
    sleepTimeout = base.config.GetInt('sleep-timeout', 120)
    swimTimeout = base.config.GetInt('afk-timeout', 600)
    _LocalAvatar__enableMarkerPlacement = base.config.GetBool('place-markers', 0)
    acceptingNewFriends = base.config.GetBool('accepting-new-friends', 1)
    acceptingNonFriendWhispers = base.config.GetBool('accepting-non-friend-whispers', 0)
    def __init__(self, x = None, y = False):
        pass
    
    def useSwimControls(self):
        pass
    
    def useGhostControls(self):
        pass
    
    def useWalkControls(self):
        pass
    
    def useTwoDControls(self):
        pass
    
    def isLockedDown(self):
        pass
    
    def lock(self):
        pass
    
    def unlock(self):
        pass
    
    def isInWater(self):
        pass
    
    def isTeleportAllowed(self):
        pass
    
    def setTeleportAllowed(self):
        pass
    
    def sendFriendsListEvent(self):
        pass
    
    def delete(self):
        pass
    
    def shadowReach(self):
        pass
    
    def wantLegacyLifter(self):
        pass
    
    def setupControls(self, a=1.3999999999999999, b=OTPGlobals.FloorOffset, c=4.0, d=OTPGlobals.WallBitmask, e=OTPGlobals.FloorBitmask, f=OTPGlobals.GhostBitmask):
        pass
    
    def initializeCollisions(self):
        pass
    
    def deleteCollisions(self):
        pass
    
    def initializeSmartCameraCollisions(self):
        pass
    
    def deleteSmartCameraCollisions(self):
        pass
    
    def collisionsOff(self):
        pass
    
    def collisionsOn(self):
        pass
    
    def recalcCameraSphere(self):
        pass
    
    def putCameraFloorRayOnAvatar(self):
        pass

    def putCameraFloorRayOnCamera(self):
        pass
    
    def attachCamera(self):
        pass
    
    def detachCamera(self):
        pass
    
    def stopJumpLandTask(self):
        pass
    
    def jumpStart(self):
        pass
    
    def returnToWalk(self):
        pass
    
    def jumpLandAnimFix(self):
        pass
    
    def jumpHardLand(self):
        pass
    
    def jumpLand(self):
        pass
    
    if 1:
        pass
    
    def setupAnimationEvents(self):
        pass
    
    def ignoreAnimationEvents(self):
        pass
    
    def allowHardLand(self):
        pass
    
    def enableSmartCameraViews(self):
        pass
    
    def disableSmartCameraViews(self):
        pass
    
    def enableAvatarControls(self):
        pass
    
    def disableAvatarControls(self):
        pass
    
    def setWalkSpeedNormal(self):
        pass
    
    def setWalkSpeedSlow(self):
        pass
    
    def pageUp(self):
        pass
    
    def pageDown(self):
        pass
    
    def clearPageUpDown(self):
        pass
    
    def nextCameraPos(self):
        pass
    
    def initCameraPositions(self):
        pass
    
    def addCameraPosition(self, x=None):
        pass
    
    def resetCameraPosition(self):
        pass

    def removeCameraPosition(self):
        pass

    def printCameraPositions(self):
        pass
    
    def printCameraPosition(self):
        pass
    
    def posCamera(self):
        pass
    
    def getClampedAvatarHeight(self):
        pass
    
    def getVisibilityPoint(self):
        pass
    
    def setLookAtPoint(self):
        pass

    def getLookAtPoint(self):
        pass

    def setIdealCameraPos(self):
        pass

    def getIdealCameraPos(self):
        pass

    def setCameraPositionByIndex(self):
        pass

    def setCameraPosForPetInteraction(self):
        pass

    def unsetCameraPosForPetInteraction(self):
        pass

    def setCameraSettings(self):
        pass

    def getCompromiseCameraPos(self):
        if self._LocalAvatar__idealCameraObstructed == 0:
            self.compromisePos = self.getIdealCameraPos
        else:
            visPnt = self.getVisibilityPoint()
            idealPos = self.getIdealCameraPos()
            
             28 JUMP_FORWARD           144 (to 175)
        >>   31 POP_TOP             

1085          56 LOAD_GLOBAL              7 (Vec3)
             59 LOAD_FAST                4 (idealPos)
             62 LOAD_FAST                3 (visPnt)
             65 BINARY_SUBTRACT     
             66 CALL_FUNCTION            1
             69 LOAD_ATTR                8 (length)
             72 CALL_FUNCTION            0
             75 STORE_FAST               1 (distance)

1086          78 LOAD_FAST                0 (self)
             81 LOAD_ATTR               10 (closestObstructionDistance)
             84 LOAD_FAST                1 (distance)
             87 BINARY_DIVIDE       
             88 STORE_FAST               2 (ratio)

1087          91 LOAD_FAST                4 (idealPos)
             94 LOAD_FAST                2 (ratio)
             97 BINARY_MULTIPLY     
             98 LOAD_FAST                3 (visPnt)
            101 LOAD_CONST               2 (1)
            104 LOAD_FAST                2 (ratio)
            107 BINARY_SUBTRACT     
            108 BINARY_MULTIPLY     
            109 BINARY_ADD          
            110 STORE_FAST               5 (compromisePos)

1089         113 LOAD_CONST               3 (1.0)
            116 LOAD_FAST                2 (ratio)
            119 LOAD_FAST                2 (ratio)
            122 BINARY_MULTIPLY     
            123 BINARY_SUBTRACT     
            124 STORE_FAST               6 (liftMult)

1090         127 LOAD_GLOBAL             13 (Point3)
            130 LOAD_FAST                5 (compromisePos)
            133 LOAD_CONST               1 (0)
            136 BINARY_SUBSCR       
            137 LOAD_FAST                5 (compromisePos)
            140 LOAD_CONST               2 (1)
            143 BINARY_SUBSCR       

1091         144 LOAD_FAST                5 (compromisePos)
            147 LOAD_CONST               4 (2)
            150 BINARY_SUBSCR       
            151 LOAD_FAST                0 (self)
            154 LOAD_ATTR               14 (getHeight)
            157 CALL_FUNCTION            0
            160 LOAD_CONST               5 (0.40000000000000002)
            163 BINARY_MULTIPLY     
            164 LOAD_FAST                6 (liftMult)
            167 BINARY_MULTIPLY     
            168 BINARY_ADD          
            169 CALL_FUNCTION            3
            172 STORE_FAST               5 (compromisePos)

1093     >>  175 LOAD_FAST                5 (compromisePos)
            178 LOAD_ATTR               15 (setZ)
            181 LOAD_FAST                5 (compromisePos)
            184 LOAD_CONST               4 (2)
            187 BINARY_SUBSCR       
            188 LOAD_FAST                0 (self)
            191 LOAD_ATTR               16 (cameraZOffset)
            194 BINARY_ADD          
            195 CALL_FUNCTION            1
            198 POP_TOP             

1094         199 LOAD_FAST                5 (compromisePos)
            202 RETURN_VALUE        

    def updateSmartCameraCollisionLineSegment(self):
        pointB = self.getIdealCameraPos()
        pointA = self.getVisibilityPoint()
        vectorAB = Vec3(pointB-pointA)
        lengthAB = vectorAB.length()
        if lengthAB > 0.001:
            self.ccLine.setPointA(pointA)
            self.ccLine.setPointB(pointB)

    def initializeSmartCamera(self):
        self._LocalAvatar__idealCameraObstructed = 0
        self.closestObstructionDistance = 0.0
        self.cameraIndex = 0
        self.auxCameraPositions = []
        self.cameraZOffset = 0.0
        self._LocalAvatar__onLevelGround = 0
        self._LocalAvatar__camCollCanMove = 0
        self._LocalAvatar__geom = render
        self._LocalAvatar__disableSmartCam = 0
        self.initializeSmartCameraCollisions()
        self._smartCamEnabled = False

    def shutdownSmartCamera(self):
        self.deleteSmartCameraCollisions()

    def setOnLevelGround(self, flag):
        self._LocalAvatar__onLevelGround = flag

    def setCameraCollisionsCanMove(self, flag):
        self._LocalAvatar__camCollCanMove = flag

    def setGeom(self, geom):
        self._LocalAvatar__geom = geom

    def startUpdateSmartCamera(self, push=1):
        if self._smartCamEnabled:
            LocalAvatar.notify.warning('redundant call to startUpdateSmartCamera')
            return
        self._smartCamEnabled = True
        self._LocalAvatar__floorDetected = 0
        self._LocalAvatar__cameraHasBeenMoved = 0
        self.recalcCameraSphere()
        self.initCameraPositions()
        self.setCameraPositionByIndex(self.cameraIndex)
        self.posCamera(0, 0.0)
        self._LocalAvatar__instantaneousCamPos = camera.getPos()
        if push:
            self.cTrav.addCollider(self.ccSphereNodePath, self.camPusher)
            self.ccTravOnFloor.addCollider(self.ccRay2NodePath, self.camFloorCollisionBroadcaster)
            self._LocalAvatar__disableSmartCam = 0
        else:
            self._LocalAvatar__disableSmartCam = 1
        self._LocalAvatar__lastPosWrtRender = camera.getPos(render)
        self._LocalAvatar__lastHprWrtRender = camera.getHpr(render)
        taskName = self.taskName('updateSmartCamera')
        taskMgr.remove(taskName)
        taskMgr.add(self.updateSmartCamera, taskName, priority=47)
        self.enableSmartCameraViews()

    def stopUpdateSmartCamera(self):
        if not self._smartCamEnabled:
            LocalAvatar.notify.warning('redundant call to stopUpdateSmartCamera')
            return
        self.disableSmartCameraViews()
        self.cTrav.removeCollider(self.ccSphereNodePath)
        self.ccTravOnFloor.removeCollider(self.ccRay2NodePath)
        if not base.localAvatar.isEmpty():
            self.putCameraFloorRayOnAvatar()
        taskName = self.taskName('updateSmartCamera')
        taskMgr.remove(taskName)
        self._smartCamEnabled = False

    def updateSmartCamera(self, task):
        if not self._LocalAvatar__camCollCanMove and not self._LocalAvatar__cameraHasBeenMoved:
           if self._LocalAvatar__lastPosWrtRender == camera.getPos(render):
                if self._LocalAvatar__lastHprWrtRender == camera.getHpr(render):
                    return Task.cont
        self._LocalAvatar__cameraHasBeenMoved = 0
        self._LocalAvatar__lastPosWrtRender = camera.getPos(render)
        self._LocalAvatar__lastHprWrtRender = camera.getHpr(render)
        self._LocalAvatar__idealCameraObstructed = 0
        if not self._LocalAvatar__disableSmartCam:
            self.ccTrav.traverse(self._LocalAvatar__geom)
            if self.camCollisionQueue.getNumEntries() > 0:
                self.camCollisionQueue.sortEntries()
                self.handleCameraObstruction(self.camCollisionQueue.getEntry(0))
            if not self._LocalAvatar__onLevelGround:
                self.handleCameraFloorInteraction()
        if not self._LocalAvatar__idealCameraObstructed:
            self.nudgeCamera()
        if not self._LocalAvatar__disableSmartCam:
            self.ccPusherTrav.traverse(self._LocalAvatar__geom)
            self.putCameraFloorRayOnCamera()
        self.ccTravOnFloor.traverse(self._LocalAvatar__geom)
        return Task.cont

    def positionCameraWithPusher(self, pos, lookAt):
        camera.setPos(pos)
        self.ccPusherTrav.traverse(self._LocalAvatar__geom)
        camera.lookAt(lookAt)

    def nudgeCamera(self):
        CLOSE_ENOUGH = 0.10000000000000001
        curCamPos = self._LocalAvatar__instantaneousCamPos
        curCamHpr = camera.getHpr()
        targetCamPos = self.getCompromiseCameraPos()
        targetCamLookAt = self.getLookAtPoint()
        posDone = 0
        if Vec3(curCamPos-targetCamPos).length() <= CLOSE_ENOUGH:
            camera.setPos(targetCamPos)
            posDone = 1
        camera.setPos(targetCamPos)
        camera.lookAt(targetCamLookAt)
        targetCamHpr = camera.getHpr()
        hprDone = 0
        if Vec3(curCamHpr-targetCamHpr).length() <= CLOSE_ENOUGH:
            hprDone = 1
        if posDone and hprDone:
            return
        lerpRatio = 0.14999999999999999
        lerpRatio = 1-pow(1-lerpRatio,globalClock.getDt()*30.0)
        self._LocalAvatar__instantaneousCamPos = targetCamPos*lerpRatio+curCamPos*(1-lerpRatio)
        if self._LocalAvatar__disableSmartCam or not self._LocalAvatar__idealCameraObstructed:
            newHpr = targetCamHpr*lerpRatio+curCamHpr*(1-lerpRatio)
        else:
            newHpr = targetCamHpr
        camera.setPos(self._LocalAvatar__instantaneousCamPos)
        camera.setHpr(newHpr)

    def popCameraToDest(self):
        newCamPos = self.getCompromiseCameraPos()
        newCamLookAt = self.getLookAtPoint()
        self.positionCameraWithPusher(newCamPos, newCamLookAt)
        self._LocalAvatar__instantaneousCamPos = camera.getPos()

    def handleCameraObstruction(self, camObstrCollisionEntry):
        collisionPoint = camObstrCollisionEntry.getSurfacePoint(self.ccLineNodePath)
        collisionVec =  Vec3(collisionPoint-self.ccLine.getPointA())
        distance = collisionVec.length()
        self._LocalAvatar__idealCameraObstructed = 1
        self.closestObstructionDistance = distance
        self.popCameraToDest()

    def handleCameraFloorInteraction(self):
        self.putCameraFloorRayOnCamera()
        self.ccTravFloor.traverse(self._LocalAvatar__geom)
        if self._LocalAvatar__onLevelGround:
            return
        if self.camFloorCollisionQueue.getNumEntries() == 0:
            return
        self.camFloorCollisionQueue.sortEntries()
        camObstrCollisionEntry = self.camFloorCollisionQueue.getEntry(0)
        camHeightFromFloor = camObstrCollisionEntry.getSurfacePoint(self.ccRayNodePath)[2]
        self.cameraZOffset = camera.getPos()[2] + camHeightFromFloor
        if self.cameraZOffset < 0:
            self.cameraZOffset = 0
        if self._LocalAvatar__floorDetected == 0:
            self._LocalAvatar__floorDetected = 1
            self.popCameraToDest()

    def lerpCameraFov(self, fov, time):
        taskMgr.remove('cam-fov-lerp-play')
        oldFov = base.camLens.getHfov()
        if abs(fov-oldFov) > 0.10000000000000001:
            def setCamFov(fov):
                base.camLens.setFov(fov)
            self.camLerpInterval = LerpFunctionInterval(setCamFov,
                fromData = oldFov, toData = fov, duration=time,
                name='cam-fov-lerp'
            )
            self.camLerpInterval.start()

    def setCameraFov(self, fov):
        self.fov = fov
        if not (self.isPageDown or self.isPageUp):
            base.camLens.setFov(self.fov)

    def gotoNode(self, node, eyeHeight=3):
        possiblePoints = (Point3(3, 6, 0),
            Point3(-3, 6, 0),
            Point3(6, 6, 0),
            Point3(-6, 6, 0),
            Point3(3, 9, 0),
            Point3(-3, 9, 0),
            Point3(6, 9, 0),
            Point3(-6, 9, 0),
            Point3(9, 9, 0),
            Point3(-9, 9, 0),
            Point3(6, 0, 0),
            Point3(-6, 0, 0),
            Point3(6, 3, 0),
            Point3(-6, 3, 0),
            Point3(9, 9, 0),
            Point3(-9, 9, 0),
            Point3(0, 12, 0),
            Point3(3, 12, 0),
            Point3(-3, 12, 0),
            Point3(6, 12, 0),
            Point3(-6, 12, 0),
            Point3(9, 12, 0),
            Point3(-9, 12, 0),
            Point3(0, -6, 0),
            Point3(-3, -6, 0),
            Point3(0, -9, 0),
            Point3(-6, -9, 0)
        )
        for point in possiblePoints:
            pos = self.positionExaminer.consider(node, point, eyeHeight)
            if pos:
                self.setPos(node, pos)
                self.lookAt(node)
                self.setHpr(self.getH() + random.choice((-10, 10)), 0, 0)
                return
        self.setPos(node, 0, 0, 0)

    def setCustomMessages(self, customMessages):
        self.customMessages = customMessages
        messenger.send('customMessagesChanged')

    def displayWhisper(self, fromId, chatString, whisperType):
        sender = None
        sfx = self.soundWhisper
        if whisperType == WhisperPopup.WTNormal or whisperType == WhisperPopup.WTQuickTalker:
            if sender == None:
                return
            chatString = sender.getName() + ': ' + chatString
        whisper = WhisperPopup(chatString, OTPGlobals.getInterfaceFont(), whisperType)
        if sender != None:
            whisper.setClickable(sender.getName(), fromId)
        whisper.manage(base.marginManager)
        base.playSfx(sfx)

    def displayWhisperPlayer(self, fromId, chatString, whisperType):
        sender = None
        playerInfo = None
        sfx = self.soundWhisper
        playerInfo = base.cr.playerFriendsManager.playerId2Info.get(fromId, None)
        if playerInfo == None:
            return
        senderName = playerInfo.playerName
        if whisperType == WhisperPopup.WTNormal or whisperType == WhisperPopup.WTQuickTalker:
            chatString = senderName + ': ' + chatString
        whisper = WhisperPopup(chatString, OTPGlobals.getInterfaceFont(), whisperType)
        if sender != None:
            whisper.setClickable(senderName, fromId)
        whisper.manage(base.marginManager)
        base.playSfx(sfx)   

    def setAnimMultiplier(self, value):
        self.animMultiplier = value

    def getAnimMultiplier(self):
        return self.animMultiplier

    def enableRun(self):
        self.accept('arrow_up', self.startRunWatch)
        self.accept('arrow_up-up', self.stopRunWatch)
        self.accept('control-arrow_up', self.startRunWatch)
        self.accept('control-arrow_up-up', self.stopRunWatch)
        self.accept('alt-arrow_up', self.startRunWatch)
        self.accept('alt-arrow_up-up', self.stopRunWatch)
        self.accept('shift-arrow_up', self.startRunWatch)
        self.accept('shift-arrow_up-up', self.stopRunWatch)

    def disableRun(self):
        self.ignore('arrow_up')
        self.ignore('arrow_up-up')
        self.ignore('control-arrow_up')
        self.ignore('control-arrow_up-up')
        self.ignore('alt-arrow_up')
        self.ignore('alt-arrow_up-up')
        self.ignore('shift-arrow_up')
        self.ignore('shift-arrow_up-up')

    def startRunWatch(self):
        def setRun(ignored):
            messenger.send('running-on')
        taskMgr.doMethodLater(self.runTimeout, setRun,
            self.uniqueName('runWatch'))
        return Task.cont

    def stopRunWatch(self):
        taskMgr.remove(self.uniqueName('runWatch'))
        messenger.send('running-off')
        return Task.cont

    def runSound(self):
        self.soundWalk.stop()
        base.playSfx(self.soundRun, looping=1)

    def walkSound(self):
        self.soundRun.stop()
        base.playSfx(self.soundWalk, looping=1)

    def stopSound(self):
        self.soundRun.stop()
        self.soundWalk.stop()

    def wakeUp(self):
        if self.sleepCallback != None:
            taskMgr.remove(self.uniqueName('sleepwatch'))
            self.startSleepWatch(self.sleepCallback)
        self.lastMoved = globalClock.getFrameTime()
        if self.sleepFlag:
            self.sleepFlag = 0

    def gotoSleep(self):
        if not self.sleepFlag:
            self.b_setAnimState('Sleep', self.animMultiplier)
            self.sleepFlag = 1

    def forceGotoSleep(self):
        if self.hp > 0:
            self.sleepFlag = 0
            self.gotoSleep()

    def startSleepWatch(self, callback):
        self.sleepCallback = callback
        taskMgr.doMethodLater(self.sleepTimeout, callback, self.uniqueName('sleepwatch'))

    def stopSleepWatch(self):
        taskMgr.remove(self.uniqueName('sleepwatch'))
        self.sleepCallback = None

    def startSleepSwimTest(self):
        taskName = self.taskName('sleepSwimTest')
        taskMgr.remove(taskName)
        task = Task.Task(self.sleepSwimTest)
        self.lastMoved = globalClock.getFrameTime()
        self.lastState = None
        self.lastAction = None
        self.sleepSwimTest(task)
        taskMgr.add(self.sleepSwimTest, taskName, 35)

    def stopSleepSwimTest(self):
        taskName = self.taskName('sleepSwimTest')
        taskMgr.remove(taskName)
        self.stopSound()

    def sleepSwimTest(self, task):
        pass
        now = globalClock.getFrameTime()
        speed, rotSpeed, slideSpeed =  self.controlManager.getSpeeds()
        if speed != 0.0 or rotSpeed != 0.0 or inputState.isSet('jump'):
            if not self.swimmingFlag:
                self.swimmingFlag = 1
        else:
            if self.swimmingFlag:
                self.swimmingFlag = 0
        if self.swimmingFlag or self.hp <= 0:
            self.wakeUp()
        else:
            if not self.sleepFlag:
                now = globalClock.getFrameTime()
                if now-self.lastMoved > self.swimTimeout:
                    self.swimTimeoutAction()
                    return Task.done
        return Task.cont

    def swimTimeoutAction(self):
        pass

    def trackAnimToSpeed(self, task):
        speed, rotSpeed, slideSpeed = self.controlManager.getSpeeds()
        if speed != 0.0 or rotSpeed != 0.0 or inputState.isSet('jump'):
            if not self.movingFlag:
                self.movingFlag = 1
                self.stopLookAround()
        else:
            if self.movingFlag:
                self.movingFlag = 0
                self.startLookAround()
        if self.movingFlag or self.hp <= 0:
            self.wakeUp()
        elif not self.sleepFlag:
            now = globalClock.getFrameTime()
            if now - self.lastMoved > self.sleepTimeout:
                self.gotoSleep()
        state = None
        if self.sleepFlag:
            state = 'Sleep'
        elif self.hp > 0:
            state = 'Happy'
        else:
            state = 'Sad'
        if state != self.lastState:
            self.lastState = state
            self.b_setAnimState(state, self.animMultiplier)
            if state == 'Sad':
                self.setWalkSpeedSlow()
            else:
                self.setWalkSpeedNormal()
        if self.cheesyEffect == OTPGlobals.CEFlatProfile or self.cheesyEffect == OTPGlobals.CEFlatPortrait:
            needH = None
            if rotSpeed > 0.0:
                needH = -10
            elif rotSpeed < 0.0:
                needH = 10
            elif speed != 0.0:
                needH = 0
            if needH != None and self.lastNeedH != needH:
                node = self.getGeomNode().getChild(0)
                lerp = Sequence(LerpHprInterval(node, 0.5, Vec3(needH, 0, 0), 
                  blendType='easeInOut'), 
                  name='cheesy-lerp-hpr', 
                  autoPause=1)
                lerp.start()
                self.lastNeedH = needH
        else:
            self.lastNeedH = None
        action = self.setSpeed(speed, rotSpeed)
        if action != self.lastAction:
            self.lastAction = action
            if self.emoteTrack:
                self.emoteTrack.finish()
                self.emoteTrack = None
            if action == OTPGlobals.WALK_INDEX or action == OTPGlobals.REVERSE_INDEX:
                self.walkSound()
            elif action == OTPGlobals.RUN_INDEX:
                self.runSound()
            else:
                self.stopSound()
        return Task.cont        

    def hasTrackAnimToSpeed(self):
        taskName = self.taskName('trackAnimToSpeed')
        return taskMgr.hasTaskNamed(taskName)

    def startTrackAnimToSpeed(self):
        taskName = self.taskName('trackAnimToSpeed')
        taskMgr.remove(taskName)
        task = Task.Task(self.trackAnimToSpeed)
        self.lastMoved = globalClock.getFrameTime()
        self.lastState = None
        self.lastAction = None
        self.trackAnimToSpeed(task)
        taskMgr.add(self.trackAnimToSpeed, taskName, 35)

    def stopTrackAnimToSpeed(self):
        taskName = self.taskName('trackAnimToSpeed')
        taskMgr.remove(taskName)
        self.stopSound()

    def startChat(self):
        self.chatMgr.start()
        self.accept(OTPGlobals.WhisperIncomingEvent, self.handlePlayerFriendWhisper)
        self.accept(OTPGlobals.ThinkPosHotkey, self.thinkPos)
        self.accept(OTPGlobals.PrintCamPosHotkey, self.printCamPos)
        if self._LocalAvatar__enableMarkerPlacement:
            self.accept(OTPGlobals.PlaceMarkerHotkey, self._LocalAvatar__placeMarker)

    def stopChat(self):
        self.chatMgr.stop()
        self.ignore(OTPGlobals.WhisperIncomingEvent)
        self.ignore(OTPGlobals.ThinkPosHotkey)
        self.ignore(OTPGlobals.PrintCamPosHotkey)
        if self._LocalAvatar__enableMarkerPlacement:
            self.ignore(OTPGlobals.PlaceMarkerHotkey)

    def printCamPos(self):
        node = base.camera.getParent()
        pos = base.cam.getPos(node)
        hpr = base.cam.getHpr(node)
        print 'cam pos = ', `pos`, ', cam hpr = ', `hpr`

    def d_broadcastPositionNow(self):
        self.d_clearSmoothing()
        self.d_broadcastPosHpr()

    def travCollisionsLOS(self, n=None):
        if n == None:
            n = self._LocalAvatar__geom
        self.ccTrav.traverse(n)

    def travCollisionsFloor(self, n=None):
        if n == None:
            n = self._LocalAvatar__geom
        self.ccTravFloor.traverse(n)

    def travCollisionsPusher(self, n=None):
        if n == None:
            n = self._LocalAvatar__geom
        self.ccPusherTrav.traverse(n)

    def __friendOnline(self, doId, commonChatFlags=0, whitelistChatFlags=0):
        friend = base.cr.identifyFriend(doId)
        if friend != None and hasattr(friend, 'setCommonAndWhitelistChatFlags'):
            friend.setCommonAndWhitelistChatFlags(commonChatFlags, whitelistChatFlags)
        if self.oldFriendsList != None:
            now = globalClock.getFrameTime()
            elapsed = now - self.timeFriendsListChanged
            if elapsed < 10.0 and self.oldFriendsList.count(doId) == 0:
                self.oldFriendsList.append(doId)
                return
        if friend != None:
            self.setSystemMessage(doId, OTPLocalizer.WhisperFriendComingOnline % friend.getName())


    def __friendOffline(self, doId):
        friend = base.cr.identifyFriend(doId)
        if friend != None:
            self.setSystemMessage(0, OTPLocalizer.WhisperFriendLoggedOut % friend.getName())

    def __playerOnline(self, playerId):
        playerInfo = base.cr.playerFriendsManager.playerId2Info[playerId]
        if playerInfo:
            self.setSystemMessage(playerId, OTPLocalizer.WhisperPlayerOnline % (playerInfo.playerName, playerInfo.location))

    def __playerOffline(self, playerId):
        playerInfo = base.cr.playerFriendsManager.playerId2Info[playerId]
        if playerInfo:
            self.setSystemMessage(playerId, OTPLocalizer.WhisperPlayerOffline % playerInfo.playerName)

    def clickedWhisper(self, doId, isPlayer=None):
        if not isPlayer:
            friend = base.cr.identifyFriend(doId)
            if friend != None:
                messenger.send('clickedNametag', [friend])
                self.chatMgr.whisperTo(friend.getName(), doId)
        else:
            friend = base.cr.playerFriendsManager.getFriendInfo(doId)
            if friend:
                messenger.send('clickedNametagPlayer', [None, doId])
                self.chatMgr.whisperTo(friend.getName(), None, doId)

    def d_setParent(self, parentToken):
        DistributedSmoothNode.DistributedSmoothNode.d_setParent(self, parentToken)

    def handlePlayerFriendWhisper(self, playerId, charMessage):
        print 'handlePlayerFriendWhisper'
        self.displayWhisperPlayer(playerId, charMessage, WhisperPopup.WTNormal)

    def canChat(self):
        return 0
