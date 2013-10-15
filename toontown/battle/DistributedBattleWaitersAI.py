from direct.directnotify import DirectNotifyGlobal
from toontown.battle.DistributedBattleFinalAI import DistributedBattleFinalAI

class DistributedBattleWaitersAI(DistributedBattleFinalAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedBattleWaitersAI")

