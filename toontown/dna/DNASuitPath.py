class DNASuitPath:
    def __init__(self):
        self.points = []

    def addPoint(self, point):
        self.points.append(point)

    def getPoints(self, index):
        return self.points

    def getPointIndex(self, index):
        return self.points[index].getIndex()
