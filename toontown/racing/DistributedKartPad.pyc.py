# 2013.08.22 22:24:06 Pacific Daylight Time
# Embedded file name: toontown.racing.DistributedKartPad
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObject import DistributedObject
if __debug__:
    import pdb

class DistributedKartPad(DistributedObject):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedKartPad')

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        self.startingBlocks = []

    def delete(self):
        del self.startingBlocks
        DistributedObject.delete(self)

    def setArea(self, area):
        self.area = area

    def getArea(self):
        return self.area

    def addStartingBlock(self, block):
        self.startingBlocks.append(block)
        self.notify.debug('KartPad %s has added starting block %s' % (self.doId, block.doId))
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\racing\DistributedKartPad.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:24:06 Pacific Daylight Time
