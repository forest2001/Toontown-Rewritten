from DNAElement import DNAElement
from DNAParser import *

class DNASceneElement(DNAElement):
    def __init__(self):
        DNAElement.__init__(self)

        self.code = None

    def _generate(self, storage, parent):
        node = self._makeNode(storage, parent)

        if node:
            node.setTag('DNARoot', self.TAG)
            if self.code is not None:
                node.setTag('DNACode', self.code)

            for child in self._children:
                child._generate(storage, node)

    def _makeNode(self, storage, parent):
        pass # Overridable by subclass
