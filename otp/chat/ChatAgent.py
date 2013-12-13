from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal
from pandac.PandaModules import *
from otp.otpbase import OTPGlobals

class ChatAgent(DistributedObjectGlobal):
    def __init__(self, cr):
        DistributedObjectGlobal.__init__(self, cr)
        self.notify.warning('ChatAgent going online')

    def delete(self):
        self.ignoreAll()
        self.notify.warning('ChatAgent going offline')
        self.cr.chatManager = None
        DistributedObjectGlobal.delete(self)
        return

    def adminChat(self, aboutId, message):
        self.notify.warning('Admin Chat(%s): %s' % (aboutId, message))
        messenger.send('adminChat', [aboutId, message])

    def sendChatMessage(self, message):
        self.sendUpdate('chatMessage', [message])
