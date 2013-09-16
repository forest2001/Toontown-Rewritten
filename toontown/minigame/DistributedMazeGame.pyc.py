# 2013.08.22 22:21:26 Pacific Daylight Time
# Embedded file name: toontown.minigame.DistributedMazeGame
from direct.interval.IntervalGlobal import LerpPosInterval, LerpHprInterval, LerpPosHprInterval
from direct.interval.IntervalGlobal import SoundInterval, LerpScaleInterval, LerpFunctionInterval
from direct.interval.IntervalGlobal import Wait, Func
from direct.interval.MetaInterval import Sequence, Parallel
from direct.gui.DirectGui import DirectWaitBar, DGG
from direct.showbase import PythonUtil
from direct.fsm import ClassicFSM, State
from direct.showbase import RandomNumGen
from direct.task.Task import Task
from direct.distributed.ClockDelta import globalClockDelta
from pandac.PandaModules import Point3, Vec3
from toontown.toonbase import TTLocalizer
from toontown.toonbase import ToontownTimer
from DistributedMinigame import DistributedMinigame
from MazeSuit import MazeSuit
from OrthoWalk import OrthoWalk
from OrthoDrive import OrthoDrive
import MazeGameGlobals
import MazeData
import MazeTreasure
import Trajectory
import Maze
import MinigameAvatarScorePanel
import MinigameGlobals

