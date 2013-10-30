from direct.directnotify import DirectNotifyGlobal
from toontown.battle.DistributedBattleFinalAI import DistributedBattleFinalAI

class DistributedBattleDinersAI(DistributedBattleFinalAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedBattleDinersAI")

