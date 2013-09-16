# 2013.08.22 22:15:48 Pacific Daylight Time
# Embedded file name: otp.speedchat.SCGMTextTerminal
from SCTerminal import SCTerminal
from otp.speedchat import SpeedChatGMHandler
SCGMTextMsgEvent = 'SCGMTextMsg'

class SCGMTextTerminal(SCTerminal):
    __module__ = __name__

    def __init__(self, textId):
        SCTerminal.__init__(self)
        gmHandler = SpeedChatGMHandler.SpeedChatGMHandler()
        self.textId = textId
        self.text = gmHandler.getPhrase(textId)

    def handleSelect(self):
        SCTerminal.handleSelect(self)
        messenger.send(self.getEventName(SCGMTextMsgEvent), [self.textId])
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\otp\speedchat\SCGMTextTerminal.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:15:48 Pacific Daylight Time
