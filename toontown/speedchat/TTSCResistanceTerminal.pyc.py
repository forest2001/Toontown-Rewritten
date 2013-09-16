# 2013.08.22 22:25:09 Pacific Daylight Time
# Embedded file name: toontown.speedchat.TTSCResistanceTerminal
from otp.speedchat.SCTerminal import SCTerminal
from toontown.chat import ResistanceChat
TTSCResistanceMsgEvent = 'TTSCResistanceMsg'

def decodeTTSCResistanceMsg(textId):
    return ResistanceChat.getChatText(textId)


class TTSCResistanceTerminal(SCTerminal):
    __module__ = __name__

    def __init__(self, textId, charges):
        SCTerminal.__init__(self)
        self.setCharges(charges)
        self.textId = textId
        self.text = ResistanceChat.getItemText(self.textId)

    def isWhisperable(self):
        return False

    def handleSelect(self):
        SCTerminal.handleSelect(self)
        messenger.send(self.getEventName(TTSCResistanceMsgEvent), [self.textId])
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\speedchat\TTSCResistanceTerminal.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:25:09 Pacific Daylight Time
