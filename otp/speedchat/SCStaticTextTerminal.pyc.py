# 2013.08.22 22:15:49 Pacific Daylight Time
# Embedded file name: otp.speedchat.SCStaticTextTerminal
from SCTerminal import SCTerminal
from otp.otpbase.OTPLocalizer import SpeedChatStaticText
SCStaticTextMsgEvent = 'SCStaticTextMsg'

def decodeSCStaticTextMsg(textId):
    return SpeedChatStaticText.get(textId, None)


class SCStaticTextTerminal(SCTerminal):
    __module__ = __name__

    def __init__(self, textId):
        SCTerminal.__init__(self)
        self.textId = textId
        self.text = SpeedChatStaticText[self.textId]

    def handleSelect(self):
        SCTerminal.handleSelect(self)
        messenger.send(self.getEventName(SCStaticTextMsgEvent), [self.textId])
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\otp\speedchat\SCStaticTextTerminal.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:15:49 Pacific Daylight Time
