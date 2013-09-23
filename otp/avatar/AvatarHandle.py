

class AvatarHandle():
    __module__ = __name__
    dclassName = 'AvatarHandle'

    def getName(self):
        if __dev__:
            pass
        return ''

    def isOnline(self):
        if __dev__:
            pass
        return False

    def isUnderstandable(self):
        if __dev__:
            pass
        return True

    def setTalkWhisper(self, fromAV, fromAC, avatarName, chat, mods, flags):
        newText, scrubbed = localAvatar.scrubTalk(chat, mods)
        base.talkAssistant.receiveWhisperTalk(fromAV, avatarName, fromAC, None, self.avatarId, self.getName(), newText, scrubbed)
        return
