from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

class LobbyManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("LobbyManagerAI")

