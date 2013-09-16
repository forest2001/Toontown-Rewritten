# 2013.08.22 22:25:11 Pacific Daylight Time
# Embedded file name: toontown.speedchat.TTSCSingingTerminal
from otp.speedchat.SCTerminal import SCTerminal
from otp.otpbase.OTPLocalizer import SpeedChatStaticText
TTSCSingingMsgEvent = 'SCSingingMsg'

def decodeSCStaticTextMsg(textId):
    return SpeedChatStaticText.get(textId, None)


class TTSCSingingTerminal(SCTerminal):
    __module__ = __name__

    def __init__(self, textId):
        SCTerminal.__init__(self)
        self.textId = textId
        self.text = SpeedChatStaticText[self.textId]

    def handleSelect(self):
        SCTerminal.handleSelect(self)
        messenger.send(self.getEventName(TTSCSingingMsgEvent), [self.textId])

    def finalize(self):
        args = {'rolloverSound': None,
         'clickSound': None}
        SCTerminal.finalize(self, args)
        return
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\speedchat\TTSCSingingTerminal.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:25:11 Pacific Daylight Time
