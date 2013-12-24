from pandac.PandaModules import *
import SafeZoneLoader
import TTPlayground
import random
from toontown.launcher import DownloadForceAcknowledge
from toontown.ai.DistributedPolarBearMgr import DistributedPolarBearMgr
from otp.speedchat import SpeedChatGlobals
from otp.nametag.NametagConstants import *

class TTSafeZoneLoader(SafeZoneLoader.SafeZoneLoader):

    def __init__(self, hood, parentFSM, doneEvent):
        SafeZoneLoader.SafeZoneLoader.__init__(self, hood, parentFSM, doneEvent)
        self.playgroundClass = TTPlayground.TTPlayground
        self.musicFile = 'phase_4/audio/bgm/TC_nbrhood.ogg'
        self.activityMusicFile = 'phase_3.5/audio/bgm/TC_SZ_activity.ogg'
        self.dnaFile = 'phase_4/dna/toontown_central_sz.dna'
        self.safeZoneStorageDNAFile = 'phase_4/dna/storage_TT_sz.dna'

    def load(self):
        SafeZoneLoader.SafeZoneLoader.load(self)

        #self.geom = loader.loadModel('phase_4/models/neighborhoods/toontown_central_full')

        # Drop "under construction" signs in front of the tunnels so the
        # alpha testers don't complain.
        '''sign = loader.loadModel('phase_4/models/props/construction_sign')
        sign.setH(180)
        sign.setY(-4)
        for tunnel in self.geom.findAllMatches('**/tunnel_origin'):
            sign.instanceTo(tunnel)'''
            
        # For the Flippy NPC:
        npcOrigin = self.geom.attachNewNode('npc_origin_12')
        npcOrigin.setPosHpr(100, 9.952, 4.025, -201.762, 0, 0)

        # For the Polar Bear:
        def phraseSaid(phraseId):
            toontastic = 5700
            if phraseId == toontastic:
                # Check distance...
                if Vec3(base.localAvatar.getPos(npcOrigin)).length() > 5:
                    return
                messenger.send(DistributedPolarBearMgr.ActivateEvent)
        self.accept(SpeedChatGlobals.SCStaticTextMsgEvent, phraseSaid)

        def transformed():
            for do in base.cr.doId2do.values():
                if do.dclass.getName() == 'DistributedNPCToonBase':
                    do.setChatAbsolute('Merry Christmas! Remember: Don\'t be wacky - vote for Slappy!', CFTimeout|CFSpeech) # Lmfao... I have no idea what to put here, but this definitely needs changing.
        self.accept('polarbear-transformed', transformed)

        self.birdSound = map(base.loadSfx, ['phase_4/audio/sfx/SZ_TC_bird1.ogg', 'phase_4/audio/sfx/SZ_TC_bird2.ogg', 'phase_4/audio/sfx/SZ_TC_bird3.ogg'])

    def unload(self):
        del self.birdSound
        self.ignore(SpeedChatGlobals.SCStaticTextMsgEvent)
        self.ignore('blackcat-transformed')
        SafeZoneLoader.SafeZoneLoader.unload(self)

    def enter(self, requestStatus):
        SafeZoneLoader.SafeZoneLoader.enter(self, requestStatus)

    def exit(self):
        SafeZoneLoader.SafeZoneLoader.exit(self)
