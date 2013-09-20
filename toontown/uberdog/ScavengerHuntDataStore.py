# 2013.08.22 22:26:56 Pacific Daylight Time
# Embedded file name: toontown.uberdog.ScavengerHuntDataStore
from direct.directnotify import DirectNotifyGlobal
from toontown.uberdog.DataStore import *

class ScavengerHuntDataStore(DataStore):
    __module__ = __name__
    QueryTypes = DataStore.addQueryTypes(['GetGoals', 'AddGoal'])
    notify = DirectNotifyGlobal.directNotify.newCategory('ScavengerHuntDataStore')

    def __init__(self, filepath):
        DataStore.__init__(self, filepath)

    def handleQuery(self, query):
        qId, qData = query
        if qId == self.QueryTypes['GetGoals']:
            avId, goal = qData
            goals = self.__getGoalsForAvatarId(avId)
            return (qId, (avId, goal, goals))
        elif qId == self.QueryTypes['AddGoal']:
            avId, goal = qData
            self.__addGoalToAvatarId(avId, goal)
            return (qId, (avId,))
        return None

    def __addGoalToAvatarId(self, avId, goal):
        if self.wantAnyDbm:
            pAvId = cPickle.dumps(avId)
            pGoal = cPickle.dumps(goal)
            pData = self.data.get(pAvId, None)
            if pData is not None:
                data = cPickle.loads(pData)
            else:
                data = set()
            data.add(goal)
            pData = cPickle.dumps(data)
            self.data[pAvId] = pData
        else:
            self.data.setdefault(avId, set())
            self.data[avId].add(goal)
        self.incrementWriteCount()
        return

    def __getGoalsForAvatarId(self, avId):
        if self.wantAnyDbm:
            pAvId = cPickle.dumps(avId)
            pData = self.data.get(pAvId, None)
            if pData is not None:
                data = list(cPickle.loads(pData))
            else:
                data = []
            return data
        else:
            return list(self.data.get(avId, []))
        return
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\uberdog\ScavengerHuntDataStore.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:26:56 Pacific Daylight Time
