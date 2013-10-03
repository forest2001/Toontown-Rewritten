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
        pass

    def updateSmartCameraCollisionLineSegment(self):
        pass

    def initializeSmartCamera(self):
        pass

    def shutdownSmartCamera(self):
        pass

    def setOnLevelGround(self):
        pass

    def setCameraCollisionsCanMove(self):
        pass

    def setGeom(self):
        pass

    def startUpdateSmartCamera(self, a=1):
        pass

    def stopUpdateSmartCamera(self):
        pass

    def updateSmartCamera(self):
        pass

    def positionCameraWithPusher(self):
        pass

    def nudgeCamera(self):
        pass

    def popCameraToDest(self):
        pass

    def handleCameraObstruction(self):
        pass

    def handleCameraFloorInteraction(self):
        pass

    def lerpCameraFov(self):
        pass

    def setCameraFov(self):
        pass

    def gotoNode(self, x=3):
        pass

    def setCustomMessages(self):
        pass

    def displayWhisper(self):
        pass

    def displayWhisperPlayer(self):
        pass

    def setAnimMultiplier(self):
        pass

    def getAnimMultiplier(self):
        pass

    def enableRun(self):
        pass

    def disableRun(self):
        pass

    def startRunWatch(self):
        pass

    def stopRunWatch(self):
        pass

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
        now = globalClock.getFrameTime()
        speed, rotSpeed, slideSpeed = self.controlManager.getSpeeds()
        if speed != 0.0 or rotSpeed != 0.0 or inputState.isSet('jump'):
            if not self.swimmingFlag:
                self.swimmingFlag = 1
        elif self.swimmingFlag:
            self.swimmingFlag = 0

        if self.swimmingFlag or self.hp <= 0:
            self.wakeUp()
        elif not self.sleepFlag:
            now = globalClock.getFrameTime()
            if now - self.lastMoved > self.swimTimeout:
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
