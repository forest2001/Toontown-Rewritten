from DNAGroup import DNAGroup
from DNAParser import *
from panda3d.core import *

class DNASign(DNAGroup):
    TAG = 'sign'

    def __init__(self, code=None):
        DNAGroup.__init__(self, code or 'sign')

        self.code = code

    def _makeNode(self, storage, parent):
        node = storage.findNode(self.code) or NodePath(self.name)

        parentSignOrigin = parent.find('**/*sign_origin') or parent
        sign = node.copyTo(parentSignOrigin)

        sign.setDepthOffset(50)

        return sign

registerElement(DNASign)
