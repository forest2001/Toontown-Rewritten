# 2013.08.22 22:25:27 Pacific Daylight Time
# Embedded file name: toontown.suit.DistributedMintSuit
from toontown.suit import DistributedFactorySuit
from direct.directnotify import DirectNotifyGlobal

class DistributedMintSuit(DistributedFactorySuit.DistributedFactorySuit):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedMintSuit')
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\suit\DistributedMintSuit.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:25:27 Pacific Daylight Time
