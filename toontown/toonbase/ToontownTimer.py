# 2013.08.22 22:26:36 Pacific Daylight Time
# Embedded file name: toontown.toonbase.ToontownTimer
from otp.otpbase.OTPTimer import OTPTimer
from pandac.PandaModules import *

class ToontownTimer(OTPTimer):
    __module__ = __name__

    def __init__(self, useImage = True, highlightNearEnd = True):
        OTPTimer.__init__(self, useImage, highlightNearEnd)
        self.initialiseoptions(ToontownTimer)

    def getImage(self):
        if ToontownTimer.ClockImage == None:
            model = loader.loadModel('phase_3.5/models/gui/clock_gui')
            ToontownTimer.ClockImage = model.find('**/alarm_clock')
            model.removeNode()
        return ToontownTimer.ClockImage
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\toonbase\ToontownTimer.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:26:36 Pacific Daylight Time
