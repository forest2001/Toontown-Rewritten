from direct.directnotify import DirectNotifyGlobal
from toontown.suit.DistributedSuitBaseAI import DistributedSuitBaseAI

class DistributedTutorialSuitAI(DistributedSuitBaseAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedTutorialSuitAI")

    def requestBattle(self, todo0, todo1, todo2, todo3, todo4, todo5):
        pass

