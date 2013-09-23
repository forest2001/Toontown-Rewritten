from toontown.suit import DistributedFactorySuit
from direct.directnotify import DirectNotifyGlobal

class DistributedMintSuit(DistributedFactorySuit.DistributedFactorySuit):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedMintSuit')
