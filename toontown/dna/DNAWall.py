from DNANode import DNANode
from DNAParser import *
from panda3d.core import *

class DNAWall(DNANode):
    TAG = 'wall'
    PARENTS = ['flat_building']

    def __init__(self, code, height="0"):
        DNANode.__init__(self, 'wall')

        self.code = code
        self.height = float(height)

    def _makeNode(self, storage, parent):
        node = storage.findNode(self.code)
        if node is None:
            raise DNAError('DNAWall uses unknown code %s' % self.code)

        buildingHeight = parent.getPythonTag('wall_height') or 0.0

        wall = node.copyTo(parent)
        wall.setScale(self.parent.width, 1, self.height)
        wall.setZ(buildingHeight)
        parent.setPythonTag('wall_height', buildingHeight + self.height)

        return wall

registerElement(DNAWall)
