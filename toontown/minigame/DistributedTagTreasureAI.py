from toontown.safezone import DistributedTreasureAI
from direct.distributed.ClockDelta import *

class DistributedTagTreasureAI(DistributedTreasureAI.DistributedTreasureAI):
    __module__ = __name__

    def __init__(self, air, treasurePlanner, x, y, z):
        DistributedTreasureAI.DistributedTreasureAI.__init__(self, air, treasurePlanner, x, y, z)
