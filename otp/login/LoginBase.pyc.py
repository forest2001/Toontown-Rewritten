# 2013.08.22 22:15:37 Pacific Daylight Time
# Embedded file name: otp.login.LoginBase


class LoginBase():
    __module__ = __name__
    freeTimeExpires = -1

    def __init__(self, cr):
        self.cr = cr

    def sendLoginMsg(self, loginName, password, createFlag):
        pass

    def getErrorCode(self):
        return 0

    def needToSetParentPassword(self):
        return 0
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\otp\login\LoginBase.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:15:37 Pacific Daylight Time
