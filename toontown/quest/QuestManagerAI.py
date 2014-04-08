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
        pass

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

    def requestInteract(self, avId, npc):
        if simbase.air.doId2do.has_key(avId):
            av = simbase.air.doId2do[avId]
            quests = av.quests
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

    def avatarCancelled(self, avId):
        pass

    def avatarChoseQuest(self, avId, npc, questId, rewardId, toNpcId):
        self.notify.debug("avatar chose quest %s"%str((questId, rewardId, toNpcId)))

    def avatarChoseTrack(self, avId, npc, pendingTrackQuest, trackId):
        pass

    def toonMadeFriend(self, av, otherAv):
        pass
