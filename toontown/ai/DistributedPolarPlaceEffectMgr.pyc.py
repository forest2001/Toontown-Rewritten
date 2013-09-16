# 2013.08.22 22:16:00 Pacific Daylight Time
# Embedded file name: toontown.ai.DistributedPolarPlaceEffectMgr
from direct.directnotify import DirectNotifyGlobal
from direct.distributed import DistributedObject
from direct.interval.IntervalGlobal import *
from otp.speedchat import SpeedChatGlobals
from toontown.toonbase import TTLocalizer

class DistributedPolarPlaceEffectMgr(DistributedObject.DistributedObject):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPolarPlaceEffectMgr')

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)

        def phraseSaid(phraseId):
            helpPhrase = 104
            if phraseId == helpPhrase:
                self.addPolarPlaceEffect()

        self.accept(SpeedChatGlobals.SCStaticTextMsgEvent, phraseSaid)

    def announceGenerate(self):
        DistributedObject.DistributedObject.announceGenerate(self)
        DistributedPolarPlaceEffectMgr.notify.debug('announceGenerate')

    def delete(self):
        self.ignore(SpeedChatGlobals.SCStaticTextMsgEvent)
        DistributedObject.DistributedObject.delete(self)

    def addPolarPlaceEffect(self):
        DistributedPolarPlaceEffectMgr.notify.debug('addResitanceEffect')
        av = base.localAvatar
        self.sendUpdate('addPolarPlaceEffect', [])
        msgTrack = Sequence(Func(av.setSystemMessage, 0, TTLocalizer.PolarPlaceEffect1), Wait(2), Func(av.setSystemMessage, 0, TTLocalizer.PolarPlaceEffect2), Wait(4), Func(av.setSystemMessage, 0, TTLocalizer.PolarPlaceEffect3))
        msgTrack.start()
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\ai\DistributedPolarPlaceEffectMgr.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:16:00 Pacific Daylight Time
