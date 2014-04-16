from direct.interval.IntervalGlobal import *
from otp.ai.MagicWordGlobal import *
from AlphaCredits import *

class CreditsSequence:
    def __init__(self):
        self.loaded = False
        self.interval = None

        self.creditsScenes = [
            # Developers
            Shockley(),
            SirMax(),
            FatMcStink(),
            McQuack(),
            Hawkheart(),
            TooManySecrets(),
            MuddyPaws(),
            Hamlet()
            # Artists
            ]

    def load(self):
        if self.loaded:
            return

        for scene in self.creditsScenes:
            scene.load()

        self.loaded = True

    def unload(self):
        if not self.loaded:
            return

        for scene in self.creditsScenes:
            scene.unload()

        self.loaded = False

    def enter(self):
        # Begin playing the credits sequence.
        if self.interval:
            return # Already playing!

        if not self.loaded:
            self.load()

        self.interval = Sequence()
        for scene in self.creditsScenes:
            self.interval.append(scene.makeInterval())
        self.interval.start()

    def exit(self):
        if self.interval:
            self.interval.finish()
            self.interval = None

@magicWord()
def rollCredits():
    """Request that the credits sequence play back.

    This will disconnect you.
    """

    taskMgr.doMethodLater(0.1, base.cr.loginFSM.request,
                          'rollCredits-magic-word',
                          extraArgs=['credits'])
