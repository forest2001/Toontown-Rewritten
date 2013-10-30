from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

class TutorialManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("TutorialManagerAI")

    def requestTutorial(self):
        pass

    def rejectTutorial(self):
        pass

    def requestSkipTutorial(self):
        pass

    def skipTutorialResponse(self, todo0):
        pass

    def enterTutorial(self, todo0, todo1, todo2, todo3):
        pass

    def allDone(self):
        pass

    def toonArrived(self):
        pass

