from direct.directnotify import DirectNotifyGlobal
from toontown.battle.DistributedBattleBaseAI import DistributedBattleBaseAI

class DistributedBattleAI(DistributedBattleBaseAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedBattleAI")

