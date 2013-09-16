# 2013.08.22 22:25:09 Pacific Daylight Time
# Embedded file name: toontown.speedchat.TTSCIndexedTerminal
from otp.speedchat.SCTerminal import *
from otp.otpbase.OTPLocalizer import SpeedChatStaticText
TTSCIndexedMsgEvent = 'SCIndexedMsg'

def decodeTTSCIndexedMsg(msgIndex):
    return SpeedChatStaticText.get(msgIndex, None)


class TTSCIndexedTerminal(SCTerminal):
    __module__ = __name__

    def __init__(self, msg, msgIndex):
        SCTerminal.__init__(self)
        self.text = msg
        self.msgIndex = msgIndex

    def handleSelect(self):
        SCTerminal.handleSelect(self)
        messenger.send(self.getEventName(TTSCIndexedMsgEvent), [self.msgIndex])
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\speedchat\TTSCIndexedTerminal.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:25:09 Pacific Daylight Time
