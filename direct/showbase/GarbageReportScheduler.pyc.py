# 2013.08.22 22:14:35 Pacific Daylight Time
# Embedded file name: direct.showbase.GarbageReportScheduler
from direct.showbase.GarbageReport import GarbageReport

class GarbageReportScheduler():
    __module__ = __name__

    def __init__(self, waitBetween = None, waitScale = None):
        if waitBetween is None:
            waitBetween = 30 * 60
        if waitScale is None:
            waitScale = 1.5
        self._waitBetween = waitBetween
        self._waitScale = waitScale
        self._taskName = 'startScheduledGarbageReport-%s' % serialNum()
        self._garbageReport = None
        self._scheduleNextGarbageReport()
        return

    def getTaskName(self):
        return self._taskName

    def _scheduleNextGarbageReport(self, garbageReport = None):
        if garbageReport:
            self._garbageReport = None
        taskMgr.doMethodLater(self._waitBetween, self._runGarbageReport, self._taskName)
        self._waitBetween = self._waitBetween * self._waitScale
        return

    def _runGarbageReport(self, task):
        self._garbageReport = GarbageReport('ScheduledGarbageReport', threaded=True, doneCallback=self._scheduleNextGarbageReport, autoDestroy=True, priority=GarbageReport.Priorities.Normal * 3)
        return task.done
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\showbase\GarbageReportScheduler.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:14:35 Pacific Daylight Time
