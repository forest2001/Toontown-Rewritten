# 2013.08.22 22:18:00 Pacific Daylight Time
# Embedded file name: toontown.cogdominium.DistCogdoMazeGameBase
from direct.showbase.RandomNumGen import RandomNumGen
from toontown.cogdominium.CogdoMaze import CogdoMazeFactory
import CogdoMazeGameGlobals as Globals

class DistCogdoMazeGameBase():
    __module__ = __name__

    def createRandomNumGen(self):
        return RandomNumGen(self.doId)

    def createMazeFactory(self, randomNumGen):
        return CogdoMazeFactory(randomNumGen, Globals.NumQuadrants[0], Globals.NumQuadrants[1])
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\cogdominium\DistCogdoMazeGameBase.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:18:00 Pacific Daylight Time
