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
        node = storage.findNode(self.code)
        if node:
            np = node.copyTo(parent)
            np.setName(self.name)
            return np

    def getName(self):
        return self.name
        
    def getCode(self):
        return self.code


registerElement(DNAProp)
