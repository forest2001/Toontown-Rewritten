# 2013.08.22 22:17:00 Pacific Daylight Time
# Embedded file name: toontown.catalog.CatalogAnimatedFurnitureItem
from CatalogFurnitureItem import *
FTAnimRate = 6
AnimatedFurnitureItemKeys = (10020, 270, 990, 460, 470, 480, 490, 491, 492)

class CatalogAnimatedFurnitureItem(CatalogFurnitureItem):
    __module__ = __name__

    def loadModel(self):
        model = CatalogFurnitureItem.loadModel(self)
        self.setAnimRate(model, self.getAnimRate())
        return model

    def getAnimRate(self):
        item = FurnitureTypes[self.furnitureType]
        if FTAnimRate < len(item):
            animRate = item[FTAnimRate]
            if not animRate == None:
                return item[FTAnimRate]
            else:
                return 1
        else:
            return 1
        return

    def setAnimRate(self, model, rate):
        seqNodes = model.findAllMatches('**/seqNode*')
        for seqNode in seqNodes:
            seqNode.node().setPlayRate(rate)
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\catalog\CatalogAnimatedFurnitureItem.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:17:00 Pacific Daylight Time
