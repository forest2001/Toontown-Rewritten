from DNASceneElement import DNASceneElement
from DNAParser import *
from panda3d.core import *

class DNAGroup(DNASceneElement):
    TAG = 'group'
    PARENTS = ['scene', 'group', 'node', 'visgroup', 'prop', 'landmark_building',
               'flat_building']

    def __init__(self, name):
        DNASceneElement.__init__(self)

        self.name = name
        
    def getName(self):
        return self.name

    def _makeNode(self, storage, parent):
        return parent.attachNewNode(self.name)

registerElement(DNAGroup)
