from direct.distributed import DistributedObject
from direct.directnotify import DirectNotifyGlobal
from otp.ai.MagicWordGlobal import *
from otp.nametag.NametagConstants import *

lastClickedNametag = None

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
            if lastClickedNametag == None:
                target = base.localAvatar
            else:
                target = lastClickedNametag
            magicWord = magicWord[2:]
        if magicWord.startswith('~'):
            target = base.localAvatar
            magicWord = magicWord[1:]

        targetId = target.doId
        if target == base.localAvatar:
            response = spellbook.process(base.localAvatar, target, magicWord) # Packed as (response, foundMagicWord)
            if response[1]:
                # Magic word found!
                if response[0]:
                    self.sendMagicWordResponse(response[0])
                self.sendUpdate('sendMagicWord', [magicWord, targetId, False])
            else:
                # Client's spellbook has no idea about this MW. Tell the AI to execute.
                self.sendUpdate('sendMagicWord', [magicWord, targetId, True])

    def sendMagicWordResponse(self, response):
        self.notify.info(response)
        base.localAvatar.setSystemMessage(0, 'Spellbook: ' + str(response))
