from DNASceneElement import DNASceneElement
from DNAParser import *
from panda3d.core import *

class DNASign(DNASceneElement):
    TAG = 'sign'
    PARENTS = ['prop', 'landmark_building']

    def __init__(self, code=None):
        DNASceneElement.__init__(self)

        self.code = code

    def _makeNode(self, storage, parent):
        pass # TODO

registerElement(DNASign)
