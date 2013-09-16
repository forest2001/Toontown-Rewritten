# 2013.08.22 22:16:00 Pacific Daylight Time
# Embedded file name: toontown.ai.DistributedHydrantZeroMgr
from direct.directnotify import DirectNotifyGlobal
from direct.distributed import DistributedObject
from toontown.ai import DistributedPhaseEventMgr

class DistributedHydrantZeroMgr(DistributedPhaseEventMgr.DistributedPhaseEventMgr):
    __module__ = __name__
    neverDisable = 1
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedHydrantZeroMgr')

    def __init__(self, cr):
        DistributedPhaseEventMgr.DistributedPhaseEventMgr.__init__(self, cr)
        cr.hydrantZeroMgr = self

    def announceGenerate(self):
        DistributedPhaseEventMgr.DistributedPhaseEventMgr.announceGenerate(self)
        messenger.send('hydrantZeroIsRunning', [self.isRunning])

    def delete(self):
        self.notify.debug('deleting hydrantzeromgr')
        messenger.send('hydrantZeroIsRunning', [False])
        DistributedPhaseEventMgr.DistributedPhaseEventMgr.delete(self)
        if hasattr(self.cr, 'hydrantZeroMgr'):
            del self.cr.hydrantZeroMgr

    def setCurPhase(self, newPhase):
        DistributedPhaseEventMgr.DistributedPhaseEventMgr.setCurPhase(self, newPhase)
        messenger.send('hydrantZeroPhase', [newPhase])

    def setIsRunning(self, isRunning):
        DistributedPhaseEventMgr.DistributedPhaseEventMgr.setIsRunning(self, isRunning)
        messenger.send('hydrantZeroIsRunning', [isRunning])
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\ai\DistributedHydrantZeroMgr.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:16:00 Pacific Daylight Time
