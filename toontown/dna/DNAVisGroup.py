from DNASceneElement import DNASceneElement
from DNAParser import *
from panda3d.core import *

class DNAVisGroup(DNASceneElement):
    TAG = 'visgroup'
    PARENTS = ['group']

    def __init__(self, zone, vis=''):
        DNASceneElement.__init__(self)

        self.zone = zone
        self.vis = vis.split()

    def _makeNode(self, storage, parent):
        return parent.attachNewNode(self.name)

registerElement(DNAVisGroup)
