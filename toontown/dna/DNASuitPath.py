class DNASuitPath:
    def __init__(self):
        self.points = []

    def addPoint(self, point):
        self.points.append(point)

    def getNumPoints(self):
        return len(self.points)

    def getPoint(self, index):
        return self.points[index]

    def getPointIndex(self, index):
        return self.points[index].getIndex()
