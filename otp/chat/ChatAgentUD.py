from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
# TODO: OTP should not depend on Toontown... Hrrm.
from toontown.chat.TTWhiteList import TTWhiteList
from otp.distributed import OtpDoGlobals

class ChatAgentUD(DistributedObjectGlobalUD):
    notify = DirectNotifyGlobal.directNotify.newCategory("ChatAgentUD")

    def announceGenerate(self):
        DistributedObjectGlobalUD.announceGenerate(self)

        self.whiteList = TTWhiteList()
        self.chatMode2channel = {
            1 : OtpDoGlobals.OTP_MOD_CHANNEL,
            2 : OtpDoGlobals.OTP_ADMIN_CHANNEL,
            3 : OtpDoGlobals.OTP_SYSADMIN_CHANNEL,
        }
        self.chatMode2prefix = {
            1 : "[MOD] ",
            2 : "[ADMIN] ",
            3 : "[SYSADMIN] ",
        }
    # Open chat
    def chatMessage(self, message, chatMode):
        sender = self.air.getAvatarIdFromSender()
        if sender == 0:
            self.air.writeServerEvent('suspicious', accId=self.air.getAccountIdFromSender(),
                                         issue='Account sent chat without an avatar', message=message)
            return

        cleanMessage, modifications = self.cleanWhitelist(message)

        self.air.writeServerEvent('chat-said', avId=sender, chatMode=chatMode, msg=message, cleanMsg=cleanMessage)

        # TODO: The above is probably a little too ugly for my taste... Maybe AIR
        # should be given an API for sending updates for unknown objects?
        if chatMode != 0:
            # Staff messages do not need to be cleaned. [TODO: Blacklist this?]
            if message.startswith('.'):
                # This is a thought bubble, move the point to the start.
                cleanMessage = '.' + self.chatMode2prefix.get(chatMode, "") + message[1:]
            else:
                cleanMessage = self.chatMode2prefix.get(chatMode, "") + message
            modifications = []
        DistributedAvatar = self.air.dclassesByName['DistributedAvatarUD']
        dg = DistributedAvatar.aiFormatUpdate('setTalk', sender, self.chatMode2channel.get(chatMode, sender),
                                              self.air.ourChannel,
                                              [0, 0, '', cleanMessage, modifications, 0])
        self.air.send(dg)

    # Regular filtered chat
    def whisperMessage(self, receiverAvId, message):
        sender = self.air.getAvatarIdFromSender()
        if sender == 0:
            self.air.writeServerEvent('suspicious', accId=self.air.getAccountIdFromSender(),
                                         issue='Account sent chat without an avatar', message=message)
            return

        cleanMessage, modifications = self.cleanWhitelist(message)

        # Maybe a better "cleaner" way of doing this, but it works
        self.air.writeServerEvent('whisper-said', avId=sender, reciever=receiverAvId, msg=message, cleanMsg=cleanMessage)
        DistributedAvatar = self.air.dclassesByName['DistributedAvatarUD']
        dg = DistributedAvatar.aiFormatUpdate('setTalkWhisper', receiverAvId, receiverAvId, self.air.ourChannel,
                                            [sender, sender, '', cleanMessage, modifications, 0])
        self.air.send(dg)

    # True friend unfiltered chat
    def sfWhisperMessage(self, receiverAvId, message):
        sender = self.air.getAvatarIdFromSender()
        if sender == 0:
            self.air.writeServerEvent('suspicious', accId=self.air.getAccountIdFromSender(),
                                         issue='Account sent chat without an avatar', message=message)
            return

        cleanMessage = self.cleanBlacklist(message)

        self.air.writeServerEvent('sf-whisper-said', avId=sender, reciever=receiverAvId, msg=message, cleanMsg=cleanMessage)
        DistributedAvatar = self.air.dclassesByName['DistributedAvatarUD']
        dg = DistributedAvatar.aiFormatUpdate('setTalkWhisper', receiverAvId, receiverAvId, self.air.ourChannel,
                                            [sender, sender, '', cleanMessage, [], 0])
        self.air.send(dg)

    # Filter the chat message
    def cleanWhitelist(self, message):
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

    # Check the black list for black-listed words
    def cleanBlacklist(self, message):
        # We don't have a black list so we just return the full message
        return message
