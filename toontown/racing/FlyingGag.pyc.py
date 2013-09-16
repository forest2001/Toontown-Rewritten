# 2013.08.22 22:24:14 Pacific Daylight Time
# Embedded file name: toontown.racing.FlyingGag
from pandac.PandaModules import *
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from otp.avatar.ShadowCaster import ShadowCaster

class FlyingGag(NodePath, ShadowCaster):
    __module__ = __name__

    def __init__(self, name, geom = None):
        an = ActorNode('flyingGagAN')
        NodePath.__init__(self, an)
        self.actorNode = an
        self.gag = None
        self.gagNode = None
        ShadowCaster.__init__(self, False)
        if geom:
            self.gagNode = self.attachNewNode('PieNode')
            self.gag = geom.copyTo(self.gagNode)
            self.gag.setScale(3)
            self.gagNode.setHpr(0, -45, 0)
            self.gagNode.setPos(0, 0, 2)
            self.initializeDropShadow()
            self.setActiveShadow()
            self.dropShadow.setPos(0, 0, 2)
            self.dropShadow.setScale(3)
        return

    def delete(self):
        ShadowCaster.delete(self)
        NodePath.remove(self)
        self.gag = None
        return

    def getGeomNode(self):
        return self.gag
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\racing\FlyingGag.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:24:14 Pacific Daylight Time
