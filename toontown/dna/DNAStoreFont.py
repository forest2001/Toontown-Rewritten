from DNAStorageElement import DNAStorageElement
from DNAParser import *

class DNAStoreFont(DNAStorageElement):
    TAG = 'store_font'
    PARENTS = ['storage']

    def __init__(self, root, code, path):
        DNAStorageElement.__init__(self)

        self.root = root
        self.code = code
        self.path = path

    def _store(self, storage):
        font = loader.loadFont(self.path)
        storage.storeFont(self.code, font, self.getScope())

registerElement(DNAStoreFont)
