from DNASceneElement import DNASceneElement
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
        pass # TODO

registerElement(DNAText)
