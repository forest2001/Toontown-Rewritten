from direct.interval.IntervalGlobal import *
from otp.ai.MagicWordGlobal import *

class CreditsSequence:
    def __init__(self, sequence):
        self.loaded = False
        self.sequence = sequence # So we can load different types of sequences
        self.interval = None

        if sequence == 'alpha':
            from AlphaCredits import *
            self.creditsScenes = [
                # Developers
                Shockley(),
                Credits('Sir Max', 'Team Lead\nCommunity Manager\nWriter\nDeveloper', '10-29-13_cannon.jpg', 'Left'),
                Credits('Fat McStink', 'Server Administraitor\nWeb Backend Development\nDeveloper', '11-8-13_pieornot.jpg', 'Right'),
                Credits('McQuack', 'Expert of Explosives\nDeveloper\nAstron Team', '12-28-13-hiatus.jpg', 'Right'),
                Credits('Hawkheart', 'Fish Bingo Controller\nDeveloper', '11-11-13_bingo.jpg', 'Left'),
                Credits('Hamlet', 'Astron Team\nDeveloper', 'hamlet.jpg', 'Left'),
                Credits('Muddy Paws', 'Expert Cake Maker\nDeveloper\nMac Team', 'muddy-paws.jpg', 'Right'),
                Credits('Goshi', 'Support Manager\nModerator', '14-4-1_itsabirthdefect-nothingsilly.jpg', 'Right'),
                Credits('Too Many Secrets', 'Many Secret Things\nDeveloper', 'toomanysecrets.jpg', 'Left'),
                ]
        elif sequence == 'beta':
            # For when beta comes around
            pass

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
