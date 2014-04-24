from DNANode import DNANode
from DNAParser import *
from panda3d.core import *

class DNASign(DNANode):
    TAG = 'sign'

    def __init__(self, code=None):
        DNANode.__init__(self, code or 'sign')

        self.code = code

    def _makeNode(self, storage, parent):
        node = storage.findNode(self.code) or NodePath(self.name)

        parentSignOrigin = parent.find('**/*sign_origin') or parent
        sign = node.copyTo(parentSignOrigin)

        sign.setDepthOffset(self.DEPTH_OFFSET)

        return sign

registerElement(DNASign)
