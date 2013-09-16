# 2013.08.22 22:13:52 Pacific Daylight Time
# Embedded file name: direct.directtools.DirectManipulation
from direct.showbase.DirectObject import DirectObject
from DirectGlobals import *
from DirectUtil import *
from DirectGeometry import *
from DirectSelection import SelectionRay
from direct.task import Task
import types

class DirectManipulationControl(DirectObject):
    __module__ = __name__

    def __init__(self):
        self.objectHandles = ObjectHandles()
        self.hitPt = Point3(0)
        self.prevHit = Vec3(0)
        self.hitPtScale = Point3(0)
        self.prevHitScale = Vec3(0)
        self.rotationCenter = Point3(0)
        self.initScaleMag = 1
        self.manipRef = base.direct.group.attachNewNode('manipRef')
        self.hitPtDist = 0
        self.constraint = None
        self.rotateAxis = 'x'
        self.lastCrankAngle = 0
        self.fSetCoa = 0
        self.fHitInit = 1
        self.fScaleInit = 1
        self.fScaleInit1 = 1
        self.fWidgetTop = 0
        self.fFreeManip = 1
        self.fScaling3D = 0
        self.fScaling1D = 0
        self.fMovable = 1
        self.mode = None
        self.actionEvents = [['DIRECT-mouse1', self.manipulationStart],
         ['DIRECT-mouse1Up', self.manipulationStop],
         ['tab', self.toggleObjectHandlesMode],
         ['DIRECT-widgetScaleUp', self.scaleWidget, 2.0],
         ['DIRECT-widgetScaleDown', self.scaleWidget, 0.5],
         ['shift-f', self.objectHandles.growToFit],
         ['i', self.plantSelectedNodePath]]
        self.defaultSkipFlags = SKIP_HIDDEN | SKIP_BACKFACE
        self.optionalSkipFlags = 0
        self.unmovableTagList = []
        self.fAllowSelectionOnly = 0
        self.fAllowMarquee = 0
        self.marquee = None
        self.fMultiView = 0
        self.fGridSnap = 0
        return

    def scaleWidget(self, factor):
        if hasattr(base.direct, 'widget'):
            base.direct.widget.multiplyScalingFactorBy(factor)
        else:
            self.objectHandles.multiplyScalingFactorBy(factor)

    def supportMultiView(self):
        if self.fMultiView:
            return
        self.objectHandles.hide(BitMask32.bit(0))
        self.objectHandles.hide(BitMask32.bit(1))
        self.objectHandles.hide(BitMask32.bit(2))
        self.topViewWidget = ObjectHandles('topViewWidget')
        self.frontViewWidget = ObjectHandles('frontViewWidget')
        self.leftViewWidget = ObjectHandles('leftViewWidget')
        self.widgetList = [self.topViewWidget,
         self.frontViewWidget,
         self.leftViewWidget,
         self.objectHandles]
        self.topViewWidget.hide(BitMask32.bit(1))
        self.topViewWidget.hide(BitMask32.bit(2))
        self.topViewWidget.hide(BitMask32.bit(3))
        self.frontViewWidget.hide(BitMask32.bit(0))
        self.frontViewWidget.hide(BitMask32.bit(2))
        self.frontViewWidget.hide(BitMask32.bit(3))
        self.leftViewWidget.hide(BitMask32.bit(0))
        self.leftViewWidget.hide(BitMask32.bit(1))
        self.leftViewWidget.hide(BitMask32.bit(3))
        self.fMultiView = 1

    def manipulationStart(self, modifiers):
        self.mode = 'select'
        if base.direct.cameraControl.useMayaCamControls and modifiers == 4:
            self.mode = 'camera'
        if self.fAllowSelectionOnly:
            return
        if self.fScaling1D == 0 and self.fScaling3D == 0:
            entry = base.direct.iRay.pickWidget(skipFlags=SKIP_WIDGET)
            if entry:
                self.hitPt.assign(entry.getSurfacePoint(entry.getFromNodePath()))
                self.hitPtDist = Vec3(self.hitPt).length()
                self.constraint = entry.getIntoNodePath().getName()
            else:
                self.constraint = None
                if base.direct.cameraControl.useMayaCamControls and not base.direct.gotControl(modifiers) and not self.fAllowMarquee:
                    return
        else:
            entry = None
        if not base.direct.gotAlt(modifiers):
            if entry:
                taskMgr.doMethodLater(MANIPULATION_MOVE_DELAY, self.switchToMoveMode, 'manip-move-wait')
                self.moveDir = None
                watchMouseTask = Task.Task(self.watchMouseTask)
                watchMouseTask.initX = base.direct.dr.mouseX
                watchMouseTask.initY = base.direct.dr.mouseY
                taskMgr.add(watchMouseTask, 'manip-watch-mouse')
            elif base.direct.fControl:
                self.mode = 'move'
                self.manipulateObject()
            elif not base.direct.fAlt and self.fAllowMarquee:
                self.moveDir = None
                watchMarqueeTask = Task.Task(self.watchMarqueeTask)
                watchMarqueeTask.initX = base.direct.dr.mouseX
                watchMarqueeTask.initY = base.direct.dr.mouseY
                taskMgr.add(watchMarqueeTask, 'manip-marquee-mouse')
        return

    def switchToMoveMode(self, state):
        taskMgr.remove('manip-watch-mouse')
        self.mode = 'move'
        self.manipulateObject()
        return Task.done

    def watchMouseTask(self, state):
        if abs(state.initX - base.direct.dr.mouseX) > 0.01 or abs(state.initY - base.direct.dr.mouseY) > 0.01:
            taskMgr.remove('manip-move-wait')
            self.mode = 'move'
            self.manipulateObject()
            return Task.done
        else:
            return Task.cont

    def watchMarqueeTask(self, state):
        taskMgr.remove('manip-watch-mouse')
        taskMgr.remove('manip-move-wait')
        self.mode = 'select'
        self.drawMarquee(state.initX, state.initY)
        return Task.cont

    def drawMarquee(self, startX, startY):
        if self.marquee:
            self.marquee.remove()
            self.marquee = None
        if base.direct.cameraControl.useMayaCamControls and base.direct.fAlt:
            return
        if base.direct.fControl:
            return
        endX = base.direct.dr.mouseX
        endY = base.direct.dr.mouseY
        if abs(endX - startX) < 0.01 and abs(endY - startY) < 0.01:
            return
        self.marquee = LineNodePath(render2d, 'marquee', 0.5, VBase4(0.8, 0.6, 0.6, 1))
        self.marqueeInfo = (startX,
         startY,
         endX,
         endY)
        self.marquee.drawLines([[(startX, 0, startY), (startX, 0, endY)],
         [(startX, 0, endY), (endX, 0, endY)],
         [(endX, 0, endY), (endX, 0, startY)],
         [(endX, 0, startY), (startX, 0, startY)]])
        self.marquee.create()
        if self.fMultiView:
            LE_showInOneCam(self.marquee, base.direct.camera.getName())
        return

    def manipulationStop(self):
        taskMgr.remove('manipulateObject')
        taskMgr.remove('manip-move-wait')
        taskMgr.remove('manip-watch-mouse')
        taskMgr.remove('manip-marquee-mouse')
        if self.mode == 'select':
            skipFlags = self.defaultSkipFlags | self.optionalSkipFlags
            skipFlags |= SKIP_CAMERA * (1 - base.getControl())
            if self.marquee:
                self.marquee.remove()
                self.marquee = None
                base.direct.deselectAll()
                startX = self.marqueeInfo[0]
                startY = self.marqueeInfo[1]
                endX = self.marqueeInfo[2]
                endY = self.marqueeInfo[3]
                fll = Point3(0, 0, 0)
                flr = Point3(0, 0, 0)
                fur = Point3(0, 0, 0)
                ful = Point3(0, 0, 0)
                nll = Point3(0, 0, 0)
                nlr = Point3(0, 0, 0)
                nur = Point3(0, 0, 0)
                nul = Point3(0, 0, 0)
                lens = base.direct.cam.node().getLens()
                lens.extrude((startX, startY), nul, ful)
                lens.extrude((endX, startY), nur, fur)
                lens.extrude((endX, endY), nlr, flr)
                lens.extrude((startX, endY), nll, fll)
                marqueeFrustum = BoundingHexahedron(fll, flr, fur, ful, nll, nlr, nur, nul)
                marqueeFrustum.xform(base.direct.cam.getNetTransform().getMat())
                base.marqueeFrustum = marqueeFrustum

                def findTaggedNodePath(nodePath):
                    for tag in base.direct.selected.tagList:
                        if nodePath.hasNetTag(tag):
                            nodePath = nodePath.findNetTag(tag)
                            return nodePath

                    return None

                selectionList = []
                for geom in render.findAllMatches('**/+GeomNode'):
                    if skipFlags & SKIP_HIDDEN and geom.isHidden():
                        continue
                    elif skipFlags & SKIP_CAMERA and camera in geom.getAncestors():
                        continue
                    elif skipFlags & SKIP_UNPICKABLE and geom.getName() in base.direct.iRay.unpickable:
                        continue
                    nodePath = findTaggedNodePath(geom)
                    if nodePath in selectionList:
                        continue
                    bb = geom.getBounds()
                    bbc = bb.makeCopy()
                    bbc.xform(geom.getParent().getNetTransform().getMat())
                    boundingSphereTest = marqueeFrustum.contains(bbc)
                    if boundingSphereTest > 1:
                        if boundingSphereTest == 7:
                            if nodePath not in selectionList:
                                selectionList.append(nodePath)
                        else:
                            tMat = Mat4(geom.getMat())
                            geom.clearMat()
                            min = Point3(0)
                            max = Point3(0)
                            geom.calcTightBounds(min, max)
                            geom.setMat(tMat)
                            fll = Point3(min[0], max[1], min[2])
                            flr = Point3(max[0], max[1], min[2])
                            fur = max
                            ful = Point3(min[0], max[1], max[2])
                            nll = min
                            nlr = Point3(max[0], min[1], min[2])
                            nur = Point3(max[0], min[1], max[2])
                            nul = Point3(min[0], min[1], max[2])
                            tbb = BoundingHexahedron(fll, flr, fur, ful, nll, nlr, nur, nul)
                            tbb.xform(geom.getNetTransform().getMat())
                            tightBoundTest = marqueeFrustum.contains(tbb)
                            if tightBoundTest > 1:
                                if nodePath not in selectionList:
                                    selectionList.append(nodePath)

                for nodePath in selectionList:
                    base.direct.select(nodePath, 1)

            else:
                entry = base.direct.iRay.pickGeom(skipFlags=skipFlags)
                if entry:
                    self.hitPt.assign(entry.getSurfacePoint(entry.getFromNodePath()))
                    self.hitPtDist = Vec3(self.hitPt).length()
                    base.direct.select(entry.getIntoNodePath(), base.direct.fShift)
                else:
                    base.direct.deselectAll()
        self.manipulateObjectCleanup()
        self.mode = None
        return

    def manipulateObjectCleanup(self):
        if self.fScaling3D or self.fScaling1D:
            if hasattr(base.direct, 'widget'):
                base.direct.widget.transferObjectHandlesScale()
            else:
                self.objectHandles.transferObjectHandlesScale()
            self.fScaling3D = 0
            self.fScaling1D = 0
        base.direct.selected.highlightAll()
        if hasattr(base.direct, 'widget'):
            base.direct.widget.showAllHandles()
        else:
            self.objectHandles.showAllHandles()
        if base.direct.clusterMode == 'client':
            cluster('base.direct.manipulationControl.objectHandles.showAllHandles()')
        if hasattr(base.direct, 'widget'):
            base.direct.widget.hideGuides()
        else:
            self.objectHandles.hideGuides()
        self.spawnFollowSelectedNodePathTask()
        messenger.send('DIRECT_manipulateObjectCleanup', [base.direct.selected.getSelectedAsList()])

    def spawnFollowSelectedNodePathTask(self):
        if not base.direct.selected.last:
            return
        taskMgr.remove('followSelectedNodePath')
        pos = VBase3(0)
        hpr = VBase3(0)
        decomposeMatrix(base.direct.selected.last.mCoa2Dnp, VBase3(0), hpr, pos, CSDefault)
        t = Task.Task(self.followSelectedNodePathTask)
        t.pos = pos
        t.hpr = hpr
        t.base = base.direct.selected.last
        taskMgr.add(t, 'followSelectedNodePath')

    def followSelectedNodePathTask(self, state):
        if hasattr(base.direct, 'manipulationControl') and base.direct.manipulationControl.fMultiView:
            for widget in base.direct.manipulationControl.widgetList:
                widget.setPosHpr(state.base, state.pos, state.hpr)

        else:
            base.direct.widget.setPosHpr(state.base, state.pos, state.hpr)
        return Task.cont

    def enableManipulation(self):
        for event in self.actionEvents:
            self.accept(event[0], event[1], extraArgs=event[2:])

        self.fAllowSelectionOnly = 0

    def disableManipulation(self, allowSelectionOnly = False):
        for event in self.actionEvents:
            self.ignore(event[0])

        if allowSelectionOnly:
            self.fAllowSelectionOnly = allowSelectionOnly
            self.accept('DIRECT-mouse1', self.manipulationStart)
            self.accept('DIRECT-mouse1Up', self.manipulationStop)
        self.removeManipulateObjectTask()
        taskMgr.remove('manipulateObject')
        taskMgr.remove('manip-move-wait')
        taskMgr.remove('manip-watch-mouse')
        taskMgr.remove('highlightWidgetTask')
        taskMgr.remove('resizeObjectHandles')

    def toggleObjectHandlesMode(self):
        if self.fMovable:
            self.fSetCoa = 1 - self.fSetCoa
            if self.fSetCoa:
                if hasattr(base.direct, 'widget'):
                    base.direct.widget.coaModeColor()
                else:
                    self.objectHandles.coaModeColor()
            elif hasattr(base.direct, 'widget'):
                base.direct.widget.manipModeColor()
            else:
                self.objectHandles.manipModeColor()
        elif hasattr(base.direct, 'widget'):
            base.direct.widget.disabledModeColor()
        else:
            self.objectHandles.disabledModeColor()

    def removeManipulateObjectTask(self):
        taskMgr.remove('manipulateObject')

    def enableWidgetMove(self):
        self.fMovable = 1
        if self.fSetCoa:
            if hasattr(base.direct, 'widget'):
                base.direct.widget.coaModeColor()
            else:
                self.objectHandles.coaModeColor()
        elif hasattr(base.direct, 'widget'):
            base.direct.widget.manipModeColor()
        else:
            self.objectHandles.manipModeColor()

    def disableWidgetMove(self):
        self.fMovable = 0
        if hasattr(base.direct, 'widget'):
            base.direct.widget.disabledModeColor()
        else:
            self.objectHandles.disabledModeColor()

    def getEditTypes(self, objects):
        editTypes = 0
        for tag in self.unmovableTagList:
            for selected in objects:
                unmovableTag = selected.getTag(tag)
                if unmovableTag:
                    editTypes |= int(unmovableTag)

        return editTypes

    def manipulateObject(self):
        selectedList = base.direct.selected.getSelectedAsList()
        editTypes = self.getEditTypes(selectedList)
        if editTypes & EDIT_TYPE_UNEDITABLE == EDIT_TYPE_UNEDITABLE:
            return
        self.currEditTypes = editTypes
        if selectedList:
            taskMgr.remove('followSelectedNodePath')
            taskMgr.remove('highlightWidgetTask')
            self.fManip = 1
            base.direct.pushUndo(base.direct.selected)
            if hasattr(base.direct, 'widget'):
                base.direct.widget.showGuides()
                base.direct.widget.hideAllHandles()
                base.direct.widget.showHandle(self.constraint)
            else:
                self.objectHandles.showGuides()
                self.objectHandles.hideAllHandles()
                self.objectHandles.showHandle(self.constraint)
            if base.direct.clusterMode == 'client':
                oh = 'base.direct.manipulationControl.objectHandles'
                cluster(oh + '.showGuides()', 0)
                cluster(oh + '.hideAllHandles()', 0)
                cluster(oh + '.showHandle("%s")' % self.constraint, 0)
            base.direct.selected.getWrtAll()
            base.direct.selected.dehighlightAll()
            messenger.send('DIRECT_manipulateObjectStart')
            self.spawnManipulateObjectTask()

    def spawnManipulateObjectTask(self):
        self.fHitInit = 1
        self.fScaleInit = 1
        if not self.fScaling1D and not self.fScaling3D:
            self.fScaleInit1 = 1
        t = Task.Task(self.manipulateObjectTask)
        t.fMouseX = abs(base.direct.dr.mouseX) > 0.9
        t.fMouseY = abs(base.direct.dr.mouseY) > 0.9
        if t.fMouseX:
            t.constrainedDir = 'y'
        else:
            t.constrainedDir = 'x'
        t.coaCenter = getScreenXY(base.direct.widget)
        if t.fMouseX and t.fMouseY:
            t.lastAngle = getCrankAngle(t.coaCenter)
        taskMgr.add(t, 'manipulateObject')

    def manipulateObjectTask(self, state):
        if self.fScaling1D:
            self.scale1D(state)
        elif self.fScaling3D:
            self.scale3D(state)
        elif self.constraint:
            type = self.constraint[2:]
            if base.direct.fControl and not self.currEditTypes & EDIT_TYPE_UNSCALABLE:
                if type == 'post':
                    self.fScaling1D = 1
                    self.scale1D(state)
                else:
                    self.fScaling3D = 1
                    self.scale3D(state)
            elif type == 'post' and not self.currEditTypes & EDIT_TYPE_UNMOVABLE:
                self.xlate1D(state)
            elif type == 'disc' and not self.currEditTypes & EDIT_TYPE_UNMOVABLE:
                self.xlate2D(state)
            elif type == 'ring' and not self.currEditTypes & EDIT_TYPE_UNROTATABLE:
                self.rotate1D(state)
        elif self.fFreeManip:
            if 0 and (self.fScaling1D or self.fScaling3D) and not base.direct.fAlt:
                if hasattr(base.direct, 'widget'):
                    base.direct.widget.transferObjectHandleScale()
                else:
                    self.objectHandles.transferObjectHandlesScale()
                self.fScaling1D = 0
                self.fScaling3D = 0
            if base.direct.fControl and not self.currEditTypes & EDIT_TYPE_UNSCALABLE:
                self.fScaling3D = 1
                self.scale3D(state)
            elif state.fMouseX and state.fMouseY and not self.currEditTypes & EDIT_TYPE_UNROTATABLE:
                self.rotateAboutViewVector(state)
            elif state.fMouseX or state.fMouseY and not self.currEditTypes & EDIT_TYPE_UNMOVABLE:
                self.rotate2D(state)
            elif not self.currEditTypes & EDIT_TYPE_UNMOVABLE:
                if base.direct.fShift or base.direct.fControl:
                    self.xlateCamXY(state)
                else:
                    self.xlateCamXZ(state)
        if self.fSetCoa:
            base.direct.selected.last.mCoa2Dnp.assign(base.direct.widget.getMat(base.direct.selected.last))
        else:
            base.direct.selected.moveWrtWidgetAll()
        return Task.cont

    def addTag(self, tag):
        if tag not in self.unmovableTagList:
            self.unmovableTagList.append(tag)

    def removeTag(self, tag):
        self.unmovableTagList.remove(tag)

    def gridSnapping(self, nodePath, offset):
        offsetX = nodePath.getX() + offset.getX()
        offsetY = nodePath.getY() + offset.getY()
        offsetZ = nodePath.getZ() + offset.getZ()
        if offsetX < 0.0:
            signX = -1.0
        else:
            signX = 1.0
        modX = math.fabs(offsetX) % base.direct.grid.gridSpacing
        floorX = math.floor(math.fabs(offsetX) / base.direct.grid.gridSpacing)
        if modX < base.direct.grid.gridSpacing / 2.0:
            offsetX = signX * floorX * base.direct.grid.gridSpacing
        else:
            offsetX = signX * (floorX + 1) * base.direct.grid.gridSpacing
        if offsetY < 0.0:
            signY = -1.0
        else:
            signY = 1.0
        modY = math.fabs(offsetY) % base.direct.grid.gridSpacing
        floorY = math.floor(math.fabs(offsetY) / base.direct.grid.gridSpacing)
        if modY < base.direct.grid.gridSpacing / 2.0:
            offsetY = signY * floorY * base.direct.grid.gridSpacing
        else:
            offsetY = signY * (floorY + 1) * base.direct.grid.gridSpacing
        if offsetZ < 0.0:
            signZ = -1.0
        else:
            signZ = 1.0
        modZ = math.fabs(offsetZ) % base.direct.grid.gridSpacing
        floorZ = math.floor(math.fabs(offsetZ) / base.direct.grid.gridSpacing)
        if modZ < base.direct.grid.gridSpacing / 2.0:
            offsetZ = signZ * floorZ * base.direct.grid.gridSpacing
        else:
            offsetZ = signZ * (floorZ + 1) * base.direct.grid.gridSpacing
        return Point3(offsetX, offsetY, offsetZ)

    def xlate1D(self, state):
        self.hitPt.assign(self.objectHandles.getAxisIntersectPt(self.constraint[:1]))
        if self.fHitInit:
            self.fHitInit = 0
            self.prevHit.assign(self.hitPt)
        else:
            offset = self.hitPt - self.prevHit
            if hasattr(base.direct, 'manipulationControl') and base.direct.manipulationControl.fMultiView:
                for widget in base.direct.manipulationControl.widgetList:
                    if self.fGridSnap:
                        widget.setPos(self.gridSnapping(widget, offset))
                    else:
                        widget.setPos(widget, offset)

                if base.direct.camera.getName() != 'persp':
                    self.prevHit.assign(self.hitPt)
            elif self.fGridSnap:
                base.direct.widget.setPos(self.gridSnapping(base.direct.widget, offset))
            else:
                base.direct.widget.setPos(base.direct.widget, offset)

    def xlate2D(self, state):
        self.hitPt.assign(self.objectHandles.getWidgetIntersectPt(base.direct.widget, self.constraint[:1]))
        if self.fHitInit:
            self.fHitInit = 0
            self.prevHit.assign(self.hitPt)
        else:
            offset = self.hitPt - self.prevHit
            if hasattr(base.direct, 'manipulationControl') and base.direct.manipulationControl.fMultiView:
                for widget in base.direct.manipulationControl.widgetList:
                    if self.fGridSnap:
                        widget.setPos(self.gridSnapping(widget, offset))
                    else:
                        widget.setPos(widget, offset)

                if base.direct.camera.getName() != 'persp':
                    self.prevHit.assign(self.hitPt)
            elif self.fGridSnap:
                base.direct.widget.setPos(self.gridSnapping(base.direct.widget, offset))
            else:
                base.direct.widget.setPos(base.direct.widget, offset)

    def rotate1D(self, state):
        if self.fHitInit:
            self.fHitInit = 0
            self.rotateAxis = self.constraint[:1]
            self.fWidgetTop = self.widgetCheck('top?')
            self.rotationCenter = getScreenXY(base.direct.widget)
            self.lastCrankAngle = getCrankAngle(self.rotationCenter)
        newAngle = getCrankAngle(self.rotationCenter)
        deltaAngle = self.lastCrankAngle - newAngle
        if self.fWidgetTop:
            deltaAngle = -1 * deltaAngle
        if self.rotateAxis == 'x':
            if hasattr(base.direct, 'manipulationControl') and base.direct.manipulationControl.fMultiView:
                for widget in base.direct.manipulationControl.widgetList:
                    widget.setP(widget, deltaAngle)

            else:
                base.direct.widget.setP(base.direct.widget, deltaAngle)
        elif self.rotateAxis == 'y':
            if hasattr(base.direct, 'manipulationControl') and base.direct.manipulationControl.fMultiView:
                for widget in base.direct.manipulationControl.widgetList:
                    widget.setR(widget, deltaAngle)

            else:
                base.direct.widget.setR(base.direct.widget, deltaAngle)
        elif self.rotateAxis == 'z':
            if hasattr(base.direct, 'manipulationControl') and base.direct.manipulationControl.fMultiView:
                for widget in base.direct.manipulationControl.widgetList:
                    widget.setH(widget, deltaAngle)

            else:
                base.direct.widget.setH(base.direct.widget, deltaAngle)
        self.lastCrankAngle = newAngle

    def widgetCheck(self, type):
        axis = self.constraint[:1]
        mWidget2Cam = base.direct.widget.getMat(base.direct.camera)
        pos = VBase3(0)
        decomposeMatrix(mWidget2Cam, VBase3(0), VBase3(0), pos, CSDefault)
        widgetDir = Vec3(pos)
        widgetDir.normalize()
        if axis == 'x':
            widgetAxis = Vec3(mWidget2Cam.xformVec(X_AXIS))
        elif axis == 'y':
            widgetAxis = Vec3(mWidget2Cam.xformVec(Y_AXIS))
        elif axis == 'z':
            widgetAxis = Vec3(mWidget2Cam.xformVec(Z_AXIS))
        widgetAxis.normalize()
        if type == 'top?':
            return widgetDir.dot(widgetAxis) < 0.0
        elif type == 'edge?':
            return abs(widgetDir.dot(widgetAxis)) < 0.2

    def xlateCamXZ(self, state):
        self.fHitInit = 1
        self.fScaleInit = 1
        vWidget2Camera = base.direct.widget.getPos(base.direct.camera)
        x = vWidget2Camera[0]
        y = vWidget2Camera[1]
        z = vWidget2Camera[2]
        dr = base.direct.dr
        base.direct.widget.setX(base.direct.camera, x + 0.5 * dr.mouseDeltaX * dr.nearWidth * (y / dr.near))
        base.direct.widget.setZ(base.direct.camera, z + 0.5 * dr.mouseDeltaY * dr.nearHeight * (y / dr.near))

    def xlateCamXY(self, state):
        self.fScaleInit = 1
        vWidget2Camera = base.direct.widget.getPos(base.direct.camera)
        if self.fHitInit:
            self.fHitInit = 0
            self.xlateSF = Vec3(vWidget2Camera).length()
            coaCenter = getNearProjectionPoint(base.direct.widget)
            self.deltaNearX = coaCenter[0] - base.direct.dr.nearVec[0]
        if base.direct.fControl:
            moveDir = Vec3(vWidget2Camera)
            if moveDir[1] < 0.0:
                moveDir.assign(moveDir * -1)
            moveDir.normalize()
        else:
            moveDir = Vec3(Y_AXIS)
        dr = base.direct.dr
        moveDir.assign(moveDir * (2.0 * dr.mouseDeltaY * self.xlateSF))
        vWidget2Camera += moveDir
        vWidget2Camera.setX((dr.nearVec[0] + self.deltaNearX) * (vWidget2Camera[1] / dr.near))
        base.direct.widget.setPos(base.direct.camera, vWidget2Camera)

    def rotate2D(self, state):
        self.fHitInit = 1
        self.fScaleInit = 1
        tumbleRate = 360
        if state.constrainedDir == 'y' and abs(base.direct.dr.mouseX) > 0.9:
            deltaX = 0
            deltaY = base.direct.dr.mouseDeltaY
        elif state.constrainedDir == 'x' and abs(base.direct.dr.mouseY) > 0.9:
            deltaX = base.direct.dr.mouseDeltaX
            deltaY = 0
        else:
            deltaX = base.direct.dr.mouseDeltaX
            deltaY = base.direct.dr.mouseDeltaY
        relHpr(base.direct.widget, base.direct.camera, deltaX * tumbleRate, -deltaY * tumbleRate, 0)

    def rotateAboutViewVector(self, state):
        self.fHitInit = 1
        self.fScaleInit = 1
        angle = getCrankAngle(state.coaCenter)
        deltaAngle = angle - state.lastAngle
        state.lastAngle = angle
        relHpr(base.direct.widget, base.direct.camera, 0, 0, -deltaAngle)

    def scale1D(self, state):
        print self.constraint
        if hasattr(base.direct, 'manipulationControl') and base.direct.manipulationControl.fMultiView:
            self.hitPtScale.assign(self.objectHandles.getMouseIntersectPt())
            if self.fScaleInit1:
                self.fScaleInit1 = 0
                self.prevHitScale.assign(self.hitPtScale)
            else:
                widgetPos = base.direct.widget.getPos()
                d0 = (self.prevHitScale - widgetPos).length()
                d1 = (self.hitPtScale - widgetPos).length()
                offset = d1 - d0
                currScale = base.direct.widget.getScale()
                if self.constraint[:1] == 'x':
                    currScale = Vec3(currScale.getX() + offset, currScale.getY(), currScale.getZ())
                    if currScale.getX() < 0.0:
                        currScale.setX(0.01)
                elif self.constraint[:1] == 'y':
                    currScale = Vec3(currScale.getX(), currScale.getY() + offset, currScale.getZ())
                    if currScale.getY() < 0.0:
                        currScale.setY(0.01)
                elif self.constraint[:1] == 'z':
                    currScale = Vec3(currScale.getX(), currScale.getY(), currScale.getZ() + offset)
                    if currScale.getZ() < 0.0:
                        currScale.setZ(0.01)
                base.direct.widget.setScale(currScale)
                self.prevHitScale.assign(self.hitPtScale)
            return
        if self.fScaleInit:
            self.fScaleInit = 0
            self.initScaleMag = Vec3(self.objectHandles.getAxisIntersectPt(self.constraint[:1])).length()
            self.initScale = base.direct.widget.getScale()
        self.fHitInit = 1
        base.direct.widget.setScale(1, 1, 1)
        if self.constraint[:1] == 'x':
            currScale = Vec3(self.initScale.getX() * self.objectHandles.getAxisIntersectPt('x').length() / self.initScaleMag, self.initScale.getY(), self.initScale.getZ())
        elif self.constraint[:1] == 'y':
            currScale = Vec3(self.initScale.getX(), self.initScale.getY() * self.objectHandles.getAxisIntersectPt('y').length() / self.initScaleMag, self.initScale.getZ())
        elif self.constraint[:1] == 'z':
            currScale = Vec3(self.initScale.getX(), self.initScale.getY(), self.initScale.getZ() * self.objectHandles.getAxisIntersectPt('z').length() / self.initScaleMag)
        base.direct.widget.setScale(currScale)

    def scale3D(self, state):
        if hasattr(base.direct, 'manipulationControl') and base.direct.manipulationControl.fMultiView:
            self.hitPtScale.assign(self.objectHandles.getMouseIntersectPt())
            if self.fScaleInit1:
                self.fScaleInit1 = 0
                self.prevHitScale.assign(self.hitPtScale)
            else:
                widgetPos = base.direct.widget.getPos()
                d0 = (self.prevHitScale - widgetPos).length()
                d1 = (self.hitPtScale - widgetPos).length()
                offset = d1 - d0
                currScale = base.direct.widget.getScale()
                currScale += offset
                if currScale.getX() < 0.0 and currScale.getY() < 0.0 and currScale.getZ() < 0.0:
                    currScale = VBase3(0.01, 0.01, 0.01)
                base.direct.widget.setScale(currScale)
                self.prevHitScale.assign(self.hitPtScale)
            return
        if self.fScaleInit:
            self.fScaleInit = 0
            self.manipRef.setPos(base.direct.widget, 0, 0, 0)
            self.manipRef.setHpr(base.direct.camera, 0, 0, 0)
            self.initScaleMag = Vec3(self.objectHandles.getWidgetIntersectPt(self.manipRef, 'y')).length()
            self.initScale = base.direct.widget.getScale()
        self.fHitInit = 1
        currScale = self.initScale * (self.objectHandles.getWidgetIntersectPt(self.manipRef, 'y').length() / self.initScaleMag)
        base.direct.widget.setScale(currScale)

    def plantSelectedNodePath(self):
        entry = base.direct.iRay.pickGeom(skipFlags=SKIP_HIDDEN | SKIP_BACKFACE | SKIP_CAMERA)
        if entry != None and base.direct.selected.last != None:
            base.direct.pushUndo(base.direct.selected)
            base.direct.selected.getWrtAll()
            base.direct.widget.setPos(base.direct.camera, entry.getSurfacePoint(entry.getFromNodePath()))
            base.direct.selected.moveWrtWidgetAll()
            messenger.send('DIRECT_manipulateObjectCleanup', [base.direct.selected.getSelectedAsList()])
        return


