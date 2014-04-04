from DNAPropertyElement import DNAPropertyElement
from DNAParser import *
from panda3d.core import *

class DNAScale(DNAPropertyElement):
    TAG = 'scale'

    def __init__(self, x="1", y="1", z="1"):
        DNAPropertyElement.__init__(self)

        self.scale = (float(x), float(y), float(z))

    def _apply(self, parent):
        parent.setScale(self.scale)

registerElement(DNAScale)
