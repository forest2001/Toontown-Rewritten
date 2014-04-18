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
import ElectionGlobals
import random

class DistributedElectionEventAI(DistributedObjectAI, FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedElectionEventAI")

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        FSM.__init__(self, 'ElectionFSM')
        self.air = air
        self.stateTime = globalClockDelta.getRealNetworkTime()
        self.pieTypeAmount = [4, 20, 1]
        self.balloon = None
        self.cogDead = False
        
        # For the DistributedInvasionSuitAI
        self.master = InvasionMasterAI(self)
        self.toons = []
        self.suits = []

    def enterOff(self):
        self.requestDelete()


    '''
     PRE-ELECTION CAMPAIGNS
       These bits are for things used before Election Day, and mostly unrelated to the Election Sequence.
    '''
    def enterIdle(self):
        # Generate Slappy's Hot Air Balloon!
        if self.balloon is None:
            # Pump some self.air into Slappy's Balloon
            self.balloon = DistributedHotAirBalloonAI(self.air)
            self.balloon.generateWithRequired(self.zoneId)
        if simbase.config.GetBool('want-doomsday', False):
            # It's Election day!
            self.balloon.b_setState('ElectionIdle')
            # Better spawn some cameras
            if not hasattr(simbase.air, 'cameraManager'):
                camMgr = DistributedElectionCameraManagerAI(simbase.air)
                camMgr.spawnManager()
        else:
            self.balloon.b_setState('Waiting')
    
    def phraseSaidToFlippy(self, phraseId):
        # Someone said something (relavent) to Flippy!
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId, None)
        if not av:
            self.air.writeServerEvent('suspicious', avId, 'Someone tried to talk to Flippy while they aren\'t on the district!')
            return
        self.sendUpdate('flippySpeech', [avId, phraseId])

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

    def setPieTypeAmount(self, type, num):
        # This is more for the invasion than the pre-invasion elections.
        self.pieTypeAmount = [type, num]
        
    def slappyAvatarEnter(self):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId, None)
        if not av:
            self.air.writeServerEvent('suspicious', avId, 'Got a request for Slappy\'s Cheesy Effect from a toon that isn\'t on the district!')
            return
        av.b_setCheesyEffect(15, 0, 0)


    '''
     ELETION DAY SEQUENCE
       Next up we have the things that relate to the election sequence, which is controlled by both the AI and client.
       The AI has the global timer, which will fire off which state should be played and when. Sort of like checkpoints.
       The client has the sequences themselves, though, just in case anyone has any network lag when watching it.
       The client also shoots a message to the AI to ask how much time has elapsed since the sequence started so that late-joining clients can stay in sync with the sequence.
    '''
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
            Wait(34),
            Func(event.b_setState, 'Begin'),
            Wait(10),
            Func(event.b_setState, 'AlecSpeech'),
            Wait(155),
            Func(event.b_setState, 'VoteBuildup'),
            Wait(16),
            Func(event.b_setState, 'WinnerAnnounce'),
            Wait(12),
            Func(event.b_setState, 'CogLanding'),
            Wait(117),
            Func(event.b_setState, 'Invasion')
        )
        self.eventSequence.start()

    def enterPreShow(self):
        self.showAnnounceInterval = Sequence(
            Func(self.sendGlobalUpdate, 'TOON HQ: We just got word from Alec Tinn that the Toon Council Presidential Elections will be starting any second.'),
            Wait(5),
            Func(self.sendGlobalUpdate, 'TOON HQ: Please silence your Shtickerbooks and keep any Oinks, Squeaks, and Owooos to a minimum.')
        )
        self.showAnnounceInterval.start()

    def exitPreShow(self):
        self.showAnnounceInterval.finish()

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

    def exitCogLanding(self):
        self.landingSequence.finish()

    def enterInvasion(self):
        self.surleePhraseLoop = Sequence(
            Wait(30),
            Func(self.saySurleePhrase)
        )
        self.invasionSequence = Sequence(
            Wait(15),
            Func(self.spawnInvasion),
            Func(self.surleePhraseLoop.loop)                        
        )
        self.invasionSequence.start()

    def exitInvasion(self):
        self.invasionSequence.finish()

    def enterWrapUp(self):
        self.cogDead = False


    '''
     ELETION DAY MISC.
       Just a few other bits and pieces we need for Election Day, unrelated to the main sequence.
    '''
    def spawnInvasion(self):
        invasion = simbase.air.doFind('SafezoneInvasion')
        if invasion is None:
            invasion = DistributedSafezoneInvasionAI(simbase.air, self)
            invasion.generateWithRequired(2000)

    def setSuitDamage(self, hp):
        if not self.cogDead:
            self.cogDead = True
            if self.state == 'WrapUp':
                invasion = simbase.air.doFind('SafezoneInvasion')
                if invasion:
                    invasion.setFinaleSuitStunned(hp)
            else:
                self.suit = DistributedInvasionSuitAI(self.air, self)
                self.suit.dna.newSuit('ym')
                self.suit.setSpawnPoint(99)
                self.suit.setLevel(0)
                self.suit.generateWithRequired(ToontownGlobals.ToontownCentral)
                self.suit.takeDamage(hp)

    def saySurleePhrase(self, phrase = None, interrupt = 0, broadcast = False):
        if not phrase:
            phrase = random.choice(ElectionGlobals.SurleeTips)
        self.sendUpdate('saySurleePhrase', [phrase, interrupt, broadcast])

    def sendGlobalUpdate(self, text):
        # Send a whisper to everyone on the district from our local Toon HQ
        for doId in simbase.air.doId2do:
            if str(doId)[:2] == '10': # Are they a real player?
                do = simbase.air.doId2do.get(doId)
                do.d_setSystemMessage(0, text)

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
