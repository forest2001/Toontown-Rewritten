from DNAElement import DNAElement
from DNAParser import *

class DNAStorageElement(DNAElement):
    def __init__(self):
        DNAElement.__init__(self)

        self.scope = None

    def getScope(self):
        if self.scope is not None:
            return self.scope
        elif self.parent is not None:
            return self.parent
        else:
            raise DNAParseError('No scope defined')

    def store(self, storage):
        """
        Stores everything into the specified DNAStorage object.
        """
        
        self._store(storage)

        for child in self.children:
            child.store(storage)

    def _store(self, storage):
        pass # Overridable by subclass
