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
        pass # TODO

registerElement(DNAWindows)
