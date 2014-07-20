from DNAParser import *
import DNAStoreSuitPoint
from collections import deque

class DNASuitGraphLink(object):
    unboundedDistance = None
    unboundedNext = None
    boundedDistance = None
    boundedNext = None

class DNASuitGraphVertex(object):
    def __init__(self, point, traversable):
        self.visitIndex = 0

        self.paths = {}
        self.neighbors = []

        self.point = point
        self.traversable = traversable

    def processLink(self, neighbor, distance, destination, unbounded=False):
        """Process a link announcement from a neighbor:

        Neighbor `neighbor` is telling us that it has a `distance` cost link to
        `destination`.
        """

        unbounded = (self.visitIndex > 0) or unbounded

        self.visitIndex += 1

        link = self.paths.setdefault(destination, DNASuitGraphLink())
        existingDistance = link.unboundedDistance if unbounded else link.boundedDistance

        if existingDistance is None or distance < existingDistance:
            if unbounded:
                link.unboundedDistance = distance
                link.unboundedNext = neighbor
            else:
                link.boundedDistance = distance
                link.boundedNext = neighbor

            if self.traversable:
                # Duplicated from announceLink to prevent deep recursion.
                for neighbor in self.neighbors:
                    neighbor.processLink(self, distance, destination, unbounded)

        self.visitIndex -= 1

    def announceLink(self, distance, destination, unbounded):
        for neighbor in self.neighbors:
            neighbor.processLink(self, distance, destination, unbounded)

class DNASuitGraph(object):
    def __init__(self, points, edges):
        self.points = points
        self.edges = edges

        self._pointId2point = {}
        self._point2vertex = {}
        self._point2outboundEdges = {}
        self._point2inboundEdges = {}

        for point in points:
            self._pointId2point[point.id] = point

            traversable = point.type in (DNAStoreSuitPoint.STREETPOINT,
                                         DNAStoreSuitPoint.COGHQINPOINT,
                                         DNAStoreSuitPoint.COGHQOUTPOINT)
            self._point2vertex[point] = DNASuitGraphVertex(point, traversable)

        for edge in edges:
            try:
                a = self._pointId2point[edge.a]
                b = self._pointId2point[edge.b]
            except KeyError:
                raise DNAError('Edge connects a nonexistent point!')

            self._point2outboundEdges.setdefault(a, []).append(edge)
            self._point2inboundEdges.setdefault(b, []).append(edge)

            self._point2vertex[b].neighbors.append(self._point2vertex[a])

        for vertex in self._point2vertex.values():
            vertex.announceLink(1, vertex, False)

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
        minpl = minPathLen
        maxpl = maxPathLen
        start = self._point2vertex[startPoint]
        end = self._point2vertex[endPoint]

        at = start
        path = [startPoint]

        while at != end or minPathLen > 0:
            link = at.paths.get(end)

            if link is None:
                return None # Failure!

            if link.boundedDistance is not None and minPathLen <= link.boundedDistance <= maxPathLen:
                at = link.boundedNext
            elif link.unboundedDistance is not None and link.unboundedDistance <= maxPathLen:
                at = link.unboundedNext
            else:
                # No path exists!
                return None

            path.append(at.point)
            minPathLen -= 1
            maxPathLen -= 1

        return path

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
    node = None

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
