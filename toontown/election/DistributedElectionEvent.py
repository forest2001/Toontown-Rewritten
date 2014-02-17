from pandac.PandaModules import *
from otp.nametag.NametagConstants import *
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
from direct.distributed.DistributedObject import DistributedObject
from direct.fsm.FSM import FSM
from toontown.toon import NPCToons
from toontown.suit import Suit
from toontown.suit import SuitDNA

class DistributedElectionEvent(DistributedObject, FSM):
    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        FSM.__init__(self, 'ElectionFSM')

        self.showFloor = NodePath('ShowFloor') #This currently isn't part of the main geometry, so it isn't dimmed with the sky. Will fix later.
        self.showFloor.setPos(80, 0, 4)

        #Stage
        stage = loader.loadModel('phase_4/models/events/election_stage')
        stage.reparentTo(self.showFloor)
        stage.setHpr(270, 0, 0)
        stage.setScale(2.0, 1.8, 1.5)
        podium = loader.loadModel('phase_4/models/events/election_stagePodium')
        podium.reparentTo(self.showFloor)
        podium.setPosHpr(-6, 0, 3.185, 270, -2, 5)
        podium.setScale(0.7)
        counterLeft = loader.loadModel('phase_4/models/events/election_counterLeft')
        counterLeft.reparentTo(self.showFloor)
        counterLeft.setPosHpr(13.5, 10, 2.95, 270, 0, 0)
        counterLeft.setScale(2.0)
        counterRight = loader.loadModel('phase_4/models/events/election_counterRight')
        counterRight.reparentTo(self.showFloor)
        counterRight.setPosHpr(13.5, -10, 3.25, 270, 0, 0)
        counterRight.setScale(2.0)
        rope = loader.loadModel('phase_4/models/events/election_rope')
        rope.reparentTo(self.showFloor)
        rope.setPosHpr(-34, 18, 0.46, 270, 0, 0)
        rope.setScale(2, 2, 2)
        rope.show()

        #Campaign stands
        flippyStand = loader.loadModel('phase_4/models/events/election_flippyStand-static')
        flippyStand.reparentTo(self.showFloor)
        flippyStand.setPosHprScale(-43.6, -24.5, 0.01, 200, 0, 0, 0.55, 0.55, 0.55)
        flippyTable = flippyStand.find('**/Cube')
        wheelbarrow = flippyStand.find('**/Box')
        wheelbarrow.setPosHprScale(-3.61, -1.4, 0, 319, 0, 270, 3, 2, 1.8)
        
        slappyStand = loader.loadModel('phase_4/models/events/election_slappyStand-static')
        slappyStand.reparentTo(self.showFloor)
        slappyStand.setPosHprScale(-62.45, 14.39, 0.01, 325, 0, 0, 0.55, 0.55, 0.55)

        #Let's give FlippyStand a bunch of pies.
        pie = loader.loadModel('phase_3.5/models/props/tart')
        pie.reparentTo(flippyStand)
        pie.setScale(2.2, 2.2, 1.6)
        pieS = pie.copyTo(flippyStand)
        pie1 = pie.copyTo(wheelbarrow)
        pie2 = pie.copyTo(wheelbarrow)
        pie3 = pie.copyTo(wheelbarrow)
        pie4 = pie.copyTo(wheelbarrow)
        pie5 = pie.copyTo(wheelbarrow)
        pie6 = pie.copyTo(wheelbarrow)
        pie7 = pie.copyTo(wheelbarrow)
        pie8 = pie.copyTo(wheelbarrow)
        pie9 = pie.copyTo(wheelbarrow)
        pie10 = pie.copyTo(wheelbarrow)
        pie.setPosHprScale(-2.8, -2.4, 6.1, 0, 355.24, 351.87, 2, 2.1, 1.6)
        pieS.setPosHprScale(3.54, -3.94, 0.42, 45.00, 42.27, 0, 1.6, 1.6, 1.6)
        pie1.setPosHprScale(1.16, 11.24, 7.00, 246.80, 351.25, 0.00, 1.60, 1.40, 1.8)
        pie2.setPosHprScale(2.27, 8.02, 6.35, 104.04, 311.99, 9.46, 1.35, 1.35, 1)
        pie3.setPosHprScale(-1.23, 7.33, 6.88, 276.34, 28.61, 350.54, 1.41, 1.41, 1.6)
        pie4.setPosHprScale(0.27, 8.24, 6.42, 198.15, 351.87, 355.24, 1.93, 2, 2)
        pie5.setPosHprScale(0.06, 5.23, 6.78, 63.43, 355.91, 15.26, 1.3, 1.6, 1.8)
        pie6.setPosHprScale(-0.81, 11.37, 6.82, 326.31, 5.19, 19.98, 1.76, 1.86, 1.5)
        pie7.setPosHprScale(1.35, 10.09, 5.92, 35.54, 353.66, 343.30, 1.50, 1.90, 1.8)
        pie8.setPosHprScale(1.9, 5.59, 6.5, 75.96, 326.31, 8, 1.76, 1.56, 1.5)
        pie9.setPosHprScale(-1.74, 5.42, 6.28, 327.53, 318.81, 4.76, 1.8, 2, 2)
        pie10.setPosHprScale(-1.55, 9.22, 5.72, 266.53, 341.57, 0.00, 2.09, 1.68, 1.81)

        #self.flippy = NPCToons.createLocalNPC(2001)
        #self.alec = NPCToons.createLocalNPC(2022)        
        #self.slappy = NPCToons.createLocalNPC(2021)
        #self.flippy.reparentTo(self.showFloor)
        #self.slappy.reparentTo(self.showFloor)
        #self.alec.reparentTo(self.showFloor)

        #self.suit = Suit.Suit()
        #cogDNA = SuitDNA.SuitDNA()
        #cogDNA.newSuit('ym')
        #self.suit.setDNA(cogDNA)
        #self.suit.reparentTo(self.showFloor)

    def delete(self):
        self.demand('Off', 0.)

        # Clean up everything...
        self.showFloor.removeNode()

        DistributedObject.delete(self)

    def setState(self, state, timestamp):
        if state != 'Intro':
            return
        self.request(state, globalClockDelta.localElapsedTime(timestamp))

    def enterOff(self, offset):
        self.showFloor.reparentTo(hidden)

    def exitOff(self):
        self.showFloor.reparentTo(render)

    def enterIntro(self, offset):
        pass # In the future, set NPC animations.

    def enterFlippyRunning(self, offset):
        # First, put Flippy at a start position:
        self.flippy.setPos(0, -10, 0)
        self.flippy.setHpr(0, 0, 0)           

        self.interval = Sequence(
            # Flippy runs toward the bank:
            Func(self.flippy.loop, 'run'),
            self.flippy.posInterval(2.5, (0, 10, 0)),

            # He stops, admires it:
            Func(self.flippy.loop, 'neutral'),
            Wait(2.5),
            Func(self.flippy.setChatAbsolute, 'My, what a lovely bank!', CFSpeech|CFTimeout),
            Wait(5),

            # Now he turns around:
            Func(self.flippy.loop, 'walk'),
            self.flippy.hprInterval(2.5, (180, 0, 0)),

            # Now he runs toward the library:
            Func(self.flippy.loop, 'run'),
            self.flippy.posInterval(2.5, (0, -10, 0)),

            # He stops, admires it:
            Func(self.flippy.loop, 'neutral'),
            Wait(2.5),
            Func(self.flippy.setChatAbsolute, 'The library is kind of ugly though. :(', CFSpeech|CFTimeout),
            Wait(5),

            # Now he turns back to prepare to head to the bank:
            Func(self.flippy.loop, 'walk'),
            self.flippy.hprInterval(2.5, (0, 0, 0)),
        )

        self.interval.loop()

        # This fast-fowards the interval to the proper time-offset, so that
        # people entering the area while the state is running can catch up.
        self.interval.setT(offset)

    def exitFlippyRunning(self):
        # Return back to a "neutral state"
        self.interval.finish()
        self.flippy.loop('neutral')
        self.flippy.setChatAbsolute('', 0)
        self.flippy.setPos(0, 0, 0)
        self.flippy.setHpr(0, 0, 0)

    def enterFlippyWaving(self, offset):
        self.flippy.loop('wave')
        self.flippy.setPos(0, -10, 0)
        self.flippy.setHpr(90, 0, 0)
        self.slappy.loop('bow')
        self.slappy.setPos(0, 10, 0)
        self.slappy.setHpr(90, 0, 0)
        self.alec.setPos(-5, 0, 0)
        self.alec.setHpr(90, 0, 0)
        self.suit.loop('neutral')
        self.suit.setPos(5, 0, 0)
        self.suit.setHpr(90, 0, 0)

    def exitFlippyWaving(self):
        self.flippy.loop('neutral')
        self.flippy.setPos(0, -10, 0)
        self.flippy.setHpr(90, 0, 0)
        self.slappy.loop('neutral')
        self.flippy.setPos(0, 10, 0)
        self.flippy.setHpr(90, 0, 0)
        self.alec.setPos(-5, 0, 0)
        self.alec.setHpr(90, 0, 0)         
