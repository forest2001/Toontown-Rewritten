# 2013.08.22 22:17:55 Pacific Daylight Time
# Embedded file name: toontown.cogdominium.DistCogdoBoardroomGame
from direct.directnotify.DirectNotifyGlobal import directNotify
from toontown.cogdominium.DistCogdoLevelGame import DistCogdoLevelGame
from toontown.cogdominium.CogdoBoardroomGameBase import CogdoBoardroomGameBase
from toontown.cogdominium import CogdoBoardroomGameConsts as Consts
from toontown.toonbase import ToontownTimer
from toontown.toonbase import TTLocalizer as TTL

class DistCogdoBoardroomGame(CogdoBoardroomGameBase, DistCogdoLevelGame):
    __module__ = __name__
    notify = directNotify.newCategory('DistCogdoBoardroomGame')

    def __init__(self, cr):
        DistCogdoLevelGame.__init__(self, cr)

    def getTitle(self):
        return TTL.BoardroomGameTitle

    def getInstructions(self):
        return TTL.BoardroomGameInstructions

    def announceGenerate(self):
        DistCogdoLevelGame.announceGenerate(self)
        self.timer = ToontownTimer.ToontownTimer()
        self.timer.setScale(Consts.Settings.TimerScale.get())
        self.timer.stash()

    def disable(self):
        self.timer.destroy()
        self.timer = None
        DistCogdoLevelGame.disable(self)
        return

    def enterGame(self):
        DistCogdoLevelGame.enterGame(self)
        timeLeft = Consts.GameDuration.get() - (globalClock.getRealTime() - self.getStartTime())
        self.timer.setTime(timeLeft)
        self.timer.countdown(timeLeft, self.timerExpired)
        self.timer.unstash()

    def enterFinish(self):
        DistCogdoLevelGame.enterFinish(self)
        timeLeft = Consts.FinishDuration.get() - (globalClock.getRealTime() - self.getFinishTime())
        self.timer.setTime(timeLeft)
        self.timer.countdown(timeLeft, self.timerExpired)
        self.timer.unstash()

    def timerExpired(self):
        pass

    if __dev__:

        def _handleTimerScaleChanged(self, timerScale):
            if hasattr(self, 'timer'):
                self.timer.setScale(timerScale)
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\cogdominium\DistCogdoBoardroomGame.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:17:56 Pacific Daylight Time
