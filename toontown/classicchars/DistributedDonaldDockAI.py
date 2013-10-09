from direct.directnotify import DirectNotifyGlobal
from toontown.classicchars.DistributedCCharBaseAI import DistributedCCharBaseAI

class DistributedDonaldDockAI(DistributedCCharBaseAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedDonaldDockAI")