class DistributedMazeGame(DistributedMinigame):
    __module__ = __name__
    notify = directNotify.newCategory('DistributedMazeGame')
    CAMERA_TASK = 'MazeGameCameraTask'
    UPDATE_SUITS_TASK = 'MazeGameUpdateSuitsTask'
    TREASURE_GRAB_EVENT_NAME = 'MazeTreasureGrabbed'

    def __init__(self, cr):
        DistributedMinigame.__init__(self, cr)
        self.gameFSM = ClassicFSM.ClassicFSM('DistributedMazeGame', [State.State('off', self.enterOff, self.exitOff, ['play']),
         State.State('play', self.enterPlay, self.exitPlay, ['cleanup', 'showScores']),
         State.State('showScores', self.enterShowScores, self.exitShowScores, ['cleanup']),
         State.State('cleanup', self.enterCleanup, self.exitCleanup, [])], 'off', 'cleanup')
        self.addChildGameFSM(self.gameFSM)
        self.usesLookAround = 1

    def getTitle(self):
        return TTLocalizer.MazeGameTitle

    def getInstructions(self):
        return TTLocalizer.MazeGameInstructions

    def getMaxDuration(self):
        return MazeGameGlobals.GAME_DURATION

    def __defineConstants(self):
        self.TOON_SPEED = 8.0
        self.TOON_Z = 0
        self.MinSuitSpeedRange = [0.8 * self.TOON_SPEED, 0.6 * self.TOON_SPEED]
        self.MaxSuitSpeedRange = [1.1 * self.TOON_SPEED, 2.0 * self.TOON_SPEED]
        self.FASTER_SUIT_CURVE = 1
        self.SLOWER_SUIT_CURVE = self.getDifficulty() < 0.5
        self.slowerSuitPeriods = {2000: {4: [128, 76],
                8: [128,
                    99,
                    81,
                    68],
                12: [128,
                     108,
                     93,
                     82,
                     74,
                     67],
                16: [128,
                     112,
                     101,
                     91,
                     83,
                     76,
                     71,
                     66]},
         1000: {4: [110, 69],
                8: [110,
                    88,
                    73,
                    62],
                12: [110,
                     95,
                     83,
                     74,
                     67,
                     61],
                16: [110,
                     98,
                     89,
                     81,
                     75,
                     69,
                     64,
                     60]},
         5000: {4: [96, 63],
                8: [96,
                    79,
                    66,
                    57],
                12: [96,
                     84,
                     75,
                     67,
                     61,
                     56],
                16: [96,
                     87,
                     80,
                     73,
                     68,
                     63,
                     59,
                     55]},
         4000: {4: [86, 58],
                8: [86,
                    71,
                    61,
                    53],
                12: [86,
                     76,
                     68,
                     62,
                     56,
                     52],
                16: [86,
                     78,
                     72,
                     67,
                     62,
                     58,
                     54,
                     51]},
         3000: {4: [78, 54],
                8: [78,
                    65,
                    56,
                    49],
                12: [78,
                     69,
                     62,
                     57,
                     52,
                     48],
                16: [78,
                     71,
                     66,
                     61,
                     57,
                     54,
                     51,
                     48]},
         9000: {4: [71, 50],
                8: [71,
                    60,
                    52,
                    46],
                12: [71,
                     64,
                     58,
                     53,
                     49,
                     45],
                16: [71,
                     65,
                     61,
                     57,
                     53,
                     50,
                     47,
                     45]}}
        self.slowerSuitPeriodsCurve = {2000: {4: [128, 65],
                8: [128,
                    78,
                    66,
                    64],
                12: [128,
                     88,
                     73,
                     67,
                     64,
                     64],
                16: [128,
                     94,
                     79,
                     71,
                     67,
                     65,
                     64,
                     64]},
         1000: {4: [110, 59],
                8: [110,
                    70,
                    60,
                    58],
                12: [110,
                     78,
                     66,
                     61,
                     59,
                     58],
                16: [110,
                     84,
                     72,
                     65,
                     61,
                     59,
                     58,
                     58]},
         5000: {4: [96, 55],
                8: [96,
                    64,
                    56,
                    54],
                12: [96,
                     71,
                     61,
                     56,
                     54,
                     54],
                16: [96,
                     76,
                     65,
                     59,
                     56,
                     55,
                     54,
                     54]},
         4000: {4: [86, 51],
                8: [86,
                    59,
                    52,
                    50],
                12: [86,
                     65,
                     56,
                     52,
                     50,
                     50],
                16: [86,
                     69,
                     60,
                     55,
                     52,
                     51,
                     50,
                     50]},
         3000: {4: [78, 47],
                8: [78,
                    55,
                    48,
                    47],
                12: [78,
                     60,
                     52,
                     48,
                     47,
                     47],
                16: [78,
                     63,
                     55,
                     51,
                     49,
                     47,
                     47,
                     47]},
         9000: {4: [71, 44],
                8: [71,
                    51,
                    45,
                    44],
                12: [71,
                     55,
                     48,
                     45,
                     44,
                     44],
                16: [71,
                     58,
                     51,
                     48,
                     45,
                     44,
                     44,
                     44]}}
        self.fasterSuitPeriods = {2000: {4: [54, 42],
                8: [59,
                    52,
                    47,
                    42],
                12: [61,
                     56,
                     52,
                     48,
                     45,
                     42],
                16: [61,
                     58,
                     54,
                     51,
                     49,
                     46,
                     44,
                     42]},
         1000: {4: [50, 40],
                8: [55,
                    48,
                    44,
                    40],
                12: [56,
                     52,
                     48,
                     45,
                     42,
                     40],
                16: [56,
                     53,
                     50,
                     48,
                     45,
                     43,
                     41,
                     40]},
         5000: {4: [47, 37],
                8: [51,
                    45,
                    41,
                    37],
                12: [52,
                     48,
                     45,
                     42,
                     39,
                     37],
                16: [52,
                     49,
                     47,
                     44,
                     42,
                     40,
                     39,
                     37]},
         4000: {4: [44, 35],
                8: [47,
                    42,
                    38,
                    35],
                12: [48,
                     45,
                     42,
                     39,
                     37,
                     35],
                16: [49,
                     46,
                     44,
                     42,
                     40,
                     38,
                     37,
                     35]},
         3000: {4: [41, 33],
                8: [44,
                    40,
                    36,
                    33],
                12: [45,
                     42,
                     39,
                     37,
                     35,
                     33],
                16: [45,
                     43,
                     41,
                     39,
                     38,
                     36,
                     35,
                     33]},
         9000: {4: [39, 32],
                8: [41,
                    37,
                    34,
                    32],
                12: [42,
                     40,
                     37,
                     35,
                     33,
                     32],
                16: [43,
                     41,
                     39,
                     37,
                     35,
                     34,
                     33,
                     32]}}
        self.fasterSuitPeriodsCurve = {2000: {4: [62, 42],
                8: [63,
                    61,
                    54,
                    42],
                12: [63,
                     63,
                     61,
                     56,
                     50,
                     42],
                16: [63,
                     63,
                     62,
                     60,
                     57,
                     53,
                     48,
                     42]},
         1000: {4: [57, 40],
                8: [58,
                    56,
                    50,
                    40],
                12: [58,
                     58,
                     56,
                     52,
                     46,
                     40],
                16: [58,
                     58,
                     57,
                     56,
                     53,
                     49,
                     45,
                     40]},
         5000: {4: [53, 37],
                8: [54,
                    52,
                    46,
                    37],
                12: [54,
                     53,
                     52,
                     48,
                     43,
                     37],
                16: [54,
                     54,
                     53,
                     51,
                     49,
                     46,
                     42,
                     37]},
         4000: {4: [49, 35],
                8: [50,
                    48,
                    43,
                    35],
                12: [50,
                     49,
                     48,
                     45,
                     41,
                     35],
                16: [50,
                     50,
                     49,
                     48,
                     46,
                     43,
                     39,
                     35]},
         3000: {4: [46, 33],
                8: [47,
                    45,
                    41,
                    33],
                12: [47,
                     46,
                     45,
                     42,
                     38,
                     33],
                16: [47,
                     46,
                     46,
                     45,
                     43,
                     40,
                     37,
                     33]},
         9000: {4: [43, 32],
                8: [44,
                    42,
                    38,
                    32],
                12: [44,
                     43,
                     42,
                     40,
                     36,
                     32],
                16: [44,
                     44,
                     43,
                     42,
                     40,
                     38,
                     35,
                     32]}}
        self.CELL_WIDTH = MazeData.CELL_WIDTH
        self.MAX_FRAME_MOVE = self.CELL_WIDTH / 2
        startOffset = 3
        self.startPosHTable = [[Point3(0, startOffset, self.TOON_Z), 0],
         [Point3(0, -startOffset, self.TOON_Z), 180],
         [Point3(startOffset, 0, self.TOON_Z), 270],
         [Point3(-startOffset, 0, self.TOON_Z), 90]]
        self.camOffset = Vec3(0, -19, 45)

    def load(self):
        self.notify.debug('load')
        DistributedMinigame.load(self)
        self.__defineConstants()
        mazeName = MazeGameGlobals.getMazeName(self.doId, self.numPlayers, MazeData.mazeNames)
        self.maze = Maze.Maze(mazeName)
        model = loader.loadModel('phase_3.5/models/props/mickeySZ')
        self.treasureModel = model.find('**/mickeySZ')
        model.removeNode()
        self.treasureModel.setScale(1.6)
        self.treasureModel.setP(-90)
        self.music = base.loadMusic('phase_4/audio/bgm/MG_toontag.mid')
        self.toonHitTracks = {}
        self.scorePanels = []

    def unload(self):
        self.notify.debug('unload')
        DistributedMinigame.unload(self)
        del self.toonHitTracks
        self.maze.destroy()
        del self.maze
        self.treasureModel.removeNode()
        del self.treasureModel
        del self.music
        self.removeChildGameFSM(self.gameFSM)
        del self.gameFSM

    def onstage(self):
        self.notify.debug('onstage')
        DistributedMinigame.onstage(self)
        self.maze.onstage()
        self.randomNumGen.shuffle(self.startPosHTable)
        lt = base.localAvatar
        lt.reparentTo(render)
        lt.hideName()
        self.__placeToon(self.localAvId)
        lt.setAnimState('Happy', 1.0)
        lt.setSpeed(0, 0)
        self.camParent = render.attachNewNode('mazeGameCamParent')
        self.camParent.reparentTo(base.localAvatar)
        self.camParent.setPos(0, 0, 0)
        self.camParent.setHpr(render, 0, 0, 0)
        camera.reparentTo(self.camParent)
        camera.setPos(self.camOffset)
        self.__spawnCameraTask()
        self.toonRNGs = []
        for i in xrange(self.numPlayers):
            self.toonRNGs.append(RandomNumGen.RandomNumGen(self.randomNumGen))

        self.treasures = []
        for i in xrange(self.maze.numTreasures):
            self.treasures.append(MazeTreasure.MazeTreasure(self.treasureModel, self.maze.treasurePosList[i], i, self.doId))

        self.__loadSuits()
        for suit in self.suits:
            suit.onstage()

        self.sndTable = {'hitBySuit': [None] * self.numPlayers,
         'falling': [None] * self.numPlayers}
        for i in xrange(self.numPlayers):
            self.sndTable['hitBySuit'][i] = base.loadSfx('phase_4/audio/sfx/MG_Tag_C.mp3')
            self.sndTable['falling'][i] = base.loadSfx('phase_4/audio/sfx/MG_cannon_whizz.mp3')

        self.grabSounds = []
        for i in xrange(5):
            self.grabSounds.append(base.loadSfx('phase_4/audio/sfx/MG_maze_pickup.mp3'))

        self.grabSoundIndex = 0
        for avId in self.avIdList:
            self.toonHitTracks[avId] = Wait(0.1)

        self.scores = [0] * self.numPlayers
        self.goalBar = DirectWaitBar(parent=render2d, relief=DGG.SUNKEN, frameSize=(-0.35,
         0.35,
         -0.15,
         0.15), borderWidth=(0.02, 0.02), scale=0.42, pos=(0.84, 0, 0.5 - 0.28 * self.numPlayers + 0.05), barColor=(0, 0.7, 0, 1))
        self.goalBar.setBin('unsorted', 0)
        self.goalBar.hide()
        self.introTrack = self.getIntroTrack()
        self.introTrack.start()
        return

    def offstage(self):
        self.notify.debug('offstage')
        if self.introTrack.isPlaying():
            self.introTrack.finish()
        del self.introTrack
        for avId in self.toonHitTracks.keys():
            track = self.toonHitTracks[avId]
            if track.isPlaying():
                track.finish()

        self.__killCameraTask()
        camera.wrtReparentTo(render)
        self.camParent.removeNode()
        del self.camParent
        for panel in self.scorePanels:
            panel.cleanup()

        self.scorePanels = []
        self.goalBar.destroy()
        del self.goalBar
        base.setCellsAvailable(base.rightCells, 1)
        for suit in self.suits:
            suit.offstage()

        self.__unloadSuits()
        for treasure in self.treasures:
            treasure.destroy()

        del self.treasures
        del self.sndTable
        del self.grabSounds
        del self.toonRNGs
        self.maze.offstage()
        base.localAvatar.showName()
        DistributedMinigame.offstage(self)

    def __placeToon(self, avId):
        toon = self.getAvatar(avId)
        if self.numPlayers == 1:
            toon.setPos(0, 0, self.TOON_Z)
            toon.setHpr(180, 0, 0)
        else:
            posIndex = self.avIdList.index(avId)
            toon.setPos(self.startPosHTable[posIndex][0])
            toon.setHpr(self.startPosHTable[posIndex][1], 0, 0)

    def setGameReady(self):
        if not self.hasLocalToon:
            return
        self.notify.debug('setGameReady')
        if DistributedMinigame.setGameReady(self):
            return
        for avId in self.remoteAvIdList:
            toon = self.getAvatar(avId)
            if toon:
                toon.reparentTo(render)
                self.__placeToon(avId)
                toon.setAnimState('Happy', 1.0)
                toon.startSmooth()
                toon.startLookAround()

    def setGameStart(self, timestamp):
        if not self.hasLocalToon:
            return
        self.notify.debug('setGameStart')
        DistributedMinigame.setGameStart(self, timestamp)
        if self.introTrack.isPlaying():
            self.introTrack.finish()
        for avId in self.remoteAvIdList:
            toon = self.getAvatar(avId)
            if toon:
                toon.stopLookAround()

        self.gameFSM.request('play')

    def handleDisabledAvatar(self, avId):
        hitTrack = self.toonHitTracks[avId]
        if hitTrack.isPlaying():
            hitTrack.finish()
        DistributedMinigame.handleDisabledAvatar(self, avId)

    def enterOff(self):
        self.notify.debug('enterOff')

    def exitOff(self):
        pass

    def enterPlay(self):
        self.notify.debug('enterPlay')
        for i in xrange(self.numPlayers):
            avId = self.avIdList[i]
            avName = self.getAvatarName(avId)
            scorePanel = MinigameAvatarScorePanel.MinigameAvatarScorePanel(avId, avName)
            scorePanel.setPos(1.12, 0.0, 0.5 - 0.28 * i)
            self.scorePanels.append(scorePanel)

        self.goalBar.show()
        self.goalBar['value'] = 0.0
        base.setCellsAvailable(base.rightCells, 0)
        self.__spawnUpdateSuitsTask()
        orthoDrive = OrthoDrive(self.TOON_SPEED, maxFrameMove=self.MAX_FRAME_MOVE, customCollisionCallback=self.__doMazeCollisions, priority=1)
        self.orthoWalk = OrthoWalk(orthoDrive, broadcast=not self.isSinglePlayer())
        self.orthoWalk.start()
        self.accept(MazeSuit.COLLISION_EVENT_NAME, self.__hitBySuit)
        self.accept(self.TREASURE_GRAB_EVENT_NAME, self.__treasureGrabbed)
        self.timer = ToontownTimer.ToontownTimer()
        self.timer.posInTopRightCorner()
        self.timer.setTime(MazeGameGlobals.GAME_DURATION)
        self.timer.countdown(MazeGameGlobals.GAME_DURATION, self.timerExpired)
        self.accept('resetClock', self.__resetClock)
        base.playMusic(self.music, looping=0, volume=0.8)

    def exitPlay(self):
        self.notify.debug('exitPlay')
        self.ignore('resetClock')
        self.ignore(MazeSuit.COLLISION_EVENT_NAME)
        self.ignore(self.TREASURE_GRAB_EVENT_NAME)
        self.orthoWalk.stop()
        self.orthoWalk.destroy()
        del self.orthoWalk
        self.__killUpdateSuitsTask()
        self.timer.stop()
        self.timer.destroy()
        del self.timer
        for avId in self.avIdList:
            toon = self.getAvatar(avId)
            if toon:
                toon.loop('neutral')

    def __resetClock(self, tOffset):
        self.notify.debug('resetClock')
        self.gameStartTime += tOffset
        self.timer.countdown(self.timer.currentTime + tOffset, self.timerExpired)

    def __treasureGrabbed(self, treasureNum):
        self.treasures[treasureNum].showGrab()
        self.grabSounds[self.grabSoundIndex].play()
        self.grabSoundIndex = (self.grabSoundIndex + 1) % len(self.grabSounds)
        self.sendUpdate('claimTreasure', [treasureNum])

    def setTreasureGrabbed(self, avId, treasureNum):
        if not self.hasLocalToon:
            return
        if avId != self.localAvId:
            self.treasures[treasureNum].showGrab()
        i = self.avIdList.index(avId)
        self.scores[i] += 1
        self.scorePanels[i].setScore(self.scores[i])
        total = 0
        for score in self.scores:
            total += score

        self.goalBar['value'] = 100.0 * (float(total) / float(self.maze.numTreasures))

    def __hitBySuit(self, suitNum):
        self.notify.debug('hitBySuit')
        timestamp = globalClockDelta.localToNetworkTime(globalClock.getFrameTime())
        self.sendUpdate('hitBySuit', [self.localAvId, timestamp])
        self.__showToonHitBySuit(self.localAvId, timestamp)

    def hitBySuit(self, avId, timestamp):
        if not self.hasLocalToon:
            return
        if self.gameFSM.getCurrentState().getName() not in ['play', 'showScores']:
            self.notify.warning('ignoring msg: av %s hit by suit' % avId)
            return
        self.notify.debug('avatar ' + `avId` + ' hit by a suit')
        if avId != self.localAvId:
            self.__showToonHitBySuit(avId, timestamp)

    def __showToonHitBySuit--- This code section failed: ---

