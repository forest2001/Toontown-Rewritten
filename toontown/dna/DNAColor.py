from DNAPropertyElement import DNAPropertyElement
from DNAParser import *
from panda3d.core import *

class DNAColor(DNAPropertyElement):
    TAG = 'color'

    def __init__(self, r="1", g="1", b="1", a="1"):
        DNAPropertyElement.__init__(self)

        self.color = (float(r), float(g), float(b), float(a))

    def _apply(self, parent):
        parent.setColor(self.color)

registerElement(DNAColor)
