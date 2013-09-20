# 2013.08.22 22:26:55 Pacific Daylight Time
# Embedded file name: toontown.uberdog.DistributedSecurityMgr
import socket
import datetime
import os
from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal
from direct.distributed.DistributedObject import DistributedObject
from toontown.toonbase import ToontownGlobals

class DistributedSecurityMgr(DistributedObject):
    __module__ = __name__
    notify = directNotify.newCategory('SecurityMgr')
    neverDisable = 1

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        base.cr.whitelistMgr = self

    def delete(self):
        DistributedObject.delete(self)
        self.cr.whitelistMgr = None
        return

    def disable(self):
        self.notify.debug("i'm disabling SecurityMgr right now.")
        DistributedObject.disable(self)

    def generate(self):
        self.notify.debug('BASE: generate')
        DistributedObject.generate(self)

    def updateWhitelist(self):
        messenger.send('updateWhitelist')
        self.notify.info('Updating white list')
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\uberdog\DistributedSecurityMgr.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:26:55 Pacific Daylight Time
