from DNAParser import *
from DNASuitPath import DNASuitPath
import DNAStoreSuitPoint
from collections import deque

class DNASuitGraph:
    def __init__(self, points, edges):
        self.points = points
        self.edges = edges

        self._pointId2point = {}
        self._point2outboundEdges = {}
        self._point2inboundEdges = {}

        for point in points:
            self._pointId2point[point.id] = point

        for edge in edges:
            try:
                a = self._pointId2point[edge.a]
                a.zone = int(edge.parent.getZone())
                b = self._pointId2point[edge.b]
            except KeyError:
                raise DNAError('Edge connects a nonexistent point!')

            self._point2outboundEdges.setdefault(a, []).append(edge)
            self._point2inboundEdges.setdefault(b, []).append(edge)

    def getEdgeEndpoints(self, edge):
        return self._pointId2point[edge.a], self._pointId2point[edge.b]

    def getEdgesFrom(self, point):
        return self._point2outboundEdges.get(point, [])

    def getEdgesTo(self, point):
        return self._point2inboundEdges.get(point, [])

    def getPointFromIndex(self, index):
        return self._pointId2point[index]

    def getSuitPath(self, startPoint, endPoint, minPathLen, maxPathLen):
        if minPathLen > 1:
            pointDeque = deque()
            pointDeque.append(startPoint)
            if self._getSuitPathBreadthFirst(0, pointDeque, endPoint, minPathLen, maxPathLen):
                path = DNASuitPath()
                for i in range(len(pointDeque)):
                    point = pointDeque.popleft()
                    path.addPoint(point)
                return path
        else:
            path = DNASuitPath()
            path.addPoint(startPoint)
            path.addPoint(endPoint)
            return path

    def _getSuitPathBreadthFirst(self, depth, pointDeque, endPoint, minPathLen, maxPathLen):
        point = pointDeque.pop()
        pointDeque.append(point)
        if depth > maxPathLen:
            return False
        if point == endPoint:
            if depth > minPathLen:
                pointDeque.append(point)
                return True
        edges = self.getEdgesFrom(point)
        for edge in edges:
            if self.getPointFromIndex(edge.b) != point and not self.getPointFromIndex(edge.b) in pointDeque \
              and (self.getPointFromIndex(edge.b).type in [DNAStoreSuitPoint.STREETPOINT, DNAStoreSuitPoint.COGHQINPOINT, DNAStoreSuitPoint.COGHQOUTPOINT] or self.getPointFromIndex(edge.b) == endPoint):
                pointDeque.append(self.getPointFromIndex(edge.b))
                if self._getSuitPathBreadthFirst(depth+1, pointDeque, endPoint, minPathLen, maxPathLen):
                    return True
        return False

    def getAdjacentPoints(self, point):
        path = DNASuitPath()
        edges = self.getEdgesFrom(point)
        for edge in edges:
            path.addPoint(self.getPointFromIndex(edge.b))
        return path

    def getConnectingEdge(self, pointA, pointB):
        for edge in self.edges:
            a = self.suitGraph.getPointFromIndex(edge.a)
            b = self.suitGraph.getPointFromIndex(edge.b)
            if (a == pointA and b == pointB) or (a == pointB and b == pointA):
                return edge
        return None

    def getSuitEdgeTravelTime(self, p1, p2, speed):
        pos1 = self.getPointFromIndex(p1).getPos()
        pos2 = self.getPointFromIndex(p1).getPos()
        return (pos1 - pos2).length()/speed

class DNABlock:
    title = None
    door = None
    buildingType = None
    zone = None

class DNASceneData:
    def __init__(self):
        self.visgroups = []

        self.suitPoints = []
        self.suitEdges = []
        self.suitGraph = None
        
        self._blocks = {}

    def update(self):
        self.suitGraph = DNASuitGraph(self.suitPoints, self.suitEdges)

    def getBlock(self, block):
        assert type(block) == int
        if not block in self._blocks:
            self._blocks[block] = DNABlock()
        return self._blocks[block]

    def getBlocks(self):
        return self._blocks.items()
