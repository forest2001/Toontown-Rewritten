from direct.directnotify import DirectNotifyGlobal
from toontown.coghq.DistributedBarrelBaseAI import DistributedBarrelBaseAI

class DistributedBeanBarrelAI(DistributedBarrelBaseAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedBeanBarrelAI")

