# 2013.08.22 22:17:33 Pacific Daylight Time
# Embedded file name: toontown.cogdominium.CogdoEntityCreator
from otp.level import EntityCreator
from toontown.cogdominium import CogdoCraneGameConsts
from toontown.cogdominium.CogdoLevelMgr import CogdoLevelMgr
from toontown.cogdominium import CogdoBoardroomGameConsts
from toontown.cogdominium import CogdoCraneGameConsts

class CogdoEntityCreator(EntityCreator.EntityCreator):
    __module__ = __name__

    def __init__(self, level):
        EntityCreator.EntityCreator.__init__(self, level)
        nothing = EntityCreator.nothing
        nonlocal = EntityCreator.nonlocal
        self.privRegisterTypes({'levelMgr': CogdoLevelMgr,
         'cogdoBoardroomGameSettings': Functor(self._createCogdoSettings, CogdoBoardroomGameConsts.Settings),
         'cogdoCraneGameSettings': Functor(self._createCogdoSettings, CogdoCraneGameConsts.Settings),
         'cogdoCraneCogSettings': Functor(self._createCogdoSettings, CogdoCraneGameConsts.CogSettings)})

    def _createCogdoSettings(self, ent, level, entId):
        ent.initializeEntity(level, entId)
        return ent
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\cogdominium\CogdoEntityCreator.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:17:33 Pacific Daylight Time
