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
import ElectionGlobals

class DistributedHotAirBalloon(DistributedObject, FSM):
    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        FSM.__init__(self, 'HotAirBalloonFSM')
        self.avId = 0
        
        # Create the balloon
        self.balloon = loader.loadModel('phase_4/models/events/election_slappyBalloon-static')
        self.balloon.reparentTo(base.render)
        self.balloon.setPos(*ElectionGlobals.BalloonBasePosition)
        self.balloon.setScale(ElectionGlobals.BalloonScale)
        # So we can reparent toons to the balloon so they don't fall out
        self.cr.parentMgr.registerParent(ToontownGlobals.SPSlappysBalloon, self.balloon)
        # Balloon collision NodePath (outside)
        self.collisionNP = self.balloon.find('**/Collision_Outer')
        self.slappy = NPCToons.createLocalNPC(2021)
        self.slappy.reparentTo(self.balloon)
        self.slappy.setPos(0.7, 0.7, 0.4)
        self.slappy.setH(150)
        self.slappy.setScale((1/ElectionGlobals.BalloonScale)) # We want a normal sized Slappy
        self.slappy.loop('neutral')
        
        # Create balloon flight paths. It's important we do this AFTER we load everything
        # else as this requires both the balloon and Slappy.
        self.flightPaths = ElectionGlobals.generateFlightPaths(self)
        self.toonFlightPaths = ElectionGlobals.generateToonFlightPaths(self)
        
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
            base.localAvatar.disableAvatarControls()
            
            self.hopOnAnim = Sequence(Parallel(
                Func(base.localAvatar.b_setParent, ToontownGlobals.SPSlappysBalloon), # Required to put the toon in the basket
                Func(base.localAvatar.b_setAnimState, 'jump', 1.0)), 
                base.localAvatar.posInterval(0.6, (0, 0, 2)), 
                base.localAvatar.posInterval(0.4, (0, 0, 0.7)), 
                Func(base.localAvatar.enableAvatarControls), 
                Func(self.ignore, 'control'),
                Parallel(Func(base.localAvatar.b_setParent, ToontownGlobals.SPRender))) # Unparent the toon and balloon

            self.hopOnAnim.start()
            self.ignore('control')

        self.occupiedSequence = Sequence(
            Func(self.slappy.setChatAbsolute, ElectionGlobals.SlappyUpForARide, CFSpeech | CFTimeout),
            Wait(3.5),
        )
        self.occupiedSequence.start()
        self.occupiedSequence.setT(offset)
        
    def exitOccupied(self):
        self.occupiedSequence.finish()

    def setFlightPath(self, flightPathIndex):
        self.flightPathIndex = flightPathIndex
        
    def enterStartRide(self, offset):
        # Try and get the flightPath from the AI
        try:
            self.rideSequence = self.flightPaths[self.flightPathIndex]
            self.rideSequence.start()
            self.rideSequence.setT(offset)
        except Exception, e:
            self.notify.debug('Exception: %s' % e)

        if self.avId == base.localAvatar.doId:
            # More Try/Excepts!
            try:
                self.toonRideSequence = self.toonFlightPaths[self.flightPathIndex]
                self.toonRideSequence.start()
                self.toonRideSequence.setT(offset)
            except Exception, e:
                self.notify.debug('Exception: %s' % e)
        
    def exitStartRide(self):
        # Try and finish the sequence
        try:
            self.rideSequence.finish()
        except Exception, e:
            self.notify.debug('Exception: %s' % e)

    def enterRideOver(self, offset):
        if self.avId == base.localAvatar.doId:
            # We were on the ride! Better reparent to the render and get out of the balloon...
            base.localAvatar.disableAvatarControls()

            self.hopOffAnim = Sequence(
                Parallel(Func(base.localAvatar.b_setParent, ToontownGlobals.SPRender), Func(base.localAvatar.b_setAnimState, 'jump', 1.0)), 
                Wait(0.3), 
                base.localAvatar.posInterval(0.3, (-14, 25, 6)), 
                base.localAvatar.posInterval(0.7, (-14, 20, 0)), 
                Wait(0.3), 
                Func(base.localAvatar.enableAvatarControls), 
                Wait(0.3), 
                Func(base.localAvatar.b_setAnimState, 'neutral')
                )

            self.hopOffAnim.start()
        