0	LOAD_FAST         'self'
3	LOAD_ATTR         'getAvatar'
6	LOAD_FAST         'avId'
9	CALL_FUNCTION_1   None
12	STORE_DEREF       'toon'

15	LOAD_DEREF        'toon'
18	LOAD_CONST        None
21	COMPARE_OP        '=='
24	JUMP_IF_FALSE     '34'

27	LOAD_CONST        None
30	RETURN_VALUE      None
31	JUMP_FORWARD      '34'
34_0	COME_FROM         '31'

34	LOAD_FAST         'self'
37	LOAD_ATTR         'toonRNGs'
40	LOAD_FAST         'self'
43	LOAD_ATTR         'avIdList'
46	LOAD_ATTR         'index'
49	LOAD_FAST         'avId'
52	CALL_FUNCTION_1   None
55	BINARY_SUBSCR     None
56	STORE_FAST        'rng'

59	LOAD_DEREF        'toon'
62	LOAD_ATTR         'getPos'
65	LOAD_GLOBAL       'render'
68	CALL_FUNCTION_1   None
71	STORE_FAST        'curPos'

74	LOAD_FAST         'self'
77	LOAD_ATTR         'toonHitTracks'
80	LOAD_FAST         'avId'
83	BINARY_SUBSCR     None
84	STORE_FAST        'oldTrack'

87	LOAD_FAST         'oldTrack'
90	LOAD_ATTR         'isPlaying'
93	CALL_FUNCTION_0   None
96	JUMP_IF_FALSE     '112'

99	LOAD_FAST         'oldTrack'
102	LOAD_ATTR         'finish'
105	CALL_FUNCTION_0   None
108	POP_TOP           None
109	JUMP_FORWARD      '112'
112_0	COME_FROM         '109'

112	LOAD_DEREF        'toon'
115	LOAD_ATTR         'setPos'
118	LOAD_FAST         'curPos'
121	CALL_FUNCTION_1   None
124	POP_TOP           None

125	LOAD_DEREF        'toon'
128	LOAD_ATTR         'setZ'
131	LOAD_FAST         'self'
134	LOAD_ATTR         'TOON_Z'
137	CALL_FUNCTION_1   None
140	POP_TOP           None

141	LOAD_GLOBAL       'render'
144	LOAD_ATTR         'attachNewNode'
147	LOAD_CONST        'mazeFlyToonParent-'
150	LOAD_FAST         'avId'
153	UNARY_CONVERT     None
154	BINARY_ADD        None
155	CALL_FUNCTION_1   None
158	STORE_FAST        'parentNode'

161	LOAD_FAST         'parentNode'
164	LOAD_ATTR         'setPos'
167	LOAD_DEREF        'toon'
170	LOAD_ATTR         'getPos'
173	CALL_FUNCTION_0   None
176	CALL_FUNCTION_1   None
179	POP_TOP           None

180	LOAD_DEREF        'toon'
183	LOAD_ATTR         'reparentTo'
186	LOAD_FAST         'parentNode'
189	CALL_FUNCTION_1   None
192	POP_TOP           None

193	LOAD_DEREF        'toon'
196	LOAD_ATTR         'setPos'
199	LOAD_CONST        0
202	LOAD_CONST        0
205	LOAD_CONST        0
208	CALL_FUNCTION_3   None
211	POP_TOP           None

212	LOAD_FAST         'parentNode'
215	LOAD_ATTR         'getPos'
218	CALL_FUNCTION_0   None
221	STORE_FAST        'startPos'

224	LOAD_DEREF        'toon'
227	LOAD_ATTR         'dropShadow'
230	LOAD_ATTR         'copyTo'
233	LOAD_FAST         'parentNode'
236	CALL_FUNCTION_1   None
239	STORE_FAST        'dropShadow'

242	LOAD_FAST         'dropShadow'
245	LOAD_ATTR         'setScale'
248	LOAD_DEREF        'toon'
251	LOAD_ATTR         'dropShadow'
254	LOAD_ATTR         'getScale'
257	LOAD_GLOBAL       'render'
260	CALL_FUNCTION_1   None
263	CALL_FUNCTION_1   None
266	POP_TOP           None

267	LOAD_GLOBAL       'Trajectory'
270	LOAD_ATTR         'Trajectory'
273	LOAD_CONST        0

276	LOAD_GLOBAL       'Point3'
279	LOAD_CONST        0
282	LOAD_CONST        0
285	LOAD_CONST        0
288	CALL_FUNCTION_3   None

291	LOAD_GLOBAL       'Point3'
294	LOAD_CONST        0
297	LOAD_CONST        0
300	LOAD_CONST        50
303	CALL_FUNCTION_3   None

306	LOAD_CONST        'gravMult'
309	LOAD_CONST        1.0
312	CALL_FUNCTION_259 None
315	STORE_FAST        'trajectory'

318	LOAD_FAST         'trajectory'
321	LOAD_ATTR         'calcTimeOfImpactOnPlane'
324	LOAD_CONST        0.0
327	CALL_FUNCTION_1   None
330	STORE_FAST        'flyDur'

333	SETUP_LOOP        '429'

336	LOAD_FAST         'rng'
339	LOAD_ATTR         'randint'
342	LOAD_CONST        2
345	LOAD_FAST         'self'
348	LOAD_ATTR         'maze'
351	LOAD_ATTR         'width'
354	LOAD_CONST        1
357	BINARY_SUBTRACT   None
358	CALL_FUNCTION_2   None
361	LOAD_FAST         'rng'
364	LOAD_ATTR         'randint'
367	LOAD_CONST        2
370	LOAD_FAST         'self'
373	LOAD_ATTR         'maze'
376	LOAD_ATTR         'height'
379	LOAD_CONST        1
382	BINARY_SUBTRACT   None
383	CALL_FUNCTION_2   None
386	BUILD_LIST_2      None
389	STORE_FAST        'endTile'

392	LOAD_FAST         'self'
395	LOAD_ATTR         'maze'
398	LOAD_ATTR         'isWalkable'
401	LOAD_FAST         'endTile'
404	LOAD_CONST        0
407	BINARY_SUBSCR     None
408	LOAD_FAST         'endTile'
411	LOAD_CONST        1
414	BINARY_SUBSCR     None
415	CALL_FUNCTION_2   None
418	JUMP_IF_FALSE     '425'

421	BREAK_LOOP        None
422	JUMP_BACK         '336'
425	JUMP_BACK         '336'
428	POP_BLOCK         None
429_0	COME_FROM         '333'

429	LOAD_FAST         'self'
432	LOAD_ATTR         'maze'
435	LOAD_ATTR         'tile2world'
438	LOAD_FAST         'endTile'
441	LOAD_CONST        0
444	BINARY_SUBSCR     None
445	LOAD_FAST         'endTile'
448	LOAD_CONST        1
451	BINARY_SUBSCR     None
452	CALL_FUNCTION_2   None
455	STORE_FAST        'endWorldCoords'

458	LOAD_GLOBAL       'Point3'
461	LOAD_FAST         'endWorldCoords'
464	LOAD_CONST        0
467	BINARY_SUBSCR     None
468	LOAD_FAST         'endWorldCoords'
471	LOAD_CONST        1
474	BINARY_SUBSCR     None
475	LOAD_FAST         'startPos'
478	LOAD_CONST        2
481	BINARY_SUBSCR     None
482	CALL_FUNCTION_3   None
485	STORE_DEREF       'endPos'

488	LOAD_FAST         'startPos'
491	LOAD_DEREF        'endPos'
494	LOAD_FAST         'flyDur'
497	LOAD_FAST         'parentNode'
500	LOAD_DEREF        'toon'
503	LOAD_CONST        '<code_object flyFunc>'
506	MAKE_FUNCTION_5   None
509	STORE_FAST        'flyFunc'

512	LOAD_GLOBAL       'Sequence'
515	LOAD_GLOBAL       'LerpFunctionInterval'
518	LOAD_FAST         'flyFunc'

521	LOAD_CONST        'fromData'
524	LOAD_CONST        0.0
527	LOAD_CONST        'toData'
530	LOAD_FAST         'flyDur'

533	LOAD_CONST        'duration'
536	LOAD_FAST         'flyDur'

539	LOAD_CONST        'extraArgs'
542	LOAD_FAST         'trajectory'
545	BUILD_LIST_1      None
548	CALL_FUNCTION_1025 None

551	LOAD_CONST        'name'
554	LOAD_DEREF        'toon'
557	LOAD_ATTR         'uniqueName'
560	LOAD_CONST        'hitBySuit-fly'
563	CALL_FUNCTION_1   None
566	CALL_FUNCTION_257 None
569	STORE_FAST        'flyTrack'

572	LOAD_FAST         'avId'
575	LOAD_FAST         'self'
578	LOAD_ATTR         'localAvId'
581	COMPARE_OP        '!='
584	JUMP_IF_FALSE     '599'

587	LOAD_GLOBAL       'Sequence'
590	CALL_FUNCTION_0   None
593	STORE_FAST        'cameraTrack'
596	JUMP_FORWARD      '815'

