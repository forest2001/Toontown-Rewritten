# 2013.08.22 22:20:01 Pacific Daylight Time
# Embedded file name: toontown.estate.DistributedCannon
from pandac.PandaModules import *
from toontown.toonbase.ToonBaseGlobal import *
from toontown.toonbase import ToontownGlobals
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import ToontownTimer
from direct.task.Task import Task
from toontown.minigame import Trajectory
import math
from toontown.toon import ToonHead
from toontown.effects import Splash
from toontown.effects import DustCloud
from toontown.minigame import CannonGameGlobals
import CannonGlobals
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from toontown.toonbase import TTLocalizer
from direct.distributed import DistributedObject
from toontown.effects import Wake
from direct.controls.ControlManager import CollisionHandlerRayStart
LAND_TIME = 2
WORLD_SCALE = 2.0
GROUND_SCALE = 1.4 * WORLD_SCALE
CANNON_SCALE = 1.0
FAR_PLANE_DIST = 600 * WORLD_SCALE
GROUND_PLANE_MIN = -15
CANNON_Y = -int(CannonGameGlobals.TowerYRange / 2 * 1.3)
CANNON_X_SPACING = 12
CANNON_Z = 20
CANNON_ROTATION_MIN = -55
CANNON_ROTATION_MAX = 50
CANNON_ROTATION_VEL = 15.0
CANNON_ANGLE_MIN = 15
CANNON_ANGLE_MAX = 85
CANNON_ANGLE_VEL = 15.0
CANNON_MOVE_UPDATE_FREQ = 0.5
CAMERA_PULLBACK_MIN = 20
CAMERA_PULLBACK_MAX = 40
MAX_LOOKAT_OFFSET = 80
TOON_TOWER_THRESHOLD = 150
SHADOW_Z_OFFSET = 0.5
TOWER_HEIGHT = 43.85
TOWER_RADIUS = 10.5
BUCKET_HEIGHT = 36
TOWER_Y_RANGE = CannonGameGlobals.TowerYRange
TOWER_X_RANGE = int(TOWER_Y_RANGE / 2.0)
INITIAL_VELOCITY = 80.0
WHISTLE_SPEED = INITIAL_VELOCITY * 0.35

