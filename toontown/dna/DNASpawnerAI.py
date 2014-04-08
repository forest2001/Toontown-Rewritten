import re

_type2constructorList = {}

class DNASpawnerAI:
    def __init__(self, air):
        self.air = air

    def spawnObjects(self, filename, zone):
        dna = self.air.loadDNA(filename)

        zoneOffset = zone - dna.zone

        self._traverse(dna, zoneOffset)

    def lookupConstructor(self, element):
        # Returns constructor, regexmatch

        constructorList = _type2constructorList.get(element.__class__)
        if not constructorList:
            return None, None

        # Match regexes within:
        for pattern, constructor in constructorList:
            if pattern is None:
                return constructor, None

            match = pattern.match(element.name)
            if match:
                return constructor, match

        # Full failure.
        return None, None

    def _traverse(self, element, zoneOffset):
        spawned = self._spawn(element, zoneOffset)

        if not spawned:
            for child in element.children:
                self._traverse(child, zoneOffset)

    def _spawn(self, element, zoneOffset):
        """Spawn 'element' into a zone, if it's an element that corresponds to a
        server-sided game object.
        """

        constructor, match = self.lookupConstructor(element)

        if not constructor:
            return False

        vis = element.getVisGroup()
        if not vis:
            return False

        zone = int(vis.name.split(':', 1)[0]) + zoneOffset

        if match is not None:
            # This is a regex-matched constructor; 4 parameters.
            constructor(self.air, zone, element, match)
        else:
            # This is a type-matched constructor; 3 parameters.
            constructor(self.air, zone, element)

        return True

# Decorator to declare the existence of constructors:
def dnaSpawn(type, pattern=None):
    def _decorator(func):
        if pattern:
            # func is a 4-parameter function: (air, zone, element, match)
            _type2constructorList.setdefault(type, []).append((re.compile(pattern), func))
        else:
            # func is a 3-parameter function: (air, zone, element)
            _type2constructorList[type] = [(None, func)]
        return func
    return _decorator
