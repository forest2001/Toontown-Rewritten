from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

class DistributedDGFlowerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedDGFlowerAI")
    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.avatarsPresent = 0
        self.height = 2.0

    def avatarEnter(self):
        if self.avatarsPresent == 0:
             self.setHeight(10)
        self.avatarsPresent += 1

    def avatarExit(self):
        self.avatarsPresent -= 1
        if self.avatarsPresent == 0:
            self.setHeight(2)

    def setHeight(self, height):
        self.height = height
        self.sendUpdate('setHeight', [self.height])

    def getHeight(self):
        return self.height
