from direct.directnotify import DirectNotifyGlobal
from toontown.classicchars.DistributedCCharBaseAI import DistributedCCharBaseAI

class DistributedMickeyAI(DistributedCCharBaseAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedMickeyAI")

