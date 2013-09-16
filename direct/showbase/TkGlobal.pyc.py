# 2013.08.22 22:14:49 Pacific Daylight Time
# Embedded file name: direct.showbase.TkGlobal
__all__ = ['taskMgr']
from Tkinter import *
from direct.task.TaskManagerGlobal import *
from direct.task.Task import Task
import Pmw
import sys
if '_Pmw' in sys.modules:
    sys.modules['_Pmw'].__name__ = '_Pmw'
__builtins__['tkroot'] = Pmw.initialise()

def tkLoop(self):
    while tkinter.dooneevent(tkinter.ALL_EVENTS | tkinter.DONT_WAIT):
        pass

    return Task.cont


def spawnTkLoop():
    taskMgr.add(tkLoop, 'tkLoop')


taskMgr.remove('tkLoop')
spawnTkLoop()
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\showbase\TkGlobal.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:14:49 Pacific Daylight Time
