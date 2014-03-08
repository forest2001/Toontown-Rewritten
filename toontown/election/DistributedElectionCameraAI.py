from direct.distributed.DistributedNodeAI import DistributedNodeAI

class DistributedElectionCameraAI(DistributedNodeAI):

    def __init__(self, air):
        DistributedNodeAI.__init__(self, air)