from DistributedNPCToonAI import *

class DistributedNPCFlippyInToonHallAI(DistributedNPCToonAI):
    __module__ = __name__

    def __init__(self, air, npcId, questCallback = None, hq = 0):
        DistributedNPCToonAI.__init__(self, air, npcId, questCallback)
