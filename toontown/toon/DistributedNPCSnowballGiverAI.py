from otp.ai.AIBaseGlobal import *
from direct.task.Task import Task
from pandac.PandaModules import *
from DistributedNPCToonBaseAI import *
from toontown.quest import Quests
from random import randrange

class DistributedNPCSnowballGiverAI(DistributedNPCToonBaseAI):

    def __init__(self, air, npcId, questCallback = None, hq = 0):
        DistributedNPCToonBaseAI.__init__(self, air, npcId, questCallback)
        self.air = air

    def avatarEnter(self):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)
        self.notify.debug('avatar enter ' + str(avId))
        av.b_setPieType(1)
        av.b_setNumPies(25)
        self.sendUpdate('gaveSnowballs', [self.npcId, avId, randrange(1)])
