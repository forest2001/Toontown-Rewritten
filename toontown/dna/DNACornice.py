from DNANode import DNANode
from DNAParser import *
from panda3d.core import *

class DNACornice(DNANode):
    TAG = 'cornice'
    PARENTS = ['wall']

    def __init__(self, code):
        DNANode.__init__(self, 'cornice')

        self.code = code

    def _makeNode(self, storage, parent):
        node = storage.findNode(self.code)
        if node is None:
            raise DNAError('DNACornice uses unknown code %s' % self.code)

        np = node.copyTo(parent)
        np.setZ(1)
        np.setDepthOffset(50) # Appear on top of the wall.

        return np

registerElement(DNACornice)
