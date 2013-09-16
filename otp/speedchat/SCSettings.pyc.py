# 2013.08.22 22:15:49 Pacific Daylight Time
# Embedded file name: otp.speedchat.SCSettings
from SCColorScheme import SCColorScheme
from otp.otpbase import OTPLocalizer

class SCSettings():
    __module__ = __name__

    def __init__(self, eventPrefix, whisperMode = 0, colorScheme = None, submenuOverlap = OTPLocalizer.SCOsubmenuOverlap, topLevelOverlap = None):
        self.eventPrefix = eventPrefix
        self.whisperMode = whisperMode
        if colorScheme is None:
            colorScheme = SCColorScheme()
        self.colorScheme = colorScheme
        self.submenuOverlap = submenuOverlap
        self.topLevelOverlap = topLevelOverlap
        return
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\otp\speedchat\SCSettings.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:15:49 Pacific Daylight Time
