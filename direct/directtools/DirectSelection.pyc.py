# 2013.08.22 22:13:55 Pacific Daylight Time
# Embedded file name: direct.directtools.DirectSelection
from direct.showbase.DirectObject import DirectObject
from DirectGlobals import *
from DirectUtil import *
from DirectGeometry import *
COA_ORIGIN = 0
COA_CENTER = 1

class DirectNodePath(NodePath):
    __module__ = __name__

    def __init__(self, nodePath, bboxColor = None):
        NodePath.__init__(self)
        self.assign(nodePath)
        self.bbox = DirectBoundingBox(self, bboxColor)
        center = self.bbox.getCenter()
        self.mCoa2Dnp = Mat4(Mat4.identMat())
        if base.direct.coaMode == COA_CENTER:
            self.mCoa2Dnp.setRow(3, Vec4(center[0], center[1], center[2], 1))
        self.tDnp2Widget = TransformState.makeIdentity()

    def highlight(self, fRecompute = 1):
        if fRecompute:
            pass
        self.bbox.show()

    def dehighlight(self):
        self.bbox.hide()

    def getCenter(self):
        return self.bbox.getCenter()

    def getRadius(self):
        return self.bbox.getRadius()

    def getMin(self):
        return self.bbox.getMin()

    def getMax(self):
        return self.bbox.getMax()


class SelectedNodePaths(DirectObject):
    __module__ = __name__

    def __init__(self):
        self.reset()
        self.tagList = []

    def addTag(self, tag):
        if tag not in self.tagList:
            self.tagList.append(tag)

    def removeTag(self, tag):
        self.tagList.remove(tag)

    def reset(self):
        self.selectedDict = {}
        self.selectedList = []
        self.deselectedDict = {}
        __builtins__['last'] = self.last = None
        return

    def select(self, nodePath, fMultiSelect = 0, fSelectTag = 1):
        if not nodePath:
            print 'Nothing selected!!'
            return None
        if not fMultiSelect:
            self.deselectAll()
        if fSelectTag:
            for tag in self.tagList:
                if nodePath.hasNetTag(tag):
                    nodePath = nodePath.findNetTag(tag)
                    break

        id = nodePath.id()
        dnp = self.getSelectedDict(id)
        if dnp:
            self.deselect(nodePath)
            return None
        else:
            dnp = self.getDeselectedDict(id)
            if dnp:
                del self.deselectedDict[id]
                dnp.highlight()
            else:
                dnp = DirectNodePath(nodePath)
                dnp.highlight(fRecompute=0)
            self.selectedDict[dnp.id()] = dnp
            self.selectedList.append(dnp)
        __builtins__['last'] = self.last = dnp
        if base.direct.clusterMode == 'client':
            cluster.selectNodePath(dnp)
        return dnp

    def deselect(self, nodePath):
        id = nodePath.id()
        dnp = self.getSelectedDict(id)
        if dnp:
            dnp.dehighlight()
            del self.selectedDict[id]
            if dnp in self.selectedList:
                self.selectedList.remove(dnp)
            self.deselectedDict[id] = dnp
            messenger.send('DIRECT_deselectedNodePath', [dnp])
            if base.direct.clusterMode == 'client':
                cluster.deselectNodePath(dnp)
        return dnp

    def getSelectedAsList(self):
        return self.selectedList[:]

    def __getitem__(self, index):
        return self.getSelectedAsList()[index]

    def getSelectedDict(self, id):
        dnp = self.selectedDict.get(id, None)
        if dnp:
            return dnp
        else:
            return
        return

    def getDeselectedAsList(self):
        return self.deselectedDict.values()[:]

    def getDeselectedDict(self, id):
        dnp = self.deselectedDict.get(id, None)
        if dnp:
            return dnp
        else:
            return
        return

    def forEachSelectedNodePathDo(self, func):
        selectedNodePaths = self.getSelectedAsList()
        for nodePath in selectedNodePaths:
            func(nodePath)

    def forEachDeselectedNodePathDo(self, func):
        deselectedNodePaths = self.getDeselectedAsList()
        for nodePath in deselectedNodePaths:
            func(nodePath)

    def getWrtAll(self):
        self.forEachSelectedNodePathDo(self.getWrt)

    def getWrt(self, nodePath):
        nodePath.tDnp2Widget = nodePath.getTransform(base.direct.widget)

    def moveWrtWidgetAll(self):
        self.forEachSelectedNodePathDo(self.moveWrtWidget)

    def moveWrtWidget(self, nodePath):
        nodePath.setTransform(base.direct.widget, nodePath.tDnp2Widget)

    def deselectAll(self):
        self.forEachSelectedNodePathDo(self.deselect)

    def highlightAll(self):
        self.forEachSelectedNodePathDo(DirectNodePath.highlight)

    def dehighlightAll(self):
        self.forEachSelectedNodePathDo(DirectNodePath.dehighlight)

    def removeSelected(self):
        selected = self.last
        if selected:
            selected.remove()
        __builtins__['last'] = self.last = None
        return

    def removeAll(self):
        self.forEachSelectedNodePathDo(NodePath.remove)

    def toggleVisSelected(self):
        selected = self.last
        if selected:
            selected.toggleVis()

    def toggleVisAll(self):
        self.forEachSelectedNodePathDo(NodePath.toggleVis)

    def isolateSelected(self):
        selected = self.last
        if selected:
            selected.isolate()

    def getDirectNodePath(self, nodePath):
        id = nodePath.id()
        dnp = self.getSelectedDict(id)
        if dnp:
            return dnp
        return self.getDeselectedDict(id)

    def getNumSelected(self):
        return len(self.selectedDict.keys())


