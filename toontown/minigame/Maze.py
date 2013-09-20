# 2013.08.22 22:21:57 Pacific Daylight Time
# Embedded file name: toontown.minigame.Maze
from MazeBase import MazeBase
import MazeData

class Maze(MazeBase):
    __module__ = __name__

    def __init__(self, mapName, mazeData = MazeData.mazeData, cellWidth = MazeData.CELL_WIDTH):
        model = loader.loadModel(mapName)
        mData = mazeData[mapName]
        self.treasurePosList = mData['treasurePosList']
        self.numTreasures = len(self.treasurePosList)
        MazeBase.__init__(self, model, mData, cellWidth)
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\minigame\Maze.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:21:57 Pacific Daylight Time
