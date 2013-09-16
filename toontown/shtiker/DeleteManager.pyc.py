# 2013.08.22 22:24:46 Pacific Daylight Time
# Embedded file name: toontown.shtiker.DeleteManager
from pandac.PandaModules import *
from direct.distributed import DistributedObject
from direct.directnotify import DirectNotifyGlobal

class DeleteManager(DistributedObject.DistributedObject):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('DeleteManager')
    neverDisable = 1

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)

    def generate(self):
        DistributedObject.DistributedObject.generate(self)
        self.accept('deleteItems', self.d_setInventory)

    def disable(self):
        self.ignore('deleteItems')
        DistributedObject.DistributedObject.disable(self)

    def d_setInventory(self, newInventoryString):
        self.sendUpdate('setInventory', [newInventoryString])
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\shtiker\DeleteManager.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:24:46 Pacific Daylight Time
