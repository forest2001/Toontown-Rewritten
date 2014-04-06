from DNASceneElement import DNASceneElement
from DNAParser import *
from panda3d.core import *

class DNAWall(DNASceneElement):
    TAG = 'wall'
    PARENTS = ['flat_building']

    def __init__(self, code, height="0"):
        DNASceneElement.__init__(self)

        self.code = code
        self.height = float(height)

    def _makeNode(self, storage, parent):
        node = storage.findNode(self.code)
        if node is None:
            raise DNAError('DNAWall uses unknown code %s' % self.code)

        buildingHeight = parent.getPythonTag('wall_height') or 0.0

        wall = node.copyTo(parent)
        wall.setScale(self._parent.width, 1, self.height)
        wall.setZ(buildingHeight)
        parent.setPythonTag('wall_height', buildingHeight + self.height)

        return wall

registerElement(DNAWall)
