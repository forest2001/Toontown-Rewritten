# 2013.08.22 22:14:03 Pacific Daylight Time
# Embedded file name: direct.distributed.DistributedNodeAI
from pandac.PandaModules import NodePath
import DistributedObjectAI
import GridParent
import types

class DistributedNodeAI(DistributedObjectAI.DistributedObjectAI, NodePath):
    __module__ = __name__

    def __init__(self, air, name = None):
        try:
            self.DistributedNodeAI_initialized
        except:
            self.DistributedNodeAI_initialized = 1
            DistributedObjectAI.DistributedObjectAI.__init__(self, air)
            if name is None:
                name = self.__class__.__name__
            NodePath.__init__(self, name)
            self.gridParent = None

        return

    def delete(self):
        if self.gridParent:
            self.gridParent.delete()
            self.gridParent = None
        if not self.isEmpty():
            self.removeNode()
        DistributedObjectAI.DistributedObjectAI.delete(self)
        return

    def setLocation(self, parentId, zoneId, teleport = 0):
        DistributedObjectAI.DistributedObjectAI.setLocation(self, parentId, zoneId)
        parentObj = self.air.doId2do.get(parentId)
        if parentObj:
            if parentObj.isGridParent():
                if not self.gridParent:
                    self.gridParent = GridParent.GridParent(self)
                self.gridParent.setGridParent(parentObj, zoneId)
            elif self.gridParent:
                self.gridParent.delete()
                self.gridParent = None
        return

    def b_setParent(self, parentToken):
        if type(parentToken) == types.StringType:
            self.setParentStr(parentToken)
        else:
            self.setParent(parentToken)
        self.d_setParent(parentToken)

    def d_setParent(self, parentToken):
        if type(parentToken) == type(''):
            self.sendUpdate('setParentStr', [parentToken])
        else:
            self.sendUpdate('setParent', [parentToken])

    def setParentStr(self, parentToken):
        self.notify.debug('setParentStr(%s): %s' % (self.doId, parentToken))
        if len(parentToken) > 0:
            self.do_setParent(parentToken)

    def setParent(self, parentToken):
        self.notify.debug('setParent(%s): %s' % (self.doId, parentToken))
        if parentToken == 0:
            senderId = self.air.getAvatarIdFromSender()
            self.air.writeServerEvent('suspicious', senderId, 'setParent(0)')
        else:
            self.do_setParent(parentToken)

    def do_setParent(self, parentToken):
        self.getParentMgr().requestReparent(self, parentToken)

    def d_setX(self, x):
        self.sendUpdate('setX', [x])

    def d_setY(self, y):
        self.sendUpdate('setY', [y])

    def d_setZ(self, z):
        self.sendUpdate('setZ', [z])

    def d_setH(self, h):
        self.sendUpdate('setH', [h])

    def d_setP(self, p):
        self.sendUpdate('setP', [p])

    def d_setR(self, r):
        self.sendUpdate('setR', [r])

    def setXY(self, x, y):
        self.setX(x)
        self.setY(y)

    def d_setXY(self, x, y):
        self.sendUpdate('setXY', [x, y])

    def d_setPos(self, x, y, z):
        self.sendUpdate('setPos', [x, y, z])

    def d_setHpr(self, h, p, r):
        self.sendUpdate('setHpr', [h, p, r])

    def setXYH(self, x, y, h):
        self.setX(x)
        self.setY(y)
        self.setH(h)

    def d_setXYH(self, x, y, h):
        self.sendUpdate('setXYH', [x, y, h])

    def b_setXYZH(self, x, y, z, h):
        self.setXYZH(x, y, z, h)
        self.d_setXYZH(x, y, z, h)

    def setXYZH(self, x, y, z, h):
        self.setPos(x, y, z)
        self.setH(h)

    def getXYZH(self):
        pos = self.getPos()
        h = self.getH()
        return (pos[0],
         pos[1],
         pos[2],
         h)

    def d_setXYZH(self, x, y, z, h):
        self.sendUpdate('setXYZH', [x,
         y,
         z,
         h])

    def b_setPosHpr(self, x, y, z, h, p, r):
        self.setPosHpr(x, y, z, h, p, r)
        self.d_setPosHpr(x, y, z, h, p, r)

    def d_setPosHpr(self, x, y, z, h, p, r):
        self.sendUpdate('setPosHpr', [x,
         y,
         z,
         h,
         p,
         r])
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\distributed\DistributedNodeAI.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:14:03 Pacific Daylight Time
