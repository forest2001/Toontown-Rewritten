# 2013.08.22 22:17:09 Pacific Daylight Time
# Embedded file name: toontown.catalog.CatalogInvalidItem
import CatalogItem
from toontown.toonbase import TTLocalizer
from direct.showbase import PythonUtil
from toontown.toonbase import ToontownGlobals

class CatalogInvalidItem(CatalogItem.CatalogItem):
    __module__ = __name__

    def requestPurchase(self, phone, callback):
        self.notify.error('Attempt to purchase invalid item.')

    def acceptItem(self, mailbox, index, callback):
        self.notify.error('Attempt to accept invalid item.')

    def output(self, store = -1):
        return 'CatalogInvalidItem()'
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\catalog\CatalogInvalidItem.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:17:09 Pacific Daylight Time
