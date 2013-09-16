# 2013.08.22 22:22:50 Pacific Daylight Time
# Embedded file name: toontown.minigame.MazeGameGlobals
from direct.showbase import RandomNumGen

def getMazeName(gameDoId, numPlayers, mazeNames):
    try:
        return forcedMaze
    except:
        names = mazeNames[numPlayers - 1]
        return names[RandomNumGen.randHash(gameDoId) % len(names)]


ENDLESS_GAME = config.GetBool('endless-maze-game', 0)
GAME_DURATION = 60.0
SHOWSCORES_DURATION = 2.0
SUIT_TIC_FREQ = int(256)
WALK_SAME_DIRECTION_PROB = 4
WALK_TURN_AROUND_PROB = 30
SUIT_START_POSITIONS = ((0.25, 0.25),
 (0.75, 0.75),
 (0.25, 0.75),
 (0.75, 0.25),
 (0.2, 0.5),
 (0.8, 0.5),
 (0.5, 0.2),
 (0.5, 0.8),
 (0.33, 0.0),
 (0.66, 0.0),
 (0.33, 1.0),
 (0.66, 1.0),
 (0.0, 0.33),
 (0.0, 0.66),
 (1.0, 0.33),
 (1.0, 0.66))
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\minigame\MazeGameGlobals.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:22:50 Pacific Daylight Time
