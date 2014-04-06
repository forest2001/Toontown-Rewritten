from DNAGroup import DNAGroup
from DNAParser import *
from panda3d.core import *

class DNALandmarkBuilding(DNAGroup):
    TAG = 'landmark_building'

    def __init__(self, id, code, type=None):
        DNAGroup.__init__(self, id)

        self.id = id
        self.code = code
        self.type = type

    def _makeNode(self, storage, parent):
        pass # TODO

registerElement(DNALandmarkBuilding)
