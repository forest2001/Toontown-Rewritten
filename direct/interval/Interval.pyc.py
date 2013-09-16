# 2013.08.22 22:14:21 Pacific Daylight Time
# Embedded file name: direct.interval.Interval
__all__ = ['Interval']
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import *
from direct.task.Task import Task, TaskManager
from direct.showbase import PythonUtil
from pandac.PandaModules import *
import math

class Interval(DirectObject):
    __module__ = __name__
    notify = directNotify.newCategory('Interval')
    playbackCounter = 0

    def __init__(self, name, duration, openEnded = 1):
        self.name = name
        self.duration = max(duration, 0.0)
        self.state = CInterval.SInitial
        self.currT = 0.0
        self.doneEvent = None
        self.setTHooks = []
        self.__startT = 0
        self.__startTAtStart = 1
        self.__endT = duration
        self.__endTAtEnd = 1
        self.__playRate = 1.0
        self.__doLoop = 0
        self.__loopCount = 0
        self.pstats = None
        if __debug__ and TaskManager.taskTimerVerbose:
            self.pname = name.split('-', 1)[0]
            self.pstats = PStatCollector('App:Show code:ivalLoop:%s' % self.pname)
        self.openEnded = openEnded
        return

    def getName(self):
        return self.name

    def getDuration(self):
        return self.duration

    def getOpenEnded(self):
        return self.openEnded

    def setLoop(self, loop = 1):
        self.__doLoop = loop

    def getLoop(self):
        return self.__doLoop

    def getState(self):
        return self.state

    def isPaused(self):
        return self.getState() == CInterval.SPaused

    def isStopped(self):
        return self.getState() == CInterval.SInitial or self.getState() == CInterval.SFinal

    def setT(self, t):
        state = self.getState()
        if state == CInterval.SInitial:
            self.privInitialize(t)
            if self.isPlaying():
                self.setupResume()
            else:
                self.privInterrupt()
        elif state == CInterval.SStarted:
            self.privInterrupt()
            self.privStep(t)
            self.setupResume()
        elif state == CInterval.SPaused:
            self.privStep(t)
            self.privInterrupt()
        elif state == CInterval.SFinal:
            self.privReverseInitialize(t)
            if self.isPlaying():
                self.setupResume()
            else:
                self.privInterrupt()
        else:
            self.notify.error('Invalid state: %s' % state)
        self.privPostEvent()

    def getT(self):
        return self.currT

    def start(self, startT = 0.0, endT = -1.0, playRate = 1.0):
        self.setupPlay(startT, endT, playRate, 0)
        self.__spawnTask()

    def loop(self, startT = 0.0, endT = -1.0, playRate = 1.0):
        self.setupPlay(startT, endT, playRate, 1)
        self.__spawnTask()

    def pause(self):
        if self.getState() == CInterval.SStarted:
            self.privInterrupt()
        self.privPostEvent()
        self.__removeTask()
        return self.getT()

    def resume(self, startT = None):
        if startT != None:
            self.setT(startT)
        self.setupResume()
        if not self.isPlaying():
            self.__spawnTask()
        return

    def resumeUntil(self, endT):
        duration = self.getDuration()
        if endT < 0 or endT >= duration:
            self.__endT = duration
            self.__endTAtEnd = 1
        else:
            self.__endT = endT
            self.__endTAtEnd = 0
        self.setupResume()
        if not self.isPlaying():
            self.__spawnTask()

    def finish(self):
        state = self.getState()
        if state == CInterval.SInitial:
            self.privInstant()
        elif state != CInterval.SFinal:
            self.privFinalize()
        self.privPostEvent()
        self.__removeTask()

    def clearToInitial(self):
        self.pause()
        self.state = CInterval.SInitial
        self.currT = 0.0

    def isPlaying(self):
        return taskMgr.hasTaskNamed(self.getName() + '-play')

    def getPlayRate(self):
        return self.__playRate

    def setPlayRate(self, playRate):
        if self.isPlaying():
            self.pause()
            self.__playRate = playRate
            self.resume()
        else:
            self.__playRate = playRate

    def setDoneEvent(self, event):
        self.doneEvent = event

    def getDoneEvent(self):
        return self.doneEvent

    def privDoEvent(self, t, event):
        if self.pstats:
            self.pstats.start()
        if event == CInterval.ETStep:
            self.privStep(t)
        elif event == CInterval.ETFinalize:
            self.privFinalize()
        elif event == CInterval.ETInterrupt:
            self.privInterrupt()
        elif event == CInterval.ETInstant:
            self.privInstant()
        elif event == CInterval.ETInitialize:
            self.privInitialize(t)
        elif event == CInterval.ETReverseFinalize:
            self.privReverseFinalize()
        elif event == CInterval.ETReverseInstant:
            self.privReverseInstant()
        elif event == CInterval.ETReverseInitialize:
            self.privReverseInitialize(t)
        else:
            self.notify.error('Invalid event type: %s' % event)
        if self.pstats:
            self.pstats.stop()

    def privInitialize(self, t):
        self.state = CInterval.SStarted
        self.privStep(t)

    def privInstant(self):
        self.state = CInterval.SStarted
        self.privStep(self.getDuration())
        self.state = CInterval.SFinal
        self.intervalDone()

    def privStep(self, t):
        self.state = CInterval.SStarted
        self.currT = t

    def privFinalize(self):
        self.privStep(self.getDuration())
        self.state = CInterval.SFinal
        self.intervalDone()

    def privReverseInitialize(self, t):
        self.state = CInterval.SStarted
        self.privStep(t)

    def privReverseInstant(self):
        self.state = CInterval.SStarted
        self.privStep(self.getDuration())
        self.state = CInterval.SInitial

    def privReverseFinalize(self):
        self.privStep(0)
        self.state = CInterval.SInitial

    def privInterrupt(self):
        self.state = CInterval.SPaused

    def intervalDone(self):
        if self.doneEvent:
            messenger.send(self.doneEvent)

    def setupPlay(self, startT, endT, playRate, doLoop):
        duration = self.getDuration()
        if startT <= 0:
            self.__startT = 0
            self.__startTAtStart = 1
        elif startT > duration:
            self.__startT = duration
            self.__startTAtStart = 0
        else:
            self.__startT = startT
            self.__startTAtStart = 0
        if endT < 0 or endT >= duration:
            self.__endT = duration
            self.__endTAtEnd = 1
        else:
            self.__endT = endT
            self.__endTAtEnd = 0
        self.__clockStart = globalClock.getFrameTime()
        self.__playRate = playRate
        self.__doLoop = doLoop
        self.__loopCount = 0

    def setupResume(self):
        now = globalClock.getFrameTime()
        if self.__playRate > 0:
            self.__clockStart = now - (self.getT() - self.__startT) / self.__playRate
        elif self.__playRate < 0:
            self.__clockStart = now - (self.getT() - self.__endT) / self.__playRate
        self.__loopCount = 0

    def stepPlay(self):
        now = globalClock.getFrameTime()
        if self.__playRate >= 0:
            t = (now - self.__clockStart) * self.__playRate + self.__startT
            if self.__endTAtEnd:
                self.__endT = self.getDuration()
            if t < self.__endT:
                if self.isStopped():
                    self.privInitialize(t)
                else:
                    self.privStep(t)
            else:
                if self.__endTAtEnd:
                    if self.isStopped():
                        if self.getOpenEnded() or self.__loopCount != 0:
                            self.privInstant()
                    else:
                        self.privFinalize()
                elif self.isStopped():
                    self.privInitialize(self.__endT)
                else:
                    self.privStep(self.__endT)
                if self.__endT == self.__startT:
                    self.__loopCount += 1
                else:
                    timePerLoop = (self.__endT - self.__startT) / self.__playRate
                    numLoops = math.floor((now - self.__clockStart) / timePerLoop)
                    self.__loopCount += numLoops
                    self.__clockStart += numLoops * timePerLoop
        else:
            t = (now - self.__clockStart) * self.__playRate + self.__endT
            if t >= self.__startT:
                if self.isStopped():
                    self.privInitialize(t)
                else:
                    self.privStep(t)
            else:
                if self.__startTAtStart:
                    if self.isStopped():
                        if self.getOpenEnded() or self.__loopCount != 0:
                            self.privReverseInstant()
                    else:
                        self.privReverseFinalize()
                elif self.isStopped():
                    self.privReverseInitialize(self.__startT)
                else:
                    self.privStep(self.__startT)
                if self.__endT == self.__startT:
                    self.__loopCount += 1
                else:
                    timePerLoop = (self.__endT - self.__startT) / -self.__playRate
                    numLoops = math.floor((now - self.__clockStart) / timePerLoop)
                    self.__loopCount += numLoops
                    self.__clockStart += numLoops * timePerLoop
        if not self.__loopCount == 0:
            shouldContinue = self.__doLoop
            not shouldContinue and self.getState() == CInterval.SStarted and self.privInterrupt()
        return shouldContinue

    def __repr__(self, indent = 0):
        space = ''
        for l in range(indent):
            space = space + ' '

        return space + self.name + ' dur: %.2f' % self.duration

    def privPostEvent(self):
        if self.pstats:
            self.pstats.start()
        t = self.getT()
        if hasattr(self, 'setTHooks'):
            for func in self.setTHooks:
                func(t)

        if self.pstats:
            self.pstats.stop()

    def __spawnTask(self):
        self.__removeTask()
        taskName = self.getName() + '-play'
        task = Task(self.__playTask)
        task.interval = self
        taskMgr.add(task, taskName)

    def __removeTask(self):
        taskName = self.getName() + '-play'
        oldTasks = taskMgr.getTasksNamed(taskName)
        for task in oldTasks:
            if hasattr(task, 'interval'):
                task.interval.privInterrupt()
                taskMgr.remove(task)

    def __playTask(self, task):
        again = self.stepPlay()
        self.privPostEvent()
        if again:
            return Task.cont
        else:
            return Task.done

    def popupControls(self, tl = None):
        from direct.showbase import TkGlobal
        import math
        from Tkinter import Toplevel, Frame, Button, LEFT, X
        import Pmw
        from direct.tkwidgets import EntryScale
        if tl == None:
            tl = Toplevel()
            tl.title('Interval Controls')
        outerFrame = Frame(tl)

        def entryScaleCommand(t, s = self):
            s.setT(t)
            s.pause()

        self.es = es = EntryScale.EntryScale(outerFrame, text=self.getName(), min=0, max=math.floor(self.getDuration() * 100) / 100, command=entryScaleCommand)
        es.set(self.getT(), fCommand=0)
        es.pack(expand=1, fill=X)
        bf = Frame(outerFrame)

        def toStart(s = self, es = es):
            s.clearToInitial()
            es.set(0, fCommand=0)

        def toEnd(s = self):
            s.pause()
            s.setT(s.getDuration())
            es.set(s.getDuration(), fCommand=0)
            s.pause()

        jumpToStart = Button(bf, text='<<', command=toStart)

        def doPlay(s = self, es = es):
            s.resume(es.get())

        stop = Button(bf, text='Stop', command=lambda s = self: s.pause())
        play = Button(bf, text='Play', command=doPlay)
        jumpToEnd = Button(bf, text='>>', command=toEnd)
        jumpToStart.pack(side=LEFT, expand=1, fill=X)
        play.pack(side=LEFT, expand=1, fill=X)
        stop.pack(side=LEFT, expand=1, fill=X)
        jumpToEnd.pack(side=LEFT, expand=1, fill=X)
        bf.pack(expand=1, fill=X)
        outerFrame.pack(expand=1, fill=X)

        def update(t, es = es):
            es.set(t, fCommand=0)

        if not hasattr(self, 'setTHooks'):
            self.setTHooks = []
        self.setTHooks.append(update)

        def onDestroy(e, s = self, u = update):
            if u in s.setTHooks:
                s.setTHooks.remove(u)

        tl.bind('<Destroy>', onDestroy)
        return
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\interval\Interval.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:14:22 Pacific Daylight Time