class DirectBoundingBox():
    __module__ = __name__

    def __init__(self, nodePath, bboxColor = None):
        self.nodePath = nodePath
        self.computeTightBounds()
        self.lines = self.createBBoxLines(bboxColor)

    def recompute(self):
        self.computeTightBounds()
        self.updateBBoxLines()

    def computeTightBounds(self):
        tMat = Mat4(self.nodePath.getMat())
        self.nodePath.clearMat()
        self.min = Point3(0)
        self.max = Point3(0)
        self.nodePath.calcTightBounds(self.min, self.max)
        self.center = Point3((self.min + self.max) / 2.0)
        self.radius = Vec3(self.max - self.min).length()
        self.nodePath.setMat(tMat)
        del tMat

    def computeBounds(self):
        self.bounds = self.getBounds()
        if self.bounds.isEmpty() or self.bounds.isInfinite():
            self.center = Point3(0)
            self.radius = 1.0
        else:
            self.center = self.bounds.getCenter()
            self.radius = self.bounds.getRadius()
        self.min = Point3(self.center - Point3(self.radius))
        self.max = Point3(self.center + Point3(self.radius))

    def createBBoxLines(self, bboxColor = None):
        lines = LineNodePath(hidden)
        lines.node().setName('bboxLines')
        if bboxColor:
            lines.setColor(VBase4(*bboxColor))
        else:
            lines.setColor(VBase4(1.0, 0.0, 0.0, 1.0))
        lines.setThickness(0.5)
        minX = self.min[0]
        minY = self.min[1]
        minZ = self.min[2]
        maxX = self.max[0]
        maxY = self.max[1]
        maxZ = self.max[2]
        lines.moveTo(minX, minY, minZ)
        lines.drawTo(maxX, minY, minZ)
        lines.drawTo(maxX, maxY, minZ)
        lines.drawTo(minX, maxY, minZ)
        lines.drawTo(minX, minY, minZ)
        lines.drawTo(minX, minY, maxZ)
        lines.drawTo(maxX, minY, maxZ)
        lines.drawTo(maxX, maxY, maxZ)
        lines.drawTo(minX, maxY, maxZ)
        lines.drawTo(minX, minY, maxZ)
        lines.moveTo(maxX, minY, minZ)
        lines.drawTo(maxX, minY, maxZ)
        lines.moveTo(maxX, maxY, minZ)
        lines.drawTo(maxX, maxY, maxZ)
        lines.moveTo(minX, maxY, minZ)
        lines.drawTo(minX, maxY, maxZ)
        lines.create()
        useDirectRenderStyle(lines)
        return lines

    def setBoxColorScale(self, r, g, b, a):
        if self.lines:
            self.lines.reset()
            self.lines = None
        self.lines = self.createBBoxLines((r,
         g,
         b,
         a))
        self.show()
        return

    def updateBBoxLines(self):
        ls = self.lines.lineSegs
        minX = self.min[0]
        minY = self.min[1]
        minZ = self.min[2]
        maxX = self.max[0]
        maxY = self.max[1]
        maxZ = self.max[2]
        ls.setVertex(0, minX, minY, minZ)
        ls.setVertex(1, maxX, minY, minZ)
        ls.setVertex(2, maxX, maxY, minZ)
        ls.setVertex(3, minX, maxY, minZ)
        ls.setVertex(4, minX, minY, minZ)
        ls.setVertex(5, minX, minY, maxZ)
        ls.setVertex(6, maxX, minY, maxZ)
        ls.setVertex(7, maxX, maxY, maxZ)
        ls.setVertex(8, minX, maxY, maxZ)
        ls.setVertex(9, minX, minY, maxZ)
        ls.setVertex(10, maxX, minY, minZ)
        ls.setVertex(11, maxX, minY, maxZ)
        ls.setVertex(12, maxX, maxY, minZ)
        ls.setVertex(13, maxX, maxY, maxZ)
        ls.setVertex(14, minX, maxY, minZ)
        ls.setVertex(15, minX, maxY, maxZ)

    def getBounds(self):
        nodeBounds = BoundingSphere()
        nodeBounds.extendBy(self.nodePath.node().getInternalBound())
        for child in self.nodePath.getChildren():
            nodeBounds.extendBy(child.getBounds())

        return nodeBounds.makeCopy()

    def show(self):
        self.lines.reparentTo(self.nodePath)

    def hide(self):
        self.lines.reparentTo(hidden)

    def getCenter(self):
        return self.center

    def getRadius(self):
        return self.radius

    def getMin(self):
        return self.min

    def getMax(self):
        return self.max

    def vecAsString(self, vec):
        return '%.2f %.2f %.2f' % (vec[0], vec[1], vec[2])

    def __repr__(self):
        return repr(self.__class__) + '\nNodePath:\t%s\n' % self.nodePath.getName() + 'Min:\t\t%s\n' % self.vecAsString(self.min) + 'Max:\t\t%s\n' % self.vecAsString(self.max) + 'Center:\t\t%s\n' % self.vecAsString(self.center) + 'Radius:\t\t%.2f' % self.radius


