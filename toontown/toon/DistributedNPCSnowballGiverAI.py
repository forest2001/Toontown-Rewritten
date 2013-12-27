from otp.ai.AIBaseGlobal import *
from direct.task.Task import Task
from pandac.PandaModules import *
from DistributedNPCToonBaseAI import *
from toontown.quest import Quests

class DistributedNPCSnowballGiverAI(DistributedNPCToonBaseAI):

    def __init__(self, air, npcId, questCallback = None, hq = 0):
        DistributedNPCToonBaseAI.__init__(self, air, npcId, questCallback)
        self.air = air
        self.hq = hq
        self.tutorial = 0
        self.pendingAvId = None
        return

    def getTutorial(self):
        return self.tutorial

    def setTutorial(self, val):
        self.tutorial = val

    def getHq(self):
        return self.hq

    def avatarEnter(self):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)
        self.notify.debug('avatar enter ' + str(avId))
        #av.d_setSystemMessage(0, 'avatar entered, gib snowballs pls')
        av.b_setPieType(1)
        av.b_setNumPies(10)
        
        self.sendUpdate('gaveSnowballs', [self.npcId, avId])
        
        #self.air.questManager.requestInteract(avId, self)
        #DistributedNPCToonBaseAI.avatarEnter(self)
        #self.rejectAvatar(avId)

    def setMovieDone(self):
        avId = self.air.getAvatarIdFromSender()
        self.notify.debug('setMovieDone busy: %s avId: %s' % (self.busy, avId))
        if self.busy == avId:
            taskMgr.remove(self.uniqueName('clearMovie'))
            self.sendClearMovie(None)
        elif self.busy:
            self.air.writeServerEvent('suspicious', avId, 'DistributedNPCToonAI.setMovieDone busy with %s' % self.busy)
            self.notify.warning('somebody called setMovieDone that I was not busy with! avId: %s' % avId)
        return