class DistributedCannon(DistributedObject.DistributedObject):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedCannon')
    font = ToontownGlobals.getToonFont()
    LOCAL_CANNON_MOVE_TASK = 'localCannonMoveTask'
    REWARD_COUNTDOWN_TASK = 'cannonGameRewardCountdown'
    HIT_GROUND = 0
    HIT_TOWER = 1
    HIT_WATER = 2
    FIRE_KEY = 'control'
    UP_KEY = 'arrow_up'
    DOWN_KEY = 'arrow_down'
    LEFT_KEY = 'arrow_left'
    RIGHT_KEY = 'arrow_right'
    BUMPER_KEY = 'delete'
    BUMPER_KEY2 = 'insert'
    INTRO_TASK_NAME = 'CannonGameIntro'
    INTRO_TASK_NAME_CAMERA_LERP = 'CannonGameIntroCamera'

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        self.avId = 0
        self.av = None
        self.localToonShooting = 0
        self.nodePath = None
        self.collSphere = None
        self.collNode = None
        self.collNodePath = None
        self.madeGui = 0
        self.gui = None
        self.cannonLocation = None
        self.cannonPosition = None
        self.cannon = None
        self.toonModel = None
        self.shadowNode = None
        self.toonHead = None
        self.toonScale = None
        self.estateId = None
        self.targetId = None
        self.splash = None
        self.dustCloud = None
        self.model_Created = 0
        self.lastWakeTime = 0
        self.leftPressed = 0
        self.rightPressed = 0
        self.upPressed = 0
        self.downPressed = 0
        self.hitBumper = 0
        self.hitTarget = 0
        self.lastPos = Vec3(0, 0, 0)
        self.lastVel = Vec3(0, 0, 0)
        self.vel = Vec3(0, 0, 0)
        self.landingPos = Vec3(0, 0, 0)
        self.t = 0
        self.lastT = 0
        self.deltaT = 0
        self.hitTrack = None
        self.cTrav = None
        self.cRay = None
        self.cRayNode = None
        self.cRayNodePath = None
        self.lifter = None
        self.flyColNode = None
        self.flyColNodePath = None
        self.bumperCol = None
        self.cannonMoving = 0
        self.inWater = 0
        self.localAvId = base.localAvatar.doId
        self.nextState = None
        self.nextKey = None
        self.cannonsActive = 0
        self.codeFSM = ClassicFSM.ClassicFSM('CannonCode', [State.State('init', self.enterInit, self.exitInit, ['u1', 'init']),
         State.State('u1', self.enteru1, self.exitu1, ['u2', 'init']),
         State.State('u2', self.enteru2, self.exitu2, ['d3', 'init']),
         State.State('d3', self.enterd3, self.exitd3, ['d4', 'init']),
         State.State('d4', self.enterd4, self.exitd4, ['l5', 'init']),
         State.State('l5', self.enterl5, self.exitl5, ['r6', 'init']),
         State.State('r6', self.enterr6, self.exitr6, ['l7', 'init']),
         State.State('l7', self.enterl7, self.exitl7, ['r8', 'init']),
         State.State('r8', self.enterr8, self.exitr8, ['acceptCode', 'init']),
         State.State('acceptCode', self.enterAcceptCode, self.exitAcceptCode, ['init', 'final']),
         State.State('final', self.enterFinal, self.exitFinal, [])], 'init', 'final')
        self.codeFSM.enterInitialState()
        self.curPinballScore = 0
        self.curPinballMultiplier = 1
        return

    def disable(self):
        self.__unmakeGui()
        taskMgr.remove(self.taskNameFireCannon)
        taskMgr.remove(self.taskNameShoot)
        taskMgr.remove(self.taskNameFly)
        taskMgr.remove(self.taskNameSmoke)
        self.ignoreAll()
        self.setMovie(CannonGlobals.CANNON_MOVIE_CLEAR, 0)
        self.nodePath.detachNode()
        if self.hitTrack:
            self.hitTrack.finish()
            del self.hitTrack
            self.hitTrack = None
        DistributedObject.DistributedObject.disable(self)
        return

    def __unmakeGui(self):
        if not self.madeGui:
            return
        self.aimPad.destroy()
        del self.aimPad
        del self.fireButton
        del self.upButton
        del self.downButton
        del self.leftButton
        del self.rightButton
        self.madeGui = 0

    def generateInit(self):
        DistributedObject.DistributedObject.generateInit(self)
        self.taskNameFireCannon = self.taskName('fireCannon')
        self.taskNameShoot = self.taskName('shootTask')
        self.taskNameSmoke = self.taskName('smokeTask')
        self.taskNameFly = self.taskName('flyTask')
        self.nodePath = NodePath(self.uniqueName('Cannon'))
        self.load()
        self.activateCannons()
        self.listenForCode()

    def listenForCode(self):
        self.accept(self.UP_KEY + '-up', self.__upKeyCode)
        self.accept(self.DOWN_KEY + '-up', self.__downKeyCode)
        self.accept(self.LEFT_KEY + '-up', self.__leftKeyCode)
        self.accept(self.RIGHT_KEY + '-up', self.__rightKeyCode)

    def ignoreCode(self):
        self.ignore(self.UP_KEY + '-up')
        self.ignore(self.DOWN_KEY + '-up')
        self.ignore(self.LEFT_KEY + '-up')
        self.ignore(self.RIGHT_KEY + '-up')

    def activateCannons(self):
        if not self.cannonsActive:
            self.cannonsActive = 1
            self.onstage()
            self.nodePath.reparentTo(self.getParentNodePath())
            self.accept(self.uniqueName('enterCannonSphere'), self.__handleEnterSphere)

    def deActivateCannons(self):
        if self.cannonsActive:
            self.cannonsActive = 0
            self.offstage()
            self.nodePath.reparentTo(hidden)
            self.ignore(self.uniqueName('enterCannonSphere'))

    def delete(self):
        self.offstage()
        self.unload()
        DistributedObject.DistributedObject.delete(self)

    def __handleEnterSphere(self, collEntry):
        self.notify.debug('collEntry: %s' % collEntry)
        base.cr.playGame.getPlace().setState('fishing')
        self.d_requestEnter()

    def d_requestEnter(self):
        self.sendUpdate('requestEnter', [])

    def requestExit(self):
        self.notify.debug('requestExit')
        base.localAvatar.reparentTo(render)
        base.cr.playGame.getPlace().setState('walk')

    def getSphereRadius(self):
        return 1.5

    def getParentNodePath(self):
        return base.cr.playGame.hood.loader.geom

    def setEstateId(self, estateId):
        self.estateId = estateId

    def setTargetId(self, targetId):
        self.notify.debug('setTargetId %d' % targetId)
        self.targetId = targetId

    def setPosHpr(self, x, y, z, h, p, r):
        self.nodePath.setPosHpr(x, y, z, h, p, r)

    def setMovie(self, mode, avId):
        wasLocalToon = self.localToonShooting
        self.avId = avId
        if mode == CannonGlobals.CANNON_MOVIE_CLEAR:
            self.listenForCode()
            self.setLanded()
        elif mode == CannonGlobals.CANNON_MOVIE_LANDED:
            self.setLanded()
        elif mode == CannonGlobals.CANNON_MOVIE_FORCE_EXIT:
            self.exitCannon(self.avId)
            self.setLanded()
        elif mode == CannonGlobals.CANNON_MOVIE_LOAD:
            self.ignoreCode()
            if self.avId == base.localAvatar.doId:
                base.localAvatar.pose('lose', 110)
                base.localAvatar.pose('slip-forward', 25)
                base.cr.playGame.getPlace().setState('fishing')
                base.localAvatar.setTeleportAvailable(0)
                base.localAvatar.collisionsOff()
                base.setCellsAvailable([base.bottomCells[3], base.bottomCells[4]], 0)
                base.setCellsAvailable([base.rightCells[1]], 0)
                self.localToonShooting = 1
                self.__makeGui()
                camera.reparentTo(self.barrel)
                camera.setPos(0.5, -2, 2.5)
                self.curPinballScore = 0
                self.curPinballMultiplier = 1
                self.incrementPinballInfo(0, 0)
            if self.cr.doId2do.has_key(self.avId):
                self.av = self.cr.doId2do[self.avId]
                self.acceptOnce(self.av.uniqueName('disable'), self.__avatarGone)
                self.av.stopSmooth()
                self.__createToonModels()
            else:
                self.notify.warning('Unknown avatar %d in cannon %d' % (self.avId, self.doId))
        if wasLocalToon and not self.localToonShooting:
            base.setCellsAvailable([base.bottomCells[3], base.bottomCells[4]], 1)
            base.setCellsAvailable([base.rightCells[1]], 1)

    def __avatarGone(self):
        self.setMovie(CannonGlobals.CANNON_MOVIE_CLEAR, 0)

    def load(self):
        self.cannon = loader.loadModel('phase_4/models/minigames/toon_cannon')
        self.shadow = loader.loadModel('phase_3/models/props/drop_shadow')
        self.shadowNode = hidden.attachNewNode('dropShadow')
        self.shadow.copyTo(self.shadowNode)
        self.smoke = loader.loadModel('phase_4/models/props/test_clouds')
        self.smoke.setBillboardPointEye()
        self.cannon.setScale(CANNON_SCALE)
        self.shadowNode.setColor(0, 0, 0, 0.5)
        self.shadowNode.setBin('fixed', 0, 1)
        self.splash = Splash.Splash(render)
        self.dustCloud = DustCloud.DustCloud(render)
        self.dustCloud.setBillboardPointEye()
        self.sndCannonMove = base.loadSfx('phase_4/audio/sfx/MG_cannon_adjust.mp3')
        self.sndCannonFire = base.loadSfx('phase_4/audio/sfx/MG_cannon_fire_alt.mp3')
        self.sndHitGround = base.loadSfx('phase_4/audio/sfx/MG_cannon_hit_dirt.mp3')
        self.sndHitTower = base.loadSfx('phase_4/audio/sfx/MG_cannon_hit_tower.mp3')
        self.sndHitWater = base.loadSfx('phase_4/audio/sfx/MG_cannon_splash.mp3')
        self.sndWhizz = base.loadSfx('phase_4/audio/sfx/MG_cannon_whizz.mp3')
        self.sndWin = base.loadSfx('phase_4/audio/sfx/MG_win.mp3')
        self.sndHitHouse = base.loadSfx('phase_5/audio/sfx/AA_drop_sandbag.mp3')
        self.collSphere = CollisionSphere(0, 0, 0, self.getSphereRadius())
        self.collSphere.setTangible(1)
        self.collNode = CollisionNode(self.uniqueName('CannonSphere'))
        self.collNode.setCollideMask(ToontownGlobals.WallBitmask)
        self.collNode.addSolid(self.collSphere)
        self.collNodePath = self.nodePath.attachNewNode(self.collNode)
        self.loadCannonBumper()

    def setupMovingShadow(self):
        self.cTrav = base.cTrav
        self.cRay = CollisionRay(0.0, 0.0, CollisionHandlerRayStart, 0.0, 0.0, -1.0)
        self.cRayNode = CollisionNode('cRayNode')
        self.cRayNode.addSolid(self.cRay)
        self.cRayNodePath = self.shadowNode.attachNewNode(self.cRayNode)
        self.cRayNodePath.hide()
        self.cRayBitMask = ToontownGlobals.FloorBitmask
        self.cRayNode.setFromCollideMask(self.cRayBitMask)
        self.cRayNode.setIntoCollideMask(BitMask32.allOff())
        self.lifter = CollisionHandlerFloor()
        self.lifter.setOffset(ToontownGlobals.FloorOffset)
        self.lifter.setReach(20.0)
        self.enableRaycast(1)

    def enableRaycast(self, enable = 1):
        if not self.cTrav or not hasattr(self, 'cRayNode') or not self.cRayNode:
            return
        self.notify.debug('-------enabling raycast--------')
        self.cTrav.removeCollider(self.cRayNodePath)
        if enable:
            self.cTrav.addCollider(self.cRayNodePath, self.lifter)

    def __makeGui(self):
        if self.madeGui:
            return
        guiModel = 'phase_4/models/gui/cannon_game_gui'
        cannonGui = loader.loadModel(guiModel)
        self.aimPad = DirectFrame(image=cannonGui.find('**/CannonFire_PAD'), relief=None, pos=(0.7, 0, -0.553333), scale=0.8)
        cannonGui.removeNode()
        self.fireButton = DirectButton(parent=self.aimPad, image=((guiModel, '**/Fire_Btn_UP'), (guiModel, '**/Fire_Btn_DN'), (guiModel, '**/Fire_Btn_RLVR')), relief=None, pos=(0.0115741, 0, 0.00505051), scale=1.0, command=self.__firePressed)
        self.upButton = DirectButton(parent=self.aimPad, image=((guiModel, '**/Cannon_Arrow_UP'), (guiModel, '**/Cannon_Arrow_DN'), (guiModel, '**/Cannon_Arrow_RLVR')), relief=None, pos=(0.0115741, 0, 0.221717))
        self.downButton = DirectButton(parent=self.aimPad, image=((guiModel, '**/Cannon_Arrow_UP'), (guiModel, '**/Cannon_Arrow_DN'), (guiModel, '**/Cannon_Arrow_RLVR')), relief=None, pos=(0.0136112, 0, -0.210101), image_hpr=(0, 0, 180))
        self.leftButton = DirectButton(parent=self.aimPad, image=((guiModel, '**/Cannon_Arrow_UP'), (guiModel, '**/Cannon_Arrow_DN'), (guiModel, '**/Cannon_Arrow_RLVR')), relief=None, pos=(-0.199352, 0, -0.000505269), image_hpr=(0, 0, -90))
        self.rightButton = DirectButton(parent=self.aimPad, image=((guiModel, '**/Cannon_Arrow_UP'), (guiModel, '**/Cannon_Arrow_DN'), (guiModel, '**/Cannon_Arrow_RLVR')), relief=None, pos=(0.219167, 0, -0.00101024), image_hpr=(0, 0, 90))
        self.aimPad.setColor(1, 1, 1, 0.9)

        def bindButton(button, upHandler, downHandler):
            button.bind(DGG.B1PRESS, lambda x, handler = upHandler: handler())
            button.bind(DGG.B1RELEASE, lambda x, handler = downHandler: handler())

        bindButton(self.upButton, self.__upPressed, self.__upReleased)
        bindButton(self.downButton, self.__downPressed, self.__downReleased)
        bindButton(self.leftButton, self.__leftPressed, self.__leftReleased)
        bindButton(self.rightButton, self.__rightPressed, self.__rightReleased)
        self.__enableAimInterface()
        self.madeGui = 1
        return

    def __unmakeGui(self):
        self.notify.debug('__unmakeGui')
        if not self.madeGui:
            return
        self.__disableAimInterface()
        self.upButton.unbind(DGG.B1PRESS)
        self.upButton.unbind(DGG.B1RELEASE)
        self.downButton.unbind(DGG.B1PRESS)
        self.downButton.unbind(DGG.B1RELEASE)
        self.leftButton.unbind(DGG.B1PRESS)
        self.leftButton.unbind(DGG.B1RELEASE)
        self.rightButton.unbind(DGG.B1PRESS)
        self.rightButton.unbind(DGG.B1RELEASE)
        self.aimPad.destroy()
        del self.aimPad
        del self.fireButton
        del self.upButton
        del self.downButton
        del self.leftButton
        del self.rightButton
        self.madeGui = 0

    def unload(self):
        self.ignoreCode()
        del self.codeFSM
        if self.cannon:
            self.cannon.removeNode()
            self.cannon = None
        if self.shadowNode != None:
            self.shadowNode.removeNode()
            del self.shadowNode
        if self.splash != None:
            self.splash.destroy()
            del self.splash
        if self.dustCloud != None:
            self.dustCloud.destroy()
            del self.dustCloud
        del self.sndCannonMove
        del self.sndCannonFire
        del self.sndHitHouse
        del self.sndHitGround
        del self.sndHitTower
        del self.sndHitWater
        del self.sndWhizz
        del self.sndWin
        self.bumperCol = None
        taskMgr.remove(self.uniqueName('BumperON'))
        if self.av:
            self.__resetToon(self.av)
            self.av.loop('neutral')
            self.av.setPlayRate(1.0, 'run')
            if hasattr(self.av, 'nametag'):
                self.av.nametag.removeNametag(self.toonHead.tag)
        if self.toonHead != None:
            self.toonHead.stopBlink()
            self.toonHead.stopLookAroundNow()
            self.toonHead.delete()
            self.toonHead = None
        if self.toonModel != None:
            self.toonModel.removeNode()
            self.toonModel = None
        del self.toonScale
        del self.cannonLocation
        del self.cRay
        del self.cRayNode
        if self.cRayNodePath:
            self.cRayNodePath.removeNode()
            del self.cRayNodePath
        del self.lifter
        self.enableRaycast(0)
        return

    def onstage(self):
        self.__createCannon()
        self.cannon.reparentTo(self.nodePath)
        self.splash.reparentTo(render)
        self.dustCloud.reparentTo(render)

    def offstage(self):
        if self.cannon:
            self.cannon.reparentTo(hidden)
        if self.splash:
            self.splash.reparentTo(hidden)
            self.splash.stop()
        if self.dustCloud:
            self.dustCloud.reparentTo(hidden)
            self.dustCloud.stop()

    def __createCannon(self):
        self.barrel = self.cannon.find('**/cannon')
        self.cannonLocation = Point3(0, 0, 0.025)
        self.cannonPosition = [0, CANNON_ANGLE_MIN]
        self.cannon.setPos(self.cannonLocation)
        self.__updateCannonPosition(self.avId)

    def __createToonModels(self):
        self.model_Created = 1
        toon = self.av
        self.toonScale = toon.getScale()
        toon.useLOD(1000)
        toonParent = render.attachNewNode('toonOriginChange')
        toon.wrtReparentTo(toonParent)
        toon.setPosHpr(0, 0, -(toon.getHeight() / 2.0), 0, -90, 0)
        self.toonModel = toonParent
        self.toonHead = ToonHead.ToonHead()
        self.toonHead.setupHead(self.av.style)
        self.toonHead.reparentTo(hidden)
        tag = NametagFloat3d()
        tag.setContents(Nametag.CSpeech | Nametag.CThought)
        tag.setBillboardOffset(0)
        tag.setAvatar(self.toonHead)
        toon.nametag.addNametag(tag)
        tagPath = self.toonHead.attachNewNode(tag.upcastToPandaNode())
        tagPath.setPos(0, 0, 1)
        self.toonHead.tag = tag
        self.__loadToonInCannon()
        self.av.dropShadow.hide()
        self.dropShadow = self.shadowNode.copyTo(hidden)

    def __destroyToonModels(self):
        if self.av != None:
            self.av.dropShadow.show()
            if self.dropShadow != None:
                self.dropShadow.removeNode()
                self.dropShadow = None
            self.hitBumper = 0
            self.hitTarget = 0
            self.angularVel = 0
            self.vel = Vec3(0, 0, 0)
            self.lastVel = Vec3(0, 0, 0)
            self.lastPos = Vec3(0, 0, 0)
            self.landingPos = Vec3(0, 0, 0)
            self.t = 0
            self.lastT = 0
            self.deltaT = 0
            self.av = None
            self.lastWakeTime = 0
            self.localToonShooting = 0
        if self.toonHead != None:
            self.toonHead.reparentTo(hidden)
            self.toonHead.stopBlink()
            self.toonHead.stopLookAroundNow()
            self.toonHead.delete()
            self.toonHead = None
        if self.toonModel != None:
            self.toonModel.removeNode()
            self.toonModel = None
        self.model_Created = 0
        return

    def updateCannonPosition(self, avId, zRot, angle):
        if avId != self.localAvId:
            self.cannonPosition = [zRot, angle]
            self.__updateCannonPosition(avId)

    def setCannonWillFire(self, avId, fireTime, zRot, angle, timestamp):
        self.notify.debug('setCannonWillFire: ' + str(avId) + ': zRot=' + str(zRot) + ', angle=' + str(angle) + ', time=' + str(fireTime))
        if not self.model_Created:
            self.notify.warning("We walked into the zone mid-flight, so we won't see it")
            return
        self.cannonPosition[0] = zRot
        self.cannonPosition[1] = angle
        self.__updateCannonPosition(avId)
        task = Task(self.__fireCannonTask)
        task.avId = avId
        ts = globalClockDelta.localElapsedTime(timestamp)
        task.fireTime = fireTime - ts
        if task.fireTime < 0.0:
            task.fireTime = 0.0
        taskMgr.add(task, self.taskNameFireCannon)

    def exitCannon(self, avId):
        self.__unmakeGui()
        if self.avId == avId:
            if self.av:
                self.__resetToonToCannon(self.av)

    def __enableAimInterface(self):
        self.aimPad.show()
        self.accept(self.FIRE_KEY, self.__fireKeyPressed)
        self.accept(self.UP_KEY, self.__upKeyPressed)
        self.accept(self.DOWN_KEY, self.__downKeyPressed)
        self.accept(self.LEFT_KEY, self.__leftKeyPressed)
        self.accept(self.RIGHT_KEY, self.__rightKeyPressed)
        self.accept(self.BUMPER_KEY, self.__bumperKeyPressed)
        self.accept(self.BUMPER_KEY2, self.__bumperKeyPressed)
        self.__spawnLocalCannonMoveTask()

    def __disableAimInterface(self):
        self.aimPad.hide()
        self.ignore(self.FIRE_KEY)
        self.ignore(self.UP_KEY)
        self.ignore(self.DOWN_KEY)
        self.ignore(self.LEFT_KEY)
        self.ignore(self.RIGHT_KEY)
        self.ignore(self.FIRE_KEY + '-up')
        self.ignore(self.UP_KEY + '-up')
        self.ignore(self.DOWN_KEY + '-up')
        self.ignore(self.LEFT_KEY + '-up')
        self.ignore(self.RIGHT_KEY + '-up')
        self.__killLocalCannonMoveTask()

    def __fireKeyPressed(self):
        self.ignore(self.FIRE_KEY)
        self.accept(self.FIRE_KEY + '-up', self.__fireKeyReleased)
        self.__firePressed()

    def __upKeyPressed(self):
        self.ignore(self.UP_KEY)
        self.accept(self.UP_KEY + '-up', self.__upKeyReleased)
        self.__upPressed()

    def __downKeyPressed(self):
        self.ignore(self.DOWN_KEY)
        self.accept(self.DOWN_KEY + '-up', self.__downKeyReleased)
        self.__downPressed()

    def __leftKeyPressed(self):
        self.ignore(self.LEFT_KEY)
        self.accept(self.LEFT_KEY + '-up', self.__leftKeyReleased)
        self.__leftPressed()

    def __rightKeyPressed(self):
        self.ignore(self.RIGHT_KEY)
        self.accept(self.RIGHT_KEY + '-up', self.__rightKeyReleased)
        self.__rightPressed()

    def __fireKeyReleased(self):
        self.ignore(self.FIRE_KEY + '-up')
        self.accept(self.FIRE_KEY, self.__fireKeyPressed)
        self.__fireReleased()

    def __leftKeyReleased(self):
        self.ignore(self.LEFT_KEY + '-up')
        self.accept(self.LEFT_KEY, self.__leftKeyPressed)
        self.handleCodeKey('left')
        self.__leftReleased()

    def __rightKeyReleased(self):
        self.ignore(self.RIGHT_KEY + '-up')
        self.accept(self.RIGHT_KEY, self.__rightKeyPressed)
        self.handleCodeKey('right')
        self.__rightReleased()

    def __upKeyReleased(self):
        self.ignore(self.UP_KEY + '-up')
        self.accept(self.UP_KEY, self.__upKeyPressed)
        self.__upReleased()

    def __downKeyReleased(self):
        self.ignore(self.DOWN_KEY + '-up')
        self.accept(self.DOWN_KEY, self.__downKeyPressed)
        self.handleCodeKey('down')
        self.__downReleased()

    def __upKeyCode(self):
        self.handleCodeKey('up')

    def __downKeyCode(self):
        self.handleCodeKey('down')

    def __rightKeyCode(self):
        self.handleCodeKey('right')

    def __leftKeyCode(self):
        self.handleCodeKey('left')

    def __firePressed(self):
        self.notify.debug('fire pressed')
        self.__broadcastLocalCannonPosition()
        self.__unmakeGui()
        self.sendUpdate('setCannonLit', [self.cannonPosition[0], self.cannonPosition[1]])

    def __upPressed(self):
        self.notify.debug('up pressed')
        self.upPressed = self.__enterControlActive(self.upPressed)

    def __downPressed(self):
        self.notify.debug('down pressed')
        self.downPressed = self.__enterControlActive(self.downPressed)

    def __leftPressed(self):
        self.notify.debug('left pressed')
        self.leftPressed = self.__enterControlActive(self.leftPressed)

    def __rightPressed(self):
        self.notify.debug('right pressed')
        self.rightPressed = self.__enterControlActive(self.rightPressed)

    def __upReleased(self):
        self.notify.debug('up released')
        self.upPressed = self.__exitControlActive(self.upPressed)

    def __downReleased(self):
        self.notify.debug('down released')
        self.downPressed = self.__exitControlActive(self.downPressed)

    def __leftReleased(self):
        self.notify.debug('left released')
        self.leftPressed = self.__exitControlActive(self.leftPressed)

    def __rightReleased(self):
        self.notify.debug('right released')
        self.rightPressed = self.__exitControlActive(self.rightPressed)

    def __enterControlActive(self, control):
        return control + 1

    def __exitControlActive(self, control):
        return max(0, control - 1)

    def __spawnLocalCannonMoveTask(self):
        self.leftPressed = 0
        self.rightPressed = 0
        self.upPressed = 0
        self.downPressed = 0
        self.cannonMoving = 0
        task = Task(self.__localCannonMoveTask)
        task.lastPositionBroadcastTime = 0.0
        taskMgr.add(task, self.LOCAL_CANNON_MOVE_TASK)

    def __killLocalCannonMoveTask(self):
        taskMgr.remove(self.LOCAL_CANNON_MOVE_TASK)
        if self.cannonMoving:
            self.sndCannonMove.stop()

    def __localCannonMoveTask(self, task):
        pos = self.cannonPosition
        oldRot = pos[0]
        oldAng = pos[1]
        rotVel = 0
        if self.leftPressed:
            rotVel += CANNON_ROTATION_VEL
        if self.rightPressed:
            rotVel -= CANNON_ROTATION_VEL
        pos[0] += rotVel * globalClock.getDt()
        if pos[0] < CANNON_ROTATION_MIN:
            pos[0] = CANNON_ROTATION_MIN
        elif pos[0] > CANNON_ROTATION_MAX:
            pos[0] = CANNON_ROTATION_MAX
        angVel = 0
        if self.upPressed:
            angVel += CANNON_ANGLE_VEL
        if self.downPressed:
            angVel -= CANNON_ANGLE_VEL
        pos[1] += angVel * globalClock.getDt()
        if pos[1] < CANNON_ANGLE_MIN:
            pos[1] = CANNON_ANGLE_MIN
        elif pos[1] > CANNON_ANGLE_MAX:
            pos[1] = CANNON_ANGLE_MAX
        if oldRot != pos[0] or oldAng != pos[1]:
            if self.cannonMoving == 0:
                self.cannonMoving = 1
                base.playSfx(self.sndCannonMove, looping=1)
            self.__updateCannonPosition(self.localAvId)
            if task.time - task.lastPositionBroadcastTime > CANNON_MOVE_UPDATE_FREQ:
                task.lastPositionBroadcastTime = task.time
                self.__broadcastLocalCannonPosition()
        elif self.cannonMoving:
            self.cannonMoving = 0
            self.sndCannonMove.stop()
            self.__broadcastLocalCannonPosition()
            print 'Cannon Rot:%s Angle:%s' % (pos[0], pos[1])
        return Task.cont

    def __broadcastLocalCannonPosition(self):
        self.sendUpdate('setCannonPosition', [self.cannonPosition[0], self.cannonPosition[1]])

    def __updateCannonPosition(self, avId):
        self.cannon.setHpr(self.cannonPosition[0], 0.0, 0.0)
        self.barrel.setHpr(0.0, self.cannonPosition[1], 0.0)
        maxP = 90
        newP = self.barrel.getP()
        yScale = 1 - 0.5 * float(newP) / maxP
        shadow = self.cannon.find('**/square_drop_shadow')
        shadow.setScale(1, yScale, 1)

    def __getCameraPositionBehindCannon(self):
        return Point3(self.cannonLocationDict[self.localAvId][0], CANNON_Y - 5.0, CANNON_Z + 7)

    def __putCameraBehindCannon(self):
        camera.setPos(self.__getCameraPositionBehindCannon())
        camera.setHpr(0, 0, 0)

    def __loadToonInCannon(self):
        self.toonModel.reparentTo(hidden)
        self.toonHead.startBlink()
        self.toonHead.startLookAround()
        self.toonHead.reparentTo(self.barrel)
        self.toonHead.setPosHpr(0, 6, 0, 0, -45, 0)
        sc = self.toonScale
        self.toonHead.setScale(render, sc[0], sc[1], sc[2])
        self.toonModel.setPos(self.toonHead.getPos(render))

    def __toRadians(self, angle):
        return angle * 2.0 * math.pi / 360.0

    def __toDegrees(self, angle):
        return angle * 360.0 / (2.0 * math.pi)

    def __calcFlightResults(self, avId, launchTime):
        head = self.toonHead
        startPos = head.getPos(render)
        startHpr = head.getHpr(render)
        hpr = self.barrel.getHpr(render)
        rotation = self.__toRadians(hpr[0])
        angle = self.__toRadians(hpr[1])
        horizVel = INITIAL_VELOCITY * math.cos(angle)
        xVel = horizVel * -math.sin(rotation)
        yVel = horizVel * math.cos(rotation)
        zVel = INITIAL_VELOCITY * math.sin(angle)
        startVel = Vec3(xVel, yVel, zVel)
        trajectory = Trajectory.Trajectory(launchTime, startPos, startVel)
        self.trajectory = trajectory
        hitTreasures = self.__calcHitTreasures(trajectory)
        timeOfImpact, hitWhat = self.__calcToonImpact(trajectory)
        return {'startPos': startPos,
         'startHpr': startHpr,
         'startVel': startVel,
         'trajectory': trajectory,
         'timeOfImpact': 3 * timeOfImpact,
         'hitWhat': hitWhat}

    def __fireCannonTask(self, task):
        launchTime = task.fireTime
        avId = task.avId
        self.inWater = 0
        if not self.toonHead:
            return Task.done
        flightResults = self.__calcFlightResults(avId, launchTime)
        if not isClient():
            print 'EXECWARNING DistributedCannon: %s' % flightResults
            printStack()
        for key in flightResults:
            exec "%s = flightResults['%s']" % (key, key)

        self.notify.debug('start position: ' + str(startPos))
        self.notify.debug('start velocity: ' + str(startVel))
        self.notify.debug('time of launch: ' + str(launchTime))
        self.notify.debug('time of impact: ' + str(timeOfImpact))
        self.notify.debug('location of impact: ' + str(trajectory.getPos(timeOfImpact)))
        if hitWhat == self.HIT_WATER:
            self.notify.debug('toon will land in the water')
        elif hitWhat == self.HIT_TOWER:
            self.notify.debug('toon will hit the tower')
        else:
            self.notify.debug('toon will hit the ground')
        head = self.toonHead
        head.stopBlink()
        head.stopLookAroundNow()
        head.reparentTo(hidden)
        av = self.toonModel
        av.reparentTo(render)
        print 'start Pos%s Hpr%s' % (startPos, startHpr)
        av.setPos(startPos)
        barrelHpr = self.barrel.getHpr(render)
        place = base.cr.playGame.getPlace()
        if self.av == base.localAvatar:
            place.fsm.request('stopped')
        av.setHpr(startHpr)
        avatar = self.av
        avatar.loop('swim')
        avatar.setPosHpr(0, 0, -(avatar.getHeight() / 2.0), 0, 0, 0)
        info = {}
        info['avId'] = avId
        info['trajectory'] = trajectory
        info['launchTime'] = launchTime
        info['timeOfImpact'] = timeOfImpact
        info['hitWhat'] = hitWhat
        info['toon'] = self.toonModel
        info['hRot'] = self.cannonPosition[0]
        info['haveWhistled'] = 0
        info['maxCamPullback'] = CAMERA_PULLBACK_MIN
        if self.localToonShooting:
            camera.reparentTo(self.av)
            camera.setP(45.0)
            camera.setZ(-10.0)
        self.flyColSphere = CollisionSphere(0, 0, self.av.getHeight() / 2.0, 1.0)
        self.flyColNode = CollisionNode(self.uniqueName('flySphere'))
        self.flyColNode.setCollideMask(ToontownGlobals.WallBitmask | ToontownGlobals.FloorBitmask)
        self.flyColNode.addSolid(self.flyColSphere)
        self.flyColNodePath = self.av.attachNewNode(self.flyColNode)
        self.flyColNodePath.setColor(1, 0, 0, 1)
        self.handler = CollisionHandlerEvent()
        self.handler.setInPattern(self.uniqueName('cannonHit'))
        base.cTrav.addCollider(self.flyColNodePath, self.handler)
        self.accept(self.uniqueName('cannonHit'), self.__handleCannonHit)
        shootTask = Task(self.__shootTask, self.taskNameShoot)
        smokeTask = Task(self.__smokeTask, self.taskNameSmoke)
        flyTask = Task(self.__flyTask, self.taskNameFly)
        shootTask.info = info
        flyTask.info = info
        seqTask = Task.sequence(shootTask, smokeTask, flyTask)
        if self.av == base.localAvatar:
            print 'disable controls'
            base.localAvatar.disableAvatarControls()
        taskMgr.add(seqTask, self.taskName('flyingToon') + '-' + str(avId))
        self.acceptOnce(self.uniqueName('stopFlyTask'), self.__stopFlyTask)
        return Task.done

    def __stopFlyTask(self, avId):
        taskMgr.remove(self.taskName('flyingToon') + '-' + str(avId))

    def b_setLanded(self):
        self.d_setLanded()

    def d_setLanded(self):
        self.notify.debug('localTOonshooting = %s' % self.localToonShooting)
        if self.localToonShooting:
            self.sendUpdate('setLanded', [])

    def setLanded(self):
        self.removeAvFromCannon()

    def removeAvFromCannon(self):
        place = base.cr.playGame.getPlace()
        print 'removeAvFromCannon'
        self.notify.debug('self.inWater = %s' % self.inWater)
        if place:
            if not hasattr(place, 'fsm'):
                return
            placeState = place.fsm.getCurrentState().getName()
            print placeState
            if (self.inWater or place.toonSubmerged) and placeState != 'fishing':
                if self.av != None:
                    self.av.startSmooth()
                    self.__destroyToonModels()
                    return
        self.inWater = 0
        if self.av != None:
            self.__stopCollisionHandler(self.av)
            self.av.resetLOD()
            if self.av == base.localAvatar:
                if place and not self.inWater:
                    place.fsm.request('walk')
            self.av.setPlayRate(1.0, 'run')
            self.av.nametag.removeNametag(self.toonHead.tag)
            if self.av.getParent().getName() == 'toonOriginChange':
                self.av.wrtReparentTo(render)
                self.__setToonUpright(self.av)
            if self.av == base.localAvatar:
                self.av.startPosHprBroadcast()
            self.av.startSmooth()
            self.av.setScale(1, 1, 1)
            if self.av == base.localAvatar:
                print 'enable controls'
                base.localAvatar.enableAvatarControls()
            self.ignore(self.av.uniqueName('disable'))
            self.__destroyToonModels()
        return

    def __stopCollisionHandler(self, avatar):
        if avatar:
            avatar.loop('neutral')
            if self.flyColNode:
                self.flyColNode = None
            if avatar == base.localAvatar:
                avatar.collisionsOn()
            self.flyColSphere = None
            if self.flyColNodePath:
                base.cTrav.removeCollider(self.flyColNodePath)
                self.flyColNodePath.removeNode()
                self.flyColNodePath = None
            self.handler = None
        return

    def __handleCannonHit--- This code section failed: ---

