from pandac.PandaModules import *
from DistributedNPCToonBase import *
from toontown.quest import QuestParser
from toontown.quest import QuestChoiceGui
from toontown.quest import TrackChoiceGui
from toontown.toonbase import TTLocalizer
from toontown.hood import ZoneUtil
from toontown.toontowngui import TeaserPanel
from otp.nametag.NametagConstants import *

class DistributedNPCSnowballGiver(DistributedNPCToonBase):

    def __init__(self, cr):
        DistributedNPCToonBase.__init__(self, cr)

    def delayDelete(self):
        DistributedNPCToonBase.delayDelete(self)
        DistributedNPCToonBase.disable(self)

    def handleCollisionSphereEnter(self, collEntry):
        sbCount = base.localAvatar.numPies
        if sbCount <= 0: # Incase they somehow go negative...
            self.sendUpdate('avatarEnter', [])
        
    def gaveSnowballs(self, npcId, avId, sbPhraseId):
        if avId in base.cr.doId2do:
            avName = base.cr.doId2do.get(avId).getName()
            chatPhrases = [
                'Go get \'em, %s!' % avName,
                'You can do it, %s!' % avName,
            ]
            self.setChatAbsolute(chatPhrases[sbPhraseId], CFSpeech | CFTimeout)
        else:
            self.setChatAbsolute('Go get \'em!', CFSpeech | CFTimeout)
