# 2013.08.22 22:16:00 Pacific Daylight Time
# Embedded file name: toontown.ai.DistributedMailboxZeroMgr
from direct.directnotify import DirectNotifyGlobal
from direct.distributed import DistributedObject
from toontown.ai import DistributedPhaseEventMgr

class DistributedMailboxZeroMgr(DistributedPhaseEventMgr.DistributedPhaseEventMgr):
    __module__ = __name__
    neverDisable = 1
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedMailboxZeroMgr')

    def __init__(self, cr):
        DistributedPhaseEventMgr.DistributedPhaseEventMgr.__init__(self, cr)
        cr.mailboxZeroMgr = self

    def announceGenerate(self):
        DistributedPhaseEventMgr.DistributedPhaseEventMgr.announceGenerate(self)
        messenger.send('mailboxZeroIsRunning', [self.isRunning])

    def delete(self):
        self.notify.debug('deleting mailboxzeromgr')
        messenger.send('mailboxZeroIsRunning', [False])
        DistributedPhaseEventMgr.DistributedPhaseEventMgr.delete(self)
        if hasattr(self.cr, 'mailboxZeroMgr'):
            del self.cr.mailboxZeroMgr

    def setCurPhase(self, newPhase):
        DistributedPhaseEventMgr.DistributedPhaseEventMgr.setCurPhase(self, newPhase)
        messenger.send('mailboxZeroPhase', [newPhase])

    def setIsRunning(self, isRunning):
        DistributedPhaseEventMgr.DistributedPhaseEventMgr.setIsRunning(self, isRunning)
        messenger.send('mailboxZeroIsRunning', [isRunning])
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\ai\DistributedMailboxZeroMgr.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:16:00 Pacific Daylight Time
