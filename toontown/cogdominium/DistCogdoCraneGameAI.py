from direct.directnotify import DirectNotifyGlobal
from toontown.cogdominium.DistCogdoLevelGameAI import DistCogdoLevelGameAI

class DistCogdoCraneGameAI(DistCogdoLevelGameAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistCogdoCraneGameAI")

