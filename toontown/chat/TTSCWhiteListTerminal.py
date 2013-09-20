# 2013.08.22 22:17:25 Pacific Daylight Time
# Embedded file name: toontown.chat.TTSCWhiteListTerminal
from otp.speedchat.SCTerminal import SCTerminal
from otp.otpbase.OTPLocalizer import SpeedChatStaticText
SCStaticTextMsgEvent = 'SCStaticTextMsg'

def decodeSCStaticTextMsg(textId):
    return SpeedChatStaticText.get(textId, None)


class TTSCWhiteListTerminal(SCTerminal):
    __module__ = __name__

    def __init__(self, textId, parentMenu = None):
        SCTerminal.__init__(self)
        self.parentClass = parentMenu
        self.textId = textId
        self.text = SpeedChatStaticText[self.textId]
        print 'SpeedText %s %s' % (self.textId, self.text)

    def handleSelect(self):
        SCTerminal.handleSelect(self)
        if not self.parentClass.whisperAvatarId:
            base.localAvatar.chatMgr.fsm.request('whiteListOpenChat')
        elif self.parentClass.toPlayer:
            base.localAvatar.chatMgr.fsm.request('whiteListPlayerChat', [self.parentClass.whisperAvatarId])
        else:
            base.localAvatar.chatMgr.fsm.request('whiteListAvatarChat', [self.parentClass.whisperAvatarId])
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\chat\TTSCWhiteListTerminal.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:17:25 Pacific Daylight Time
