# 2013.08.22 22:14:40 Pacific Daylight Time
# Embedded file name: direct.showbase.ProfileSession
from pandac.libpandaexpressModules import TrueClock
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.showbase.PythonUtil import StdoutCapture, _installProfileCustomFuncs, _removeProfileCustomFuncs, _profileWithoutGarbageLeak, _getProfileResultFileInfo, _setProfileResultsFileInfo, _clearProfileResultFileInfo
import __builtin__
import profile
import pstats
from StringIO import StringIO
import marshal

class PercentStats(pstats.Stats):
    __module__ = __name__

    def setTotalTime(self, tt):
        self._totalTime = tt

    def add(self, *args, **kArgs):
        pstats.Stats.add(self, *args, **kArgs)
        self.files = []

    def print_stats(self, *amount):
        for filename in self.files:
            print filename

        if self.files:
            print
        indent = ' ' * 8
        for func in self.top_level:
            print indent, func_get_function_name(func)

        print indent, self.total_calls, 'function calls',
        if self.total_calls != self.prim_calls:
            print '(%d primitive calls)' % self.prim_calls,
        print 'in %s CPU milliseconds' % (self.total_tt * 1000.0)
        if self._totalTime != self.total_tt:
            print indent, 'percentages are of %s CPU milliseconds' % (self._totalTime * 1000)
        print
        width, list = self.get_print_list(amount)
        if list:
            self.print_title()
            for func in list:
                self.print_line(func)

            print
        return self

    def f8(self, x):
        if self._totalTime == 0.0:
            return '    Inf%'
        return '%7.2f%%' % (x * 100.0 / self._totalTime)

    @staticmethod
    def func_std_string(func_name):
        return '%s:%d(%s)' % func_name

    def print_line(self, func):
        cc, nc, tt, ct, callers = self.stats[func]
        c = str(nc)
        f8 = self.f8
        if nc != cc:
            c = c + '/' + str(cc)
        print c.rjust(9),
        print f8(tt),
        if nc == 0:
            print ' ' * 8,
        else:
            print f8(tt / nc),
        print f8(ct),
        if cc == 0:
            print ' ' * 8,
        else:
            print f8(ct / cc),
        print PercentStats.func_std_string(func)


