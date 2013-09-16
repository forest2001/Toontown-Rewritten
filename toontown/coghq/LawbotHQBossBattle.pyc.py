# 2013.08.22 22:19:06 Pacific Daylight Time
# Embedded file name: toontown.coghq.LawbotHQBossBattle
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from toontown.suit import DistributedLawbotBoss
from direct.directnotify import DirectNotifyGlobal
from toontown.coghq import CogHQBossBattle

class LawbotHQBossBattle(CogHQBossBattle.CogHQBossBattle):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('LawbotHQBossBattle')

    def __init__(self, loader, parentFSM, doneEvent):
        CogHQBossBattle.CogHQBossBattle.__init__(self, loader, parentFSM, doneEvent)
        self.teleportInPosHpr = (88, -214, 0, 210, 0, 0)

    def load(self):
        CogHQBossBattle.CogHQBossBattle.load(self)

    def unload(self):
        CogHQBossBattle.CogHQBossBattle.unload(self)

    def enter(self, requestStatus):
        CogHQBossBattle.CogHQBossBattle.enter(self, requestStatus, DistributedLawbotBoss.OneBossCog)

    def exit(self):
        CogHQBossBattle.CogHQBossBattle.exit(self)
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\coghq\LawbotHQBossBattle.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:19:07 Pacific Daylight Time
