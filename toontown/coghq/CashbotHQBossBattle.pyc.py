# 2013.08.22 22:18:11 Pacific Daylight Time
# Embedded file name: toontown.coghq.CashbotHQBossBattle
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from toontown.suit import DistributedCashbotBoss
from direct.directnotify import DirectNotifyGlobal
from toontown.coghq import CogHQBossBattle

class CashbotHQBossBattle(CogHQBossBattle.CogHQBossBattle):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('CashbotHQBossBattle')

    def __init__(self, loader, parentFSM, doneEvent):
        CogHQBossBattle.CogHQBossBattle.__init__(self, loader, parentFSM, doneEvent)
        self.teleportInPosHpr = (88, -214, 0, 210, 0, 0)

    def load(self):
        CogHQBossBattle.CogHQBossBattle.load(self)

    def unload(self):
        CogHQBossBattle.CogHQBossBattle.unload(self)

    def enter(self, requestStatus):
        CogHQBossBattle.CogHQBossBattle.enter(self, requestStatus, DistributedCashbotBoss.OneBossCog)

    def exit(self):
        CogHQBossBattle.CogHQBossBattle.exit(self)

    def exitCrane(self):
        CogHQBossBattle.CogHQBossBattle.exitCrane(self)
        messenger.send('exitCrane')
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\coghq\CashbotHQBossBattle.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:18:11 Pacific Daylight Time
