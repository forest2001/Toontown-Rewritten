from DNANode import DNANode
from DNAParser import *
from panda3d.core import *

class DNAFlatDoor(DNANode):
    TAG = 'flat_door'
    PARENTS = ['wall']

    def __init__(self, code):
        DNANode.__init__(self, code)

        self.code = code

    def _makeNode(self, storage, parent):
        node = storage.findNode(self.code)
        if node is None:
            raise DNAError('DNAFlatDoor uses unknown code %s' % self.code)

        np = node.copyTo(parent)
        np.setScale(np.getTop(), (1, 1, 1)) # No net scale
        np.setPos(0.5, 0, 0) # Centered within the wall

        # Appear on top of wall:
        np.setDepthOffset(self.DEPTH_OFFSET)

        return np

registerElement(DNAFlatDoor)
