# 2013.08.22 22:20:56 Pacific Daylight Time
# Embedded file name: toontown.hood.PetShopFishAnimatedProp
import AnimatedProp
from direct.actor import Actor
from direct.interval.IntervalGlobal import *

class PetShopFishAnimatedProp(AnimatedProp.AnimatedProp):
    __module__ = __name__

    def __init__(self, node):
        AnimatedProp.AnimatedProp.__init__(self, node)
        parent = node.getParent()
        self.fish = Actor.Actor(node, copy=0)
        self.fish.reparentTo(parent)
        self.fish.loadAnims({'swim': 'phase_4/models/props/exteriorfish-swim'})
        self.fish.pose('swim', 0)
        self.node = self.fish

    def delete(self):
        AnimatedProp.AnimatedProp.delete(self)
        self.fish.cleanup()
        del self.fish
        del self.node

    def enter(self):
        AnimatedProp.AnimatedProp.enter(self)
        self.fish.loop('swim')

    def exit(self):
        AnimatedProp.AnimatedProp.exit(self)
        self.fish.stop()
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\hood\PetShopFishAnimatedProp.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:20:56 Pacific Daylight Time
