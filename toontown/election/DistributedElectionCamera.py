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
        DistributedNode.generate(self)
        self.camera = loader.loadModel('phase_4/models/events/camera.egg')
        self.camera.reparentTo(render)
        self.camera.setScale(0.25)
        propJoint = self.camera.find('**/hat')
        self.camBody = self.camera.find('**/camera_body')
        prop = BattleProps.globalPropPool.getProp('propeller')
        prop.reparentTo(propJoint)
        prop.setZ(1)
        prop.loop('propeller', fromFrame=0, toFrame=8)
        self.idleInterval = None
        
    def delete(self):
        self.camera.removeNode()
        DistributedNode.delete(self)

                
    def setState(self, state, ts, x, y, z, h, p, target):
        if self.idleInterval and self.idleInterval.isPlaying():
            self.idleInterval.pause()
        self.camera.setPos(self.getX(), self.getY(), self.getZ())
        if state == 'Move':
            self.wrtReparentTo(render)
            self.camera.wrtReparentTo(render)
            testNode = render.attachNewNode('test')
            testNode.setPosHpr(x, y, z, h, p, 0)
            cH, cP, cR = testNode.getHpr(self.camera)
            cH += + 180
            testNode.removeNode()
        elif state == 'Follow' and target in base.cr.doId2do:
            object = base.cr.doId2do[target]
            self.wrtReparentTo(object)
            self.camera.wrtReparentTo(object)
            testNode = object.attachNewNode('test')
            testNode.setPos(x, y, z)
            testNode.lookAt(object)
            h, p, r = testNode.getHpr()
            cH, cP, cR = testNode.getHpr(self.camera)
            p += 10
            cP = cP + 190
            testNode.removeNode()
        else:
            return
        dist = math.sqrt( (self.getX() - x)**2 + (self.getY() - y)**2 + (self.getZ() - z)**2)
        time = dist/10.0
        self.idleInterval = Parallel(
            Sequence(
                self.posInterval(2.5, (x, y, z + 0.5), startPos=(x, y, z), blendType='easeInOut'),
                self.posInterval(2.5, (x, y, z), blendType='easeInOut'),
            ),
            Sequence(
                self.camera.posInterval(2.5, (x, y, z + 0.5), startPos=(x, y, z), blendType='easeInOut'),
                self.camera.posInterval(2.5, (x, y, z), blendType='easeInOut'),
            )
        )


        elapsed = globalClockDelta.localElapsedTime(ts)
        movement = Sequence(Parallel(self.camera.posInterval(time, Point3(x, y, z)), self.camBody.hprInterval(time, Vec3(cH, cP, 0)), self.posHprInterval(time, Point3(x, y, z), Vec3(h, p, 0))),
            Func(self.idleInterval.loop))
        movement.start()
        movement.setT(elapsed)
