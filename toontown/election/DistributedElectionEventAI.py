from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
from direct.fsm.FSM import FSM
from otp.ai.MagicWordGlobal import *
from toontown.election.DistributedHotAirBalloonAI import DistributedHotAirBalloonAI
from DistributedSafezoneInvasionAI import DistributedSafezoneInvasionAI
from DistributedInvasionSuitAI import DistributedInvasionSuitAI
from InvasionMasterAI import InvasionMasterAI
from toontown.toonbase import ToontownGlobals
import SafezoneInvasionGloabls

class DistributedElectionEventAI(DistributedObjectAI, FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedElectionEventAI")

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        FSM.__init__(self, 'ElectionFSM')
        self.air = air
        self.stateTime = globalClockDelta.getRealNetworkTime()
        self.pieTypeAmount = [4, 20, 1]

        # For the DistributedInvasionSuitAI
        self.master = InvasionMasterAI(self)
        self.toons = []
        self.suits = []

    def enterOff(self):
        self.requestDelete()
    
    def setPieTypeAmount(self, type, num):
        # This is more for the invasion than the pre-invasion elections.
        self.pieTypeAmount = [type, num]
    
    def wheelbarrowAvatarEnter(self):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId, None)
        if not av:
            self.air.writeServerEvent('suspicious', avId, 'Got a request for pies from a toon that isn\'t on the district!')
            return
        av.b_setPieType(self.pieTypeAmount[0])
        av.b_setNumPies(self.pieTypeAmount[1])
        av.b_setPieThrowType(self.pieTypeAmount[2])

    def enterIdle(self):
        pass

    def enterEvent(self):
        event = simbase.air.doFind('ElectionEvent')
        if event is None:
            event = DistributedElectionEventAI(simbase.air)
            event.generateWithRequired(2000)
        self.eventSequence = Sequence(
            Wait(140),
            Func(event.b_setState, 'Invasion'),
        )
        self.eventSequence.start()

    def enterBegin(self):
        pass

    def enterAlecSpeech(self):
        pass

    def enterCogLanding(self):
        pass

    def enterInvasion(self):
        invasion = simbase.air.doFind('SafezoneInvasion')
        if invasion is None:
            invasion = DistributedSafezoneInvasionAI(simbase.air)
            invasion.generateWithRequired(2000)

    def enterFlippyRunning(self):
        pass

    def enterFlippyWaving(self):
        pass

    def setState(self, state):
        self.demand(state)

    def d_setState(self, state):
        self.stateTime = globalClockDelta.getRealNetworkTime()
        self.sendUpdate('setState', [state, self.stateTime])

    def b_setState(self, state):
        self.setState(state)
        self.d_setState(state)

    def getState(self):
        return (self.state, self.stateTime)

    def requestSuit(self):
        # TODO: Set a spawn point on the stage
        # Figure out why it doesnt spawn at the custom point
        suit = DistributedInvasionSuitAI(self.air, self)
        suit.dna.newSuit(SafezoneInvasionGloabls.FirstSuitType)
        suit.setSpawnPoint(99)
        suit.setLevel(0)
        suit.generateWithRequired(ToontownGlobals.ToontownCentral)
        suit.b_setState('FlyDown')

@magicWord()
def election(state):
    event = simbase.air.doFind('ElectionEvent')
    if event is None:
        event = DistributedElectionEventAI(simbase.air)
        event.generateWithRequired(2000)

    if not hasattr(event, 'enter'+state):
        return 'Invalid state'

    event.b_setState(state)

    return 'Election event now in %r state' % state