class SelectionQueue(CollisionHandlerQueue):
    __module__ = __name__

    def __init__(self, parentNP = render):
        CollisionHandlerQueue.__init__(self)
        self.index = -1
        self.entry = None
        self.skipFlags = SKIP_NONE
        self.collisionNodePath = NodePath(CollisionNode('collisionNP'))
        self.setParentNP(parentNP)
        self.collisionNodePath.hide()
        self.collisionNode = self.collisionNodePath.node()
        self.collideWithGeom()
        self.ct = CollisionTraverser('DirectSelection')
        self.ct.setRespectPrevTransform(False)
        self.ct.addCollider(self.collisionNodePath, self)
        self.unpickable = UNPICKABLE
        return

    def setParentNP(self, parentNP):
        self.collisionNodePath.reparentTo(parentNP)

    def addCollider(self, collider):
        self.collider = collider
        self.collisionNode.addSolid(self.collider)

    def collideWithBitMask(self, bitMask):
        self.collisionNode.setIntoCollideMask(BitMask32().allOff())
        self.collisionNode.setFromCollideMask(bitMask)

    def collideWithGeom(self):
        self.collisionNode.setIntoCollideMask(BitMask32().allOff())
        self.collisionNode.setFromCollideMask(GeomNode.getDefaultCollideMask())

    def collideWithWidget(self):
        self.collisionNode.setIntoCollideMask(BitMask32().allOff())
        mask = BitMask32()
        mask.setWord(2147483648L)
        self.collisionNode.setFromCollideMask(mask)

    def addUnpickable(self, item):
        if item not in self.unpickable:
            self.unpickable.append(item)

    def removeUnpickable(self, item):
        if item in self.unpickable:
            self.unpickable.remove(item)

    def setCurrentIndex(self, index):
        if index < 0 or index >= self.getNumEntries():
            self.index = -1
        else:
            self.index = index

    def setCurrentEntry(self, entry):
        self.entry = entry

    def getCurrentEntry(self):
        return self.entry

    def isEntryBackfacing(self, entry):
        if not entry.hasSurfaceNormal():
            return 0
        if direct:
            cam = base.direct.cam
        else:
            cam = base.cam
        fromNodePath = entry.getFromNodePath()
        v = Vec3(entry.getSurfacePoint(fromNodePath))
        n = entry.getSurfaceNormal(fromNodePath)
        if self.collisionNodePath.getParent() != cam:
            p2cam = self.collisionNodePath.getParent().getMat(cam)
            v = Vec3(p2cam.xformPoint(v))
            n = p2cam.xformVec(n)
        v.normalize()
        return v.dot(n) >= 0

    def findNextCollisionEntry(self, skipFlags = SKIP_NONE):
        return self.findCollisionEntry(skipFlags, self.index + 1)

    def findCollisionEntry(self, skipFlags = SKIP_NONE, startIndex = 0):
        self.setCurrentIndex(-1)
        self.setCurrentEntry(None)
        for i in range(startIndex, self.getNumEntries()):
            entry = self.getEntry(i)
            nodePath = entry.getIntoNodePath()
            if skipFlags & SKIP_HIDDEN and nodePath.isHidden():
                pass
            elif skipFlags & SKIP_BACKFACE and self.isEntryBackfacing(entry):
                pass
            elif skipFlags & SKIP_CAMERA and camera in nodePath.getAncestors():
                pass
            elif skipFlags & SKIP_UNPICKABLE and nodePath.getName() in self.unpickable:
                pass
            elif base.direct and skipFlags & SKIP_WIDGET and nodePath.getTag('WidgetName') != base.direct.widget.getName():
                pass
            elif base.direct and skipFlags & SKIP_WIDGET and base.direct.fControl and nodePath.getName()[2:] == 'ring':
                pass
            else:
                self.setCurrentIndex(i)
                self.setCurrentEntry(entry)
                break

        return self.getCurrentEntry()


