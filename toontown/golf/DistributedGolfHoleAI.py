from direct.directnotify import DirectNotifyGlobal
from toontown.golf.DistributedPhysicsWorldAI import DistributedPhysicsWorldAI

class DistributedGolfHoleAI(DistributedPhysicsWorldAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedGolfHoleAI")
    
    def __init__(self, air):
        DistributedPhysicsWorldAI.__init__(self, air)
        self.air = air
        self.holeId = 1
        self.tcLength = 1.0
        self.gcDoId = 0
        self.avatars = []
        self.readyAvatars = []
        self.finishedAvatars = []
        self.avatarSwings = {}
        self.curGolfer = 0
        
    def generate(self):
        for av in self.avatars:
            self.avatarSwings[av] = 0

    def setHoleId(self, holeId):
        self.holeId = holeId
    
    def d_setHoleId(self, holeId):
        self.sendUpdate('setHoleId', [holeId])
        
    def b_setHoleId(self, holeId):
        self.setHoleId(holeId)
        self.d_setHoleId(holeId)
        
    def getHoleId(self):
        return self.holeId
        
    #this is required, but the client doesn't HAVE this. WTF
    def setTimingCycleLength(self, tcLength):
        self.tcLength = tcLength
        
    def d_setTimingCycleLength(self, tcLength):
        self.sendUpdate('setTimingCycleLength', [tcLength])
        
    def b_setTimingCycleLength(self, tcLength):
        self.setTimingCycleLength(tcLength)
        self.d_setTimingCycleLength(tcLength)

    def getTimingCycleLength(self):
        return self.tcLength
        
    def setAvatarReadyHole(self):
        avId = self.air.getAvatarIdFromSender()
        if not avId in self.avatars:
            self.air.writeServerEvent('suspicious', avId, 'Toon tried to join a hole for a game of golf they\'re not in!')
            return
        if avId in self.readyAvatars:
            self.air.writeServerEvent('suspicious', avId, 'Toon tried to join a golf hole twice!')
            return
        self.readyAvatars.append(avId)
        if set(self.readyAvatars) == set(self.avatars):
            self.curGolfer = self.avatars[0]
            self.sendUpdate('golferChooseTee', [self.curGolfer])

    def setGolfCourseDoId(self, gcDoId):
        self.gcDoId = gcDoId
        
    def d_setGolfCourseDoId(self, gcDoId):
        self.sendUpdate('setGolfCourseDoId', [gcDoId])
        
    def b_setGolfCourseDoId(self, gcDoId):
        self.setGolfCourseDoId(gcDoId)
        self.d_setGolfCourseDoId(gcDoId)
        
    def getGolfCourseDoId(self):
        return self.gcDoId
        
    def turnDone(self):
        avId = self.air.getAvatarIdFromSender()
        if not avId in self.avatars:
            self.air.writeServerEvent('suspicious', avId, 'Toon tried to end their turn in a golf game they\'re not playing in!')
            return
        if avId != self.curGolfer:
            self.air.writeServerEvent('suspicious', avId, 'Toon tried to end someone else\'s turn in a game of golf!')
            return
        avIndex = self.avatars.index(avId)
        if set(self.avatars) == self.finishedAvatars:
            return
        if len(self.avatars) == 1:
            self.__newGolfer(avId)
            return
        while avIndex != len(self.avatars) - 1:
            avIndex += 1
            if self.avatars[avIndex] not in self.finishedAvatars:
                self.__newGolfer(self.avatars[avIndex])
                return
        for i in range(len(self.avatars)):
            if self.avatars[i] not in self.finishedAvatars:
                self.__newGolfer(self.avatars[i])
                return

    def __newGolfer(self, avId):
        self.curGolfer = avId
        if self.avatarSwings[avId] == 0:
            self.sendUpdate('golferChooseTee', [self.curGolfer])
        else:
            self.sendUpdate('golfersTurn', [avId])
        self.avatarSwings[avId] += 1
    def ballInHole(self):
        avId = self.air.getAvatarIdFromSender()
        if not avId in self.avatars:
            self.air.writeServerEvent('suspicious', avId, 'Toon tried to get a hole in a golf game they\'re not playing in!')
            return
        if avId in self.finishedAvatars:
            self.air.writeServerEvent('suspicious', avId, 'Toon tried to get a hole twice!')
            return
        if avId != self.curGolfer:
            self.air.writeServerEvent('suspicious', avId, 'Toon tried to get a hole while someone else is golfing!')
            return
        self.finishedAvatars.append(avId)

    def setAvatarTempTee(self, todo0, todo1):
        pass

    def setTempAimHeading(self, todo0, todo1):
        pass

    def setAvatarFinalTee(self, avId, tee):
        pass

    def setGolferIds(self, avatars):
        self.avatars = avatars
    
    def d_setGolferIds(self, avatars):
        self.sendUpdate('setGolferIds', [avatars])
        
    def b_setGolferIds(self, avatars):
        self.setGolferIds(avatars)
        self.d_setGolferIds(avatars)
        
    def getGolferIds(self):
        return self.avatars

    def golfersTurn(self, todo0):
        pass

    def golferChooseTee(self, todo0):
        pass

    def setAvatarTee(self, tee):
        avId = self.air.getAvatarIdFromSender()
        if not avId in self.avatars:
            self.air.writeServerEvent('suspicious', avId, 'Toon tried to set their tee in a game they\'re not in!')
            return
        if avId != self.curGolfer:
            self.air.writeServerEvent('suspicious', avId, 'Toon tried to set their tee while not being the current golfer!')
            return
        self.sendUpdate('setAvatarFinalTee', [avId, tee])
        self.sendUpdate('golfersTurn', [avId])

    def postSwing(self, todo0, todo1, todo2, todo3, todo4, todo5, todo6):
        pass

    def postSwingState(self, cycleTime, power, bX, bY, bZ, x, y, aimTime, cod):
        avId = self.air.getAvatarIdFromSender()
        if not avId in self.avatars:
            self.air.writeServerEvent('suspicious', avId, 'Toon tried to swing in a golf game they\'re not playing in!')
            return
        if avId != self.curGolfer:
            self.air.writeServerEvent('suspicious', avId, 'Toon tried to golf outside of their turn!')
            return
        self.sendUpdateToAvatarId(avId, 'assignRecordSwing', [avId, cycleTime, power, bX, bY, bZ, x, y, cod])

    def swing(self, todo0, todo1, todo2, todo3, todo4, todo5, todo6):
        pass

    def ballMovie2AI(self, cycleTime, avId, recording, aVRecording, ballInHoleFrame, ballTouchedHoleFrame, ballFirstTouchedHoleFrame, COD):
        #who needs security?
        self.sendUpdate('ballMovie2Client', [cycleTime, avId, recording, aVRecording, ballInHoleFrame, ballTouchedHoleFrame, ballFirstTouchedHoleFrame, COD])
        pass

    def ballMovie2Client(self, todo0, todo1, todo2, todo3, todo4, todo5, todo6, todo7):
        pass

    def assignRecordSwing(self, todo0, todo1, todo2, todo3, todo4, todo5, todo6, todo7, todo8):
        pass

    def setBox(self, todo0, todo1, todo2, todo3, todo4, todo5, todo6, todo7, todo8, todo9, todo10, todo11, todo12):
        pass

    def sendBox(self, todo0, todo1, todo2, todo3, todo4, todo5, todo6, todo7, todo8, todo9, todo10, todo11, todo12):
        pass

