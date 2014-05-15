from direct.distributed.AstronInternalRepository import AstronInternalRepository
from otp.distributed.OtpDoGlobals import *
from otp.rpc.RPCClient import RPCClient
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.MsgTypes import *
from panda3d.core import *
import pymongo, urlparse

# HACKFIX TODO: Have the dev server's panda3d installation update properly?
# Currently, it doesn't have the new message types required for the
# DBSS_OBJECT_GET_ACTIVATED MsgType, so for now we will hard-code it in.

mongodb_url = ConfigVariableString('mongodb-url', 'mongodb://localhost',
                                   'Specifies the URL of the MongoDB server that'
                                   'stores all gameserver data.')

class ToontownInternalRepository(AstronInternalRepository):
    GameGlobalsId = OTP_DO_ID_TOONTOWN
    dbId = 4003
    
    def __init__(self, baseChannel, serverId=None, dcFileNames = None,
                 dcSuffix='AI', connectMethod=None, threadedNet=None):
        AstronInternalRepository.__init__(self, baseChannel, serverId, dcFileNames,
                                 dcSuffix, connectMethod, threadedNet)
        self._callbacks = {}

        mongourl = mongodb_url.getValue()
        db = (urlparse.urlparse(mongourl).path or '/test')[1:]
        self.mongo = pymongo.Connection(mongourl)
        self.mongodb = self.mongo[db]

        self.rpc = RPCClient()

    def handleConnected(self):
        self.netMessenger.register(0, 'shardStatus')

    def getAvatarIdFromSender(self):
        return self.getMsgSender() & 0xFFFFFFFF

    def getAccountIdFromSender(self):
        return (self.getMsgSender()>>32) & 0xFFFFFFFF

    def _isValidPlayerLocation(self, parentId, zoneId):
        if zoneId < 1000 and zoneId != 1:
            return False

        return True
