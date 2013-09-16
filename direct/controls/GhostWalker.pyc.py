# 2013.08.22 22:13:46 Pacific Daylight Time
# Embedded file name: direct.controls.GhostWalker
from direct.showbase.ShowBaseGlobal import *
from direct.directnotify import DirectNotifyGlobal
import NonPhysicsWalker

class GhostWalker(NonPhysicsWalker.NonPhysicsWalker):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('GhostWalker')
    slideName = 'jump'
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\controls\GhostWalker.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:13:46 Pacific Daylight Time
