import random
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.fsm.FSM import FSM
from otp.ai.MagicWordGlobal import *
from DistributedInvasionSuitAI import DistributedInvasionSuitAI
import SafezoneInvasionGlobals
from toontown.suit import SuitTimings

class DistributedSafezoneInvasionAI(DistributedObjectAI, FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedSafezoneInvasionAI")

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        FSM.__init__(self, 'InvasionFSM')

        self.waveNumber = 0
        self.spawnPoints = []
        self.suits = []

    def announceGenerate(self):
        self.demand('BeginWave', 0)

    def delete(self):
        DistributedObjectAI.delete(self)
        self.demand('Off')

    def hitToon(self, doId):
        # Someone hit a Toon!
        avId = self.air.getAvatarIdFromSender()

        toon = self.air.doId2do.get(doId)
        if not toon:
            self.air.writeServerEvent('suspicious', avId, 'Hit a nonexistent Toon with a pie!')
            return

        from toontown.toon.DistributedToonAI import DistributedToonAI
        if not isinstance(toon, DistributedToonAI):
            self.air.writeServerEvent('suspicious', avId, 'Hit a non-Toon with a pie through hitToon()!')
            return

        toon.toonUp(SafezoneInvasionGlobals.ToonHealAmount)

    def hitSuit(self, doId):
        # Someone hit one of our suits...
        avId = self.air.getAvatarIdFromSender()

        suit = self.air.doId2do.get(doId)
        if suit not in self.suits:
            # N.B. this is NOT suspicious as it can happen as a result of a race condition
            return

        suit.takeDamage(SafezoneInvasionGlobals.ToonAttackAmount)

    def __deleteSuits(self):
        for suit in self.suits:
            suit.requestDelete()

    def spawnOne(self, suitType, levelOffset=0):
        # Pick a spawnpoint:
        pointId = random.choice(self.spawnPoints)
        self.spawnPoints.remove(pointId)

        suit = DistributedInvasionSuitAI(self.air, self)
        suit.dna.newSuit(suitType)
        suit.setSpawnPoint(pointId)
        suit.setLevel(levelOffset)
        suit.generateWithRequired(self.zoneId)
        suit.b_setState('FlyDown')

        self.suits.append(suit)

    def suitDied(self, suit):
        if suit not in self.suits:
            self.notify.warning('suitDied called twice for same suit!')
            return

        self.suits.remove(suit)
        if not self.suits:
            self.waveWon()

    def waveWon(self):
        if self.state != 'Wave':
            return

        lastWave = (self.waveNumber == len(SafezoneInvasionGlobals.SuitWaves)-1)

        if lastWave:
            self.demand('Victory')
        else:
            self.demand('Intermission')

    def enterBeginWave(self, waveNumber):
        # In this state, Cogs rain down from the heavens. We call .spawnOne at
        # regular intervals until the quota for the wave is met.
        self.waveNumber = waveNumber

        # Reset spawnpoints and suits:
        self.spawnPoints = range(len(SafezoneInvasionGlobals.SuitSpawnPoints))
        self.__deleteSuits()

        # Get the suits to call:
        suitsToCall = SafezoneInvasionGlobals.SuitWaves[self.waveNumber]

        # How long do we have to spread out the suit calldowns?
        # In case some dummkopf set WaveBeginningTime too low:
        delay = max(SafezoneInvasionGlobals.WaveBeginningTime, SuitTimings.fromSky)
        spread = delay - SuitTimings.fromSky
        spreadPerSuit = spread/len(suitsToCall)

        self._waveBeginTasks = []
        for i, suit in enumerate(suitsToCall):
            self._waveBeginTasks.append(
                taskMgr.doMethodLater(i*spreadPerSuit, self.spawnOne,
                                      self.uniqueName('summon-suit-%s' % i),
                                      extraArgs=[suit]))

        # Plus a task to switch to the 'Wave' state:
        self._waveBeginTasks.append(
            taskMgr.doMethodLater(delay, self.demand,
                                  self.uniqueName('begin-wave'),
                                  extraArgs=['Wave']))


    def exitBeginWave(self):
        for task in self._waveBeginTasks:
            task.remove()

    def enterWave(self):
        # This state is entered after all Cogs have been spawned by BeginWave.
        # We wait for all of them to die, then move to the intermission.

        # Start the suits marching!
        for suit in self.suits:
            suit.start()

    def exitWave(self):
        # Clean up any loose suits, in case the wave is being ended by MW.
        self.__deleteSuits()

    def enterIntermission(self):
        # This state is entered after a wave is successfully over. There's a
        # pause in the action until the next wave.
        self._delay = taskMgr.doMethodLater(SafezoneInvasionGlobals.IntermissionTime,
                                            self.__endIntermission,
                                            self.uniqueName('intermission'))

    def __endIntermission(self, task):
        self.demand('BeginWave', self.waveNumber + 1)

    def exitIntermission(self):
        self._delay.remove()

    def enterVictory(self):
        # The Toons win! ...
        pass

    def enterOff(self):
        self.__deleteSuits()

@magicWord(category=CATEGORY_DEBUG, types=[str, str])
def szInvasion(cmd, arg=''):
    invasion = simbase.air.doFind('SafezoneInvasion')

    if invasion is None and cmd != 'start':
        return 'No invasion has been created'

    if cmd == 'start':
        if invasion is None:
            invasion = DistributedSafezoneInvasionAI(simbase.air)
            invasion.generateWithRequired(2000)
        else:
            return 'An invasion object already exists.'
    elif cmd == 'stop':
        invasion.requestDelete()
    elif cmd == 'spawn':
        invasion.spawnOne(arg)
    elif cmd == 'wave':
        invasion.demand('BeginWave', int(arg))
    elif cmd == 'endWave':
        invasion.waveWon()
