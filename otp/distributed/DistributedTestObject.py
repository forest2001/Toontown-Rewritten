# 2013.08.22 22:15:16 Pacific Daylight Time
# Embedded file name: otp.distributed.DistributedTestObject
from direct.distributed import DistributedObject

class DistributedTestObject(DistributedObject.DistributedObject):
    __module__ = __name__

    def setRequiredField(self, r):
        self.requiredField = r

    def setB(self, B):
        self.B = B

    def setBA(self, BA):
        self.BA = BA

    def setBO(self, BO):
        self.BO = BO

    def setBR(self, BR):
        self.BR = BR

    def setBRA(self, BRA):
        self.BRA = BRA

    def setBRO(self, BRO):
        self.BRO = BRO

    def setBROA(self, BROA):
        self.BROA = BROA

    def gotNonReqThatWasntSet(self):
        for field in ('B', 'BA', 'BO', 'BR', 'BRA', 'BRO', 'BROA'):
            if hasattr(self, field):
                return True

        return False
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\otp\distributed\DistributedTestObject.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:15:16 Pacific Daylight Time
