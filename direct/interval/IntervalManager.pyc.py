# 2013.08.22 22:14:22 Pacific Daylight Time
# Embedded file name: direct.interval.IntervalManager
__all__ = ['IntervalManager', 'ivalMgr']
from pandac.PandaModules import *
from pandac import PandaModules
from direct.directnotify.DirectNotifyGlobal import *
from direct.showbase import EventManager
import Interval
import types
import fnmatch

class IntervalManager(CIntervalManager):
    __module__ = __name__

    def __init__(self, globalPtr = 0):
        if globalPtr:
            self.cObj = CIntervalManager.getGlobalPtr()
            Dtool_BorrowThisReference(self, self.cObj)
            self.dd = self
        else:
            CIntervalManager.__init__(self)
        self.eventQueue = EventQueue()
        self.MyEventmanager = EventManager.EventManager(self.eventQueue)
        self.setEventQueue(self.eventQueue)
        self.ivals = []
        self.removedIvals = {}

    def addInterval(self, interval):
        index = self.addCInterval(interval, 1)
        self.__storeInterval(interval, index)

    def removeInterval(self, interval):
        index = self.findCInterval(interval.getName())
        if index >= 0:
            self.removeCInterval(index)
            if index < len(self.ivals):
                self.ivals[index] = None
            return 1
        return 0

    def getInterval(self, name):
        index = self.findCInterval(name)
        if index >= 0:
            if index < len(self.ivals) and self.ivals[index]:
                return self.ivals[index]
            return self.getCInterval(index)
        return None

    def getIntervalsMatching(self, pattern):
        ivals = []
        count = 0
        maxIndex = self.getMaxIndex()
        for index in range(maxIndex):
            ival = self.getCInterval(index)
            if ival and fnmatch.fnmatchcase(ival.getName(), pattern):
                count += 1
                if index < len(self.ivals) and self.ivals[index]:
                    ivals.append(self.ivals[index])
                else:
                    ivals.append(ival)

        return ivals

    def finishIntervalsMatching(self, pattern):
        ivals = self.getIntervalsMatching(pattern)
        for ival in ivals:
            ival.finish()

        return len(ivals)

    def pauseIntervalsMatching(self, pattern):
        ivals = self.getIntervalsMatching(pattern)
        for ival in ivals:
            ival.pause()

        return len(ivals)

    def step(self):
        CIntervalManager.step(self)
        self.__doPythonCallbacks()

    def interrupt(self):
        CIntervalManager.interrupt(self)
        self.__doPythonCallbacks()

    def __doPythonCallbacks(self):
        index = self.getNextRemoval()
        while index >= 0:
            ival = self.ivals[index]
            self.ivals[index] = None
            ival.privPostEvent()
            index = self.getNextRemoval()

        index = self.getNextEvent()
        while index >= 0:
            self.ivals[index].privPostEvent()
            index = self.getNextEvent()

        self.MyEventmanager.doEvents()
        return

    def __storeInterval(self, interval, index):
        while index >= len(self.ivals):
            self.ivals.append(None)

        self.ivals[index] = interval
        return


ivalMgr = IntervalManager(1)
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\interval\IntervalManager.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:14:22 Pacific Daylight Time
