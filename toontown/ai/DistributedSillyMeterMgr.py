# 2013.08.22 22:16:01 Pacific Daylight Time
# Embedded file name: toontown.ai.DistributedSillyMeterMgr
from direct.directnotify import DirectNotifyGlobal
from direct.distributed import DistributedObject
from toontown.ai import DistributedPhaseEventMgr
import time

class DistributedSillyMeterMgr(DistributedPhaseEventMgr.DistributedPhaseEventMgr):
    __module__ = __name__
    neverDisable = 1
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedSillyMeterMgr')

    def __init__(self, cr):
        DistributedPhaseEventMgr.DistributedPhaseEventMgr.__init__(self, cr)
        cr.SillyMeterMgr = self

    def announceGenerate(self):
        DistributedPhaseEventMgr.DistributedPhaseEventMgr.announceGenerate(self)
        messenger.send('SillyMeterIsRunning', [self.isRunning])

    def delete(self):
        self.notify.debug('deleting SillyMetermgr')
        messenger.send('SillyMeterIsRunning', [False])
        DistributedPhaseEventMgr.DistributedPhaseEventMgr.delete(self)
        if hasattr(self.cr, 'SillyMeterMgr'):
            del self.cr.SillyMeterMgr

    def setCurPhase(self, newPhase):
        DistributedPhaseEventMgr.DistributedPhaseEventMgr.setCurPhase(self, newPhase)
        messenger.send('SillyMeterPhase', [newPhase])

    def setIsRunning(self, isRunning):
        DistributedPhaseEventMgr.DistributedPhaseEventMgr.setIsRunning(self, isRunning)
        messenger.send('SillyMeterIsRunning', [isRunning])

    def getCurPhaseDuration(self):
        if len(self.holidayDates) > 0:
            startHolidayDate = self.holidayDates[self.curPhase]
            if self.curPhase + 1 >= len(self.holidayDates):
                self.notify.error('No end date for phase %' % self.curPhase)
                return -1
            else:
                endHolidayDate = self.holidayDates[self.curPhase + 1]
            startHolidayTime = time.mktime(startHolidayDate.timetuple())
            endHolidayTime = time.mktime(endHolidayDate.timetuple())
            holidayDuration = endHolidayTime - startHolidayTime
            if holidayDuration < 0:
                self.notify.error('Duration not set for phase %' % self.curPhase)
                return -1
            else:
                return holidayDuration
        else:
            self.notify.warning('Phase dates not yet known')
            return -1

    def getCurPhaseStartDate(self):
        if len(self.holidayDates) > 0:
            return self.holidayDates[self.curPhase]
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\ai\DistributedSillyMeterMgr.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:16:01 Pacific Daylight Time
