from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedSmoothNodeAI import DistributedSmoothNodeAI
from toontown.catalog import CatalogItem

class DistributedFurnitureItemAI(DistributedSmoothNodeAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedFurnitureItemAI")

    def __init__(self, air, furnitureMgr, catalogItem):
        DistributedSmoothNodeAI.__init__(self, air)

        self.furnitureMgr = furnitureMgr
        self.catalogItem = catalogItem

        x, y, z, h, p, r = self.catalogItem.posHpr
        self.setPosHpr(x, y, z, h, p, r)

    def getItem(self):
        return (self.furnitureMgr.doId,
                self.catalogItem.getBlob(CatalogItem.Customization))

    def requestPosHpr(self, final, x, y, z, h, p, r, t):
        # TODO: Smoothing. For now, just set position and update catalogItem:
        self.catalogItem.posHpr = x, y, z, h, p, r
        self.b_setPosHpr(x, y, z, h, p, r)

    def getMode(self):
        # TODO: Enable/disable smoothing mode.
        return 0, 0

