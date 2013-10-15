from direct.directnotify import DirectNotifyGlobal
from toontown.building.DistributedDoorAI import DistributedDoorAI

class DistributedCogHQDoorAI(DistributedDoorAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedCogHQDoorAI")

