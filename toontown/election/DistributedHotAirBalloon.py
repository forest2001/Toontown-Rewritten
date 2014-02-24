from pandac.PandaModules import *
from otp.nametag.NametagConstants import *
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
from direct.distributed.DistributedObject import DistributedObject
from direct.fsm.FSM import FSM
from toontown.toon import NPCToons
from toontown.toonbase import ToontownGlobals
from direct.task import Task
from random import choice

# TODO: ElectionGlobals C:?
# ^ Already done in Doomsday Branch
BALLOON_BASE_POS = [-15, 33, 1.1]
BALLOON_SCALE = 2.5

class DistributedHotAirBalloon(DistributedObject, FSM):
    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        FSM.__init__(self, 'HotAirBalloonFSM')
        self.avId = 0
        
        # Create the balloon
        self.balloon = loader.loadModel('phase_4/models/events/airballoon.egg') # TODO: Use .bam model
        self.balloon.reparentTo(base.render)
        self.balloon.setPos(*BALLOON_BASE_POS)
        self.balloon.setScale(BALLOON_SCALE)
        # So we can reparent toons to the balloon so they don't fall out
        self.cr.parentMgr.registerParent(ToontownGlobals.SPSlappysBalloon, self.balloon)
        # Balloon collision NodePath (outside)
        self.collisionNP = self.balloon.find('**/Collision_Outer')
        # Slappy
        # TODO: Give Slappy a collision
        self.slappy = NPCToons.createLocalNPC(2021)
        self.slappy.reparentTo(self.balloon)
        self.slappy.setPos(0.7, 0.7, 0.4)
        self.slappy.setH(150)
        self.slappy.setScale((1/BALLOON_SCALE)) # We want a normal sized Slappy
        self.slappy.loop('neutral')
        
    def delete(self):
        # Clean up after our mess...
        # This is what happens when you don't clean up:
        # http://puu.sh/77zAm.jpg
        self.demand('Off')
        self.ignore('enter' + self.collisionNP.node().getName())
        self.cr.parentMgr.unregisterParent(ToontownGlobals.SPSlappysBalloon)
        self.balloon.removeNode()
        self.slappy.delete()
        DistributedObject.delete(self)
        
    def setState(self, state, timestamp, avId):
        if avId != self.avId:
            self.avId = avId
        self.demand(state, globalClockDelta.localElapsedTime(timestamp))
            
    def enterWaiting(self, offset):
        # Wait for a collision...
        self.accept('enter' + self.collisionNP.node().getName(), self.__handleToonEnter)
        # Mini animation for the balloon hovering near the floor
        self.balloonIdle = Sequence(
            Wait(0.3),
            self.balloon.posInterval(3, (-15, 33, 1.5)),
            Wait(0.3),
            self.balloon.posInterval(3, (-15, 33, 1.1)),
        )
        self.balloonIdle.loop()
        self.balloonIdle.setT(offset)
        
    def __handleToonEnter(self, collEntry):
        if self.avId != 0:
            # Someone is already occupying the balloon
            return
        if self.state != 'Waiting':
            # The balloon isn't waiting for a toon
            return
        self.sendUpdate('requestEnter', [])
        
    def exitWaiting(self):
        self.balloonIdle.finish()
        self.ignore('enter' + self.collisionNP.node().getName())
        
    def enterOccupied(self, offset):
        if self.avId == base.localAvatar.doId:
            # This is us! We need to reparent to the balloon and position ourselves accordingly.
            # TODO: Disable Jumping
            base.localAvatar.disableAvatarControls()
            self.hopOnAnim = Sequence(Parallel(Func(base.localAvatar.b_setParent, ToontownGlobals.SPSlappysBalloon), Func(base.localAvatar.b_setAnimState, 'jump', 1.0)), base.localAvatar.posInterval(0.6, (0, 0, 4)), base.localAvatar.posInterval(0.4, (0, 0, 0.7)), Func(base.localAvatar.enableAvatarControls))
            self.hopOnAnim.start()

        # Maybe we want a short speech before we take off?
        # DONE: Randomly select some Slappy speeches to say throughout the ride
        # Not sure what to add here. Just added a few for testing. 
        slappySpeaches = ['Keep your hands and feet in the basket at all times',
                          'Hold on tight! Here we Go!',
                          'Remember, don\'t be wacky and vote for slappy!',
                          'Ready to sore through the sky?']
        self.occupiedSequence = Sequence(
            Func(self.slappy.setChatAbsolute, choice(slappySpeaches), CFSpeech | CFTimeout),
            Wait(3.5),
        )
        self.occupiedSequence.start()
        self.occupiedSequence.setT(offset)
        
    def exitOccupied(self):
        self.occupiedSequence.finish()
        
    def enterStartRide(self, offset):
        # TODO: Choose a random route to fly on (or at least improve this one)
        self.rideSequence = Sequence(
            Func(self.slappy.setChatAbsolute, 'Off we go!', CFSpeech | CFTimeout),

            # Lift Off
            Wait(0.5),
            self.balloon.posInterval(5.0, Point3(-15, 33, 54)),
            # 5.5 Seconds

            # To the tunnel we go
            Wait(0.5),
            Func(self.slappy.setChatAbsolute, 'How about that view?', CFSpeech | CFTimeout),
            self.balloon.posInterval(5.0, Point3(-125, 33, 54)),
            # 11 Seconds

            # Lets drop a weight on the gag shop
            Wait(0.5),
            self.balloon.posInterval(4.0, Point3(-100, -60, 54)),
            Func(self.slappy.setChatAbsolute, 'Rats! The weight missed the gag shop!', CFSpeech | CFTimeout),        
            # 16.5 Seconds

            # Rats, we missed! Lets checkout the podium
            Wait(0.5),
            self.balloon.posInterval(7.0, Point3(60, -10, 54)),
            Func(self.slappy.setChatAbsolute, 'Hey look! The Beatles are playing!', CFSpeech | CFTimeout),
            # 22 Seconds

            # Back to the Launchpad
            Wait(0.5),
            self.balloon.posInterval(4.0, Point3(-15, 33, 54)),
            Func(self.slappy.setChatAbsolute, 'Hope you enjoyed the Ride!', CFSpeech | CFTimeout),
            # 27.5 Seconds

            # Set her down; gently
            Wait(0.5),
            self.balloon.posInterval(5.0, Point3(-15, 33, 1.1)),
            # 33 Seconds
        )
        self.rideSequence.start()
        self.rideSequence.setT(offset)
        
    def exitStartRide(self):
        self.rideSequence.finish()

    def enterRideOver(self, offset):
        self.ignore('enter' + self.collisionNP.node().getName())
        if self.avId == base.localAvatar.doId:
            # We were on the ride! Better reparent to the render and get out of the balloon...
            base.localAvatar.disableAvatarControls()
            self.hopOffAnim = Sequence(Wait(1), Parallel(Func(base.localAvatar.b_setParent, ToontownGlobals.SPRender), Func(base.localAvatar.b_setAnimState, 'jump', 1.0)), Wait(0.3), base.localAvatar.posInterval(0.3, (-14, 25, 6)), base.localAvatar.posInterval(0.7, (-14, 20, 0)), Wait(0.3), Func(base.localAvatar.enableAvatarControls))
            self.hopOffAnim.start()
        