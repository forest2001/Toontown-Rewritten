from DNANode import DNANode
from DNAParser import *
from DNATexture import DNATexture
from panda3d.core import *

class DNAStreet(DNANode):
    TAG = 'street'

    def __init__(self, name, code):
        DNANode.__init__(self, name)

        self.name = name
        self.code = code

    def _makeNode(self, storage, parent):
        node = storage.findNode(self.code)
        if node is None:
            raise DNAError('DNAStreet uses unknown code %s' % self.code)

        np = node.copyTo(parent)

        for textureElement, nodeName in zip(self.findChildren(DNATexture),
                                            ('street', 'sidewalk', 'curb')):
            texture = storage.findTexture(textureElement.code)
            if texture is None:
                raise DNAError('DNATexture uses unknown code %s' % textureElement.code)

            texNode = np.find('**/*_' + nodeName)
            if not texNode.isEmpty():
                texNode.setTexture(texture, 1)

        return np


registerElement(DNAStreet)
