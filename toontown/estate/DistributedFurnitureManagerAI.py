from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from toontown.catalog.CatalogItemList import CatalogItemList
from toontown.catalog import CatalogItem

class DistributedFurnitureManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedFurnitureManagerAI")

    def __init__(self, air, house, interior):
        DistributedObjectAI.__init__(self, air)

        self.house = house
        self.interior = interior

        self.director = None

        self.ownerId = house.avatarId
        self.ownerName = house.name

        self.atticItems = None
        self.atticWallpaper = None
        self.atticWindows = None
        self.deletedItems = None

        # Initialize the above variables:
        self.loadFromHouse()

    def loadFromHouse(self):
        self.b_setAtticItems(self.house.getAtticItems())
        self.b_setAtticWallpaper(self.house.getAtticWallpaper())
        self.b_setAtticWindows(self.house.getAtticWindows())
        self.b_setDeletedItems(self.house.getDeletedItems())

        self.interior.b_setWallpaper(self.house.getInteriorWallpaper())
        self.interior.b_setWindows(self.house.getInteriorWindows())

        self.setItems(self.house.getInteriorItems())

    def saveToHouse(self):
        self.house.b_setAtticItems(self.getAtticItems())
        self.house.b_setAtticWallpaper(self.getAtticWallpaper())
        self.house.b_setAtticWindows(self.getAtticWindows())
        self.house.b_setDeletedItems(self.getDeletedItems())

        self.house.b_setInteriorWallpaper(self.interior.getWallpaper())
        self.house.b_setInteriorWindows(self.interior.getWindows())

        self.house.b_setInteriorItems(self.getItems())

    def setItems(self, items):
        pass

    def getItems(self):
        return ''

    def setOwnerId(self, ownerId):
        self.ownerId = ownerId

    def d_setOwnerId(self, ownerId):
        self.sendUpdate('setOwnerId', [ownerId])

    def b_setOwnerId(self, ownerId):
        self.setOwnerId(ownerId)
        self.d_setOwnerId(ownerId)

    def getOwnerId(self):
        return self.ownerId

    def setOwnerName(self, ownerName):
        self.ownerName = ownerName

    def d_setOwnerName(self, ownerName):
        self.sendUpdate('setOwnerName', [ownerName])

    def b_setOwnerName(self, ownerName):
        self.setOwnerName(ownerName)
        self.d_setOwnerName(ownerName)

    def getOwnerName(self):
        return self.ownerName

    def getInteriorId(self):
        return self.interior.doId

    def setAtticItems(self, items):
        self.atticItems = CatalogItemList(items, store=CatalogItem.Customization)

    def d_setAtticItems(self, items):
        self.sendUpdate('setAtticItems', [items])

    def b_setAtticItems(self, items):
        self.setAtticItems(items)
        if self.isGenerated():
            self.d_setAtticItems(items)

    def getAtticItems(self):
        return self.atticItems.getBlob()

    def setAtticWallpaper(self, items):
        self.atticWallpaper = CatalogItemList(items, store=CatalogItem.Customization)

    def d_setAtticWallpaper(self, items):
        self.sendUpdate('setAtticWallpaper', [items])

    def b_setAtticWallpaper(self, items):
        self.setAtticWallpaper(items)
        if self.isGenerated():
            self.d_setAtticWallpaper(items)

    def getAtticWallpaper(self):
        return self.atticWallpaper.getBlob()

    def setAtticWindows(self, items):
        self.atticWindows = CatalogItemList(items, store=CatalogItem.Customization)

    def d_setAtticWindows(self, items):
        self.sendUpdate('setAtticWindows', [items])

    def b_setAtticWindows(self, items):
        self.setAtticWindows(items)
        if self.isGenerated():
            self.d_setAtticWindows(items)

    def getAtticWindows(self):
        return self.atticWindows.getBlob()

    def setDeletedItems(self, items):
        self.deletedItems = CatalogItemList(items, store=CatalogItem.Customization)

    def d_setDeletedItems(self, items):
        self.sendUpdate('setDeletedItems', [items])

    def b_setDeletedItems(self, items):
        self.setDeletedItems(items)
        if self.isGenerated():
            self.d_setDeletedItems(items)

    def getDeletedItems(self):
        return self.deletedItems.getBlob()

    def suggestDirector(self, directorId):
        senderId = self.air.getAvatarIdFromSender()

        if self.ownerId != senderId:
            self.air.writeServerEvent('suspicious', senderId,
                                      'Tried to move furniture, but not the house owner!')
            return

        if senderId != directorId and directorId != 0:
            self.air.writeServerEvent('suspicious', senderId,
                                      'Tried to make someone else (%d) move their furniture!' % directorId)
            return

        director = self.air.doId2do.get(directorId)
        if directorId and not director:
            self.air.writeServerEvent('suspicious', directorId,
                                      'Tried to move furniture without being on the shard!')
            return

        if self.director:
            self.director.b_setGhostMode(0)
        if director:
            director.b_setGhostMode(1)

        self.director = director
        self.sendUpdate('setDirector', [directorId])

        # Let's also save the furniture to the house (and thus to the DB) while
        # we're at it...
        self.saveToHouse()

    def avatarEnter(self):
        pass

    def avatarExit(self):
        pass

    def moveItemToAtticMessage(self, todo0, todo1):
        pass

    def moveItemFromAtticMessage(self, todo0, todo1, todo2, todo3, todo4, todo5, todo6, todo7):
        pass

    def deleteItemFromAtticMessage(self, todo0, todo1, todo2):
        pass

    def deleteItemFromRoomMessage(self, todo0, todo1, todo2):
        pass

    def moveWallpaperFromAtticMessage(self, todo0, todo1, todo2):
        pass

    def deleteWallpaperFromAtticMessage(self, todo0, todo1, todo2):
        pass

    def moveWindowToAtticMessage(self, todo0, todo1):
        pass

    def moveWindowFromAtticMessage(self, todo0, todo1, todo2):
        pass

    def moveWindowMessage(self, todo0, todo1, todo2):
        pass

    def deleteWindowFromAtticMessage(self, todo0, todo1, todo2):
        pass

    def recoverDeletedItemMessage(self, todo0, todo1, todo2):
        pass
