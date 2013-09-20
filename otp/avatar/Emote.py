# 2013.08.22 22:15:10 Pacific Daylight Time
# Embedded file name: otp.avatar.Emote
from otp.otpbase import OTPLocalizer
import types

class Emote():
    __module__ = __name__
    EmoteClear = -1
    EmoteEnableStateChanged = 'EmoteEnableStateChanged'

    def __init__(self):
        self.emoteFunc = None
        return

    def isEnabled(self, index):
        if isinstance(index, types.StringType):
            index = OTPLocalizer.EmoteFuncDict[index]
        if self.emoteFunc == None:
            return 0
        elif self.emoteFunc[index][1] == 0:
            return 1
        return 0


globalEmote = None
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\otp\avatar\Emote.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:15:10 Pacific Daylight Time
