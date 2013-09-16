# 2013.08.22 22:13:46 Pacific Daylight Time
# Embedded file name: direct.controls.GravityWalker
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.showbase import DirectObject
from direct.controls.ControlManager import CollisionHandlerRayStart
from direct.showbase.InputStateGlobal import inputState
from direct.task.Task import Task
from pandac.PandaModules import *
import math

class GravityWalker(DirectObject.DirectObject):
    __module__ = __name__
    notify = directNotify.newCategory('GravityWalker')
    wantDebugIndicator = base.config.GetBool('want-avatar-physics-indicator', 0)
    wantFloorSphere = base.config.GetBool('want-floor-sphere', 0)
    earlyEventSphere = base.config.GetBool('early-event-sphere', 0)
    DiagonalFactor = math.sqrt(2.0) / 2.0

    def __init__(self, gravity = 64.348, standableGround = 0.707, hardLandingForce = 16.0, legacyLifter = False):
        DirectObject.DirectObject.__init__(self)
        self.__gravity = gravity
        self.__standableGround = standableGround
        self.__hardLandingForce = hardLandingForce
        self._legacyLifter = legacyLifter
        self.mayJump = 1
        self.jumpDelayTask = None
        self.controlsTask = None
        self.indicatorTask = None
        self.falling = 0
        self.needToDeltaPos = 0
        self.physVelocityIndicator = None
        self.avatarControlForwardSpeed = 0
        self.avatarControlJumpForce = 0
        self.avatarControlReverseSpeed = 0
        self.avatarControlRotateSpeed = 0
        self.getAirborneHeight = None
        self.priorParent = Vec3(0)
        self.__oldPosDelta = Vec3(0)
        self.__oldDt = 0
        self.moving = 0
        self.speed = 0.0
        self.rotationSpeed = 0.0
        self.slideSpeed = 0.0
        self.vel = Vec3(0.0)
        self.collisionsActive = 0
        self.isAirborne = 0
        self.highMark = 0
        return

    def setWalkSpeed(self, forward, jump, reverse, rotate):
        self.avatarControlForwardSpeed = forward
        self.avatarControlJumpForce = jump
        self.avatarControlReverseSpeed = reverse
        self.avatarControlRotateSpeed = rotate

    def getSpeeds(self):
        return (self.speed, self.rotationSpeed, self.slideSpeed)

    def getIsAirborne(self):
        return self.isAirborne

    def setAvatar(self, avatar):
        self.avatar = avatar
        if avatar is not None:
            pass
        return

    def setupRay(self, bitmask, floorOffset, reach):
        cRay = CollisionRay(0.0, 0.0, CollisionHandlerRayStart, 0.0, 0.0, -1.0)
        cRayNode = CollisionNode('GW.cRayNode')
        cRayNode.addSolid(cRay)
        self.cRayNodePath = self.avatarNodePath.attachNewNode(cRayNode)
        cRayNode.setFromCollideMask(bitmask)
        cRayNode.setIntoCollideMask(BitMask32.allOff())
        self.lifter = CollisionHandlerGravity()
        self.lifter.setLegacyMode(self._legacyLifter)
        self.lifter.setGravity(self.__gravity)
        self.lifter.addInPattern('enter%in')
        self.lifter.addAgainPattern('again%in')
        self.lifter.addOutPattern('exit%in')
        self.lifter.setOffset(floorOffset)
        self.lifter.setReach(reach)
        self.lifter.addCollider(self.cRayNodePath, self.avatarNodePath)

    def setupWallSphere(self, bitmask, avatarRadius):
        self.avatarRadius = avatarRadius
        cSphere = CollisionSphere(0.0, 0.0, avatarRadius, avatarRadius)
        cSphereNode = CollisionNode('GW.cWallSphereNode')
        cSphereNode.addSolid(cSphere)
        cSphereNodePath = self.avatarNodePath.attachNewNode(cSphereNode)
        cSphereNode.setFromCollideMask(bitmask)
        cSphereNode.setIntoCollideMask(BitMask32.allOff())
        if config.GetBool('want-fluid-pusher', 0):
            self.pusher = CollisionHandlerFluidPusher()
        else:
            self.pusher = CollisionHandlerPusher()
        self.pusher.addCollider(cSphereNodePath, self.avatarNodePath)
        self.cWallSphereNodePath = cSphereNodePath

    def setupEventSphere(self, bitmask, avatarRadius):
        self.avatarRadius = avatarRadius
        cSphere = CollisionSphere(0.0, 0.0, avatarRadius - 0.1, avatarRadius * 1.04)
        cSphere.setTangible(0)
        cSphereNode = CollisionNode('GW.cEventSphereNode')
        cSphereNode.addSolid(cSphere)
        cSphereNodePath = self.avatarNodePath.attachNewNode(cSphereNode)
        cSphereNode.setFromCollideMask(bitmask)
        cSphereNode.setIntoCollideMask(BitMask32.allOff())
        self.event = CollisionHandlerEvent()
        self.event.addInPattern('enter%in')
        self.event.addOutPattern('exit%in')
        self.cEventSphereNodePath = cSphereNodePath

    def setupFloorSphere(self, bitmask, avatarRadius):
        self.avatarRadius = avatarRadius
        cSphere = CollisionSphere(0.0, 0.0, avatarRadius, 0.01)
        cSphereNode = CollisionNode('GW.cFloorSphereNode')
        cSphereNode.addSolid(cSphere)
        cSphereNodePath = self.avatarNodePath.attachNewNode(cSphereNode)
        cSphereNode.setFromCollideMask(bitmask)
        cSphereNode.setIntoCollideMask(BitMask32.allOff())
        self.pusherFloorhandler = CollisionHandlerPusher()
        self.pusherFloor.addCollider(cSphereNodePath, self.avatarNodePath)
        self.cFloorSphereNodePath = cSphereNodePath

    def setWallBitMask(self, bitMask):
        self.wallBitmask = bitMask

    def setFloorBitMask(self, bitMask):
        self.floorBitmask = bitMask

    def swapFloorBitMask(self, oldMask, newMask):
        self.floorBitmask = self.floorBitmask & ~oldMask
        self.floorBitmask |= newMask
        if self.cRayNodePath and not self.cRayNodePath.isEmpty():
            self.cRayNodePath.node().setFromCollideMask(self.floorBitmask)

    def setGravity(self, gravity):
        self.__gravity = gravity
        self.lifter.setGravity(self.__gravity)

    def getGravity(self, gravity):
        return self.__gravity

    def initializeCollisions(self, collisionTraverser, avatarNodePath, avatarRadius = 1.4, floorOffset = 1.0, reach = 1.0):
        self.avatarNodePath = avatarNodePath
        self.cTrav = collisionTraverser
        self.setupRay(self.floorBitmask, floorOffset, reach)
        self.setupWallSphere(self.wallBitmask, avatarRadius)
        self.setupEventSphere(self.wallBitmask, avatarRadius)
        if self.wantFloorSphere:
            self.setupFloorSphere(self.floorBitmask, avatarRadius)
        self.setCollisionsActive(1)

    def setTag(self, key, value):
        self.cEventSphereNodePath.setTag(key, value)

    def setAirborneHeightFunc(self, unused_parameter):
        self.getAirborneHeight = self.lifter.getAirborneHeight

    def getAirborneHeight(self):
        self.lifter.getAirborneHeight()

    def setAvatarPhysicsIndicator(self, indicator):
        self.cWallSphereNodePath.show()

    def deleteCollisions(self):
        del self.cTrav
        self.cWallSphereNodePath.removeNode()
        del self.cWallSphereNodePath
        if self.wantFloorSphere:
            self.cFloorSphereNodePath.removeNode()
            del self.cFloorSphereNodePath
        del self.pusher
        del self.event
        del self.lifter
        del self.getAirborneHeight

    def setCollisionsActive--- This code section failed: ---

