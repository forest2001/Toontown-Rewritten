from DNASceneElement import DNASceneElement
from DNAParser import *
from panda3d.core import *

class DNATitle(DNASceneElement):
    TAG = 'title'
    PARENTS = ['landmark_building']

    def __init__(self):
        DNASceneElement.__init__(self)

        self.title = ''

    def handleText(self, text):
        self.title = text


    def _makeNode(self, storage, parent):
        pass # TODO

registerElement(DNATitle)
