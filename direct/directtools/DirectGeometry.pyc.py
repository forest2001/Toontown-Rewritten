# 2013.08.22 22:13:51 Pacific Daylight Time
# Embedded file name: direct.directtools.DirectGeometry
from pandac.PandaModules import *
from DirectGlobals import *
from DirectUtil import *
import math

class LineNodePath(NodePath):
    __module__ = __name__

    def __init__(self, parent = None, name = None, thickness = 1.0, colorVec = VBase4(1)):
        NodePath.__init__(self)
        if parent is None:
            parent = hidden
        self.lineNode = GeomNode('lineNode')
        self.assign(parent.attachNewNode(self.lineNode))
        if name:
            self.setName(name)
        ls = self.lineSegs = LineSegs()
        ls.setThickness(thickness)
        ls.setColor(colorVec)
        return

    def moveTo(self, *_args):
        apply(self.lineSegs.moveTo, _args)

    def drawTo(self, *_args):
        apply(self.lineSegs.drawTo, _args)

    def create(self, frameAccurate = 0):
        self.lineSegs.create(self.lineNode, frameAccurate)

    def reset(self):
        self.lineSegs.reset()
        self.lineNode.removeAllGeoms()

    def isEmpty(self):
        return self.lineSegs.isEmpty()

    def setThickness(self, thickness):
        self.lineSegs.setThickness(thickness)

    def setColor(self, *_args):
        apply(self.lineSegs.setColor, _args)

    def setVertex(self, *_args):
        apply(self.lineSegs.setVertex, _args)

    def setVertexColor(self, vertex, *_args):
        apply(self.lineSegs.setVertexColor, (vertex,) + _args)

    def getCurrentPosition(self):
        return self.lineSegs.getCurrentPosition()

    def getNumVertices(self):
        return self.lineSegs.getNumVertices()

    def getVertex(self, index):
        return self.lineSegs.getVertex(index)

    def getVertexColor(self):
        return self.lineSegs.getVertexColor()

    def drawArrow(self, sv, ev, arrowAngle, arrowLength):
        self.moveTo(sv)
        self.drawTo(ev)
        v = sv - ev
        angle = math.atan2(v[1], v[0])
        a1 = angle + deg2Rad(arrowAngle)
        a2 = angle - deg2Rad(arrowAngle)
        a1x = arrowLength * math.cos(a1)
        a1y = arrowLength * math.sin(a1)
        a2x = arrowLength * math.cos(a2)
        a2y = arrowLength * math.sin(a2)
        z = ev[2]
        self.moveTo(ev)
        self.drawTo(Point3(ev + Point3(a1x, a1y, z)))
        self.moveTo(ev)
        self.drawTo(Point3(ev + Point3(a2x, a2y, z)))

    def drawArrow2d(self, sv, ev, arrowAngle, arrowLength):
        self.moveTo(sv)
        self.drawTo(ev)
        v = sv - ev
        angle = math.atan2(v[2], v[0])
        a1 = angle + deg2Rad(arrowAngle)
        a2 = angle - deg2Rad(arrowAngle)
        a1x = arrowLength * math.cos(a1)
        a1y = arrowLength * math.sin(a1)
        a2x = arrowLength * math.cos(a2)
        a2y = arrowLength * math.sin(a2)
        self.moveTo(ev)
        self.drawTo(Point3(ev + Point3(a1x, 0.0, a1y)))
        self.moveTo(ev)
        self.drawTo(Point3(ev + Point3(a2x, 0.0, a2y)))

    def drawLines(self, lineList):
        for pointList in lineList:
            apply(self.moveTo, pointList[0])
            for point in pointList[1:]:
                apply(self.drawTo, point)


def planeIntersect(lineOrigin, lineDir, planeOrigin, normal):
    t = 0
    offset = planeOrigin - lineOrigin
    t = offset.dot(normal) / lineDir.dot(normal)
    hitPt = lineDir * t
    return hitPt + lineOrigin


