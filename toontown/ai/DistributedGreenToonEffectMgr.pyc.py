# 2013.08.22 22:16:00 Pacific Daylight Time
# Embedded file name: toontown.ai.DistributedGreenToonEffectMgr
from direct.directnotify import DirectNotifyGlobal
from direct.distributed import DistributedObject
from direct.interval.IntervalGlobal import *
from otp.speedchat import SpeedChatGlobals
from toontown.toonbase import TTLocalizer

class DistributedGreenToonEffectMgr(DistributedObject.DistributedObject):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedGreenToonEffectMgr')

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)

        def phraseSaid(phraseId):
            greenPhrase = 30450
            if phraseId == greenPhrase:
                self.addGreenToonEffect()

        self.accept(SpeedChatGlobals.SCStaticTextMsgEvent, phraseSaid)

    def announceGenerate(self):
        DistributedObject.DistributedObject.announceGenerate(self)
        DistributedGreenToonEffectMgr.notify.debug('announceGenerate')

    def delete(self):
        self.ignore(SpeedChatGlobals.SCStaticTextMsgEvent)
        DistributedObject.DistributedObject.delete(self)

    def addGreenToonEffect(self):
        DistributedGreenToonEffectMgr.notify.debug('addGreenToonEffect')
        av = base.localAvatar
        self.sendUpdate('addGreenToonEffect', [])
        msgTrack = Sequence(Func(av.setSystemMessage, 0, TTLocalizer.GreenToonEffectMsg))
        msgTrack.start()
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\ai\DistributedGreenToonEffectMgr.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:16:00 Pacific Daylight Time
