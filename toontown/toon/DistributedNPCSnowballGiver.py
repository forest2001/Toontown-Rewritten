from pandac.PandaModules import *
from DistributedNPCToonBase import *
from toontown.quest import QuestParser
from toontown.quest import QuestChoiceGui
from toontown.quest import TrackChoiceGui
from toontown.toonbase import TTLocalizer
from toontown.hood import ZoneUtil
from toontown.toontowngui import TeaserPanel
from otp.nametag.NametagConstants import *
ChoiceTimeout = 20

class DistributedNPCSnowballGiver(DistributedNPCToonBase):

    def __init__(self, cr):
        DistributedNPCToonBase.__init__(self, cr)

    def delayDelete(self):
        DistributedNPCToonBase.delayDelete(self)
        DistributedNPCToonBase.disable(self)

    def handleCollisionSphereEnter(self, collEntry):
        self.sendUpdate('avatarEnter', [])
        
    def gaveSnowballs(self, npcId, avId):
        if avId in base.cr.doId2do:
            av = base.cr.doId2do.get(avId)
        else:
            return
        self.setChatAbsolute('Go get \'em, %s!' % av.getName(), CFSpeech | CFTimeout)
