# 2013.08.22 22:13:50 Pacific Daylight Time
# Embedded file name: direct.directtools.DirectCameraControl
from direct.showbase.DirectObject import DirectObject
from DirectUtil import *
from DirectGeometry import *
from DirectGlobals import *
from DirectSelection import SelectionRay
from direct.interval.IntervalGlobal import Sequence, Func
from direct.directnotify import DirectNotifyGlobal
from direct.task import Task
CAM_MOVE_DURATION = 1.2
COA_MARKER_SF = 0.0075
Y_AXIS = Vec3(0, 1, 0)

class DirectCameraControl(DirectObject):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('DirectCameraControl')

    def __init__(self):
        self.startT = 0.0
        self.startF = 0
        self.orthoViewRoll = 0.0
        self.lastView = 0
        self.coa = Point3(0, 100, 0)
        self.coaMarker = loader.loadModel('models/misc/sphere')
        self.coaMarker.setName('DirectCameraCOAMarker')
        self.coaMarker.setTransparency(1)
        self.coaMarker.setColor(1, 0, 0, 0)
        self.coaMarker.setPos(0, 100, 0)
        useDirectRenderStyle(self.coaMarker)
        self.coaMarkerPos = Point3(0)
        self.coaMarkerColorIval = None
        self.fLockCOA = 0
        self.nullHitPointCount = 0
        self.cqEntries = []
        self.coaMarkerRef = base.direct.group.attachNewNode('coaMarkerRef')
        self.camManipRef = base.direct.group.attachNewNode('camManipRef')
        t = CAM_MOVE_DURATION
        self.actionEvents = [['DIRECT-mouse1', self.mouseRotateStart],
         ['DIRECT-mouse1Up', self.mouseDollyStop],
         ['DIRECT-mouse2', self.mouseFlyStart],
         ['DIRECT-mouse2Up', self.mouseFlyStop],
         ['DIRECT-mouse3', self.mouseDollyStart],
         ['DIRECT-mouse3Up', self.mouseDollyStop]]
        self.keyEvents = [['DIRECT-centerCamIn', self.centerCamIn, 0.5],
         ['DIRECT-fitOnWidget', self.fitOnWidget],
         ['DIRECT-homeCam', self.homeCam],
         ['DIRECT-toggleMarkerVis', self.toggleMarkerVis],
         ['DIRECT-moveToFit', self.moveToFit],
         ['DIRECT-pickNextCOA', self.pickNextCOA],
         ['DIRECT-orbitUprightCam', self.orbitUprightCam],
         ['DIRECT-uprightCam', self.uprightCam],
         ['DIRECT-spwanMoveToView-1', self.spawnMoveToView, 1],
         ['DIRECT-spwanMoveToView-2', self.spawnMoveToView, 2],
         ['DIRECT-spwanMoveToView-3', self.spawnMoveToView, 3],
         ['DIRECT-spwanMoveToView-4', self.spawnMoveToView, 4],
         ['DIRECT-spwanMoveToView-5', self.spawnMoveToView, 5],
         ['DIRECT-spwanMoveToView-6', self.spawnMoveToView, 6],
         ['DIRECT-spwanMoveToView-7', self.spawnMoveToView, 7],
         ['DIRECT-spwanMoveToView-8', self.spawnMoveToView, 8],
         ['DIRECT-swingCamAboutWidget-0',
          self.swingCamAboutWidget,
          -90.0,
          t],
         ['DIRECT-swingCamAboutWidget-1',
          self.swingCamAboutWidget,
          90.0,
          t],
         ['DIRECT-removeManipulateCameraTask', self.removeManipulateCameraTask],
         ['DIRECT-zoomInCam',
          self.zoomCam,
          0.5,
          t],
         ['DIRECT-zoomOutCam',
          self.zoomCam,
          -2.0,
          t]]
        self.lockRoll = False
        self.useMayaCamControls = 0
        self.altDown = 0
        self.perspCollPlane = None
        self.perspCollPlane2 = None
        return None

    def toggleMarkerVis(self):
        if self.coaMarker.isHidden():
            self.coaMarker.show()
        else:
            self.coaMarker.hide()

    def mouseRotateStart(self, modifiers):
        if self.useMayaCamControls and modifiers == 4:
            self.spawnMouseRotateTask()

    def mouseDollyStart(self, modifiers):
        if self.useMayaCamControls and modifiers == 4:
            self.coaMarker.hide()
            self.startT = globalClock.getFrameTime()
            self.startF = globalClock.getFrameCount()
            if hasattr(base.direct, 'manipulationControl') and base.direct.manipulationControl.fMultiView and base.direct.camera.getName() != 'persp':
                self.spawnOrthoZoom()
            else:
                self.spawnHPanYZoom()

    def mouseDollyStop(self):
        taskMgr.remove('manipulateCamera')

    def mouseFlyStart(self, modifiers):
        if self.useMayaCamControls and modifiers == 4:
            self.coaMarker.hide()
            self.startT = globalClock.getFrameTime()
            self.startF = globalClock.getFrameCount()
            if hasattr(base.direct, 'manipulationControl') and base.direct.manipulationControl.fMultiView and base.direct.camera.getName() != 'persp':
                self.spawnOrthoTranslate()
            else:
                self.spawnXZTranslate()
            self.altDown = 1
        elif not self.useMayaCamControls:
            if abs(base.direct.dr.mouseX) < 0.9 and abs(base.direct.dr.mouseY) < 0.9:
                self.coaMarker.hide()
                self.startT = globalClock.getFrameTime()
                self.startF = globalClock.getFrameCount()
                self.spawnXZTranslateOrHPanYZoom()
            elif abs(base.direct.dr.mouseX) > 0.9 and abs(base.direct.dr.mouseY) > 0.9:
                self.spawnMouseRollTask()
            else:
                self.spawnMouseRotateTask()
        if not modifiers == 4:
            self.altDown = 0

    def mouseFlyStop(self):
        taskMgr.remove('manipulateCamera')
        stopT = globalClock.getFrameTime()
        deltaT = stopT - self.startT
        stopF = globalClock.getFrameCount()
        deltaF = stopF - self.startF
        if not self.altDown and len(base.direct.selected.getSelectedAsList()) == 0:
            skipFlags = SKIP_HIDDEN | SKIP_BACKFACE
            skipFlags |= SKIP_CAMERA * (1 - base.getControl())
            self.computeCOA(base.direct.iRay.pickGeom(skipFlags=skipFlags))
            self.coaMarkerRef.iPosHprScale(base.cam)
            self.cqEntries = []
            for i in range(base.direct.iRay.getNumEntries()):
                self.cqEntries.append(base.direct.iRay.getEntry(i))

        self.coaMarker.show()
        self.updateCoaMarkerSize()

    def mouseFlyStartTopWin(self):
        print 'Moving mouse 2 in new window'

    def mouseFlyStopTopWin(self):
        print 'Stopping mouse 2 in new window'

    def spawnXZTranslateOrHPanYZoom(self):
        taskMgr.remove('manipulateCamera')
        t = Task.Task(self.XZTranslateOrHPanYZoomTask)
        t.zoomSF = Vec3(self.coaMarker.getPos(base.direct.camera)).length()
        taskMgr.add(t, 'manipulateCamera')

    def spawnXZTranslateOrHPPan(self):
        taskMgr.remove('manipulateCamera')
        taskMgr.add(self.XZTranslateOrHPPanTask, 'manipulateCamera')

    def spawnXZTranslate(self):
        taskMgr.remove('manipulateCamera')
        taskMgr.add(self.XZTranslateTask, 'manipulateCamera')

    def spawnOrthoTranslate(self):
        taskMgr.remove('manipulateCamera')
        taskMgr.add(self.OrthoTranslateTask, 'manipulateCamera')

    def spawnHPanYZoom(self):
        taskMgr.remove('manipulateCamera')
        t = Task.Task(self.HPanYZoomTask)
        t.zoomSF = Vec3(self.coaMarker.getPos(base.direct.camera)).length()
        taskMgr.add(t, 'manipulateCamera')

    def spawnOrthoZoom(self):
        taskMgr.remove('manipulateCamera')
        t = Task.Task(self.OrthoZoomTask)
        taskMgr.add(t, 'manipulateCamera')

    def spawnHPPan(self):
        taskMgr.remove('manipulateCamera')
        taskMgr.add(self.HPPanTask, 'manipulateCamera')

    def XZTranslateOrHPanYZoomTask(self, state):
        if base.direct.fShift:
            return self.XZTranslateTask(state)
        else:
            return self.HPanYZoomTask(state)

    def XZTranslateOrHPPanTask(self, state):
        if base.direct.fShift:
            return self.HPPanTask(state)
        else:
            return self.XZTranslateTask(state)

    def XZTranslateTask(self, state):
        coaDist = Vec3(self.coaMarker.getPos(base.direct.camera)).length()
        xlateSF = coaDist / base.direct.dr.near
        base.direct.camera.setPos(base.direct.camera, -0.5 * base.direct.dr.mouseDeltaX * base.direct.dr.nearWidth * xlateSF, 0.0, -0.5 * base.direct.dr.mouseDeltaY * base.direct.dr.nearHeight * xlateSF)
        return Task.cont

    def OrthoTranslateTask(self, state):
        iRay = SelectionRay(base.direct.camera)
        iRay.collider.setFromLens(base.direct.camNode, base.direct.dr.mouseX, base.direct.dr.mouseY)
        iRay.collideWithBitMask(BitMask32.bit(21))
        iRay.ct.traverse(base.direct.grid)
        entry = iRay.getEntry(0)
        hitPt = entry.getSurfacePoint(entry.getFromNodePath())
        iRay.collisionNodePath.removeNode()
        del iRay
        if hasattr(state, 'prevPt'):
            base.direct.camera.setPos(base.direct.camera, state.prevPt - hitPt)
        state.prevPt = hitPt
        return Task.cont

    def HPanYZoomTask(self, state):
        if hasattr(base.direct.cam.node(), 'getLens') and base.direct.cam.node().getLens().__class__.__name__ == 'OrthographicLens':
            return
        if base.direct.fControl:
            moveDir = Vec3(self.coaMarker.getPos(base.direct.camera))
            if moveDir[1] < 0.0:
                moveDir.assign(moveDir * -1)
            moveDir.normalize()
        else:
            moveDir = Vec3(Y_AXIS)
        if self.useMayaCamControls:
            moveDir.assign(moveDir * ((base.direct.dr.mouseDeltaX - 1.0 * base.direct.dr.mouseDeltaY) * state.zoomSF))
            hVal = 0.0
        else:
            moveDir.assign(moveDir * (-1.0 * base.direct.dr.mouseDeltaY * state.zoomSF))
            if base.direct.dr.mouseDeltaY > 0.0:
                moveDir.setY(moveDir[1] * 1.0)
            hVal = 0.5 * base.direct.dr.mouseDeltaX * base.direct.dr.fovH
        base.direct.camera.setPosHpr(base.direct.camera, moveDir[0], moveDir[1], moveDir[2], hVal, 0.0, 0.0)
        if self.lockRoll == True:
            base.direct.camera.setR(0)
        return Task.cont

    def OrthoZoomTask(self, state):
        filmSize = base.direct.camNode.getLens().getFilmSize()
        factor = (base.direct.dr.mouseDeltaX - 1.0 * base.direct.dr.mouseDeltaY) * 0.1
        x = base.direct.dr.getWidth()
        y = base.direct.dr.getHeight()
        base.direct.dr.orthoFactor -= factor
        if base.direct.dr.orthoFactor < 0:
            base.direct.dr.orthoFactor = 0.0001
        base.direct.dr.updateFilmSize(x, y)
        return Task.cont

    def HPPanTask(self, state):
        base.direct.camera.setHpr(base.direct.camera, 0.5 * base.direct.dr.mouseDeltaX * base.direct.dr.fovH, -0.5 * base.direct.dr.mouseDeltaY * base.direct.dr.fovV, 0.0)
        return Task.cont

    def spawnMouseRotateTask(self):
        taskMgr.remove('manipulateCamera')
        if self.perspCollPlane:
            iRay = SelectionRay(base.direct.camera)
            iRay.collider.setFromLens(base.direct.camNode, 0.0, 0.0)
            iRay.collideWithBitMask(1)
            if base.direct.camera.getPos().getZ() >= 0:
                iRay.ct.traverse(self.perspCollPlane)
            else:
                iRay.ct.traverse(self.perspCollPlane2)
            if iRay.getNumEntries() > 0:
                entry = iRay.getEntry(0)
                hitPt = entry.getSurfacePoint(entry.getFromNodePath())
                np = NodePath('temp')
                np.setPos(base.direct.camera, hitPt)
                self.coaMarkerPos = np.getPos()
                np.remove()
                self.coaMarker.setPos(self.coaMarkerPos)
            iRay.collisionNodePath.removeNode()
            del iRay
        self.camManipRef.setPos(self.coaMarkerPos)
        self.camManipRef.setHpr(base.direct.camera, ZERO_POINT)
        t = Task.Task(self.mouseRotateTask)
        if abs(base.direct.dr.mouseX) > 0.9:
            t.constrainedDir = 'y'
        else:
            t.constrainedDir = 'x'
        taskMgr.add(t, 'manipulateCamera')

    def mouseRotateTask(self, state):
        if hasattr(base.direct.cam.node(), 'getLens') and base.direct.cam.node().getLens().__class__.__name__ == 'OrthographicLens':
            return
        if state.constrainedDir == 'y' and abs(base.direct.dr.mouseX) > 0.9:
            deltaX = 0
            deltaY = base.direct.dr.mouseDeltaY
        elif state.constrainedDir == 'x' and abs(base.direct.dr.mouseY) > 0.9:
            deltaX = base.direct.dr.mouseDeltaX
            deltaY = 0
        else:
            deltaX = base.direct.dr.mouseDeltaX
            deltaY = base.direct.dr.mouseDeltaY
        if base.direct.fShift:
            base.direct.camera.setHpr(base.direct.camera, deltaX * base.direct.dr.fovH, -deltaY * base.direct.dr.fovV, 0.0)
            if self.lockRoll == True:
                base.direct.camera.setR(0)
            self.camManipRef.setPos(self.coaMarkerPos)
            self.camManipRef.setHpr(base.direct.camera, ZERO_POINT)
        else:
            if base.direct.camera.getPos().getZ() >= 0:
                dirX = -1
            else:
                dirX = 1
            wrt = base.direct.camera.getTransform(self.camManipRef)
            self.camManipRef.setHpr(self.camManipRef, dirX * deltaX * 180.0, deltaY * 180.0, 0.0)
            if self.lockRoll == True:
                self.camManipRef.setR(0)
            base.direct.camera.setTransform(self.camManipRef, wrt)
        return Task.cont

    def spawnMouseRollTask(self):
        taskMgr.remove('manipulateCamera')
        self.camManipRef.setPos(self.coaMarkerPos)
        self.camManipRef.setHpr(base.direct.camera, ZERO_POINT)
        t = Task.Task(self.mouseRollTask)
        t.coaCenter = getScreenXY(self.coaMarker)
        t.lastAngle = getCrankAngle(t.coaCenter)
        t.wrt = base.direct.camera.getTransform(self.camManipRef)
        taskMgr.add(t, 'manipulateCamera')

    def mouseRollTask(self, state):
        wrt = state.wrt
        angle = getCrankAngle(state.coaCenter)
        deltaAngle = angle - state.lastAngle
        state.lastAngle = angle
        self.camManipRef.setHpr(self.camManipRef, 0, 0, deltaAngle)
        if self.lockRoll == True:
            self.camManipRef.setR(0)
        base.direct.camera.setTransform(self.camManipRef, wrt)
        return Task.cont

    def lockCOA(self):
        self.fLockCOA = 1
        base.direct.message('COA Lock On')

    def unlockCOA(self):
        self.fLockCOA = 0
        base.direct.message('COA Lock Off')

    def toggleCOALock(self):
        self.fLockCOA = 1 - self.fLockCOA
        if self.fLockCOA:
            base.direct.message('COA Lock On')
        else:
            base.direct.message('COA Lock Off')

    def pickNextCOA(self):
        if self.cqEntries:
            entry = self.cqEntries[0]
            self.cqEntries = self.cqEntries[1:] + self.cqEntries[:1]
            nodePath = entry.getIntoNodePath()
            if base.direct.camera not in nodePath.getAncestors():
                hitPt = entry.getSurfacePoint(entry.getFromNodePath())
                self.updateCoa(hitPt, ref=self.coaMarkerRef)
            else:
                self.cqEntries = self.cqEntries[:-1]
                self.pickNextCOA()

    def computeCOA(self, entry):
        coa = Point3(0)
        dr = base.direct.drList.getCurrentDr()
        if self.fLockCOA:
            coa.assign(self.coaMarker.getPos(base.direct.camera))
            self.nullHitPointCount = 0
        elif entry:
            hitPt = entry.getSurfacePoint(entry.getFromNodePath())
            hitPtDist = Vec3(hitPt).length()
            coa.assign(hitPt)
            if hitPtDist < 1.1 * dr.near or hitPtDist > dr.far:
                coa.assign(self.coaMarker.getPos(base.direct.camera))
            self.nullHitPointCount = 0
        else:
            self.nullHitPointCount = (self.nullHitPointCount + 1) % 7
            dist = pow(10.0, self.nullHitPointCount)
            base.direct.message('COA Distance: ' + repr(dist))
            coa.set(0, dist, 0)
        coaDist = Vec3(coa - ZERO_POINT).length()
        if coaDist < 1.1 * dr.near:
            coa.set(0, 100, 0)
            coaDist = 100
        self.updateCoa(coa, coaDist=coaDist)

    def updateCoa(self, ref2point, coaDist = None, ref = None):
        self.coa.set(ref2point[0], ref2point[1], ref2point[2])
        if not coaDist:
            coaDist = Vec3(self.coa - ZERO_POINT).length()
        if ref == None:
            ref = base.direct.drList.getCurrentDr().cam
        self.coaMarker.setPos(ref, self.coa)
        pos = self.coaMarker.getPos()
        self.coaMarker.setPosHprScale(pos, Vec3(0), Vec3(1))
        self.updateCoaMarkerSize(coaDist)
        self.coaMarkerPos.assign(self.coaMarker.getPos())
        return

    def updateCoaMarkerSizeOnDeath(self, state):
        self.updateCoaMarkerSize()

    def updateCoaMarkerSize(self, coaDist = None):
        if not coaDist:
            coaDist = Vec3(self.coaMarker.getPos(base.direct.camera)).length()
        sf = COA_MARKER_SF * coaDist * (base.direct.drList.getCurrentDr().fovV / 30.0)
        if sf == 0.0:
            sf = 0.1
        self.coaMarker.setScale(sf)
        if self.coaMarkerColorIval:
            self.coaMarkerColorIval.finish()
        self.coaMarkerColorIval = Sequence(Func(self.coaMarker.unstash), self.coaMarker.colorInterval(1.5, Vec4(1, 0, 0, 0), startColor=Vec4(1, 0, 0, 1), blendType='easeInOut'), Func(self.coaMarker.stash))
        self.coaMarkerColorIval.start()

    def homeCam(self):
        base.direct.pushUndo([base.direct.camera])
        base.direct.camera.reparentTo(render)
        base.direct.camera.clearMat()
        self.updateCoaMarkerSize()

    def uprightCam(self):
        taskMgr.remove('manipulateCamera')
        base.direct.pushUndo([base.direct.camera])
        currH = base.direct.camera.getH()
        base.direct.camera.lerpHpr(currH, 0, 0, CAM_MOVE_DURATION, other=render, blendType='easeInOut', task='manipulateCamera')

    def orbitUprightCam(self):
        taskMgr.remove('manipulateCamera')
        base.direct.pushUndo([base.direct.camera])
        mCam2Render = Mat4(Mat4.identMat())
        mCam2Render.assign(base.direct.camera.getMat(render))
        zAxis = Vec3(mCam2Render.xformVec(Z_AXIS))
        zAxis.normalize()
        orbitAngle = rad2Deg(math.acos(CLAMP(zAxis.dot(Z_AXIS), -1, 1)))
        if orbitAngle < 0.1:
            return
        rotAxis = Vec3(zAxis.cross(Z_AXIS))
        rotAxis.normalize()
        rotAngle = rad2Deg(math.acos(CLAMP(rotAxis.dot(X_AXIS), -1, 1)))
        if rotAxis[1] < 0:
            rotAngle *= -1
        self.camManipRef.setPos(self.coaMarker, Vec3(0))
        self.camManipRef.setHpr(render, rotAngle, 0, 0)
        parent = base.direct.camera.getParent()
        base.direct.camera.wrtReparentTo(self.camManipRef)
        t = self.camManipRef.lerpHpr(rotAngle, orbitAngle, 0, CAM_MOVE_DURATION, other=render, blendType='easeInOut', task='manipulateCamera')
        t.parent = parent
        t.setUponDeath(self.reparentCam)

    def centerCam(self):
        self.centerCamIn(1.0)

    def centerCamNow(self):
        self.centerCamIn(0.0)

    def centerCamIn(self, t):
        taskMgr.remove('manipulateCamera')
        base.direct.pushUndo([base.direct.camera])
        markerToCam = self.coaMarker.getPos(base.direct.camera)
        dist = Vec3(markerToCam - ZERO_POINT).length()
        scaledCenterVec = Y_AXIS * dist
        delta = markerToCam - scaledCenterVec
        self.camManipRef.setPosHpr(base.direct.camera, Point3(0), Point3(0))
        t = base.direct.camera.lerpPos(Point3(delta), CAM_MOVE_DURATION, other=self.camManipRef, blendType='easeInOut', task='manipulateCamera')
        t.setUponDeath(self.updateCoaMarkerSizeOnDeath)

    def zoomCam(self, zoomFactor, t):
        taskMgr.remove('manipulateCamera')
        base.direct.pushUndo([base.direct.camera])
        zoomPtToCam = self.coaMarker.getPos(base.direct.camera) * zoomFactor
        self.camManipRef.setPos(base.direct.camera, zoomPtToCam)
        t = base.direct.camera.lerpPos(ZERO_POINT, CAM_MOVE_DURATION, other=self.camManipRef, blendType='easeInOut', task='manipulateCamera')
        t.setUponDeath(self.updateCoaMarkerSizeOnDeath)

    def spawnMoveToView(self, view):
        taskMgr.remove('manipulateCamera')
        base.direct.pushUndo([base.direct.camera])
        hprOffset = VBase3()
        if view == 8:
            self.orthoViewRoll = (self.orthoViewRoll + 90.0) % 360.0
            view = self.lastView
        else:
            self.orthoViewRoll = 0.0
        if view == 1:
            hprOffset.set(180.0, 0.0, 0.0)
        elif view == 2:
            hprOffset.set(0.0, 0.0, 0.0)
        elif view == 3:
            hprOffset.set(90.0, 0.0, 0.0)
        elif view == 4:
            hprOffset.set(-90.0, 0.0, 0.0)
        elif view == 5:
            hprOffset.set(0.0, -90.0, 0.0)
        elif view == 6:
            hprOffset.set(0.0, 90.0, 0.0)
        elif view == 7:
            hprOffset.set(135.0, -35.264, 0.0)
        self.camManipRef.setPosHpr(self.coaMarker, ZERO_VEC, hprOffset)
        offsetDistance = Vec3(base.direct.camera.getPos(self.camManipRef) - ZERO_POINT).length()
        scaledCenterVec = Y_AXIS * (-1.0 * offsetDistance)
        self.camManipRef.setPosHpr(self.camManipRef, scaledCenterVec, ZERO_VEC)
        self.lastView = view
        t = base.direct.camera.lerpPosHpr(ZERO_POINT, VBase3(0, 0, self.orthoViewRoll), CAM_MOVE_DURATION, other=self.camManipRef, blendType='easeInOut', task='manipulateCamera')
        t.setUponDeath(self.updateCoaMarkerSizeOnDeath)

    def swingCamAboutWidget(self, degrees, t):
        taskMgr.remove('manipulateCamera')
        base.direct.pushUndo([base.direct.camera])
        self.camManipRef.setPos(self.coaMarker, ZERO_POINT)
        self.camManipRef.setHpr(ZERO_POINT)
        parent = base.direct.camera.getParent()
        base.direct.camera.wrtReparentTo(self.camManipRef)
        manipTask = self.camManipRef.lerpHpr(VBase3(degrees, 0, 0), CAM_MOVE_DURATION, blendType='easeInOut', task='manipulateCamera')
        manipTask.parent = parent
        manipTask.setUponDeath(self.reparentCam)

    def reparentCam(self, state):
        base.direct.camera.wrtReparentTo(state.parent)
        self.updateCoaMarkerSize()

    def fitOnWidget(self, nodePath = 'None Given'):
        taskMgr.remove('manipulateCamera')
        nodeScale = base.direct.widget.scalingNode.getScale(render)
        maxScale = max(nodeScale[0], nodeScale[1], nodeScale[2])
        maxDim = min(base.direct.dr.nearWidth, base.direct.dr.nearHeight)
        camY = base.direct.dr.near * (2.0 * maxScale) / (0.3 * maxDim)
        centerVec = Y_AXIS * camY
        vWidget2Camera = base.direct.widget.getPos(base.direct.camera)
        deltaMove = vWidget2Camera - centerVec
        try:
            self.camManipRef.setPos(base.direct.camera, deltaMove)
        except Exception:
            self.notify.debug

        parent = base.direct.camera.getParent()
        base.direct.camera.wrtReparentTo(self.camManipRef)
        fitTask = base.direct.camera.lerpPos(Point3(0, 0, 0), CAM_MOVE_DURATION, blendType='easeInOut', task='manipulateCamera')
        fitTask.parent = parent
        fitTask.setUponDeath(self.reparentCam)

    def moveToFit(self):
        widgetScale = base.direct.widget.scalingNode.getScale(render)
        maxScale = max(widgetScale[0], widgetScale[1], widgetScale[2])
        camY = 2 * base.direct.dr.near * (1.5 * maxScale) / min(base.direct.dr.nearWidth, base.direct.dr.nearHeight)
        centerVec = Y_AXIS * camY
        base.direct.selected.getWrtAll()
        base.direct.pushUndo(base.direct.selected)
        taskMgr.remove('followSelectedNodePath')
        taskMgr.add(self.stickToWidgetTask, 'stickToWidget')
        t = base.direct.widget.lerpPos(Point3(centerVec), CAM_MOVE_DURATION, other=base.direct.camera, blendType='easeInOut', task='moveToFitTask')
        t.setUponDeath(lambda state: taskMgr.remove('stickToWidget'))

    def stickToWidgetTask(self, state):
        base.direct.selected.moveWrtWidgetAll()
        return Task.cont

    def enableMouseFly(self, fKeyEvents = 1):
        base.disableMouse()
        for event in self.actionEvents:
            self.accept(event[0], event[1], extraArgs=event[2:])

        if fKeyEvents:
            for event in self.keyEvents:
                self.accept(event[0], event[1], extraArgs=event[2:])

        self.coaMarker.reparentTo(base.direct.group)

    def disableMouseFly(self):
        self.coaMarker.reparentTo(hidden)
        for event in self.actionEvents:
            self.ignore(event[0])

        for event in self.keyEvents:
            self.ignore(event[0])

        self.removeManipulateCameraTask()
        taskMgr.remove('stickToWidget')
        base.enableMouse()

    def removeManipulateCameraTask(self):
        taskMgr.remove('manipulateCamera')
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\directtools\DirectCameraControl.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:13:51 Pacific Daylight Time
