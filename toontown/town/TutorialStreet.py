# 2013.08.22 22:26:53 Pacific Daylight Time
# Embedded file name: toontown.town.TutorialStreet
import TTStreet

class TutorialStreet(TTStreet.TTStreet):
    __module__ = __name__

    def enter(self, requestStatus):
        TTStreet.TTStreet.enter(self, requestStatus, visibilityFlag=0, arrowsOn=0)

    def exit(self):
        TTStreet.TTStreet.exit(self, visibilityFlag=0)

    def enterTeleportIn(self, requestStatus):
        TTStreet.TTStreet.enterTeleportIn(self, requestStatus)

    def enterTownBattle(self, event):
        self.loader.townBattle.enter(event, self.fsm.getStateNamed('battle'), tutorialFlag=1)

    def handleEnterTunnel(self, requestStatus, collEntry):
        messenger.send('stopTutorial')
        TTStreet.TTStreet.handleEnterTunnel(self, requestStatus, collEntry)

    def exitDoorIn(self):
        base.localAvatar.obscureMoveFurnitureButton(-1)
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\town\TutorialStreet.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:26:53 Pacific Daylight Time
