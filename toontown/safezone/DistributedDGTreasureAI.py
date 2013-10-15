from direct.directnotify import DirectNotifyGlobal
from toontown.safezone.DistributedTreasureAI import DistributedTreasureAI

class DistributedDGTreasureAI(DistributedTreasureAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedDGTreasureAI")

