import Quests
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import ToontownBattleGlobals
import random

class QuestManagerAI:
    notify = DirectNotifyGlobal.directNotify.newCategory('QuestManagerAI')
    def __init__(self):
        pass

    def toonKilledCogs(self, toon, suitsKilled, zoneId, activeToonList):
        '''
        Called in battleExpierience to alert the quest system that a
        toon has killed some cogs
        '''
        for questIndex in range(len(toon.quests)):
            quest = Quests.getQuest(toon.quests[questIndex][0])
            if isinstance(quest, Quests.CogQuest):
                for suit in suitsKilled:
                    if quest.doesCogCount(toon.getDoId(), suit, zoneId, activeToonList):
                        toon.quests[questIndex][4] += 1
        toon.b_setQuests(toon.quests)

    def recoverItems(self, toon, suitsKilled, zoneId):
        '''
        Called in battleExpierience to alert the quest system that a toon
        should test for recovered items
        
        Returns a tuple of two lists, [0] - list of recovered items, [1] - list of items not recovered
        '''
        recovered = []
        notRecovered = []
        for questIndex in range(len(toon.quests)):
            quest = Quests.getQuest(toon.quests[questIndex][0])
            if isinstance(quest, Quests.RecoverItemQuest):
                if quest.isLocationMatch(zoneId):
                    if quest.getHolder() == Quests.Any or quest.getHolderType() == 'type' or quest.getHolderType() == 'track' \
                      or quest.getHolderType() == 'level':
                        for suit in suitsKilled:
                            if quest.getHolder() == Quests.Any \
                             or (quest.getHolderType() == 'type' and quest.getHolder() == suit['type']) \
                             or (quest.getHolderType() == 'track' and quest.getHolder() == suit['track']) \
                             or (quest.getHolderType() == 'level' and quest.getHolder() >= suit['level']):
                                self.notify.debug("passed check")
                                if random.randint(1, 100) <= quest.getPercentChance():
                                    recovered.append(quest.getItem())
                                    toon.quests[questIndex][4] += 1
                                else:
                                    notRecovered.append(quest.getItem())
        toon.b_setQuests(toon.quests)
        return (recovered, notRecovered)

    def toonKilledBuilding(self, toon, track, difficulty, numFloors, zoneId, activeToons):
        '''
        Called when a toon defeats a cog building
        '''
        for questIndex in range(len(toon.quests)):
            quest = Quests.getQuest(toon.quests[questIndex][0])
            if isinstance(quest, Quests.BuildingQuest):
                if quest.isLocationMatch(zoneId):
                    if quest.getBuildingTrack() == Quests.Any or quest.getBuildingTrack() == track:
                        if quest.getNumFloors() >= numFloors:
                            toon.quests[questIndex][4] += 1
        toon.b_setQuests(toon.quests)

    def toonKilledCogdo(self, toon, difficulty, numFloors, zoneId, activeToons):
        pass

    def toonRecoveredCogSuitPart(self, av, zoneId, avList):
        pass

    def toonDefeatedFactory(self, toon, factoryId, activeVictors):
        '''
        Called when a toon defeats a factory
        '''
        for questIndex in range(len(toon.quests)):
            quest = Quests.getQuest(toon.quests[questIndex][0])
            if isinstance(quest, Quests.FactoryQuest):
                if quest.doesFactoryCount(toon.getDoId(), factoryId, activeVictors):
                    toon.quests[questIndex][4] += 1
        toon.b_setQuests(toon.quests)

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
        finalReward = 0
        rewardId = Quests.transformReward(rewardId, av)
        if Quests.isStartingQuest(questId):
            finalReward = rewardId
        av.addQuest((questId, npc.getDoId(), toNpcId, rewardId, 0), finalReward)
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
                        if isinstance(quest, Quests.TrackChoiceQuest):
                            #TrackTrainingReward quests are a little different
                            npc.presentTrackChoice(avId, questId, quest.getChoices())
                            return
                        rewardId = Quests.getAvatarRewardId(av, questId) #idk about this one, maybe a single quest can have different rewards?
                        npc.completeQuest(avId, questId, rewardId)
                        self.completeQuest(av, questId)
                        self.giveReward(av, rewardId)
                        return
                    else:
                        #gib quest
                        self.completeQuest(av, questId)
                        questId = nextQuest[0]
                        rewardId = Quests.getFinalRewardId(questId, 1)
                        toNpcId = nextQuest[1]
                        self.npcGiveQuest(npc, av, questId, rewardId, toNpcId)
                        return

            numQuests = len(quests)
            if numQuests+1 > av.getQuestCarryLimit():
                self.notify.debug("Rejecting avId({0}) because their quest inventory is full".format(avId))
                npc.rejectAvatar(avId)
                return

            #check if any quests left in current tier
            rewardHistory = av.getRewardHistory()
            tier = rewardHistory[0]

            #See if eligible for tier upgrade
            if Quests.avatarHasAllRequiredRewards(av, tier):
                if not Quests.avatarWorkingOnRequiredRewards(av):
                    if tier != Quests.ELDER_TIER: #lmao elder tier
                        tier += 1
                    av.b_setRewardHistory(tier, [])
                else:
                    self.notify.debug("Rejecting avId({0}) because still working on tier, but will be eligible for tierup".format(avId))
                    npc.rejectAvatarTierNotDone(avId)

            offeredQuests = Quests.chooseBestQuests(tier, npc, av)
            if not offeredQuests:
                self.notify.debug("Rejecting avId({0}) because no quests available".format(avId))
                npc.rejectAvatar(avId)
                return

            npc.presentQuestChoice(avId, offeredQuests)
            return
        #if nothing else, reject them
        npc.rejectAvatar(avId)

    def avatarCancelled(self, avId):
        '''
        Called by NPCToon to alert the quest system that an avatar
        has cancelled an interaction.
        '''
        #SECURITYTODO: IMPLEMENT THIS
        pass

    def avatarChoseQuest(self, avId, npc, questId, rewardId, toNpcId):
        '''
        Called by NPCToon to alert the quest system that an avatar
        has chosen a quest from the list supplied
        '''
        if simbase.air.doId2do.has_key(avId):
            av = simbase.air.doId2do[avId]
            self.notify.debug("avatar chose quest %s"%str((questId, rewardId, toNpcId)))
            self.npcGiveQuest(npc, av, questId, rewardId, toNpcId)

    def avatarChoseTrack(self, avId, npc, questId, trackId):
        '''
        Called by NPCToon to alert the quest system that an avatar
        has chosen a track from the list supplied
        '''
        if simbase.air.doId2do.has_key(avId):
            av = simbase.air.doId2do[avId]
            #see Quests.py for rewardIds
            rewardId = 400
            if trackId == ToontownBattleGlobals.HEAL_TRACK:
                rewardId = 401
            if trackId == ToontownBattleGlobals.TRAP_TRACK:
                rewardId = 402
            if trackId == ToontownBattleGlobals.LURE_TRACK:
                rewardId = 403
            if trackId == ToontownBattleGlobals.SOUND_TRACK:
                rewardId = 404
            if trackId == ToontownBattleGlobals.THROW_TRACK:
                rewardId = 405
            if trackId == ToontownBattleGlobals.SQUIRT_TRACK:
                rewardId = 406
            if trackId == ToontownBattleGlobals.DROP_TRACK:
                rewardId = 407
            npc.completeQuest(avId, questId, rewardId)
            self.completeQuest(av, questId)
            self.giveReward(av, rewardId)

    def toonMadeFriend(self, av, otherAv):
        pass

    def toonFished(self, toon):
        '''
        Retval: -1 = no relevant quest
        0 = not caught
        itemid = caught
        '''
        for questIndex in range(len(toon.quests)):
            quest = Quests.getQuest(toon.quests[questIndex][0])
            if isinstance(quest, Quests.RecoverItemQuest):
                if quest.isLocationMatch(zoneId):
                    if quest.getHolder() == Quests.AnyFish:
                        if random.randint(1, 100) <= quest.getPercentChance():
                            recovered.append(quest.getItem())
                            toon.quests[questIndex][4] += 1
                            toon.b_setQuests(toon.quests)
                            return quest.getItem()
                        else:
                            return 0
        return -1