class ObjectHandles(NodePath, DirectObject):
    __module__ = __name__

    def __init__(self, name = 'objectHandles'):
        NodePath.__init__(self)
        self.assign(loader.loadModel('models/misc/objectHandles'))
        self.setName(name)
        self.scalingNode = self.getChild(0)
        self.scalingNode.setName('ohScalingNode')
        self.ohScalingFactor = 1.0
        self.directScalingFactor = 1.0
        self.hitPt = Vec3(0)
        self.xHandles = self.find('**/X')
        self.xPostGroup = self.xHandles.find('**/x-post-group')
        self.xPostCollision = self.xHandles.find('**/x-post')
        self.xRingGroup = self.xHandles.find('**/x-ring-group')
        self.xRingCollision = self.xHandles.find('**/x-ring')
        self.xDiscGroup = self.xHandles.find('**/x-disc-group')
        self.xDisc = self.xHandles.find('**/x-disc-visible')
        self.xDiscCollision = self.xHandles.find('**/x-disc')
        self.yHandles = self.find('**/Y')
        self.yPostGroup = self.yHandles.find('**/y-post-group')
        self.yPostCollision = self.yHandles.find('**/y-post')
        self.yRingGroup = self.yHandles.find('**/y-ring-group')
        self.yRingCollision = self.yHandles.find('**/y-ring')
        self.yDiscGroup = self.yHandles.find('**/y-disc-group')
        self.yDisc = self.yHandles.find('**/y-disc-visible')
        self.yDiscCollision = self.yHandles.find('**/y-disc')
        self.zHandles = self.find('**/Z')
        self.zPostGroup = self.zHandles.find('**/z-post-group')
        self.zPostCollision = self.zHandles.find('**/z-post')
        self.zRingGroup = self.zHandles.find('**/z-ring-group')
        self.zRingCollision = self.zHandles.find('**/z-ring')
        self.zDiscGroup = self.zHandles.find('**/z-disc-group')
        self.zDisc = self.zHandles.find('**/z-disc-visible')
        self.zDiscCollision = self.zHandles.find('**/z-disc')
        self.xPostCollision.hide()
        self.xRingCollision.hide()
        self.xDisc.setColor(1, 0, 0, 0.2)
        self.yPostCollision.hide()
        self.yRingCollision.hide()
        self.yDisc.setColor(0, 1, 0, 0.2)
        self.zPostCollision.hide()
        self.zRingCollision.hide()
        self.zDisc.setColor(0, 0, 1, 0.2)
        self.createObjectHandleLines()
        self.createGuideLines()
        self.hideGuides()
        self.xPostCollision.setTag('WidgetName', name)
        self.yPostCollision.setTag('WidgetName', name)
        self.zPostCollision.setTag('WidgetName', name)
        self.xRingCollision.setTag('WidgetName', name)
        self.yRingCollision.setTag('WidgetName', name)
        self.zRingCollision.setTag('WidgetName', name)
        self.xDiscCollision.setTag('WidgetName', name)
        self.yDiscCollision.setTag('WidgetName', name)
        self.zDiscCollision.setTag('WidgetName', name)
        self.xDisc.find('**/+GeomNode').setName('x-disc-geom')
        self.yDisc.find('**/+GeomNode').setName('y-disc-geom')
        self.zDisc.find('**/+GeomNode').setName('z-disc-geom')
        self.fActive = 1
        self.toggleWidget()
        useDirectRenderStyle(self)

    def coaModeColor(self):
        self.setColor(0.5, 0.5, 0.5, 0.5, 1)

    def disabledModeColor(self):
        self.setColor(0.1, 0.1, 0.1, 0.1, 1)

    def manipModeColor(self):
        self.clearColor()

    def toggleWidget(self):
        if self.fActive:
            if hasattr(base.direct, 'manipulationControl') and base.direct.manipulationControl.fMultiView:
                for widget in base.direct.manipulationControl.widgetList:
                    widget.deactivate()

            else:
                self.deactivate()
        elif hasattr(base.direct, 'manipulationControl') and base.direct.manipulationControl.fMultiView:
            for widget in base.direct.manipulationControl.widgetList:
                widget.activate()
                widget.showWidgetIfActive()

        else:
            self.activate()

    def activate(self):
        self.scalingNode.reparentTo(self)
        self.fActive = 1

    def deactivate(self):
        self.scalingNode.reparentTo(hidden)
        self.fActive = 0

    def showWidgetIfActive(self):
        if self.fActive:
            self.reparentTo(base.direct.group)

    def showWidget(self):
        self.reparentTo(base.direct.group)

    def hideWidget(self):
        self.reparentTo(hidden)

    def enableHandles(self, handles):
        if type(handles) == types.ListType:
            for handle in handles:
                self.enableHandle(handle)

        elif handles == 'x':
            self.enableHandles(['x-post', 'x-ring', 'x-disc'])
        elif handles == 'y':
            self.enableHandles(['y-post', 'y-ring', 'y-disc'])
        elif handles == 'z':
            self.enableHandles(['z-post', 'z-ring', 'z-disc'])
        elif handles == 'post':
            self.enableHandles(['x-post', 'y-post', 'z-post'])
        elif handles == 'ring':
            self.enableHandles(['x-ring', 'y-ring', 'z-ring'])
        elif handles == 'disc':
            self.enableHandles(['x-disc', 'y-disc', 'z-disc'])
        elif handles == 'all':
            self.enableHandles(['x-post',
             'x-ring',
             'x-disc',
             'y-post',
             'y-ring',
             'y-disc',
             'z-post',
             'z-ring',
             'z-disc'])

    def enableHandle(self, handle):
        if handle == 'x-post':
            self.xPostGroup.reparentTo(self.xHandles)
        elif handle == 'x-ring':
            self.xRingGroup.reparentTo(self.xHandles)
        elif handle == 'x-disc':
            self.xDiscGroup.reparentTo(self.xHandles)
        if handle == 'y-post':
            self.yPostGroup.reparentTo(self.yHandles)
        elif handle == 'y-ring':
            self.yRingGroup.reparentTo(self.yHandles)
        elif handle == 'y-disc':
            self.yDiscGroup.reparentTo(self.yHandles)
        if handle == 'z-post':
            self.zPostGroup.reparentTo(self.zHandles)
        elif handle == 'z-ring':
            self.zRingGroup.reparentTo(self.zHandles)
        elif handle == 'z-disc':
            self.zDiscGroup.reparentTo(self.zHandles)

    def disableHandles(self, handles):
        if type(handles) == types.ListType:
            for handle in handles:
                self.disableHandle(handle)

        elif handles == 'x':
            self.disableHandles(['x-post', 'x-ring', 'x-disc'])
        elif handles == 'y':
            self.disableHandles(['y-post', 'y-ring', 'y-disc'])
        elif handles == 'z':
            self.disableHandles(['z-post', 'z-ring', 'z-disc'])
        elif handles == 'post':
            self.disableHandles(['x-post', 'y-post', 'z-post'])
        elif handles == 'ring':
            self.disableHandles(['x-ring', 'y-ring', 'z-ring'])
        elif handles == 'disc':
            self.disableHandles(['x-disc', 'y-disc', 'z-disc'])
        elif handles == 'all':
            self.disableHandles(['x-post',
             'x-ring',
             'x-disc',
             'y-post',
             'y-ring',
             'y-disc',
             'z-post',
             'z-ring',
             'z-disc'])

    def disableHandle(self, handle):
        if handle == 'x-post':
            self.xPostGroup.reparentTo(hidden)
        elif handle == 'x-ring':
            self.xRingGroup.reparentTo(hidden)
        elif handle == 'x-disc':
            self.xDiscGroup.reparentTo(hidden)
        if handle == 'y-post':
            self.yPostGroup.reparentTo(hidden)
        elif handle == 'y-ring':
            self.yRingGroup.reparentTo(hidden)
        elif handle == 'y-disc':
            self.yDiscGroup.reparentTo(hidden)
        if handle == 'z-post':
            self.zPostGroup.reparentTo(hidden)
        elif handle == 'z-ring':
            self.zRingGroup.reparentTo(hidden)
        elif handle == 'z-disc':
            self.zDiscGroup.reparentTo(hidden)

    def showAllHandles(self):
        self.xPost.show()
        self.xRing.show()
        self.xDisc.show()
        self.yPost.show()
        self.yRing.show()
        self.yDisc.show()
        self.zPost.show()
        self.zRing.show()
        self.zDisc.show()

    def hideAllHandles(self):
        self.xPost.hide()
        self.xRing.hide()
        self.xDisc.hide()
        self.yPost.hide()
        self.yRing.hide()
        self.yDisc.hide()
        self.zPost.hide()
        self.zRing.hide()
        self.zDisc.hide()

    def showHandle(self, handle):
        if handle == 'x-post':
            self.xPost.show()
        elif handle == 'x-ring':
            self.xRing.show()
        elif handle == 'x-disc':
            self.xDisc.show()
        elif handle == 'y-post':
            self.yPost.show()
        elif handle == 'y-ring':
            self.yRing.show()
        elif handle == 'y-disc':
            self.yDisc.show()
        elif handle == 'z-post':
            self.zPost.show()
        elif handle == 'z-ring':
            self.zRing.show()
        elif handle == 'z-disc':
            self.zDisc.show()

    def showGuides(self):
        self.guideLines.show()

    def hideGuides(self):
        self.guideLines.hide()

    def setDirectScalingFactor(self, factor):
        self.directScalingFactor = factor
        self.setScalingFactor(1)

    def setScalingFactor(self, scaleFactor):
        self.ohScalingFactor = self.ohScalingFactor * scaleFactor
        self.scalingNode.setScale(self.ohScalingFactor * self.directScalingFactor)

    def getScalingFactor(self):
        return self.scalingNode.getScale()

    def transferObjectHandlesScale(self):
        ohs = self.getScale()
        sns = self.scalingNode.getScale()
        self.scalingNode.setScale(ohs[0] * sns[0], ohs[1] * sns[1], ohs[2] * sns[2])
        self.setScale(1)

    def multiplyScalingFactorBy(self, factor):
        taskMgr.remove('resizeObjectHandles')
        self.ohScalingFactor = self.ohScalingFactor * factor
        sf = self.ohScalingFactor * self.directScalingFactor
        self.scalingNode.lerpScale(sf, sf, sf, 0.5, blendType='easeInOut', task='resizeObjectHandles')

    def growToFit(self):
        taskMgr.remove('resizeObjectHandles')
        pos = base.direct.widget.getPos(base.direct.camera)
        minDim = min(base.direct.dr.nearWidth, base.direct.dr.nearHeight)
        sf = 0.15 * minDim * (pos[1] / base.direct.dr.near)
        self.ohScalingFactor = sf
        sf = sf * self.directScalingFactor
        self.scalingNode.lerpScale(sf, sf, sf, 0.5, blendType='easeInOut', task='resizeObjectHandles')

    def createObjectHandleLines(self):
        self.xPost = self.xPostGroup.attachNewNode('x-post-visible')
        lines = LineNodePath(self.xPost)
        lines.setColor(VBase4(1, 0, 0, 1))
        lines.setThickness(5)
        lines.moveTo(1.5, 0, 0)
        lines.drawTo(-1.5, 0, 0)
        arrowInfo0 = 1.3
        arrowInfo1 = 0.1
        lines.moveTo(1.5, 0, 0)
        lines.drawTo(arrowInfo0, arrowInfo1, arrowInfo1)
        lines.moveTo(1.5, 0, 0)
        lines.drawTo(arrowInfo0, arrowInfo1, -1 * arrowInfo1)
        lines.moveTo(1.5, 0, 0)
        lines.drawTo(arrowInfo0, -1 * arrowInfo1, arrowInfo1)
        lines.moveTo(1.5, 0, 0)
        lines.drawTo(arrowInfo0, -1 * arrowInfo1, -1 * arrowInfo1)
        lines.create()
        lines.setName('x-post-line')
        self.xRing = self.xRingGroup.attachNewNode('x-ring-visible')
        lines = LineNodePath(self.xRing)
        lines.setColor(VBase4(1, 0, 0, 1))
        lines.setThickness(3)
        lines.moveTo(0, 1, 0)
        for ang in range(15, 370, 15):
            lines.drawTo(0, math.cos(deg2Rad(ang)), math.sin(deg2Rad(ang)))

        lines.create()
        lines.setName('x-ring-line')
        self.yPost = self.yPostGroup.attachNewNode('y-post-visible')
        lines = LineNodePath(self.yPost)
        lines.setColor(VBase4(0, 1, 0, 1))
        lines.setThickness(5)
        lines.moveTo(0, 1.5, 0)
        lines.drawTo(0, -1.5, 0)
        lines.moveTo(0, 1.5, 0)
        lines.drawTo(arrowInfo1, arrowInfo0, arrowInfo1)
        lines.moveTo(0, 1.5, 0)
        lines.drawTo(arrowInfo1, arrowInfo0, -1 * arrowInfo1)
        lines.moveTo(0, 1.5, 0)
        lines.drawTo(-1 * arrowInfo1, arrowInfo0, arrowInfo1)
        lines.moveTo(0, 1.5, 0)
        lines.drawTo(-1 * arrowInfo1, arrowInfo0, -1 * arrowInfo1)
        lines.create()
        lines.setName('y-post-line')
        self.yRing = self.yRingGroup.attachNewNode('y-ring-visible')
        lines = LineNodePath(self.yRing)
        lines.setColor(VBase4(0, 1, 0, 1))
        lines.setThickness(3)
        lines.moveTo(1, 0, 0)
        for ang in range(15, 370, 15):
            lines.drawTo(math.cos(deg2Rad(ang)), 0, math.sin(deg2Rad(ang)))

        lines.create()
        lines.setName('y-ring-line')
        self.zPost = self.zPostGroup.attachNewNode('z-post-visible')
        lines = LineNodePath(self.zPost)
        lines.setColor(VBase4(0, 0, 1, 1))
        lines.setThickness(5)
        lines.moveTo(0, 0, 1.5)
        lines.drawTo(0, 0, -1.5)
        lines.moveTo(0, 0, 1.5)
        lines.drawTo(arrowInfo1, arrowInfo1, arrowInfo0)
        lines.moveTo(0, 0, 1.5)
        lines.drawTo(arrowInfo1, -1 * arrowInfo1, arrowInfo0)
        lines.moveTo(0, 0, 1.5)
        lines.drawTo(-1 * arrowInfo1, arrowInfo1, arrowInfo0)
        lines.moveTo(0, 0, 1.5)
        lines.drawTo(-1 * arrowInfo1, -1 * arrowInfo1, arrowInfo0)
        lines.create()
        lines.setName('z-post-line')
        self.zRing = self.zRingGroup.attachNewNode('z-ring-visible')
        lines = LineNodePath(self.zRing)
        lines.setColor(VBase4(0, 0, 1, 1))
        lines.setThickness(3)
        lines.moveTo(1, 0, 0)
        for ang in range(15, 370, 15):
            lines.drawTo(math.cos(deg2Rad(ang)), math.sin(deg2Rad(ang)), 0)

        lines.create()
        lines.setName('z-ring-line')

    def createGuideLines(self):
        self.guideLines = self.attachNewNode('guideLines')
        lines = LineNodePath(self.guideLines)
        lines.setColor(VBase4(1, 0, 0, 1))
        lines.setThickness(0.5)
        lines.moveTo(-500, 0, 0)
        lines.drawTo(500, 0, 0)
        lines.create()
        lines.setName('x-guide')
        lines = LineNodePath(self.guideLines)
        lines.setColor(VBase4(0, 1, 0, 1))
        lines.setThickness(0.5)
        lines.moveTo(0, -500, 0)
        lines.drawTo(0, 500, 0)
        lines.create()
        lines.setName('y-guide')
        lines = LineNodePath(self.guideLines)
        lines.setColor(VBase4(0, 0, 1, 1))
        lines.setThickness(0.5)
        lines.moveTo(0, 0, -500)
        lines.drawTo(0, 0, 500)
        lines.create()
        lines.setName('z-guide')

    def getAxisIntersectPt(self, axis):
        if hasattr(base.direct, 'manipulationControl') and base.direct.manipulationControl.fMultiView and base.direct.camera.getName() != 'persp':
            iRay = SelectionRay(base.direct.camera)
            iRay.collider.setFromLens(base.direct.camNode, base.direct.dr.mouseX, base.direct.dr.mouseY)
            iRay.collideWithBitMask(BitMask32.bit(21))
            iRay.ct.traverse(base.direct.grid)
            if iRay.getNumEntries() == 0:
                del iRay
                return self.hitPt
            entry = iRay.getEntry(0)
            hitPt = entry.getSurfacePoint(entry.getFromNodePath())
            np = NodePath('temp')
            np.setPos(base.direct.camera, hitPt)
            self.hitPt.assign(np.getPos())
            np.remove()
            del iRay
            if axis == 'x':
                self.hitPt.setY(0)
                self.hitPt.setZ(0)
            elif axis == 'y':
                self.hitPt.setX(0)
                self.hitPt.setZ(0)
            elif axis == 'z':
                self.hitPt.setX(0)
                self.hitPt.setY(0)
            return self.hitPt
        mCam2Widget = base.direct.camera.getMat(base.direct.widget)
        lineDir = Vec3(mCam2Widget.xformVec(base.direct.dr.nearVec))
        lineDir.normalize()
        lineOrigin = VBase3(0)
        decomposeMatrix(mCam2Widget, VBase3(0), VBase3(0), lineOrigin, CSDefault)
        if axis == 'x':
            if abs(lineDir.dot(Y_AXIS)) > abs(lineDir.dot(Z_AXIS)):
                self.hitPt.assign(planeIntersect(lineOrigin, lineDir, ORIGIN, Y_AXIS))
            else:
                self.hitPt.assign(planeIntersect(lineOrigin, lineDir, ORIGIN, Z_AXIS))
            self.hitPt.setY(0)
            self.hitPt.setZ(0)
        elif axis == 'y':
            if abs(lineDir.dot(X_AXIS)) > abs(lineDir.dot(Z_AXIS)):
                self.hitPt.assign(planeIntersect(lineOrigin, lineDir, ORIGIN, X_AXIS))
            else:
                self.hitPt.assign(planeIntersect(lineOrigin, lineDir, ORIGIN, Z_AXIS))
            self.hitPt.setX(0)
            self.hitPt.setZ(0)
        elif axis == 'z':
            if abs(lineDir.dot(X_AXIS)) > abs(lineDir.dot(Y_AXIS)):
                self.hitPt.assign(planeIntersect(lineOrigin, lineDir, ORIGIN, X_AXIS))
            else:
                self.hitPt.assign(planeIntersect(lineOrigin, lineDir, ORIGIN, Y_AXIS))
            self.hitPt.setX(0)
            self.hitPt.setY(0)
        return self.hitPt

    def getMouseIntersectPt(self):
        iRay = SelectionRay(base.direct.camera)
        iRay.collider.setFromLens(base.direct.camNode, base.direct.dr.mouseX, base.direct.dr.mouseY)
        iRay.collideWithBitMask(BitMask32.bit(21))
        iRay.ct.traverse(base.direct.grid)
        if iRay.getNumEntries() == 0:
            del iRay
            return Point3(0)
        entry = iRay.getEntry(0)
        hitPt = entry.getSurfacePoint(entry.getFromNodePath())
        np = NodePath('temp')
        np.setPos(base.direct.camera, hitPt)
        resultPt = Point3(0)
        resultPt.assign(np.getPos())
        np.remove()
        del iRay
        return resultPt

    def getWidgetIntersectPt(self, nodePath, plane):
        if hasattr(base.direct, 'manipulationControl') and base.direct.manipulationControl.fMultiView and base.direct.camera.getName() != 'persp':
            self.hitPt.assign(self.getMouseIntersectPt())
            return self.hitPt
        mCam2NodePath = base.direct.camera.getMat(nodePath)
        lineOrigin = VBase3(0)
        decomposeMatrix(mCam2NodePath, VBase3(0), VBase3(0), lineOrigin, CSDefault)
        lineDir = Vec3(mCam2NodePath.xformVec(base.direct.dr.nearVec))
        lineDir.normalize()
        if plane == 'x':
            self.hitPt.assign(planeIntersect(lineOrigin, lineDir, ORIGIN, X_AXIS))
        elif plane == 'y':
            self.hitPt.assign(planeIntersect(lineOrigin, lineDir, ORIGIN, Y_AXIS))
        elif plane == 'z':
            self.hitPt.assign(planeIntersect(lineOrigin, lineDir, ORIGIN, Z_AXIS))
        return self.hitPt
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\directtools\DirectManipulation.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:13:55 Pacific Daylight Time
