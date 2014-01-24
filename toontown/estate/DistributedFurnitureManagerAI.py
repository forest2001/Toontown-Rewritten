from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from toontown.catalog.CatalogItemList import CatalogItemList
from toontown.catalog import CatalogItem
from toontown.catalog.CatalogFurnitureItem import CatalogFurnitureItem
from DistributedFurnitureItemAI import DistributedFurnitureItemAI

FURNITURE_FAILURE_BAD_ARGS = -1
FURNITURE_FAILURE_MISSING_OBJECT = -2
FURNITURE_FAILURE_MISSING_INDEX = -3
FURNITURE_FAILURE_NONMATCHING_ITEM = -4
FURNITURE_FAILURE_DESTINATION_OCCUPIED = -5

class FurnitureError(Exception):
    def __init__(self, code):
        Exception.__init__(self)
        self.code = code

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
        self.items = []

        # Initialize the above variables:
        self.loadFromHouse()

    def announceGenerate(self):
        DistributedObjectAI.announceGenerate(self)
        for item in self.items:
            item.generateWithRequired(self.zoneId)

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
        # Decode the blob:
        items = CatalogItemList(items, store=CatalogItem.Customization|CatalogItem.Location)

        # Throw out our old items:
        for item in self.items:
            item.destroy()
        self.items = []

        for item in items:
            do = DistributedFurnitureItemAI(self.air, self, item)
            if self.isGenerated():
                do.generateWithRequired(self.zoneId)
            self.items.append(do)

    def getItems(self):
        items = CatalogItemList(store=CatalogItem.Customization|CatalogItem.Location)

        for item in self.items:
            items.append(item.catalogItem)

        return items.getBlob()

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


    # Furniture-manipulation:
    def moveItemToAttic(self, doId):
        item = self.getItemObject(doId)

        self.atticItems.append(item.catalogItem)
        self.d_setAtticItems(self.getAtticItems())

        item.destroy()
        self.items.remove(item)

    def moveItemFromAttic(self, index, x, y, z, h, p, r):
        item = self.getAtticFurniture(self.atticItems, index)

        self.atticItems.remove(item)
        self.d_setAtticItems(self.getAtticItems())

        item.posHpr = (x, y, z, h, p, r)

        do = DistributedFurnitureItemAI(self.air, self, item)
        do.generateWithRequired(self.zoneId)
        self.items.append(do)

        return (0, do.doId)

    def deleteItemFromAttic(self, blob, index):
        pass

    def deleteItemFromRoom(self, blob, doId):
        pass

    def moveWallpaperFromAttic(self, index, room):
        pass

    def deleteWallpaperFromAttic(self, blob, index):
        pass

    def moveWindowToAttic(self, slot):
        pass

    def moveWindowFromAttic(self, index, slot):
        pass

    def moveWindow(self, fromSlot, toSlot):
        pass

    def deleteWindowFromAttic(self, blob, index):
        pass

    def recoverDeletedItem(self, blob, index):
        pass

    # Network handlers for the above:
    def handleMessage(self, func, response, *args):
        context = args[-1]
        args = args[:-1]

        try:
            retval = func(*args) or 0
        except FurnitureError as e:
            retval = e.code

        if response == 'moveItemFromAtticResponse':
            # This message actually includes a doId; we split the retval apart
            # if it's a tuple, otherwise it falls back to 0.
            if type(retval) == tuple:
                retval, doId = retval
            else:
                doId = 0

            self.sendUpdate(response, [retval, doId, context])
        else:
            self.sendUpdate(response, [retval, context])

    def moveItemToAtticMessage(self, doId, context):
        self.handleMessage(self.moveItemToAttic, 'moveItemToAtticResponse', doId, context)

    def moveItemFromAtticMessage(self, index, x, y, z, h, p, r, context):
        self.handleMessage(self.moveItemFromAttic, 'moveItemFromAtticResponse',
                           index, x, y, z, h, p, r, context)

    def deleteItemFromAtticMessage(self, blob, index, context):
        self.handleMessage(self.deleteItemFromAttic, 'deleteItemFromAtticResponse', blob, index, context)

    def deleteItemFromRoomMessage(self, blob, doId, context):
        self.handleMessage(self.deleteItemFromRoom, 'deleteItemFromRoomResponse', blob, doId, context)

    def moveWallpaperFromAtticMessage(self, index, room, context):
        self.handleMessage(self.moveWallpaperFromAttic, 'moveWallpaperFromAtticResponse', index, room, context)

    def deleteWallpaperFromAtticMessage(self, blob, index, context):
        self.handleMessage(self.deleteWallpaperFromAttic, 'deleteWallpaperFromAtticResponse', blob, index, context)

    def moveWindowToAtticMessage(self, slot, context):
        self.handleMessage(self.moveWindowToAttic, 'moveWindowToAtticResponse', slot, context)

    def moveWindowFromAtticMessage(self, index, slot, context):
        self.handleMessage(self.moveWindowFromAttic, 'moveWindowFromAtticResponse', index, slot, context)

    def moveWindowMessage(self, fromSlot, toSlot, context):
        self.handleMessage(self.moveWindow, 'moveWindowResponse', fromSlot, toSlot, context)

    def deleteWindowFromAtticMessage(self, blob, index, context):
        self.handleMessage(self.deleteWindowFromAttic, 'deleteWindowFromAtticResponse', blob, index, context)

    def recoverDeletedItemMessage(self, blob, index, context):
        self.handleMessage(self.recoverDeletedItem, 'recoverDeletedItemResponse', blob, index, context)

    # Functions to safely process data off the wire:
    def getItemObject(self, doId):
        item = self.air.doId2do.get(doId)

        if item is None:
            raise FurnitureError(FURNITURE_FAILURE_MISSING_OBJECT)

        if item not in self.items:
            raise FurnitureError(FURNITURE_FAILURE_MISSING_OBJECT)

        return item

    def getAtticFurniture(self, attic, index):
        if index >= len(attic):
            raise FurnitureError(FURNITURE_FAILURE_MISSING_INDEX)

        return attic[index]
