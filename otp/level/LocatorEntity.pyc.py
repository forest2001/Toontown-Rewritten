# 2013.08.22 22:15:34 Pacific Daylight Time
# Embedded file name: otp.level.LocatorEntity
import Entity, BasicEntities
from pandac.PandaModules import NodePath
from direct.directnotify import DirectNotifyGlobal

class LocatorEntity(Entity.Entity, NodePath):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('LocatorEntity')

    def __init__(self, level, entId):
        node = hidden.attachNewNode('LocatorEntity-%s' % entId)
        NodePath.__init__(self, node)
        Entity.Entity.__init__(self, level, entId)
        self.doReparent()

    def destroy(self):
        Entity.Entity.destroy(self)
        self.removeNode()

    def getNodePath(self):
        return self

    def doReparent(self):
        if self.searchPath != '':
            parent = self.level.geom.find(self.searchPath)
            if parent.isEmpty():
                LocatorEntity.notify.warning("could not find '%s'" % self.searchPath)
                self.reparentTo(hidden)
            else:
                self.reparentTo(parent)

    if __dev__:

        def attribChanged(self, attrib, value):
            self.doReparent()
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\otp\level\LocatorEntity.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:15:34 Pacific Daylight Time
