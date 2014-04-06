from panda3d.core import *

class DNAStorageEntry:
    def __init__(self, entity, type, code, scope):
        self.type = type
        self.code = code
        self.scope = scope
        self.entity = entity

class DNAStorage:
    def __init__(self):
        self._typecode2entry = {}

    def store(self, entity, type, code, scope):
        entry = DNAStorageEntry(entity, type, code, scope)
        self._typecode2entry[(type, code)] = entry

    def find(self, type, code):
        entry = self._typecode2entry.get((type, code))
        if entry:
            return entry.entity

    def reset(self, type=None, scope=None):
        toPurge = set()
        for entry in self._typecode2entry.itervalues():
            if type is not None and entry.type != type:
                continue
            if scope is not None and entry.scope != scope:
                continue
            toPurge.add(entry)

        for purge in toPurge:
            del self._typecode2entity[(purge.type, purge.code)]

    # Helpers for the above:
    def storeNode(self, node, code, scope='global'):
        self.store(node, 'node', code, scope)

    def storeFont(self, font, code, scope='global'):
        self.store(font, 'font', code, scope)

    def storeTexture(self, texture, code, scope='global'):
        self.store(texture, 'texture', code, scope)

    def findNode(self, code):
        return self.find('node', code)

    def findFont(self, code):
        return self.find('font', code)

    def findTexture(self, code):
        return self.find('texture', code)