def getNearProjectionPoint(nodePath):
    origin = nodePath.getPos(base.direct.camera)
    if origin[1] != 0.0:
        return origin * (base.direct.dr.near / origin[1])
    else:
        return Point3(0, base.direct.dr.near, 0)


def getScreenXY(nodePath):
    nearVec = getNearProjectionPoint(nodePath)
    nearX = CLAMP(nearVec[0], base.direct.dr.left, base.direct.dr.right)
    nearY = CLAMP(nearVec[2], base.direct.dr.bottom, base.direct.dr.top)
    percentX = (nearX - base.direct.dr.left) / base.direct.dr.nearWidth
    percentY = (nearY - base.direct.dr.bottom) / base.direct.dr.nearHeight
    screenXY = Vec3(2 * percentX - 1.0, nearVec[1], 2 * percentY - 1.0)
    return screenXY


def getCrankAngle(center):
    x = base.direct.dr.mouseX - center[0]
    y = base.direct.dr.mouseY - center[2]
    return 180 + rad2Deg(math.atan2(y, x))


def relHpr(nodePath, base, h, p, r):
    mNodePath2Base = nodePath.getMat(base)
    mBase2NewBase = Mat4(Mat4.identMat())
    composeMatrix(mBase2NewBase, UNIT_VEC, VBase3(h, p, r), ZERO_VEC, CSDefault)
    mBase2NodePath = base.getMat(nodePath)
    mNodePath2Parent = nodePath.getMat()
    resultMat = mNodePath2Base * mBase2NewBase
    resultMat = resultMat * mBase2NodePath
    resultMat = resultMat * mNodePath2Parent
    hpr = Vec3(0)
    decomposeMatrix(resultMat, VBase3(), hpr, VBase3(), CSDefault)
    nodePath.setHpr(hpr)


def qSlerp(startQuat, endQuat, t):
    startQ = Quat(startQuat)
    destQuat = Quat(Quat.identQuat())
    cosOmega = startQ.getI() * endQuat.getI() + startQ.getJ() * endQuat.getJ() + startQ.getK() * endQuat.getK() + startQ.getR() * endQuat.getR()
    if cosOmega < 0.0:
        cosOmega *= -1
        startQ.setI(-1 * startQ.getI())
        startQ.setJ(-1 * startQ.getJ())
        startQ.setK(-1 * startQ.getK())
        startQ.setR(-1 * startQ.getR())
    if 1.0 + cosOmega > Q_EPSILON:
        if 1.0 - cosOmega > Q_EPSILON:
            omega = math.acos(cosOmega)
            sinOmega = math.sin(omega)
            startScale = math.sin((1.0 - t) * omega) / sinOmega
            endScale = math.sin(t * omega) / sinOmega
        else:
            startScale = 1.0 - t
            endScale = t
        destQuat.setI(startScale * startQ.getI() + endScale * endQuat.getI())
        destQuat.setJ(startScale * startQ.getJ() + endScale * endQuat.getJ())
        destQuat.setK(startScale * startQ.getK() + endScale * endQuat.getK())
        destQuat.setR(startScale * startQ.getR() + endScale * endQuat.getR())
    else:
        destQuat.setI(-startQ.getJ())
        destQuat.setJ(startQ.getI())
        destQuat.setK(-startQ.getR())
        destQuat.setR(startQ.getK())
        startScale = math.sin((0.5 - t) * math.pi)
        endScale = math.sin(t * math.pi)
        destQuat.setI(startScale * startQ.getI() + endScale * endQuat.getI())
        destQuat.setJ(startScale * startQ.getJ() + endScale * endQuat.getJ())
        destQuat.setK(startScale * startQ.getK() + endScale * endQuat.getK())
    return destQuat
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\directtools\DirectGeometry.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:13:52 Pacific Daylight Time
