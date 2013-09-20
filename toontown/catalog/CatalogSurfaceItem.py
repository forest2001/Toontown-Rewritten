# 2013.08.22 22:17:16 Pacific Daylight Time
# Embedded file name: toontown.catalog.CatalogSurfaceItem
import CatalogItem
import CatalogAtticItem
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from CatalogSurfaceColors import *
STWallpaper = 0
STMoulding = 1
STFlooring = 2
STWainscoting = 3
NUM_ST_TYPES = 4

class CatalogSurfaceItem(CatalogAtticItem.CatalogAtticItem):
    __module__ = __name__

    def makeNewItem(self):
        CatalogAtticItem.CatalogAtticItem.makeNewItem(self)

    def setPatternIndex(self, patternIndex):
        self.patternIndex = patternIndex

    def setColorIndex(self, colorIndex):
        self.colorIndex = colorIndex

    def saveHistory(self):
        return 1

    def recordPurchase(self, avatar, optional):
        self.giftTag = None
        house, retcode = self.getHouseInfo(avatar)
        if retcode >= 0:
            house.addWallpaper(self)
        return retcode

    def getDeliveryTime(self):
        return 60
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\catalog\CatalogSurfaceItem.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:17:16 Pacific Daylight Time