0	LOAD_FAST         'self'
3	LOAD_ATTR         'collisionsActive'
6	LOAD_FAST         'active'
9	COMPARE_OP        '!='
12	JUMP_IF_FALSE     '365'

15	LOAD_FAST         'active'
18	LOAD_FAST         'self'
21	STORE_ATTR        'collisionsActive'

24	LOAD_FAST         'self'
27	LOAD_ATTR         'oneTimeCollide'
30	CALL_FUNCTION_0   None
33	POP_TOP           None

34	LOAD_GLOBAL       'base'
37	LOAD_ATTR         'initShadowTrav'
40	CALL_FUNCTION_0   None
43	POP_TOP           None

44	LOAD_FAST         'active'
47	JUMP_IF_FALSE     '237'

50	LOAD_FAST         'self'
53	LOAD_ATTR         'avatarNodePath'
56	LOAD_ATTR         'setP'
59	LOAD_CONST        0.0
62	CALL_FUNCTION_1   None
65	POP_TOP           None

66	LOAD_FAST         'self'
69	LOAD_ATTR         'avatarNodePath'
72	LOAD_ATTR         'setR'
75	LOAD_CONST        0.0
78	CALL_FUNCTION_1   None
81	POP_TOP           None
82	JUMP_FORWARD      '85'
85_0	COME_FROM         '82'

