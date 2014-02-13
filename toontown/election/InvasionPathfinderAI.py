import bisect
from pandac.PandaModules import *

class InvasionPathfinderAI:
    def __init__(self, polygons=None):
        self.borders = []
        self.vertices = []

        if polygons:
            for polygon in polygons:
                self.addPolygon(polygon)
            self.buildNeighbors()

    def addPolygon(self, points):
        newVertices = []
        for i,point in enumerate(points):
            prevPoint = points[i-1]
            x, y = point

            # Add a boundary line from the previous to here:
            x2, y2 = prevPoint
            self.borders.append((x2, y2, x, y))

            # Create our vertex:
            vertex = AStarVertex(Point2(x, y))
            self.vertices.append(vertex)
            newVertices.append(vertex)

        # Now set up the polygonal neighbors on all vertices:
        for i,vertex in enumerate(newVertices):
            prevVertex = newVertices[i-1]
            nextVertex = newVertices[(i+1)%len(newVertices)]

            vertex.setPolygonalNeighbors(prevVertex, nextVertex)

            if vertex.interiorAngle > 180:
                # This vertex is concave. Nothing is ever going to *walk to* it
                # in order to go somewhere else, so we can actually exclude it
                # from the pathfinding system.
                self.vertices.remove(vertex)

    def buildNeighbors(self):
        # First reset all vertex neighbors:
        for vertex in self.vertices:
            vertex.resetNeighbors()

        # Now we test every vertex pair for visibility to each other:
        for i,v1 in enumerate(self.vertices):
            for v2 in self.vertices[i+1:]:
                self._considerLink(v1, v2)

    def planPath(self, fromPoint, toPoint):
        # Find a path from fromPoint to toPoint, and return it as a series of
        # waypoints (including toPoint, excluding fromPoint).
        # If a direct path exists, this will simply return [toPoint].
        # If no direct path exists, the pathfinder will use the A* algorithm to
        # generate a path linking the two points.
        # If no path is possible, this function returns None.

        # See if the fromPoint->toPoint path crosses any polygons:
        x1, y1 = fromPoint
        x2, y2 = toPoint
        if not self._testLineIntersections((x1, y1, x2, y2), self.borders):
            # Nope, we can just go direct!
            return [toPoint]

        # Pathfinding is necessary. First, create the endpoint vertices:
        fromVertex = AStarVertex(Point2(x1, y1))
        toVertex = AStarVertex(Point2(x2, y2))

        # Now create edges for both vertices:
        for vertex in self.vertices:
            self._considerLink(vertex, fromVertex)
            self._considerLink(vertex, toVertex)

        try:
            # Run A* search:
            astar = AStarSearch()
            result = astar.search(fromVertex, toVertex)

            if result:
                return [vertex.pos for vertex in result]
            else:
                return None
        finally:
            # Clean up the temporary vertices:
            fromVertex.unlinkAll()
            toVertex.unlinkAll()

    def _considerLink(self, v1, v2):
        # If the vertices are polygonal neighbors, they should also be
        # edges on the nav graph:
        if v1.isVertexPolygonalNeighbor(v2):
            v1.link(v2)
            return

        # First, test to make sure a link between the vertices would not
        # go across the inside of a polygon (even if there are no line
        # segments in the way)
        if v1.isVertexInsideAngle(v2) or v2.isVertexInsideAngle(v1):
            return # These vertices are not "facing" each other.

        # As an optimization, if either vertex is inside the other's
        # vertically opposite angle, no link between them will ever be
        # used, since neither vertex will obstruct the other.
        if v1.isVertexInsideOpposite(v2) or v2.isVertexInsideOpposite(v1):
            return

        # Now test for intersections with any of the polygon borders:
        x1, y1 = v1.pos
        x2, y2 = v2.pos
        if self._testLineIntersections((x1, y1, x2, y2), self.borders):
            return # Nope, a border is in the way!

        # If we made it here, the two vertices can "see" each other and
        # should thus be made neighbors for pathfinding purposes.
        v1.link(v2)

    ############################################################################
    # If you are allergic to linear math, stop reading this file and consult   #
    # your doctor right away.                                                  #
    ############################################################################
    def _makeLineMat(self, x1, y1, x2, y2):
        # This function generates a transformation matrix to convert coordinates
        # from worldspace to be local to the provided line.

        # This matrix will do the forward transformation. In other words, it
        # transforms (0, 0) -> (x1, y1) and (0, 1) -> (x2, y2)
        # N.B. the notation below is the transpose of the matrix I'm defining,
        # because Panda3D's Mat3 constructor is column-major.
        mat = Mat3(
            y2-y1, x1-x2, 0,
            x2-x1, y2-y1, 0,
               x1,    y1, 1)

        # Now we invert it, so that it does what we want: the reverse
        # transformation (i.e. (x1, y1) -> (0, 0) and (x2, y2) -> (0, 1))
        if not mat.invertInPlace():
            # The matrix is singular, which means it has no inverse.
            return None

        return mat

    def _testLineIntersections(self, incident, lines):
        # Tests if "incident" intersects any of the lines in the "lines" list.
        # Each line is a tuple of (x1, y1, x2, y2).

        x1, y1, x2, y2 = incident
        mat = self._makeLineMat(x1, y1, x2, y2)

        if not mat:
            # The incident line is not valid, and so an inverse transformation
            # cannot be made. The line is probably 0-length or otherwise cannot
            # intersect anything anyway, so we'll just say it's okay:
            return False

        for x1, y1, x2, y2 in lines:
            # First let's transform the endpoints of the line.
            # N.B. this uses homogeneous coordinates, hence the use of
            # 3-dimensional points.
            x1, y1, _ = mat.xform(Point3(x1, y1, 1))
            x2, y2, _ = mat.xform(Point3(x2, y2, 1))

            # In order for an intersection to be happening, one point must be
            # on our left (negative X) and one on our right (positive X):
            if not ((x1 < 0 and x2 > 0) or (x1 > 0 and x2 < 0)):
                # This line has both points on one side of us, no intersection
                # is possible. Skip it.
                continue

            # As the points are on opposite sides, we need to find the line's
            # y-intercept.
            m = (y2-y1)/(x2-x1)
            b = m*-x1 + y1

            # If the y-intercept is between 0-1, we have an intersection, as our
            # incident line runs from (0,0)->(0,1) in this coordinate space.
            # This is an exclusive range as *grazing* the line (skimming by one
            # of its endpoints) is OK.
            epsilon = 0.001
            if 0.0+epsilon < b < 1.0-epsilon:
                return True

        # The for loop concluded, nothing found.
        return False

