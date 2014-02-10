from pandac.PandaModules import *
from direct.distributed.ClockDelta import *
from direct.fsm.FSM import FSM
from toontown.suit.DistributedSuitBase import DistributedSuitBase

class DistributedInvasionSuit(DistributedSuitBase, FSM):
    def __init__(self, cr):
        DistributedSuitBase.__init__(self, cr)
        FSM.__init__(self, 'InvasionSuitFSM')

    def setState(self, state, timestamp):
        self.request(state, globalClockDelta.localElapsedTime(timestamp))

    def enterFlyDown(self, time):
        self.loop('neutral', 0)
        self.mtrack = self.beginSupaFlyMove(Point3(0, 0, 0), 1, 'fromSky')
        self.mtrack.start(time)

    def exitFlyDown(self):
        self.mtrack.finish()
        del self.mtrack
        self.detachPropeller()

    def enterIdle(self, time):
        self.loop('neutral', 0)

    def enterMarch(self, time):
        self.loop('walk', 0)
