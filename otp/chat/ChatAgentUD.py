from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
# TODO: OTP should not depend on Toontown... Hrrm.
from toontown.chat.TTWhiteList import TTWhiteList

class ChatAgentUD(DistributedObjectGlobalUD):
    notify = DirectNotifyGlobal.directNotify.newCategory("ChatAgentUD")

    def announceGenerate(self):
        DistributedObjectGlobalUD.announceGenerate(self)

        self.whiteList = TTWhiteList()

    def chatMessage(self, message):
        sender = self.air.getAvatarIdFromSender()
        if sender == 0:
            self.air.writeServerEvent('suspicious', accId=self.air.getAccountIdFromSender(),
                                         issue='Account sent chat without an avatar', message=message)
            return

        cleanMessage, modifications = self.cleanMessage(message)

        self.air.writeServerEvent('chat-said', avId=sender, msg=message, cleanMsg=cleanMessage)

        # TODO: The above is probably a little too ugly for my taste... Maybe AIR
        # should be given an API for sending updates for unknown objects?
        DistributedAvatar = self.air.dclassesByName['DistributedAvatarUD']
        dg = DistributedAvatar.aiFormatUpdate('setTalk', sender, sender,
                                              self.air.ourChannel,
                                              [0, 0, '', cleanMessage, modifications, 0])
        self.air.send(dg)

    def whisperMessage(self, receiverAvId, message):
        sender = self.air.getAvatarIdFromSender()
        if sender == 0:
            self.air.writeServerEvent('suspicious', accId=self.air.getAccountIdFromSender(),
                                         issue='Account sent chat without an avatar', message=message)
            return

        cleanMessage, modifications = self.cleanMessage(message)

        # Maybe a better "cleaner" way of doing this, but it works
        self.air.writeServerEvent('whisper-said', avId=sender, msg=message, cleanMsg=cleanMessage)
        DistributedAvatar = self.air.dclassesByName['DistributedAvatarUD']
        dg = DistributedAvatar.aiFormatUpdate('setTalkWhisper', receiverAvId, receiverAvId, self.air.ourChannel, 
                                            [sender, sender, '', cleanMessage, modifications, 0])
        self.air.send(dg)

    def cleanMessage(self, message):
        modifications = []
        words = message.split(' ')
        offset = 0
        WantWhitelist = self.air.config.GetBool('want-whitelist', True)
        for word in words:
            if word and not self.whiteList.isWord(word) and WantWhitelist:
                modifications.append((offset, offset+len(word)-1))
            offset += len(word) + 1

        cleanMessage = message
        for modStart, modStop in modifications:
            cleanMessage = cleanMessage[:modStart] + '*'*(modStop-modStart+1) + cleanMessage[modStop+1:]

        return (cleanMessage, modifications)
