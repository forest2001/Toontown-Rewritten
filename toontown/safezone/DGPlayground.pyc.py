# 2013.08.22 22:24:24 Pacific Daylight Time
# Embedded file name: toontown.safezone.DGPlayground
from pandac.PandaModules import *
import Playground
import random
from direct.task import Task

class DGPlayground(Playground.Playground):
    __module__ = __name__

    def __init__(self, loader, parentFSM, doneEvent):
        Playground.Playground.__init__(self, loader, parentFSM, doneEvent)

    def load(self):
        Playground.Playground.load(self)

    def unload(self):
        Playground.Playground.unload(self)

    def enter(self, requestStatus):
        Playground.Playground.enter(self, requestStatus)
        self.nextBirdTime = 0
        taskMgr.add(self.__birds, 'DG-birds')

    def exit(self):
        Playground.Playground.exit(self)
        taskMgr.remove('DG-birds')

    def __birds(self, task):
        if task.time < self.nextBirdTime:
            return Task.cont
        randNum = random.random()
        bird = int(randNum * 100) % 4 + 1
        if bird == 1:
            base.playSfx(self.loader.bird1Sound)
        elif bird == 2:
            base.playSfx(self.loader.bird2Sound)
        elif bird == 3:
            base.playSfx(self.loader.bird3Sound)
        elif bird == 4:
            base.playSfx(self.loader.bird4Sound)
        self.nextBirdTime = task.time + randNum * 20.0
        return Task.cont

    def showPaths(self):
        from toontown.classicchars import CCharPaths
        from toontown.toonbase import TTLocalizer
        self.showPathPoints(CCharPaths.getPaths(TTLocalizer.Goofy))
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\safezone\DGPlayground.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:24:24 Pacific Daylight Time
