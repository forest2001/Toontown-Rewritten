from direct.distributed import DistributedObject
from direct.directnotify import DirectNotifyGlobal
from otp.ai.MagicWordGlobal import *
from otp.nametag.NametagConstants import *

class MagicWordManager(DistributedObject.DistributedObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('MagicWordManager')
    neverDisable = 1

    def generate(self):
        DistributedObject.DistributedObject.generate(self)
        self.accept('magicWord', self.handleMagicWord)

    def disable(self):
        self.ignore('magicWord')
        DistributedObject.DistributedObject.disable(self)

    def handleMagicWord(self, magicWord):
        if not self.cr.wantMagicWords:
            return

        if magicWord.startswith('~~'):
            # TODO: Target selected avatar.
            target = base.localAvatar
            magicWord = magicWord[2:]
        if magicWord.startswith('~'):
            target = base.localAvatar
            magicWord = magicWord[1:]

        targetId = target.doId
        self.sendUpdate('sendMagicWord', [magicWord, targetId])
        if target == base.localAvatar:
            response = spellbook.process(base.localAvatar, targetId, target, magicWord)
            if response:
                self.sendMagicWordResponse(response)

    def sendMagicWordResponse(self, response):
        self.notify.info(response)
        base.localAvatar.setChatAbsolute(response, CFSpeech | CFTimeout)
        base.talkAssistant.receiveDeveloperMessage(response)
