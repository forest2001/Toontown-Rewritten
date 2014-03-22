from direct.distributed.DistributedNode import DistributedNode
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *
import math

class DistributedElectionCamera(DistributedNode):

    def __init__(self, cr):
        DistributedNode.__init__(self, cr)
        NodePath.__init__(self)
        
    def generate(self):
        self.assign(render.attachNewNode('DistributedElectionCamera'))
        DistributedNode.generate(self)
        
    def setState(self, state, ts, x, y, z, h, p, target):
        if state == 'Move':
            self.wrtReparentTo(render)
        elif state == 'Follow' and target in base.cr.doId2do:
            object = base.cr.doId2do[target]
            self.wrtReparentTo(object)
        else:
            return
        dist = math.sqrt( (self.getX() - x)**2 + (self.getY() - y)**2 + (self.getZ() - z)**2)
        time = dist/10.0
        elapsed = globalClockDelta.localElapsedTime(ts)
        self.setHpr(h, p, 0)
        movement = self.posInterval(time-elapsed, Point3(x, y, z))
        movement.start()
