from direct.directnotify import DirectNotifyGlobal
from toontown.parties.DistributedPartyActivityAI import DistributedPartyActivityAI
from direct.task import Task
import PartyGlobals

class DistributedPartyJukeboxActivityBaseAI(DistributedPartyActivityAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedPartyJukeboxActivityBaseAI")
    
    def __init__(self, air, parent, activityTuple):
        DistributedPartyActivityAI.__init__(self, air, parent, activityTuple)
        self.music = PartyGlobals.PhaseToMusicData40
        self.queue = []
        self.owners = []
        self.currentToon = 0
        self.playing = False
        
    def delete(self):
        taskMgr.remove('playSong%d' % self.doId)
        DistributedPartyActivityAI.delete(self)
        
    
    def setNextSong(self, song):
        avId = self.air.getAvatarIdFromSender()
        phase = self.music.get(song[0])
        if avId != self.currentToon:
            self.air.writeServerEvent('suspicious',avId,'Toon tried to set song without using the jukebox!')
        if not phase:
            self.air.writeServerEvent('suspicious',avId,'Toon supplied invalid phase for song!')
            return
        if not phase.has_key(song[1]):
            self.air.writeServerEvent('suspicious',avId,'Toon supplied invalid song name!')
            return
        if avId in self.owners:
            self.queue[self.owners.index(avId)] = song
        else:
            self.queue.append(song)
            self.owners.append(avId)
        for toon in self.toonsPlaying:
            self.sendUpdateToAvatarId(toon, 'setSongInQueue', [song])
        if not self.playing:
            #stop default party music...
            self.d_setSongPlaying([0, ''], 0)
            self.__startPlaying()
            
    def __startPlaying(self):
        if len(self.queue) == 0:
            #start default party music!
            self.d_setSongPlaying([13, 'party_original_theme.ogg'], 0)
            self.playing = False
            return
        self.playing = True
        
        #get song information....
        details = self.queue.pop(0)
        owner = self.owners.pop(0)
        
        songInfo = self.music[details[0]][details[1]]
        
        #play song!
        self.d_setSongPlaying(details, owner)
        
        taskMgr.doMethodLater(songInfo[1]*PartyGlobals.getMusicRepeatTimes(songInfo[1]), self.__pause, 'playSong%d' % self.doId, extraArgs=[])
        
    def __pause(self):
        #stop music!
        self.d_setSongPlaying([0, ''], 0)
        #and hold.
        taskMgr.doMethodLater(PartyGlobals.MUSIC_GAP, self.__startPlaying, 'playSong%d' % self.doId, extraArgs=[])
        
    def toonJoinRequest(self):
        avId = self.air.getAvatarIdFromSender()
        if self.currentToon:
            self.sendUpdateToAvatarId(avId, 'joinRequestDenied', [1])
            return
        self.currentToon = avId
        taskMgr.doMethodLater(PartyGlobals.JUKEBOX_TIMEOUT, self.__removeToon, 'removeToon%d', extraArgs=[])
        self.toonsPlaying.append(avId)
        self.updateToonsPlaying()

    def toonExitRequest(self):
        pass

    def toonExitDemand(self):
        avId = self.air.getAvatarIdFromSender()
        if avId != self.currentToon:
            return
        taskMgr.remove('removeToon%d' % self.doId)
        self.currentToon = 0
        self.toonsPlaying.remove(avId)
        self.updateToonsPlaying()

    def __removeToon(self):
        if not self.currentToon:
            return
        self.toonsPlaying.remove(self.currentToon)
        self.updateToonsPlaying()
        self.currentToon = 0
        
    def d_setSongPlaying(self, details, owner):
        self.sendUpdate('setSongPlaying', [details, owner])

    def queuedSongsRequest(self):
        avId = self.air.getAvatarIdFromSender()
        if avId in self.owners:
            index = self.owners.index(avId)
        else:
            index = -1
        self.sendUpdateToAvatarId(avId, 'queuedSongsResponse', [self.queue, index])

    def moveHostSongToTopRequest(self):
        avId = self.air.getAvatarIdFromSender()
        if avId != self.currentToon:
            self.air.writeServerEvent('suspicious',avId,'Toon tried to set song without using the jukebox!')
        host = self.air.doId2do[self.parent].hostId
        if avId != host:
            self.air.writeServerEvent('suspicious',avId,'Toon tried to move the host\'s song to the top!')
            return
        if not host in self.owners:
            self.air.writeServerEvent('suspicious',avId,'Host tried to move non-existent song to the top of the queue!')
            return
        index = self.owners.index(host)
        
        self.owners.remove(host)
        song = self.queue.pop(index)
        
        self.owners.insert(0, host)
        self.queue.insert(0, song)
        
        for toon in self.toonsPlaying:
            self.sendUpdateToAvatarId(toon, 'moveHostSongToTop')