from DNAParser import *

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

class DNASceneData:
    def __init__(self):
        self.visgroups = []

        self.suitPoints = []
        self.suitEdges = []
        self.suitGraph = None

    def update(self):
        self.suitGraph = DNASuitGraph(self.suitPoints, self.suitEdges)
