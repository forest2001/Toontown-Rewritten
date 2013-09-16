# 2013.08.22 22:20:59 Pacific Daylight Time
# Embedded file name: toontown.hood.SleepingHydrantAnimatedProp
import AnimatedProp
from direct.interval.IntervalGlobal import *
from direct.task import Task
import math

class SleepingHydrantAnimatedProp(AnimatedProp.AnimatedProp):
    __module__ = __name__

    def __init__(self, node):
        AnimatedProp.AnimatedProp.__init__(self, node)
        self.task = None
        return

    def bobTask(self, task):
        self.node.setSz(1.0 + 0.08 * math.sin(task.time))
        return Task.cont

    def enter(self):
        AnimatedProp.AnimatedProp.enter(self)
        self.task = taskMgr.add(self.bobTask, self.uniqueName('bobTask'))

    def exit(self):
        AnimatedProp.AnimatedProp.exit(self)
        if self.task:
            taskMgr.remove(self.task)
            self.task = None
        return
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\hood\SleepingHydrantAnimatedProp.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:20:59 Pacific Daylight Time
