from DNAStorageElement import DNAStorageElement
from DNAParser import *

class DNAStorageRoot(DNAStorageElement):
    TAG = 'storage'
    PARENTS = [None]

    def __init__(self, scope='global'):
        DNAStorageElement.__init__(self)

        self.scope = scope

registerElement(DNAStorageRoot)
