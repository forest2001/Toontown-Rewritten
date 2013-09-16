# 2013.08.22 22:19:31 Pacific Daylight Time
# Embedded file name: toontown.effects.DistributedFireworkShow
from direct.distributed import DistributedObject
from toontown.effects.FireworkShowMixin import FireworkShowMixin

class DistributedFireworkShow(DistributedObject.DistributedObject, FireworkShowMixin):
    __module__ = __name__
    notify = directNotify.newCategory('DistributedFireworkShow')

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        FireworkShowMixin.__init__(self)

    def generate(self):
        DistributedObject.DistributedObject.generate(self)

    def disable(self):
        DistributedObject.DistributedObject.disable(self)
        FireworkShowMixin.disable(self)

    def delete(self):
        DistributedObject.DistributedObject.delete(self)

    def d_requestFirework(self, x, y, z, style, color1, color2):
        self.sendUpdate('requestFirework', (x,
         y,
         z,
         style,
         color1,
         color2))
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\effects\DistributedFireworkShow.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:19:31 Pacific Daylight Time
