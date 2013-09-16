# 2013.08.22 22:16:01 Pacific Daylight Time
# Embedded file name: toontown.ai.DistributedTrickOrTreatTarget
from direct.directnotify import DirectNotifyGlobal
from direct.distributed import DistributedObject
from otp.speedchat import SpeedChatGlobals
import DistributedScavengerHuntTarget

class DistributedTrickOrTreatTarget(DistributedScavengerHuntTarget.DistributedScavengerHuntTarget):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedTrickOrTreatTarget')

    def __init__(self, cr):
        DistributedScavengerHuntTarget.DistributedScavengerHuntTarget.__init__(self, cr)

    def phraseSaid(self, phraseId):
        self.notify.debug('Checking if phrase was said')
        helpPhrase = 10003

        def reset():
            self.triggered = False

        if phraseId == helpPhrase and not self.triggered:
            self.triggered = True
            self.attemptScavengerHunt()
            taskMgr.doMethodLater(self.triggerDelay, reset, 'ScavengerHunt-phrase-reset', extraArgs=[])
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\ai\DistributedTrickOrTreatTarget.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:16:01 Pacific Daylight Time
