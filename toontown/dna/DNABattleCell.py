from DNASceneElement import DNASceneElement
from DNAParser import *
from panda3d.core import *

class DNABattleCell(DNASceneElement):
    TAG = 'battle_cell'
    PARENTS = ['visgroup']

    def __init__(self, width, height, x, y, z):
        DNASceneElement.__init__(self)

        self.width = float(width)
        self.height = float(height)
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    # TODO: Put stuff in the data pass.

registerElement(DNABattleCell)
