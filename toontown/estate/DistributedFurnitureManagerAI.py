from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

class DistributedFurnitureManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedFurnitureManagerAI")

    def setOwnerId(self, todo0):
        pass

    def setOwnerName(self, todo0):
        pass

    def setInteriorId(self, todo0):
        pass

    def setAtticItems(self, todo0):
        pass

    def setAtticWallpaper(self, todo0):
        pass

    def setAtticWindows(self, todo0):
        pass

    def setDeletedItems(self, todo0):
        pass

    def suggestDirector(self, todo0):
        pass

    def setDirector(self, todo0):
        pass

    def avatarEnter(self):
        pass

    def avatarExit(self):
        pass

    def moveItemToAtticMessage(self, todo0, todo1):
        pass

    def moveItemToAtticResponse(self, todo0, todo1):
        pass

    def moveItemFromAtticMessage(self, todo0, todo1, todo2, todo3, todo4, todo5, todo6, todo7):
        pass

    def moveItemFromAtticResponse(self, todo0, todo1, todo2):
        pass

    def deleteItemFromAtticMessage(self, todo0, todo1, todo2):
        pass

    def deleteItemFromAtticResponse(self, todo0, todo1):
        pass

    def deleteItemFromRoomMessage(self, todo0, todo1, todo2):
        pass

    def deleteItemFromRoomResponse(self, todo0, todo1):
        pass

    def moveWallpaperFromAtticMessage(self, todo0, todo1, todo2):
        pass

    def moveWallpaperFromAtticResponse(self, todo0, todo1):
        pass

    def deleteWallpaperFromAtticMessage(self, todo0, todo1, todo2):
        pass

    def deleteWallpaperFromAtticResponse(self, todo0, todo1):
        pass

    def moveWindowToAtticMessage(self, todo0, todo1):
        pass

    def moveWindowToAtticResponse(self, todo0, todo1):
        pass

    def moveWindowFromAtticMessage(self, todo0, todo1, todo2):
        pass

    def moveWindowFromAtticResponse(self, todo0, todo1):
        pass

    def moveWindowMessage(self, todo0, todo1, todo2):
        pass

    def moveWindowResponse(self, todo0, todo1):
        pass

    def deleteWindowFromAtticMessage(self, todo0, todo1, todo2):
        pass

    def deleteWindowFromAtticResponse(self, todo0, todo1):
        pass

    def recoverDeletedItemMessage(self, todo0, todo1, todo2):
        pass

    def recoverDeletedItemResponse(self, todo0, todo1):
        pass

