# 2013.08.22 22:16:01 Pacific Daylight Time
# Embedded file name: toontown.ai.DistributedWinterCarolingTarget
from direct.directnotify import DirectNotifyGlobal
from direct.distributed import DistributedObject
from toontown.speedchat.TTSCIndexedTerminal import TTSCIndexedMsgEvent
import DistributedScavengerHuntTarget

class DistributedWinterCarolingTarget(DistributedScavengerHuntTarget.DistributedScavengerHuntTarget):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedWinterCarolingTarget')

    def __init__(self, cr):
        DistributedScavengerHuntTarget.DistributedScavengerHuntTarget.__init__(self, cr)

    def setupListenerDetails(self):
        self.triggered = False
        self.triggerDelay = 15
        self.accept(TTSCIndexedMsgEvent, self.phraseSaid)

    def phraseSaid(self, phraseId):
        self.notify.debug('Checking if phrase was said')
        helpPhrases = []
        for i in range(6):
            helpPhrases.append(30220 + i)

        def reset():
            self.triggered = False

        if phraseId in helpPhrases and not self.triggered:
            self.triggered = True
            self.attemptScavengerHunt()
            taskMgr.doMethodLater(self.triggerDelay, reset, 'ScavengerHunt-phrase-reset', extraArgs=[])
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\ai\DistributedWinterCarolingTarget.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:16:01 Pacific Daylight Time
