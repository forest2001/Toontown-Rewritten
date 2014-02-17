import random

class InvasionMasterAI:
    # How long to ignore an unreachable Toon for:
    UNREACHABLE_TIMEOUT = 30.0

    def __init__(self, invasion):
        self.invasion = invasion

        self._unreachables = {}

    def getAttackableToons(self):
        # This gets the list of Toons in the area that are "attackable" -- they
        # aren't unreachable, they aren't ghosting, etc.

        result = []
        for toon in self.invasion.toons:
            if toon.ghostMode:
                continue

            unreachableTimestamp = self._unreachables.get(toon.doId)
            if (unreachableTimestamp and
                unreachableTimestamp > globalClock.getFrameTime()):
                continue

            result.append(toon)

        return result

    def requestOrders(self, brain):
        # A Suit brain is requesting orders. For now, we just attack a Toon at
        # random...

        attackables = self.getAttackableToons()

        if attackables:
            toonId = random.choice(attackables).doId
            brain.demand('Attack', toonId)
        else:
            pass # Below state not implemented yet.
            #brain.demand('Wander')

    def toonUnreachable(self, toonId):
        # A Cog couldn't get to a Toon to attack them.
        self._unreachables[toonId] = (globalClock.getFrameTime() +
                                      self.UNREACHABLE_TIMEOUT)
