from DNAGroup import DNAGroup
from DNAParser import *
from panda3d.core import *

class DNAFlatBuilding(DNAGroup):
    TAG = 'flat_building'

    def __init__(self, id, width="0"):
        DNAGroup.__init__(self, id)

        self.id = id
        self.width = float(width)

    def _makeNode(self, storage, parent):
        pass # TODO

registerElement(DNAFlatBuilding)
