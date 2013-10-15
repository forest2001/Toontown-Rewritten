from direct.directnotify import DirectNotifyGlobal
from toontown.classicchars.DistributedCCharBaseAI import DistributedCCharBaseAI

class DistributedMinnieAI(DistributedCCharBaseAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedMinnieAI")

