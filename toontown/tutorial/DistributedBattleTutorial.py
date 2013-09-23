from toontown.battle import DistributedBattle
from direct.directnotify import DirectNotifyGlobal

class DistributedBattleTutorial(DistributedBattle.DistributedBattle):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBattleTutorial')

    def startTimer(self, ts = 0):
        self.townBattle.timer.hide()

    def playReward(self, ts):
        self.movie.playTutorialReward(ts, self.uniqueName('reward'), self.handleRewardDone)
