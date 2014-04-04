from DNASceneElement import DNASceneElement
from DNAParser import *
from panda3d.core import *

class DNABaseline(DNASceneElement):
    TAG = 'baseline'
    PARENTS = ['sign']

    def __init__(self, code=None, flags='', wiggle='0', stumble='0', stomp='0', kern='0', width='0', height='0'):
        DNASceneElement.__init__(self)

        self.code = code
        self.flags = flags
        self.wiggle = float(wiggle)
        self.stumble = float(stumble)
        self.stomp = float(stomp)
        self.kern = float(kern)
        self.width = float(width)
        self.height = float(height)

    def _makeNode(self, storage, parent):
        pass # TODO

registerElement(DNABaseline)
