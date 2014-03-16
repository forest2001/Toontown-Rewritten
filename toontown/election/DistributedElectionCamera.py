from direct.distributed.DistributedSmoothNode import DistributedSmoothNode
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *
import math

class DistributedElectionCamera(DistributedSmoothNode):

    def __init__(self, cr):
        DistributedSmoothNode.__init__(self, cr)
        NodePath.__init__(self)
        
    def generate(self):
        self.assign(render.attachNewNode('DistributedElectionCamera'))
        DistributedSmoothNode.generate(self)
        self.startSmooth()