0	LOAD_FAST         'self'
3	LOAD_ATTR         'av'
6	LOAD_CONST        None
9	COMPARE_OP        '=='
12	JUMP_IF_TRUE      '30'
15	LOAD_FAST         'self'
18	LOAD_ATTR         'flyColNode'
21	LOAD_CONST        None
24	COMPARE_OP        '=='
27_0	COME_FROM         '12'
27	JUMP_IF_FALSE     '37'

30	LOAD_CONST        None
33	RETURN_VALUE      None
34	JUMP_FORWARD      '37'
37_0	COME_FROM         '34'

37	LOAD_FAST         'collisionEntry'
40	LOAD_ATTR         'getIntoNode'
43	CALL_FUNCTION_0   None
46	LOAD_ATTR         'getName'
49	CALL_FUNCTION_0   None
52	STORE_FAST        'hitNode'

55	LOAD_FAST         'self'
58	LOAD_ATTR         'notify'
61	LOAD_ATTR         'debug'
64	LOAD_CONST        'hitNode = %s'
67	LOAD_FAST         'hitNode'
70	BINARY_MODULO     None
71	CALL_FUNCTION_1   None
74	POP_TOP           None

75	LOAD_FAST         'self'
78	LOAD_ATTR         'notify'
81	LOAD_ATTR         'debug'
84	LOAD_CONST        'hitNodePath.getParent = %s'
87	LOAD_FAST         'collisionEntry'
90	LOAD_ATTR         'getIntoNodePath'
93	CALL_FUNCTION_0   None
96	LOAD_ATTR         'getParent'
99	CALL_FUNCTION_0   None
102	BINARY_MODULO     None
103	CALL_FUNCTION_1   None
106	POP_TOP           None

107	LOAD_FAST         'self'
110	LOAD_ATTR         'trajectory'
113	LOAD_ATTR         'getVel'
116	LOAD_FAST         'self'
119	LOAD_ATTR         't'
122	CALL_FUNCTION_1   None
125	LOAD_FAST         'self'
128	STORE_ATTR        'vel'

131	LOAD_FAST         'self'
134	LOAD_ATTR         'trajectory'
137	LOAD_ATTR         'getVel'
140	LOAD_FAST         'self'
143	LOAD_ATTR         't'
146	CALL_FUNCTION_1   None
149	STORE_FAST        'vel'

152	LOAD_FAST         'vel'
155	LOAD_ATTR         'normalize'
158	CALL_FUNCTION_0   None
161	POP_TOP           None

162	LOAD_FAST         'self'
165	LOAD_ATTR         'hitBumper'
168	JUMP_IF_FALSE     '197'

171	LOAD_FAST         'self'
174	LOAD_ATTR         'lastVel'
177	LOAD_CONST        1
180	BINARY_MULTIPLY   None
181	STORE_FAST        'vel'

184	LOAD_FAST         'vel'
187	LOAD_ATTR         'normalize'
190	CALL_FUNCTION_0   None
193	POP_TOP           None
194	JUMP_FORWARD      '197'
197_0	COME_FROM         '194'

197	LOAD_FAST         'self'
200	LOAD_ATTR         'notify'
203	LOAD_ATTR         'debug'
206	LOAD_CONST        'normalized vel=%s'
209	LOAD_FAST         'vel'
212	BINARY_MODULO     None
213	CALL_FUNCTION_1   None
216	POP_TOP           None

217	LOAD_FAST         'collisionEntry'
220	LOAD_ATTR         'getInto'
223	CALL_FUNCTION_0   None
226	STORE_FAST        'solid'

229	LOAD_FAST         'collisionEntry'
232	LOAD_ATTR         'getSurfaceNormal'
235	LOAD_FAST         'collisionEntry'
238	LOAD_ATTR         'getIntoNodePath'
241	CALL_FUNCTION_0   None
244	CALL_FUNCTION_1   None
247	STORE_FAST        'intoNormal'

250	LOAD_FAST         'self'
253	LOAD_ATTR         'notify'
256	LOAD_ATTR         'debug'
259	LOAD_CONST        'old intoNormal = %s'
262	LOAD_FAST         'intoNormal'
265	BINARY_MODULO     None
266	CALL_FUNCTION_1   None
269	POP_TOP           None

270	LOAD_FAST         'collisionEntry'
273	LOAD_ATTR         'getSurfaceNormal'
276	LOAD_GLOBAL       'render'
279	CALL_FUNCTION_1   None
282	STORE_FAST        'intoNormal'

285	LOAD_FAST         'self'
288	LOAD_ATTR         'notify'
291	LOAD_ATTR         'debug'
294	LOAD_CONST        'new intoNormal = %s'
297	LOAD_FAST         'intoNormal'
300	BINARY_MODULO     None
301	CALL_FUNCTION_1   None
304	POP_TOP           None

305	LOAD_GLOBAL       'False'
308	STORE_FAST        'hitPylonAboveWater'

311	LOAD_GLOBAL       'False'
314	STORE_FAST        'hitPylonBelowWater'

317	LOAD_FAST         'hitNode'
320	LOAD_CONST        'pier_pylon_collisions_1'
323	LOAD_CONST        'pier_pylon_collisions_3'
326	BUILD_LIST_2      None
329	COMPARE_OP        'in'
332	JUMP_IF_FALSE     '410'

335	LOAD_FAST         'collisionEntry'
338	LOAD_ATTR         'getSurfacePoint'
341	LOAD_GLOBAL       'render'
344	CALL_FUNCTION_1   None
347	LOAD_CONST        2
350	BINARY_SUBSCR     None
351	LOAD_CONST        0
354	COMPARE_OP        '>'
357	JUMP_IF_FALSE     '385'

360	LOAD_GLOBAL       'True'
363	STORE_FAST        'hitPylonAboveWater'

366	LOAD_FAST         'self'
369	LOAD_ATTR         'notify'
372	LOAD_ATTR         'debug'
375	LOAD_CONST        'hitPylonAboveWater = True'
378	CALL_FUNCTION_1   None
381	POP_TOP           None
382	JUMP_ABSOLUTE     '410'

385	LOAD_GLOBAL       'True'
388	STORE_FAST        'hitPylonBelowWater'

391	LOAD_FAST         'self'
394	LOAD_ATTR         'notify'
397	LOAD_ATTR         'debug'
400	LOAD_CONST        'hitPylonBelowWater = True'
403	CALL_FUNCTION_1   None
406	POP_TOP           None
407	JUMP_FORWARD      '410'
410_0	COME_FROM         '407'

410	LOAD_FAST         'intoNormal'
413	STORE_FAST        'hitNormal'

416	LOAD_FAST         'hitNode'
419	LOAD_ATTR         'find'
422	LOAD_CONST        'cSphere'
425	CALL_FUNCTION_1   None
428	LOAD_CONST        0
431	COMPARE_OP        '=='
434	JUMP_IF_TRUE      '647'
437	LOAD_FAST         'hitNode'
440	LOAD_ATTR         'find'
443	LOAD_CONST        'treasureSphere'
446	CALL_FUNCTION_1   None
449	LOAD_CONST        0
452	COMPARE_OP        '=='
455	JUMP_IF_TRUE      '647'
458	LOAD_FAST         'hitNode'
461	LOAD_ATTR         'find'
464	LOAD_CONST        'prop'
467	CALL_FUNCTION_1   None
470	LOAD_CONST        0
473	COMPARE_OP        '=='
476	JUMP_IF_TRUE      '647'
479	LOAD_FAST         'hitNode'
482	LOAD_ATTR         'find'
485	LOAD_CONST        'distAvatarCollNode'
488	CALL_FUNCTION_1   None
491	LOAD_CONST        0
494	COMPARE_OP        '=='
497	JUMP_IF_TRUE      '647'
500	LOAD_FAST         'hitNode'
503	LOAD_ATTR         'find'
506	LOAD_CONST        'CannonSphere'
509	CALL_FUNCTION_1   None
512	LOAD_CONST        0
515	COMPARE_OP        '=='
518	JUMP_IF_TRUE      '647'
521	LOAD_FAST         'hitNode'
524	LOAD_ATTR         'find'
527	LOAD_CONST        'plotSphere'
530	CALL_FUNCTION_1   None
533	LOAD_CONST        0
536	COMPARE_OP        '=='
539	JUMP_IF_TRUE      '647'
542	LOAD_FAST         'hitNode'
545	LOAD_ATTR         'find'
548	LOAD_CONST        'flySphere'
551	CALL_FUNCTION_1   None
554	LOAD_CONST        0
557	COMPARE_OP        '=='
560	JUMP_IF_TRUE      '647'
563	LOAD_FAST         'hitNode'
566	LOAD_ATTR         'find'
569	LOAD_CONST        'mailboxSphere'
572	CALL_FUNCTION_1   None
575	LOAD_CONST        0
578	COMPARE_OP        '=='
581	JUMP_IF_TRUE      '647'
584	LOAD_FAST         'hitNode'
587	LOAD_ATTR         'find'
590	LOAD_CONST        'FishingSpotSphere'
593	CALL_FUNCTION_1   None
596	LOAD_CONST        0
599	COMPARE_OP        '=='
602	JUMP_IF_TRUE      '647'
605	LOAD_FAST         'hitNode'
608	LOAD_CONST        'gagtree_collision'
611	COMPARE_OP        '=='
614	JUMP_IF_TRUE      '647'
617	LOAD_FAST         'hitNode'
620	LOAD_CONST        'sign_collision'
623	COMPARE_OP        '=='
626	JUMP_IF_TRUE      '647'
629	LOAD_FAST         'hitNode'
632	LOAD_CONST        'FlowerSellBox'
635	COMPARE_OP        '=='
638	JUMP_IF_TRUE      '647'
641	LOAD_FAST         'hitPylonBelowWater'
644_0	COME_FROM         '434'
644_1	COME_FROM         '455'
644_2	COME_FROM         '476'
644_3	COME_FROM         '497'
644_4	COME_FROM         '518'
644_5	COME_FROM         '539'
644_6	COME_FROM         '560'
644_7	COME_FROM         '581'
644_8	COME_FROM         '602'
644_9	COME_FROM         '614'
644_10	COME_FROM         '626'
644_11	COME_FROM         '638'
644	JUMP_IF_FALSE     '674'

