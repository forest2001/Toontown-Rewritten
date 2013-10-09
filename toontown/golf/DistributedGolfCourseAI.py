from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

class DistributedGolfCourseAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedGolfCourseAI")

    def setGolferIds(self, todo0):
        pass

    def setCourseId(self, todo0):
        pass

    def setAvatarJoined(self):
        pass

    def setAvatarReadyCourse(self):
        pass

    def setAvatarReadyHole(self):
        pass

    def setAvatarExited(self):
        pass

    def setCurHoleIndex(self, todo0):
        pass

    def setCurHoleDoId(self, todo0):
        pass

    def setDoneReward(self):
        pass

    def setReward(self, todo0, todo1, todo2, todo3, todo4, todo5, todo6, todo7, todo8, todo9):
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

    def setScores(self, todo0):
        pass

    def changeDrivePermission(self, todo0, todo1):
        pass

