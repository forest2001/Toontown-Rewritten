from SCColorScheme import SCColorScheme
from otp.otpbase import OTPLocalizer

class SCSettings:
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
