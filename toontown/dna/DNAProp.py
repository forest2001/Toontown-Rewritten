from DNASceneElement import DNASceneElement
from DNAParser import *
from panda3d.core import *

class DNAProp(DNASceneElement):
    TAG = 'prop'
    PARENTS = ['group', 'node', 'visgroup', 'prop', 'landmark_building']

    def __init__(self, name, code):
        DNASceneElement.__init__(self)

        self.name = name
        self.code = code

    def _makeNode(self, storage, parent):
        node = storage.requestNode(self.code).copyTo(parent)
        node.setName(self.name)
        return node


registerElement(DNAProp)
