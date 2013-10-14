import toontown.minigame.MinigameCreatorAI
from toontown.distributed.ToontownDistrictAI import ToontownDistrictAI
from toontown.distributed.ToontownDistrictStatsAI import ToontownDistrictStatsAI
from direct.distributed.AstronInternalRepository import AstronInternalRepository
from direct.distributed.PyDatagram import *
from otp.distributed.OtpDoGlobals import *

class ToontownAIRepository(AstronInternalRepository):
    GameGlobalsId = OTP_DO_ID_TOONTOWN

    def __init__(self, baseChannel, serverId, districtName):
        AstronInternalRepository.__init__(self, baseChannel, serverId, dcSuffix='AI')

        self.districtName = districtName

        self.doLiveUpdates = False

    def getTrackClsends(self):
        return False

    def handleConnected(self):
        self.districtId = self.allocateChannel()
        self.distributedDistrict = ToontownDistrictAI(self)
        self.distributedDistrict.setName(self.districtName)
        self.distributedDistrict.generateWithRequiredAndId(simbase.air.districtId,
                                                           self.getGameDoId(), 2)

        # Claim ownership of that district...
        dg = PyDatagram()
        dg.addServerHeader(simbase.air.districtId, simbase.air.ourChannel, STATESERVER_OBJECT_SET_AI_CHANNEL)
        dg.addUint32(simbase.air.districtId)
        dg.addChannel(simbase.air.ourChannel)
        simbase.air.send(dg)

        self.createGlobals()
        self.loadDNA()
        self.createZones()

        self.distributedDistrict.b_setAvailable(1)

    def incrementPopulation(self):
        self.districtStats.b_setAvatarCount(self.districtStats.getAvatarCount() + 1)

    def decrementPopulation(self):
        self.districtStats.b_setAvatarCount(self.districtStats.getAvatarCount() - 1)

    def createGlobals(self):
        """
        Create "global" objects, e.g. TimeManager et al.
        """
        self.districtStats = ToontownDistrictStatsAI(self)
        self.districtStats.settoontownDistrictId(self.districtId)
        self.districtStats.generateWithRequired(2)

        self.holidayManager = None

    def loadDNA(self):
        """
        Load DNA files for all zones.
        """

    def createZones(self):
        """
        Spawn safezone objects, streets, doors, NPCs, etc.
        """
