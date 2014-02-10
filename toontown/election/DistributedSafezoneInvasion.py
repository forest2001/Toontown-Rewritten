from pandac.PandaModules import *
from direct.distributed.DistributedObject import DistributedObject

class DistributedSafezoneInvasion(DistributedObject):
    def __init__(self, cr):
        DistributedObject.__init__(self, cr)

    def delete(self):
        DistributedObject.delete(self)
