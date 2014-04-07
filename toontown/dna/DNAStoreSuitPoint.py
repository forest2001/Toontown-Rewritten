from DNASceneElement import DNASceneElement
from DNAParser import *
from panda3d.core import *


STREETPOINT = 0
FRONTDOORPOINT = 1
SIDEDOORPOINT = 2
COGHQINPOINT = 3
COGHQOUTPOINT = 4

class DNAStoreSuitPoint(DNASceneElement):
    TAG = 'store_suit_point'
    PARENTS = ['scene']

    def __init__(self, id, type, x, y, z, building=None):
        DNASceneElement.__init__(self)

        self.id = int(id)
        self.type = type
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self.building = building and int(building)

    def getPointType(self):
        return self.type

    def getIndex(self):
        return self.id

    def _storeData(self, data):
        data.suitPoints.append(self)

registerElement(DNAStoreSuitPoint)
