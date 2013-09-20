# 2013.08.22 22:21:12 Pacific Daylight Time
# Embedded file name: toontown.minigame.CannonGameGlobals
TowerYRange = 200
GameTime = 90
MAX_SCORE = 23
MIN_SCORE = 5
FUSE_TIME = 0.0
CANNON_ROTATION_MIN = -20
CANNON_ROTATION_MAX = 20
CANNON_ROTATION_VEL = 15.0
CANNON_ANGLE_MIN = 10
CANNON_ANGLE_MAX = 85
CANNON_ANGLE_VEL = 15.0

def calcScore(t):
    range = MAX_SCORE - MIN_SCORE
    score = MAX_SCORE - range * (float(t) / GameTime)
    return int(score + 0.5)
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\minigame\CannonGameGlobals.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:21:12 Pacific Daylight Time
