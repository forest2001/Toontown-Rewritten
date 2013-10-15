from direct.directnotify import DirectNotifyGlobal
from toontown.suit.DistributedFactorySuitAI import DistributedFactorySuitAI

class DistributedMintSuitAI(DistributedFactorySuitAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedMintSuitAI")

