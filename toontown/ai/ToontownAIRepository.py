import toontown.minigame.MinigameCreatorAI
from toontown.distributed.ToontownDistrictAI import ToontownDistrictAI
from toontown.distributed.ToontownDistrictStatsAI import ToontownDistrictStatsAI
from toontown.distributed.ShardStatus import ShardStatusSender
from otp.ai.TimeManagerAI import TimeManagerAI
from otp.ai.MagicWordManagerAI import MagicWordManagerAI
from toontown.ai.HolidayManagerAI import HolidayManagerAI
from toontown.ai.NewsManagerAI import NewsManagerAI
from toontown.ai.FishManagerAI import FishManagerAI
from toontown.distributed.ToontownInternalRepository import ToontownInternalRepository
from toontown.toon import NPCToons
from toontown.hood import TTHoodAI, DDHoodAI, DGHoodAI, BRHoodAI, MMHoodAI, DLHoodAI, OZHoodAI, GSHoodAI, GZHoodAI, ZoneUtil
from toontown.hood import SellbotHQAI, CashbotHQAI, LawbotHQAI, BossbotHQAI
from toontown.toonbase import ToontownGlobals
from direct.distributed.PyDatagram import *
from otp.ai.AIZoneData import *
from toontown.dna import DNAParser
from toontown.dna.DNASpawnerAI import DNASpawnerAI
from direct.stdpy.file import open
import time
import random

# Friends!
from otp.friends.FriendManagerAI import FriendManagerAI

# Estates!
from toontown.estate.EstateManagerAI import EstateManagerAI

# Par-tay!
if simbase.config.GetBool('want-parties', True):
    from toontown.uberdog.DistributedPartyManagerAI import DistributedPartyManagerAI
    from otp.distributed.OtpDoGlobals import *

# Fireworks!
from direct.task import Task
from toontown.toonbase import ToontownGlobals
from toontown.effects.DistributedFireworkShowAI import DistributedFireworkShowAI
from toontown.effects import FireworkShows
from direct.distributed.ClockDelta import *
from toontown.parties import PartyGlobals

# Tasks!
from toontown.quest.QuestManagerAI import QuestManagerAI
from toontown.building.DistributedTrophyMgrAI import DistributedTrophyMgrAI
from toontown.shtiker.CogPageManagerAI import CogPageManagerAI
from toontown.coghq.FactoryManagerAI import FactoryManagerAI
from toontown.coghq.MintManagerAI import MintManagerAI
from toontown.coghq.LawOfficeManagerAI import LawOfficeManagerAI
from toontown.coghq.PromotionManagerAI import PromotionManagerAI
from toontown.coghq.CogSuitManagerAI import CogSuitManagerAI
from toontown.coghq.CountryClubManagerAI import CountryClubManagerAI

# Suits.
from toontown.suit.SuitInvasionManagerAI import SuitInvasionManagerAI

# Toontorial
from toontown.tutorial.TutorialManagerAI import TutorialManagerAI

# Catalogs.
from toontown.catalog.CatalogManagerAI import CatalogManagerAI

# Magic Words!
from panda3d.core import PStatClient
from otp.ai.MagicWordGlobal import *
import otp.ai.DiagnosticMagicWords

