# 2013.08.22 22:14:25 Pacific Daylight Time
# Embedded file name: direct.interval.SoundInterval
__all__ = ['SoundInterval']
from pandac.PandaModules import *
from direct.directnotify.DirectNotifyGlobal import *
import Interval
import random

class SoundInterval(Interval.Interval):
    __module__ = __name__
    soundNum = 1
    notify = directNotify.newCategory('SoundInterval')

    def __init__(self, sound, loop = 0, duration = 0.0, name = None, volume = 1.0, startTime = 0.0, node = None, seamlessLoop = True, listenerNode = None, cutOff = None):
        id = 'Sound-%d' % SoundInterval.soundNum
        SoundInterval.soundNum += 1
        self.sound = sound
        if sound:
            self.soundDuration = sound.length()
        else:
            self.soundDuration = 0
        self.fLoop = loop
        self.volume = volume
        self.startTime = startTime
        self.node = node
        self.listenerNode = listenerNode
        self.cutOff = cutOff
        self._seamlessLoop = seamlessLoop
        if self._seamlessLoop:
            self._fLoop = True
        self._soundPlaying = False
        if float(duration) == 0.0 and self.sound != None:
            duration = max(self.soundDuration - self.startTime, 0)
        if name == None:
            name = id
        Interval.Interval.__init__(self, name, duration)
        return

    def privInitialize(self, t):
        t1 = t + self.startTime
        if t1 < 0.1:
            t1 = 0.0
        if t1 < self.soundDuration:
            self._seamlessLoop and not self._soundPlaying and base.sfxPlayer.playSfx(self.sound, self.fLoop, 1, self.volume, t1, self.node, listenerNode=self.listenerNode, cutoff=self.cutOff)
            self._soundPlaying = True
        self.state = CInterval.SStarted
        self.currT = t

    def privStep(self, t):
        if self.state == CInterval.SPaused:
            t1 = t + self.startTime
            if t1 < self.soundDuration:
                base.sfxPlayer.playSfx(self.sound, self.fLoop, 1, self.volume, t1, self.node, listenerNode=self.listenerNode)
        if self.listenerNode and not self.listenerNode.isEmpty() and self.node and not self.node.isEmpty():
            base.sfxPlayer.setFinalVolume(self.sound, self.node, self.volume, self.listenerNode, self.cutOff)
        self.state = CInterval.SStarted
        self.currT = t

    def finish(self, *args, **kArgs):
        self._inFinish = True
        Interval.Interval.finish(self, *args, **kArgs)
        del self._inFinish

    def privFinalize(self):
        if self._seamlessLoop and self._soundPlaying and self.getLoop() and not hasattr(self, '_inFinish'):
            base.sfxPlayer.setFinalVolume(self.sound, self.node, self.volume, self.listenerNode, self.cutOff)
            return
        elif self.sound != None:
            self.sound.stop()
            self._soundPlaying = False
        self.currT = self.getDuration()
        self.state = CInterval.SFinal
        return

    def privInterrupt(self):
        if self.sound != None:
            self.sound.stop()
            self._soundPlaying = False
        self.state = CInterval.SPaused
        return

    def loop(self, startT = 0.0, endT = -1.0, playRate = 1.0, stagger = False):
        self.fLoop = 1
        Interval.Interval.loop(self, startT, endT, playRate)
        if stagger:
            self.setT(random.random() * self.getDuration())
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\interval\SoundInterval.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:14:25 Pacific Daylight Time
