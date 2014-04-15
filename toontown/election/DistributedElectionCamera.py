from direct.distributed.DistributedNode import DistributedNode
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
from toontown.battle import BattleProps
from pandac.PandaModules import *
import math

class DistributedElectionCamera(DistributedNode):

    def __init__(self, cr):
        DistributedNode.__init__(self, cr)
        NodePath.__init__(self)
        
    def generate(self):
        self.assign(render.attachNewNode('DistributedElectionCamera'))
        self.camAttach = self.attachNewNode('CameraAttach')
        DistributedNode.generate(self)
        camera = loader.loadModel('phase_4/models/events/camera.egg')
        camera.reparentTo(self)
        camera.setScale(0.25)
        propJoint = camera.find('**/hat')
        self.camBody = camera.find('**/camera_body')
        prop = BattleProps.globalPropPool.getProp('propeller')
        prop.reparentTo(propJoint)
        prop.setZ(1)
        prop.loop('propeller', fromFrame=0, toFrame=8)
        
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
        #self.setHpr(h, p, 0)
        idleInterval = Sequence(
            self.posInterval(2.5, (x, y, z + 0.5), startPos=(x, y, z), blendType='easeInOut'),
            self.posInterval(2.5, (x, y, z), blendType='easeInOut'),
        )
        movement = Sequence(
            Parallel(self.posInterval(time, Point3(x, y, z)), self.camBody.hprInterval(time, (h + 180, p, 0)), self.camAttach.hprInterval(time, (h, p, 0))),
            Func(idleInterval.loop)
        )
        movement.start()
        movement.setT(elapsed)
