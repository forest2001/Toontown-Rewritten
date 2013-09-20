# 2013.08.22 22:19:32 Pacific Daylight Time
# Embedded file name: toontown.effects.EffectController
from pandac.PandaModules import *

class EffectController():
    __module__ = __name__
    particleDummy = None

    def __init__(self):
        self.track = None
        self.startEffect = None
        self.endEffect = None
        self.f = None
        self.p0 = None
        return

    def createTrack(self):
        pass

    def destroy(self):
        self.finish()
        if self.f:
            self.f.cleanup()
        self.f = None
        self.p0 = None
        self.removeNode()
        return

    def cleanUpEffect(self):
        if self.f:
            self.setPosHpr(0, 0, 0, 0, 0, 0)
            self.f.disable()
            self.detachNode()

    def reallyCleanUpEffect(self):
        self.cleanUpEffect()
        self.finish()

    def play(self, lod = None):
        if lod != None:
            try:
                self.createTrack(lod)
            except TypeError as e:
                raise TypeError('Error loading %s effect.' % self.__class__.__name__)

        else:
            self.createTrack()
        self.track.start()
        return

    def stop(self):
        if self.track:
            self.track.pause()
            self.track = None
        if self.startEffect:
            self.startEffect.pause()
            self.startEffect = None
        if self.endEffect:
            self.endEffect.pause()
            self.endEffect = None
        self.cleanUpEffect()
        return

    def finish(self):
        if self.track:
            self.track.pause()
            self.track = None
        if self.startEffect:
            self.startEffect.pause()
            self.startEffect = None
        if self.endEffect:
            self.endEffect.pause()
            self.endEffect = None
        return

    def startLoop(self, lod = None):
        if lod != None:
            try:
                self.createTrack(lod)
            except TypeError as e:
                raise TypeError('Error loading %s effect.' % self.__class__.__name__)

        else:
            self.createTrack()
        if self.startEffect:
            self.startEffect.start()
        return

    def stopLoop(self):
        if self.startEffect:
            self.startEffect.pause()
            self.startEffect = None
        if self.endEffect and not self.endEffect.isPlaying():
            self.endEffect.start()
        return

    def getTrack(self):
        if not self.track:
            self.createTrack()
        return self.track

    def enableEffect(self):
        if self.f and self.particleDummy:
            self.f.start(self, self.particleDummy)
        elif self.f:
            self.f.start(self, self)

    def disableEffect(self):
        if self.f:
            self.f.disable()
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\effects\EffectController.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:19:32 Pacific Daylight Time
