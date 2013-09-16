# 2013.08.22 22:18:00 Pacific Daylight Time
# Embedded file name: toontown.cogdominium.DistributedCogdoBattleBldg
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import TTLocalizer
from toontown.battle import DistributedBattleBldg

class DistributedCogdoBattleBldg(DistributedBattleBldg.DistributedBattleBldg):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedCogdoBattleBldg')

    def __init__(self, cr):
        DistributedBattleBldg.DistributedBattleBldg.__init__(self, cr)

    def getBossBattleTaunt(self):
        return TTLocalizer.CogdoBattleBldgBossTaunt
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\cogdominium\DistributedCogdoBattleBldg.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:18:00 Pacific Daylight Time
