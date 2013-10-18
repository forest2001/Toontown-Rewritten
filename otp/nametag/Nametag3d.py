from Nametag import *
from pandac.PandaModules import *

class Nametag3d(Nametag, PandaNode):
    def __init__(self):
        Nametag.__init__(self)
        PandaNode.__init__(self, '')

    def setContents(self, contents):
        pass
