from DNANode import DNANode
from DNAParser import *
from panda3d.core import *

class DNAProp(DNANode):
    TAG = 'prop'

    def __init__(self, name, code):
        DNANode.__init__(self, name)

        self.name = name
        self.code = code

    def _makeNode(self, storage, parent):
        node = storage.findNode(self.code).copyTo(parent)
        return node


registerElement(DNAProp)
