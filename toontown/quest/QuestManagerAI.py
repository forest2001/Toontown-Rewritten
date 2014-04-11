import Quests
from direct.directnotify import DirectNotifyGlobal

class QuestManagerAI:
    notify = DirectNotifyGlobal.directNotify.newCategory('QuestManagerAI')
    def __init__(self):
        pass

    def toonKilledCogs(self, toon, suitsKilled, zoneId, activeToonList):
        pass

    def recoverItems(self, toon, suitsKilled, zoneId):
        #return (recovered, notRecovered)
        return ([], [])

    def toonKilledBuilding(self, toon, track, difficulty, numFloors, zoneId, activeToons):
        pass

    def toonKilledCogdo(self, toon, difficulty, numFloors, zoneId, activeToons):
        pass

    def toonRecoveredCogSuitPart(self, av, zoneId, avList):
        pass

    def toonDefeatedFactory(self, toon, factoryId, activeVictors):
        pass

    def toonDefeatedMint(self, toon, mintId, activeVictors):
        pass

    def toonDefeatedStage(self, toon, stageId, activeVictors):
        pass

    def toonPlayedMinigame(self, toon, toons):
        pass

    def toonRodeTrolleyFirstTime(self, toon):
        pass

    def completeQuest(self, av, questId):
        '''
        Remove the quest from the player's quest inventory
        This function exists because I think it may be necesary to do more logic here in the future, time will tell
        '''
        av.removeQuest(questId)

    def giveReward(self, av, rewardId):
        '''Give the player the reward'''
        reward = Quests.getReward(rewardId)
        if reward:
            reward.sendRewardAI(av)

    def npcGiveQuest(self, npc, av, questId, rewardId, toNpcId):
        '''Have npc assign quest to av'''
        av.addQuest((questId, npc.getDoId(), toNpcId, rewardId, 0), Quests.Quest2RemainingStepsDict[questId] == 1)
        npc.assignQuest(av.getDoId(), questId, rewardId, toNpcId)

    def requestInteract(self, avId, npc):
        '''Handle interactions between a player and an npc'''
        if simbase.air.doId2do.has_key(avId):
            av = simbase.air.doId2do[avId]
            quests = av.quests

            #First, check if there are any quests to turn in
            for quest in quests:
                questDesc = quest
                questId, fromNpcId, toNpcId, rewardId, toonProgress = questDesc
                quest = Quests.getQuest(questId)
                complete = quest.getCompletionStatus(av, questDesc, npc)
                if complete == Quests.COMPLETE:
                    #check if there is a next quest
                    nextQuest = Quests.getNextQuest(questId, npc, av)
                    if nextQuest == (Quests.NA, Quests.NA):
                        rewardId = Quests.getAvatarRewardId(av, questId) #idk about this one, maybe a single quest can have different rewards?
                        npc.completeQuest(avId, questId, rewardId)
                        self.completeQuest(av, questId)
                        self.giveReward(av, rewardId)
                        return
                    else:
                        #gib quest
                        questId = nextQuest[0]
                        rewardId = Quests.getFinalRewardId(questId, 1)
                        toNpcId = nextQuest[1]
                        self.completeQuest(av, questId)
                        self.npcGiveQuest(npc, av, questId, rewardId, toNpcId)

            #stuff below this return is to-be rewritten
            npc.rejectAvatar(npcId)
            return
            numQuests = len(quests)
            if numQuests+1 > av.getQuestCarryLimit():
                npc.rejectAvatar(avId)
                return
            questHistory = av.getQuestHistory()
            #HACK ALERT
            #TODO: fix this for tutorial quests
            toonTier = 1
            for tier, questList in Quests.Tier2QuestsDict.items():
                if tier < toonTier:
                    continue
                toonTier = tier
                breaking = False
                for questId in questList:
                    if not questId in questHistory:
                        breaking = True
                        break
                if breaking:
                    break

            offeredQuests = Quests.chooseBestQuests(toonTier, npc, av)
            if not offeredQuests:
                npc.rejectAvatarTierNotDone(avId)
                return
            npc.presentQuestChoice(avId, offeredQuests)
            return
        #if nothing else, reject them
        npc.rejectAvatar(avId)

    def avatarCancelled(self, avId):
        pass

    def avatarChoseQuest(self, avId, npc, questId, rewardId, toNpcId):
        if simbase.air.doId2do.has_key(avId):
            av = simbase.air.doId2do[avId]
            self.notify.debug("avatar chose quest %s"%str((questId, rewardId, toNpcId)))
            self.npcGiveQuest(npc, av, questId, rewardId, toNpcId)

    def avatarChoseTrack(self, avId, npc, pendingTrackQuest, trackId):
        pass

    def toonMadeFriend(self, av, otherAv):
        pass
