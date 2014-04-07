from DNANode import DNANode
from DNAParser import *
from panda3d.core import *

class DNABaseline(DNANode):
    TAG = 'baseline'
    PARENTS = ['sign']

    def __init__(self, code=None, flags='', wiggle='0', stumble='0', indent='0', stomp='0', kern='0', width='0', height='0'):
        DNANode.__init__(self, 'baseline')

        self.code = code
        self.flags = flags

        # TODO: Text spacing parameters must have the scaling factor applied.
        self.wiggle = float(wiggle)
        self.stumble = float(stumble)
        self.indent = float(indent)
        self.stomp = float(stomp)
        self.kern = float(kern)
        self.width = float(width)
        self.height = float(height)

    def _makeNode(self, storage, parent):
        np = parent.attachNewNode('baseline')

        # Don't z-fight with the sign.
        np.setDepthOffset(50)

        return np

registerElement(DNABaseline)
