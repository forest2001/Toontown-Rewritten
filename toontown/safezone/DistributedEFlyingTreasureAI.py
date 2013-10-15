from direct.directnotify import DirectNotifyGlobal
from toontown.safezone.DistributedTreasureAI import DistributedTreasureAI

class DistributedEFlyingTreasureAI(DistributedTreasureAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedEFlyingTreasureAI")

