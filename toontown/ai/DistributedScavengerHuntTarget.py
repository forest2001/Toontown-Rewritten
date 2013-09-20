# 2013.08.22 22:16:00 Pacific Daylight Time
# Embedded file name: toontown.ai.DistributedScavengerHuntTarget
from direct.directnotify import DirectNotifyGlobal
from direct.distributed import DistributedObject
from otp.speedchat import SpeedChatGlobals

class DistributedScavengerHuntTarget(DistributedObject.DistributedObject):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedScavengerHuntTarget')

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)

    def setupListenerDetails(self):
        self.triggered = False
        self.triggerDelay = 15
        self.accept(SpeedChatGlobals.SCCustomMsgEvent, self.phraseSaid)

    def phraseSaid(self, phraseId):
        self.notify.debug('Checking if phrase was said')
        helpPhrase = 10003

        def reset():
            self.triggered = False

        if phraseId == helpPhrase and not self.triggered:
            self.triggered = True
            self.attemptScavengerHunt()
            taskMgr.doMethodLater(self.triggerDelay, reset, 'ScavengerHunt-phrase-reset', extraArgs=[])

    def announceGenerate(self):
        DistributedObject.DistributedObject.announceGenerate(self)
        DistributedScavengerHuntTarget.notify.debug('announceGenerate')
        self.setupListenerDetails()

    def delete(self):
        self.ignoreAll()
        taskMgr.remove('ScavengerHunt-phrase-reset')
        DistributedObject.DistributedObject.delete(self)

    def attemptScavengerHunt(self):
        DistributedScavengerHuntTarget.notify.debug('attempScavengerHunt')
        self.sendUpdate('attemptScavengerHunt', [])
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\ai\DistributedScavengerHuntTarget.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:16:01 Pacific Daylight Time
