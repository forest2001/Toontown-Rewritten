# 2013.08.22 22:21:55 Pacific Daylight Time
# Embedded file name: toontown.minigame.DivingTreasure
from direct.showbase.DirectObject import DirectObject
from toontown.toonbase.ToontownGlobals import *
from direct.directnotify import DirectNotifyGlobal
from direct.interval.IntervalGlobal import *
import DivingGameGlobals

class DivingTreasure(DirectObject):
    __module__ = __name__

    def __init__(self, i):
        self.treasureNode = render.attachNewNode('treasure')
        loadBase = 'phase_4/models/minigames/'
        self.chest = loader.loadModel(loadBase + 'treasure.bam')
        self.chest.reparentTo(self.treasureNode)
        self.chest.setPos(0, 0, -25)
        self.chest.setScale(1, 0.7, 1)
        self.chestId = i
        self.grabbedId = 0
        self.moveLerp = Sequence()
        self.treasureNode.setScale(0.04)
        self.treasureNode.setPos(-15 + 10.0 * i, 0.25, -36.0)
        cSphere = CollisionSphere(0.0, 0.0, 0.0, 45)
        cSphere.setTangible(0)
        name = str(i)
        cSphereNode = CollisionNode(name)
        cSphereNode.setIntoCollideMask(DivingGameGlobals.CollideMask)
        cSphereNode.addSolid(cSphere)
        self.chestNode = cSphereNode
        self.chestCNP = self.treasureNode.attachNewNode(cSphereNode)

    def destroy(self):
        self.ignoreAll()
        del self.chest
        self.moveLerp.finish()
        del self.moveLerp
        self.treasureNode.removeNode()
        del self.treasureNode
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\minigame\DivingTreasure.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:21:55 Pacific Daylight Time
