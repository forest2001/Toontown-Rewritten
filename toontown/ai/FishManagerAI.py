from toontown.fishing import FishGlobals
from toontown.fishing.FishBase import FishBase
import random

class FishManagerAI:
        
    def creditFishTank(self, av):
        totalFish = len(av.fishCollection)
        trophies = int(totalFish / 10)
        curTrophies = len(av.fishingTrophies)
        av.addMoney(av.fishTank.getTotalValue())
        av.b_setFishTank([], [], [])
        if trophies > curTrophies:
            av.b_setMaxHp(av.getMaxHp() + trophies - curTrophies)
            av.toonUp(av.getMaxHp())
            av.b_setFishingTrophies(range(trophies))
            return True
        return False

    def generateCatch(self, av, zoneId):
        if len(av.fishTank) >= av.getMaxFishTank():
            return [FishGlobals.OverTankLimit, 0, 0, 0]
        rand = random.random() * 100.0
        for cutoff in FishGlobals.SortedProbabilityCutoffs:
            if rand <= cutoff:
                itemType = FishGlobals.ProbabilityDict[cutoff]
                break
        if itemType == FishGlobals.FishItem:
            success, genus, species, weight = FishGlobals.getRandomFishVitals(zoneId, av.getFishingRod())
            fish = FishBase(genus, species, weight)
            fishType = av.fishCollection.collectFish(fish)
            if fishType == FishGlobals.COLLECT_NEW_ENTRY:
                itemType = FishGlobals.FishItemNewEntry
            elif fishType == FishGlobals.COLLECT_NEW_RECORD:
                itemType = FishGlobals.FishItemNewRecord
            else:
                itemType = FishGlobals.FishItem
            netlist = av.fishCollection.getNetLists()
            av.d_setFishCollection(netlist[0], netlist[1], netlist[2])
            av.fishTank.addFish(fish)
            netlist = av.fishTank.getNetLists()
            av.d_setFishTank(netlist[0], netlist[1], netlist[2])
            return [itemType, genus, species, weight]
        elif itemType == FishGlobals.BootItem:
            return [itemType, 0, 0, 0]
        else:
            money = FishGlobals.Rod2JellybeanDict[av.getFishingRod()]
            av.addMoney(money)
            return [itemType, money, 0, 0]
