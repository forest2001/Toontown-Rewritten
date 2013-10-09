from direct.directnotify import DirectNotifyGlobal
from toontown.classicchars.DistributedCCharBaseAI import DistributedCCharBaseAI

class DistributedChipAI(DistributedCCharBaseAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedChipAI")

