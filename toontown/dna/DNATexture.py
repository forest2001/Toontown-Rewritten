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

    def _makeNode(self, storage, parent):
        texture = storage.findTexture(self.code)
        if texture is None:
            raise DNAError('DNATexture uses unknown code %s' % self.code)

        index = parent.getPythonTag('texture_index') or 0

        node = parent.find('**/*_' + ['street', 'sidewalk', 'curb'][index])
        parent.setPythonTag('texture_index', index+1)

        if not node.isEmpty():
            node.setTexture(texture, 1)

registerElement(DNATexture)
