from DNAElement import DNAElement
from DNAParser import *

class DNASceneElement(DNAElement):
    def __init__(self):
        DNAElement.__init__(self)

        self.code = None

    def _generate(self, storage, parent):
        node = self._makeNode(storage, parent)
        node.setTag('DNARoot', self.TAG)
        node.setTag('DNACode', self.code)

        if node:
            for child in self._children:
                child._generate(storage, node)

    def _makeNode(self, storage, parent):
        pass # Overridable by subclass
