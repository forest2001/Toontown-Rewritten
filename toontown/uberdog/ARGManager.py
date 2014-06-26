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
    ToontownGlobals.DonaldsDock: [(-23, 5, 6), 1522, 2519],
    ToontownGlobals.ToontownCentral: [(93, 106, 3), 1603, 3509],
    ToontownGlobals.TheBrrrgh: [(-111, -41, 9), 1003, 4612],
    ToontownGlobals.MinniesMelodyland: [(0, -20, -16), 1209, 5502],
    ToontownGlobals.DaisyGardens: [(1, 91, 0), 1134, 9501],
    ToontownGlobals.DonaldsDreamland: [(48, -96, 0), 5500, 6000],
    ToontownGlobals.CashbotHQ: [(-78, -134, -63), 1004, 13000],
}
Interior2Messages = {
    2519: ["Welcome, Dr. Surlee! Taking you to GOOFY'S GAG SHOP", "-7"], # DD
    3509: ["Welcome, Dr. Surlee! Taking you to CLOTHING SHOP.", "8"], # TTC
    4612: ["Welcome, Dr. Surlee! Taking you to DR. FRET'S DENTISTRY", ","], # TB
    5502: ["Welcome, Dr. Surlee! Taking you to TOON HQ", "-1"], # MML
    9501: ["Welcome, Dr. Surlee! Taking you to LULLABY LIBRARY", "3"], # DG
    6000: ["Welcome, Dr. Surlee! Taking you to CHIP 'N DALE'S ACORN ACRES", "4"], # DDL
    13000: ["Welcome, Dr. Surlee! Taking you to UNKNOWN", "Well, it looks like they're getting more clever."], # CBHQ (unlocks LBHQ)
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
        self.accept(SpeedChatGlobals.SCStaticTextMsgEvent, phraseSaid)

    def cleanupPortableHoleEvent(self):
        self.ignore(SpeedChatGlobals.SCStaticTextMsgEvent)
