# 2013.08.22 22:15:37 Pacific Daylight Time
# Embedded file name: otp.login.LoginDISLTokenAccount
from direct.showbase.ShowBaseGlobal import *
from direct.distributed.MsgTypes import *
from direct.directnotify import DirectNotifyGlobal
import LoginBase
from direct.distributed.PyDatagram import PyDatagram

class LoginDISLTokenAccount(LoginBase.LoginBase):
    __module__ = __name__

    def __init__(self, cr):
        LoginBase.LoginBase.__init__(self, cr)

    def supportsRelogin(self):
        return 0

    def authorize(self, loginName, password):
        self.loginName = loginName
        self.DISLToken = password

    def sendLoginMsg(self):
        cr = self.cr
        datagram = PyDatagram()
        datagram.addUint16(CLIENT_LOGIN_3)
        datagram.addString(self.DISLToken)
        datagram.addString(cr.serverVersion)
        datagram.addUint32(cr.hashVal)
        datagram.addInt32(CLIENT_LOGIN_3_DISL_TOKEN)
        datagram.addString(cr.validateDownload)
        datagram.addString(cr.wantMagicWords)
        cr.send(datagram)

    def supportsParentPassword(self):
        return 0

    def supportsAuthenticateDelete(self):
        return 0
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\otp\login\LoginDISLTokenAccount.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:15:37 Pacific Daylight Time
