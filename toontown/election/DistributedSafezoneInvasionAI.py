import random
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.fsm.FSM import FSM
from otp.ai.MagicWordGlobal import *
from DistributedInvasionSuitAI import DistributedInvasionSuitAI
import SafezoneInvasionConstants
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
        self.__deleteSuits()

    def __deleteSuits(self):
        for suit in self.suits:
            suit.requestDelete()
        self.suits = []

    def spawnOne(self, suitType):
        # Pick a spawnpoint:
        pointId = random.choice(self.spawnPoints)
        self.spawnPoints.remove(pointId)

        suit = DistributedInvasionSuitAI(self.air, self)
        suit.dna.newSuit(suitType)
        suit.setSpawnPoint(pointId)
        suit.generateWithRequired(self.zoneId)
        suit.b_setState('FlyDown')

        self.suits.append(suit)

    def enterBeginWave(self, waveNumber):
        # In this state, Cogs rain down from the heavens. We call .spawnOne at
        # regular intervals until the quota for the wave is met.
        self.waveNumber = waveNumber

        # Reset spawnpoints and suits:
        self.spawnPoints = range(len(SafezoneInvasionConstants.SuitSpawnPoints))
        self.__deleteSuits()

        # Get the suits to call:
        suitsToCall = SafezoneInvasionConstants.SuitWaves[self.waveNumber]

        # How long do we have to spread out the suit calldowns?
        # In case some dummkopf set WaveBeginningTime too low:
        delay = max(SafezoneInvasionConstants.WaveBeginningTime, SuitTimings.fromSky)
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
        pass


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
    elif cmd == 'intermission':
        invasion.demand('Intermission')
