# 2013.08.22 22:15:29 Pacific Daylight Time
# Embedded file name: otp.level.DistributedEntityAI
from direct.distributed import DistributedObjectAI
import Entity
from direct.directnotify import DirectNotifyGlobal

class DistributedEntityAI(DistributedObjectAI.DistributedObjectAI, Entity.Entity):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedEntityAI')

    def __init__(self, level, entId):
        if hasattr(level, 'air'):
            air = level.air
            self.levelDoId = level.doId
        else:
            air = level
            level = None
            self.levelDoId = 0
        DistributedObjectAI.DistributedObjectAI.__init__(self, air)
        Entity.Entity.__init__(self, level, entId)
        return

    def generate(self):
        self.notify.debug('generate')
        DistributedObjectAI.DistributedObjectAI.generate(self)

    def destroy(self):
        self.notify.debug('destroy')
        Entity.Entity.destroy(self)
        self.requestDelete()

    def delete(self):
        self.notify.debug('delete')
        DistributedObjectAI.DistributedObjectAI.delete(self)

    def getLevelDoId(self):
        return self.levelDoId

    def getEntId(self):
        return self.entId

    if __dev__:

        def setParentEntId(self, parentEntId):
            self.parentEntId = parentEntId
            newZoneId = self.getZoneEntity().getZoneId()
            if newZoneId != self.zoneId:
                self.sendSetZone(newZoneId)
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\otp\level\DistributedEntityAI.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:15:29 Pacific Daylight Time
