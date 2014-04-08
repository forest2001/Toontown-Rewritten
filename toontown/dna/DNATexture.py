from DNASceneElement import DNASceneElement
from DNAParser import *
from panda3d.core import *

class DNATexture(DNASceneElement):
    TAG = 'texture'
    PARENTS = ['street']

    def __init__(self):
        DNASceneElement.__init__(self)

        self.code = ''

    def handleText(self, text):
        self.code += text

registerElement(DNATexture)
