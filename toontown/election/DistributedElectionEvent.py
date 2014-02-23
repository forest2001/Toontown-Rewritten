from pandac.PandaModules import *
from otp.nametag.NametagConstants import *
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
from direct.distributed.DistributedObject import DistributedObject
from direct.fsm.FSM import FSM
from toontown.toon import NPCToons
from toontown.suit import Suit, SuitDNA
from direct.task import Task
from toontown.toonbase import ToontownGlobals

# TODO: ElectionGlobals (especially since it's scripted!)
FLIPPY_WHEELBARROW_PIES = [
    # Format: posHprScale
    [1.16, 11.24, 7.00, 246.80, 351.25, 0.00, 1.60, 1.40, 1.8],
    [2.27, 8.02, 6.35, 104.04, 311.99, 9.46, 1.35, 1.35, 1],
    [-1.23, 7.33, 6.88, 276.34, 28.61, 350.54, 1.41, 1.41, 1.6],
    [0.27, 8.24, 6.42, 198.15, 351.87, 355.24, 1.93, 2, 2],
    [0.06, 5.23, 6.78, 63.43, 355.91, 15.26, 1.3, 1.6, 1.8],
    [-0.81, 11.37, 6.82, 326.31, 5.19, 19.98, 1.76, 1.86, 1.5],
    [1.35, 10.09, 5.92, 35.54, 353.66, 343.30, 1.50, 1.90, 1.8],
    [1.9, 5.59, 6.5, 75.96, 326.31, 8, 1.76, 1.56, 1.5],
    [-1.74, 5.42, 6.28, 327.53, 318.81, 4.76, 1.8, 2, 2],
    [-1.55, 9.22, 5.72, 266.53, 341.57, 0.00, 2.09, 1.68, 1.81],
]
SLAPPY_BALLOON_SCALE = 2.5

