# 2013.08.22 22:15:03 Pacific Daylight Time
# Embedded file name: otp.ai.AIBaseGlobal
from AIBase import *
__builtins__['simbase'] = AIBase()
__builtins__['ostream'] = Notify.out()
__builtins__['run'] = simbase.run
__builtins__['taskMgr'] = simbase.taskMgr
__builtins__['jobMgr'] = simbase.jobMgr
__builtins__['eventMgr'] = simbase.eventMgr
__builtins__['messenger'] = simbase.messenger
__builtins__['bboard'] = simbase.bboard
__builtins__['config'] = simbase.config
__builtins__['directNotify'] = directNotify
from direct.showbase import Loader
simbase.loader = Loader.Loader(simbase)
__builtins__['loader'] = simbase.loader
directNotify.setDconfigLevels()

def inspect(anObject):
    from direct.tkpanels import Inspector
    Inspector.inspect(anObject)


__builtins__['inspect'] = inspect
if not __debug__ and __dev__:
    notify = directNotify.newCategory('ShowBaseGlobal')
    notify.error("You must set 'want-dev' to false in non-debug mode.")
taskMgr.finalInit()
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\otp\ai\AIBaseGlobal.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:15:03 Pacific Daylight Time
