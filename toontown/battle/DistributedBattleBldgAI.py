from direct.directnotify import DirectNotifyGlobal
from toontown.battle.DistributedBattleBaseAI import DistributedBattleBaseAI

class DistributedBattleBldgAI(DistributedBattleBaseAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedBattleBldgAI")

