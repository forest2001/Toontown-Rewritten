from DNANode import DNANode
from DNAParser import *
from panda3d.core import *

class DNAWindows(DNANode):
    TAG = 'windows'
    PARENTS = ['wall']

    def __init__(self, code, count="0"):
        DNANode.__init__(self, 'windows')

        self.code = code
        self.count = int(count)

    def _makeNode(self, storage, parent):
        node = storage.findNode(self.code)
        if node is None:
            raise DNAError('DNAWindows uses unknown code %s' % self.code)

        windows = parent.attachNewNode('windows')
        windows.setDepthOffset(self.DEPTH_OFFSET)

        for i in xrange(self.count):
            x = (i + 1)/(self.count + 1.0)

            np = node.copyTo(windows)
            np.setScale(np.getTop(), 1, 1, 1)
            np.setX(x)
            np.setZ(0.5)

registerElement(DNAWindows)
