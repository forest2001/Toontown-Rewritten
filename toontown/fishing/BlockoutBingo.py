# 2013.08.22 22:20:32 Pacific Daylight Time
# Embedded file name: toontown.fishing.BlockoutBingo
from direct.directnotify import DirectNotifyGlobal
from toontown.fishing import BingoGlobals
from toontown.fishing import BingoCardBase

class BlockoutBingo(BingoCardBase.BingoCardBase):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('BlockoutBingo')

    def __init__(self, cardSize = BingoGlobals.CARD_SIZE, rowSize = BingoGlobals.CARD_ROWS, colSize = BingoGlobals.CARD_COLS):
        BingoCardBase.BingoCardBase.__init__(self, cardSize, rowSize, colSize)
        self.gameType = BingoGlobals.BLOCKOUT_CARD

    def checkForWin(self, id = 0):
        for i in xrange(self.rowSize):
            if not self.rowCheck(i):
                return BingoGlobals.NO_UPDATE

        return BingoGlobals.WIN

    def checkForColor(self, id):
        return 1

    def checkForBingo(self):
        if self.checkForWin():
            return BingoGlobals.WIN
        return BingoGlobals.NO_UPDATE
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\fishing\BlockoutBingo.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:20:32 Pacific Daylight Time
