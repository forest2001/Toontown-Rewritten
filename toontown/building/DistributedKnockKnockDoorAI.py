from direct.directnotify import DirectNotifyGlobal
from toontown.building.DistributedAnimatedPropAI import DistributedAnimatedPropAI

class DistributedKnockKnockDoorAI(DistributedAnimatedPropAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedKnockKnockDoorAI")

