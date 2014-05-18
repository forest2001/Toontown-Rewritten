from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from operator import itemgetter

class DistributedTrophyMgrAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedTrophyMgrAI")

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.scores = {}
        self.scoreLists = ([], [], [])

    def requestTrophyScore(self):
        avId = self.air.getAvatarIdFromSender()
        if avId in self.scores:
            if avId in self.air.doId2do:
                self.air.doId2do[avId].sendUpdate('setTrophyScore', [self.scores[avId][1]])

    def removeTrophy(self, avId, numFloors):
        if not avId in self.scores:
            self.notify.warning("avId %d is not in scores"%avId)
            return
        self.scores[avId][1] -= numFloors
        if self.scores[avId][1] < 0:
            self.notify.warning("avId %d has a negative scorevalue?~?~?!"%avId)
            self.scores[avId][1] = 0
        self.sort()
        messenger.send('leaderboardChanged')
        messenger.send('leaderboardFlush')
        if avId in self.air.doId2do:
            self.air.doId2do[avId].sendUpdate('setTrophyScore', [self.scores[avId][1]])

    def addTrophy(self, avId, name, numFloors):
        if not avId in self.scores:
            if not self.air.doId2do.has_key(avId):
                    return
            self.scores[avId] = ['', 0]
            self.scores[avId][1] = 0
            av = self.air.doId2do[avId]
            self.scores[avId][0] = av.getName()
        self.scores[avId][1] += numFloors
        self.sort()
        messenger.send('leaderboardChanged')
        messenger.send('leaderboardFlush')
        if avId in self.air.doId2do:
            self.air.doId2do[avId].sendUpdate('setTrophyScore', [self.scores[avId][1]])
            
    def sort(self):
        scoreList = []
        for avId, data in self.scores.items():
            scoreList.append(avId, data[0], data[1])
        sorted(scoreList, key=itemgetter(2), reverse=True)
        avIds = []
        names = []
        scores = []
        for avId, name, score in scoreList:
            avIds.append(avId)
            names.append(name)
            scores.append(score)
            if len(scores) == 10:
                break # We're done!
        self.scoreLists = (avIds, names, scores)

    def getLeaderInfo(self):
        return self.scoreLists
