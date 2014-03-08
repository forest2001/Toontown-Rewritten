from direct.distributed.DistributedNode import DistributedNode
from pandac.PandaModules import *

class DistributedElectionCamera(DistributedNode):

    def __init__(self, cr):
        DistributedNode.__init__(self, cr)
        NodePath.__init__(self)
        
    def generate(self):
        self.assign(render.attachNewNode('DistributedElectionCamera'))
        DistributedNode.generate(self)