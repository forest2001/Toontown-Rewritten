from DNANode import DNANode
from DNAParser import *
from panda3d.core import *

class DNAFlatBuilding(DNANode):
    TAG = 'flat_building'

    def __init__(self, id, width="0"):
        DNANode.__init__(self, id)

        self.id = id
        self.width = float(width)

    def _makeNode(self, storage, parent):
        return parent.attachNewNode(self.id)

registerElement(DNAFlatBuilding)
