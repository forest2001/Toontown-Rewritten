from direct.directnotify import DirectNotifyGlobal
from toontown.building.DistributedBuildingAI import DistributedBuildingAI

class DistributedAnimBuildingAI(DistributedBuildingAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedAnimBuildingAI")

