from direct.directnotify import DirectNotifyGlobal
from toontown.suit.DistributedFactorySuitAI import DistributedFactorySuitAI

class DistributedStageSuitAI(DistributedFactorySuitAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedStageSuitAI")

