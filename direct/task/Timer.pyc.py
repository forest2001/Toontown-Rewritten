# 2013.08.22 22:14:56 Pacific Daylight Time
# Embedded file name: direct.task.Timer
__all__ = ['Timer']
from pandac.PandaModules import *
import Task

class Timer():
    __module__ = __name__
    id = 0

    def __init__(self, name = None):
        self.finalT = 0.0
        self.currT = 0.0
        if name == None:
            name = 'default-timer-%d' % Timer.id
            Timer.id += 1
        self.name = name
        self.started = 0
        self.callback = None
        return

    def start(self, t, name):
        if self.started:
            self.stop()
        self.callback = None
        self.finalT = t
        self.name = name
        self.startT = globalClock.getFrameTime()
        self.currT = 0.0
        taskMgr.add(self.__timerTask, self.name + '-run')
        self.started = 1
        return

    def startCallback(self, t, callback):
        if self.started:
            self.stop()
        self.callback = callback
        self.finalT = t
        self.startT = globalClock.getFrameTime()
        self.currT = 0.0
        taskMgr.add(self.__timerTask, self.name + '-run')
        self.started = 1

    def stop(self):
        if not self.started:
            return 0.0
        taskMgr.remove(self.name + '-run')
        self.started = 0
        return self.currT

    def resume(self):
        self.start(self.finalT - self.currT, self.name)

    def restart(self):
        if self.callback != None:
            self.startCallback(self.finalT, self.callback)
        else:
            self.start(self.finalT, self.name)
        return

    def isStarted(self):
        return self.started

    def addT(self, t):
        self.finalT = self.finalT + t

    def setT(self, t):
        self.finalT = t

    def getT(self):
        return self.finalT - self.currT

    def __timerTask(self, task):
        t = globalClock.getFrameTime()
        te = t - self.startT
        self.currT = te
        if te >= self.finalT:
            if self.callback != None:
                self.callback()
            else:
                messenger.send(self.name)
            return Task.done
        return Task.cont
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\task\Timer.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:14:56 Pacific Daylight Time
