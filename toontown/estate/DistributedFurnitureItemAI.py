from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedSmoothNodeAI import DistributedSmoothNodeAI
from toontown.catalog import CatalogItem
import HouseGlobals

class DistributedFurnitureItemAI(DistributedSmoothNodeAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedFurnitureItemAI")

    def __init__(self, air, furnitureMgr, catalogItem):
        DistributedSmoothNodeAI.__init__(self, air)

        self.furnitureMgr = furnitureMgr
        self.catalogItem = catalogItem

        self.mode = HouseGlobals.FURNITURE_MODE_OFF
        self.modeAvId = 0

    def announceGenerate(self):
        x, y, z, h, p, r = self.catalogItem.posHpr
        self.b_setPosHpr(x, y, z, h, p, r)

    def getItem(self):
        return (self.furnitureMgr.doId,
                self.catalogItem.getBlob(CatalogItem.Customization))

    def requestPosHpr(self, final, x, y, z, h, p, r, t):
        senderId = self.air.getAvatarIdFromSender()
        if (not self.furnitureMgr.director or
                senderId != self.furnitureMgr.director.doId):
            self.air.writeServerEvent('suspicious', senderId,
                                      'Tried to move furniture without being the director!')
            return

        self.catalogItem.posHpr = x, y, z, h, p, r

        if not final and self.mode != HouseGlobals.FURNITURE_MODE_START:
            self.b_setMode(HouseGlobals.FURNITURE_MODE_START, senderId)
        elif final and self.mode == HouseGlobals.FURNITURE_MODE_START:
            self.b_setMode(HouseGlobals.FURNITURE_MODE_STOP, 0)
            return

        self.sendUpdate('setSmPosHpr', [x, y, z, h, p, r, t])

    def setMode(self, mode, avId):
        self.mode = mode
        self.modeAvId = avId

        if mode == HouseGlobals.FURNITURE_MODE_STOP:
            x, y, z, h, p, r = self.catalogItem.posHpr
            self.b_setPosHpr(x, y, z, h, p, r)

    def d_setMode(self, mode, avId):
        self.sendUpdate('setMode', [mode, avId])

    def b_setMode(self, mode, avId):
        self.setMode(mode, avId)
        self.d_setMode(mode, avId)

    def getMode(self):
        return self.mode, self.modeAvId

    def destroy(self):
        # Presently, we just delete ourselves... No real shutdown needed.
        self.requestDelete()
