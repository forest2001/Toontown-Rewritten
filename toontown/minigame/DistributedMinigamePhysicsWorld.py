# 2013.08.22 22:21:29 Pacific Daylight Time
# Embedded file name: toontown.minigame.DistributedMinigamePhysicsWorld
from direct.distributed import DistributedObject
from direct.directnotify import DirectNotifyGlobal
from toontown.minigame import MinigamePhysicsWorldBase

class DistributedMinigamePhysicsWorld(DistributedObject.DistributedObject, MinigamePhysicsWorldBase.MinigamePhysicsWorldBase):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedMinigamePhysicsWorld')

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        MinigamePhysicsWorldBase.MinigamePhysicsWorldBase.__init__(self, canRender=1)

    def delete(self):
        MinigamePhysicsWorldBase.MinigamePhysicsWorldBase.delete(self)
        DistributedObject.DistributedObject.delete(self)
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\minigame\DistributedMinigamePhysicsWorld.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:21:29 Pacific Daylight Time
