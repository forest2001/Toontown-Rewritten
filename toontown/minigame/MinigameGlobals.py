# 2013.08.22 22:22:52 Pacific Daylight Time
# Embedded file name: toontown.minigame.MinigameGlobals
from direct.showbase import PythonUtil
from toontown.toonbase import ToontownGlobals
from toontown.hood import ZoneUtil
latencyTolerance = 10.0
MaxLoadTime = 40.0
rulesDuration = 16
JellybeanTrolleyHolidayScoreMultiplier = 2
DifficultyOverrideMult = int(1 << 16)

def QuantizeDifficultyOverride(diffOverride):
    return int(round(diffOverride * DifficultyOverrideMult)) / float(DifficultyOverrideMult)


NoDifficultyOverride = 2147483647
NoTrolleyZoneOverride = -1
SafeZones = [ToontownGlobals.ToontownCentral,
 ToontownGlobals.DonaldsDock,
 ToontownGlobals.DaisyGardens,
 ToontownGlobals.MinniesMelodyland,
 ToontownGlobals.TheBrrrgh,
 ToontownGlobals.DonaldsDreamland]

def getDifficulty(trolleyZone):
    hoodZone = getSafezoneId(trolleyZone)
    return float(SafeZones.index(hoodZone)) / (len(SafeZones) - 1)


def getSafezoneId(trolleyZone):
    return ZoneUtil.getCanonicalHoodId(trolleyZone)


def getScoreMult(trolleyZone):
    szId = getSafezoneId(trolleyZone)
    multiplier = PythonUtil.lerp(1.0, 1.5, float(SafeZones.index(szId)) / (len(SafeZones) - 1))
    return multiplier
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\minigame\MinigameGlobals.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:22:52 Pacific Daylight Time
