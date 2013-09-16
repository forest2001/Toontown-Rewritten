# 2013.08.22 22:14:05 Pacific Daylight Time
# Embedded file name: direct.distributed.DistributedObjectGlobal
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed.DistributedObject import DistributedObject

class DistributedObjectGlobal(DistributedObject):
    __module__ = __name__
    notify = directNotify.newCategory('DistributedObjectGlobal')
    neverDisable = 1

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        self.parentId = 0
        self.zoneId = 0
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\distributed\DistributedObjectGlobal.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:14:05 Pacific Daylight Time