class HotAirBalloonFSM(FSM):
    def __init__(self, election): # maybe a callback?
        FSM.__init__(self, 'HotAirBalloonFSM')
        self.election = election
        self.balloon = None
        self.currentToon = 0
        
    def start(self):
        self.balloon = loader.loadModel('phase_4/models/events/airballoon.egg')
        self.balloon.reparentTo(self.election.showFloor)
        self.balloon.setPosHprScale(-95, 33, -3.1, 0, 0, 0, SLAPPY_BALLOON_SCALE, SLAPPY_BALLOON_SCALE, SLAPPY_BALLOON_SCALE)
        self.collisionNP = self.balloon.find('**/BasketOutsideCollision')
        self.collisionNP.show()
        self.slappy = NPCToons.createLocalNPC(2021)
        self.slappy.reparentTo(self.balloon)
        self.slappy.setScale(0.4)
        self.slappy.loop('wave')
        base.cr.parentMgr.registerParent(ToontownGlobals.SPSlappysBalloon, self.balloon)
        
    def enterWaiting(self, offset):
        # Waiting for a toon to enter...
        self.balloonIdle = Sequence(
            Wait(0.3),
            self.balloon.posInterval(3, (-95, 33, -2.7)),
            Wait(0.3),
            self.balloon.posInterval(3, (-95, 33, -3.1)),
        )
        self.balloonIdle.loop()
        self.balloonIdle.setT(offset) # Might as well make use of the offset...
        self.accept('enter' + self.collisionNP.node().getName(), self.__handleToonEnter)
        
    def __handleToonEnter(self, collEntry):
        if self.currentToon != 0:
            print "error: toon currently assigned..."
            return # Weird... we already have a toon?
        if self.state != 'Waiting':
            print "error: not waiting"
            return # We're not waiting for a toon...
        print "i hit the collision!"
        self.election.sendUpdate('balloonAvatarEnter', [])
        
    def exitWaiting(self):
        self.balloonIdle.finish()
        self.ignore('enter' + self.collisionNP.node().getName())
        
    def enterStartBalloon(self, avId, offset):
        self.currentToon = avId
        # Up we go!
        if self.currentToon == base.localAvatar.doId:
            # TODO: Fix the glitchy jittering that the toon likes to do...
            base.localAvatar.b_setParent(ToontownGlobals.SPSlappysBalloon)
            base.localAvatar.setPos(0, 0, 0.5)
        self.balloonSequence = Sequence(
            Func(self.slappy.setChatAbsolute, 'Off we go!', CFSpeech|CFTimeout),
            Wait(0.5),
            self.balloon.posInterval(5.0, Point3(-95, 33, 50)),
            Wait(0.5),
            self.balloon.posInterval(5.0, Point3(-205, 33, 50)),
            Wait(0.5),
            self.balloon.posInterval(5.0, Point3(-95, 33, 50)),
            Wait(0.5),
            self.balloon.posInterval(5.0, Point3(-95, 33, -3.1)),
        )
        self.balloonSequence.start()
        self.balloonSequence.setT(offset)
        
    def exitStartBalloon(self):
        self.balloonSequence.finish()
        
    def enterFinished(self, offset):
        if self.currentToon == base.localAvatar.doId:
            base.localAvatar.b_setParent(ToontownGlobals.SPRender)
            base.localAvatar.setPos(-17.178, 6, 43.3134)
        self.currentToon = 0
        self.demand('Waiting', 0.0)

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
        rope.find('**/collide').setPosHprScale(0.31, 1.10, 0.00, 0.00, 0.00, 0.00, 0.89, 1.00, 1.25)

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
        # Pies on/around the stand.
        pie = loader.loadModel('phase_3.5/models/props/tart')
        pie.reparentTo(flippyStand)
        pieS = pie.copyTo(flippyStand)
        pie.setPosHprScale(-2.8, -2.4, 6.1, 0, 355.24, 351.87, 2, 2.1, 1.6)
        pieS.setPosHprScale(3.54, -3.94, 0.42, 45.00, 42.27, 0, 1.6, 1.6, 1.6)
        # Pies in the wheelbarrow.
        for pieSettings in FLIPPY_WHEELBARROW_PIES:
            pieModel = pie.copyTo(wheelbarrow)
            pieModel.setPosHprScale(*pieSettings)
        self.restockSfx = loader.loadSfx('phase_9/audio/sfx/CHQ_SOS_pies_restock.ogg')
            
        #Find FlippyStand's collision to give people pies.
        #Roger didn't separate the main stand from the wheelbarrow, so currently running to both gives pies.
        #That should probably be fixed before Doomsday, but it's fine for now.
        self.pieCollision = flippyStand.find('**/FlippyCollision')
        self.pieCollision.setScale(7.83, 4.36, 9.41)
        self.accept('enter' + self.pieCollision.node().getName(), self.handleWheelbarrowCollisionSphereEnter)
        
        # Hot Air Balloon!!! woo!
        self.balloon = HotAirBalloonFSM(self)
        self.balloon.start()

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

    def handleWheelbarrowCollisionSphereEnter(self, collEntry):
        if base.localAvatar.numPies >= 0 and base.localAvatar.numPies < 20:
            # We need to give them more pies! Send a request to the server.
            self.sendUpdate('wheelbarrowAvatarEnter', [])
            self.restockSfx.play()
    
    def delete(self):
        self.demand('Off', 0.)
        
        self.ignore('enter' + self.pieCollision.node().getName())
        
        # Clean up everything...
        self.showFloor.removeNode()

        DistributedObject.delete(self)
    
    def setBalloonState(self, state, timestamp):
        print "entering state %s" %state
        self.balloon.demand(state, globalClockDelta.localElapsedTime(timestamp))
        
    def setBalloonStart(self, toonId, timestamp):
        print "entering state StartBalloon"
        self.balloon.demand('StartBalloon', toonId, globalClockDelta.localElapsedTime(timestamp))
        
    def setBalloonCurrentToon(self, avId):
        self.balloon.currentToon = avId
    
    def setState(self, state, timestamp):
        if state != 'Intro':
            return
        self.request(state, globalClockDelta.localElapsedTime(timestamp))

    def enterOff(self, offset):
        base.cr.parentMgr.unregisterParent(ToontownGlobals.SPSlappysBalloon)
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
