# 2013.08.22 22:21:14 Pacific Daylight Time
# Embedded file name: toontown.minigame.CogThiefWalk
from toontown.safezone import Walk

class CogThiefWalk(Walk.Walk):
    __module__ = __name__
    notify = directNotify.newCategory('CogThiefWalk')

    def __init__(self, doneEvent):
        Walk.Walk.__init__(self, doneEvent)

    def enter(self, slowWalk = 0):
        base.localAvatar.startPosHprBroadcast()
        base.localAvatar.startBlink()
        base.localAvatar.showName()
        base.localAvatar.collisionsOn()
        base.localAvatar.startGlitchKiller()
        base.localAvatar.enableAvatarControls()

    def exit(self):
        self.fsm.request('off')
        self.ignore('control')
        base.localAvatar.disableAvatarControls()
        base.localAvatar.stopPosHprBroadcast()
        base.localAvatar.stopBlink()
        base.localAvatar.stopGlitchKiller()
        base.localAvatar.collisionsOff()
        base.localAvatar.controlManager.placeOnFloor()
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\minigame\CogThiefWalk.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:21:14 Pacific Daylight Time
