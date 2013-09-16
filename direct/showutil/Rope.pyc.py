# 2013.08.22 22:14:50 Pacific Daylight Time
# Embedded file name: direct.showutil.Rope
from pandac.PandaModules import *
import types

class Rope(NodePath):
    __module__ = __name__
    showRope = base.config.GetBool('show-rope', 1)

    def __init__(self, name = 'Rope'):
        self.ropeNode = RopeNode(name)
        self.curve = NurbsCurveEvaluator()
        self.ropeNode.setCurve(self.curve)
        NodePath.__init__(self, self.ropeNode)
        self.name = name

    def setup(self, order, verts, knots = None):
        self.order = order
        self.verts = verts
        self.knots = knots
        self.recompute()

    def recompute(self):
        if not self.showRope:
            return
        numVerts = len(self.verts)
        self.curve.reset(numVerts)
        self.curve.setOrder(self.order)
        defaultNodePath = None
        defaultPoint = (0, 0, 0)
        defaultColor = (1, 1, 1, 1)
        defaultThickness = 1
        useVertexColor = self.ropeNode.getUseVertexColor()
        useVertexThickness = self.ropeNode.getUseVertexThickness()
        vcd = self.ropeNode.getVertexColorDimension()
        vtd = self.ropeNode.getVertexThicknessDimension()
        for i in range(numVerts):
            v = self.verts[i]
            if isinstance(v, types.TupleType):
                nodePath, point = v
                color = defaultColor
                thickness = defaultThickness
            else:
                nodePath = v.get('node', defaultNodePath)
                point = v.get('point', defaultPoint)
                color = v.get('color', defaultColor)
                thickness = v.get('thickness', defaultThickness)
            if isinstance(point, types.TupleType):
                if len(point) >= 4:
                    self.curve.setVertex(i, VBase4(point[0], point[1], point[2], point[3]))
                else:
                    self.curve.setVertex(i, VBase3(point[0], point[1], point[2]))
            else:
                self.curve.setVertex(i, point)
            if nodePath:
                self.curve.setVertexSpace(i, nodePath)
            if useVertexColor:
                self.curve.setExtendedVertex(i, vcd + 0, color[0])
                self.curve.setExtendedVertex(i, vcd + 1, color[1])
                self.curve.setExtendedVertex(i, vcd + 2, color[2])
                self.curve.setExtendedVertex(i, vcd + 3, color[3])
            if useVertexThickness:
                self.curve.setExtendedVertex(i, vtd, thickness)

        if self.knots != None:
            for i in range(len(self.knots)):
                self.curve.setKnot(i, self.knots[i])

        self.ropeNode.resetBound(self)
        return

    def getPoints(self, len):
        result = self.curve.evaluate(self)
        startT = result.getStartT()
        sizeT = result.getEndT() - startT
        numPts = len
        ropePts = []
        for i in range(numPts):
            pt = Point3()
            result.evalPoint(sizeT * i / float(numPts - 1) + startT, pt)
            ropePts.append(pt)

        return ropePts
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\showutil\Rope.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:14:50 Pacific Daylight Time
