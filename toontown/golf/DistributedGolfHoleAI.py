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
        pass

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
        pass

    def ballInHole(self):
        pass

    def setAvatarTempTee(self, todo0, todo1):
        pass

    def setTempAimHeading(self, todo0, todo1):
        pass

    def setAvatarFinalTee(self, todo0, todo1):
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

    def setAvatarTee(self, todo0):
        pass

    def postSwing(self, todo0, todo1, todo2, todo3, todo4, todo5, todo6):
        pass

    def postSwingState(self, todo0, todo1, todo2, todo3, todo4, todo5, todo6, todo7, todo8):
        pass

    def swing(self, todo0, todo1, todo2, todo3, todo4, todo5, todo6):
        pass

    def ballMovie2AI(self, todo0, todo1, todo2, todo3, todo4, todo5, todo6, todo7):
        pass

    def ballMovie2Client(self, todo0, todo1, todo2, todo3, todo4, todo5, todo6, todo7):
        pass

    def assignRecordSwing(self, todo0, todo1, todo2, todo3, todo4, todo5, todo6, todo7, todo8):
        pass

    def setBox(self, todo0, todo1, todo2, todo3, todo4, todo5, todo6, todo7, todo8, todo9, todo10, todo11, todo12):
        pass

    def sendBox(self, todo0, todo1, todo2, todo3, todo4, todo5, todo6, todo7, todo8, todo9, todo10, todo11, todo12):
        pass

