from DNANode import DNANode
from DNAParser import *
from panda3d.core import *

class DNACornice(DNANode):
    TAG = 'cornice'
    PARENTS = ['wall']

    def __init__(self, code):
        DNANode.__init__(self, 'cornice')

        self.code = code

    def _makeNode(self, storage, parent):
        pass # TODO

registerElement(DNACornice)