class AStarVertex:
    def __init__(self, pos):
        self.pos = pos

        self.neighbors = []

        self.prevPolyNeighbor = None
        self.nextPolyNeighbor = None
        self.interiorAngle = None

    def link(self, neighbor):
        self.__addNeighbor(neighbor)
        neighbor.__addNeighbor(self)

    def unlink(self, neighbor):
        self.__removeNeighbor(neighbor)
        neighbor.__removeNeighbor(self)

    def unlinkAll(self):
        neighbors = list(self.neighbors)
        for neighbor in neighbors:
            self.unlink(neighbor)

    def resetNeighbors(self):
        self.neighbors = []

    def __addNeighbor(self, neighbor):
        if neighbor not in self.neighbors:
            self.neighbors.append(neighbor)

    def __removeNeighbor(self, neighbor):
        if neighbor in self.neighbors:
            self.neighbors.remove(neighbor)

    def setPolygonalNeighbors(self, prev, next):
        vecToPrev = prev.pos - self.pos
        vecToNext = next.pos - self.pos

        angle = vecToPrev.signedAngleDeg(vecToNext)
        angle %= 360 # Convert this to an unsigned angle.

        self.prevPolyNeighbor = prev
        self.nextPolyNeighbor = next
        self.interiorAngle = angle

    def isVertexInsideAngle(self, other):
        if self.prevPolyNeighbor is None or self.interiorAngle is None:
            # We are a single vertex, not part of a polygon. Nothing can be
            # "inside" the angle.
            return False

        vecToPrev = self.prevPolyNeighbor.pos - self.pos
        vecToOther = other.pos - self.pos

        angle = vecToPrev.signedAngleDeg(vecToOther)
        angle %= 360 # Convert this to an unsigned angle.

        # 'angle' represents the degrees CCW from the vecToPrev, while
        # self.interiorAngle represents the overall degrees CCW that our corner
        # has (and it may be >180 if this is a concave angle). Therefore, if the
        # 'other' vertex is inside our interior angle, angle < interiorAngle.
        return angle < self.interiorAngle

    def isVertexInsideOpposite(self, other):
        if self.prevPolyNeighbor is None or self.interiorAngle is None:
            # We are a single vertex, not part of a polygon. Nothing can be
            # "inside" the angle.
            return False

        vecToPrev = self.prevPolyNeighbor.pos - self.pos
        vecToOther = other.pos - self.pos

        angle = vecToPrev.signedAngleDeg(vecToOther)
        angle -= 180 # Spin it around to test the opposite.
        angle %= 360 # Convert this to an unsigned angle.

        return angle < self.interiorAngle

    def isVertexPolygonalNeighbor(self, other):
        return other in (self.prevPolyNeighbor, self.nextPolyNeighbor)

    # The 3 functions required by AStarSearch:
    def getNeighbors(self):
        return self.neighbors

    def getHeuristicTo(self, other):
        return (self.pos-other.pos).length()

    def getCostTo(self, other):
        return (self.pos-other.pos).length()

