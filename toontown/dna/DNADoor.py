from DNANode import DNANode
from DNAParser import *
from panda3d.core import *

class DNADoor(DNANode):
    TAG = 'door'
    PARENTS = ['landmark_building']

    def __init__(self, code):
        DNANode.__init__(self, 'door')

        self.code = code

    def _makeNode(self, storage, parent):
        pass # TODO

registerElement(DNADoor)
