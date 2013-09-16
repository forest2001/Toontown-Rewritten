# 2013.08.22 22:15:30 Pacific Daylight Time
# Embedded file name: otp.level.EditMgrBase
import Entity
from direct.directnotify import DirectNotifyGlobal

class EditMgrBase(Entity.Entity):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('EditMgr')

    def __init__(self, level, entId):
        Entity.Entity.__init__(self, level, entId)

    def destroy(self):
        Entity.Entity.destroy(self)
        self.ignoreAll()

    if __dev__:

        def setInsertEntity(self, data):
            self.level.setEntityCreatorUsername(data['entId'], data['username'])
            self.level.levelSpec.insertEntity(data['entId'], data['entType'], data['parentEntId'])
            self.level.levelSpec.doSetAttrib(self.entId, 'insertEntity', None)
            return

        def setRemoveEntity(self, data):
            self.level.levelSpec.removeEntity(data['entId'])
            self.level.levelSpec.doSetAttrib(self.entId, 'removeEntity', None)
            return
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\otp\level\EditMgrBase.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:15:30 Pacific Daylight Time
