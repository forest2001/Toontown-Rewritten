class QuestManagerAI:
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
        pass

    def avatarCancelled(self, avId):
        pass

    def avatarChoseQuest(self, avId, npc, *quest):
        pass

    def avatarChoseTrack(self, avId, npc, pendingTrackQuest, trackId):
        pass

    def toonMadeFriend(self, av, otherAv):
        pass