class ToontownAIRepository(ToontownInternalRepository):
    def __init__(self, baseChannel, serverId, districtName):
        ToontownInternalRepository.__init__(self, baseChannel, serverId, dcSuffix='AI')

        self.dnaSpawner = DNASpawnerAI(self)

        self.districtName = districtName

        self.zoneAllocator = UniqueIdAllocator(ToontownGlobals.DynamicZonesBegin,
                                               ToontownGlobals.DynamicZonesEnd)
        self.zoneId2owner = {}

        NPCToons.generateZone2NpcDict()

        self.hoods = []
        self.zoneDataStore = AIZoneDataStore()

        self.useAllMinigames = self.config.GetBool('want-all-minigames', False)
        self.doLiveUpdates = self.config.GetBool('want-live-updates', True)

        self.holidayManager = HolidayManagerAI(self)

        self.fishManager = FishManagerAI()
        self.questManager = QuestManagerAI(self)
        self.cogPageManager = CogPageManagerAI()
        self.factoryMgr = FactoryManagerAI(self)
        self.mintMgr = MintManagerAI(self)
        self.lawOfficeMgr = LawOfficeManagerAI(self)
        self.countryClubMgr = CountryClubManagerAI(self)
        self.promotionMgr = PromotionManagerAI(self)
        self.cogSuitMgr = CogSuitManagerAI(self)
        self.suitInvasionManager = SuitInvasionManagerAI(self)

        self.statusSender = ShardStatusSender(self)

        self.dnaStoreMap = {}

        self.buildingManagers = {}
        self.suitPlanners = {}

    def getTrackClsends(self):
        return False


    def handleConnected(self):
        ToontownInternalRepository.handleConnected(self)
        self.districtId = self.allocateChannel()
        self.distributedDistrict = ToontownDistrictAI(self)
        self.distributedDistrict.setName(self.districtName)
        self.distributedDistrict.generateWithRequiredAndId(simbase.air.districtId,
                                                           self.getGameDoId(), 2)

        # Claim ownership of that district...
        dg = PyDatagram()
        dg.addServerHeader(simbase.air.districtId, simbase.air.ourChannel, STATESERVER_OBJECT_SET_AI)
        dg.addChannel(simbase.air.ourChannel)
        simbase.air.send(dg)

        self.createGlobals()
        self.createZones()

        self.statusSender.start()

        self.distributedDistrict.b_setAvailable(1)
        self.notify.info('District is now ready.')

    def incrementPopulation(self):
        self.districtStats.b_setAvatarCount(self.districtStats.getAvatarCount() + 1)
        self.statusSender.sendStatus()

    def decrementPopulation(self):
        self.districtStats.b_setAvatarCount(self.districtStats.getAvatarCount() - 1)
        self.statusSender.sendStatus()

    def allocateZone(self, owner=None):
        zoneId = self.zoneAllocator.allocate()
        if owner:
            self.zoneId2owner[zoneId] = owner
        return zoneId

    def deallocateZone(self, zone):
        if self.zoneId2owner.get(zone):
            del self.zoneId2owner[zone]
        self.zoneAllocator.free(zone)

    def getZoneDataStore(self):
        return self.zoneDataStore

    def getAvatarExitEvent(self, avId):
        return 'distObjDelete-%d' % avId

    def createGlobals(self):
        """
        Create "global" objects, e.g. TimeManager et al.
        """
        self.districtStats = ToontownDistrictStatsAI(self)
        self.districtStats.settoontownDistrictId(self.districtId)
        self.districtStats.generateWithRequiredAndId(self.allocateChannel(),
                                                     self.getGameDoId(), 3)

        self.timeManager = TimeManagerAI(self)
        self.timeManager.generateWithRequired(2)

        self.newsManager = NewsManagerAI(self)
        self.newsManager.generateWithRequired(2)

        self.magicWordManager = MagicWordManagerAI(self)
        self.magicWordManager.generateWithRequired(2)

        self.friendManager = FriendManagerAI(self)
        self.friendManager.generateWithRequired(2)

        if simbase.config.GetBool('want-parties', True):
            self.partyManager = DistributedPartyManagerAI(self)
            self.partyManager.generateWithRequired(2)

            # setup our view of the global party manager ud
            self.globalPartyMgr = self.generateGlobalObject(OTP_DO_ID_GLOBAL_PARTY_MANAGER, 'GlobalPartyManager')

        self.estateManager = EstateManagerAI(self)
        self.estateManager.generateWithRequired(2)

        self.trophyMgr = DistributedTrophyMgrAI(self)
        self.trophyMgr.generateWithRequired(2)

        self.tutorialManager = TutorialManagerAI(self)
        self.tutorialManager.generateWithRequired(2)
        
        self.catalogManager = CatalogManagerAI(self)
        self.catalogManager.generateWithRequired(2)

    def createZones(self):
        """
        Spawn safezone objects, streets, doors, NPCs, etc.
        """
        start = time.clock()
        def clearQueue():
            '''So the TCP window doesn't fill up and we get the axe'''
            while self.readerPollOnce():
                pass

        self.hoods.append(TTHoodAI.TTHoodAI(self))
        clearQueue()
        self.hoods.append(DDHoodAI.DDHoodAI(self))
        clearQueue()
        self.hoods.append(DGHoodAI.DGHoodAI(self))
        clearQueue()
        self.hoods.append(BRHoodAI.BRHoodAI(self))
        clearQueue()
        self.hoods.append(MMHoodAI.MMHoodAI(self))
        clearQueue()
        self.hoods.append(DLHoodAI.DLHoodAI(self))
        clearQueue()
        self.hoods.append(GSHoodAI.GSHoodAI(self))
        clearQueue()
        self.hoods.append(OZHoodAI.OZHoodAI(self))
        clearQueue()
        self.hoods.append(GZHoodAI.GZHoodAI(self))
        clearQueue()

        if simbase.config.GetBool('want-sbhq', True):
            self.hoods.append(SellbotHQAI.SellbotHQAI(self))
            clearQueue()

        if simbase.config.GetBool('want-cbhq', True):
            self.hoods.append(CashbotHQAI.CashbotHQAI(self))
            clearQueue()

        if simbase.config.GetBool('want-lbhq', True):
            self.hoods.append(LawbotHQAI.LawbotHQAI(self))
            clearQueue()

        if simbase.config.GetBool('want-bbhq', True):
            self.hoods.append(BossbotHQAI.BossbotHQAI(self))
            clearQueue()

        for sp in self.suitPlanners.values():
            sp.assignInitialSuitBuildings()

    def genDNAFileName(self, zoneId):
        zoneId = ZoneUtil.getCanonicalZoneId(zoneId)
        hoodId = ZoneUtil.getCanonicalHoodId(zoneId)
        hood = ToontownGlobals.dnaMap[hoodId]
        if hoodId == zoneId:
            zoneId = 'sz'
            phase = ToontownGlobals.phaseMap[hoodId]
        else:
            phase = ToontownGlobals.streetPhaseMap[hoodId]

        return 'phase_%s/dna/%s_%s.xml' % (phase, hood, zoneId)

    def loadDNA(self, filename):
        with open('/' + filename) as f:
            tree = DNAParser.parse(f)

        return tree


