from toontown.toonbase import ToontownGlobals
import SuitTimings

class SuitLegList:
    def __init__(self, path):
        self.suitLegType = 0
        self.startTime = 0.0
        self.legTime = 0.0
        self.blockNumber = 0
        self.legs = []
        i = 0
        self.legs.append(SuitLeg(path.getPoint(0), path.getPoint(0), SuitLeg.TFromSky))
        while i+1 < path.getNumPoints():
            point = path.getPoint(i)
            point2 = path.getPoint(i+1)
            self.legs.append(SuitLeg(point, point2, SuitLeg.TWalk))
            i += 1
        endPoint = path.getPoint(path.getNumPoints()-1)
        self.legs.append(SuitLeg(endPoint, endPoint, SuitLeg.TToSky))

    def getStartTime(self, index):
        time = 0
        i = 0
        while i < self.getNumLegs() and i < index:
            time += self.legs[i].getLegTime()
            i += 1
        return time
    
    def getLegIndexAtTime(self, time, startLeg):
        endTime = 0
        i = 0
        while i < startLeg:
            endTime += self.legs[i].getLegTime()
            i += 1
        while i < self.getNumLegs():
            endTime += self.legs[i].getLegTime()
            if endTime > time:
                return i
            i += 1
        return len(self.legs)-1

    def getNumLegs(self):
        return len(self.legs)

    def getZoneId(self, legNum):
        return self.legs[legNum].getZone()

    def getType(self, legNum):
        return self.legs[legNum].getType()

    def isPointInRange(self, point, startTime, endTime):
        leg = self.getLegIndexAtTime(startTime, 0)
        time = startTime
        while time < endTime:
            if leg >= len(self.legs):
                return False
            if self[leg].pointA == point or self[leg].pointB == point:
                return True
            time += self[leg].getLegTime()
            leg += 1
        return False

    def __getitem__(self, key):
        return self.legs[key]

class SuitLeg:
    TWalkFromStreet = 0
    TWalkToStreet = 1
    TWalk = 2
    TFromSky = 3
    TToSky = 4
    TFromSuitBuilding = 5
    TToSuitBuilding = 6
    TToToonBuilding = 7
    TFromCoghq = 8
    TToCoghq = 9
    TOff = 10
    TypeToName = {
      0 : 'WalkFromStreet',
      1 : 'WalkToStreet',
      2 : 'Walk',
      3 : 'FromSky',
      4 : 'ToSky',
      5 : 'FromSuitBuilding',
      6 : 'ToSuitBuilding',
      7 : 'ToToonBuilding',
      8 : 'FromCoghq',
      9 : 'ToCoghq',
      10 : 'Off'
    }
    def __init__(self, pointA, pointB, type):
        self.pointA = pointA
        self.pointB = pointB
        self.posA = pointA.getPos()
        self.posB = pointB.getPos()
        self.type = type
    def getLegTime(self):
        if self.type == SuitLeg.TWalk:
            return (self.posA-self.posB).length()/ToontownGlobals.SuitWalkSpeed
        elif self.type == SuitLeg.TFromSky:
            return SuitTimings.fromSky
        elif self.type == SuitLeg.TToSky:
            return SuitTimings.toSky
    def getPosA(self):
        return self.posA
    def getPosB(self):
        return self.posB
    def getPosAtTime(self, time):
        pos = self.getPosB()-self.getPosA()
        pos = self.getPosA() + pos*(time/self.getLegTime())
        return pos
    def getZone(self):
        return self.pointB.zone
    @staticmethod
    def getTypeName(type):
        return SuitLeg.TypeToName[type]
    def getType(self):
        return self.type
