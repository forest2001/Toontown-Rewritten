# 2013.08.22 22:26:54 Pacific Daylight Time
# Embedded file name: toontown.tutorial.DistributedBattleTutorial
from toontown.battle import DistributedBattle
from direct.directnotify import DirectNotifyGlobal

class DistributedBattleTutorial(DistributedBattle.DistributedBattle):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBattleTutorial')

    def startTimer(self, ts = 0):
        self.townBattle.timer.hide()

    def playReward(self, ts):
        self.movie.playTutorialReward(ts, self.uniqueName('reward'), self.handleRewardDone)
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\tutorial\DistributedBattleTutorial.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:26:54 Pacific Daylight Time