class ProfileSession():
    __module__ = __name__
    TrueClock = TrueClock.getGlobalPtr()
    notify = directNotify.newCategory('ProfileSession')

    def __init__(self, name, func = None, logAfterProfile = False):
        self._func = func
        self._name = name
        self._logAfterProfile = logAfterProfile
        self._filenameBase = 'profileData-%s-%s' % (self._name, id(self))
        self._refCount = 0
        self._aggregate = False
        self._lines = 500
        self._sorts = ['cumulative', 'time', 'calls']
        self._callInfo = True
        self._totalTime = None
        self._reset()
        self.acquire()
        return

    def getReference(self):
        self.acquire()
        return self

    def acquire(self):
        self._refCount += 1

    def release(self):
        self._refCount -= 1
        if not self._refCount:
            self._destroy()

    def _destroy(self):
        del self._func
        del self._name
        del self._filenameBase
        del self._filenameCounter
        del self._filenames
        del self._duration
        del self._filename2ramFile
        del self._resultCache
        del self._successfulProfiles

    def _reset(self):
        self._filenameCounter = 0
        self._filenames = []
        self._statFileCounter = 0
        self._successfulProfiles = 0
        self._duration = None
        self._filename2ramFile = {}
        self._stats = None
        self._resultCache = {}
        return

    def _getNextFilename(self):
        filename = '%s-%s' % (self._filenameBase, self._filenameCounter)
        self._filenameCounter += 1
        return filename

    def run(self):
        self.acquire()
        if not self._aggregate:
            self._reset()
        if 'globalProfileSessionFunc' in __builtin__.__dict__:
            self.notify.warning('could not profile %s' % self._func)
            result = self._func()
            if self._duration is None:
                self._duration = 0.0
        else:
            __builtin__.globalProfileSessionFunc = self._func
            __builtin__.globalProfileSessionResult = [None]
            self._filenames.append(self._getNextFilename())
            filename = self._filenames[-1]
            _installProfileCustomFuncs(filename)
            Profile = profile.Profile
            statement = 'globalProfileSessionResult[0]=globalProfileSessionFunc()'
            sort = -1
            retVal = None
            prof = Profile()
            try:
                prof = prof.run(statement)
            except SystemExit:
                pass

            prof.dump_stats(filename)
            del prof.dispatcher
            profData = _getProfileResultFileInfo(filename)
            self._filename2ramFile[filename] = profData
            maxTime = 0.0
            for cc, nc, tt, ct, callers in profData[1].itervalues():
                if ct > maxTime:
                    maxTime = ct

            self._duration = maxTime
            _removeProfileCustomFuncs(filename)
            result = globalProfileSessionResult[0]
            del __builtin__.__dict__['globalProfileSessionFunc']
            del __builtin__.__dict__['globalProfileSessionResult']
            self._successfulProfiles += 1
            if self._logAfterProfile:
                self.notify.info(self.getResults())
        self.release()
        return result

    def getDuration(self):
        return self._duration

    def profileSucceeded(self):
        return self._successfulProfiles > 0

    def _restoreRamFile(self, filename):
        _installProfileCustomFuncs(filename)
        _setProfileResultsFileInfo(filename, self._filename2ramFile[filename])

    def _discardRamFile(self, filename):
        _removeProfileCustomFuncs(filename)
        del self._filename2ramFile[filename]

    def setName(self, name):
        self._name = name

    def getName(self):
        return self._name

    def setFunc(self, func):
        self._func = func

    def getFunc(self):
        return self._func

    def setAggregate(self, aggregate):
        self._aggregate = aggregate

    def getAggregate(self):
        return self._aggregate

    def setLogAfterProfile(self, logAfterProfile):
        self._logAfterProfile = logAfterProfile

    def getLogAfterProfile(self):
        return self._logAfterProfile

    def setLines(self, lines):
        self._lines = lines

    def getLines(self):
        return self._lines

    def setSorts(self, sorts):
        self._sorts = sorts

    def getSorts(self):
        return self._sorts

    def setShowCallInfo(self, showCallInfo):
        self._showCallInfo = showCallInfo

    def getShowCallInfo(self):
        return self._showCallInfo

    def setTotalTime(self, totalTime = None):
        self._totalTime = totalTime

    def resetTotalTime(self):
        self._totalTime = None
        return

    def getTotalTime(self):
        return self._totalTime

    def aggregate(self, other):
        other._compileStats()
        self._compileStats()
        self._stats.add(other._stats)

    def _compileStats(self):
        statsChanged = self._statFileCounter < len(self._filenames)
        if self._stats is None:
            for filename in self._filenames:
                self._restoreRamFile(filename)

            self._stats = PercentStats(*self._filenames)
            self._statFileCounter = len(self._filenames)
            for filename in self._filenames:
                self._discardRamFile(filename)

        else:
            while self._statFileCounter < len(self._filenames):
                filename = self._filenames[self._statFileCounter]
                self._restoreRamFile(filename)
                self._stats.add(filename)
                self._discardRamFile(filename)

        if statsChanged:
            self._stats.strip_dirs()
            self._resultCache = {}
        return statsChanged

    def getResults(self, lines = Default, sorts = Default, callInfo = Default, totalTime = Default):
        if not self.profileSucceeded():
            output = '%s: profiler already running, could not profile' % self._name
        else:
            if lines is Default:
                lines = self._lines
            if sorts is Default:
                sorts = self._sorts
            if callInfo is Default:
                callInfo = self._callInfo
            if totalTime is Default:
                totalTime = self._totalTime
            self._compileStats()
            if totalTime is None:
                totalTime = self._stats.total_tt
            lines = int(lines)
            sorts = list(sorts)
            callInfo = bool(callInfo)
            totalTime = float(totalTime)
            k = str((lines,
             sorts,
             callInfo,
             totalTime))
            if k in self._resultCache:
                output = self._resultCache[k]
            else:
                sc = StdoutCapture()
                s = self._stats
                s.setTotalTime(totalTime)
                for sort in sorts:
                    s.sort_stats(sort)
                    s.print_stats(lines)
                    if callInfo:
                        s.print_callees(lines)
                        s.print_callers(lines)

                output = sc.getString()
                sc.destroy()
                self._resultCache[k] = output
        return output
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\showbase\ProfileSession.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:14:40 Pacific Daylight Time
