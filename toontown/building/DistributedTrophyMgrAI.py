from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

class DistributedTrophyMgrAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedTrophyMgrAI")

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.scores = {}

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
        messenger.send('leaderboardChanged')
        messenger.send('leaderboardFlush')
        if avId in self.air.doId2do:
            self.air.doId2do[avId].sendUpdate('setTrophyScore', [self.scores[avId][1]])

    def getLeaderInfo(self):
        avIds = []
        names = []
        scores = []
        for avId, data in self.scores.items():
            avIds.append(avId)
            names.append(data[0])
            scores.append(data[1])
        return (avIds, names, scores)
