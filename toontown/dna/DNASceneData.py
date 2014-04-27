from DNAParser import *
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

    def getEdgeZone(self, edge):
        return edge.getVisGroup().getZone()

    def getPointZone(self, point):
        edges = self.getEdgesTo(point)
        return self.getEdgeZone(edges[0])

    def getSuitPath(self, startPoint, endPoint, minPathLen, maxPathLen):
        if minPathLen > 1:
            pointDeque = deque()
            pointDeque.append(startPoint)
            if self._getSuitPathBreadthFirst(0, pointDeque, endPoint, minPathLen, maxPathLen):
                path = []
                for i in range(len(pointDeque)):
                    point = pointDeque.popleft()
                    path.append(point)
                return path
        else:
            path = [startPoint, endPoint]
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
        return [self.getPointFromIndex(edge.b) for edge in self.getEdgesFrom(point)]

    def getConnectingEdge(self, pointA, pointB):
        assert isinstance(pointA, DNAStoreSuitPoint.DNAStoreSuitPoint)
        assert isinstance(pointB, DNAStoreSuitPoint.DNAStoreSuitPoint)
        for edge in self.edges:
            a = self.getPointFromIndex(edge.a)
            b = self.getPointFromIndex(edge.b)
            if (a == pointA and b == pointB) or (a == pointB and b == pointA):
                return edge
        return None

    def getSuitEdgeTravelTime(self, p1, p2, speed):
        pos1 = p1.getPos()
        pos2 = p1.getPos()
        return (pos1 - pos2).length()/speed

class DNABlock:
    index = None
    title = None
    buildingType = None
    zone = None

    def __init__(self, index):
        self.index = index

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
            self._blocks[block] = DNABlock(block)
        return self._blocks[block]

    def getBlocks(self):
        return self._blocks.items()
