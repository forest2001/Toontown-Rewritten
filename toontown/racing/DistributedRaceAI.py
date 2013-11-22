from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from toontown.racing.DistributedVehicleAI import DistributedVehicleAI
from toontown.racing.DistributedGagAI import DistributedGagAI
from toontown.racing import RaceGlobals
from direct.distributed.ClockDelta import *
from otp.ai.MagicWordGlobal import *
from direct.fsm.FSM import FSM

import random

class DistributedRaceAI(DistributedObjectAI, FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedRaceAI")
    
    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        FSM.__init__(self, 'DistributedRaceAI')
        self.air = air
        self.zoneId = 0
        self.trackId = 0
        self.raceType = 0
        self.circuitLoop = []
        self.avatars = []
        self.finishedAvatars = []
        self.startingPlaces = []
        self.avatarKarts = []
        self.lapCount = 1
        self.gags = {}
        self.avatarProgress = {}
    
    def generate(self):
        self.request('Join')
        
    def enterJoin(self):
        self.beginBarrier('waitingForJoin', self.avatars, 60, self.joinBarrierCallback)
        self.d_waitingForJoin()
        
    def exitJoin(self):
        pass
        
    def enterPrep(self):
        self.beginBarrier('waitingForReady', self.avatars, 60, self.readyBarrierCallback)
        self.gagPoints = RaceGlobals.TrackDict[self.trackId][4]
        for i in range(len(self.gagPoints)):
            gagId = random.randint(0, 5)
            self.b_genGag(i, 1, gagId)
        self.d_prepForRace()
        
    def exitPrep(self):
        pass
        
    def enterTutorial(self):
        self.beginBarrier('readRules', self.avatars, 30, self.readRulesCallback)
        self.d_startTutorial()
    
    def exitTutorial(self):
        pass
        
    def enterStart(self):
        self.startTime = globalClockDelta.networkToLocalTime(globalClockDelta.getRealNetworkTime())
        self.d_startRace()
        for avatarKart in self.avatarKarts:
            kart = self.air.doId2do[avatarKart[1]]
            kart.sendUpdate('setInput', [1])
            self.avatarProgress[avatarKart[0]] = 0
    
    def exitStart(self):
        pass
    
    def readyBarrierCallback(self, avatars):
        self.request('Tutorial')
        
    def readRulesCallback(self, avatars):
        self.request('Start')
    
    def joinBarrierCallback(self, avatars):
        self.avatars = avatars
        for av in avatars:
            kart = DistributedVehicleAI(self.air, av)
            kart.generateWithRequired(self.zoneId)
            self.avatarKarts.append([av, kart.getDoId()])
        self.beginBarrier('waitingForPrep', self.avatars, 60, self.prepBarrierCallback)
        self.sendUpdate('setEnteredRacers', [self.avatarKarts])
        
    def prepBarrierCallback(self, avatars):
        self.request('Prep')

    
    def setZoneId(self, zoneId):
        self.zoneId = zoneId
        
    def d_setZoneId(self, zoneId):
        self.sendUpdate('setZoneId', [zoneId])
    
    def b_setZoneId(self, zoneId):
        self.setZoneId(zoneId)
        self.d_setZoneId(zoneId)
    
    def getZoneId(self):
        return self.zoneId

    def setTrackId(self, trackId):
        self.trackId = trackId
        
    def getTrackId(self):
        return self.trackId

    def setRaceType(self, raceType):
        self.raceType = raceType
    
    def getRaceType(self):
        return self.raceType
    
    def setCircuitLoop(self, circuitLoop):
        self.circuitLoop = circuitLoop
        
    def getCircuitLoop(self):
        return self.circuitLoop

    def setAvatars(self, avatarList):
        self.avatars = avatarList
        
    def getAvatars(self):
        return self.avatars

    def setStartingPlaces(self, startingPlaces):
        self.startingPlaces = startingPlaces
        
    def getStartingPlaces(self):
        return self.startingPlaces

    def setLapCount(self, lapCount):
        self.lapCount = lapCount
        
    def getLapCount(self):
        return self.lapCount

    def waitingForJoin(self):
        self.beginBarrier('waitingForJoin', self.avatars, 60, self.b_prepForRace)
    
    def d_waitingForJoin(self):
        self.sendUpdate('waitingForJoin', [])
        
    def b_waitingForJoin(self):
        self.waitingForJoin()
        self.d_waitingForJoin()

    def setEnteredRacers(self, todo0):
        pass
    
    
    def d_prepForRace(self):
        self.sendUpdate('prepForRace', [])
    
    def b_prepForRace(self, avatars):
        self.prepForRace()
        self.d_prepForRace()
    
    def startTutorial(self):
        self.beginBarrier('readRules', self.avatars, 60, self.raceStart)
    
    def d_startTutorial(self):
        self.sendUpdate('startTutorial', [])
    
    def b_startTutorial(self, avatars):
        self.startTutorial()
        self.d_startTutorial()

    def startRace(self, startTime):
        pass
    
    
    def d_startRace(self):
        self.sendUpdate('startRace', [globalClockDelta.getRealNetworkTime()])
    
    def goToSpeedway(self, todo0, todo1):
        pass

    def genGag(self, slot, number, type):
        self.gags[slot] = [number, type]
        
    def d_genGag(self, slot, number, type):
        self.sendUpdate('genGag', [slot, number, type])
    
    def b_genGag(self, slot, number, type):
        self.genGag(slot, number, type)
        self.d_genGag(slot, number, type)
    
    def dropAnvilOn(self, todo0, todo1, todo2):
        pass

    def shootPiejectile(self, todo0, todo1, todo2):
        pass

    def racerDisconnected(self, todo0):
        pass

    def setPlace(self, todo0, todo1, todo2, todo3, todo4, todo5, todo6, todo7, todo8, todo9):
        pass

    def setCircuitPlace(self, todo0, todo1, todo2, todo3, todo4, todo5):
        pass

    def endCircuitRace(self):
        pass

    def setRaceZone(self, todo0, todo1):
        pass

    def hasGag(self, todo0, todo1, todo2):
        pass

    def racerLeft(self, todo0):
        pass

    def heresMyT(self, avId, laps, currentLapT, timestamp):
        realAvId = self.air.getAvatarIdFromSender()
        if not avId == realAvId:
            self.air.writeServerEvent('suspicious', realAvId, 'Toon tried to send a message as another toon!')
            return
        if not avId in self.avatars:
            self.air.writeServerEvent('suspicious', avId, 'Toon not in race tried to send update to race!')
            return
        if laps == self.lapCount:
            self.avatarFinished(avId)
            return
        self.avatarProgress[avId] = laps + currentLapT

    def avatarFinished(self, avId):
        av = self.air.doId2do.get(avId)
        self.finishedAvatars.append(avId)
        place = len(self.finishedAvatars) - 1
        entryFee = RaceGlobals.getEntryFee(self.trackId, self.raceType)
        bonus = 0
        totalTime = globalClockDelta.networkToLocalTime(globalClockDelta.getRealNetworkTime()) - self.startTime
        qualify = False
        if totalTime < RaceGlobals.getQualifyingTime(self.trackId):
            qualify = True
        if self.raceType == 'Practice':
            winnings = RaceGlobals.PracticeWinnings
            trophies = []
        else: 
            winnings = entryFee*RaceGlobals.Winnings[place]
            trophies = self.calculateTrophies(avId, place == 0, qualify, totalTime)
        av.b_setTickets(av.getTickets() + winnings)
        if av.getTickets() > RaceGlobals.MaxTickets:
            av.b_setTickets(RaceGlobals.MaxTickets)
        self.sendUpdate('setPlace', [avId, totalTime, place, entryFee, qualify, winnings, bonus, trophies, [], 0])
    
    def calculateTrophies(self, avId, won, qualify, time):
        av = self.air.doId2do[avId]
        kartingHistory = av.getKartingHistory()
        avTrophies = av.getKartingTrophies()
        numTrophies = 0
        for i in range(30):
            if avTrophies[i] != 0:
                numTrophies += 1
        oldLaffBoost = int(numTrophies/10)
        genre = RaceGlobals.getTrackGenre(self.trackId)
        trophies = []
        if won:
            kartingHistory[genre] += 1
            kartingHistory[3] += 1
            if kartingHistory[3] > RaceGlobals.TotalWonRaces:
                avTrophies[RaceGlobals.TotalWins] = 1
                trophies.append(RaceGlobals.TotalWins)
            for i in range(3):
                if kartingHistory[genre] >= RaceGlobals.WonRaces[i] and avTrophies[RaceGlobals.AllWinsList[genre][i]] != 1:
                    avTrophies[RaceGlobals.AllWinsList[genre][i]] = 1
                    trophies.append(RaceGlobals.AllWinsList[genre][i])
        if qualify:
            kartingHistory[genre + 4] += 1
            kartingHistory[7] += 1
            if kartingHistory[7] >= RaceGlobals.TotalQualifiedRaces and avTrophies[RaceGlobals.TotalQuals] != 1:
                avTrophies[RaceGlobals.TotalQuals] = 1
                trophies.append(RaceGlobals.TotalQuals)
            for i in range(3):
                if kartingHistory[genre + 4] >= RaceGlobals.QualifiedRaces[i] and avTrophies[RaceGlobals.AllQualsList[genre][i]] != 1:
                    avTrophies[RaceGlobals.AllQualsList[genre][i]] = 1
                    trophies.append(RaceGlobals.AllQualsList[genre][i])
        pKartingBest = av.getKartingPersonalBestAll()
        gTourTrophy = True
        for bestTime in pKartingBest:
            if not bestTime:
                gTourTrophy = False
        if gTourTrophy:
            for bestTime in pKartingBest2:
                if not bestTime:
                    gTourTrophy = False
            if gTourTrophy:
                if avTrophies[RaceGlobals.GrandTouring] != 1:
                    avTrophies[RaceGlobals.GrandTouring] = 1
                    trophies.append(RaceGlobals.GrandTouring)
        newLaffBoost = int((len(trophies) + numTrophies)/10)
        if newLaffBoost - oldLaffBoost != 0:
            for i in range(newLaffBoost):
                if avTrophies[RaceGlobals.TrophyCups[i]] != 1:
                    avTrophies[RaceGlobals.TrophyCups[i]] = 1
                    trophies.append(RaceGlobals.TrophyCups[i])
            av.b_setMaxHp(av.getMaxHp() + newLaffBoost - oldLaffBoost)
            av.toonUp(av.getMaxHp())
        av.b_setKartingTrophies(avTrophies)
        return trophies

    def requestThrow(self, x, y, z):
        #TODO - perhaps check actual distance?
        pass

    def requestKart(self):
        pass
        avId = self.air.getAvatarIdFromSender()
        accId = self.air.getAccountIdFromSender()
        if not avId in self.avatars:
            self.air.writeServerEvent('suspicious', avId, 'Toon tried to request kart in race they\'re not in!')
            return
        for i in range(len(self.avatarKarts)):
            if self.avatarKarts[i][0] == avId:
                self.air.doId2do[self.avatarKarts[i][1]].request('Controlled', avId, accId)
