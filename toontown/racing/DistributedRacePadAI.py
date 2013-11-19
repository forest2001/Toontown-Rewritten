from direct.directnotify import DirectNotifyGlobal
from toontown.racing.DistributedKartPadAI import DistributedKartPadAI
from toontown.racing.DistributedRaceAI import DistributedRaceAI
from toontown.racing import RaceGlobals
from direct.distributed.ClockDelta import *
from direct.task import *

#TODO - change race type

class DistributedRacePadAI(DistributedKartPadAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedRacePadAI")
    
    def __init__(self, air):
        DistributedKartPadAI.__init__(self, air)
        self.air = air
        self.trackId, self.trackType = [None, None]
        self.lastTime = globalClockDelta.getRealNetworkTime()
        self.state = 'WaitEmpty'
        self.startingBlocks = []
    
    def updateTimer(self):
        hasAvatars = False
        for block in self.startingBlocks:
            if block.avId != 0:
                hasAvatars = True
                break
        if hasAvatars and self.state == 'WaitEmpty':
            self.b_setState('WaitCountdown', globalClockDelta.getRealNetworkTime())
            taskMgr.doMethodLater(30, DistributedRacePadAI.startRace, 'startRace%i' % self.doId, [self])
        elif not hasAvatars and self.state == 'WaitCountdown':
            self.b_setState('WaitEmpty', globalClockDelta.getRealNetworkTime())
            taskMgr.remove('startRace%i' % self.doId)
            
    def startRace(self):
        self.b_setState('AllAboard', globalClockDelta.getRealNetworkTime())
        taskMgr.doMethodLater(2, DistributedRacePadAI.createRace, 'createRace%i' % self.doId, [self])
        
    def createRace(self):
        self.raceZone = self.air.allocateZone()
        avatars = []
        for block in self.startingBlocks:
            if block.avId != 0:
                avatars.append(block.avId)
                self.sendUpdateToAvatarId(block.avId, 'setRaceZone', [self.raceZone])
        race = DistributedRaceAI(self.air)
        race.setZoneId(self.raceZone)
        race.setTrackId(self.trackId)
        race.setRaceType(self.trackType)
        race.setCircuitLoop([])
        race.setAvatars(avatars)
        race.setStartingPlaces(range(len(avatars)))
        race.setLapCount(3)
        race.generateWithRequired(self.raceZone)
        for block in self.startingBlocks:
            block.b_setOccupied(0)
        self.b_setState('WaitEmpty', globalClockDelta.getRealNetworkTime())

        
     
    def addStartingBlock(self, block):
        self.startingBlocks.append(block)
        
    def removeStartingBlock(self, block):
        if self.startingBlocks.count(block):
            self.startingBlocks.remove(block)

    def setState(self, state, timeStamp):
        self.state = state
        self.lastTime = globalClockDelta.getRealNetworkTime()
    
    def d_setState(self, state, timeStamp):
        self.sendUpdate('setState', [state, timeStamp])
    
    def b_setState(self, state, timeStamp):
        self.setState(state, timeStamp)
        self.d_setState(state, timeStamp)
    
    def getState(self):
        return [self.state, self.lastTime]
        
    def setRaceZone(self, todo0):
        pass
        
    def getTrackInfo(self):
        return [self.trackId, self.trackType]
        
    def setTrackInfo(self, trackInfo):
        self.trackId, self.trackType = trackInfo
        
    def d_setTrackInfo(self, trackInfo):
        self.sendUpdate('setTrackInfo',  [trackInfo])
    
    def b_setTrackInfo(self, trackInfo):
        self.setTrackInfo(trackInfo)
        self.b_setTrackInfo(trackInfo)

