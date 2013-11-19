from pandac.PandaModules import *
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
from direct.distributed.DistributedObject import DistributedObject
from direct.fsm.FSM import FSM

class DistributedDoomsdayEvent(DistributedObject, FSM):
    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        FSM.__init__(self, 'DoomsdayFSM')

        self.stage = NodePath('stage')
        self.stage.setPos(64, 0, 4)

        rope = loader.loadModel('phase_4/models/modules/tt_m_ara_int_ropes')
        rope.reparentTo(self.stage)

    def delete(self):
        self.demand('Off')

        # Clean up everything...
        self.stage.removeNode()

        DistributedObject.delete(self)

    def setState(self, state, timestamp):
        self.request(state, [globalClockDelta.localElapsedTime(timestamp)])

    def enterOff(self, offset):
        self.stage.reparentTo(hidden)

    def exitOff(self):
        self.stage.reparentTo(render)

    def enterIntro(self, offset):
        pass # In the future, set NPC animations.
