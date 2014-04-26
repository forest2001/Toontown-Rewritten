from DNASceneElement import DNASceneElement
from DNAParser import *
from panda3d.core import *


STREETPOINT = 0
FRONTDOORPOINT = 1
SIDEDOORPOINT = 2
COGHQINPOINT = 3
COGHQOUTPOINT = 4
 
pointTypeMap = {
  'STREET_POINT' : 0,
  'FRONT_DOOR_POINT' : 1,
  'SIDE_DOOR_POINT' : 2,
  'COGHQ_IN_POINT' : 3,
  'COGHQ_OUT_POINT' : 4
}

class DNAStoreSuitPoint(DNASceneElement):
    TAG = 'store_suit_point'
    PARENTS = ['scene']

    def __init__(self, id, type, x, y, z, building=None):
        DNASceneElement.__init__(self)

        self.id = int(id)
        self.type = pointTypeMap[type]
        self.pos = Point3(float(x), float(y), float(z))
        self.building = (building and int(building)) or -1

    def getPointType(self):
        return self.type

    def getIndex(self):
        return self.id

    def getPos(self):
        return self.pos

    def getLandmarkBuildingIndex(self):
        return self.building

    def _storeData(self, data):
        data.suitPoints.append(self)

registerElement(DNAStoreSuitPoint)
