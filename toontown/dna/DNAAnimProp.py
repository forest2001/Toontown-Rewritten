from DNAProp import DNAProp
from DNAParser import *
from panda3d.core import *

class DNAAnimProp(DNAProp):
    TAG = 'anim_prop'

    def __init__(self, name, code, anim):
        DNAProp.__init__(self, name, code)

        self.anim = anim

    def _makeNode(self, parent, storage):
        node = DNAProp._makeNode(self, parent, storage)

        node.setTag('DNAAnim', self.anim)

        return node


registerElement(DNAAnimProp)
