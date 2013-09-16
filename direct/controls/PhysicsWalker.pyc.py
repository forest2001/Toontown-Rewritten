# 2013.08.22 22:13:48 Pacific Daylight Time
# Embedded file name: direct.controls.PhysicsWalker
from direct.directnotify import DirectNotifyGlobal
from direct.showbase import DirectObject
from direct.controls.ControlManager import CollisionHandlerRayStart
from direct.showbase.InputStateGlobal import inputState
from direct.task.Task import Task
from pandac.PandaModules import *
import math

class PhysicsWalker(DirectObject.DirectObject):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('PhysicsWalker')
    wantDebugIndicator = base.config.GetBool('want-avatar-physics-indicator', 0)
    wantAvatarPhysicsIndicator = base.config.GetBool('want-avatar-physics-indicator', 0)
    useLifter = 0
    useHeightRay = 0

    def __init__(self, gravity = -32.174, standableGround = 0.707, hardLandingForce = 16.0):
        DirectObject.DirectObject.__init__(self)
        self.__gravity = gravity
        self.__standableGround = standableGround
        self.__hardLandingForce = hardLandingForce
        self.needToDeltaPos = 0
        self.physVelocityIndicator = None
        self.avatarControlForwardSpeed = 0
        self.avatarControlJumpForce = 0
        self.avatarControlReverseSpeed = 0
        self.avatarControlRotateSpeed = 0
        self.__oldAirborneHeight = None
        self.getAirborneHeight = None
        self.__oldContact = None
        self.__oldPosDelta = Vec3(0)
        self.__oldDt = 0
        self.__speed = 0.0
        self.__rotationSpeed = 0.0
        self.__slideSpeed = 0.0
        self.__vel = Vec3(0.0)
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
        return (self.__speed, self.__rotationSpeed)

    def setAvatar(self, avatar):
        self.avatar = avatar
        if avatar is not None:
            self.setupPhysics(avatar)
        return

    def setupRay(self, floorBitmask, floorOffset):
        self.cRay = CollisionRay(0.0, 0.0, CollisionHandlerRayStart, 0.0, 0.0, -1.0)
        cRayNode = CollisionNode('PW.cRayNode')
        cRayNode.addSolid(self.cRay)
        self.cRayNodePath = self.avatarNodePath.attachNewNode(cRayNode)
        self.cRayBitMask = floorBitmask
        cRayNode.setFromCollideMask(self.cRayBitMask)
        cRayNode.setIntoCollideMask(BitMask32.allOff())
        if self.useLifter:
            self.lifter = CollisionHandlerFloor()
            self.lifter.setInPattern('enter%in')
            self.lifter.setOutPattern('exit%in')
            self.lifter.setOffset(floorOffset)
            self.lifter.addCollider(self.cRayNodePath, self.avatarNodePath)
        else:
            self.cRayQueue = CollisionHandlerQueue()
            self.cTrav.addCollider(self.cRayNodePath, self.cRayQueue)

    def determineHeight(self):
        if self.useLifter:
            height = self.avatarNodePath.getPos(self.cRayNodePath)
            return height.getZ() - self.floorOffset
        else:
            height = 0.0
            if self.cRayQueue.getNumEntries() != 0:
                self.cRayQueue.sortEntries()
                floorPoint = self.cRayQueue.getEntry(0).getFromIntersectionPoint()
                height = -floorPoint.getZ()
            self.cRayQueue.clearEntries()
            return height

    def setupSphere(self, bitmask, avatarRadius):
        self.avatarRadius = avatarRadius
        centerHeight = avatarRadius
        if self.useHeightRay:
            centerHeight *= 2.0
        self.cSphere = CollisionSphere(0.0, 0.0, centerHeight, avatarRadius)
        cSphereNode = CollisionNode('PW.cSphereNode')
        cSphereNode.addSolid(self.cSphere)
        self.cSphereNodePath = self.avatarNodePath.attachNewNode(cSphereNode)
        self.cSphereBitMask = bitmask
        cSphereNode.setFromCollideMask(self.cSphereBitMask)
        cSphereNode.setIntoCollideMask(BitMask32.allOff())
        self.pusher = PhysicsCollisionHandler()
        self.pusher.setInPattern('enter%in')
        self.pusher.setOutPattern('exit%in')
        self.pusher.addCollider(self.cSphereNodePath, self.avatarNodePath)

    def setupPhysics(self, avatarNodePath):
        self.actorNode = ActorNode('PW physicsActor')
        self.actorNode.getPhysicsObject().setOriented(1)
        self.actorNode.getPhysical(0).setViscosity(0.1)
        physicsActor = NodePath(self.actorNode)
        avatarNodePath.reparentTo(physicsActor)
        avatarNodePath.assign(physicsActor)
        self.phys = PhysicsManager()
        fn = ForceNode('gravity')
        fnp = NodePath(fn)
        fnp.reparentTo(render)
        gravity = LinearVectorForce(0.0, 0.0, self.__gravity)
        fn.addForce(gravity)
        self.phys.addLinearForce(gravity)
        self.gravity = gravity
        fn = ForceNode('priorParent')
        fnp = NodePath(fn)
        fnp.reparentTo(render)
        priorParent = LinearVectorForce(0.0, 0.0, 0.0)
        fn.addForce(priorParent)
        self.phys.addLinearForce(priorParent)
        self.priorParentNp = fnp
        self.priorParent = priorParent
        fn = ForceNode('viscosity')
        fnp = NodePath(fn)
        fnp.reparentTo(render)
        self.avatarViscosity = LinearFrictionForce(0.0, 1.0, 0)
        fn.addForce(self.avatarViscosity)
        self.phys.addLinearForce(self.avatarViscosity)
        self.phys.attachLinearIntegrator(LinearEulerIntegrator())
        self.phys.attachPhysicalNode(physicsActor.node())
        self.acForce = LinearVectorForce(0.0, 0.0, 0.0)
        fn = ForceNode('avatarControls')
        fnp = NodePath(fn)
        fnp.reparentTo(render)
        fn.addForce(self.acForce)
        self.phys.addLinearForce(self.acForce)
        return avatarNodePath

    def initializeCollisions(self, collisionTraverser, avatarNodePath, wallBitmask, floorBitmask, avatarRadius = 1.4, floorOffset = 1.0, reach = 1.0):
        self.cTrav = collisionTraverser
        self.floorOffset = floorOffset = 7.0
        self.avatarNodePath = self.setupPhysics(avatarNodePath)
        if 0 or self.useHeightRay:
            self.setupRay(floorBitmask, 0.0)
        self.setupSphere(wallBitmask | floorBitmask, avatarRadius)
        self.setCollisionsActive(1)

    def setAirborneHeightFunc(self, getAirborneHeight):
        self.getAirborneHeight = getAirborneHeight

    def setAvatarPhysicsIndicator(self, indicator):
        self.cSphereNodePath.show()
        if indicator:
            change = render.attachNewNode('change')
            change.setScale(0.1)
            indicator.reparentTo(change)
            indicatorNode = render.attachNewNode('physVelocityIndicator')
            indicatorNode.setPos(self.avatarNodePath, 0.0, 0.0, 6.0)
            indicatorNode.setColor(0.0, 0.0, 1.0, 1.0)
            change.reparentTo(indicatorNode)
            self.physVelocityIndicator = indicatorNode
            contactIndicatorNode = render.attachNewNode('physContactIndicator')
            contactIndicatorNode.setScale(0.25)
            contactIndicatorNode.setP(90.0)
            contactIndicatorNode.setPos(self.avatarNodePath, 0.0, 0.0, 5.0)
            contactIndicatorNode.setColor(1.0, 0.0, 0.0, 1.0)
            indicator.instanceTo(contactIndicatorNode)
            self.physContactIndicator = contactIndicatorNode
        else:
            print 'failed load of physics indicator'

    def avatarPhysicsIndicator(self, task):
        self.physVelocityIndicator.setPos(self.avatarNodePath, 0.0, 0.0, 6.0)
        physObject = self.actorNode.getPhysicsObject()
        a = physObject.getVelocity()
        self.physVelocityIndicator.setScale(math.sqrt(a.length()))
        a += self.physVelocityIndicator.getPos()
        self.physVelocityIndicator.lookAt(Point3(a))
        contact = self.actorNode.getContactVector()
        if contact == Vec3.zero():
            self.physContactIndicator.hide()
        else:
            self.physContactIndicator.show()
            self.physContactIndicator.setPos(self.avatarNodePath, 0.0, 0.0, 5.0)
            point = Point3(contact + self.physContactIndicator.getPos())
            self.physContactIndicator.lookAt(point)
        return Task.cont

    def deleteCollisions(self):
        del self.cTrav
        if self.useHeightRay:
            del self.cRayQueue
            self.cRayNodePath.removeNode()
            del self.cRayNodePath
        del self.cSphere
        self.cSphereNodePath.removeNode()
        del self.cSphereNodePath
        del self.pusher
        del self.getAirborneHeight

    def setCollisionsActive(self, active = 1):
        if self.collisionsActive != active:
            self.collisionsActive = active
            if active:
                self.cTrav.addCollider(self.cSphereNodePath, self.pusher)
                if self.useHeightRay:
                    if self.useLifter:
                        self.cTrav.addCollider(self.cRayNodePath, self.lifter)
                    else:
                        self.cTrav.addCollider(self.cRayNodePath, self.cRayQueue)
            else:
                self.cTrav.removeCollider(self.cSphereNodePath)
                if self.useHeightRay:
                    self.cTrav.removeCollider(self.cRayNodePath)
                self.oneTimeCollide()

    def getCollisionsActive(self):
        return self.collisionsActive

    def placeOnFloor(self):
        self.oneTimeCollide()
        self.avatarNodePath.setZ(self.avatarNodePath.getZ() - self.getAirborneHeight())

    def oneTimeCollide(self):
        tempCTrav = CollisionTraverser('oneTimeCollide')
        if self.useHeightRay:
            if self.useLifter:
                tempCTrav.addCollider(self.cRayNodePath, self.lifter)
            else:
                tempCTrav.addCollider(self.cRayNodePath, self.cRayQueue)
        tempCTrav.traverse(render)

    def addBlastForce(self, vector):
        pass

    def displayDebugInfo(self):
        onScreenDebug.add('w controls', 'PhysicsWalker')
        if self.useLifter:
            onScreenDebug.add('w airborneHeight', self.lifter.getAirborneHeight())
            onScreenDebug.add('w isOnGround', self.lifter.isOnGround())
            onScreenDebug.add('w contact normal', self.lifter.getContactNormal().pPrintValues())
            onScreenDebug.add('w impact', self.lifter.getImpactVelocity())
            onScreenDebug.add('w velocity', self.lifter.getVelocity())
            onScreenDebug.add('w hasContact', self.lifter.hasContact())
        onScreenDebug.add('w isAirborne', self.isAirborne)

    def handleAvatarControls(self, task):
        physObject = self.actorNode.getPhysicsObject()
        contact = self.actorNode.getContactVector()
        if contact == Vec3.zero() and self.avatarNodePath.getZ() < -50.0:
            self.reset()
            self.avatarNodePath.setZ(50.0)
            messenger.send('walkerIsOutOfWorld', [self.avatarNodePath])
        if self.wantDebugIndicator:
            self.displayDebugInfo()
        forward = inputState.isSet('forward')
        reverse = inputState.isSet('reverse')
        turnLeft = inputState.isSet('turnLeft')
        turnRight = inputState.isSet('turnRight')
        slide = 0
        slideLeft = 0
        slideRight = 0
        jump = inputState.isSet('jump')
        if base.localAvatar.getAutoRun():
            forward = 1
            reverse = 0
        self.__speed = forward and self.avatarControlForwardSpeed or reverse and -self.avatarControlReverseSpeed
        avatarSlideSpeed = self.avatarControlForwardSpeed * 0.5
        self.__slideSpeed = slideLeft and -avatarSlideSpeed or slideRight and avatarSlideSpeed
        if not (not slide and turnLeft and self.avatarControlRotateSpeed):
            if turnRight:
                self.__rotationSpeed = -self.avatarControlRotateSpeed
                dt = ClockObject.getGlobalClock().getDt()
                if self.needToDeltaPos:
                    self.setPriorParentVector()
                    self.needToDeltaPos = 0
                self.__oldPosDelta = self.avatarNodePath.getPosDelta(render)
                self.__oldDt = dt
                airborneHeight = self.getAirborneHeight()
                if airborneHeight > self.highMark:
                    self.highMark = airborneHeight
                if airborneHeight > self.avatarRadius * 0.5 or physObject.getVelocity().getZ() > 0.0:
                    self.isAirborne = 1
                elif self.isAirborne and physObject.getVelocity().getZ() <= 0.0:
                    contactLength = contact.length()
                    if contactLength > self.__hardLandingForce:
                        messenger.send('jumpHardLand')
                    else:
                        messenger.send('jumpLand')
                    self.priorParent.setVector(Vec3.zero())
                    self.isAirborne = 0
                elif jump:
                    messenger.send('jumpStart')
                    jumpVec = Vec3.up()
                    jumpVec *= self.avatarControlJumpForce
                    physObject.addImpulse(Vec3(jumpVec))
                    self.isAirborne = 1
                else:
                    self.isAirborne = 0
            elif contact != Vec3.zero():
                contactLength = contact.length()
                contact.normalize()
                angle = contact.dot(Vec3.up())
                if angle > self.__standableGround:
                    if self.__oldContact == Vec3.zero():
                        self.jumpCount -= 1
                        if contactLength > self.__hardLandingForce:
                            messenger.send('jumpHardLand')
                        else:
                            messenger.send('jumpLand')
                    elif jump:
                        self.jumpCount += 1
                        messenger.send('jumpStart')
                        jump = Vec3(contact + Vec3.up())
                        jump.normalize()
                        jump *= self.avatarControlJumpForce
                        physObject.addImpulse(Vec3(jump))
            if contact != self.__oldContact:
                self.__oldContact = Vec3(contact)
            self.__oldAirborneHeight = airborneHeight
            moveToGround = Vec3.zero()
            if not self.useHeightRay or self.isAirborne:
                self.phys.doPhysics(dt)
            else:
                physObject.setVelocity(Vec3.zero())
                moveToGround = Vec3(0.0, 0.0, -self.determineHeight())
            distance = (self.__speed or self.__slideSpeed or self.__rotationSpeed or moveToGround != Vec3.zero()) and dt * self.__speed
            slideDistance = dt * self.__slideSpeed
            rotation = dt * self.__rotationSpeed
            self.__vel = Vec3(Vec3.forward() * distance + Vec3.right() * slideDistance)
            rotMat = Mat3.rotateMatNormaxis(self.avatarNodePath.getH(), Vec3.up())
            step = rotMat.xform(self.__vel)
            physObject.setPosition(Point3(physObject.getPosition() + step + moveToGround))
            o = physObject.getOrientation()
            r = LRotationf()
            r.setHpr(Vec3(rotation, 0.0, 0.0))
            physObject.setOrientation(o * r)
            self.actorNode.updateTransform()
            messenger.send('avatarMoving')
        else:
            self.__vel.set(0.0, 0.0, 0.0)
        self.actorNode.setContactVector(Vec3.zero())
        return Task.cont

    def doDeltaPos(self):
        self.needToDeltaPos = 1

    def setPriorParentVector(self):
        print 'self.__oldDt', self.__oldDt, 'self.__oldPosDelta', self.__oldPosDelta
        velocity = self.__oldPosDelta * (1 / self.__oldDt) * 4.0
        self.priorParent.setVector(Vec3(velocity))

    def reset(self):
        self.actorNode.getPhysicsObject().resetPosition(self.avatarNodePath.getPos())
        self.priorParent.setVector(Vec3.zero())
        self.highMark = 0
        self.actorNode.setContactVector(Vec3.zero())

    def getVelocity(self):
        physObject = self.actorNode.getPhysicsObject()
        return physObject.getVelocity()

    def enableAvatarControls(self):
        taskName = 'AvatarControls-%s' % (id(self),)
        taskMgr.remove(taskName)
        taskMgr.add(self.handleAvatarControls, taskName, 25)
        if self.physVelocityIndicator:
            taskMgr.add(self.avatarPhysicsIndicator, 'AvatarControlsIndicator%s' % (id(self),), 35)

    def disableAvatarControls(self):
        taskName = 'AvatarControls-%s' % (id(self),)
        taskMgr.remove(taskName)
        taskName = 'AvatarControlsIndicator%s' % (id(self),)
        taskMgr.remove(taskName)

    def flushEventHandlers(self):
        if hasattr(self, 'cTrav'):
            if self.useLifter:
                self.lifter.flush()
            self.pusher.flush()
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\controls\PhysicsWalker.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:13:49 Pacific Daylight Time
