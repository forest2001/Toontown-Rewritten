# 2013.08.22 22:21:11 Pacific Daylight Time
# Embedded file name: toontown.makeatoon.TTPickANamePattern
from direct.showbase.PythonUtil import listToItem2index
from otp.namepanel.PickANamePattern import PickANamePatternTwoPartLastName
from toontown.makeatoon.NameGenerator import NameGenerator
import types

class TTPickANamePattern(PickANamePatternTwoPartLastName):
    __module__ = __name__
    NameParts = None
    LastNamePrefixesCapped = None

    def _getNameParts(self, gender):
        if TTPickANamePattern.NameParts is None:
            TTPickANamePattern.NameParts = {}
            ng = NameGenerator()
            TTPickANamePattern.NameParts['m'] = ng.getMaleNameParts()
            TTPickANamePattern.NameParts['f'] = ng.getFemaleNameParts()
        return TTPickANamePattern.NameParts[gender]

    def _getLastNameCapPrefixes(self):
        if TTPickANamePattern.LastNamePrefixesCapped is None:
            ng = NameGenerator()
            TTPickANamePattern.LastNamePrefixesCapped = ng.getLastNamePrefixesCapped()[:]
        return TTPickANamePattern.LastNamePrefixesCapped
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\makeatoon\TTPickANamePattern.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:21:11 Pacific Daylight Time
