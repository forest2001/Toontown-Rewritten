from DNASceneElement import DNASceneElement
from DNAParser import *
from panda3d.core import *

class DNAGroup(DNASceneElement):
    TAG = 'group'
    PARENTS = ['scene', 'visgroup']

    def __init__(self, name):
        DNASceneElement.__init__(self)

        self.name = name

    def _makeNode(self, storage, parent):
        return parent.attachNewNode(self.name)

registerElement(DNAGroup)
