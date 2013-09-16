# 2013.08.22 22:13:46 Pacific Daylight Time
# Embedded file name: direct.actor.DistributedActor
__all__ = ['DistributedActor']
from direct.distributed import DistributedNode
import Actor

class DistributedActor(DistributedNode.DistributedNode, Actor.Actor):
    __module__ = __name__

    def __init__(self, cr):
        try:
            self.DistributedActor_initialized
        except:
            self.DistributedActor_initialized = 1
            Actor.Actor.__init__(self)
            DistributedNode.DistributedNode.__init__(self, cr)
            self.setCacheable(1)

    def disable(self):
        if not self.isEmpty():
            Actor.Actor.unloadAnims(self, None, None, None)
        DistributedNode.DistributedNode.disable(self)
        return

    def delete(self):
        try:
            self.DistributedActor_deleted
        except:
            self.DistributedActor_deleted = 1
            DistributedNode.DistributedNode.delete(self)
            Actor.Actor.delete(self)

    def loop(self, animName, restart = 1, partName = None, fromFrame = None, toFrame = None):
        return Actor.Actor.loop(self, animName, restart, partName, fromFrame, toFrame)
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\actor\DistributedActor.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:13:46 Pacific Daylight Time
