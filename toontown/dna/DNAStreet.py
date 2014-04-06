from DNANode import DNANode
from DNAParser import *
from panda3d.core import *

class DNAStreet(DNANode):
    TAG = 'street'

    def __init__(self, name, code):
        DNANode.__init__(self, name)

        self.name = name
        self.code = code

    def _makeNode(self, storage, parent):
        node = storage.findNode(self.code)
        if node is None:
            raise DNAError('DNAStreet uses unknown code %s' % self.code)

        return node.copyTo(parent)


registerElement(DNAStreet)
