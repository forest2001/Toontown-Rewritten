from DNAPropertyElement import DNAPropertyElement
from DNAParser import *
from panda3d.core import *

class DNAHpr(DNAPropertyElement):
    TAG = 'hpr'

    def __init__(self, h="0", p="0", r="0"):
        DNAPropertyElement.__init__(self)

        self.hpr = (float(h), float(p), float(r))

    def _apply(self, parent):
        parent.setHpr(self.hpr)

registerElement(DNAHpr)
