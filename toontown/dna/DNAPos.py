from DNAPropertyElement import DNAPropertyElement
from DNAParser import *
from panda3d.core import *

class DNAPos(DNAPropertyElement):
    TAG = 'pos'

    def __init__(self, x="0", y="0", z="0"):
        DNAPropertyElement.__init__(self)

        self.pos = (float(x), float(y), float(z))

    def _apply(self, parent):
        parent.setPos(self.pos)

registerElement(DNAPos)
