from direct.directnotify import DirectNotifyGlobal
from toontown.classicchars.DistributedCCharBaseAI import DistributedCCharBaseAI

class DistributedGoofyAI(DistributedCCharBaseAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedGoofyAI")