85	LOAD_FAST         'self'
88	LOAD_ATTR         'cTrav'
91	LOAD_ATTR         'addCollider'
94	LOAD_FAST         'self'
97	LOAD_ATTR         'cWallSphereNodePath'
100	LOAD_FAST         'self'
103	LOAD_ATTR         'pusher'
106	CALL_FUNCTION_2   None
109	POP_TOP           None

110	LOAD_FAST         'self'
113	LOAD_ATTR         'wantFloorSphere'
116	JUMP_IF_FALSE     '147'

119	LOAD_FAST         'self'
122	LOAD_ATTR         'cTrav'
125	LOAD_ATTR         'addCollider'
128	LOAD_FAST         'self'
131	LOAD_ATTR         'cFloorSphereNodePath'
134	LOAD_FAST         'self'
137	LOAD_ATTR         'pusherFloor'
140	CALL_FUNCTION_2   None
143	POP_TOP           None
144	JUMP_FORWARD      '147'
147_0	COME_FROM         '144'

147	LOAD_GLOBAL       'base'
150	LOAD_ATTR         'shadowTrav'
153	LOAD_ATTR         'addCollider'
156	LOAD_FAST         'self'
159	LOAD_ATTR         'cRayNodePath'
162	LOAD_FAST         'self'
165	LOAD_ATTR         'lifter'
168	CALL_FUNCTION_2   None
171	POP_TOP           None

172	LOAD_FAST         'self'
175	LOAD_ATTR         'earlyEventSphere'
178	JUMP_IF_FALSE     '209'

181	LOAD_FAST         'self'
184	LOAD_ATTR         'cTrav'
187	LOAD_ATTR         'addCollider'
190	LOAD_FAST         'self'
193	LOAD_ATTR         'cEventSphereNodePath'
196	LOAD_FAST         'self'
199	LOAD_ATTR         'event'
202	CALL_FUNCTION_2   None
205	POP_TOP           None
206	JUMP_ABSOLUTE     '362'

209	LOAD_GLOBAL       'base'
212	LOAD_ATTR         'shadowTrav'
215	LOAD_ATTR         'addCollider'
218	LOAD_FAST         'self'
221	LOAD_ATTR         'cEventSphereNodePath'
224	LOAD_FAST         'self'
227	LOAD_ATTR         'event'
230	CALL_FUNCTION_2   None
233	POP_TOP           None
234	JUMP_ABSOLUTE     '365'

237	LOAD_GLOBAL       'hasattr'
240	LOAD_FAST         'self'
243	LOAD_CONST        'cTrav'
246	CALL_FUNCTION_2   None
249	JUMP_IF_FALSE     '324'

252	LOAD_FAST         'self'
255	LOAD_ATTR         'cTrav'
258	LOAD_ATTR         'removeCollider'
261	LOAD_FAST         'self'
264	LOAD_ATTR         'cWallSphereNodePath'
267	CALL_FUNCTION_1   None
270	POP_TOP           None

