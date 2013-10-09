from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

class DistributedStageBattleAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedStageBattleAI")

