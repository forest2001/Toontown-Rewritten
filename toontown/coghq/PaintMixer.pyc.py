# 2013.08.22 22:19:19 Pacific Daylight Time
# Embedded file name: toontown.coghq.PaintMixer
import PlatformEntity

class PaintMixer(PlatformEntity.PlatformEntity):
    __module__ = __name__

    def start(self):
        PlatformEntity.PlatformEntity.start(self)
        model = self.platform.model
        shaft = model.find('**/PaintMixerBase1')
        shaft.setSz(self.shaftScale)
        shaft.node().setPreserveTransform(0)
        shaftChild = shaft.find('**/PaintMixerBase')
        shaftChild.node().setPreserveTransform(0)
        model.flattenMedium()
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\coghq\PaintMixer.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:19:19 Pacific Daylight Time