271	LOAD_FAST         'self'
274	LOAD_ATTR         'wantFloorSphere'
277	JUMP_IF_FALSE     '302'

280	LOAD_FAST         'self'
283	LOAD_ATTR         'cTrav'
286	LOAD_ATTR         'removeCollider'
289	LOAD_FAST         'self'
292	LOAD_ATTR         'cFloorSphereNodePath'
295	CALL_FUNCTION_1   None
298	POP_TOP           None
299	JUMP_FORWARD      '302'
302_0	COME_FROM         '299'

302	LOAD_FAST         'self'
305	LOAD_ATTR         'cTrav'
308	LOAD_ATTR         'removeCollider'
311	LOAD_FAST         'self'
314	LOAD_ATTR         'cEventSphereNodePath'
317	CALL_FUNCTION_1   None
320	POP_TOP           None
321	JUMP_FORWARD      '324'
324_0	COME_FROM         '321'

324	LOAD_GLOBAL       'base'
327	LOAD_ATTR         'shadowTrav'
330	LOAD_ATTR         'removeCollider'
333	LOAD_FAST         'self'
336	LOAD_ATTR         'cEventSphereNodePath'
339	CALL_FUNCTION_1   None
342	POP_TOP           None

343	LOAD_GLOBAL       'base'
346	LOAD_ATTR         'shadowTrav'
349	LOAD_ATTR         'removeCollider'
352	LOAD_FAST         'self'
355	LOAD_ATTR         'cRayNodePath'
358	CALL_FUNCTION_1   None
361	POP_TOP           None
362	JUMP_FORWARD      '365'
365_0	COME_FROM         '362'

