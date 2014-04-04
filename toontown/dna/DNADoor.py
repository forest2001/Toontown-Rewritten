from DNASceneElement import DNASceneElement
from DNAParser import *
from panda3d.core import *

class DNADoor(DNASceneElement):
    TAG = 'door'
    PARENTS = ['landmark_building']

    def __init__(self, code):
        DNASceneElement.__init__(self)

        self.code = code

    def _makeNode(self, storage, parent):
        pass # TODO

registerElement(DNADoor)
