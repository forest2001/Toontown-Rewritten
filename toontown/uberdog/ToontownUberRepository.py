import toontown.minigame.MinigameCreatorAI
from toontown.distributed.ToontownInternalRepository import ToontownInternalRepository
from direct.distributed.PyDatagram import *
from otp.distributed.DistributedDirectoryAI import DistributedDirectoryAI
from otp.distributed.OtpDoGlobals import *

class ToontownUberRepository(ToontownInternalRepository):
    def __init__(self, baseChannel, serverId):
        ToontownInternalRepository.__init__(self, baseChannel, serverId, dcSuffix='UD')

    def handleConnected(self):
        rootObj = DistributedDirectoryAI(self)
        rootObj.generateWithRequiredAndId(self.getGameDoId(), 0, 0)

        self.createGlobals()

    def createGlobals(self):
        """
        Create "global" objects.
        """
        default = simbase.config.GetBool('want-ud', 1)
        if simbase.config.GetBool('want-ClientServicesManagerUD', default):
            self.csm = simbase.air.generateGlobalObject(OTP_DO_ID_CLIENT_SERVICES_MANAGER,
                                                        'ClientServicesManager')
        if simbase.config.GetBool('want-ChatAgentUD', default):
            self.chatAgent = simbase.air.generateGlobalObject(OTP_DO_ID_CHAT_MANAGER,
                                                            'ChatAgent')
        if simbase.config.GetBool('want-TTRFriendsManagerUD', default):
            self.friendsManager = simbase.air.generateGlobalObject(OTP_DO_ID_TTR_FRIENDS_MANAGER,
                                                                 'TTRFriendsManager')
        if simbase.config.GetBool('want-GlobalPartyManagerUD', default):
            self.globalPartyMgr = simbase.air.generateGlobalObject(OTP_DO_ID_GLOBAL_PARTY_MANAGER, 'GlobalPartyManager')
