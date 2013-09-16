# 2013.08.22 22:15:52 Pacific Daylight Time
# Embedded file name: pandac.libpandaexpressModules
from extension_native_helpers import *
Dtool_PreloadDLL('libpandaexpress')
from libpandaexpress import *
from extension_native_helpers import *
Dtool_PreloadDLL('libpandaexpress')
from libpandaexpress import *

def readlines(self):
    lines = []
    line = self.readline()
    while line:
        lines.append(line)
        line = self.readline()

    return lines


Dtool_funcToMethod(readlines, Ramfile)
del readlines
from extension_native_helpers import *
Dtool_PreloadDLL('libpandaexpress')
from libpandaexpress import *

def readlines(self):
    lines = []
    line = self.readline()
    while line:
        lines.append(line)
        line = self.readline()

    return lines


Dtool_funcToMethod(readlines, StreamReader)
del readlines
from extension_native_helpers import *
Dtool_PreloadDLL('libpandaexpress')
from libpandaexpress import *

def spawnTask(self, name = None, callback = None, extraArgs = []):
    if not name:
        name = self.getUrl().cStr()
    from direct.task import Task
    task = Task.Task(self.doTask)
    task.callback = callback
    task.callbackArgs = extraArgs
    return taskMgr.add(task, name)


Dtool_funcToMethod(spawnTask, HTTPChannel)
del spawnTask

def doTask(self, task):
    from direct.task import Task
    if self.run():
        return Task.cont
    if task.callback:
        task.callback(*task.callbackArgs)
    return Task.done


Dtool_funcToMethod(doTask, HTTPChannel)
del doTask
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\pandac\libpandaexpressModules.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:15:52 Pacific Daylight Time
