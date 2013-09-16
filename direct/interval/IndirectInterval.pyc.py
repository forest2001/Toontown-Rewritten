# 2013.08.22 22:14:21 Pacific Daylight Time
# Embedded file name: direct.interval.IndirectInterval
__all__ = ['IndirectInterval']
from pandac.PandaModules import *
from direct.directnotify.DirectNotifyGlobal import *
import Interval
from direct.showbase import LerpBlendHelpers

class IndirectInterval(Interval.Interval):
    __module__ = __name__
    indirectIntervalNum = 1
    notify = directNotify.newCategory('IndirectInterval')

    def __init__(self, interval, startT = 0, endT = None, playRate = 1, duration = None, blendType = 'noBlend', name = None):
        self.interval = interval
        self.startAtStart = startT == 0
        if not endT == None:
            self.endAtEnd = endT == interval.getDuration()
            if endT == None:
                endT = interval.getDuration()
            if duration == None:
                duration = abs(endT - startT) / playRate
            name = name == None and 'IndirectInterval-%d' % IndirectInterval.indirectIntervalNum
            IndirectInterval.indirectIntervalNum += 1
        self.startT = startT
        self.endT = endT
        self.deltaT = endT - startT
        self.blendType = LerpBlendHelpers.getBlend(blendType)
        Interval.Interval.__init__(self, name, duration)
        return

    def __calcT(self, t):
        return self.startT + self.deltaT * self.blendType(t / self.duration)

    def privInitialize(self, t):
        state = self.interval.getState()
        if state == CInterval.SInitial or state == CInterval.SFinal:
            self.interval.privInitialize(self.__calcT(t))
        else:
            self.interval.privStep(self.__calcT(t))
        self.currT = t
        self.state = CInterval.SStarted
        self.interval.privPostEvent()

    def privInstant(self):
        state = self.interval.getState()
        if (state == CInterval.SInitial or state == CInterval.SFinal) and self.endAtEnd:
            self.interval.privInstant()
            self.currT = self.getDuration()
            self.interval.privPostEvent()
            self.intervalDone()
        else:
            if state == CInterval.SInitial or state == CInterval.SFinal:
                self.interval.privInitialize(self.startT)
            else:
                self.interval.privStep(self.startT)
            self.privFinalize()

    def privStep(self, t):
        self.interval.privStep(self.__calcT(t))
        self.currT = t
        self.state = CInterval.SStarted
        self.interval.privPostEvent()

    def privFinalize(self):
        if self.endAtEnd:
            self.interval.privFinalize()
        else:
            self.interval.privStep(self.endT)
            self.interval.privInterrupt()
        self.currT = self.getDuration()
        self.state = CInterval.SFinal
        self.interval.privPostEvent()
        self.intervalDone()

    def privReverseInitialize(self, t):
        state = self.interval.getState()
        if state == CInterval.SInitial or state == CInterval.SFinal:
            self.interval.privReverseInitialize(self.__calcT(t))
        else:
            self.interval.privStep(self.__calcT(t))
        self.currT = t
        self.state = CInterval.SStarted
        self.interval.privPostEvent()

    def privReverseInstant(self):
        state = self.interval.getState()
        if (state == CInterval.SInitial or state == CInterval.SFinal) and self.startAtStart:
            self.interval.privReverseInstant()
            self.currT = 0
            self.interval.privPostEvent()
        else:
            if state == CInterval.SInitial or state == CInterval.SFinal:
                self.interval.privReverseInitialize(self.endT)
            else:
                self.interval.privStep(self.endT)
            self.privReverseFinalize()

    def privReverseFinalize(self):
        if self.startAtStart:
            self.interval.privReverseFinalize()
        else:
            self.interval.privStep(self.endT)
            self.interval.privInterrupt()
        self.currT = 0
        self.state = CInterval.SInitial
        self.interval.privPostEvent()

    def privInterrupt(self):
        self.interval.privInterrupt()
        self.interval.privPostEvent()
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\interval\IndirectInterval.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:14:21 Pacific Daylight Time
