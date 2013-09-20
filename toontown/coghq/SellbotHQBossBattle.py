# 2013.08.22 22:19:20 Pacific Daylight Time
# Embedded file name: toontown.coghq.SellbotHQBossBattle
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from toontown.suit import DistributedSellbotBoss
from direct.directnotify import DirectNotifyGlobal
from toontown.coghq import CogHQBossBattle

class SellbotHQBossBattle(CogHQBossBattle.CogHQBossBattle):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('SellbotHQBossBattle')

    def __init__(self, loader, parentFSM, doneEvent):
        CogHQBossBattle.CogHQBossBattle.__init__(self, loader, parentFSM, doneEvent)
        self.teleportInPosHpr = (0, 95, 18, 180, 0, 0)

    def load(self):
        CogHQBossBattle.CogHQBossBattle.load(self)

    def unload(self):
        CogHQBossBattle.CogHQBossBattle.unload(self)

    def enter(self, requestStatus):
        CogHQBossBattle.CogHQBossBattle.enter(self, requestStatus, DistributedSellbotBoss.OneBossCog)
        self.__setupHighSky()

    def exit(self):
        CogHQBossBattle.CogHQBossBattle.exit(self)
        self.__cleanupHighSky()

    def __setupHighSky(self):
        self.loader.hood.startSky()
        sky = self.loader.hood.sky
        sky.setH(150)
        sky.setZ(-100)

    def __cleanupHighSky(self):
        self.loader.hood.stopSky()
        sky = self.loader.hood.sky
        sky.setH(0)
        sky.setZ(0)
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\coghq\SellbotHQBossBattle.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:19:20 Pacific Daylight Time
