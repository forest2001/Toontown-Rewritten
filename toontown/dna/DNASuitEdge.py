from DNASceneElement import DNASceneElement
from DNAParser import *
from panda3d.core import *

class DNASuitEdge(DNASceneElement):
    TAG = 'suit_edge'
    PARENTS = ['visgroup']

    def __init__(self, a, b):
        DNASceneElement.__init__(self)

        self.a = int(a)
        self.b = int(b)

    def _storeData(self, data):
        data.suitEdges.append(self)

registerElement(DNASuitEdge)