647	LOAD_FAST         'self'
650	LOAD_ATTR         'notify'
653	LOAD_ATTR         'debug'
656	LOAD_CONST        '--------------hit and ignoring %s'
659	LOAD_FAST         'hitNode'
662	BINARY_MODULO     None
663	CALL_FUNCTION_1   None
666	POP_TOP           None

667	LOAD_CONST        None
670	RETURN_VALUE      None
671	JUMP_FORWARD      '674'
674_0	COME_FROM         '671'

674	LOAD_FAST         'vel'
677	LOAD_ATTR         'dot'
680	LOAD_FAST         'hitNormal'
683	CALL_FUNCTION_1   None
686	LOAD_CONST        0
689	COMPARE_OP        '>'
692	JUMP_IF_FALSE     '763'
695	LOAD_FAST         'hitNode'
698	LOAD_CONST        'collision_roof'
701	COMPARE_OP        '=='
704	UNARY_NOT         None
705	JUMP_IF_FALSE     '763'
708	LOAD_FAST         'hitNode'
711	LOAD_CONST        'collision_fence'
714	COMPARE_OP        '=='
717	UNARY_NOT         None
718_0	COME_FROM         '692'
718_1	COME_FROM         '705'
718	JUMP_IF_FALSE     '763'

721	LOAD_FAST         'self'
724	LOAD_ATTR         'notify'
727	LOAD_ATTR         'debug'
730	LOAD_CONST        '--------------hit and ignoring backfacing %s, dot=%s'
733	LOAD_FAST         'hitNode'
736	LOAD_FAST         'vel'
739	LOAD_ATTR         'dot'
742	LOAD_FAST         'hitNormal'
745	CALL_FUNCTION_1   None
748	BUILD_TUPLE_2     None
751	BINARY_MODULO     None
752	CALL_FUNCTION_1   None
755	POP_TOP           None

756	LOAD_CONST        None
759	RETURN_VALUE      None
760	JUMP_FORWARD      '763'
763_0	COME_FROM         '760'

763	LOAD_FAST         'collisionEntry'
766	LOAD_ATTR         'getIntoNodePath'
769	CALL_FUNCTION_0   None
772	STORE_FAST        'intoNode'

775	LOAD_CONST        'collision_house'
778	LOAD_CONST        'collision_fence'
781	LOAD_CONST        'targetSphere'
784	LOAD_CONST        'collision_roof'
787	LOAD_CONST        'collision_cannon_bumper'
790	LOAD_CONST        'statuaryCol'
793	BUILD_LIST_6      None
796	STORE_FAST        'bumperNodes'

799	LOAD_CONST        'cloudSphere-0'
802	BUILD_LIST_1      None
805	STORE_FAST        'cloudBumpers'

808	LOAD_FAST         'bumperNodes'
811	LOAD_FAST         'cloudBumpers'
814	INPLACE_ADD       None
815	STORE_FAST        'bumperNodes'

818	LOAD_FAST         'hitNode'
821	LOAD_FAST         'bumperNodes'
824	COMPARE_OP        'not in'
827	JUMP_IF_FALSE     '916'

830	LOAD_FAST         'self'
833	LOAD_ATTR         '__stopCollisionHandler'
836	LOAD_FAST         'self'
839	LOAD_ATTR         'av'
842	CALL_FUNCTION_1   None
845	POP_TOP           None

846	LOAD_FAST         'self'
849	LOAD_ATTR         '__stopFlyTask'
852	LOAD_FAST         'self'
855	LOAD_ATTR         'avId'
858	CALL_FUNCTION_1   None
861	POP_TOP           None

862	LOAD_FAST         'self'
865	LOAD_ATTR         'notify'
868	LOAD_ATTR         'debug'
871	LOAD_CONST        'stopping flying since we hit %s'
874	LOAD_FAST         'hitNode'
877	BINARY_MODULO     None
878	CALL_FUNCTION_1   None
881	POP_TOP           None

882	LOAD_FAST         'self'
885	LOAD_ATTR         'hitTarget'
888	LOAD_CONST        0
891	COMPARE_OP        '=='
894	JUMP_IF_FALSE     '913'

897	LOAD_GLOBAL       'messenger'
900	LOAD_ATTR         'send'
903	LOAD_CONST        'missedTarget'
906	CALL_FUNCTION_1   None
909	POP_TOP           None
910	JUMP_ABSOLUTE     '1180'
913	JUMP_FORWARD      '1180'

916	LOAD_FAST         'hitNode'
919	LOAD_CONST        'collision_house'
922	COMPARE_OP        '=='
925	JUMP_IF_FALSE     '950'

928	LOAD_FAST         'self'
931	LOAD_ATTR         '__hitHouse'
934	LOAD_FAST         'self'
937	LOAD_ATTR         'av'
940	LOAD_FAST         'collisionEntry'
943	CALL_FUNCTION_2   None
946	POP_TOP           None
947	JUMP_FORWARD      '1176'

950	LOAD_FAST         'hitNode'
953	LOAD_CONST        'collision_fence'
956	COMPARE_OP        '=='
959	JUMP_IF_FALSE     '984'

962	LOAD_FAST         'self'
965	LOAD_ATTR         '__hitFence'
968	LOAD_FAST         'self'
971	LOAD_ATTR         'av'
974	LOAD_FAST         'collisionEntry'
977	CALL_FUNCTION_2   None
980	POP_TOP           None
981	JUMP_FORWARD      '1176'

984	LOAD_FAST         'hitNode'
987	LOAD_CONST        'collision_roof'
990	COMPARE_OP        '=='
993	JUMP_IF_FALSE     '1018'

996	LOAD_FAST         'self'
999	LOAD_ATTR         '__hitRoof'
1002	LOAD_FAST         'self'
1005	LOAD_ATTR         'av'
1008	LOAD_FAST         'collisionEntry'
1011	CALL_FUNCTION_2   None
1014	POP_TOP           None
1015	JUMP_FORWARD      '1176'

1018	LOAD_FAST         'hitNode'
1021	LOAD_CONST        'targetSphere'
1024	COMPARE_OP        '=='
1027	JUMP_IF_FALSE     '1058'

1030	LOAD_FAST         'self'
1033	LOAD_ATTR         '__hitTarget'
1036	LOAD_FAST         'self'
1039	LOAD_ATTR         'av'
1042	LOAD_FAST         'collisionEntry'
1045	LOAD_FAST         'vel'
1048	BUILD_LIST_1      None
1051	CALL_FUNCTION_3   None
1054	POP_TOP           None
1055	JUMP_FORWARD      '1176'

1058	LOAD_FAST         'hitNode'
1061	LOAD_FAST         'cloudBumpers'
1064	COMPARE_OP        'in'
1067	JUMP_IF_FALSE     '1092'

1070	LOAD_FAST         'self'
1073	LOAD_ATTR         '__hitCloudPlatform'
1076	LOAD_FAST         'self'
1079	LOAD_ATTR         'av'
1082	LOAD_FAST         'collisionEntry'
1085	CALL_FUNCTION_2   None
1088	POP_TOP           None
1089	JUMP_FORWARD      '1176'

1092	LOAD_FAST         'hitNode'
1095	LOAD_CONST        'collision_cannon_bumper'
1098	COMPARE_OP        '=='
1101	JUMP_IF_FALSE     '1126'

1104	LOAD_FAST         'self'
1107	LOAD_ATTR         '__hitCannonBumper'
1110	LOAD_FAST         'self'
1113	LOAD_ATTR         'av'
1116	LOAD_FAST         'collisionEntry'
1119	CALL_FUNCTION_2   None
1122	POP_TOP           None
1123	JUMP_FORWARD      '1176'

1126	LOAD_FAST         'hitNode'
1129	LOAD_CONST        'statuaryCol'
1132	COMPARE_OP        '=='
1135	JUMP_IF_FALSE     '1160'

1138	LOAD_FAST         'self'
1141	LOAD_ATTR         '__hitStatuary'
1144	LOAD_FAST         'self'
1147	LOAD_ATTR         'av'
1150	LOAD_FAST         'collisionEntry'
1153	CALL_FUNCTION_2   None
1156	POP_TOP           None
1157	JUMP_FORWARD      '1176'

1160	LOAD_FAST         'self'
1163	LOAD_ATTR         'notify'
1166	LOAD_ATTR         'debug'
1169	LOAD_CONST        '*************** hit something else ************'
1172	CALL_FUNCTION_1   None
1175	POP_TOP           None
1176_0	COME_FROM         '947'
1176_1	COME_FROM         '981'
1176_2	COME_FROM         '1015'
1176_3	COME_FROM         '1055'
1176_4	COME_FROM         '1089'
1176_5	COME_FROM         '1123'
1176_6	COME_FROM         '1157'

1176	LOAD_CONST        None
1179	RETURN_VALUE      None
1180_0	COME_FROM         '913'

1180	LOAD_FAST         'self'
1183	LOAD_ATTR         'localToonShooting'
1186	JUMP_IF_FALSE     '1205'

1189	LOAD_GLOBAL       'camera'
1192	LOAD_ATTR         'wrtReparentTo'
1195	LOAD_GLOBAL       'render'
1198	CALL_FUNCTION_1   None
1201	POP_TOP           None
1202	JUMP_FORWARD      '1205'
1205_0	COME_FROM         '1202'

1205	LOAD_FAST         'self'
1208	LOAD_ATTR         'dropShadow'
1211	JUMP_IF_FALSE     '1233'

1214	LOAD_FAST         'self'
1217	LOAD_ATTR         'dropShadow'
1220	LOAD_ATTR         'reparentTo'
1223	LOAD_GLOBAL       'hidden'
1226	CALL_FUNCTION_1   None
1229	POP_TOP           None
1230	JUMP_FORWARD      '1233'
1233_0	COME_FROM         '1230'

1233	LOAD_FAST         'collisionEntry'
1236	LOAD_ATTR         'getSurfacePoint'
1239	LOAD_GLOBAL       'render'
1242	CALL_FUNCTION_1   None
1245	STORE_FAST        'pos'

1248	LOAD_FAST         'self'
1251	LOAD_ATTR         'av'
1254	LOAD_ATTR         'getHpr'
1257	CALL_FUNCTION_0   None
1260	STORE_FAST        'hpr'

1263	LOAD_FAST         'collisionEntry'
1266	LOAD_ATTR         'getSurfacePoint'
1269	LOAD_GLOBAL       'render'
1272	CALL_FUNCTION_1   None
1275	STORE_FAST        'hitPos'

1278	LOAD_FAST         'hitPos'
1281	STORE_FAST        'pos'

1284	LOAD_FAST         'pos'
1287	LOAD_FAST         'self'
1290	STORE_ATTR        'landingPos'

1293	LOAD_FAST         'self'
1296	LOAD_ATTR         'notify'
1299	LOAD_ATTR         'debug'
1302	LOAD_CONST        'hitNode,Normal = %s,%s'
1305	LOAD_FAST         'hitNode'
1308	LOAD_FAST         'intoNormal'
1311	BUILD_TUPLE_2     None
1314	BINARY_MODULO     None
1315	CALL_FUNCTION_1   None
1318	POP_TOP           None

1319	LOAD_GLOBAL       'Sequence'
1322	CALL_FUNCTION_0   None
1325	STORE_FAST        'track'

1328	LOAD_FAST         'track'
1331	LOAD_ATTR         'append'
1334	LOAD_GLOBAL       'Func'
1337	LOAD_FAST         'self'
1340	LOAD_ATTR         'av'
1343	LOAD_ATTR         'wrtReparentTo'
1346	LOAD_GLOBAL       'render'
1349	CALL_FUNCTION_2   None
1352	CALL_FUNCTION_1   None
1355	POP_TOP           None

1356	LOAD_FAST         'self'
1359	LOAD_ATTR         'localToonShooting'
1362	JUMP_IF_FALSE     '1393'

1365	LOAD_FAST         'track'
1368	LOAD_ATTR         'append'
1371	LOAD_GLOBAL       'Func'
1374	LOAD_FAST         'self'
1377	LOAD_ATTR         'av'
1380	LOAD_ATTR         'collisionsOff'
1383	CALL_FUNCTION_1   None
1386	CALL_FUNCTION_1   None
1389	POP_TOP           None
1390	JUMP_FORWARD      '1393'
1393_0	COME_FROM         '1390'

1393	LOAD_FAST         'hitPylonAboveWater'
1396	JUMP_IF_TRUE      '1435'
1399	LOAD_FAST         'hitNode'
1402	LOAD_CONST        'matCollisions'
1405	LOAD_CONST        'collision1'
1408	LOAD_CONST        'floor'
1411	LOAD_CONST        'sand_collision'
1414	LOAD_CONST        'dirt_collision'
1417	LOAD_CONST        'soil1'
1420	LOAD_CONST        'collision2'
1423	LOAD_CONST        'floor_collision'
1426	BUILD_LIST_8      None
1429	COMPARE_OP        'in'
1432_0	COME_FROM         '1396'
1432	JUMP_IF_FALSE     '1522'

1435	LOAD_FAST         'track'
1438	LOAD_ATTR         'append'
1441	LOAD_GLOBAL       'Func'
1444	LOAD_FAST         'self'
1447	LOAD_ATTR         '__hitGround'
1450	LOAD_FAST         'self'
1453	LOAD_ATTR         'av'
1456	LOAD_FAST         'pos'
1459	CALL_FUNCTION_3   None
1462	CALL_FUNCTION_1   None
1465	POP_TOP           None

1466	LOAD_FAST         'track'
1469	LOAD_ATTR         'append'
1472	LOAD_GLOBAL       'Wait'
1475	LOAD_CONST        1.0
1478	CALL_FUNCTION_1   None
1481	CALL_FUNCTION_1   None
1484	POP_TOP           None

1485	LOAD_FAST         'track'
1488	LOAD_ATTR         'append'
1491	LOAD_GLOBAL       'Func'
1494	LOAD_FAST         'self'
1497	LOAD_ATTR         '__setToonUpright'
1500	LOAD_FAST         'self'
1503	LOAD_ATTR         'av'
1506	LOAD_FAST         'self'
1509	LOAD_ATTR         'landingPos'
1512	CALL_FUNCTION_3   None
1515	CALL_FUNCTION_1   None
1518	POP_TOP           None
1519	JUMP_FORWARD      '2011'

1522	LOAD_FAST         'hitNode'
1525	LOAD_CONST        'collision_house'
1528	COMPARE_OP        '=='
1531	JUMP_IF_FALSE     '1568'

1534	LOAD_FAST         'track'
1537	LOAD_ATTR         'append'
1540	LOAD_GLOBAL       'Func'
1543	LOAD_FAST         'self'
1546	LOAD_ATTR         '__hitHouse'
1549	LOAD_FAST         'self'
1552	LOAD_ATTR         'av'
1555	LOAD_FAST         'collisionEntry'
1558	CALL_FUNCTION_3   None
1561	CALL_FUNCTION_1   None
1564	POP_TOP           None
1565	JUMP_FORWARD      '2011'

1568	LOAD_FAST         'hitNode'
1571	LOAD_CONST        'collision_fence'
1574	COMPARE_OP        '=='
1577	JUMP_IF_TRUE      '1592'
1580	LOAD_FAST         'hitNode'
1583	LOAD_CONST        'collision4'
1586	COMPARE_OP        '=='
1589_0	COME_FROM         '1577'
1589	JUMP_IF_FALSE     '1626'

