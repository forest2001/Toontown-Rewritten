# 2013.08.22 22:15:08 Pacific Daylight Time
# Embedded file name: otp.avatar.AvatarHandle


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
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\otp\avatar\AvatarHandle.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:15:08 Pacific Daylight Time
