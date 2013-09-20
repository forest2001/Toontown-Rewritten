# 2013.08.22 22:18:05 Pacific Daylight Time
# Embedded file name: toontown.coghq.BossbotHQBossBattle
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from toontown.suit import DistributedBossbotBoss
from direct.directnotify import DirectNotifyGlobal
from toontown.coghq import CogHQBossBattle

class BossbotHQBossBattle(CogHQBossBattle.CogHQBossBattle):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('BossbotHQBossBattle')

    def __init__(self, loader, parentFSM, doneEvent):
        CogHQBossBattle.CogHQBossBattle.__init__(self, loader, parentFSM, doneEvent)
        self.teleportInPosHpr = (88, -214, 0, 210, 0, 0)
        for stateName in ['movie']:
            state = self.fsm.getStateNamed(stateName)
            state.addTransition('crane')

        state = self.fsm.getStateNamed('finalBattle')
        state.addTransition('finalBattle')

    def load(self):
        CogHQBossBattle.CogHQBossBattle.load(self)

    def unload(self):
        CogHQBossBattle.CogHQBossBattle.unload(self)

    def enter(self, requestStatus):
        CogHQBossBattle.CogHQBossBattle.enter(self, requestStatus, DistributedBossbotBoss.OneBossCog)

    def exit(self):
        CogHQBossBattle.CogHQBossBattle.exit(self)

    def exitCrane(self):
        CogHQBossBattle.CogHQBossBattle.exitCrane(self)
        messenger.send('exitCrane')
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\coghq\BossbotHQBossBattle.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:18:05 Pacific Daylight Time