class SelectionRay(SelectionQueue):
    __module__ = __name__

    def __init__(self, parentNP = render):
        SelectionQueue.__init__(self, parentNP)
        self.addCollider(CollisionRay())

    def pick(self, targetNodePath, xy = None):
        if xy:
            mx = xy[0]
            my = xy[1]
        elif direct:
            mx = base.direct.dr.mouseX
            my = base.direct.dr.mouseY
        else:
            if not base.mouseWatcherNode.hasMouse():
                self.clearEntries()
                return
            mx = base.mouseWatcherNode.getMouseX()
            my = base.mouseWatcherNode.getMouseY()
        if direct:
            self.collider.setFromLens(base.direct.camNode, mx, my)
        else:
            self.collider.setFromLens(base.camNode, mx, my)
        self.ct.traverse(targetNodePath)
        self.sortEntries()

    def pickBitMask(self, bitMask = BitMask32.allOff(), targetNodePath = render, skipFlags = SKIP_ALL):
        self.collideWithBitMask(bitMask)
        self.pick(targetNodePath)
        return self.findCollisionEntry(skipFlags)

    def pickGeom(self, targetNodePath = render, skipFlags = SKIP_ALL, xy = None):
        self.collideWithGeom()
        self.pick(targetNodePath, xy=xy)
        return self.findCollisionEntry(skipFlags)

    def pickWidget(self, targetNodePath = render, skipFlags = SKIP_NONE):
        self.collideWithWidget()
        self.pick(targetNodePath)
        return self.findCollisionEntry(skipFlags)

    def pick3D(self, targetNodePath, origin, dir):
        self.collider.setOrigin(origin)
        self.collider.setDirection(dir)
        self.ct.traverse(targetNodePath)
        self.sortEntries()

    def pickGeom3D(self, targetNodePath = render, origin = Point3(0), dir = Vec3(0, 0, -1), skipFlags = SKIP_HIDDEN | SKIP_CAMERA):
        self.collideWithGeom()
        self.pick3D(targetNodePath, origin, dir)
        return self.findCollisionEntry(skipFlags)

    def pickBitMask3D(self, bitMask = BitMask32.allOff(), targetNodePath = render, origin = Point3(0), dir = Vec3(0, 0, -1), skipFlags = SKIP_ALL):
        self.collideWithBitMask(bitMask)
        self.pick3D(targetNodePath, origin, dir)
        return self.findCollisionEntry(skipFlags)


