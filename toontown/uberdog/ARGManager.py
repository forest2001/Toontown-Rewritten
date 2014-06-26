from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal
from toontown.toonbase import ToontownGlobals
from otp.speedchat import SpeedChatGlobals
from direct.directnotify.DirectNotifyGlobal import directNotify
from toontown.hood import ZoneUtil
from pandac.PandaModules import Vec3

# Portable Hole settings
POSITION_TOLERANCE = 10
Hood2Details = {
    # hood : [pos, speedchatIndex, destination]
    ToontownGlobals.DonaldsDock: [(-23, 5, 6), 1522, 2714], # Bring it on!
    ToontownGlobals.ToontownCentral: [(93, -106, 3), 1603, 3823], # I like this game!
    ToontownGlobals.TheBrrrgh: [(-111, -41, 9), 1003, 4612], # Follow me.
    ToontownGlobals.MinniesMelodyland: [(0, -20, -16), 1209, 5602], # I found what you need.
    ToontownGlobals.DaisyGardens: [(1, 91, 0), 1134, 9501], # Don't wait for me.
    ToontownGlobals.DonaldsDreamland: [(48, -96, 0), 5500, 17000], # :)
    ToontownGlobals.OutdoorZone: [(-46, -140, 0), 1556, 11000], # Go for the weakest Cog first.
    ToontownGlobals.SellbotHQ: [(39, -37, 10), 1555, 12000], # Let's all go for the same Cog.
    ToontownGlobals.CashbotHQ: [(-78, -134, -63), 1558, 13000], # Save your powerful Gags.
}
Interior2Messages = {
    3823: ["Welcome, Doctor Surlee! You are on your way to see KOOKY CINEPLEX", "-4"], # DD to TTC
    5602: ["Hello, Doctor Surlee! Taking you to the PRECIPITATION FOUNDATION", "6,"], # TTC to TB
    4612: ["Hi, Doctor Surlee! Sending you to DR. FRET'S DENTISTRY", ","], # TB to MML
    2714: ["Welcome, Dr. Surlee! You are on route to ARTIE CHOKE'S NECKTIES", "-1"], # MML to DG
    9501: ["Good afternoon, Doctor Surlee! Setting destination to the LULLABY LIBRARY", "4"], # DG to DDL
    17000: ["Good evening, Dr. Surlee! You are on route to CHIP 'N DALE'S MINIGOLF", "0"], # DDL to AA
    11000: ["Greetings, Doctor Surlee. You will soon arrive at SELLBOT HQ.", "Do you think they're going too far?"],
    12000: ["Greetings, Doctor Surlee. You are now going to CASHBOT HQ.", "Well there's certainly no stopping them now."],
    13000: ["Greetings, Doctor Surlee. Taking you to ERROR: UNKNOWN LOCATION", "They are indeed quite clever."], # CBHQ (unlocks LBHQ)
}

class ARGManager(DistributedObjectGlobal):
    """
    This is a client-view of the manager that handles everything to do
    with the portable hole ARG event.
    """

    notify = directNotify.newCategory('ARGManager')

    def __init__(self, cr):
        DistributedObjectGlobal.__init__(self, cr)
        self.setupPortableHoleEvent()

    def disable(self):
        self.cleanupPortableHoleEvent()
        DistributedObjectGlobal.disable(self)

    def delete(self):
        self.cleanupPortableHoleEvent()
        DistributedObjectGlobal.delete(self)

    def setupPortableHoleEvent(self):
        def phraseSaid(phraseId):
            position, speedchatIndex, destination = Hood2Details.get(base.cr.playGame.getPlace().getZoneId(), [None, None, None])
            if not position or not speedchatIndex or not destination:
                return
            if speedchatIndex != phraseId:
                return
            dummyNode = base.cr.playGame.getPlace().loader.geom.attachNewNode("arg_dummy")
            dummyNode.setPos(*position)
            if Vec3(base.localAvatar.getPos(dummyNode)).length() > POSITION_TOLERANCE:
                return
            dummyNode.removeNode()
            msgBefore, msgAfter = Interior2Messages.get(destination, [None, None])
            if not msgBefore:
                self.notify.warning("Interior %d has no message definitions!" % destination)
                return
            base.localAvatar.setSystemMessage(0, msgBefore)
            requestStatus = [{
                'loader': ZoneUtil.getBranchLoaderName(destination),
                'where': ZoneUtil.getToonWhereName(destination),
                'how': 'teleportIn',
                'hoodId': ZoneUtil.getCanonicalHoodId(destination),
                'zoneId': destination,
                'shardId': None,
                'avId': -1,
            }]
            base.cr.playGame.getPlace().fsm.forceTransition('teleportOut', requestStatus)
            # NOTE: This is somewhat hacky. A better solution would be to fire this once the placeFSM
            # successfully loads the destination. Perhaps this can be fired off upon zone change?
            taskMgr.doMethodLater(10, base.localAvatar.setSystemMessage, self.uniqueName("arg-after-msg"), extraArgs=[0, msgAfter])
            if destination == 13000:
                taskMgr.doMethodLater(15, base.localAvatar.setSystemMessage, self.uniqueName("arg-after-msg"), extraArgs=[0, "Perhaps, however I don't believe they realize what they have unfolded."])
                taskMgr.doMethodLater(20, base.localAvatar.setSystemMessage, self.uniqueName("arg-after-msg"), extraArgs=[0, "I don't think you have either."])
        self.accept(SpeedChatGlobals.SCStaticTextMsgEvent, phraseSaid)

    def cleanupPortableHoleEvent(self):
        self.ignore(SpeedChatGlobals.SCStaticTextMsgEvent)
