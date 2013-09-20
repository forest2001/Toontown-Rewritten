# 2013.08.22 22:26:47 Pacific Daylight Time
# Embedded file name: toontown.toontowngui.TTDialog
from otp.otpgui.OTPDialog import *

class TTDialog(OTPDialog):
    __module__ = __name__

    def __init__(self, parent = None, style = NoButtons, **kw):
        self.path = 'phase_3/models/gui/dialog_box_buttons_gui'
        OTPDialog.__init__(self, parent, style, **kw)
        self.initialiseoptions(TTDialog)


class TTGlobalDialog(GlobalDialog):
    __module__ = __name__

    def __init__(self, message = '', doneEvent = None, style = NoButtons, okButtonText = OTPLocalizer.DialogOK, cancelButtonText = OTPLocalizer.DialogCancel, **kw):
        self.path = 'phase_3/models/gui/dialog_box_buttons_gui'
        GlobalDialog.__init__(self, message, doneEvent, style, okButtonText, cancelButtonText, **kw)
        self.initialiseoptions(TTGlobalDialog)
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\toontowngui\TTDialog.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:26:47 Pacific Daylight Time