1592	LOAD_FAST         'track'
1595	LOAD_ATTR         'append'
1598	LOAD_GLOBAL       'Func'
1601	LOAD_FAST         'self'
1604	LOAD_ATTR         '__hitFence'
1607	LOAD_FAST         'self'
1610	LOAD_ATTR         'av'
1613	LOAD_FAST         'collisionEntry'
1616	CALL_FUNCTION_3   None
1619	CALL_FUNCTION_1   None
1622	POP_TOP           None
1623	JUMP_FORWARD      '2011'

1626	LOAD_FAST         'hitNode'
1629	LOAD_CONST        'targetSphere'
1632	COMPARE_OP        '=='
1635	JUMP_IF_FALSE     '1672'

1638	LOAD_FAST         'track'
1641	LOAD_ATTR         'append'
1644	LOAD_GLOBAL       'Func'
1647	LOAD_FAST         'self'
1650	LOAD_ATTR         '__hitHouse'
1653	LOAD_FAST         'self'
1656	LOAD_ATTR         'av'
1659	LOAD_FAST         'collisionEntry'
1662	CALL_FUNCTION_3   None
1665	CALL_FUNCTION_1   None
1668	POP_TOP           None
1669	JUMP_FORWARD      '2011'

1672	LOAD_FAST         'hitNode'
1675	LOAD_CONST        'collision3'
1678	COMPARE_OP        '=='
1681	JUMP_IF_FALSE     '1774'

1684	LOAD_FAST         'track'
1687	LOAD_ATTR         'append'
1690	LOAD_GLOBAL       'Func'
1693	LOAD_FAST         'self'
1696	LOAD_ATTR         '__hitWater'
1699	LOAD_FAST         'self'
1702	LOAD_ATTR         'av'
1705	LOAD_FAST         'pos'
1708	LOAD_FAST         'collisionEntry'
1711	CALL_FUNCTION_4   None
1714	CALL_FUNCTION_1   None
1717	POP_TOP           None

1718	LOAD_FAST         'track'
1721	LOAD_ATTR         'append'
1724	LOAD_GLOBAL       'Wait'
1727	LOAD_CONST        2.0
1730	CALL_FUNCTION_1   None
1733	CALL_FUNCTION_1   None
1736	POP_TOP           None

1737	LOAD_FAST         'track'
1740	LOAD_ATTR         'append'
1743	LOAD_GLOBAL       'Func'
1746	LOAD_FAST         'self'
1749	LOAD_ATTR         '__setToonUpright'
1752	LOAD_FAST         'self'
1755	LOAD_ATTR         'av'
1758	LOAD_FAST         'self'
1761	LOAD_ATTR         'landingPos'
1764	CALL_FUNCTION_3   None
1767	CALL_FUNCTION_1   None
1770	POP_TOP           None
1771	JUMP_FORWARD      '2011'

1774	LOAD_FAST         'hitNode'
1777	LOAD_CONST        'roofOutside'
1780	COMPARE_OP        '=='
1783	JUMP_IF_TRUE      '1810'
1786	LOAD_FAST         'hitNode'
1789	LOAD_CONST        'collision_roof'
1792	COMPARE_OP        '=='
1795	JUMP_IF_TRUE      '1810'
1798	LOAD_FAST         'hitNode'
1801	LOAD_CONST        'roofclision'
1804	COMPARE_OP        '=='
1807_0	COME_FROM         '1783'
1807_1	COME_FROM         '1795'
1807	JUMP_IF_FALSE     '1897'

1810	LOAD_FAST         'track'
1813	LOAD_ATTR         'append'
1816	LOAD_GLOBAL       'Func'
1819	LOAD_FAST         'self'
1822	LOAD_ATTR         '__hitRoof'
1825	LOAD_FAST         'self'
1828	LOAD_ATTR         'av'
1831	LOAD_FAST         'collisionEntry'
1834	CALL_FUNCTION_3   None
1837	CALL_FUNCTION_1   None
1840	POP_TOP           None

1841	LOAD_FAST         'track'
1844	LOAD_ATTR         'append'
1847	LOAD_GLOBAL       'Wait'
1850	LOAD_CONST        2.0
1853	CALL_FUNCTION_1   None
1856	CALL_FUNCTION_1   None
1859	POP_TOP           None

1860	LOAD_FAST         'track'
1863	LOAD_ATTR         'append'
1866	LOAD_GLOBAL       'Func'
1869	LOAD_FAST         'self'
1872	LOAD_ATTR         '__setToonUpright'
1875	LOAD_FAST         'self'
1878	LOAD_ATTR         'av'
1881	LOAD_FAST         'self'
1884	LOAD_ATTR         'landingPos'
1887	CALL_FUNCTION_3   None
1890	CALL_FUNCTION_1   None
1893	POP_TOP           None
1894	JUMP_FORWARD      '2011'

1897	LOAD_FAST         'hitNode'
1900	LOAD_ATTR         'find'
1903	LOAD_CONST        'MovingPlatform'
1906	CALL_FUNCTION_1   None
1909	LOAD_CONST        0
1912	COMPARE_OP        '=='
1915	JUMP_IF_TRUE      '1939'
1918	LOAD_FAST         'hitNode'
1921	LOAD_ATTR         'find'
1924	LOAD_CONST        'cloudSphere'
1927	CALL_FUNCTION_1   None
1930	LOAD_CONST        0
1933	COMPARE_OP        '=='
1936_0	COME_FROM         '1915'
1936	JUMP_IF_FALSE     '1973'

1939	LOAD_FAST         'track'
1942	LOAD_ATTR         'append'
1945	LOAD_GLOBAL       'Func'
1948	LOAD_FAST         'self'
1951	LOAD_ATTR         '__hitCloudPlatform'
1954	LOAD_FAST         'self'
1957	LOAD_ATTR         'av'
1960	LOAD_FAST         'collisionEntry'
1963	CALL_FUNCTION_3   None
1966	CALL_FUNCTION_1   None
1969	POP_TOP           None
1970	JUMP_FORWARD      '2011'

1973	LOAD_FAST         'self'
1976	LOAD_ATTR         'notify'
1979	LOAD_ATTR         'warning'
1982	LOAD_CONST        '************* unhandled hitNode=%s parent =%s'
1985	LOAD_FAST         'hitNode'
1988	LOAD_FAST         'collisionEntry'
1991	LOAD_ATTR         'getIntoNodePath'
1994	CALL_FUNCTION_0   None
1997	LOAD_ATTR         'getParent'
2000	CALL_FUNCTION_0   None
2003	BUILD_TUPLE_2     None
2006	BINARY_MODULO     None
2007	CALL_FUNCTION_1   None
2010	POP_TOP           None
2011_0	COME_FROM         '1519'
2011_1	COME_FROM         '1565'
2011_2	COME_FROM         '1623'
2011_3	COME_FROM         '1669'
2011_4	COME_FROM         '1771'
2011_5	COME_FROM         '1894'
2011_6	COME_FROM         '1970'

2011	LOAD_FAST         'track'
2014	LOAD_ATTR         'append'
2017	LOAD_GLOBAL       'Func'
2020	LOAD_FAST         'self'
2023	LOAD_ATTR         'b_setLanded'
2026	CALL_FUNCTION_1   None
2029	CALL_FUNCTION_1   None
2032	POP_TOP           None

2033	LOAD_FAST         'self'
2036	LOAD_ATTR         'localToonShooting'
2039	JUMP_IF_FALSE     '2070'

2042	LOAD_FAST         'track'
2045	LOAD_ATTR         'append'
2048	LOAD_GLOBAL       'Func'
2051	LOAD_FAST         'self'
2054	LOAD_ATTR         'av'
2057	LOAD_ATTR         'collisionsOn'
2060	CALL_FUNCTION_1   None
2063	CALL_FUNCTION_1   None
2066	POP_TOP           None
2067	JUMP_FORWARD      '2070'
2070_0	COME_FROM         '2067'

2070	LOAD_FAST         'self'
2073	LOAD_ATTR         'hitTrack'
2076	JUMP_IF_FALSE     '2095'

2079	LOAD_FAST         'self'
2082	LOAD_ATTR         'hitTrack'
2085	LOAD_ATTR         'finish'
2088	CALL_FUNCTION_0   None
2091	POP_TOP           None
2092	JUMP_FORWARD      '2095'
2095_0	COME_FROM         '2092'

2095	LOAD_FAST         'track'
2098	LOAD_FAST         'self'
2101	STORE_ATTR        'hitTrack'

2104	LOAD_FAST         'self'
2107	LOAD_ATTR         'hitTrack'
2110	LOAD_ATTR         'start'
2113	CALL_FUNCTION_0   None
2116	POP_TOP           None
2117	JUMP_FORWARD      '2120'
2120_0	COME_FROM         '2117'
2120	LOAD_CONST        None
2123	RETURN_VALUE      None

