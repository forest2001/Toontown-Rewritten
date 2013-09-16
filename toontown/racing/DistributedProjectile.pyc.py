# 2013.08.22 22:24:07 Pacific Daylight Time
# Embedded file name: toontown.racing.DistributedProjectile
from pandac.PandaModules import *
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.fsm import FSM
from direct.distributed.DistributedSmoothNode import DistributedSmoothNode
from otp.avatar.ShadowCaster import ShadowCaster

class DistributedProjectile(DistributedSmoothNode, ShadowCaster, NodePath):
    __module__ = __name__

    def __init__(self, cr):
        ShadowCaster.__init__(self)
        DistributedSmoothNode.__init__(self, cr)
        NodePath.__init__(self, 'Projectile')

    def announceGenerate(self):
        DistributedSmoothNode.announceGenerate(self)
        self.name = self.uniqueName('projectile')
        self.posHprBroadcastName = self.uniqueName('projectileBroadcast')
        geom = loader.loadModel('models/smiley')
        self.geom = geom
        self.geom.reparentTo(self)
        self.startSmooth()
        self.reparentTo(render)

    def generate(self):
        DistributedSmoothNode.generate(self)
        self.name = self.uniqueName('projectile')
        self.posHprBroadcastName = self.uniqueName('projectileBroadcast')
        geom = loader.loadModel('models/smiley')
        self.geom = geom
        self.geom.reparentTo(self)
        self.startSmooth()
        self.reparentTo(render)

    def setAvId(self, avId):
        self.avId = avId

    def delete(self):
        DistributedSmoothNode.delete(self)
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\racing\DistributedProjectile.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:24:07 Pacific Daylight Time
