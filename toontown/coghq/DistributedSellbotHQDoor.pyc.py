# 2013.08.22 22:18:52 Pacific Daylight Time
# Embedded file name: toontown.coghq.DistributedSellbotHQDoor
from direct.directnotify import DirectNotifyGlobal
from toontown.coghq import DistributedCogHQDoor
from toontown.toonbase import TTLocalizer
import CogDisguiseGlobals

class DistributedSellbotHQDoor(DistributedCogHQDoor.DistributedCogHQDoor):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedSellbotHQDoor')

    def __init__(self, cr):
        DistributedCogHQDoor.DistributedCogHQDoor.__init__(self, cr)

    def informPlayer(self, suitType):
        self.notify.debugStateCall(self)
        if suitType == CogDisguiseGlobals.suitTypes.NoSuit:
            popupMsg = TTLocalizer.SellbotRentalSuitMessage
        elif suitType == CogDisguiseGlobals.suitTypes.NoMerits:
            popupMsg = TTLocalizer.SellbotCogSuitNoMeritsMessage
        elif suitType == CogDisguiseGlobals.suitTypes.FullSuit:
            popupMsg = TTLocalizer.SellbotCogSuitHasMeritsMessage
        else:
            popupMsg = TTLocalizer.FADoorCodes_SB_DISGUISE_INCOMPLETE
        localAvatar.elevatorNotifier.showMeWithoutStopping(popupMsg, pos=(0, 0, 0.26), ttDialog=True)
        localAvatar.elevatorNotifier.setOkButton()
        localAvatar.elevatorNotifier.doneButton.setZ(-0.3)
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\coghq\DistributedSellbotHQDoor.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:18:52 Pacific Daylight Time
