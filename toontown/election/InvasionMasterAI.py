import random

class InvasionMasterAI:
    def __init__(self, invasion):
        self.invasion = invasion

    def requestOrders(self, brain):
        # A Suit brain is requesting orders. For now, we just attack a Toon at
        # random...
        if not self.invasion.toons:
            pass # No Toons in area, let Suits idle for the rest of time.

        toonId = random.choice(self.invasion.toons).doId
        brain.demand('Attack', toonId)

    def toonUnreachable(self, toonId):
        # A Cog couldn't get to a Toon to attack them.
        pass
