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
    
    def addCameraPosition(self):
        pass
    
    def resetCameraPosition(self):
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

    def setLookAtPoint(self):
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

    def gotoNode(self, x=1):
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
        pass

    def walkSound(self):
        pass

    def stopSound(self):
        pass

    def wakeUp(self):
        pass

    def gotoSleep(self):
        pass

    def forceGotoSleep(self):
        pass

    def startSleepWatch(self):
        pass

    def stopSleepWatch(self):
        pass

    def startSleepSwimTest(self):
        pass

    def stopSleepSwimTest(self):
        pass

    def sleepSwimTest(self):
        pass

    def swimTimeoutAction(self):
        pass

    def trackAnimToSpeed(self):
        pass

    def startTrackAnimToSpeed(self):
        pass

    def stopTrackAnimToSpeed(self):
        pass

    def startChat(self):
        pass

    def stopChat(self):
        pass

    def printCamPos(self):
        pass

    def d_broadcastPositionNow(self):
        pass

    def travCollisionsLOS(self, x=None):
        pass

    def travCollisionsFloor(self, x=None):
        pass

    def travCollisionsPusher(self, x=None):
        pass

    def _LocalAvatar__friendOnline(self, a=0, b=0):
        pass

    def _LocalAvatar__friendOffline(self):
        pass

    def _LocalAvatar__playerOnline(self):
        pass

    def _LocalAvatar__playerOffline(self):
        pass

    def clickedWhisper(self, x=None):
        pass

    def d_setParent(self):
        pass

    def handlePlayerFriendWhisper(self):
        pass

    def canChat(self):
        pass
