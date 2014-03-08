from direct.distributed.DistributedNodeAI import DistributedNodeAI
from direct.distributed.ClockDelta import *
from direct.task import Task
import math

class DistributedElectionCameraAI(DistributedNodeAI):

    def __init__(self, air):
        DistributedNodeAI.__init__(self, air)
        
        
    def getState(self):
        return self.state
        
    def setState(self, state, ts, x, y, z, h, target):
        self.state = [state, ts, x, y, z, h, target]
        
    def d_setState(self, state, ts, x, y, z, h, target):
        self.sendUpdate('setState', [state, ts, x, y, z, h, target])
        
    def b_setState(self, state, ts, x, y, z, h, target):
        self.setState(state, ts, x, y, z, h, target)
        self.d_setState(state, ts, x, y, z, h, target)
        
    def _moveTo(self, x, y, z, h):
        dist = math.sqrt( (self.getX() - x)**2 + (self.getY() - y)**2 + (self.getZ() - z)**2)
        time = dist/10.0
        self.b_setState('Move', globalClockDelta.getRealNetworkTime(), x, y, z, h, 0)
        taskMgr.remove('finish%d' % self.doId)
        taskMgr.doMethodLater(time, self.__finishMove, 'finish%d' % self.doId, extraArgs=[x, y, z, h])
        
    def __finishMove(self, x, y, z, h):
        self.b_setPosHpr(x, y, z, 0, h, 0)