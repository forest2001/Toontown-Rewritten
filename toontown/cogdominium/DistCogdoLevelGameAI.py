from direct.directnotify import DirectNotifyGlobal
from toontown.cogdominium.DistCogdoGameAI import DistCogdoGameAI
from otp.level.DistributedLevelAI import DistributedLevelAI

class DistCogdoLevelGameAI(DistCogdoGameAI, DistributedLevelAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistCogdoLevelGameAI")

