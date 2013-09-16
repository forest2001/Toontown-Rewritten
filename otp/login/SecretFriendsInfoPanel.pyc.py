# 2013.08.22 22:15:40 Pacific Daylight Time
# Embedded file name: otp.login.SecretFriendsInfoPanel
from pandac.PandaModules import *
from otp.otpbase.OTPGlobals import *
from direct.gui.DirectGui import *
from MultiPageTextFrame import *
from otp.otpbase import OTPLocalizer
from otp.otpgui import OTPDialog

class SecretFriendsInfoPanel(getGlobalDialogClass()):
    __module__ = __name__

    def __init__(self, doneEvent, hidePageNum = 0, pageChangeCallback = None):
        dialogClass = getGlobalDialogClass()
        dialogClass.__init__(self, parent=aspect2d, dialogName='secretFriendsInfoDialog', doneEvent=doneEvent, okButtonText=OTPLocalizer.SecretFriendsInfoPanelClose, style=OTPDialog.Acknowledge, text='', topPad=1.5, sidePad=1.2, pos=(0, 0, 0.1), scale=0.9)
        self.textPanel = MultiPageTextFrame(parent=self, textList=OTPLocalizer.SecretFriendsInfoPanelText, hidePageNum=hidePageNum, pageChangeCallback=pageChangeCallback)
        self['image'] = self['image']
        self['image_pos'] = (0, 0, -0.1)
        self['image_scale'] = (2, 1, 1.3)
        closeButton = self.getChild(0)
        closeButton.setZ(-0.56)
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\otp\login\SecretFriendsInfoPanel.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:15:40 Pacific Daylight Time
