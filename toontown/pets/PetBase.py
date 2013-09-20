# 2013.08.22 22:23:50 Pacific Daylight Time
# Embedded file name: toontown.pets.PetBase
from toontown.pets.PetConstants import AnimMoods
from toontown.pets import PetMood
import string

class PetBase():
    __module__ = __name__

    def getSetterName(self, valueName, prefix = 'set'):
        return '%s%s%s' % (prefix, string.upper(valueName[0]), valueName[1:])

    def getAnimMood(self):
        if self.mood.getDominantMood() in PetMood.PetMood.ExcitedMoods:
            return AnimMoods.EXCITED
        elif self.mood.getDominantMood() in PetMood.PetMood.UnhappyMoods:
            return AnimMoods.SAD
        else:
            return AnimMoods.NEUTRAL

    def isExcited(self):
        return self.getAnimMood() == AnimMoods.EXCITED

    def isSad(self):
        return self.getAnimMood() == AnimMoods.SAD
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\pets\PetBase.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:23:50 Pacific Daylight Time
