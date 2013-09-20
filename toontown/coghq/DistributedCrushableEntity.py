# 2013.08.22 22:18:33 Pacific Daylight Time
# Embedded file name: toontown.coghq.DistributedCrushableEntity
from otp.level import DistributedEntity
from direct.directnotify import DirectNotifyGlobal
from pandac.PandaModules import NodePath
from otp.level import BasicEntities

class DistributedCrushableEntity(DistributedEntity.DistributedEntity, NodePath, BasicEntities.NodePathAttribs):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedCrushableEntity')

    def __init__(self, cr):
        DistributedEntity.DistributedEntity.__init__(self, cr)
        node = hidden.attachNewNode('DistributedNodePathEntity')

    def initNodePath(self):
        node = hidden.attachNewNode('DistributedNodePathEntity')
        NodePath.__init__(self, node)

    def announceGenerate(self):
        DistributedEntity.DistributedEntity.announceGenerate(self)
        BasicEntities.NodePathAttribs.initNodePathAttribs(self)

    def disable(self):
        self.reparentTo(hidden)
        BasicEntities.NodePathAttribs.destroy(self)
        DistributedEntity.DistributedEntity.disable(self)

    def delete(self):
        self.removeNode()
        DistributedEntity.DistributedEntity.delete(self)

    def setPosition(self, x, y, z):
        self.setPos(x, y, z)

    def setCrushed(self, crusherId, axis):
        self.playCrushMovie(crusherId, axis)

    def playCrushMovie(self, crusherId, axis):
        pass
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\coghq\DistributedCrushableEntity.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:18:33 Pacific Daylight Time
