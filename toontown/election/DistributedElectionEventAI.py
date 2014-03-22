from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
from direct.fsm.FSM import FSM
from otp.ai.MagicWordGlobal import *
from toontown.election.DistributedHotAirBalloonAI import DistributedHotAirBalloonAI
from DistributedElectionCameraManagerAI import DistributedElectionCameraManagerAI
from DistributedSafezoneInvasionAI import DistributedSafezoneInvasionAI
from DistributedInvasionSuitAI import DistributedInvasionSuitAI
from InvasionMasterAI import InvasionMasterAI
from toontown.toonbase import ToontownGlobals
import SafezoneInvasionGlobals

class DistributedElectionEventAI(DistributedObjectAI, FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedElectionEventAI")

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        FSM.__init__(self, 'ElectionFSM')
        self.air = air
        self.stateTime = globalClockDelta.getRealNetworkTime()
        self.pieTypeAmount = [4, 20, 1]
        self.balloon = None
        
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
        if av.hp > 0:
            av.b_setPieType(self.pieTypeAmount[0])
            av.b_setNumPies(self.pieTypeAmount[1])
            av.b_setPieThrowType(self.pieTypeAmount[2])
        self.sendUpdate('flippySpeech', [avId, 1]) # 1 = Pie Request

    def phraseSaidToFlippy(self, phraseId):
        # Someone said something (relavent) to Flippy!
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId, None)
        if not av:
            self.air.writeServerEvent('suspicious', avId, 'Someone tried to talk to Flippy while they aren\'t on the district!')
            return
        self.sendUpdate('flippySpeech', [avId, phraseId])

    def enterIdle(self):
        # Spawn some cameras
        if not hasattr(simbase.air, 'cameraManager'):
            camMgr = DistributedElectionCameraManagerAI(simbase.air)
            camMgr.spawnManager()
        # Generate Slappy's Hot Air Balloon!
        if self.balloon is None:
            # Pump some self.air into Slappy's Balloon
            self.balloon = DistributedHotAirBalloonAI(self.air)
            self.balloon.generateWithRequired(self.zoneId)
        self.balloon.b_setState('ElectionIdle')

    def enterEvent(self):
        event = simbase.air.doFind('ElectionEvent')
        if event is None:
            event = DistributedElectionEventAI(simbase.air)
            event.generateWithRequired(2000)
        if self.balloon is None:
            # Pump some self.air into Slappy's Balloon
            self.balloon = DistributedHotAirBalloonAI(self.air)
            self.balloon.generateWithRequired(self.zoneId)
        self.eventSequence = Sequence(
            Func(event.b_setState, 'PreShow'),
            Wait(30),
            Func(event.b_setState, 'Begin'),
            Wait(10),
            #Func(event.b_setState, 'AlecSpeech'),
            #Wait(140),
            Func(event.b_setState, 'VoteBuildup'),
            Wait(12),
            Func(event.b_setState, 'WinnerAnnounce'),
            Wait(12),
            Func(event.b_setState, 'CogLanding'),
            Wait(90),
            Func(event.b_setState, 'Invasion')
        )
        self.eventSequence.start()

    def enterPreShow(self):
        pass

    def enterBegin(self):
        pass

    def enterAlecSpeech(self):
        pass

    def enterCogLanding(self):
        self.landingSequence = Sequence(
            Wait(65),
            Func(self.balloon.b_setState, 'ElectionCrashing')
        )
        self.landingSequence.start()

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

    def setSuitDamage(self, hp):
        self.suit = DistributedInvasionSuitAI(self.air, self)
        self.suit.dna.newSuit('ym')
        self.suit.setSpawnPoint(99)
        self.suit.setLevel(0)
        self.suit.generateWithRequired(ToontownGlobals.ToontownCentral)
        self.suit.takeDamage(hp)

@magicWord()
def election(state):
    if not simbase.config.GetBool('want-doomsday', False):
        simbase.air.writeServerEvent('aboose', spellbook.getInvoker().doId, 'Attempted to change the election state while doomsday is disabled.')
        return 'ABOOSE! The election is currently disabled. Your request has been logged.'
        
    event = simbase.air.doFind('ElectionEvent')
    if event is None:
        event = DistributedElectionEventAI(simbase.air)
        event.generateWithRequired(2000)

    if not hasattr(event, 'enter'+state):
        return 'Invalid state'

    event.b_setState(state)

    return 'Election event now in %r state' % state
