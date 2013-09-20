# 2013.08.22 22:16:07 Pacific Daylight Time
# Embedded file name: toontown.battle.BattleExperience
from toontown.toonbase import ToontownBattleGlobals

def genRewardDicts(entries):
    toonRewardDicts = []
    for toonId, origExp, earnedExp, origQuests, items, missedItems, origMerits, merits, parts in entries:
        if toonId != -1:
            dict = {}
            toon = base.cr.doId2do.get(toonId)
            if toon == None:
                continue
            dict['toon'] = toon
            dict['origExp'] = origExp
            dict['earnedExp'] = earnedExp
            dict['origQuests'] = origQuests
            dict['items'] = items
            dict['missedItems'] = missedItems
            dict['origMerits'] = origMerits
            dict['merits'] = merits
            dict['parts'] = parts
            toonRewardDicts.append(dict)

    return toonRewardDicts
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\battle\BattleExperience.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:16:07 Pacific Daylight Time
