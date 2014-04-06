from DNASceneElement import DNASceneElement
from DNAParser import *
from panda3d.core import *

class DNAGraphic(DNASceneElement):
    TAG = 'graphic'
    PARENTS = ['baseline']

    def __init__(self, code):
        DNASceneElement.__init__(self)

        self.code = code

    def _makeNode(self, storage, parent):
        node = storage.findNode(self.code)
        if node is None:
            raise DNAError('DNAGraphic uses unknown code %s' % self.code)
        return node.copyTo(parent)

registerElement(DNAGraphic)
