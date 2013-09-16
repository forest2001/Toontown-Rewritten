# 2013.08.22 22:15:31 Pacific Daylight Time
# Embedded file name: otp.level.EntityCreator
import CutScene
import EntityCreatorBase
import BasicEntities
from direct.directnotify import DirectNotifyGlobal
import EditMgr
import EntrancePoint
import LevelMgr
import LogicGate
import ZoneEntity
import ModelEntity
import PathEntity
import VisibilityExtender
import PropSpinner
import AmbientSound
import LocatorEntity
import CollisionSolidEntity

def nothing(*args):
    return 'nothing'


def nonlocal(*args):
    return 'nonlocal'


class EntityCreator(EntityCreatorBase.EntityCreatorBase):
    __module__ = __name__

    def __init__(self, level):
        EntityCreatorBase.EntityCreatorBase.__init__(self, level)
        self.level = level
        self.privRegisterTypes({'attribModifier': nothing,
         'ambientSound': AmbientSound.AmbientSound,
         'collisionSolid': CollisionSolidEntity.CollisionSolidEntity,
         'cutScene': CutScene.CutScene,
         'editMgr': EditMgr.EditMgr,
         'entityGroup': nothing,
         'entrancePoint': EntrancePoint.EntrancePoint,
         'levelMgr': LevelMgr.LevelMgr,
         'locator': LocatorEntity.LocatorEntity,
         'logicGate': LogicGate.LogicGate,
         'model': ModelEntity.ModelEntity,
         'nodepath': BasicEntities.NodePathEntity,
         'path': PathEntity.PathEntity,
         'propSpinner': PropSpinner.PropSpinner,
         'visibilityExtender': VisibilityExtender.VisibilityExtender,
         'zone': ZoneEntity.ZoneEntity})

    def doCreateEntity(self, ctor, entId):
        return ctor(self.level, entId)
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\otp\level\EntityCreator.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:15:31 Pacific Daylight Time
