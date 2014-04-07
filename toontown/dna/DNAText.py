from DNASceneElement import DNASceneElement
from DNATypesetter import DNATypesetter
from DNAParser import *
from panda3d.core import *

class DNAText(DNASceneElement):
    TAG = 'text'
    PARENTS = ['baseline']

    def __init__(self):
        DNASceneElement.__init__(self)

        self.text = ''

    def handleText(self, text):
        self.text = text

    def _makeNode(self, storage, parent):
        typesetter = DNATypesetter(self.parent, storage)

        np = typesetter.generate(self.text)
        if np:
            np.reparentTo(parent)
            return np

registerElement(DNAText)
