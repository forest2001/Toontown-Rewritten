from DNAStorageElement import DNAStorageElement
from DNAParser import *

class DNAStoreTexture(DNAStorageElement):
    TAG = 'store_texture'
    PARENTS = ['storage']

    def __init__(self, root, code, path):
        DNAStorageElement.__init__(self)

        self.root = root
        self.code = code
        self.path = path

    def _store(self, storage):
        texture = loader.loadTexture(self.path)
        storage.storeTexture(texture, self.code, self.getScope())
        storage.storeCatalogCode(self.root, self.code)

registerElement(DNAStoreTexture)
