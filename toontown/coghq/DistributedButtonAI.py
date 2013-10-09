from direct.directnotify import DirectNotifyGlobal
from toontown.coghq.DistributedSwitchAI import DistributedSwitchAI

class DistributedButtonAI(DistributedSwitchAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedButtonAI")

