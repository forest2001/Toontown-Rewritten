from direct.distributed.AstronInternalRepository import AstronInternalRepository
from otp.distributed.OtpDoGlobals import *
from otp.rpc.RPCClient import RPCClient
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.MsgTypes import *
from panda3d.core import *
import pymongo, urlparse

mongodb_url = ConfigVariableString('mongodb-url', 'mongodb://localhost',
                                   'Specifies the URL of the MongoDB server that'
                                   'stores all gameserver data.')
mongodb_replicaset = ConfigVariableString('mongodb-replicaset', '', 'Specifies the replica set of the gameserver data DB.')

class ToontownInternalRepository(AstronInternalRepository):
    GameGlobalsId = OTP_DO_ID_TOONTOWN
    dbId = 4003

    def __init__(self, baseChannel, serverId=None, dcFileNames = None,
                 dcSuffix='AI', connectMethod=None, threadedNet=None):
        AstronInternalRepository.__init__(self, baseChannel, serverId, dcFileNames,
                                 dcSuffix, connectMethod, threadedNet)
        self._callbacks = {}

        mongourl = mongodb_url.getValue()
        replicaset = mongodb_replicaset.getValue()
        db = (urlparse.urlparse(mongourl).path or '/test')[1:]
        if replicaset:
            self.mongo = pymongo.MongoClient(mongourl, replicaset=replicaset)
        else:
            self.mongo = pymongo.MongoClient(mongourl)
        self.mongodb = self.mongo[db]

        self.rpc = RPCClient()

    def handleConnected(self):
        self.netMessenger.register(0, 'shardStatus')
        self.netMessenger.register(1, 'accountDisconnected')
        self.netMessenger.register(2, 'avatarOnline')
        self.netMessenger.register(3, 'avatarOffline')

    def getAvatarIdFromSender(self):
        return self.getMsgSender() & 0xFFFFFFFF

    def getAccountIdFromSender(self):
        return (self.getMsgSender()>>32) & 0xFFFFFFFF

    def _isValidPlayerLocation(self, parentId, zoneId):
        if zoneId < 1000 and zoneId != 1:
            return False

        return True
