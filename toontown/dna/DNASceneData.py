from DNAParser import *
from DNASuitPath import DNASuitPath
from collections import deque

class DNASuitGraph:
    def __init__(self, points, edges):
        self._pointId2point = {}
        self._point2outboundEdges = {}
        self._point2inboundEdges = {}

        for point in points:
            self._pointId2point[point.id] = point

        for edge in edges:
            try:
                a = self._pointId2point[edge.a]
                a.zone = int(edge.parent.zone)
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
            if self.getSuitPathBreadthFirst(0, pointDeque, endPoint, minPathLen, maxPathLen):
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

    def getSuitPathBreadthFirst(self, depth, pointDeque, endPoint, minPathLen, maxPathLen):
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
            if self.getPointFromIndex(edge.b) != point and not self.getPointFromIndex(edge.b) in pointDeque:
                pointDeque.append(self.getPointFromIndex(edge.b))
                if self.getSuitPathBreadthFirst(depth+1, pointDeque, endPoint, minPathLen, maxPathLen):
                    return True
        return False

class DNASceneData:
    def __init__(self):
        self.visgroups = []

        self.suitPoints = []
        self.suitEdges = []
        self.suitGraph = None

    def update(self):
        self.suitGraph = DNASuitGraph(self.suitPoints, self.suitEdges)

    def getAdjacentPoints(self, point):
        path = DNASuitPath()
        edges = self.suitGraph.getEdgesFrom(point)
        for edge in edges:
            path.addPoint(self.suitGraph.getPointFromIndex(edge.b))
        return path

    def getConnectingEdge(self, pointA, pointB):
        for edge in self.suitEdges:
            a = self.suitGraph.getPointFromIndex(edge.a)
            b = self.suitGraph.getPointFromIndex(edge.b)
            if (a == pointA and b == pointB) or (a == pointB and b == pointA):
                return edge
        return None
