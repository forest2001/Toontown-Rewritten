# 2013.08.22 22:24:38 Pacific Daylight Time
# Embedded file name: toontown.safezone.DLPlayground
from pandac.PandaModules import *
import Playground
import random

class DLPlayground(Playground.Playground):
    __module__ = __name__

    def __init__(self, loader, parentFSM, doneEvent):
        Playground.Playground.__init__(self, loader, parentFSM, doneEvent)

    def showPaths(self):
        from toontown.classicchars import CCharPaths
        from toontown.toonbase import TTLocalizer
        self.showPathPoints(CCharPaths.getPaths(TTLocalizer.Donald))
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\safezone\DLPlayground.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:24:38 Pacific Daylight Time
