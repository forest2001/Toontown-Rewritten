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
import ElectionGlobals

class DistributedElectionEvent(DistributedObject, FSM):
    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        FSM.__init__(self, 'ElectionFSM')
        self.cr.election = self
        self.interactiveOn = None

        self.showFloor = NodePath('ShowFloor')
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
        for pieSettings in ElectionGlobals.FlippyWheelbarrowPies:
            pieModel = pie.copyTo(wheelbarrow)
            pieModel.setPosHprScale(*pieSettings)
        self.restockSfx = loader.loadSfx('phase_9/audio/sfx/CHQ_SOS_pies_restock.ogg')
            
        #Find FlippyStand's collision to give people pies.
        #Roger didn't separate the main stand from the wheelbarrow, so currently running to both gives pies.
        #That should probably be fixed before Doomsday, but it's fine for now.
        self.pieCollision = flippyStand.find('**/FlippyCollision')
        self.pieCollision.setScale(7.83, 4.36, 9.41)
        self.accept('enter' + self.pieCollision.node().getName(), self.handleWheelbarrowCollisionSphereEnter)
       
        self.flippy = NPCToons.createLocalNPC(2001)
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
        self.startInteractiveFlippy()

    def handleWheelbarrowCollisionSphereEnter(self, collEntry):
        if base.localAvatar.numPies >= 0 and base.localAvatar.numPies < 20:
            # We need to give them more pies! Send a request to the server.
            self.sendUpdate('wheelbarrowAvatarEnter', [])
            self.restockSfx.play()
            print(self.flippy.nametag.getChat())
            if self.interactiveOn and self.flippy.nametag.getChat() == '':
                sayPieChatLater = Sequence(
                    Wait(0.5),
                    Func(self.flippy.setChatAbsolute, ElectionGlobals.FlippyGibPiesChoice, CFSpeech|CFTimeout)
                )
                sayPieChatLater.start()

    def startInteractiveFlippy(self):
        from otp.speedchat import SpeedChatGlobals
        self.flippy.reparentTo(self.showFloor)
        self.flippy.setPosHpr(-40.6, -18.5, 0.01, 20, 0, 0)
        self.flippy.initializeBodyCollisions('toon')
        self.interactiveOn = 1
        self.flippyPhrase = None
        def phraseSaid(phraseId):
            # Check distance...
            if Vec3(base.localAvatar.getPos(self.flippy)).length() > 10:
                return
            
            # This is really really bad but I have no idea how to do what I wanted to do
            # Originally I wanted to do:
            # if ElectionGlobals.[literal phraseId]:
            #     say ElectionGlobals.[literal phraseId] (which would be a string)
            # but I have no idea how to translate that to real python
            if phraseId in [100, 101, 102, 103, 104, 105]:
                # Hello
                self.flippyPhrase = 'Hey there! How are you doing?'
            elif phraseId in [107, 108]:
                # Hello?/Are you still there?
                self.flippyPhrase = 'I\'m here, present and accounted for!'
            elif phraseId in [200, 201, 202, 206, 207]:
                # Bye
                self.flippyPhrase = 'Alrighty, catcha later!'
            elif phraseId in [203, 204, 205]:
                # Have a nice day
                self.flippyPhrase = 'Thanks! To you as well.'
            elif phraseId in [208, 209]:
                # I need to go
                self.flippyPhrase = 'Leaving so soon?'
            elif phraseId == 301:
                # Owooo!
                self.flippyPhrase = 'Ha, that\'s a funny phrase. Owooo!'
            elif phraseId == 500:
                # Thanks!
                self.flippyPhrase = 'No problem.'
            elif phraseId in [505, 506, 507, 5602]:
                # That was fun!
                self.flippyPhrase = 'You betcha!'
            elif phraseId in [508, 511, 1001, 1003, 1005, 1006, 1126, 1127, 5603]:
                # Let's work together!
                self.flippyPhrase = 'I would if I could, but I should stay here in case new toons come along.'
            elif phraseId == 509:
                # Need some help?
                self.flippyPhrase = 'Thanks for the offer, but I think I have things under control.'
            elif phraseId == 510:
                # Want to be friends?
                self.flippyPhrase = 'Sorry, I\'m not allowed to make friends over the election period. :('
            elif phraseId in [600, 601, 602, 603]:
                # You are ______!
                self.flippyPhrase = 'Right back \'atcha!'
            elif phraseId in [700, 701, 702, 704, 705, 706, 707]:
                # I like your ____
                self.flippyPhrase = 'Aw, shucks. I like yours too!'
            elif phraseId == 703:
                # I like your skirt
                self.flippyPhrase = 'Not sure if I should consider that a compliement or...'
            elif phraseId in [800, 801, 802, 803, 804]:
                # Sorry
                self.flippyPhrase = 'No problem. It\'s all good.'
            elif phraseId == 807:
                # Sorry, what did you say?
                # He'll repeat what he said unless the phrase is none.
                if self.flippyPhrase == None:
                    self.flippyPhrase = 'Huh. I forget.'    
                else:
                    pass
            elif phraseId == 808:
                # Sorry, I can only use speedchat
                self.flippyPhrase = 'Good, because I can only respond to SpeedChat. Haha!'
            elif phraseId == 901:
                # You stink!
                self.flippyPhrase = 'It\'s probably the leftover ingredients from all of those pies. Pee-yew!'
            elif phraseId in [900, 902, 903, 904, 905]:
                # Please go away!
                self.flippyPhrase = 'I\'m sorry. Did I do something wrong? :('
            elif phraseId == 1200:
                # What Toontask are you working on?
                self.flippyPhrase = 'I haven\'t gotten any in a while. I guess you could say that the election is my ToonTask!'
            elif phraseId == 1500:
                # Got gags?
                self.flippyPhrase = 'All the cream pies we need!'
            elif phraseId == 1501:
                # I need more gags
                self.flippyPhrase = 'Oh? No problem, just grab some from the wheelbarrow.'
            elif phraseId == 1508:
                # Lets use throw
                self.flippyPhrase = 'Totally! Throw is my favorite kind of gag.'
            elif phraseId == 1415:
                # I need more laff
                self.flippyPhrase = 'Uh oh, that\'s no good. You should find an ice cream cone around here.'
            elif phraseId == 1520:
                # Catch!
                self.flippyPhrase = 'I\'m wide open, pass it here!'
            elif phraseId == 1526:
                # Piece of cake
                self.flippyPhrase = 'Sorry, only pies here.'
            elif phraseId in [1702, 1554, 1556, 1557]:
                # Cogs
                self.flippyPhrase = '...like, the gear? What have gears ever done to you? :('
            elif phraseId == 1558:
                # Save powerful gags
                self.flippyPhrase = 'Hmm, good idea. Pies are going so fast that we might have to switch to cupcakes by the time of the election.'
            elif phraseId == 5400:
                # Toontown Rewritten
                self.flippyPhrase = 'Toontown... Rewritten? I\'ve heard Surlee say that a few times, but I can never figure out what he means.'
            elif phraseId in [5401, 5407, 5408, 5409]:
                # Found any bugs
                self.flippyPhrase = 'Hmm, well I did spot a butterfly over there.'
            elif phraseId == 5402:
                # Crashed
                self.flippyPhrase = 'Oof, plenty of times at first. Karts are tricky to get used to.'
            elif phraseId == 5404:
                # Toonbook
                self.flippyPhrase = 'I do, actually! I don\'t use it often.'
            elif phraseId == 5405:
                # Livestreaming
                self.flippyPhrase = 'Hiya, viewers! Don\'t forget to Flip for Flippy!'
            elif phraseId == 5405:
                # Livestreaming
                self.flippyPhrase = 'Hiya, viewers! Don\'t forget to Flip for Flippy!'
            elif phraseId == 5500:
                # :)
                self.flippyPhrase = ':D'
            elif phraseId == 5501:
                # :(
                self.flippyPhrase = ':C'
            elif phraseId == 5502:
                # :D
                self.flippyPhrase = ':)'
            elif phraseId == 5503:
                # :C
                self.flippyPhrase = ':('
            elif phraseId == 5504:
                # :O
                self.flippyPhrase = ':P'
            elif phraseId == 5505:
                # :P
                self.flippyPhrase = ':O'
            elif phraseId == 5506:
                # >:)
                self.flippyPhrase = '>:C'
            elif phraseId == 5507:
                # >:C
                self.flippyPhrase = '>:)'
            elif phraseId in [5600, 5601]:
                # what's up?
                self.flippyPhrase = 'I\'m doing pretty great! And you?'
            elif phraseId == 10100:
                # Who are you voting for?
                self.flippyPhrase = 'I\'m not allowed to vote, silly!'
            elif phraseId in [10101, 10102]:
                # Flippy
                self.flippyPhrase = 'That\'s the spirit! :)'
            elif phraseId in [10103, 10104]:
                # Slappy
                self.flippyPhrase = 'Slappy is pretty fun, too. Great balloon. Though... See that plane stuck up there...?'
            elif phraseId == 10105:
                # Decorations
                self.flippyPhrase = 'Me too. Alec did a great job, and I hear there are more coming.'
            else:
                self.flippyPhrase = None

            if self.flippy.nametag.getChat() == '' and self.flippyPhrase != None:
                sayChatLater = Sequence(
                    Wait(1),
                    Func(self.flippy.setChatAbsolute, self.flippyPhrase, CFSpeech|CFTimeout)
                )
                sayChatLater.start()
        
        self.accept(SpeedChatGlobals.SCStaticTextMsgEvent, phraseSaid)
        

    def delete(self):
        self.demand('Off', 0.)
        
        self.ignore('enter' + self.pieCollision.node().getName())
        
        # Clean up everything...
        self.showFloor.removeNode()

        DistributedObject.delete(self)
    
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
