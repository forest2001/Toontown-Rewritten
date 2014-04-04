from DNAStorageElement import DNAStorageElement
from DNAParser import *

class DNAModel(DNAStorageElement):
    TAG = 'model'
    PARENTS = ['storage']

    def __init__(self, path, scope=None):
        DNAStorageElement.__init__(self)

        self.path = path
        self.scope = scope

        self.model = None

    def getModel(self):
        if not self.model:
            self.model = loader.loadModel(self.path)

        return self.model

registerElement(DNAModel)