class SelectionSegment(SelectionQueue):
    __module__ = __name__

    def __init__(self, parentNP = render, numSegments = 1):
        SelectionQueue.__init__(self, parentNP)
        self.colliders = []
        self.numColliders = 0
        for i in range(numSegments):
            self.addCollider(CollisionSegment())

    def addCollider(self, collider):
        self.colliders.append(collider)
        self.collisionNode.addSolid(collider)
        self.numColliders += 1

    def pickGeom(self, targetNodePath = render, endPointList = [], skipFlags = SKIP_HIDDEN | SKIP_CAMERA):
        self.collideWithGeom()
        for i in range(min(len(endPointList), self.numColliders)):
            pointA, pointB = endPointList[i]
            collider = self.colliders[i]
            collider.setPointA(pointA)
            collider.setPointB(pointB)

        self.ct.traverse(targetNodePath)
        return self.findCollisionEntry(skipFlags)

    def pickBitMask(self, bitMask = BitMask32.allOff(), targetNodePath = render, endPointList = [], skipFlags = SKIP_HIDDEN | SKIP_CAMERA):
        self.collideWithBitMask(bitMask)
        for i in range(min(len(endPointList), self.numColliders)):
            pointA, pointB = endPointList[i]
            collider = self.colliders[i]
            collider.setPointA(pointA)
            collider.setPointB(pointB)

        self.ct.traverse(targetNodePath)
        return self.findCollisionEntry(skipFlags)


class SelectionSphere(SelectionQueue):
    __module__ = __name__

    def __init__(self, parentNP = render, numSpheres = 1):
        SelectionQueue.__init__(self, parentNP)
        self.colliders = []
        self.numColliders = 0
        for i in range(numSpheres):
            self.addCollider(CollisionSphere(Point3(0), 1))

    def addCollider(self, collider):
        self.colliders.append(collider)
        self.collisionNode.addSolid(collider)
        self.numColliders += 1

    def setCenter(self, i, center):
        c = self.colliders[i]
        c.setCenter(center)

    def setRadius(self, i, radius):
        c = self.colliders[i]
        c.setRadius(radius)

    def setCenterRadius(self, i, center, radius):
        c = self.colliders[i]
        c.setCenter(center)
        c.setRadius(radius)

    def isEntryBackfacing(self, entry):
        fromNodePath = entry.getFromNodePath()
        v = Vec3(entry.getSurfacePoint(fromNodePath) - entry.getFrom().getCenter())
        n = entry.getSurfaceNormal(fromNodePath)
        if v.length() < 0.05:
            return 1
        v.normalize()
        return v.dot(n) >= 0

    def pick(self, targetNodePath, skipFlags):
        self.ct.traverse(targetNodePath)
        self.sortEntries()
        return self.findCollisionEntry(skipFlags)

    def pickGeom(self, targetNodePath = render, skipFlags = SKIP_HIDDEN | SKIP_CAMERA):
        self.collideWithGeom()
        return self.pick(targetNodePath, skipFlags)

    def pickBitMask(self, bitMask = BitMask32.allOff(), targetNodePath = render, skipFlags = SKIP_HIDDEN | SKIP_CAMERA):
        self.collideWithBitMask(bitMask)
        return self.pick(targetNodePath, skipFlags)
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\directtools\DirectSelection.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:13:56 Pacific Daylight Time
