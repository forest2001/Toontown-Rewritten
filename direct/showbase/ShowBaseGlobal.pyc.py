# 2013.08.22 22:14:49 Pacific Daylight Time
# Embedded file name: direct.showbase.ShowBaseGlobal
__all__ = []
from ShowBase import *
directNotify.setDconfigLevels()

def inspect(anObject):
    from direct.tkpanels import Inspector
    return Inspector.inspect(anObject)


import __builtin__
__builtin__.inspect = inspect
if not __debug__ and __dev__:
    notify = directNotify.newCategory('ShowBaseGlobal')
    notify.error("You must set 'want-dev' to false in non-debug mode.")
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\showbase\ShowBaseGlobal.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:14:49 Pacific Daylight Time
