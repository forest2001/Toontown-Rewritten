from pandac.PandaModules import *
from otp.nametag.NametagConstants import *
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
from direct.distributed.DistributedObject import DistributedObject
from direct.fsm.FSM import FSM
from direct.actor import Actor
from toontown.toon import NPCToons
from toontown.suit import Suit, SuitDNA
from direct.task import Task
from toontown.toonbase import ToontownGlobals
import ElectionGlobals
from direct.directnotify import DirectNotifyGlobal
from random import choice

# Interactive Flippy
from otp.speedchat import SpeedChatGlobals

class DistributedElectionEvent(DistributedObject, FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedElectionEvent")
    
    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        FSM.__init__(self, 'ElectionFSM')
        self.cr.election = self
        self.interactiveOn = False

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
        self.flippyStand = Actor.Actor('phase_4/models/events/election_flippyStand-mod', {'idle': 'phase_4/models/events/election_flippyStand-idle'})
        self.flippyStand.reparentTo(self.showFloor)
        self.flippyStand.setPosHprScale(-43.6, -24.5, 0.01, 200, 0, 0, 0.55, 0.55, 0.55)
        self.flippyStand.exposeJoint(None,"modelRoot", "LInnerShoulder")
        flippyTable = self.flippyStand.find('**/LInnerShoulder')
        self.flippyStand.exposeJoint(None,"modelRoot", "Box_Joint")
        wheelbarrowJoint = self.flippyStand.find('**/Box_Joint')
        wheelbarrow = self.flippyStand.find('**/Box')
        wheelbarrow.setPosHprScale(-2.36, 0.00, 1.83, 0.00, 0.00, 6.34, 1.14, 1.50, 0.93)
        
        slappyStand = loader.loadModel('phase_4/models/events/election_slappyStand-static')
        slappyStand.reparentTo(self.showFloor)
        slappyStand.setPosHprScale(-62.45, 14.39, 0.01, 325, 0, 0, 0.55, 0.55, 0.55)

        #Let's give FlippyStand a bunch of pies.
        # Pies on/around the stand.
        pie = loader.loadModel('phase_3.5/models/props/tart')
        #pie.reparentTo(flippyTable)
        pieS = pie.copyTo(flippyTable)
        #pie.setPosHprScale(-2.8, -2.4, 6.1, 0, 355.24, 351.87, 2, 2.1, 1.6)
        pieS.setPosHprScale(-2.61, -0.37, -1.99, 355.60, 90.00, 4.09, 1.6, 1.6, 1.6)
        # Pies in the wheelbarrow.
        for pieSettings in ElectionGlobals.FlippyWheelbarrowPies:
            pieModel = pie.copyTo(wheelbarrowJoint)
            pieModel.setPosHprScale(*pieSettings)
        # This currently causes placement problems with the animation
        wheelbarrowJoint.setPosHprScale(2.51, 0.0, 1.0, 270.0, 344.74, 0.0, 1.47, 1.12, 1.0)
        self.restockSfx = loader.loadSfx('phase_9/audio/sfx/CHQ_SOS_pies_restock.ogg')
            
        # Find FlippyStand's collision to give people pies.
        # The new animated model doesn't have any collisions, so this needs to be replaced with a collision box. Harv did it once, just need to look back in the commit history.
        cs = CollisionBox(Point3(7, 0, 0), 12, 5, 18)
        self.pieCollision = self.flippyStand.attachNewNode(CollisionNode('wheelbarrow_collision'))
        self.pieCollision.node().addSolid(cs)
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

    def startInteractiveFlippy(self):
        self.flippy.reparentTo(self.showFloor)
        self.flippy.setPosHpr(-40.6, -18.5, 0.01, 20, 0, 0)
        self.flippy.initializeBodyCollisions('toon')
        self.interactiveOn = True
        self.flippyPhrase = None
        self.accept(SpeedChatGlobals.SCStaticTextMsgEvent, self.phraseSaidToFlippy)
        self.flippyStand.loop('idle') # Comment this out to see the proper positioning for pies

    def stopInteractiveFlippy(self):
        self.ignore(SpeedChatGlobals.SCStaticTextMsgEvent)
        self.interactiveOn = False

    def phraseSaidToFlippy(self, phraseId):
        # Check distance...
        if self.flippy.nametag.getChat() != '':
            # Flippy is already responding to someone, ignore them.
            return
        if Vec3(base.localAvatar.getPos(self.flippy)).length() > 10:
            # Too far away.
            return
        # Check if the phrase is something that Flippy should respond to.
        for phraseIdList in ElectionGlobals.FlippyPhraseIds:
            if phraseId in phraseIdList:
                self.sendUpdate('phraseSaidToFlippy', [phraseId])
                break
    
    def flippySpeech(self, avId, phraseId):
        av = self.cr.doId2do.get(avId)
        if not av:
            # An avatar we don't know about interacted with Flippy... odd.
            self.notify.warning("Received unknown avId in flippySpeech from the AI.")
            return
        if not self.interactiveOn:
            self.notify.warning("Received flippySpeech from AI while Interactive Flippy is disabled on our client.")
            return
        if self.flippy.nametag.getChat() != '':
            # Flippy is alredy responding to someone, ignore.
            return
        if phraseId == 1: # Someone requested pies... Lets pray that we don't need phraseId 1...
            taskMgr.doMethodLater(ElectionGlobals.FlippyDelayResponse, self.flippy.setChatAbsolute, 'interactive-flippy-chat-task',
                                  extraArgs = [choice(ElectionGlobals.FlippyGibPies).replace("__NAME__", av.getName()), CFSpeech | CFTimeout])
            return
        if len(ElectionGlobals.FlippyPhraseIds) != len(ElectionGlobals.FlippyPhrases):
            # There is a mismatch in the number of phrases and the phraseIds we're looking out for...
            # If this ever occurs on the live client, then clearly this wasn't tested and someone needs a slap.
            raise Exception("There is a mismatch in the number of phraseIds and the number of phrases for Flippy Interactive!")
            return
        for index, phraseIdList in enumerate(ElectionGlobals.FlippyPhraseIds):
            for pid in phraseIdList:
                if pid == phraseId:
                    # This could potentially lead to a crash if there is a mismatch in the number (indexes) of
                    # phraseIdLists and phrases. Could possibly use a python dict ( { key : value } ) to
                    # prevent this...
                    taskMgr.doMethodLater(ElectionGlobals.FlippyDelayResponse, self.flippy.setChatAbsolute, 'interactive-flippy-chat-task',
                                          extraArgs = [ElectionGlobals.FlippyPhrases[index].replace("__NAME__", av.getName()), CFSpeech | CFTimeout])
                    return 

    def delete(self):
        self.demand('Off', 0.)
        
        # Clean up everything...
        self.showFloor.removeNode()
        self.stopInteractiveFlippy()
        self.ignore('enter' + self.pieCollision.node().getName())

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