Syntax error at or near `LOAD_GLOBAL' token at offset 237

    def getCollisionsActive(self):
        return self.collisionsActive

    def placeOnFloor(self):
        self.oneTimeCollide()
        self.avatarNodePath.setZ(self.avatarNodePath.getZ() - self.lifter.getAirborneHeight())

    def oneTimeCollide(self):
        if not hasattr(self, 'cWallSphereNodePath'):
            return
        self.isAirborne = 0
        self.mayJump = 1
        tempCTrav = CollisionTraverser('oneTimeCollide')
        tempCTrav.addCollider(self.cWallSphereNodePath, self.pusher)
        if self.wantFloorSphere:
            tempCTrav.addCollider(self.cFloorSphereNodePath, self.event)
        tempCTrav.addCollider(self.cRayNodePath, self.lifter)
        tempCTrav.traverse(render)

    def setMayJump(self, task):
        self.mayJump = 1
        return Task.done

    def startJumpDelay(self, delay):
        if self.jumpDelayTask:
            self.jumpDelayTask.remove()
        self.mayJump = 0
        self.jumpDelayTask = taskMgr.doMethodLater(delay, self.setMayJump, 'jumpDelay-%s' % id(self))

    def addBlastForce(self, vector):
        self.lifter.addVelocity(vector.length())

    def displayDebugInfo(self):
        onScreenDebug.add('w controls', 'GravityWalker')
        onScreenDebug.add('w airborneHeight', self.lifter.getAirborneHeight())
        onScreenDebug.add('w falling', self.falling)
        onScreenDebug.add('w isOnGround', self.lifter.isOnGround())
        onScreenDebug.add('w contact normal', self.lifter.getContactNormal().pPrintValues())
        onScreenDebug.add('w mayJump', self.mayJump)
        onScreenDebug.add('w impact', self.lifter.getImpactVelocity())
        onScreenDebug.add('w velocity', self.lifter.getVelocity())
        onScreenDebug.add('w isAirborne', self.isAirborne)
        onScreenDebug.add('w hasContact', self.lifter.hasContact())

    def handleAvatarControls(self, task):
        run = inputState.isSet('run')
        forward = inputState.isSet('forward')
        reverse = inputState.isSet('reverse')
        turnLeft = inputState.isSet('turnLeft')
        turnRight = inputState.isSet('turnRight')
        slideLeft = inputState.isSet('slideLeft')
        slideRight = inputState.isSet('slideRight')
        jump = inputState.isSet('jump')
        if 'localAvatar' in __builtins__:
            if base.localAvatar and base.localAvatar.getAutoRun():
                forward = 1
                reverse = 0
        if not (forward and self.avatarControlForwardSpeed):
            if reverse:
                self.speed = -self.avatarControlReverseSpeed
                if not (reverse and slideLeft and -self.avatarControlReverseSpeed * 0.75):
                    if not (reverse and slideRight and self.avatarControlReverseSpeed * 0.75):
                        if not (slideLeft and -self.avatarControlForwardSpeed * 0.75):
                            if slideRight:
                                self.slideSpeed = self.avatarControlForwardSpeed * 0.75
                                if not slideLeft:
                                    if not slideRight:
                                        if not (turnLeft and self.avatarControlRotateSpeed):
                                            if turnRight:
                                                self.rotationSpeed = -self.avatarControlRotateSpeed
                                                self.speed and self.slideSpeed and self.speed *= GravityWalker.DiagonalFactor
                                                self.slideSpeed *= GravityWalker.DiagonalFactor
                                            debugRunning = inputState.isSet('debugRunning')
                                            debugRunning and self.speed *= base.debugRunningMultiplier
                                            self.slideSpeed *= base.debugRunningMultiplier
                                            self.rotationSpeed *= 1.25
                                        self.needToDeltaPos and self.setPriorParentVector()
                                        self.needToDeltaPos = 0
                                    self.wantDebugIndicator and self.displayDebugInfo()
                                if self.lifter.isOnGround():
                                    if self.isAirborne:
                                        self.isAirborne = 0
                                        impact = self.lifter.getImpactVelocity()
                                        if impact < -30.0:
                                            messenger.send('jumpHardLand')
                                            self.startJumpDelay(0.3)
                                        else:
                                            messenger.send('jumpLand')
                                            if impact < -5.0:
                                                self.startJumpDelay(0.2)
                                    self.priorParent = Vec3.zero()
                                    if jump and self.mayJump:
                                        self.lifter.addVelocity(self.avatarControlJumpForce)
                                        messenger.send('jumpStart')
                                        self.isAirborne = 1
                                else:
                                    if self.isAirborne == 0:
                                        pass
                                    self.isAirborne = 1
                                self.__oldPosDelta = self.avatarNodePath.getPosDelta(render)
                                self.__oldDt = ClockObject.getGlobalClock().getDt()
                                dt = self.__oldDt
                                self.moving = self.speed or self.slideSpeed or self.rotationSpeed or self.priorParent != Vec3.zero()
                                distance = self.moving and dt * self.speed
                                slideDistance = dt * self.slideSpeed
                                rotation = dt * self.rotationSpeed
                                rotMat = (distance or slideDistance or self.priorParent != Vec3.zero()) and Mat3.rotateMatNormaxis(self.avatarNodePath.getH(), Vec3.up())
                                forward = self.isAirborne and Vec3.forward()
                            else:
                                contact = self.lifter.getContactNormal()
                                forward = contact.cross(Vec3.right())
                                forward.normalize()
                            self.vel = Vec3(forward * distance)
                            right = slideDistance and self.isAirborne and Vec3.right()
                        else:
                            right = forward.cross(contact)
                            right.normalize()
                        self.vel = Vec3(self.vel + right * slideDistance)
                    self.vel = Vec3(rotMat.xform(self.vel))
                    step = self.vel + self.priorParent * dt
                    self.avatarNodePath.setFluidPos(Point3(self.avatarNodePath.getPos() + step))
                self.avatarNodePath.setH(self.avatarNodePath.getH() + rotation)
            else:
                self.vel.set(0.0, 0.0, 0.0)
            (self.moving or jump) and messenger.send('avatarMoving')
        return Task.cont

    def doDeltaPos(self):
        self.needToDeltaPos = 1

    def setPriorParentVector(self):
        if self.__oldDt == 0:
            velocity = 0
        else:
            velocity = self.__oldPosDelta * (1.0 / self.__oldDt)
        self.priorParent = Vec3(velocity)

    def reset(self):
        self.lifter.setVelocity(0.0)
        self.priorParent = Vec3.zero()

    def getVelocity(self):
        return self.vel

    def enableAvatarControls(self):
        if self.controlsTask:
            self.controlsTask.remove()
        taskName = 'AvatarControls-%s' % (id(self),)
        self.controlsTask = taskMgr.add(self.handleAvatarControls, taskName, 25)
        self.isAirborne = 0
        self.mayJump = 1
        if self.physVelocityIndicator:
            if self.indicatorTask:
                self.indicatorTask.remove()
            self.indicatorTask = taskMgr.add(self.avatarPhysicsIndicator, 'AvatarControlsIndicator-%s' % (id(self),), 35)

    def disableAvatarControls(self):
        if self.controlsTask:
            self.controlsTask.remove()
            self.controlsTask = None
        if self.indicatorTask:
            self.indicatorTask.remove()
            self.indicatorTask = None
        if self.jumpDelayTask:
            self.jumpDelayTask.remove()
            self.jumpDelayTask = None
        return

    def flushEventHandlers(self):
        if hasattr(self, 'cTrav'):
            self.pusher.flush()
            if self.wantFloorSphere:
                self.floorPusher.flush()
            self.event.flush()
        self.lifter.flush()

    def setCollisionRayHeight(self, height):
        cRayNode = self.cRayNodePath.node()
        cRayNode.removeSolid(0)
     
# Can't uncompyle C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\controls\GravityWalker.pyc
Traceback (most recent call last):
  File "C:\python27\lib\uncompyle2\__init__.py", line 206, in main
    uncompyle_file(infile, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 143, in uncompyle_file
    uncompyle(version, co, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 132, in uncompyle
    raise walk.ERROR
ParserError: --- This code section failed: ---

0	LOAD_FAST         'self'
3	LOAD_ATTR         'collisionsActive'
6	LOAD_FAST         'active'
9	COMPARE_OP        '!='
12	JUMP_IF_FALSE     '365'

15	LOAD_FAST         'active'
18	LOAD_FAST         'self'
21	STORE_ATTR        'collisionsActive'

24	LOAD_FAST         'self'
27	LOAD_ATTR         'oneTimeCollide'
30	CALL_FUNCTION_0   None
33	POP_TOP           None

34	LOAD_GLOBAL       'base'
37	LOAD_ATTR         'initShadowTrav'
40	CALL_FUNCTION_0   None
43	POP_TOP           None

44	LOAD_FAST         'active'
47	JUMP_IF_FALSE     '237'

50	LOAD_FAST         'self'
53	LOAD_ATTR         'avatarNodePath'
56	LOAD_ATTR         'setP'
59	LOAD_CONST        0.0
62	CALL_FUNCTION_1   None
65	POP_TOP           None

66	LOAD_FAST         'self'
69	LOAD_ATTR         'avatarNodePath'
72	LOAD_ATTR         'setR'
75	LOAD_CONST        0.0
78	CALL_FUNCTION_1   None
81	POP_TOP           None
82	JUMP_FORWARD      '85'
85_0	COME_FROM         '82'

85	LOAD_FAST         'self'
88	LOAD_ATTR         'cTrav'
91	LOAD_ATTR         'addCollider'
94	LOAD_FAST         'self'
97	LOAD_ATTR         'cWallSphereNodePath'
100	LOAD_FAST         'self'
103	LOAD_ATTR         'pusher'
106	CALL_FUNCTION_2   None
109	POP_TOP           None

110	LOAD_FAST         'self'
113	LOAD_ATTR         'wantFloorSphere'
116	JUMP_IF_FALSE     '147'

119	LOAD_FAST         'self'
122	LOAD_ATTR         'cTrav'
125	LOAD_ATTR         'addCollider'
128	LOAD_FAST         'self'
131	LOAD_ATTR         'cFloorSphereNodePath'
134	LOAD_FAST         'self'
137	LOAD_ATTR         'pusherFloor'
140	CALL_FUNCTION_2   None
143	POP_TOP           None
144	JUMP_FORWARD      '147'
147_0	COME_FROM         '144'

147	LOAD_GLOBAL       'base'
150	LOAD_ATTR         'shadowTrav'
153	LOAD_ATTR         'addCollider'
156	LOAD_FAST         'self'
159	LOAD_ATTR         'cRayNodePath'
162	LOAD_FAST         'self'
165	LOAD_ATTR         'lifter'
168	CALL_FUNCTION_2   None
171	POP_TOP           None

172	LOAD_FAST         'self'
175	LOAD_ATTR         'earlyEventSphere'
178	JUMP_IF_FALSE     '209'

181	LOAD_FAST         'self'
184	LOAD_ATTR         'cTrav'
187	LOAD_ATTR         'addCollider'
190	LOAD_FAST         'self'
193	LOAD_ATTR         'cEventSphereNodePath'
196	LOAD_FAST         'self'
199	LOAD_ATTR         'event'
202	CALL_FUNCTION_2   None
205	POP_TOP           None
206	JUMP_ABSOLUTE     '362'

209	LOAD_GLOBAL       'base'
212	LOAD_ATTR         'shadowTrav'
215	LOAD_ATTR         'addCollider'
218	LOAD_FAST         'self'
221	LOAD_ATTR         'cEventSphereNodePath'
224	LOAD_FAST         'self'
227	LOAD_ATTR         'event'
230	CALL_FUNCTION_2   None
233	POP_TOP           None
234	JUMP_ABSOLUTE     '365'

237	LOAD_GLOBAL       'hasattr'
240	LOAD_FAST         'self'
243	LOAD_CONST        'cTrav'
246	CALL_FUNCTION_2   None
249	JUMP_IF_FALSE     '324'

252	LOAD_FAST         'self'
255	LOAD_ATTR         'cTrav'
258	LOAD_ATTR         'removeCollider'
261	LOAD_FAST         'self'
264	LOAD_ATTR         'cWallSphereNodePath'
267	CALL_FUNCTION_1   None
270	POP_TOP           None

271	LOAD_FAST         'self'
274	LOAD_ATTR         'wantFloorSphere'
277	JUMP_IF_FALSE     '302'

280	LOAD_FAST         'self'
283	LOAD_ATTR         'cTrav'
286	LOAD_ATTR         'removeCollider'
289	LOAD_FAST         'self'
292	LOAD_ATTR         'cFloorSphereNodePath'
295	CALL_FUNCTION_1   None
298	POP_TOP           None
299	JUMP_FORWARD      '302'
302_0	COME_FROM         '299'

302	LOAD_FAST         'self'
305	LOAD_ATTR         'cTrav'
308	LOAD_ATTR         'removeCollider'
311	LOAD_FAST      cRay = CollisionRay(0.0, 0.0, height, 0.0, 0.0, -1.0)
        cRayNode.addSolid(cRay)# decompiled 0 files: 0 okay, 1 failed, 0 verify failed
# 2013.08.22 22:13:47 Pacific Daylight Time
      'self'
314	LOAD_ATTR         'cEventSphereNodePath'
317	CALL_FUNCTION_1   None
320	POP_TOP           None
321	JUMP_FORWARD      '324'
324_0	COME_FROM         '321'

324	LOAD_GLOBAL       'base'
327	LOAD_ATTR         'shadowTrav'
330	LOAD_ATTR         'removeCollider'
333	LOAD_FAST         'self'
336	LOAD_ATTR         'cEventSphereNodePath'
339	CALL_FUNCTION_1   None
342	POP_TOP           None

343	LOAD_GLOBAL       'base'
346	LOAD_ATTR         'shadowTrav'
349	LOAD_ATTR         'removeCollider'
352	LOAD_FAST         'self'
355	LOAD_ATTR         'cRayNodePath'
358	CALL_FUNCTION_1   None
361	POP_TOP           None
362	JUMP_FORWARD      '365'
365_0	COME_FROM         '362'

Syntax error at or near `LOAD_GLOBAL' token at offset 237

