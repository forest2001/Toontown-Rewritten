from direct.directnotify import DirectNotifyGlobal
from toontown.coghq.DistributedSwitchAI import DistributedSwitchAI

class DistributedTriggerAI(DistributedSwitchAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedTriggerAI")

