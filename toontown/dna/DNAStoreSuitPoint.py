from DNASceneElement import DNASceneElement
from DNAParser import *
from panda3d.core import *

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

    # TODO: Put stuff in the data pass.

registerElement(DNAStoreSuitPoint)
