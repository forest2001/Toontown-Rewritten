from DNAElement import DNAElement
from DNAParser import *

class DNASceneElement(DNAElement):
    def __init__(self):
        DNAElement.__init__(self)

        self.code = None
        self.name = ''

    def _generate(self, storage, parent):
        node = self._makeNode(storage, parent)

        if node:
            node.setTag('DNARoot', self.TAG)
            if self.code is not None:
                node.setTag('DNACode', self.code)

            for child in self.children:
                child._generate(storage, node)

            self._postGenerate(node)

    def _makeNode(self, storage, parent):
        pass # Overridable by subclass

    def _postGenerate(self, node):
        pass # Overridable by subclass.

    def _getData(self, data):
        self._storeData(data)

        for child in self.children:
            child._getData(data)

    def _storeData(self, data):
        pass # Also overridable by subclass.


    # Lookup functions:
    def getVisGroup(self):
        if self.parent is not None:
            return self.parent.getVisGroup()
        else:
            return None