Syntax error at or near `COME_FROM' token at offset 2120_0

    def __hitGround(self, avatar, pos, extraArgs = []):
        hitP = avatar.getPos(render)
        self.notify.debug('hitGround pos = %s, hitP = %s' % (pos, hitP))
        self.notify.debug('avatar hpr = %s' % avatar.getHpr())
        h = self.barrel.getH(render)
        avatar.setPos(pos[0], pos[1], pos[2] + avatar.getHeight() / 3.0)
        avatar.setHpr(h, -135, 0)
        self.notify.debug('parent = %s' % avatar.getParent())
        self.notify.debug('pos = %s, hpr = %s' % (avatar.getPos(render), avatar.getHpr(render)))
        self.dustCloud.setPos(render, pos[0], pos[1], pos[2] + avatar.getHeight() / 3.0)
        self.dustCloud.setScale(0.35)
        self.dustCloud.play()
        base.playSfx(self.sndHitGround)
        avatar.setPlayRate(2.0, 'run')
        avatar.loop('run')

    def __hitHouse(self, avatar, collisionEntry, extraArgs = []):
        self.__hitBumper(avatar, collisionEntry, self.sndHitHouse, kr=0.2, angVel=3)
        pinballScore = ToontownGlobals.PinballScoring[ToontownGlobals.PinballHouse]
        self.incrementPinballInfo(pinballScore[0], pinballScore[1])

    def __hitFence(self, avatar, collisionEntry, extraArgs = []):
        self.__hitBumper(avatar, collisionEntry, self.sndHitHouse, kr=0.2, angVel=3)
        pinballScore = ToontownGlobals.PinballScoring[ToontownGlobals.PinballFence]
        self.incrementPinballInfo(pinballScore[0], pinballScore[1])

    def __hitTarget(self, avatar, collisionEntry, extraArgs = []):
        self.__hitBumper(avatar, collisionEntry, self.sndHitHouse, kr=0.1, angVel=2)
        pinballScore = ToontownGlobals.PinballScoring[ToontownGlobals.PinballTarget]
        self.incrementPinballInfo(pinballScore[0], pinballScore[1])
        if self.localToonShooting:
            self.hitTarget = 1
            messenger.send('hitTarget', [self.avId, self.lastVel])

    def __hitBumper(self, avatar, collisionEntry, sound, kr = 0.6, angVel = 1):
        self.hitBumper = 1
        base.playSfx(self.sndHitHouse)
        hitP = avatar.getPos(render)
        self.lastPos = hitP
        house = collisionEntry.getIntoNodePath()
        normal = collisionEntry.getSurfaceNormal(house)
        normal.normalize()
        normal = collisionEntry.getSurfaceNormal(render)
        self.notify.debug('normal = %s' % normal)
        vel = self.vel * 1
        speed = vel.length()
        vel.normalize()
        self.notify.debug('old vel = %s' % vel)
        newVel = (normal * 2.0 + vel) * (kr * speed)
        self.lastVel = newVel
        self.notify.debug('new vel = %s' % newVel)
        self.angularVel = angVel * 360
        t = Sequence(Func(avatar.pose, 'lose', 110))
        t.start()

    def __hitRoof(self, avatar, collisionEntry, extraArgs = []):
        if True:
            self.__hitBumper(avatar, collisionEntry, self.sndHitHouse, kr=0.3, angVel=3)
            pinballScore = ToontownGlobals.PinballScoring[ToontownGlobals.PinballRoof]
            self.incrementPinballInfo(pinballScore[0], pinballScore[1])
            return
        np = collisionEntry.getIntoNodePath()
        roof = np.getParent()
        normal = collisionEntry.getSurfaceNormal(np)
        normal.normalize()
        vel = self.trajectory.getVel(self.t)
        vel.normalize()
        dot = normal.dot(vel)
        self.notify.debug('--------------dot product = %s---------------' % dot)
        temp = render.attachNewNode('temp')
        temp.iPosHpr()
        temp.lookAt(Point3(normal))
        temp.reparentTo(roof)
        self.notify.debug('avatar pos = %s, landingPos = %s' % (avatar.getPos(), self.landingPos))
        temp.setPos(render, self.landingPos)
        avatar.reparentTo(temp)
        avatar.setPosHpr(0, 0.25, 0.5, 0, 270, 180)
        avatar.pose('slip-forward', 25)
        base.playSfx(self.sndHitHouse)
        avatar.setPlayRate(1.0, 'jump')
        h = self.barrel.getH(render)
        t = Sequence(LerpPosInterval(avatar, 0.5, Point3(0, 0, -0.5), blendType='easeInOut'), Func(avatar.clearColorScale), Func(avatar.wrtReparentTo, render), Wait(0.3), Parallel(Func(avatar.setP, 0), Func(avatar.play, 'jump', None, 19, 39), LerpHprInterval(avatar, 0.3, Vec3(h, 0, 0), blendType='easeOut')), Func(avatar.play, 'neutral'))
        t.start()
        hitP = avatar.getPos(render)
        return

    def __hitBridge(self, avatar, collisionEntry, extraArgs = []):
        self.notify.debug('hit bridge')
        hitP = avatar.getPos(render)
        self.dustCloud.setPos(render, hitP[0], hitP[1], hitP[2] - 0.5)
        self.dustCloud.setScale(0.35)
        self.dustCloud.play()
        base.playSfx(self.sndHitGround)

    def __hitWater(self, avatar, pos, collisionEntry, extraArgs = []):
        hitP = avatar.getPos(render)
        if hitP[2] > ToontownGlobals.EstateWakeWaterHeight:
            self.notify.debug('we hit the ground before we hit water')
            self.__hitGround(avatar, pos, extraArgs)
            print 'but not really'
            return
        self.inWater = 1
        self.notify.debug('hit water')
        hitP = avatar.getPos(render)
        avatar.loop('neutral')
        self.splash.setPos(hitP)
        self.splash.setZ(ToontownGlobals.EstateWakeWaterHeight)
        self.splash.setScale(2)
        self.splash.play()
        base.playSfx(self.sndHitWater)
        place = base.cr.playGame.getPlace()
        self.notify.debug('hitWater: submerged = %s' % place.toonSubmerged)

    def __hitCannonBumper(self, avatar, collisionEntry, extraArgs = []):
        self.__hitBumper(avatar, collisionEntry, self.sndHitHouse, kr=0.4, angVel=5)
        score, multiplier = ToontownGlobals.PinballScoring[ToontownGlobals.PinballCannonBumper]
        self.incrementPinballInfo(score, multiplier)

    def __hitStatuary(self, avatar, collisionEntry, extraArgs = []):
        self.__hitBumper(avatar, collisionEntry, self.sndHitHouse, kr=0.4, angVel=5)
        score, multiplier = ToontownGlobals.PinballScoring[ToontownGlobals.PinballStatuary]
        intoNodePath = collisionEntry.getIntoNodePath()
        name = intoNodePath.getParent().getName()
        splitParts = name.split('-')
        if len(splitParts) >= 3:
            score = int(splitParts[1])
            multiplier = int(splitParts[2])
        self.incrementPinballInfo(score, multiplier)

    def __hitCloudPlatform(self, avatar, collisionEntry, extraArgs = []):
        if True:
            self.__hitBumper(avatar, collisionEntry, self.sndHitHouse, kr=0.4, angVel=5)
            score, multiplier = ToontownGlobals.PinballScoring[ToontownGlobals.PinballCloudBumperLow]
            intoNodePath = collisionEntry.getIntoNodePath()
            name = intoNodePath.getParent().getName()
            splitParts = name.split('-')
            if len(splitParts) >= 3:
                score = int(splitParts[1])
                multiplier = int(splitParts[2])
            self.incrementPinballInfo(score, multiplier)
            return
        avatar.reparentTo(collisionEntry.getIntoNodePath())
        h = self.barrel.getH(render)
        avatar.setPosHpr(0, 0, 0, h, 0, 0)
        messenger.send('hitCloud')

    def __setToonUpright(self, avatar, pos = None):
        if avatar:
            if self.inWater:
                avatar.setP(0)
                avatar.setR(0)
                return
            if not pos:
                pos = avatar.getPos(render)
            avatar.setPos(render, pos)
            avatar.loop('neutral')
            place = base.cr.playGame.getPlace()
            h = self.barrel.getH(render)
            p = Point3(self.vel[0], self.vel[1], self.vel[2])
            self.notify.debug('lookat = %s' % p)
            if hasattr(self, 'cannon') and self.cannon:
                avatar.lookAt(self.cannon)
            avatar.setP(0)
            avatar.setR(0)
            avatar.setScale(1, 1, 1)

    def __calcToonImpact(self, trajectory):
        t_groundImpact = trajectory.checkCollisionWithGround(GROUND_PLANE_MIN)
        if t_groundImpact >= trajectory.getStartTime():
            return (t_groundImpact, self.HIT_GROUND)
        else:
            self.notify.error('__calcToonImpact: toon never impacts ground?')
            return (0.0, self.HIT_GROUND)

    def __calcHitTreasures(self, trajectory):
        estate = self.cr.doId2do.get(self.estateId)
        self.hitTreasures = []
        if estate:
            doIds = estate.flyingTreasureId
            for id in doIds:
                t = self.cr.doId2do.get(id)
                if t:
                    pos = t.pos
                    rad = 10.5
                    height = 10.0
                    t_impact = trajectory.checkCollisionWithCylinderSides(pos, rad, height)
                    if t_impact > 0:
                        self.hitTreasures.append([t_impact, t])

        del estate
        return None

    def __shootTask(self, task):
        base.playSfx(self.sndCannonFire)
        self.dropShadow.reparentTo(render)
        return Task.done

    def __smokeTask(self, task):
        self.smoke.reparentTo(self.barrel)
        self.smoke.setPos(0, 6, -3)
        self.smoke.setScale(0.5)
        self.smoke.wrtReparentTo(render)
        track = Sequence(Parallel(LerpScaleInterval(self.smoke, 0.5, 3), LerpColorScaleInterval(self.smoke, 0.5, Vec4(2, 2, 2, 0))), Func(self.smoke.reparentTo, hidden), Func(self.smoke.clearColorScale))
        track.start()
        return Task.done

    def __flyTask(self, task):
        toon = task.info['toon']
        if toon.isEmpty():
            self.__resetToonToCannon(self.av)
            return Task.done
        curTime = task.time + task.info['launchTime']
        t = curTime
        self.lastT = self.t
        self.t = t
        deltaT = self.t - self.lastT
        self.deltaT = deltaT
        if self.hitBumper:
            pos = self.lastPos + self.lastVel * deltaT
            vel = self.lastVel
            self.lastVel += Vec3(0, 0, -32.0) * deltaT
            self.lastPos = pos
            toon.setFluidPos(pos)
            lastH = toon.getH()
            toon.setH(lastH + deltaT * self.angularVel)
            view = 0
        else:
            pos = task.info['trajectory'].getPos(t)
            toon.setFluidPos(pos)
            shadowPos = Point3(pos)
            shadowPos.setZ(SHADOW_Z_OFFSET)
            self.dropShadow.setPos(shadowPos)
            vel = task.info['trajectory'].getVel(t)
            run = math.sqrt(vel[0] * vel[0] + vel[1] * vel[1])
            rise = vel[2]
            theta = self.__toDegrees(math.atan(rise / run))
            toon.setHpr(self.cannon.getH(render), -90 + theta, 0)
            view = 2
        if pos.getZ() < -20 or pos.getZ() > 1000:
            self.notify.debug('stopping fly task toon.getZ()=%.2f' % pos.getZ())
            self.__resetToonToCannon(self.av)
            return Task.done
        lookAt = task.info['toon'].getPos(render)
        hpr = task.info['toon'].getHpr(render)
        if self.localToonShooting:
            if view == 0:
                camera.wrtReparentTo(render)
                camera.lookAt(lookAt)
            elif view == 1:
                camera.reparentTo(render)
                camera.setPos(render, 100, 100, 35.25)
                camera.lookAt(render, lookAt)
            elif view == 2:
                if hpr[1] > -90:
                    camera.setPos(0, 0, -30)
                    if camera.getZ() < lookAt[2]:
                        camera.setZ(render, lookAt[2] + 10)
                    camera.lookAt(Point3(0, 0, 0))
            self.__pickupTreasures(t)
        return Task.cont

    def __pickupTreasures(self, t):
        updatedList = []
        for tList in self.hitTreasures:
            if t > tList[0]:
                messenger.send(tList[1].uniqueName('entertreasureSphere'))
                self.notify.debug('hit something!')
            else:
                updatedList.append(tList)

        self.hitTreasures = updatedList

    def __resetToonToCannon(self, avatar):
        pos = None
        if not avatar:
            if self.avId:
                avatar = base.cr.doId2do.get(self.avId, None)
        if avatar:
            if self.cannon:
                avatar.reparentTo(self.cannon)
                avatar.setPos(2, -4, 0)
                avatar.wrtReparentTo(render)
            self.__resetToon(avatar)
        return

    def __resetToon(self, avatar, pos = None):
        self.notify.debug('__resetToon')
        if avatar:
            self.__stopCollisionHandler(avatar)
            self.__setToonUpright(avatar, pos)
            if self.localToonShooting:
                self.notify.debug('toon setting position to %s' % pos)
                if pos:
                    base.localAvatar.setPos(pos)
                camera.reparentTo(avatar)
            self.b_setLanded()

    def setActiveState(self, active):
        self.notify.debug('got setActiveState(%s)' % active)
        if active and not self.cannonsActive:
            self.activateCannons()
        elif not active and self.cannonsActive:
            self.deActivateCannons()

    def enterInit(self):
        self.nextKey = 'up'
        self.nextState = 'u1'

    def exitInit(self):
        pass

    def enteru1(self):
        self.nextKey = 'up'
        self.nextState = 'u2'

    def exitu1(self):
        pass

    def enteru2(self):
        self.nextKey = 'down'
        self.nextState = 'd3'

    def exitu2(self):
        pass

    def enterd3(self):
        self.nextKey = 'down'
        self.nextState = 'd4'

    def exitd3(self):
        pass

    def enterd4(self):
        self.nextKey = 'left'
        self.nextState = 'l5'

    def exitd4(self):
        pass

    def enterl5(self):
        self.nextKey = 'right'
        self.nextState = 'r6'

    def exitl5(self):
        pass

    def enterr6(self):
        self.nextKey = 'left'
        self.nextState = 'l7'

    def exitr6(self):
        pass

    def enterl7(self):
        self.nextKey = 'right'
        self.nextState = 'r8'

    def exitl7(self):
        pass

    def enterr8(self):
        self.nextKey = None
        self.nextState = ''
        self.codeFSM.request('acceptCode')
        return

    def exitr8(self):
        pass

    def enterAcceptCode(self):
        if not self.cannonsActive:
            self.activateCannons()
            self.sendUpdate('setActive', [1])
        else:
            self.deActivateCannons()
            self.sendUpdate('setActive', [0])
        self.codeFSM.request('init')

    def exitAcceptCode(self):
        pass

    def enterFinal(self):
        pass

    def exitFinal(self):
        pass

    def handleCodeKey(self, key):
        if self.nextKey and self.nextState:
            if key == self.nextKey:
                self.codeFSM.request(self.nextState)
            else:
                self.codeFSM.request('init')

    def incrementPinballInfo(self, score, multiplier):
        if base.localAvatar.doId == self.avId:
            self.curPinballScore += score
            self.curPinballMultiplier += multiplier
            self.notify.debug('score =%d multiplier=%d  curscore=%d curMult=%d' % (score,
             multiplier,
             self.curPinballScore,
             self.curPinballMultiplier))
            self.d_setPinballInfo()

    def d_setPinballInfo(self):
        self.notify.debug('d_setPinballInfo %d %d' % (self.curPinballScore, self.curPinballMultiplier))
        target = base.cr.doId2do[self.targetId]
        target.b_setCurPinballScore(self.avId, self.curPinballScore, self.curPinballMultiplier)

    def createBlock(self, collisionName = None):
        gFormat = GeomVertexFormat.getV3c4()
        myVertexData = GeomVertexData('Cannon bumper vertices', gFormat, Geom.UHDynamic)
        vertexWriter = GeomVertexWriter(myVertexData, 'vertex')
        colorWriter = GeomVertexWriter(myVertexData, 'color')
        vertices = [(-1, 1, 1),
         (1, 1, 1),
         (1, -1, 1),
         (-1, -1, 1),
         (-1, 1, -1),
         (1, 1, -1),
         (1, -1, -1),
         (-1, -1, -1)]
        colors = [(0, 0, 0, 1),
         (0, 0, 1, 1),
         (0, 1, 0, 1),
         (0, 1, 1, 1),
         (1, 0, 0, 1),
         (1, 0, 1, 1),
         (1, 1, 0, 1),
         (1, 1, 1, 1)]
        faces = [(0, 2, 1),
         (0, 3, 2),
         (7, 4, 5),
         (6, 7, 5),
         (2, 3, 7),
         (2, 7, 6),
         (4, 0, 1),
         (5, 4, 1),
         (0, 4, 3),
         (3, 4, 7),
         (1, 2, 6),
         (1, 6, 5)]
        quads = [(3, 2, 1, 0),
         (4, 5, 6, 7),
         (3, 7, 6, 2),
         (0, 1, 5, 4),
         (0, 4, 7, 3),
         (1, 2, 6, 
# Can't uncompyle C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\estate\DistributedCannon.pyc
Traceback (most recent call last):
  File "C:\python27\lib\uncompyle2\__init__.py", line 206, in main
    uncompyle_file(infile, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 143, in uncompyle_file
    uncompyle(version, co, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 132, in uncompyle
    raise walk.ERROR
ParserError: --- This code section failed: ---

0	LOAD_FAST         'self'
3	LOAD_ATTR         'av'
6	LOAD_CONST        None
9	COMPARE_OP        '=='
12	JUMP_IF_TRUE      '30'
15	LOAD_FAST         'self'
18	LOAD_ATTR         'flyColNode'
21	LOAD_CONST        None
24	COMPARE_OP        '=='
27_0	COME_FROM         '12'
27	JUMP_IF_FALSE     '37'

30	LOAD_CONST        None
33	RETURN_VALUE      None
34	JUMP_FORWARD      '37'
37_0	COME_FROM         '34'

37	LOAD_FAST         'collisionEntry'
40	LOAD_ATTR         'getIntoNode'
43	CALL_FUNCTION_0   None
46	LOAD_ATTR         'getName'
49	CALL_FUNCTION_0   None
52	STORE_FAST        'hitNode'

55	LOAD_FAST         'self'
58	LOAD_ATTR         'notify'
61	LOAD_ATTR         'debug'
64	LOAD_CONST        'hitNode = %s'
67	LOAD_FAST         'hitNode'
70	BINARY_MODULO     None
71	CALL_FUNCTION_1   None
74	POP_TOP           None

75	LOAD_FAST         'self'
78	LOAD_ATTR         'notify'
81	LOAD_ATTR         'debug'
84	LOAD_CONST        'hitNodePath.getParent = %s'
87	LOAD_FAST         'collisionEntry'
90	LOAD_ATTR         'getIntoNodePath'
93	CALL_FUNCTION_0   None
96	LOAD_ATTR         'getParent'
99	CALL_FUNCTION_0   None
102	BINARY_MODULO     None
103	CALL_FUNCTION_1   None
106	POP_TOP           None

107	LOAD_FAST         'self'
110	LOAD_ATTR         'trajectory'
113	LOAD_ATTR         'getVel'
116	LOAD_FAST         'self'
119	LOAD_ATTR         't'
122	CALL_FUNCTION_1   None
125	LOAD_FAST         'self'
128	STORE_ATTR        'vel'

131	LOAD_FAST         'self'
134	LOAD_ATTR         'trajectory'
137	LOAD_ATTR         'getVel'
140	LOAD_FAST         'self'
143	LOAD_ATTR         't'
146	CALL_FUNCTION_1   None
149	STORE_FAST        'vel'

152	LOAD_FAST         'vel'
155	LOAD_ATTR         'normalize'
158	CALL_FUNCTION_0   None
161	POP_TOP           None

162	LOAD_FAST         'self'
165	LOAD_ATTR         'hitBumper'
168	JUMP_IF_FALSE     '197'

171	LOAD_FAST         'self'
174	LOAD_ATTR         'lastVel'
177	LOAD_CONST        1
180	BINARY_MULTIPLY   None
181	STORE_FAST        'vel'

184	LOAD_FAST         'vel'
187	LOAD_ATTR         'normalize'
190	CALL_FUNCTION_0   None
193	POP_TOP           None
194	JUMP_FORWARD      '197'
197_0	COME_FROM         '194'

197	LOAD_FAST         'self'
200	LOAD_ATTR         'notify'
203	LOAD_ATTR         'debug'
206	LOAD_CONST        'normalized vel=%s'
209	LOAD_FAST         'vel'
212	BINARY_MODULO     None
213	CALL_FUNCTION_1   None
216	POP_TOP           None

217	LOAD_FAST         'collisionEntry'
220	LOAD_ATTR         'getInto'
223	CALL_FUNCTION_0   None
226	STORE_FAST        'solid'

229	LOAD_FAST         'collisionEntry'
232	LOAD_ATTR         'getSurfaceNormal'
235	LOAD_FAST         'collisionEntry'
238	LOAD_ATTR         'getIntoNodePath'
241	CALL_FUNCTION_0   None
244	CALL_FUNCTION_1   None
247	STORE_FAST        'intoNormal'

250	LOAD_FAST         'self'
253	LOAD_ATTR         'notify'
256	LOAD_ATTR         'debug'
259	LOAD_CONST        'old intoNormal = %s'
262	LOAD_FAST         'intoNormal'
265	BINARY_MODULO     None
266	CALL_FUNCTION_1   None
269	POP_TOP           None

270	LOAD_FAST         'collisionEntry'
273	LOAD_ATTR         'getSurfaceNormal'
276	LOAD_GLOBAL       'render'
279	CALL_FUNCTION_1   None
282	STORE_FAST        'intoNormal'

285	LOAD_FAST         'self'
288	LOAD_ATTR         'notify'
291	LOAD_ATTR         'debug'
294	LOAD_CONST        'new intoNormal = %s'
297	LOAD_FAST         'intoNormal'
300	BINARY_MODULO     None
301	CALL_FUNCTION_1   None
304	POP_TOP           None

305	LOAD_GLOBAL       'False'
308	STORE_FAST        'hitPylonAboveWater'

311	LOAD_GLOBAL       'False'
314	STORE_FAST        'hitPylonBelowWater'

317	LOAD_FAST         'hitNode'
320	LOAD_CONST        'pier_pylon_collisions_1'
323	LOAD_CONST        'pier_pylon_collisions_3'
326	BUILD_LIST_2      None
329	COMPARE_OP        'in'
332	JUMP_IF_FALSE     '410'

335	LOAD_FAST         'collisionEntry'
338	LOAD_ATTR         'getSurfacePoint'
341	LOAD_GLOBAL       'render'
344	CALL_FUNCTION_1   None
347	LOAD_CONST        2
350	BINARY_SUBSCR     None
351	LOAD_CONST        0
354	COMPARE_OP        '>'
357	JUMP_IF_FALSE     '385'

360	LOAD_GLOBAL       'True'
363	STORE_FAST        'hitPylonAboveWater'

366	LOAD_FAST         'self'
369	LOAD_ATTR         'notify'
372	LOAD_ATTR         'debug'
375	LOAD_CONST        'hitPylonAboveWater = True'
378	CALL_FUNCTION_1   None
381	POP_TOP           None
382	JUMP_ABSOLUTE     '410'

385	LOAD_GLOBAL       'True'
388	STORE_FAST        'hitPylonBelowWater'

391	LOAD_FAST         'self'
394	LOAD_ATTR         'notify'
397	LOAD_ATTR         'debug'
400	LOAD_CONST        'hitPylonBelowWater = True'
403	CALL_FUNCTION_1   None
406	POP_TOP           None
407	JUMP_FORWARD      '410'
410_0	COME_FROM         '407'

410	LOAD_FAST         'intoNormal'
413	STORE_FAST        'hitNormal'

416	LOAD_FAST         'hitNode'
419	LOAD_ATTR         'find'
422	LOAD_CONST        'cSphere'
425	CALL_FUNCTION_1   None
428	LOAD_CONST        0
431	COMPARE_OP        '=='
434	JUMP_IF_TRUE      '647'
437	LOAD_FAST         'hitNode'
440	LOAD_ATTR         'find'
443	LOAD_CONST        'treasureSphere'
446	CALL_FUNCTION_1   None
449	LOAD_CONST        0
452	COMPARE_OP        '=='
455	JUMP_IF_TRUE      '647'
458	LOAD_FAST         'hitNode'
461	LOAD_ATTR         'find'
464	LOAD_CONST        'prop'
467	CALL_FUNCTION_1   None
470	LOAD_CONST        0
473	COMPARE_OP        '=='
476	JUMP_IF_TRUE      '647'
479	LOAD_FAST         'hitNode'
482	LOAD_ATTR         'find'
485	LOAD_CONST        'distAvatarCollNode'
488	CALL_FUNCTION_1   None
491	LOAD_CONST        0
494	COMPARE_OP        '=='
497	JUMP_IF_TRUE      '647'
500	LOAD_FAST         'hitNode'
503	LOAD_ATTR         'find'
506	LOAD_CONST        'CannonSphere'
509	CALL_FUNCTION_1   None
512	LOAD_CONST        0
515	COMPARE_OP        '=='
518	JUMP_IF_TRUE      '647'
521	LOAD_FAST         'hitNode'
524	LOAD_ATTR         'find'
527	LOAD_CONST        'plotSphere'
530	CALL_FUNCTION_1   None
533	LOAD_CONST        0
536	COMPARE_OP        '=='
539	JUMP_IF_TRUE      '647'
542	LOAD_FAST         'hitNode'
545	LOAD_ATTR         'find'
548	LOAD_CONST        'flySphere'
551	CALL_FUNCTION_1   None
554	LOAD_CONST        0
557	COMPARE_OP        '=='
560	JUMP_IF_TRUE      '647'
563	LOAD_FAST         'hitNode'
566	LOAD_ATTR         'find'
569	LOAD_CONST        'mailboxSphere'
572	CALL_FUNCTION_1   None
575	LOAD_CONST        0
578	COMPARE_OP        '=='
581	JUMP_IF_TRUE      '647'
584	LOAD_FAST         'hitNode'
587	LOAD_ATTR         'find'
590	LOAD_CONST        'FishingSpotSphere'
593	CALL_FUNCTION_1   None
596	LOAD_CONST        0
599	COMPARE_OP        '=='
602	JUMP_IF_TRUE      '647'
605	LOAD_FAST         'hitNode'
608	LOAD_CONST        'gagtree_collision'
611	COMPARE_OP        '=='
614	JUMP_IF_TRUE      '647'
617	LOAD_FAST         'hitNode'
620	LOAD_CONST        'sign_collision'
623	COMPARE_OP        '=='
626	JUMP_IF_TRUE      '647'
629	LOAD_FAST         'hitNode'
632	LOAD_CONST        'FlowerSellBox'
635	COMPARE_OP        '=='
638	JUMP_IF_TRUE      '647'
641	LOAD_FAST         'hitPylonBelowWater'
644_0	COME_FROM         '434'
644_1	COME_FROM         '455'
644_2	COME_FROM         '476'
644_3	COME_FROM         '497'
644_4	COME_FROM         '518'
644_5	COME_FROM         '539'
644_6	COME_FROM         '560'
644_7	COME_FROM         '581'
644_8	COME_FROM         '602'
644_9	COME_FROM         '614'
644_10	COME_FROM         '626'
644_11	COME_FROM         '638'
644	JUMP_IF_FALSE     '674'

647	LOAD_FAST         'self'
650	LOAD_ATTR         'notify'
653	LOAD_ATTR         'debug'
656	LOAD_CONST        '--------------hit and ignoring %s'
659	LOAD_FAST         'hitNode'
662	BINARY_MODULO     None
663	CALL_FUNCTION_1   None
666	POP_TOP           None

667	LOAD_CONST        None
670	RETURN_VALUE      None
671	JUMP_FORWARD      '674'
674_0	COME_FROM         '671'

674	LOAD_FAST         'vel'
677	LOAD_ATTR         'dot'
680	LOAD_FAST         'hitNormal'
683	CALL_FUNCTION_1   None
686	LOAD_CONST        0
689	COMPARE_OP        '>'
692	JUMP_IF_FALSE     '763'
695	LOAD_FAST         'hitNode'
698	LOAD_CONST        'collision_roof'
701	COMPARE_OP        '=='
704	UNARY_NOT         None
705	JUMP_IF_FALSE     '763'
708	LOAD_FAST         'hitNode'
711	LOAD_CONST        'collision_fence'
714	COMPARE_OP        '=='
717	UNARY_NOT         None
718_0	COME_FROM         '692'
718_1	COME_FROM         '705'
718	JUMP_IF_FALSE     '763'

721	LOAD_FAST         'self'
724	LOAD_ATTR         'notify'
727	LOAD_ATTR         'debug'
730	LOAD_CONST        '--------------hit and ignoring backfacing %s, dot=%s'
733	LOAD_FAST         'hitNode'
736	LOAD_FAST         'vel'
739	LOAD_ATTR         'dot'
742	LOAD_FAST         'hitNormal'
745	CALL_FUNCTION_1   None
748	BUILD_TUPLE_2     None
751	BINARY_MODULO     None
752	CALL_FUNCTION_1   None
755	POP_TOP           None

756	LOAD_CONST        None
759	RETURN_VALUE      None
760	JUMP_FORWARD      '763'
763_0	COME_FROM         '760'

763	LOAD_FAST         'collisionEntry'
766	LOAD_ATTR         'getIntoNodePath'
769	CALL_FUNCTION_0   None
772	STORE_FAST        'intoNode'

775	LOAD_CONST        'collision_house'
778	LOAD_CONST        'collision_fence'
781	LOAD_CONST        'targetSphere'
784	LOAD_CONST        'collision_roof'
787	LOAD_CONST        'collision_cannon_bumper'
790	LOAD_CONST        'statuaryCol'
793	BUILD_LIST_6      None
796	STORE_FAST        'bumperNodes'

799	LOAD_CONST        'cloudSphere-0'
802	BUILD_LIST_1      None
805	STORE_FAST        'cloudBumpers'

808	LOAD_FAST         'bumperNodes'
811	LOAD_FAST         'cloudBumpers'
814	INPLACE_ADD       None
815	STORE_FAST        'bumperNodes'

818	LOAD_FAST         'hitNode'
821	LOAD_FAST         'bumperNodes'
824	COMPARE_OP        'not in'
827	JUMP_IF_FALSE     '916'

830	LOAD_FAST         'self'
833	LOAD_ATTR         '__stopCollisionHandler'
836	LOAD_FAST         'self'
839	LOAD_ATTR         'av'
842	CALL_FUNCTION_1   None
845	POP_TOP           None

846	LOAD_FAST         'self'
849	LOAD_ATTR         '__stopFlyTask'
852	LOAD_FAST         'self'
855	LOAD_ATTR         'avId'
858	CALL_FUNCTION_1   None
861	POP_TOP           None

862	LOAD_FAST         'self'
865	LOAD_ATTR         'notify'
868	LOAD_ATTR         'debug'
871	LOAD_CONST        'stopping flying since we hit %s'
874	LOAD_FAST         'hitNode'
877	BINARY_MODULO     None
878	CALL_FUNCTION_1   None
881	POP_TOP           None

882	LOAD_FAST         'self'
885	LOAD_ATTR         'hitTarget'
888	LOAD_CONST        0
891	COMPARE_OP        '=='
894	JUMP_IF_FALSE     '913'

897	LOAD_GLOBAL       'messenger'
900	LOAD_ATTR         'send'
903	LOAD_CONST        'missedTarget'
906	CALL_FUNCTION_1   None
909	POP_TOP           None
910	JUMP_ABSOLUTE     '1180'
913	JUMP_FORWARD      '1180'

916	LOAD_FAST         'hitNode'
919	LOAD_CONST        'collision_house'
922	COMPARE_OP        '=='
925	JUMP_IF_FALSE     '950'

928	LOAD_FAST         'self'
931	LOAD_ATTR         '__hitHouse'
934	LOAD_FAST         'self'
937	LOAD_ATTR         'av'
940	LOAD_FAST         'collisionEntry'
943	CALL_FUNCTION_2   None
946	POP_TOP           None
947	JUMP_FORWARD      '1176'

950	LOAD_FAST         'hitNode'
953	LOAD_CONST        'collision_fence'
956	COMPARE_OP        '=='
959	JUMP_IF_FALSE     '984'

962	LOAD_FAST         'self'
965	LOAD_ATTR         '__hitFence'
968	LOAD_FAST         'self'
971	LOAD_ATTR         'av'
974	LOAD_FAST         'collisionEntry'
977	CALL_FUNCTION_2   None
980	POP_TOP           None
981	JUMP_FORWARD      '1176'

984	LOAD_FAST         'hitNode'
987	LOAD_CONST        'collision_roof'
990	COMPARE_OP        '=='
993	JUMP_IF_FALSE     '1018'

996	LOAD_FAST         'self'
999	LOAD_ATTR         '__hitRoof'
1002	LOAD_FAST         'self'
1005	LOAD_ATTR         'av'
1008	LOAD_FAST         'collisionEntry'
1011	CALL_FUNCTION_2   None
1014	POP_TOP           None
1015	JUMP_FORWARD      '1176'

1018	LOAD_FAST         'hitNode'
1021	LOAD_CONST        'targetSphere'
1024	COMPARE_OP        '=='
1027	JUMP_IF_FALSE     '1058'

1030	LOAD_FAST         'self'
1033	LOAD_ATTR         '__hitTarget'
1036	LOAD_FAST         'self'
1039	LOAD_ATTR         'av'
1042	LOAD_FAST         'collisionEntry'
1045	LOAD_FAST         'vel'
1048	BUILD_LIST_1      None
1051	CALL_FUNCTION_3   None
1054	POP_TOP           None
1055	JUMP_FORWARD      '1176'

1058	LOAD_FAST         'hitNode'
1061	LOAD_FAST         'cloudBumpers'
1064	COMPARE_OP        'in'
1067	JUMP_IF_FALSE     '1092'

1070	LOAD_FAST         'self'
1073	LOAD_ATTR         '__hitCloudPlatform'
1076	LOAD_FAST         'self'
1079	LOAD_ATTR         'av'
1082	LOAD_FAST         'collisionEntry'
1085	CALL_FUNCTION_2   None
1088	POP_TOP           None
1089	JUMP_FORWARD      '1176'

1092	LOAD_FAST         'hitNode'
1095	LOAD_CONST        'collision_cannon_bumper'
1098	COMPARE_OP        '=='
1101	JUMP_IF_FALSE     '1126'

1104	LOAD_FAST         'self'
1107	LOAD_ATTR         '__hitCannonBumper'
1110	LOAD_FAST         'self'
1113	LOAD_ATTR         'av'
1116	LOAD_FAST         'collisionEntry'
1119	CALL_FUNCTION_2   None
1122	POP_TOP           None
1123	JUMP_FORWARD      '1176'

1126	LOAD_FAST         'hitNode'
1129	LOAD_CONST        'statuaryCol'
1132	COMPARE_OP        '=='
1135	JUMP_IF_FALSE     '1160'

1138	LOAD_FAST         'self'
1141	LOAD_ATTR         '__hitStatuary'
1144	LOAD_FAST         'self'
1147	LOAD_ATTR         'av'
1150	LOAD_FAST         'collisionEntry'
1153	CALL_FUNCTION_2   None
1156	POP_TOP           None
1157	JUMP_FORWARD      '1176'

1160	LOAD_FAST         'self'
1163	LOAD_ATTR         'notify'
1166	LOAD_ATTR         'debug'
1169	LOAD_CONST        '*************** hit something else ************'
1172	CALL_FUNCTION_1   None
1175	POP_TOP           None
1176_0	COME_FROM         '947'
1176_1	COME_FROM         '981'
1176_2	COME_FROM         '1015'
1176_3	COME_FROM         '1055'
1176_4	COME_FROM         '1089'
1176_5	COME_FROM         '1123'
1176_6	COME_FROM         '1157'

1176	LOAD_CONST        None
1179	RETURN_VALUE      None
1180_0	COME_FROM         '913'

1180	LOAD_FAST         'self'
1183	LOAD_ATTR         'localToonShooting'
1186	JUMP_IF_FALSE     '1205'

1189	LOAD_GLOBAL       'camera'
1192	LOAD_ATTR         'wrtReparentTo'
1195	LOAD_GLOBAL       'render'
1198	CALL_FUNCTION_1   None
1201	POP_TOP           None
1202	JUMP_FORWARD      '1205'
1205_0	COME_FROM         '1202'

1205	LOAD_FAST         'self'
1208	LOAD_ATTR         'dropShadow'
1211	JUMP_IF_FALSE     '1233'

1214	LOAD_FAST         'self'
1217	LOAD_ATTR         'dropShadow'
1220	LOAD_ATTR         'reparentTo'
1223	LOAD_GLOBAL       'hidden'
1226	CALL_FUNCTION_1   None
1229	POP_TOP           None
1230	JUMP_FORWARD      '1233'
1233_0	COME_FROM         '1230'

1233	LOAD_FAST         'collisionEntry'
1236	LOAD_ATTR         'getSurfacePoint'
1239	LOAD_GLOBAL       'render'
1242	CALL_FUNCTION_1   None
1245	STORE_FAST        'pos'

1248	LOAD_FAST         'self'
1251	LOAD_ATTR         'av'
1254	LOAD_ATTR         'getHpr'
1257	CALL_FUNCTION_0   None
1260	STORE_FAST        'hpr'

1263	LOAD_FAST         'collisionEntry'
1266	LOAD_ATTR         'getSurfacePoint'
1269	LOAD_GLOBAL       'render'
1272	CALL_FUNCTION_1   None
1275	STORE_FAST        'hitPos'

1278	LOAD_FAST         'hitPos'
1281	STORE_FAST        'pos'

1284	LOAD_FAST         'pos'
1287	LOAD_FAST         'self'
1290	STORE_ATTR        'landingPos'

1293	LOAD_FAST         'self'
1296	LOAD_ATTR         'notify'
1299	LOAD_ATTR         'debug'
1302	LOAD_CONST        'hitNode,Normal = %s,%s'
1305	LOAD_FAST         'hitNode'
1308	LOAD_FAST         'intoNormal'
1311	BUILD_TUPLE_2     None
1314	BINARY_MODULO     None
1315	CALL_FUNCTION_1   None
1318	POP_TOP           None

1319	LOAD_GLOBAL       'Sequence'
1322	CALL_FUNCTION_0   None
1325	STORE_FAST        'track'

1328	LOAD_FAST         'track'
1331	LOAD_ATTR         'append'
1334	LOAD_GLOBAL       'Func'
1337	LOAD_FAST         'self'
1340	LOAD_ATTR         'av'
1343	LOAD_ATTR         'wrtReparentTo'
1346	LOAD_GLOBAL       'render'
1349	CALL_FUNCTION_2   None
1352	CALL_FUNCTION_1   None
1355	POP_TOP           None

1356	LOAD_FAST         'self'
1359	LOAD_ATTR         'localToonShooting'
1362	JUMP_IF_FALSE     '1393'

1365	LOAD_FAST         'track'
1368	LOAD_ATTR         'append'
1371	LOAD_GLOBAL       'Func'
1374	LOAD_FAST         'self'
1377	LOAD_ATTR         'av'
1380	LOAD_ATTR         'collisionsOff'
1383	CALL_FUNCTION_1   None
1386	CALL_FUNCTION_1   None
1389	POP_TOP           None
1390	JUMP_FORWARD      '1393'
1393_0	COME_FROM         '1390'

1393	LOAD_FAST         'hitPylonAboveWater'
1396	JUMP_IF_TRUE      '1435'
1399	LOAD_FAST         'hitNode'
1402	LOAD_CONST        'matCollisions'
1405	LOAD_CONST        'collision1'
1408	LOAD_CONST        'floor'
1411	LOAD_CONST        'sand_collision'
1414	LOAD_CONST        'dirt_collision'
1417	LOAD_CONST        'soil1'
1420	LOAD_CONST        'collision2'
1423	LOAD_CONST        'floor_collision'
1426	BUILD_LIST_8      None
1429	COMPARE_OP        'in'
1432_0	COME_FROM         '1396'
1432	JUMP_IF_FALSE     '1522'

1435	LOAD_FAST         'track'
1438	LOAD_ATTR         'append'
1441	LOAD_GLOBAL       'Func'
1444	LOAD_FAST         'self'
1447	LOAD_ATTR         '__hitGround'
1450	LOAD_FAST         'self'
1453	LOAD_ATTR         'av'
1456	LOAD_FAST         'pos'
1459	CALL_FUNCTION_3   None
1462	CALL_FUNCTION_1   None
1465	POP_TOP           None

1466	LOAD_FAST         'track'
1469	LOAD_ATTR         'append'
1472	LOAD_GLOBAL       'Wait'
1475	LOAD_CONST        1.0
1478	CALL_FUNCTION_1   None
1481	CALL_FUNCTION_1   None
1484	POP_TOP           None

1485	LOAD_FAST         'track'
1488	LOAD_ATTR         'append'
1491	LOAD_GLOBAL       'Func'
1494	LOAD_FAST         'self'
1497	LOAD_ATTR         '__setToonUpright'
1500	LOAD_FAST         'self'
1503	LOAD_ATTR         'av'
1506	LOAD_FAST         'self'
1509	LOAD_ATTR         'landingPos'
1512	CALL_FUNCTION_3   None
1515	CALL_FUNCTION_1   None
1518	POP_TOP           None
1519	JUMP_FORWARD      '2011'

1522	LOAD_FAST         'hitNode'
1525	LOAD_CONST        'collision_house'
1528	COMPARE_OP        '=='
1531	JUMP_IF_FALSE     '1568'

1534	LOAD_FAST         'track'
1537	LOAD_ATTR         'append'
1540	LOAD_GLOBAL       'Func'
1543	LOAD_FAST         'self'
1546	LOAD_ATTR         '__hitHouse'
1549	LOAD_FAST         'self'
1552	LOAD_ATTR         'av'
1555	LOAD_FAST         'collisionEntry'
1558	CALL_FUNCTION_3   None
1561	CALL_FUNCTION_1   None
1564	POP_TOP           None
1565	JUMP_FORWARD      '2011'

1568	LOAD_FAST         'hitNode'
1571	LOAD_CONST        'collision_fence'
1574	COMPARE_OP        '=='
1577	JUMP_IF_TRUE      '1592'
1580	LOAD_FAST         'hitNode'
1583	LOAD_CONST        'collision4'
1586	COMPARE_OP        '=='
1589_0	COME_FROM         '1577'
1589	JUMP_IF_FALSE     '1626'

1592	LOAD_FAST         'track'
1595	LOAD_ATTR         'append'
1598	LOAD_GLOBAL       'Func'
1601	LOAD_FAST         'self'
1604	LOAD_ATTR         '__hitFence'
1607	LOAD_FAST         'self'
1610	LOAD_ATTR         'av'
1613	LOAD_FAST         'collisionEntry'
1616	CALL_FUNCTION_3   None
1619	CALL_FUNCTION_1   None
1622	POP_TOP           None
1623	JUMP_FORWARD      '2011'

1626	LOAD_FAST         'hitNode'
1629	LOAD_CONST        'targetSphere'
1632	COMPARE_OP        '=='
1635	JUMP_IF_FALSE     '1672'

1638	LOAD_FAST         'track'
1641	LOAD_ATTR         'append'
1644	LOAD_GLOBAL       'Func'
1647	LOAD_FAST         'self'
1650	LOAD_ATTR         '__hitHouse'
1653	LOAD_FAST         'self'
1656	LOAD_ATTR         'av'
1659	LOAD_FAST         'collisionEntry'
1662	CALL_FUNCTION_3   None
1665	CALL_FUNCTION_1   None
1668	POP_TOP           None
1669	JUMP_FORWARD      '2011'

1672	LOAD_FAST         'hitNode'
1675	LOAD_CONST        'collision3'
1678	COMPARE_OP        '=='
1681	JUMP_IF_FALSE     '1774'

1684	LOAD_FAST         'track'
1687	LOAD_ATTR         'append'
1690	LOAD_GLOBAL       'Func'
1693	LOAD_FAST         'self'
1696	LOAD_ATTR         '__hitWater'
1699	LOAD_FAST         'self'
1702	LOAD_ATTR         'av'
1705	LOAD_FAST         'pos'
1708	LOAD_FAST         'collisionEntry'
1711	CALL_FUNCTION_4   None
1714	CALL_FUNCTION_1   None
1717	POP_TOP           None

1718	LOAD_FAST         'track'
1721	LOAD_ATTR         'append'
1724	LOAD_GLOBAL       'Wait'
1727	LOAD_CONST        2.0
1730	CALL_FUNCTION_1   None
1733	CALL_FUNCTION_1   None
1736	POP_TOP           None

1737	LOAD_FAST         'track'
1740	LOAD_ATTR         'append'
1743	LOAD_GLOBAL       'Func'
1746	LOAD_FAST         'self'
1749	LOAD_ATTR         '__setToonUpright'
1752	LOAD_FAST         'self'
1755	LOAD_ATTR         'av'
1758	LOAD_FAST         'self'
1761	LOAD_ATTR         'landingPos'
1764	CALL_FUNCTION_3   None
1767	CALL_FUNCTION_1   None
1770	POP_TOP           None
1771	JUMP_FORWARD      '2011'

1774	LOAD_FAST         'hitNode'
1777	LOAD_CONST        'roofOutside'
1780	COMPARE_OP        '=='
1783	JUMP_IF_TRUE      '1810'
1786	LOAD_FAST         'hitNode'
1789	LOAD_CONST        'collision_roof'
1792	COMPARE_OP        '=='
1795	JUMP_IF_TRUE      '1810'
1798	LOAD_FAST         'hitNode'
1801	LOAD_CONST        'roofclision'
1804	COMPARE_OP        '=='
1807_0	COME_FROM         '1783'
1807_1	COME_FROM         '1795'
1807	JUMP_IF_FALSE     '1897'

1810	LOAD_FAST         'track'
1813	LOAD_ATTR         'append'
1816	LOAD_GLOBAL       'Func'
1819	LOAD_FAST         'self'
1822	LOAD_ATTR         '__hitRoof'
1825	LOAD_FAST         'self'
1828	LOAD_ATTR         'av'
1831	LOAD_FAST         'collisionEntry'
1834	CALL_FUNCTION_3   None
1837	CALL_FUNCTION_1   None
1840	POP_TOP           None

1841	LOAD_FAST         'track'
1844	LOAD_ATTR         'append'
1847	LOAD_GLOBAL       'Wait'
1850	LOAD_CONST        2.0
1853	CALL_FUNCTION_1   None
1856	CALL_FUNCTION_1   None
1859	POP_TOP           None

1860	LOAD_FAST         'track'
1863	LOAD_ATTR         'append'
1866	LOAD_GLOBAL       'Func'
1869	LOAD_FAST         'self'
1872	LOAD_ATTR         '__setToonUpright'
1875	LOAD_FAST         'self'
1878	LOAD_ATTR         'av'
1881	LOAD_FAST         'self'
1884	LOAD_ATTR         'landingPos'
1887	CALL_FUNCTION_3   None
1890	CALL_FUNCTION_1   None
1893	POP_TOP           None
1894	JUMP_FORWARD      '2011'

1897	LOAD_FAST         'hitNode'
1900	LOAD_ATTR         'find'
1903	LOAD_CONST        'MovingPlatform'
1906	CALL_FUNCTION_1   None
1909	LOAD_CONST        0
1912	COMPARE_OP        '=='
1915	JUMP_IF_TRUE      '1939'
1918	LOAD_FAST         'hitNode'
1921	LOAD_ATTR         'find'
1924	LOAD_CONST        'cloudSphere'
1927	CALL_FUNCTION_1   None
1930	LOAD_CONST        0
1933	COMPARE_OP        '=='
1936_0	COME_FROM         '1915'
1936	JUMP_IF_FALSE     '1973'

1939	LOAD_FAST         'track'
1942	LOAD_ATTR         'append'
1945	LOAD_GLOBAL       'Func'
1948	LOAD_FAST         'self'
1951	LOAD_ATTR         '__hitCloudPlatform'
1954	LOAD_FAST         'self'
1957	LOAD_ATTR         'av'
1960	LOAD_FAST         'collisionEntry'
1963	CALL_FUNCTION_3   None
1966	CALL_FUNCTION_1   None
1969	POP_TOP           None
1970	JUMP_FORWARD      '2011'

1973	LOAD_FAST         'self'
1976	LOAD_ATTR         'notify'
1979	LOAD_ATTR         'warning'
1982	LOAD_CONST        '************* unhandled hitNode=%s parent =%s'
1985	LOAD_FAST         'hitNode'
1988	LOAD_FAST         'collisionEntry'
1991	LOAD_ATTR         'getIntoNodePath'
1994	CALL_FUNCTION_0   None
1997	LOAD_ATTR         'getParent'
2000	CALL_FUNCTION_0   None
2003	BUILD_TUPLE_2     None
2006	BINARY_MODULO     None
2007	CALL_FUNCTION_1   None
2010	POP_TOP           None
2011_0	COME_FROM         '1519'
2011_1	COME_FROM         '1565'
2011_2	COME_FROM         '1623'
2011_3	COME_FROM         '1669'
2011_4	COME_FROM         '1771'
2011_5	COME_FROM         '1894'
2011_6	COME_FROM         '1970'

2011	LOAD_FAST         'track'
2014	LOAD_ATTR         'append'
2017	LOAD_GLOBAL       'Func'
2020	LOAD_FAST         'self'
2023	LOAD_ATTR         'b_setLanded'
2026	CALL_FUNCTION_1   None
2029	CALL_FUNCTION_1   None
2032	POP_TOP           None

2033	LOAD_FAST         'self'
2036	LOAD_ATTR         'localToonShooting'
2039	JUMP_IF_FALSE     '2070'

2042	LOAD_FAST         '5)]
        for i in range(len(vertices)):
            vertex = vertices[i]
            vertexWriter.addData3f(vertex[0], vertex[1], vertex[2])
            colorWriter.addData4f(*colors[i])

        cubeGeom = Geom(myVertexData)
        tris = GeomTriangles(Geom.UHDynamic)
        tris.makeIndexed()
        for face in faces:
            for vertex in face:
                tris.addVertex(vertex)

        tris.closePrimitive()
        cubeGeom.addPrimitive(tris)
        cubeGN = GeomNode('cubeGeom')
        cubeGN.addGeom(cubeGeom)
        if collisionName:
            colNode = CollisionNode(collisionName)
        else:
            colNode = CollisionNode('cubeCollision')
        for quad in quads:
            colQuad = CollisionPolygon(Point3(*vertices[quad[0]]), Point3(*vertices[quad[1]]), Point3(*vertices[quad[2]]), Point3(*vertices[quad[3]]))
            colQuad.setTangible(0)
            colNode.addSolid(colQuad)

        block = NodePath('cubeNodePath')
        block.attachNewNode(cubeGN)
        block.attachNewNode(colNode)
        return block

    def loadCannonBumper(self):
        self.cannonBumper = loader.loadModel('phase_5.5/models/estate/bumper_cloud')
        self.cannonBumper.reparentTo(self.nodePath)
        self.cannonBumper.setScale(4.0)
        self.cannonBumper.setColor(0.52, 0.8, 0.98, 1)
        colCube = self.cannonBumper.find('**/collision')
        colCube.setName('cloudSphere-0')
        self.bumperCol = colCube
        self.notify.debug('------------self.cannonBumper.setPos %.2f %.2f %.2f' % (ToontownGlobals.PinballCannonBumperInitialPos[0], ToontownGlobals.PinballCannonBumperInitialPos[1], ToontownGlobals.PinballCannonBumperInitialPos[2]))
        self.cannonBumper.setPos(*ToontownGlobals.PinballCannonBumperInitialPos)

    def __bumperKeyPressed(self):
        self.notify.debug('__bumperKeyPressed')
        self.__bumperPressed()

    def __bumperPressed(self):
        renderPos = base.localAvatar.getPos(render)
        if renderPos[2] > 15.0:
            if not self.localToonShooting:
                return
            self.ignore(self.BUMPER_KEY)
            self.ignore(self.BUMPER_KEY2)
            self.notify.debug('renderPos %s' % renderPos)
            cannonPos = base.localAvatar.getPos(self.nodePath)
            self.notify.debug('cannonPos %s' % cannonPos)
            self.setCannonBumperPos(cannonPos[0], cannonPos[1], cannonPos[2])
            self.requestBumperMove(cannonPos[0], cannonPos[1], cannonPos[2])

    def requestBumperMove(self, x, y, z):
        self.sendUpdate('requestBumperMove', [x, y, z])

    def setCannonBumperPos(self, x, y, z):
        self.notify.debug('------------setCannonBumperPos %f %f %f' % (x, y, z))
        self.cannonBumper.setPos(x, y, z)
        self.bumperCol.setCollideMask(BitMask32.allOff())
        taskMgr.doMethodLater(0.25, self.turnOnBumperCollision, self.uniqueName('BumperON'))

    def turnOnBumperCollision(self, whatever = 0):
        if self.bumperCol:
            self.bumperCol.setCollideMask(ToontownGlobals.WallBitmask)# decompiled 0 files: 0 okay, 1 failed, 0 verify failed
# 2013.08.22 22:20:03 Pacific Daylight Time
track'
2045	LOAD_ATTR         'append'
2048	LOAD_GLOBAL       'Func'
2051	LOAD_FAST         'self'
2054	LOAD_ATTR         'av'
2057	LOAD_ATTR         'collisionsOn'
2060	CALL_FUNCTION_1   None
2063	CALL_FUNCTION_1   None
2066	POP_TOP           None
2067	JUMP_FORWARD      '2070'
2070_0	COME_FROM         '2067'

2070	LOAD_FAST         'self'
2073	LOAD_ATTR         'hitTrack'
2076	JUMP_IF_FALSE     '2095'

2079	LOAD_FAST         'self'
2082	LOAD_ATTR         'hitTrack'
2085	LOAD_ATTR         'finish'
2088	CALL_FUNCTION_0   None
2091	POP_TOP           None
2092	JUMP_FORWARD      '2095'
2095_0	COME_FROM         '2092'

2095	LOAD_FAST         'track'
2098	LOAD_FAST         'self'
2101	STORE_ATTR        'hitTrack'

2104	LOAD_FAST         'self'
2107	LOAD_ATTR         'hitTrack'
2110	LOAD_ATTR         'start'
2113	CALL_FUNCTION_0   None
2116	POP_TOP           None
2117	JUMP_FORWARD      '2120'
2120_0	COME_FROM         '2117'
2120	LOAD_CONST        None
2123	RETURN_VALUE      None

Syntax error at or near `COME_FROM' token at offset 2120_0

