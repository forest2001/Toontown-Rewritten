from DNADoor import DNADoor
from DNAParser import *
from panda3d.core import *

class DNAFlatDoor(DNADoor):
    TAG = 'flat_door'
    PARENTS = ['wall']

    def __init__(self, code):
        DNADoor.__init__(self, code)

        self.code = code

    def _makeNode(self, storage, parent):
        pass # TODO

registerElement(DNAFlatDoor)
