from direct.directnotify import DirectNotifyGlobal
from toontown.safezone.DistributedTreasureAI import DistributedTreasureAI

class DistributedTTTreasureAI(DistributedTreasureAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedTTTreasureAI")

