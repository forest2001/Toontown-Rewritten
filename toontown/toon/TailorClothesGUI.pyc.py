# 2013.08.22 22:26:16 Pacific Daylight Time
# Embedded file name: toontown.toon.TailorClothesGUI
from toontown.makeatoon import ClothesGUI
import ToonDNA

class TailorClothesGUI(ClothesGUI.ClothesGUI):
    __module__ = __name__
    notify = directNotify.newCategory('MakeClothesGUI')

    def __init__(self, doneEvent, swapEvent, tailorId):
        ClothesGUI.ClothesGUI.__init__(self, ClothesGUI.CLOTHES_TAILOR, doneEvent, swapEvent)
        self.tailorId = tailorId

    def setupScrollInterface(self):
        self.dna = self.toon.getStyle()
        gender = self.dna.getGender()
        if self.swapEvent != None:
            self.tops = ToonDNA.getTops(gender, tailorId=self.tailorId)
            self.bottoms = ToonDNA.getBottoms(gender, tailorId=self.tailorId)
            self.gender = gender
            self.topChoice = -1
            self.bottomChoice = -1
        self.setupButtons()
        return
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\toon\TailorClothesGUI.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:26:16 Pacific Daylight Time