class AStarSearch:
    def __init__(self):
        self.openList = []
        self.closed = set()
        self.paths = {}

        self._toVertex = None

    def search(self, fromVertex, toVertex):
        self.openList = [AStarPath(None, fromVertex, 0, 0)]
        self.closed = set()
        self.paths = {}

        self._toVertex = toVertex
        while self.openList and toVertex not in self.paths:
            self.__doIteration()

        # Did we find something?
        path = self.paths.get(toVertex)
        if not path:
            # We failed. And the test will be terminated.
            return None

        return self.__getVerticesToPath(path)

    def __doIteration(self):
        path = self.openList.pop(0)
        vertex = path.vertex
        self.closed.add(vertex)

        neighbors = vertex.getNeighbors()
        for neighbor in neighbors:
            if neighbor in self.closed:
                # We already visited this neighbor; ignore.
                continue

            cost = vertex.getCostTo(neighbor) + path.totalCost

            if neighbor in self.paths:
                # There is already a path to this neighbor (i.e. they are
                # probably already on the open list) so we'll see if our
                # path's cost better, and replace it if so.
                neighborPath = self.paths[neighbor]
                if cost < neighborPath.totalCost:
                    # Yes, we're cheaper!
                    self.openList.remove(neighborPath)
                    del self.paths[neighbor]
                else:
                    # No, we're the same or more expensive; ignore this
                    # neighbor.
                    continue

            newPath = AStarPath(path, neighbor, cost, neighbor.getHeuristicTo(self._toVertex))
            self.paths[neighbor] = newPath
            bisect.insort(self.openList, newPath)

    def __getVerticesToPath(self, path):
        # Traces backwards along all of path's parents to build up a forward list
        # of vertices to visit along the path.
        result = []
        while path is not None:
            result.insert(0, path.vertex)
            path = path.parent
        return result

class AStarPath:
    def __init__(self, parent, vertex, cost, heuristic):
        self.parent = parent
        self.vertex = vertex
        self.heuristic = heuristic
        self.totalCost = cost

    def __cmp__(self, other):
        return cmp(self.totalCost + self.heuristic,
                   other.totalCost + other.heuristic)
