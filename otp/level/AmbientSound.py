# 2013.08.22 22:15:28 Pacific Daylight Time
# Embedded file name: otp.level.AmbientSound
from direct.interval.IntervalGlobal import *
import BasicEntities
import random

class AmbientSound(BasicEntities.NodePathEntity):
    __module__ = __name__

    def __init__(self, level, entId):
        BasicEntities.NodePathEntity.__init__(self, level, entId)
        self.initSound()

    def destroy(self):
        self.destroySound()
        BasicEntities.NodePathEntity.destroy(self)

    def initSound(self):
        if not self.enabled:
            return
        if self.soundPath == '':
            return
        self.sound = base.loadSfx(self.soundPath)
        if self.sound is None:
            return
        self.soundIval = SoundInterval(self.sound, node=self, volume=self.volume)
        self.soundIval.loop()
        self.soundIval.setT(random.random() * self.sound.length())
        return

    def destroySound(self):
        if hasattr(self, 'soundIval'):
            self.soundIval.pause()
            del self.soundIval
        if hasattr(self, 'sound'):
            del self.sound

    if __dev__:

        def attribChanged(self, *args):
            self.destroySound()
            self.initSound()
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\otp\level\AmbientSound.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:15:28 Pacific Daylight Time