@magicWord(category=CATEGORY_SYSADMIN, types=[str, int])
def pstats(host='localhost', port=5185):
    """ Tell the AI to connect a PStatsClient to the server specified. """
    conn = PStatClient.connect(host, port)
    if conn:
        return "%s has successfully opened a PStat connection to %s:%d" % (simbase.air.distributedDistrict.getName(), host, port)
    return "%s was unable to open a PStat connection to %s:%d." % (simbase.air.distributedDistrict.getName(), host, port)

@magicWord(category=CATEGORY_SYSADMIN, types=[str], aliases=['cpu-usage'])
def cpu(percpu=''):
    """ Return the current CPU usage of the AI server as a percentage.
    This will return a list if percpu is enabled. (~cpu percpu)
    """
    try:
        from psutil import cpu_percent
        percpu = percpu == 'percpu'
        return "Current CPU usage for %s: %s%%" % (simbase.air.distributedDistrict.getName(), str(cpu_percent(interval=None, percpu=percpu)))
    except ImportError:
        return "psutil is not installed on %s! Unable to fetch CPU usage." % simbase.air.distributedDistrict.getName()

@magicWord(category=CATEGORY_SYSADMIN, aliases=['memory', 'mem-usage'])
def mem():
    """ Return the current memory usage of the AI server as a percentage. """
    try:
        from psutil import virtual_memory
        return "Current memory usage for %s: %s%%" % (simbase.air.distributedDistrict.getName(), str(virtual_memory().percent))
    except ImportError:
        return "psutil is not installed on %s! Unable to fetch memory usage." % simbase.air.distributedDistrict.getName()