599	LOAD_FAST         'self'
602	LOAD_ATTR         'camParent'
605	LOAD_ATTR         'reparentTo'
608	LOAD_FAST         'parentNode'
611	CALL_FUNCTION_1   None
614	POP_TOP           None

615	LOAD_GLOBAL       'camera'
618	LOAD_ATTR         'getPos'
621	CALL_FUNCTION_0   None
624	STORE_FAST        'startCamPos'

627	LOAD_GLOBAL       'camera'
630	LOAD_ATTR         'getPos'
633	CALL_FUNCTION_0   None
636	STORE_FAST        'destCamPos'

639	LOAD_FAST         'trajectory'
642	LOAD_ATTR         'getPos'
645	LOAD_FAST         'flyDur'
648	LOAD_CONST        2.0
651	BINARY_DIVIDE     None
652	CALL_FUNCTION_1   None
655	LOAD_CONST        2
658	BINARY_SUBSCR     None
659	STORE_FAST        'zenith'

662	LOAD_FAST         'destCamPos'
665	LOAD_ATTR         'setZ'
668	LOAD_FAST         'zenith'
671	LOAD_CONST        1.3
674	BINARY_MULTIPLY   None
675	CALL_FUNCTION_1   None
678	POP_TOP           None

679	LOAD_FAST         'destCamPos'
682	LOAD_ATTR         'setY'
685	LOAD_FAST         'destCamPos'
688	LOAD_CONST        1
691	BINARY_SUBSCR     None
692	LOAD_CONST        0.3
695	BINARY_MULTIPLY   None
696	CALL_FUNCTION_1   None
699	POP_TOP           None

700	LOAD_FAST         'zenith'
703	LOAD_DEREF        'toon'
706	LOAD_FAST         'startCamPos'
709	LOAD_FAST         'destCamPos'
712	LOAD_FAST         'startCamPos'
715	BINARY_SUBTRACT   None
716	LOAD_CLOSURE      'toon'
719	LOAD_CONST        '<code_object camTask>'
722	MAKE_CLOSURE_4    None
725	STORE_FAST        'camTask'

728	LOAD_CONST        'mazeToonFlyCam-'
731	LOAD_FAST         'avId'
734	UNARY_CONVERT     None
735	BINARY_ADD        None
736	STORE_FAST        'camTaskName'

739	LOAD_GLOBAL       'taskMgr'
742	LOAD_ATTR         'add'
745	LOAD_FAST         'camTask'
748	LOAD_FAST         'camTaskName'
751	LOAD_CONST        'priority'
754	LOAD_CONST        20
757	CALL_FUNCTION_258 None
760	POP_TOP           None

761	LOAD_FAST         'self'
764	LOAD_DEREF        'toon'
767	LOAD_FAST         'camTaskName'
770	LOAD_FAST         'startCamPos'
773	LOAD_CONST        '<code_object cleanupCamTask>'
776	MAKE_FUNCTION_4   None
779	STORE_FAST        'cleanupCamTask'

782	LOAD_GLOBAL       'Sequence'
785	LOAD_GLOBAL       'Wait'
788	LOAD_FAST         'flyDur'
791	CALL_FUNCTION_1   None

794	LOAD_GLOBAL       'Func'
797	LOAD_FAST         'cleanupCamTask'
800	CALL_FUNCTION_1   None

803	LOAD_CONST        'name'
806	LOAD_CONST        'hitBySuit-cameraLerp'
809	CALL_FUNCTION_258 None
812	STORE_FAST        'cameraTrack'
815_0	COME_FROM         '596'

815	LOAD_DEREF        'toon'
818	LOAD_ATTR         'getGeomNode'
821	CALL_FUNCTION_0   None
824	STORE_FAST        'geomNode'

827	LOAD_FAST         'geomNode'
830	LOAD_ATTR         'getHpr'
833	CALL_FUNCTION_0   None
836	STORE_FAST        'startHpr'

839	LOAD_GLOBAL       'Point3'
842	LOAD_FAST         'startHpr'
845	CALL_FUNCTION_1   None
848	STORE_FAST        'destHpr'

851	LOAD_FAST         'rng'
854	LOAD_ATTR         'randrange'
857	LOAD_CONST        1
860	LOAD_CONST        8
863	CALL_FUNCTION_2   None
866	STORE_FAST        'hRot'

869	LOAD_FAST         'rng'
872	LOAD_ATTR         'choice'
875	LOAD_CONST        0
878	LOAD_CONST        1
881	BUILD_LIST_2      None
884	CALL_FUNCTION_1   None
887	JUMP_IF_FALSE     '900'

890	LOAD_FAST         'hRot'
893	UNARY_NEGATIVE    None
894	STORE_FAST        'hRot'
897	JUMP_FORWARD      '900'
900_0	COME_FROM         '897'

900	LOAD_FAST         'destHpr'
903	LOAD_ATTR         'setX'
906	LOAD_FAST         'destHpr'
909	LOAD_CONST        0
912	BINARY_SUBSCR     None
913	LOAD_FAST         'hRot'
916	LOAD_CONST        360
919	BINARY_MULTIPLY   None
920	BINARY_ADD        None
921	CALL_FUNCTION_1   None
924	POP_TOP           None

925	LOAD_GLOBAL       'Sequence'
928	LOAD_GLOBAL       'LerpHprInterval'
931	LOAD_FAST         'geomNode'
934	LOAD_FAST         'flyDur'
937	LOAD_FAST         'destHpr'
940	LOAD_CONST        'startHpr'
943	LOAD_FAST         'startHpr'
946	CALL_FUNCTION_259 None

949	LOAD_GLOBAL       'Func'
952	LOAD_FAST         'geomNode'
955	LOAD_ATTR         'setHpr'
958	LOAD_FAST         'startHpr'
961	CALL_FUNCTION_2   None

964	LOAD_CONST        'name'
967	LOAD_DEREF        'toon'
970	LOAD_ATTR         'uniqueName'
973	LOAD_CONST        'hitBySuit-spinH'
976	CALL_FUNCTION_1   None
979	CALL_FUNCTION_258 None
982	STORE_FAST        'spinHTrack'

985	LOAD_FAST         'geomNode'
988	LOAD_ATTR         'getParent'
991	CALL_FUNCTION_0   None
994	STORE_FAST        'parent'

997	LOAD_FAST         'parent'
1000	LOAD_ATTR         'attachNewNode'
1003	LOAD_CONST        'rotNode'
1006	CALL_FUNCTION_1   None
1009	STORE_FAST        'rotNode'

1012	LOAD_FAST         'geomNode'
1015	LOAD_ATTR         'reparentTo'
1018	LOAD_FAST         'rotNode'
1021	CALL_FUNCTION_1   None
1024	POP_TOP           None

1025	LOAD_FAST         'rotNode'
1028	LOAD_ATTR         'setZ'
1031	LOAD_DEREF        'toon'
1034	LOAD_ATTR         'getHeight'
1037	CALL_FUNCTION_0   None
1040	LOAD_CONST        2.0
1043	BINARY_DIVIDE     None
1044	CALL_FUNCTION_1   None
1047	POP_TOP           None

1048	LOAD_FAST         'geomNode'
1051	LOAD_ATTR         'getZ'
1054	CALL_FUNCTION_0   None
1057	STORE_FAST        'oldGeomNodeZ'

1060	LOAD_FAST         'geomNode'
1063	LOAD_ATTR         'setZ'
1066	LOAD_DEREF        'toon'
1069	LOAD_ATTR         'getHeight'
1072	CALL_FUNCTION_0   None
1075	UNARY_NEGATIVE    None
1076	LOAD_CONST        2.0
1079	BINARY_DIVIDE     None
1080	CALL_FUNCTION_1   None
1083	POP_TOP           None

1084	LOAD_FAST         'rotNode'
1087	LOAD_ATTR         'getHpr'
1090	CALL_FUNCTION_0   None
1093	STORE_FAST        'startHpr'

1096	LOAD_GLOBAL       'Point3'
1099	LOAD_FAST         'startHpr'
1102	CALL_FUNCTION_1   None
1105	STORE_FAST        'destHpr'

1108	LOAD_FAST         'rng'
1111	LOAD_ATTR         'randrange'
1114	LOAD_CONST        1
1117	LOAD_CONST        3
1120	CALL_FUNCTION_2   None
1123	STORE_FAST        'pRot'

1126	LOAD_FAST         'rng'
1129	LOAD_ATTR         'choice'
1132	LOAD_CONST        0
1135	LOAD_CONST        1
1138	BUILD_LIST_2      None
1141	CALL_FUNCTION_1   None
1144	JUMP_IF_FALSE     '1157'

1147	LOAD_FAST         'pRot'
1150	UNARY_NEGATIVE    None
1151	STORE_FAST        'pRot'
1154	JUMP_FORWARD      '1157'
1157_0	COME_FROM         '1154'

1157	LOAD_FAST         'destHpr'
1160	LOAD_ATTR         'setY'
1163	LOAD_FAST         'destHpr'
1166	LOAD_CONST        1
1169	BINARY_SUBSCR     None
1170	LOAD_FAST         'pRot'
1173	LOAD_CONST        360
1176	BINARY_MULTIPLY   None
1177	BINARY_ADD        None
1178	CALL_FUNCTION_1   None
1181	POP_TOP           None

1182	LOAD_GLOBAL       'Sequence'
1185	LOAD_GLOBAL       'LerpHprInterval'
1188	LOAD_FAST         'rotNode'
1191	LOAD_FAST         'flyDur'
1194	LOAD_FAST         'destHpr'
1197	LOAD_CONST        'startHpr'
1200	LOAD_FAST         'startHpr'
1203	CALL_FUNCTION_259 None

