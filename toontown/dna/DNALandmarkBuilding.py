from DNASceneElement import DNASceneElement
from DNAParser import *
from panda3d.core import *

class DNALandmarkBuilding(DNASceneElement):
    TAG = 'landmark_building'
    PARENTS = ['group', 'node', 'visgroup']

    def __init__(self, id, code, type=None):
        DNASceneElement.__init__(self)

        self.id = id
        self.code = code
        self.type = type

    def _makeNode(self, storage, parent):
        pass # TODO

registerElement(DNALandmarkBuilding)
