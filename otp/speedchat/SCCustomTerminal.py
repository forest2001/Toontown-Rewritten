# 2013.08.22 22:15:47 Pacific Daylight Time
# Embedded file name: otp.speedchat.SCCustomTerminal
from SCTerminal import SCTerminal
from otp.otpbase.OTPLocalizer import CustomSCStrings
SCCustomMsgEvent = 'SCCustomMsg'

def decodeSCCustomMsg(textId):
    return CustomSCStrings.get(textId, None)


class SCCustomTerminal(SCTerminal):
    __module__ = __name__

    def __init__(self, textId):
        SCTerminal.__init__(self)
        self.textId = textId
        self.text = CustomSCStrings[self.textId]

    def handleSelect(self):
        SCTerminal.handleSelect(self)
        messenger.send(self.getEventName(SCCustomMsgEvent), [self.textId])
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\otp\speedchat\SCCustomTerminal.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:15:47 Pacific Daylight Time