1206	LOAD_GLOBAL       'Func'
1209	LOAD_FAST         'rotNode'
1212	LOAD_ATTR         'setHpr'
1215	LOAD_FAST         'startHpr'
1218	CALL_FUNCTION_2   None

1221	LOAD_CONST        'name'
1224	LOAD_DEREF        'toon'
1227	LOAD_ATTR         'uniqueName'
1230	LOAD_CONST        'hitBySuit-spinP'
1233	CALL_FUNCTION_1   None
1236	CALL_FUNCTION_258 None
1239	STORE_FAST        'spinPTrack'

1242	LOAD_FAST         'self'
1245	LOAD_ATTR         'avIdList'
1248	LOAD_ATTR         'index'
1251	LOAD_FAST         'avId'
1254	CALL_FUNCTION_1   None
1257	STORE_FAST        'i'

1260	LOAD_GLOBAL       'Sequence'
1263	LOAD_GLOBAL       'Func'
1266	LOAD_GLOBAL       'base'
1269	LOAD_ATTR         'playSfx'
1272	LOAD_FAST         'self'
1275	LOAD_ATTR         'sndTable'
1278	LOAD_CONST        'hitBySuit'
1281	BINARY_SUBSCR     None
1282	LOAD_FAST         'i'
1285	BINARY_SUBSCR     None
1286	CALL_FUNCTION_2   None

1289	LOAD_GLOBAL       'Wait'
1292	LOAD_FAST         'flyDur'
1295	LOAD_CONST        2.0
1298	LOAD_CONST        3.0
1301	BINARY_DIVIDE     None
1302	BINARY_MULTIPLY   None
1303	CALL_FUNCTION_1   None

1306	LOAD_GLOBAL       'SoundInterval'
1309	LOAD_FAST         'self'
1312	LOAD_ATTR         'sndTable'
1315	LOAD_CONST        'falling'
1318	BINARY_SUBSCR     None
1319	LOAD_FAST         'i'
1322	BINARY_SUBSCR     None

1323	LOAD_CONST        'duration'
1326	LOAD_FAST         'flyDur'
1329	LOAD_CONST        1.0
1332	LOAD_CONST        3.0
1335	BINARY_DIVIDE     None
1336	BINARY_MULTIPLY   None
1337	CALL_FUNCTION_257 None

1340	LOAD_CONST        'name'
1343	LOAD_DEREF        'toon'
1346	LOAD_ATTR         'uniqueName'
1349	LOAD_CONST        'hitBySuit-soundTrack'
1352	CALL_FUNCTION_1   None
1355	CALL_FUNCTION_259 None
1358	STORE_FAST        'soundTrack'

1361	LOAD_FAST         'self'
1364	LOAD_FAST         'avId'
1367	LOAD_DEREF        'toon'
1370	LOAD_FAST         'dropShadow'
1373	LOAD_CONST        '<code_object preFunc>'
1376	MAKE_FUNCTION_4   None
1379	STORE_FAST        'preFunc'

1382	LOAD_FAST         'self'
1385	LOAD_FAST         'avId'
1388	LOAD_FAST         'oldGeomNodeZ'
1391	LOAD_FAST         'dropShadow'
1394	LOAD_FAST         'parentNode'
1397	LOAD_CLOSURE      'toon'
1400	LOAD_CLOSURE      'endPos'
1403	LOAD_CONST        '<code_object postFunc>'
1406	MAKE_CLOSURE_5    None
1409	STORE_FAST        'postFunc'

1412	LOAD_FAST         'preFunc'
1415	CALL_FUNCTION_0   None
1418	POP_TOP           None

1419	LOAD_GLOBAL       'Sequence'
1422	LOAD_GLOBAL       'Parallel'
1425	LOAD_FAST         'flyTrack'
1428	LOAD_FAST         'cameraTrack'

1431	LOAD_FAST         'spinHTrack'
1434	LOAD_FAST         'spinPTrack'
1437	LOAD_FAST         'soundTrack'
1440	CALL_FUNCTION_5   None

1443	LOAD_GLOBAL       'Func'
1446	LOAD_FAST         'postFunc'
1449	CALL_FUNCTION_1   None

1452	LOAD_CONST        'name'
1455	LOAD_DEREF        'toon'
1458	LOAD_ATTR         'uniqueName'
1461	LOAD_CONST        'hitBySuit'
1464	CALL_FUNCTION_1   None
1467	CALL_FUNCTION_258 None
1470	STORE_FAST        'hitTrack'

1473	LOAD_FAST         'hitTrack'
1476	LOAD_FAST         'self'
1479	LOAD_ATTR         'toonHitTracks'
1482	LOAD_FAST         'avId'
1485	STORE_SUBSCR      None

