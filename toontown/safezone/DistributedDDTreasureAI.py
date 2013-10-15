from direct.directnotify import DirectNotifyGlobal
from toontown.safezone.DistributedTreasureAI import DistributedTreasureAI

class DistributedDDTreasureAI(DistributedTreasureAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedDDTreasureAI")

