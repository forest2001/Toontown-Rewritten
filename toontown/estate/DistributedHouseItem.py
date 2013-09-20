# 2013.08.22 22:20:10 Pacific Daylight Time
# Embedded file name: toontown.estate.DistributedHouseItem
from toontown.toonbase.ToontownGlobals import *
from direct.interval.IntervalGlobal import *
from direct.distributed.ClockDelta import *
from toontown.toonbase import ToontownGlobals
from direct.distributed import DistributedObject
from toontown.toonbase import TTLocalizer

class DistributedHouseItem(DistributedObject.DistributedObject):
    __module__ = __name__
    notify = directNotify.newCategory('DistributedHouseItem')

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)

    def generate(self):
        DistributedObject.DistributedObject.generate(self)

    def announceGenerate(self):
        DistributedObject.DistributedObject.announceGenerate(self)
        self.load()

    def load(self):
        pass

    def disable(self):
        DistributedObject.DistributedObject.disable(self)

    def delete(self):
        DistributedObject.DistributedObject.delete(self)
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\estate\DistributedHouseItem.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:20:10 Pacific Daylight Time
