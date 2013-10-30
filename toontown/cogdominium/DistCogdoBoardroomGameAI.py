from direct.directnotify import DirectNotifyGlobal
from toontown.cogdominium.DistCogdoLevelGameAI import DistCogdoLevelGameAI

class DistCogdoBoardroomGameAI(DistCogdoLevelGameAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistCogdoBoardroomGameAI")

