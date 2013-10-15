from direct.directnotify import DirectNotifyGlobal
from toontown.safezone.DistributedTreasureAI import DistributedTreasureAI

class DistributedDLTreasureAI(DistributedTreasureAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedDLTreasureAI")

