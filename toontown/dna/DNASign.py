from DNAGroup import DNAGroup
from DNAParser import *
from panda3d.core import *

class DNASign(DNAGroup):
    TAG = 'sign'

    def __init__(self, code=None):
        DNAGroup.__init__(self, code or 'sign')

        self.code = code

    def _makeNode(self, storage, parent):
        pass # TODO

registerElement(DNASign)
