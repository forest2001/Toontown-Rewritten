# 2013.08.22 22:25:10 Pacific Daylight Time
# Embedded file name: toontown.speedchat.TTSCSillyPhaseFiveMenu
from direct.showbase import PythonUtil
from otp.speedchat.SCMenu import SCMenu
from otp.speedchat.SCMenuHolder import SCMenuHolder
from otp.speedchat.SCStaticTextTerminal import SCStaticTextTerminal
from otp.otpbase import OTPLocalizer
SillyPhaseFiveMenu = [(OTPLocalizer.SillyHolidayMenuSections[1], [30325, 30326, 30327]), (OTPLocalizer.SillyHolidayMenuSections[2], [30328,
   30329,
   30330,
   30331,
   30332])]

class TTSCSillyPhaseFiveMenu(SCMenu):
    __module__ = __name__

    def __init__(self):
        SCMenu.__init__(self)
        self.__SillyPhaseFiveMessagesChanged()
        submenus = []

    def destroy(self):
        SCMenu.destroy(self)

    def clearMenu(self):
        SCMenu.clearMenu(self)

    def __SillyPhaseFiveMessagesChanged(self):
        self.clearMenu()
        try:
            lt = base.localAvatar
        except:
            return

        for section in SillyPhaseFiveMenu:
            if section[0] == -1:
                for phrase in section[1]:
                    if phrase not in OTPLocalizer.SpeedChatStaticText:
                        print 'warning: tried to link Silly PhaseFive phrase %s which does not seem to exist' % phrase
                        break
                    self.append(SCStaticTextTerminal(phrase))

            else:
                menu = SCMenu()
                for phrase in section[1]:
                    if phrase not in OTPLocalizer.SpeedChatStaticText:
                        print 'warning: tried to link Silly PhaseFive phrase %s which does not seem to exist' % phrase
                        break
                    menu.append(SCStaticTextTerminal(phrase))

                menuName = str(section[0])
                self.append(SCMenuHolder(menuName, menu))
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\speedchat\TTSCSillyPhaseFiveMenu.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:25:10 Pacific Daylight Time
