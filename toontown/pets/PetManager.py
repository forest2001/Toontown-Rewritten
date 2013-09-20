# 2013.08.22 22:23:54 Pacific Daylight Time
# Embedded file name: toontown.pets.PetManager
from pandac.PandaModules import *
from toontown.toonbase import ToontownGlobals
from direct.task import Task

def acquirePetManager():
    if not hasattr(base, 'petManager'):
        PetManager()
    base.petManager.incRefCount()


def releasePetManager():
    base.petManager.decRefCount()


class PetManager():
    __module__ = __name__
    CollTaskName = 'petFloorCollisions'

    def __init__(self):
        base.petManager = self
        self.refCount = 0
        self.cTrav = CollisionTraverser('petFloorCollisions')
        taskMgr.add(self._doCollisions, PetManager.CollTaskName, priority=ToontownGlobals.PetFloorCollPriority)

    def _destroy(self):
        taskMgr.remove(PetManager.CollTaskName)
        del self.cTrav

    def _doCollisions(self, task):
        self.cTrav.traverse(render)
        return Task.cont

    def incRefCount(self):
        self.refCount += 1

    def decRefCount(self):
        self.refCount -= 1
        if self.refCount == 0:
            self._destroy()
            del base.petManager
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\pets\PetManager.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:23:54 Pacific Daylight Time
