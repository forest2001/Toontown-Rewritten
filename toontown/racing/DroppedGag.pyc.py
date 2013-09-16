# 2013.08.22 22:24:13 Pacific Daylight Time
# Embedded file name: toontown.racing.DroppedGag
from pandac.PandaModules import *
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from otp.avatar import ShadowCaster

class DroppedGag(NodePath, ShadowCaster.ShadowCaster):
    __module__ = __name__

    def __init__(self, name, geom):
        NodePath.__init__(self, name)
        ShadowCaster.ShadowCaster.__init__(self, False)
        self.gag = geom.copyTo(self)
        self.initializeDropShadow()
        self.setActiveShadow()
        self.dropShadow.setScale(1)

    def delete(self):
        ShadowCaster.ShadowCaster.delete(self)
        NodePath.removeNode(self)
        self.gag = None
        return

    def getGeomNode(self):
        return self.gag
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\racing\DroppedGag.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:24:13 Pacific Daylight Time
