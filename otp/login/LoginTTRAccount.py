from pandac.PandaModules import *
from direct.distributed.MsgTypes import *
from direct.directnotify import DirectNotifyGlobal
import LoginBase
from direct.distributed.PyDatagram import PyDatagram

# TODO: Get rid of this once the def is in direct...
CLIENT_HELLO = 1

class LoginTTRAccount(LoginBase.LoginBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('LoginTTRAccount')

    def __init__(self, cr):
        LoginBase.LoginBase.__init__(self, cr)

    def supportsRelogin(self):
        return 0

    def authorize(self, username, password):
        return 0 # No error!

    def sendLoginMsg(self):
        cr = self.cr
        datagram = PyDatagram()
        datagram.addUint16(CLIENT_HELLO)
        datagram.addUint32(cr.hashVal)
        datagram.addString(cr.serverVersion)
        cr.send(datagram)

    def resendPlayToken(self):
        self.notify.error('Cannot resend playtoken!')

    def getErrorCode(self):
        return 0

    def needToSetParentPassword(self):
        return 0

    def authenticateParentPassword(self, loginName, password, parentPassword):
        self.notify.error('authenticateParentPassword called')

    def authenticateDelete(self, loginName, password):
        return 1
