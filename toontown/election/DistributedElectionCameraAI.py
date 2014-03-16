from direct.distributed.DistributedSmoothNodeAI import DistributedSmoothNodeAI
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
from direct.task import Task
import math

class DistributedElectionCameraAI(DistributedSmoothNodeAI):

    def __init__(self, air):
        DistributedSmoothNodeAI.__init__(self, air)
        self.interval = None
        self.target = None
        
    def generate(self):
        DistributedSmoothNodeAI.generate(self)
        self.startPosHprBroadcast()
                        
    def _moveTo(self, x, y, z, h, p):
        taskMgr.remove('follow-%d' % self.doId)
        dist = self._dist(x, y, z)
        time = dist/10.0 #constant rate of 10 unit/s with some extra time just in case
        if self.interval and not self.interval.isStopped():
            self.interval.pause()
        self.interval = Sequence(self.hprInterval(1.0, Vec3(h,p,0)), self.posInterval(time, Point3(x, y, z)), Func(self.sendUpdate, 'setSmStop', [globalClockDelta.getRealNetworkTime()]), Func(self.b_setPosHpr, x,y,z,h,p,0))
        self.interval.start()
        
    def _watch(self, object):
        pass
        
    def _followBehind(self, object):
        taskMgr.remove('follow-%d' % self.doId)
        taskMgr.doMethodLater(0.1, self.followBehindTask, 'follow-%d' % self.doId, extraArgs=[object], appendTask=True)
        
    def followBehindTask(self, object, task):
        x,y,z = object.getPos()
        y = y - 10
        z = z + 7
        h,p,r = object.getHpr()
        dist = self._dist(x,y,z)
        if dist > 1:
            dir = Vec3(x - self.getX(), y - self.getY(), z - self.getZ())
            dir.normalize()
            self.setPosHpr(self.getX() + dir.getX(), self.getY() + dir.getY(), self.getZ() + dir.getZ(), h, 345, 0)
        return task.again
        
    def _dist(self, x, y, z):
        return math.sqrt( (self.getX() - x)**2 + (self.getY() - y)**2 + (self.getZ() - z)**2)