1486	LOAD_FAST         'hitTrack'
1489	LOAD_ATTR         'start'
1492	LOAD_GLOBAL       'globalClockDelta'
1495	LOAD_ATTR         'localElapsedTime'
1498	LOAD_FAST         'timestamp'
1501	CALL_FUNCTION_1   None
1504	CALL_FUNCTION_1   None
1507	POP_TOP           None
1508	LOAD_CONST        None
1511	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 428

    def allTreasuresTaken(self):
        if not self.hasLocalToon:
            return
        self.notify.debug('all treasures taken')
        if not MazeGameGlobals.ENDLESS_GAME:
            self.gameFSM.request('showScores')

    def timerExpired(self):
        self.notify.debug('local timer expired')
        if not MazeGameGlobals.ENDLESS_GAME:
            self.gameFSM.request('showScores')

    def __doMazeCollisions(self, oldPos, newPos):
        offset = newPos - oldPos
        WALL_OFFSET = 1.0
        curX = oldPos[0]
        curY = oldPos[1]
        curTX, curTY = self.maze.world2tile(curX, curY)

        def calcFlushCoord(curTile, newTile, centerTile):
            EPSILON = 0.01
            if newTile > curTile:
                return (newTile - centerTile) * self.CELL_WIDTH - EPSILON - WALL_OFFSET
            else:
                return (curTile - centerTile) * self.CELL_WIDTH + WALL_OFFSET

        offsetX = offset[0]
        offsetY = offset[1]
        WALL_OFFSET_X = WALL_OFFSET
        if offsetX < 0:
            WALL_OFFSET_X = -WALL_OFFSET_X
        WALL_OFFSET_Y = WALL_OFFSET
        if offsetY < 0:
            WALL_OFFSET_Y = -WALL_OFFSET_Y
        newX = curX + offsetX + WALL_OFFSET_X
        newY = curY
        newTX, newTY = self.maze.world2tile(newX, newY)
        if newTX != curTX:
            if self.maze.collisionTable[newTY][newTX]:
                offset.setX(calcFlushCoord(curTX, newTX, self.maze.originTX) - curX)
        newX = curX
        newY = curY + offsetY + WALL_OFFSET_Y
        newTX, newTY = self.maze.world2tile(newX, newY)
        if newTY != curTY:
            if self.maze.collisionTable[newTY][newTX]:
                offset.setY(calcFlushCoord(curTY, newTY, self.maze.originTY) - curY)
        offsetX = offset[0]
        offsetY = offset[1]
        newX = curX + offsetX + WALL_OFFSET_X
        newY = curY + offsetY + WALL_OFFSET_Y
        newTX, newTY = self.maze.world2tile(newX, newY)
        if self.maze.collisionTable[newTY][newTX]:
            cX = calcFlushCoord(curTX, newTX, self.maze.originTX)
            cY = calcFlushCoord(curTY, newTY, self.maze.originTY)
            if abs(cX - curX) < abs(cY - curY):
                offset.setX(cX - curX)
            else:
                offset.setY(cY - curY)
        return oldPos + offset

    def __spawnCameraTask(self):
        self.notify.debug('spawnCameraTask')
        camera.lookAt(base.localAvatar)
        taskMgr.remove(self.CAMERA_TASK)
        taskMgr.add(self.__cameraTask, self.CAMERA_TASK, priority=45)

    def __killCameraTask(self):
        self.notify.debug('killCameraTask')
        taskMgr.remove(self.CAMERA_TASK)

    def __cameraTask(self, task):
        self.camParent.setHpr(render, 0, 0, 0)
        return Task.cont

    def __loadSuits(self):
        self.notify.debug('loadSuits')
        self.suits = []
        self.numSuits = 4 * self.numPlayers
        safeZone = self.getSafezoneId()
        slowerTable = self.slowerSuitPeriods
        if self.SLOWER_SUIT_CURVE:
            slowerTable = self.slowerSuitPeriodsCurve
        slowerPeriods = slowerTable[safeZone][self.numSuits]
        fasterTable = self.fasterSuitPeriods
        if self.FASTER_SUIT_CURVE:
            fasterTable = self.fasterSuitPeriodsCurve
        fasterPeriods = fasterTable[safeZone][self.numSuits]
        suitPeriods = slowerPeriods + fasterPeriods
        self.notify.debug('suit periods: ' + `suitPeriods`)
        self.randomNumGen.shuffle(suitPeriods)
        for i in xrange(self.numSuits):
            self.suits.append(MazeSuit(i, self.maze, self.randomNumGen, suitPeriods[i], self.getDifficulty()))

    def __unloadSuits(self):
        self.notify.debug('unloadSuits')
        for suit in self.suits:
            suit.destroy()

        del self.suits

    def __spawnUpdateSuitsTask(self):
        self.notify.debug('spawnUpdateSuitsTask')
        for suit in self.suits:
            suit.gameStart(self.gameStartTime)

        taskMgr.remove(self.UPDATE_SUITS_TASK)
        taskMgr.add(self.__updateSuitsTask, self.UPDATE_SUITS_TASK)

    def __killUpdateSuitsTask(self):
        self.notify.debug('killUpdateSuitsTask')
        taskMgr.remove(self.UPDATE_SUITS_TASK)
        for suit in self.suits:
            suit.gameEnd()

    def __updateSuitsTask(self, task):
        curT = globalClock.getFrameTime() - self.gameStartTime
        curTic = int(curT * float(MazeGameGlobals.SUIT_TIC_FREQ))
        suitUpdates = []
        for i in xrange(len(self.suits)):
            updateTics = self.suits[i].getThinkTimestampTics(curTic)
            suitUpdates.extend(zip(updateTics, [i] * len(updateTics)))

        suitUpdates.sort(lambda a, b: a[0] - b[0])
        if len(suitUpdates) > 0:
            curTic = 0
            for i in xrange(len(suitUpdates)):
                update = suitUpdates[i]
                tic = update[0]
                suitIndex = update[1]
                suit = self.suits[suitIndex]
                if tic > curTic:
                    curTic = tic
                    j = i + 1
                    while j < len(suitUpdates):
                        if suitUpdates[j][0] > tic:
                            break
                        self.suits[suitUpdates[j][1]].prepareToThink()
                        j += 1

                unwalkables = []
                for si in xrange(suitIndex):
                    unwalkables.extend(self.suits[si].occupiedTiles)

                for si in xrange(suitIndex + 1, len(self.suits)):
                    unwalkables.extend(self.suits[si].occupiedTiles)

                suit.think(curTic, curT, unwalkables)

        return Task.cont

    def enterShowScores(self):
        self.notify.debug('enterShowScores')
        lerpTrack = Parallel()
        lerpDur = 0.5
        lerpTrack.append(Parallel(LerpPosInterval(self.goalBar, lerpDur, Point3(0, 0, -0.6), blendType='easeInOut'), LerpScaleInterval(self.goalBar, lerpDur, Vec3(self.goalBar.getScale()) * 2.0, blendType='easeInOut')))
        tY = 0.6
        bY = -0.05
        lX = -0.5
        cX = 0
        rX = 0.5
        scorePanelLocs = (((cX, bY),),
         ((lX, bY), (rX, bY)),
         ((cX, tY), (lX, bY), (rX, bY)),
         ((lX, tY),
          (rX, tY),
          (lX, bY),
          (rX, bY)))
        scorePanelLocs = scorePanelLocs[self.numPlayers - 1]
        for i in xrange(self.numPlayers):
            panel = self.scorePanels[i]
            pos = scorePanelLocs[i]
            lerpTrack.append(Parallel(LerpPosInterval(panel, lerpDur, Point3(pos[0], 0, pos[1]), blendType='easeInOut'), LerpScaleInterval(panel, lerpDur, Vec3(panel.getScale()) * 2.0, blendType='easeInOut')))

        self.showScoreTrack = Parallel(lerpTrack, Sequence(Wait(MazeGameGlobals.SHOWSCORES_DURATION), Func(self.gameOver)))
        self.showScoreTrack.start()

    def exitShowScores(self):
        self.showScoreTrack.pause()
        del self.showScoreTrack

    def enterCleanup(self):
        self.notify.debug('enterCleanup')

    def exitCleanup(self):
        pass

    def getIntroTrack(self):
        self.__cameraTask(None)
        origCamParent = camera.getParent()
        origCamPos = camera.getPos()
        origCamHpr = camera.getHpr()
        iCamParent = base.localAvatar.attachNewNode('iCamParent')
        iCamParent.setH(180)
        camera.reparentTo(iCamParent)
        toonHeight = base.localAvatar.getHeight()
        camera.setPos(0, -15, toonHeight * 3)
        camera.lookAt(0, 0, toonHeight / 2.0)
        iCamParent.wrtReparentTo(origCamParent)
        waitDur = 5.0
        lerpDur = 4.5
        lerpTrack = Parallel()
        startHpr = iCamParent.getHpr()
        startHpr.setX(PythonUtil.reduceAngle(startHpr[0]))
        lerpTrack.append(LerpPosHprInterval(iCamParent, lerpDur, pos=Point3(0, 0, 0), hpr=Point3(0, 0, 0), startHpr=startHpr, name=self.uniqueName('introLerpParent')))
        lerpTrack.append(LerpPosHprInterval(camera, lerpDur, pos=origCamPos, hpr=origCamHpr, blendType='easeInOut', name=self.uniqueName('introLerpCameraPos')))
        base.localAvatar.startLookAround()

        def cleanup(origCamParent = origCamParent, origCamPos = origCamPos, origCamHpr = origCamHpr, iCamParent = iCamParent):
            camera.reparentTo(origCamParent)
            camera.setPos(origCamPos)
            camera.setHpr(origC
# Can't uncompyle C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\minigame\DistributedMazeGame.pyc
Traceback (most recent call last):
  File "C:\python27\lib\uncompyle2\__init__.py", line 206, in main
    uncompyle_file(infile, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 143, in uncompyle_file
    uncompyle(version, co, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 132, in uncompyle
    raise walk.ERROR
ParserError: --- This code section failed: ---

0	LOAD_FAST         'self'
3	LOAD_ATTR         'getAvatar'
6	LOAD_FAST         'avId'
9	CALL_FUNCTION_1   None
12	STORE_DEREF       'toon'

15	LOAD_DEREF        'toon'
18	LOAD_CONST        None
21	COMPARE_OP        '=='
24	JUMP_IF_FALSE     '34'

27	LOAD_CONST        None
30	RETURN_VALUE      None
31	JUMP_FORWARD      '34'
34_0	COME_FROM         '31'

34	LOAD_FAST         'self'
37	LOAD_ATTR         'toonRNGs'
40	LOAD_FAST         'self'
43	LOAD_ATTR         'avIdList'
46	LOAD_ATTR         'index'
49	LOAD_FAST         'avId'
52	CALL_FUNCTION_1   None
55	BINARY_SUBSCR     None
56	STORE_FAST        'rng'

59	LOAD_DEREF        'toon'
62	LOAD_ATTR         'getPos'
65	LOAD_GLOBAL       'render'
68	CALL_FUNCTION_1   None
71	STORE_FAST        'curPos'

74	LOAD_FAST         'self'
77	LOAD_ATTR         'toonHitTracks'
80	LOAD_FAST         'avId'
83	BINARY_SUBSCR     None
84	STORE_FAST        'oldTrack'

87	LOAD_FAST         'oldTrack'
90	LOAD_ATTR         'isPlaying'
93	CALL_FUNCTION_0   None
96	JUMP_IF_FALSE     '112'

99	LOAD_FAST         'oldTrack'
102	LOAD_ATTR         'finish'
105	CALL_FUNCTION_0   None
108	POP_TOP           None
109	JUMP_FORWARD      '112'
112_0	COME_FROM         '109'

112	LOAD_DEREF        'toon'
115	LOAD_ATTR         'setPos'
118	LOAD_FAST         'curPos'
121	CALL_FUNCTION_1   None
124	POP_TOP           None

125	LOAD_DEREF        'toon'
128	LOAD_ATTR         'setZ'
131	LOAD_FAST         'self'
134	LOAD_ATTR         'TOON_Z'
137	CALL_FUNCTION_1   None
140	POP_TOP           None

141	LOAD_GLOBAL       'render'
144	LOAD_ATTR         'attachNewNode'
147	LOAD_CONST        'mazeFlyToonParent-'
150	LOAD_FAST         'avId'
153	UNARY_CONVERT     None
154	BINARY_ADD        None
155	CALL_FUNCTION_1   None
158	STORE_FAST        'parentNode'

161	LOAD_FAST         'parentNode'
164	LOAD_ATTR         'setPos'
167	LOAD_DEREF        'toon'
170	LOAD_ATTR         'getPos'
173	CALL_FUNCTION_0   None
176	CALL_FUNCTION_1   None
179	POP_TOP           None

180	LOAD_DEREF        'toon'
183	LOAD_ATTR         'reparentTo'
186	LOAD_FAST         'parentNode'
189	CALL_FUNCTION_1   None
192	POP_TOP           None

193	LOAD_DEREF        'toon'
196	LOAD_ATTR         'setPos'
199	LOAD_CONST        0
202	LOAD_CONST        0
205	LOAD_CONST        0
208	CALL_FUNCTION_3   None
211	POP_TOP           None

212	LOAD_FAST         'parentNode'
215	LOAD_ATTR         'getPos'
218	CALL_FUNCTION_0   None
221	STORE_FAST        'startPos'

224	LOAD_DEREF        'toon'
227	LOAD_ATTR         'dropShadow'
230	LOAD_ATTR         'copyTo'
233	LOAD_FAST         'parentNode'
236	CALL_FUNCTION_1   None
239	STORE_FAST        'dropShadow'

242	LOAD_FAST         'dropShadow'
245	LOAD_ATTR         'setScale'
248	LOAD_DEREF        'toon'
251	LOAD_ATTR         'dropShadow'
254	LOAD_ATTR         'getScale'
257	LOAD_GLOBAL       'render'
260	CALL_FUNCTION_1   None
263	CALL_FUNCTION_1   None
266	POP_TOP           None

267	LOAD_GLOBAL       'Trajectory'
270	LOAD_ATTR         'Trajectory'
273	LOAD_CONST        0

276	LOAD_GLOBAL       'Point3'
279	LOAD_CONST        0
282	LOAD_CONST        0
285	LOAD_CONST        0
288	CALL_FUNCTION_3   None

291	LOAD_GLOBAL       'Point3'
294	LOAD_CONST        0
297	LOAD_CONST        0
300	LOAD_CONST        50
303	CALL_FUNCTION_3   None

306	LOAD_CONST        'gravMult'
309	LOAD_CONST        1.0
312	CALL_FUNCTION_259 None
315	STORE_FAST        'trajectory'

318	LOAD_FAST         'trajectory'
321	LOAD_ATTR         'calcTimeOfImpactOnPlane'
324	LOAD_CONST        0.0
327	CALL_FUNCTION_1   None
330	STORE_FAST        'flyDur'

333	SETUP_LOOP        '429'

336	LOAD_FAST         'rng'
339	LOAD_ATTR         'randint'
342	LOAD_CONST        2
345	LOAD_FAST         'self'
348	LOAD_ATTR         'maze'
351	LOAD_ATTR         'width'
354	LOAD_CONST        1
357	BINARY_SUBTRACT   None
358	CALL_FUNCTION_2   None
361	LOAD_FAST         'rng'
364	LOAD_ATTR         'randint'
367	LOAD_CONST        2
370	LOAD_FAST         'self'
373	LOAD_ATTR         'maze'
376	LOAD_ATTR         'height'
379	LOAD_CONST        1
382	BINARY_SUBTRACT   None
383	CALL_FUNCTION_2   None
386	BUILD_LIST_2      None
389	STORE_FAST        'endTile'

392	LOAD_FAST         'self'
395	LOAD_ATTR         'maze'
398	LOAD_ATTR         'isWalkable'
401	LOAD_FAST         'endTile'
404	LOAD_CONST        0
407	BINARY_SUBSCR     None
408	LOAD_FAST         'endTile'
411	LOAD_CONST        1
414	BINARY_SUBSCR     None
415	CALL_FUNCTION_2   None
418	JUMP_IF_FALSE     '425'

421	BREAK_LOOP        None
422	JUMP_BACK         '336'
425	JUMP_BACK         '336'
428	POP_BLOCK         None
429_0	COME_FROM         '333'

429	LOAD_FAST         'self'
432	LOAD_ATTR         'maze'
435	LOAD_ATTR         'tile2world'
438	LOAD_FAST         'endTile'
441	LOAD_CONST        0
444	BINARY_SUBSCR     None
445	LOAD_FAST         'endTile'
448	LOAD_CONST        1
451	BINARY_SUBSCR     None
452	CALL_FUNCTION_2   None
455	STORE_FAST        'endWorldCoords'

458	LOAD_GLOBAL       'Point3'
461	LOAD_FAST         'endWorldCoords'
464	LOAD_CONST        0
467	BINARY_SUBSCR     None
468	LOAD_FAST         'endWorldCoords'
471	LOAD_CONST        1
474	BINARY_SUBSCR     None
475	LOAD_FAST         'startPos'
478	LOAD_CONST        2
481	BINARY_SUBSCR     None
482	CALL_FUNCTION_3   None
485	STORE_DEREF       'endPos'

488	LOAD_FAST         'startPos'
491	LOAD_DEREF        'endPos'
494	LOAD_FAST         'flyDur'
497	LOAD_FAST         'parentNode'
500	LOAD_DEREF        'toon'
503	LOAD_CONST        '<code_object flyFunc>'
506	MAKE_FUNCTION_5   None
509	STORE_FAST        'flyFunc'

512	LOAD_GLOBAL       'Sequence'
515	LOAD_GLOBAL       'LerpFunctionInterval'
518	LOAD_FAST         'flyFunc'

521	LOAD_CONST        'fromData'
524	LOAD_CONST        0.0
527	LOAD_CONST        'toData'
530	LOAD_FAST         'flyDur'

533	LOAD_CONST        'duration'
536	LOAD_FAST         'flyDur'

539	LOAD_CONST        'extraArgs'
542	LOAD_FAST         'trajectory'
545	BUILD_LIST_1      None
548	CALL_FUNCTION_1025 None

551	LOAD_CONST        'name'
554	LOAD_DEREF        'toon'
557	LOAD_ATTR         'uniqueName'
560	LOAD_CONST        'hitBySuit-fly'
563	CALL_FUNCTION_1   None
566	CALL_FUNCTION_257 None
569	STORE_FAST        'flyTrack'

572	LOAD_FAST         'avId'
575	LOAD_FAST         'self'
578	LOAD_ATTR         'localAvId'
581	COMPARE_OP        '!='
584	JUMP_IF_FALSE     '599'

587	LOAD_GLOBAL       'Sequence'
590	CALL_FUNCTION_0   None
593	STORE_FAST        'cameraTrack'
596	JUMP_FORWARD      '815'

599	LOAD_FAST         'self'
602	LOAD_ATTR         'camParent'
605	LOAD_ATTR         'reparentTo'
608	LOAD_FAST         'parentNode'
611	CALL_FUNCTION_1   None
614	POP_TOP           None

615	LOAD_GLOBAL       'camera'
618	LOAD_ATTR         'getPos'
621	CALL_FUNCTION_0   None
624	STORE_FAST        'startCamPos'

627	LOAD_GLOBAL       'camera'
630	LOAD_ATTR         'getPos'
633	CALL_FUNCTION_0   None
636	STORE_FAST        'destCamPos'

639	LOAD_FAST         'trajectory'
642	LOAD_ATTR         'getPos'
645	LOAD_FAST         'flyDur'
648	LOAD_CONST        2.0
651	BINARY_DIVIDE     None
652	CALL_FUNCTION_1   None
655	LOAD_CONST        2
658	BINARY_SUBSCR     None
659	STORE_FAST        'zenith'

662	LOAD_FAST         'destCamPos'
665	LOAD_ATTR         'setZ'
668	LOAD_FAST         'zenith'
671	LOAD_CONST        1.3
674	BINARY_MULTIPLY   None
675	CALL_FUNCTION_1   None
678	POP_TOP           None

679	LOAD_FAST         'destCamPos'
682	LOAD_ATTR         'setY'
685	LOAD_FAST         'destCamPos'
688	LOAD_CONST        1
691	BINARY_SUBSCR     None
692	LOAD_CONST        0.3
695	BINARY_MULTIPLY   None
696	CALL_FUNCTION_1   None
699	POP_TOP           None

700	LOAD_FAST         'zenith'
703	LOAD_DEREF        'toon'
706	LOAD_FAST         'startCamPos'
709	LOAD_FAST         'destCamPos'
712	LOAD_FAST         'startCamPos'
715	BINARY_SUBTRACT   None
716	LOAD_CLOSURE      'toon'
719	LOAD_CONST        '<code_object camTask>'
722	MAKE_CLOSURE_4    None
725	STORE_FAST        'camTask'

728	LOAD_CONST        'mazeToonFlyCam-'
731	LOAD_FAST         'avId'
734	UNARY_CONVERT     None
735	BINARY_ADD        None
736	STORE_FAST        'camTaskName'

739	LOAD_GLOBAL       'taskMgr'
742	LOAD_ATTR         'add'
745	LOAD_FAST         'camTask'
748	LOAD_FAST         'camTaskName'
751	LOAD_CONST        'priority'
754	LOAD_CONST        20
757	CALL_FUNCTION_258 None
760	POP_TOP           None

761	LOAD_FAST         'self'
764	LOAD_DEREF        'toon'
767	LOAD_FAST         'camTaskName'
770	LOAD_FAST         'startCamPos'
773	LOAD_CONST        '<code_object cleanupCamTask>'
776	MAKE_FUNCTION_4   None
779	STORE_FAST        'cleanupCamTask'

782	LOAD_GLOBAL       'Sequence'
785	LOAD_GLOBAL       'Wait'
788	LOAD_FAST         'flyDur'
791	CALL_FUNCTION_1   None

794	LOAD_GLOBAL       'Func'
797	LOAD_FAST         'cleanupCamTask'
800	CALL_FUNCTION_1   None

803	LOAD_CONST        'name'
806	LOAD_CONST        'hitBySuit-cameraLerp'
809	CALL_FUNCTION_258 None
812	STORE_FAST        'cameraTrack'
815_0	COME_FROM         '596'

815	LOAD_DEREF        'toon'
818	LOAD_ATTR         'getGeomNode'
821	CALL_FUNCTION_0   None
824	STORE_FAST        'geomNode'

827	LOAD_FAST         'geomNode'
830	LOAD_ATTR         'getHpr'
833	CALL_FUNCTION_0   None
836	STORE_FAST        'startHpr'

839	LOAD_GLOBAL       'Point3'
842	LOAD_FAST         'startHpr'
845	CALL_FUNCTION_1   None
848	STORE_FAST        'destHpr'

851	LOAD_FAST         'rng'
854	LOAD_ATTR         'randrange'
857	LOAD_CONST        1
860	LOAD_CONST        8
863	CALL_FUNCTION_2   None
866	STORE_FAST        'hRot'

869	LOAD_FAST         'rng'
872	LOAD_ATTR         'choice'
875	LOAD_CONST        0
878	LOAD_CONST        1
881	BUILD_LIST_2      None
884	CALL_FUNCTION_1   None
887	JUMP_IF_FALSE     '900'

890	LOAD_FAST         'hRot'
893	UNARY_NEGATIVE    None
894	STORE_FAST        'hRot'
897	JUMP_FORWARD      '900'
900_0	COME_FROM         '897'

900	LOAD_FAST         'destHpr'
903	LOAD_ATTR         'setX'
906	LOAD_FAST         'destHpr'
909	LOAD_CONST        0
912	BINARY_SUBSCR     None
913	LOAD_FAST         'hRot'
916	LOAD_CONST        360
919	BINARY_MULTIPLY   None
920	BINARY_ADD        None
921	CALL_FUNCTION_1   None
924	POP_TOP           None

925	LOAD_GLOBAL       'Sequence'
928	LOAD_GLOBAL       'LerpHprInterval'
931	LOAD_FAST         'geomNode'
934	LOAD_FAST         'flyDur'
937	LOAD_FAST         'destHpr'
940	LOAD_CONST        'startHpr'
943	LOAD_FAST         'startHpr'
946	CALL_FUNCTION_259 None

949	LOAD_GLOBAL       'Func'
952	LOAD_FAST         'geomNode'
955	LOAD_ATTR         'setHpr'
958	LOAD_FAST         'startHpr'
961	CALL_FUNCTION_2   None

964	LOAD_CONST        'name'
967	LOAD_DEREF        'toon'
970	LOAD_ATTR         'uniqueName'
973	LOAD_CONST        'hitBySuit-spinH'
976	CALL_FUNCTION_1   None
979	CALL_FUNCTION_258 None
982	STORE_FAST        'spinHTrack'

985	LOAD_FAST         'geomNode'
988	LOAD_ATTR         'getParent'
991	CALL_FUNCTION_0   None
994	STORE_FAST        'parent'

997	LOAD_FAST         'parent'
1000	LOAD_ATTR         'attachNewNode'
1003	LOAD_CONST        'rotNode'
1006	CALL_FUNCTION_1   None
1009	STORE_FAST        'rotNode'

1012	LOAD_FAST         'geomNode'
1015	LOAD_ATTR         'reparentTo'
1018	LOAD_FAST         'rotNode'
1021	CALL_FUNCTION_1   None
1024	POP_TOP           None

1025	LOAD_FAST         'rotNode'
1028	LOAD_ATTR         'setZ'
1031	LOAD_DEREF        'toon'
1034	LOAD_ATTR         'getHeight'
1037	CALL_FUNCTION_0   None
1040	LOAD_CONST        2.0
1043	BINARY_DIVIDE     None
1044	CALL_FUNCTION_1   None
1047	POP_TOP           None

1048	LOAD_FAST         'geomNode'
1051	LOAD_ATTR         'getZ'
1054	CALL_FUNCTION_0   None
1057	STORE_FAST        'oldGeomNodeZ'

1060	LOAD_FAST         'geomNode'
1063	LOAD_ATTR         'setZ'
1066	LOAD_DEREF        'toon'
1069	LOAD_ATTR         'getHeight'
1072	CALL_FUNCTION_0   None
1075	UNARY_NEGATIVE    None
1076	LOAD_CONST        2.0
1079	BINARY_DIVIDE     None
1080	CALL_FUNCTION_1   None
1083	POP_TOP           None

1084	LOAD_FAST         'rotNode'
1087	LOAD_ATTR         'getHpr'
1090	CALL_FUNCTION_0   None
1093	STORE_FAST        'startHpr'

1096	LOAD_GLOBAL       'Point3'
1099	LOAD_FAST         'startHpr'
1102	CALL_FUNCTION_1   None
1105	STORE_FAST        'destHpr'

1108	LOAD_FAST         'rng'
1111	LOAD_ATTR         'randrange'
1114	LOAD_CONST        1
1117	LOAD_CONST        3
1120	CALL_FUNCTION_2   None
1123	STORE_FAST        'pRot'

1126	LOAD_FAST         'rng'
1129	LOAD_ATTR         'choice'
1132	LOAD_CONST        0
1135	LOAD_CONST        1
1138	BUILD_LIST_2      None
1141	CALL_FUNCTION_1   None
1144	JUMP_IF_FALSE     '1157'

1147	LOAD_FAST         'pRot'
1150	UNARY_NEGATIVE    None
1151	STORE_FAST        'pRot'
1154	JUMP_FORWARD      '1157'
1157_0	COME_FROM         '1154'

1157	LOAD_FAST         'destHpr'
1160	LOAD_ATTR         'setY'
1163	LOAD_FAST         'destHpr'
1166	LOAD_CONST        1
1169	BINARY_SUBSCR     None
1170	LOAD_FAST         'pRot'
1173	LOAD_CONST        360
1176	BINARY_MULTIPLY   None
1177	BINARY_ADD        None
1178	CALL_FUNCTION_1   None
1181	POP_TOP           None

1182	LOAD_GLOBAL       'Sequence'
1185	LOAD_GLOBAL       'LerpHprInterval'
1188	LOAD_FAST         'rotNode'
1191	LOAD_FAST         'flyDur'
1194	LOAD_FAST         'destHpr'
1197	LOAD_CONST        'startHpr'
1200	LOAD_FAST         'startHpr'
1203	CALL_FUNCTION_259 None

1206	LOAD_GLOBAL       'Func'
1209	LOAD_FAST         'rotNode'
1212	LOAD_ATTR         'setHpr'
1215	LOAD_FAST         'startHpr'
1218	CALL_FUNCTION_2   None

1221	LOAD_CONST        'name'
1224	LOAD_DEREF        'toon'
1227	LOAD_ATTR         'uniqueName'
1230	LOAD_CONST        'hitBySuit-spinP'
1233	CALL_FUNCTION_1   None
1236	CALL_FUNCTION_258 None
1239	STORE_FAST        'spinPTrack'

1242	LOAD_FAST         'self'
1245	LOAD_ATTR         'avIdList'
1248	LOAD_ATTR         'index'
1251	LOAD_FAST         'avId'
1254	CALL_FUNCTION_1   None
1257	STORE_FAST        'i'

1260	LOAD_GLOBAL       'Sequence'
1263	LOAD_GLOBAL       'Func'
1266	LOAD_GLOBAL       'base'
1269	LOAD_ATTR         'playSfx'
1272	LOAD_FAST         'self'
1275	LOAD_ATTR         'sndTable'
1278	LOAD_CONST        'hitBySuit'
1281	BINARY_SUBSCR     None
1282	LOAD_FAST         'i'
1285	BINARY_SUBSCR     None
1286	CALL_FUNCTION_2   None

1289	LOAD_GLOBAL       'Wait'
1292	LOAD_FAST         'flyDur'
1295	LOAD_CONST        2.0
1298	LOAD_CONST        3.0
1301	BINARY_DIVIDE     None
1302	BINARY_MULTIPLY   None
1303	CALL_FUNCTION_1   None

1306	LOAD_GLOBAL       'SoundInterval'
1309	LOAD_FAST         'self'
1312	LOAD_ATTR         'sndTable'
1315	LOAD_CONST        'falling'
1318	BINARY_SUBSCR     None
1319	LOAD_FAST         'i'
1322	BINARY_SUBSCR     None

1323	LOAD_CONST        'duration'
1326	LOAD_FAST         'flyDur'
1329	LOAD_CONST        1.0
1332	LOAD_CONST        3.0
1335	BINARY_DIVIDE     None
1336	BINARY_MULTIPLY   None
1337	CALL_FUNCTION_257 None

1340	LOAD_CONST        'name'
1343	LOAD_DEREF        'toon'
1346	LOAD_ATTR         'uniqueName'
1349	LOAD_CONST        'hitBySuit-soundTrack'
1352	CALL_FUNCTION_1   None
1355	CALL_FUNCTION_259 None
1358	STORE_FAST        'soundTrack'

1361	LOAD_FAST         'self'
1364	LOAD_FAST         'avId'
1367	LOAD_DEREF        'toon'
1370	LOAD_FAST         'dropShadow'
1373	LOAD_CONST        '<code_object preFunc>'
1376	MAKE_FUNCTION_4   None
1379	STORE_FAST        'preFunc'

1382	LOAD_FAST         'self'
1385	LOAD_FAST         'avId'
1388	LOAD_FAST         'oldGeomNodeZ'
1391	LOAD_FAST         'dropShadow'
1394	LOAD_FAST         'parentNode'
1397	LOAD_CLOSURE      'toon'
1400	LOAD_CLOSURE      'endPos'
1403	LOAD_CONST        '<code_object postFunc>'
1406	MAKE_CLOSURE_5    None
1409	STORE_FAST        'postFunc'

1412	LOAD_FAST         'preFunc'
1415	CALL_FUNCTION_0   None
1418	POP_TOP           None

1419	LOAD_GLOBAL       'Sequence'
1422	LOamHpr)
            iCamParent.removeNode()
            del iCamParent
            base.localAvatar.stopLookAround()

        return Sequence(Wait(waitDur), lerpTrack, Func(cleanup))# decompiled 0 files: 0 okay, 1 failed, 0 verify failed
# 2013.08.22 22:21:27 Pacific Daylight Time
AD_GLOBAL       'Parallel'
1425	LOAD_FAST         'flyTrack'
1428	LOAD_FAST         'cameraTrack'

1431	LOAD_FAST         'spinHTrack'
1434	LOAD_FAST         'spinPTrack'
1437	LOAD_FAST         'soundTrack'
1440	CALL_FUNCTION_5   None

1443	LOAD_GLOBAL       'Func'
1446	LOAD_FAST         'postFunc'
1449	CALL_FUNCTION_1   None

1452	LOAD_CONST        'name'
1455	LOAD_DEREF        'toon'
1458	LOAD_ATTR         'uniqueName'
1461	LOAD_CONST        'hitBySuit'
1464	CALL_FUNCTION_1   None
1467	CALL_FUNCTION_258 None
1470	STORE_FAST        'hitTrack'

1473	LOAD_FAST         'hitTrack'
1476	LOAD_FAST         'self'
1479	LOAD_ATTR         'toonHitTracks'
1482	LOAD_FAST         'avId'
1485	STORE_SUBSCR      None

1486	LOAD_FAST         'hitTrack'
1489	LOAD_ATTR         'start'
1492	LOAD_GLOBAL       'globalClockDelta'
1495	LOAD_ATTR         'localElapsedTime'
1498	LOAD_FAST         'timestamp'
1501	CALL_FUNCTION_1   None
1504	CALL_FUNCTION_1   None
1507	POP_TOP           None
1508	LOAD_CONST        None
1511	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 428

