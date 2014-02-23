from pandac.PandaModules import *
from otp.nametag.NametagConstants import *
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
from direct.distributed.DistributedObject import DistributedObject
from direct.fsm.FSM import FSM
from toontown.toon import NPCToons
from toontown.suit import Suit
from toontown.suit import SuitDNA
import ElectionGlobals

class DistributedElectionEvent(DistributedObject, FSM):
    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        FSM.__init__(self, 'ElectionFSM')

        self.showFloor = NodePath('ShowFloor')
        self.showFloor.setPos(80, 0, 4)

        #Stage
        stage = loader.loadModel('phase_4/models/events/election_stage')
        stage.reparentTo(self.showFloor)
        stage.setHpr(270, 0, 0)
        stage.setScale(2.0, 1.8, 1.5)
        podium = loader.loadModel('phase_4/models/events/election_stagePodium')
        podium.reparentTo(self.showFloor)
        podium.setPosHpr(-6, 0, 3, 270, -2, 5)
        podium.setScale(0.65)
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
        #rope.find('**/collide').remove() #This is handy for positioning

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
        for pieSettings in ElectionGlobals.FLIPPY_WHEELBARROW_PIES:
            pieModel = pie.copyTo(wheelbarrow)
            pieModel.setPosHprScale(*pieSettings)
        self.restockSfx = loader.loadSfx('phase_9/audio/sfx/CHQ_SOS_pies_restock.ogg')

        #Find FlippyStand's collision to give people pies.
        #Roger didn't separate the main stand from the wheelbarrow, so currently running to both gives pies.
        #That should probably be fixed before Doomsday, but it's fine for now.
        self.pieCollision = flippyStand.find('**/FlippyCollision')
        self.pieCollision.setScale(7.83, 4.36, 9.41)
        self.accept('enter' + self.pieCollision.node().getName(), self.handleWheelbarrowCollisionSphereEnter)

        #Hi NPCs!
        self.alec = NPCToons.createLocalNPC(2022)
        self.slappy = NPCToons.createLocalNPC(2021)
        self.flippy = NPCToons.createLocalNPC(2001)
        #Sometimes they all need to do the same thing.
        self.characters = [self.alec, self.slappy, self.flippy]

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

    def setState(self, state, timestamp):
        self.request(state, globalClockDelta.localElapsedTime(timestamp))

    def enterOff(self, offset):
        self.showFloor.reparentTo(hidden)

    def exitOff(self):
        self.showFloor.reparentTo(render)



    def enterIdle(self, offset):
        pass

    def enterEvent(self, offset):
        self.eventInterval = Sequence(
            Func(base.cr.playGame.hood.loader.music.stop),
            Wait(3),
            Func(self.enterBegin, offset),
            Wait(10),
            Func(self.enterAlecSpeech, offset),
            Wait(130),
            #TODO: Func(self.enterVoteBuildup, offset),
            #TODO: Func(self.enterWinnerAnnounce, offset),
            #TODO: Func(self.enterCogLanding, offset),
            #TODO: Func(self.enterWinnerDeath, offset),
            Func(self.enterInvasion, offset),
        )
        self.eventInterval.start()
        self.eventInterval.setT(offset)

    def enterBegin(self, offset):
        #Oh boy, here come the candidates
        for character in self.characters:
            character.reparentTo(self.showFloor)
            character.setPosHpr(35, -0.3, 0, 90, 0, 0)
        musicIntro = base.loadMusic(ElectionGlobals.IntroMusic)

        self.alecHallInterval = Sequence(
            Parallel(Func(self.alec.loop, 'walk'), Func(base.playMusic, musicIntro, looping=0, volume=0.8)),
            self.alec.posInterval(3, (12.96, -0.38, 0)),
            self.alec.posInterval(2, (4.2, -0.25, 3.13)),
            self.alec.posInterval(2, (-4.5, -0.14, 3.13)),
            Func(self.alec.loop, 'neutral'),
        )
        self.slappyHallInterval = Sequence(
            Wait(1),
            Func(self.slappy.loop, 'walk'),
            self.slappy.posInterval(2.5, (12.96, -0.38, 0)),
            self.slappy.posHprInterval(2, (4.3, 2.72, 3.13), (70, 0, 0)),
            self.slappy.posHprInterval(1, (2.36, 5.18, 3.08), (40, 0, 0)),
            self.slappy.posHprInterval(1, (1, 9, 3.03), (90, 0, 0)),
            Func(self.slappy.loop, 'neutral'),
        )
        self.flippyHallInterval = Sequence(
            Wait(2),
            Func(self.flippy.loop, 'walk'),
            self.flippy.posInterval(3, (12.96, -0.38, 0)),
            self.flippy.posHprInterval(1, (3.3, -2.39, 3.13), (120, 0, 0)),
            self.flippy.posHprInterval(1, (2.49, -6.09, 3.17), (155, 0, 0)),
            self.flippy.posHprInterval(1, (2, -10, 3.23), (90, 0, 0)),
            Func(self.flippy.loop, 'neutral'),
        )
        self.alecHallInterval.start()
        self.alecHallInterval.setT(offset)
        self.slappyHallInterval.start()
        self.slappyHallInterval.setT(offset)
        self.flippyHallInterval.start()
        self.flippyHallInterval.setT(offset)

    def enterAlecSpeech(self, offset):
        #For some reason, the sound only plays on their first message. Can anyone look into that?
        self.alecSpeech = Sequence(
            Func(self.alec.setChatAbsolute, 'Hellooo Toontown~!', CFSpeech|CFTimeout),
            Wait(5),
            Func(self.alec.setChatAbsolute, 'As many of you know, I''m your Hilarious Host and Eccentric Elector: Alec Tinn!', CFSpeech|CFTimeout),
            Wait(8.5),
            Func(self.alec.setChatAbsolute, 'And of course, we can''t forget about our two toonerific toons who have been selected to fight for the Presidency...', CFSpeech|CFTimeout),
            Wait(9),
            Func(self.alec.setChatAbsolute, 'Slappy Quackintosh, and Flippy Doggenbottom!', CFSpeech|CFTimeout),
            Wait(6.5),
            Func(self.alec.setChatAbsolute, 'I must say, this turnout is absolutely, positivley, extra-tooneriffically, astounding!', CFSpeech|CFTimeout),
            Wait(6),
            Func(self.alec.setChatAbsolute, 'It''s truely an honor to be here on this day, and I''m sure I speak for all of us when I thank you for coming.', CFSpeech|CFTimeout),
            Wait(8),
            Func(self.alec.setChatAbsolute, 'Now, the votes are almost ready to be tallied! Flippy, Slappy, do either of you have anything to say before the moment of truth?', CFSpeech|CFTimeout),
            Wait(10),
            Func(self.slappy.setChatAbsolute, 'The only thing I have to say, no matter who wins...', CFSpeech|CFTimeout),
            Wait(6.5),
            Func(self.slappy.setChatAbsolute, 'I know that Toontown is going to grow to be even more... "Toontastic" than ever before.', CFSpeech|CFTimeout),
            Wait(8),
            Func(self.slappy.setChatAbsolute, 'All of you are truer-than-truely the best!', CFSpeech|CFTimeout),
            Wait(10),
            Func(self.flippy.setChatAbsolute, 'Like Slappy said, I can''t even begin to thank all of you Toontastic toons for this.', CFSpeech|CFTimeout),
            Wait(8),
            Func(self.flippy.setChatAbsolute, 'Even after all of this terrific time together, I''m still speechless that I''m here today.', CFSpeech|CFTimeout),
            Wait(8),
            Func(self.flippy.setChatAbsolute, 'Here''s to Toontown, Slappy, and all of you!', CFSpeech|CFTimeout),
            Wait(7),
            Func(self.alec.setChatAbsolute, 'Well said, the both of you!', CFSpeech|CFTimeout),
            Wait(5),
            Func(self.alec.setChatAbsolute, 'Ooh, I''m just jittering with excitement. Are you toons ready to hear the winners?', CFSpeech|CFTimeout),
            Wait(10),
            Func(self.alec.setChatAbsolute, 'Hmm, I''m not sure if you are. Let me ask again: Are you toons ready to hear the winners?!', CFSpeech|CFTimeout),
            Wait(8),
            Func(self.alec.setChatAbsolute, 'WOAH! Woah! No need to yell! I''m right here, I get it. You guys want to hear them.', CFSpeech|CFTimeout),
            Wait(8),
            Func(self.alec.setChatAbsolute, 'So, without further ado...', CFSpeech|CFTimeout),
            Wait(4),
            Func(self.alec.setChatAbsolute, 'I will now pull the GRAND ELECTORAL LEVER!', CFSpeech|CFTimeout),
        )
        self.alecSpeech.start()
        self.alecSpeech.setT(offset)

    def enterInvasion(self, offset):
        pass



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
