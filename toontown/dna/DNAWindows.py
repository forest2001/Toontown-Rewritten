from DNASceneElement import DNASceneElement
from DNAParser import *
from panda3d.core import *

class DNAWindows(DNASceneElement):
    TAG = 'windows'
    PARENTS = ['wall']

    def __init__(self, code, count="0"):
        DNASceneElement.__init__(self)

        self.code = code
        self.count = int(count)

    def _makeNode(self, storage, parent):
        pass # TODO

registerElement(DNAWindows)
