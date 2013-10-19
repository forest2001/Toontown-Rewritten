from toontown.safezone.DistributedTrolleyAI import DistributedTrolleyAI

class HoodAI:
    """
    AI-side representation of everything in a single neighborhood.

    One subclass of this class exists for every neighborhood in the game.
    HoodAIs are responsible for spawning all TreasurePlanners, SuitPlanners,
    ponds, and other safezone objects, etc.
    """

    SAFEZONE = None

    def __init__(self, air):
        self.air = air

        self.safezone = self.SAFEZONE

        self.trolley = None

    def createTrolley(self):
        self.trolley = DistributedTrolleyAI(self.air)
        self.trolley.generateWithRequired(self.safezone)
