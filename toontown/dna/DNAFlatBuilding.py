from DNASceneElement import DNASceneElement
from DNAParser import *
from panda3d.core import *

class DNAFlatBuilding(DNASceneElement):
    TAG = 'flat_building'
    PARENTS = ['group', 'node', 'visgroup']

    def __init__(self, id, width="0"):
        DNASceneElement.__init__(self)

        self.id = id
        self.width = float(width)

    def _makeNode(self, storage, parent):
        pass # TODO

registerElement(DNAFlatBuilding)
