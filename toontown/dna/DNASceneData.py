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
        # Performs a BFS in order to find a path from startPoint to endPoint,
        # the minimum length will be minPathLen, and the maximum will be
        # maxPathLen. N.B. these values indicate the length in edges, not
        # vertices, so the returned list will be:
        # minPathLen+1 <= len(list) <= maxPathLen+1

        # The queue of paths to consider:
        # The format is a tuple: (prevPath, depth, point)
        pathDeque = deque()
        pathDeque.append((None, 0, startPoint))
        while pathDeque:
            path = pathDeque.popleft()
            prevPath, depth, point = path

            newDepth = depth + 1
            if newDepth > maxPathLen:
                # This path has grown too long, prune it.
                continue

            for adj in self.getAdjacentPoints(point):
                if adj == endPoint and newDepth >= minPathLen:
                    # Hey, we found the end! Let's return it:
                    points = deque()
                    points.appendleft(adj)
                    while path:
                        points.appendleft(path[-1])
                        path, _, _ = path
                    return list(points)

                # We're not at the end yet... Let's see if we can traverse this
                # point:
                if adj.type not in (DNAStoreSuitPoint.STREETPOINT,
                                    DNAStoreSuitPoint.COGHQINPOINT,
                                    DNAStoreSuitPoint.COGHQOUTPOINT):
                    # This is some other special point that we cannot walk
                    # across.
                    continue

                # Append this point to the paths we are considering:
                pathDeque.append((path, newDepth, adj))


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
