from DNASceneElement import DNASceneElement
from DNAParser import *
from panda3d.core import *

class DNAWall(DNASceneElement):
    TAG = 'wall'
    PARENTS = ['flat_building']

    def __init__(self, code, height="0"):
        DNASceneElement.__init__(self)

        self.code = code
        self.height = float(height)

    def _makeNode(self, storage, parent):
        pass # TODO

registerElement(DNAWall)
