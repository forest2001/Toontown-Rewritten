from DNANode import DNANode
from DNAParser import *
from panda3d.core import *

class DNALandmarkBuilding(DNANode):
    TAG = 'landmark_building'

    def __init__(self, id, code, type=None):
        DNANode.__init__(self, id)

        self.id = id
        self.code = code
        self.type = type

    def _makeNode(self, storage, parent):
        node = storage.findNode(self.code)
        if node is None:
            raise DNAError('DNALandmarkBuilding uses unknown code %s' % self.code)
        return node.copyTo(parent)

registerElement(DNALandmarkBuilding)
