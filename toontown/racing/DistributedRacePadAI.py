from direct.directnotify import DirectNotifyGlobal
from toontown.racing.DistributedKartPadAI import DistributedKartPadAI

class DistributedRacePadAI(DistributedKartPadAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedRacePadAI")

    def setState(self, todo0, todo1):
        pass

    def setRaceZone(self, todo0):
        pass

    def setTrackInfo(self, todo0):
        pass

