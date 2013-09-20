# 2013.08.22 22:21:41 Pacific Daylight Time
# Embedded file name: toontown.minigame.DistributedTagTreasureAI
from toontown.safezone import DistributedTreasureAI
from direct.distributed.ClockDelta import *

class DistributedTagTreasureAI(DistributedTreasureAI.DistributedTreasureAI):
    __module__ = __name__

    def __init__(self, air, treasurePlanner, x, y, z):
        DistributedTreasureAI.DistributedTreasureAI.__init__(self, air, treasurePlanner, x, y, z)
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\minigame\DistributedTagTreasureAI.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:21:41 Pacific Daylight Time
