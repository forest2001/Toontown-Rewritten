from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from toontown.golf.DistributedGolfHoleAI import DistributedGolfHoleAI
from toontown.golf import GolfGlobals
import random

class DistributedGolfCourseAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedGolfCourseAI")
    
    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.air = air
        self.avatars = []
        self.joinedAvatars = []
        self.holeIds = []
        self.courseId = 0
        self.chDoId = 0
        self.scores = []
        self.zone = 0
        self.chIndex = -1
    
    def generate(self):
        self.cInfo = GolfGlobals.CourseInfo[self.courseId]
        self.scores = [0] * len(self.avatars) * self.cInfo['numHoles']
        self.d_setScores(self.scores)
        #while len(self.holeIds) != self.cInfo['numHoles']:
        while len(self.holeIds) != self.cInfo['numHoles']:
            i = random.randint(0, len(self.cInfo['holeIds']) - 1)
            try:
                holeId = int(self.cInfo['holeIds'][i])
            except:
                holeId = int(self.cInfo['holeIds'][i][0])
                
            if holeId not in self.holeIds:
                self.holeIds.append(holeId)


    def setGolferIds(self, avIds):
        self.avatars = avIds
        
    def d_setGolferIds(self, avIds):
        self.sendUpdate('setGolferIds', [avIds])
    
    def b_setGolferIds(self, avIds):
        self.setGolferIds(avIds)
        self.d_setGolferIds(avIds)
        
    def getGolferIds(self):
        return self.avatars

    def setCourseId(self, courseId):
        self.courseId = courseId
        
    def d_setCourseId(self, courseId):
        self.sendUpdate('setCourseId', [courseId])
        
    def b_setCourseId(self, courseId):
        self.setCourseId(courseId)
        self.d_setCourseId(courseId)
        
    def getCourseId(self):
        return self.courseId

    def setAvatarJoined(self):
        avId = self.air.getAvatarIdFromSender()
        if avId not in self.avatars:
            self.air.writeServerEvent('suspicious', avId=avId, issue='Toon tried to join a golf game they\'re not in!')
            return
        if avId in self.joinedAvatars:
            self.air.writeServerEvent('suspicious', avId=avId, issue='Toon tried to join a golf course twice!')
            return
        self.acceptOnce(self.air.getAvatarExitEvent(avId), self.forceExit)
        self.joinedAvatars.append(avId)
        if set(self.avatars) == set(self.joinedAvatars):
            self.sendUpdate('setCourseReady', [len(self.holeIds), self.holeIds, self.calcCoursePar()])
            self.createNextHole()
            self.sendUpdate('setPlayHole', [])

    def createNextHole(self):
        if self.chDoId:
            self.air.doId2do[self.chDoId].requestDelete()
        self.chIndex += 1
        if self.chIndex == self.cInfo['numHoles']:
            self.forceExit()
            #self.calculateTrophies()
            return
        hole = DistributedGolfHoleAI(self.air)
        hole.setHoleId(self.holeIds[self.chIndex])
        hole.setTimingCycleLength(10)
        hole.setGolfCourseDoId(self.doId)
        hole.setGolferIds(self.avatars)
        hole.generateWithRequired(self.zone)
        
        self.b_setCurHoleIndex(self.chIndex)
        self.b_setCurHoleDoId(hole.doId)
    
    def forceExit(self):
        for avId in self.avatars:
            self.sendUpdate('setCourseAbort', [avId])
            self.ignore(self.air.getAvatarExitEvent(avId))
        if self.chDoId:
            self.air.doId2do[self.chDoId].requestDelete()
        self.air.deallocateZone(self.zone)
        self.requestDelete()
    
    def calculateTrophies(self):
        #for avId in self.avatars:
        #    av = self.air.doId2do[avId]
        #    history = av.getGolfHistory()
        #    
        #trophiesList = []
        #rankingsList = []
        #holeBestList = []
        #cupList = []
        #tieBreakWinner = []
        #self.sendUpdate('setReward', [trophiesList, rankingsList, holeBestList, courseBestList, cupList, tieBreakWinner, aim0, aim1, aim2, aim3])
        pass
     
    def setAvatarReadyCourse(self):
        pass

    def setAvatarReadyHole(self):
        pass

    def setAvatarExited(self):
        pass

    def setCurHoleIndex(self, chIndex):
        self.chIndex = chIndex
    
    def d_setCurHoleIndex(self, chIndex):
        self.sendUpdate('setCurHoleIndex', [chIndex])
        
    def b_setCurHoleIndex(self, chIndex):
        self.setCurHoleIndex(chIndex)
        self.d_setCurHoleIndex(chIndex)
        
    def getCurHoleIndex(self):
        return self.chIndex

    def setCurHoleDoId(self, chDoId):
        self.chDoId = chDoId
        
    def d_setCurHoleDoId(self, chDoId):
        self.sendUpdate('setCurHoleDoId', [chDoId])
        
    def b_setCurHoleDoId(self, chDoId):
        self.setCurHoleDoId(chDoId)
        self.d_setCurHoleDoId(chDoId)
        
    def getCurHoleDoId(self):
        return self.chDoId

    def setDoneReward(self):
        pass

    def setReward(self, trophiesList, rankingsList, holeBestList, courseBestList, cupList, tieBreakWinner, aim0, aim1, aim2, aim3):
        pass

    def setCourseReady(self, todo0, todo1, todo2):
        pass

    def setHoleStart(self, todo0):
        pass

    def setCourseExit(self):
        pass

    def setCourseAbort(self, todo0):
        pass

    def setPlayHole(self):
        pass

    def avExited(self, todo0):
        pass

    def setScores(self, scores):
        self.scores = scores
    
    def d_setScores(self, scores):
        self.sendUpdate('setScores', [scores])
        
    def b_setScores(self, scores):
        self.setScores(scores)
        self.d_setScores(scores)
        
    def getScores(self):
        return self.scores

    def changeDrivePermission(self, todo0, todo1):
        pass
        
    def calcCoursePar(self):
        retval = 0
        for holeId in self.holeIds:
            holeInfo = GolfGlobals.HoleInfo[holeId]
            retval += holeInfo['par']

        return retval
        
    def __finishGolfHole(self):
        pass