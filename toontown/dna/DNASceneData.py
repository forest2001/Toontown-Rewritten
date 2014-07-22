from DNAParser import *
import DNAStoreSuitPoint
import ctypes

class DNASuitGraph(object):
    def __init__(self, points, edges):
        self.points = points
        self.edges = edges

        self._pointId2point = {}
        self._point2outboundEdges = {}
        self._point2inboundEdges = {}

        self._table = (ctypes.c_uint16*4 * len(points)*len(points))()
        ctypes.memset(self._table, 0xFF, ctypes.sizeof(self._table))

        if points:
            highestId = max(point.id for point in points)
            self._id2index = (ctypes.c_uint16 * (highestId+1))()

        for i,point in enumerate(points):
            self._pointId2point[point.id] = point
            self._id2index[point.id] = i

        for edge in edges:
            try:
                a = self._pointId2point[edge.a]
                b = self._pointId2point[edge.b]
            except KeyError:
                raise DNAError('Edge connects a nonexistent point!')

            self._point2outboundEdges.setdefault(a, []).append(edge)
            self._point2inboundEdges.setdefault(b, []).append(edge)

        visited = (ctypes.c_uint16*len(points))()
        for i, point in enumerate(points):
            for neighbor in self.getOriginPoints(point):
                self.addLink(neighbor, point, 1, point, False, visited)

    def addLink(self, point, neighbor, distance, destination, unbounded, visited):
        pointIndex = self._id2index[point.id]
        neighborIndex = self._id2index[neighbor.id]
        destinationIndex = self._id2index[destination.id]

        if visited[pointIndex]:
            # Loop detected! Modify the unbounded route:
            unbounded = True

        visited[pointIndex] += 1

        entry = self._table[pointIndex][destinationIndex]

        existingDistance = entry[3] if unbounded else entry[1]
        if distance < existingDistance:
            if not unbounded:
                entry[0] = neighborIndex
                entry[1] = distance
            else:
                entry[2] = neighborIndex
                entry[3] = distance

            # We've just updated our link. If we're traversable, announce the
            # new route to all of our neighbors:
            traversable = point.type in (DNAStoreSuitPoint.STREETPOINT,
                                         DNAStoreSuitPoint.COGHQINPOINT,
                                         DNAStoreSuitPoint.COGHQOUTPOINT)
            if traversable:
                for neighbor in self.getOriginPoints(point):
                    self.addLink(neighbor, point, distance+1, destination, unbounded, visited)

        visited[pointIndex] -= 1

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
        start = self._id2index[startPoint.id]
        end = self._id2index[endPoint.id]

        at = start
        path = [startPoint]

        while at != end or minPathLen > 0:
            boundedNext, boundedDistance, unboundedNext, unboundedDistance = self._table[at][end]

            if minPathLen <= boundedDistance <= maxPathLen:
                at = boundedNext
            elif unboundedDistance <= maxPathLen:
                at = unboundedNext
            else:
                # No path exists!
                return None

            path.append(self.points[at])
            minPathLen -= 1
            maxPathLen -= 1

        return path

    def getAdjacentPoints(self, point):
        return [self.getPointFromIndex(edge.b) for edge in self.getEdgesFrom(point)]

    def getOriginPoints(self, point):
        return [self.getPointFromIndex(edge.a) for edge in self.getEdgesTo(point)]

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
