from direct.directnotify import DirectNotifyGlobal
from toontown.battle import BattlePlace
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from direct.showbase import BulletinBoardWatcher
from pandac.PandaModules import *
from otp.distributed.TelemetryLimiter import RotationLimitToH, TLGatherAllAvs
from toontown.toon import Toon
from toontown.toonbase import ToontownGlobals
from toontown.hood import ZoneUtil
from toontown.toonbase import TTLocalizer
from toontown.toontowngui import TTDialog
from toontown.toonbase import ToontownBattleGlobals
from toontown.coghq import DistributedCountryClub
from toontown.building import Elevator
import random

class CountryClubInterior(BattlePlace.BattlePlace):
    notify = DirectNotifyGlobal.directNotify.newCategory('CountryClubInterior')

    def __init__(self, loader, parentFSM, doneEvent):
        BattlePlace.BattlePlace.__init__(self, loader, doneEvent)
        self.parentFSM = parentFSM
        self.zoneId = loader.countryClubId
        self.elevatorDoneEvent = 'elevatorDone'
        self.fsm = ClassicFSM.ClassicFSM('CountryClubInterior', [State.State('start', self.enterStart, self.exitStart, ['walk', 'teleportIn', 'fallDown']),
         State.State('walk', self.enterWalk, self.exitWalk, ['push',
          'sit',
          'stickerBook',
          'WaitForBattle',
          'battle',
          'died',
          'teleportOut',
          'squished',
          'DFA',
          'fallDown',
          'stopped',
          'elevator']),
         State.State('stopped', self.enterStopped, self.exitStopped, ['walk', 'teleportOut', 'stickerBook']),
         State.State('sit', self.enterSit, self.exitSit, ['walk', 'died', 'teleportOut']),
         State.State('push', self.enterPush, self.exitPush, ['walk', 'died', 'teleportOut']),
         State.State('stickerBook', self.enterStickerBook, self.exitStickerBook, ['walk',
          'battle',
          'DFA',
          'WaitForBattle',
          'died',
          'teleportOut']),
         State.State('WaitForBattle', self.enterWaitForBattle, self.exitWaitForBattle, ['battle',
          'walk',
          'died',
          'teleportOut']),
         State.State('battle', self.enterBattle, self.exitBattle, ['walk', 'teleportOut', 'died']),
         State.State('fallDown', self.enterFallDown, self.exitFallDown, ['walk', 'died', 'teleportOut']),
         State.State('squished', self.enterSquished, self.exitSquished, ['walk', 'died', 'teleportOut']),
         State.State('teleportIn', self.enterTeleportIn, self.exitTeleportIn, ['walk',
          'teleportOut',
          'quietZone',
          'died']),
         State.State('teleportOut', self.enterTeleportOut, self.exitTeleportOut, ['teleportIn',
          'FLA',
          'quietZone',
          'WaitForBattle']),
         State.State('DFA', self.enterDFA, self.exitDFA, ['DFAReject', 'teleportOut']),
         State.State('DFAReject', self.enterDFAReject, self.exitDFAReject, ['walkteleportOut']),
         State.State('died', self.enterDied, self.exitDied, ['teleportOut']),
         State.State('FLA', self.enterFLA, self.exitFLA, ['quietZone']),
         State.State('quietZone', self.enterQuietZone, self.exitQuietZone, ['teleportIn']),
         State.State('elevator', self.enterElevator, self.exitElevator, ['walk']),
         State.State('final', self.enterFinal, self.exitFinal, ['start'])], 'start', 'final')

    def load(self):
        self.parentFSM.getStateNamed('countryClubInterior').addChild(self.fsm)
        BattlePlace.BattlePlace.load(self)
        musicName = random.choice(['phase_12/audio/bgm/Bossbot_Factory_v1.mid', 'phase_12/audio/bgm/Bossbot_Factory_v2.mid', 'phase_12/audio/bgm/Bossbot_Factory_v3.mid'])
        self.music = base.loadMusic(musicName)

    def unload(self):
        self.parentFSM.getStateNamed('countryClubInterior').removeChild(self.fsm)
        del self.music
        del self.fsm
        del self.parentFSM
        BattlePlace.BattlePlace.unload(self)

    def enter(self, requestStatus):
        self.fsm.enterInitialState()
        base.transitions.fadeOut(t=0)
        base.localAvatar.inventory.setRespectInvasions(0)
        base.cr.forbidCheesyEffects(1)
        self._telemLimiter = TLGatherAllAvs('CountryClubInterior', RotationLimitToH)

        def commence(self = self):
            NametagGlobals.setMasterArrowsOn(1)
            self.fsm.request(requestStatus['how'], [requestStatus])
            base.playMusic(self.music, looping=1, volume=0.8)
            base.transitions.irisIn()
            CountryClub = bboard.get(DistributedCountryClub.DistributedCountryClub.ReadyPost)
            self.loader.hood.spawnTitleText(CountryClub.countryClubId, CountryClub.floorNum)

        self.CountryClubReadyWatcher = BulletinBoardWatcher.BulletinBoardWatcher('CountryClubReady', DistributedCountryClub.DistributedCountryClub.ReadyPost, commence)
        self.CountryClubDefeated = 0
        self.acceptOnce(DistributedCountryClub.DistributedCountryClub.WinEvent, self.handleCountryClubWinEvent)
        if __debug__ and 0:
            self.accept('f10', lambda : messenger.send(DistributedCountryClub.DistributedCountryClub.WinEvent))
        self.confrontedBoss = 0

        def handleConfrontedBoss(self = self):
            self.confrontedBoss = 1

        self.acceptOnce('localToonConfrontedCountryClubBoss', handleConfrontedBoss)

    def exit(self):
        NametagGlobals.setMasterArrowsOn(0)
        bboard.remove(DistributedCountryClub.DistributedCountryClub.ReadyPost)
        self._telemLimiter.destroy()
        del self._telemLimiter
        base.cr.forbidCheesyEffects(0)
        base.localAvatar.inventory.setRespectInvasions(1)
        self.fsm.requestFinalState()
        self.loader.music.stop()
        self.music.stop()
        self.ignoreAll()
        del self.CountryClubReadyWatcher

    def enterStopped(self):
        BattlePlace.BattlePlace.enterStopped(self)
        self.ignore('teleportQuery')
        base.localAvatar.setTeleportAvailable(0)

    def enterWalk(self, teleportIn = 0):
        BattlePlace.BattlePlace.enterWalk(self, teleportIn)
        self.ignore('teleportQuery')
        base.localAvatar.setTeleportAvailable(0)

    def enterPush(self):
        BattlePlace.BattlePlace.enterPush(self)
        self.ignore('teleportQuery')
        base.localAvatar.setTeleportAvailable(0)

    def enterWaitForBattle(self):
        CountryClubInterior.notify.debug('enterWaitForBattle')
        BattlePlace.BattlePlace.enterWaitForBattle(self)
        if base.localAvatar.getParent() != render:
            base.localAvatar.wrtReparentTo(render)
            base.localAvatar.b_setParent(ToontownGlobals.SPRender)

    def exitWaitForBattle(self):
        CountryClubInterior.notify.debug('exitWaitForBattle')
        BattlePlace.BattlePlace.exitWaitForBattle(self)

    def enterBattle(self, event):
        CountryClubInterior.notify.debug('enterBattle')
        self.music.stop()
        BattlePlace.BattlePlace.enterBattle(self, event)
        self.ignore('teleportQuery')
        base.localAvatar.setTeleportAvailable(0)

    def enterTownBattle(self, event):
        mult = ToontownBattleGlobals.getCountryClubCreditMultiplier(self.zoneId)
        base.localAvatar.inventory.setBattleCreditMultiplier(mult)
        self.loader.townBattle.enter(event, self.fsm.getStateNamed('battle'), bldg=1, creditMultiplier=mult)

    def exitBattle(self):
        CountryClubInterior.notify.debug('exitBattle')
        BattlePlace.BattlePlace.exitBattle(self)
        self.loader.music.stop()
        base.playMusic(self.music, looping=1, volume=0.8)

    def enterStickerBook(self, page = None):
        BattlePlace.BattlePlace.enterStickerBook(self, page)
        self.ignore('teleportQuery')
        base.localAvatar.setTeleportAvailable(0)

    def enterSit(self):
        BattlePlace.BattlePlace.enterSit(self)
        self.ignore('teleportQuery')
        base.localAvatar.setTeleportAvailable(0)

    def enterZone(self, zoneId):
        pass

    def enterTeleportOut(self, requestStatus):
        CountryClubInterior.notify.debug('enterTeleportOut()')
        BattlePlace.BattlePlace.enterTeleportOut(self, requestStatus, self.__teleportOutDone)

    def __processLeaveRequest(self, requestStatus):
        hoodId = requestStatus['hoodId']
        if hoodId == ToontownGlobals.MyEstate:
            self.getEstateZoneAndGoHome(requestStatus)
        else:
            self.doneStatus = requestStatus
            messenger.send(self.doneEvent)

    def __teleportOutDone(self, requestStatus):
        CountryClubInterior.notify.debug('__teleportOutDone()')
        messenger.send('leavingCountryClub')
        messenger.send('localToonLeft')
        if self.CountryClubDefeated and not self.confrontedBoss:
            self.fsm.request('FLA', [requestStatus])
        else:
            self.__processLeaveRequest(requestStatus)

    def exitTeleportOut(self):
        CountryClubInterior.notify.debug('exitTeleportOut()')
        BattlePlace.BattlePlace.exitTeleportOut(self)

    def handleCountryClubWinEvent--- This code section failed: ---

0	LOAD_GLOBAL       'CountryClubInterior'
3	LOAD_ATTR         'notify'
6	LOAD_ATTR         'debug'
9	LOAD_CONST        'handleCountryClubWinEvent'
12	CALL_FUNCTION_1   None
15	POP_TOP           None

16	LOAD_GLOBAL       'base'
19	LOAD_ATTR         'cr'
22	LOAD_ATTR         'playGame'
25	LOAD_ATTR         'getPlace'
28	CALL_FUNCTION_0   None
31	LOAD_ATTR         'fsm'
34	LOAD_ATTR         'getCurrentState'
37	CALL_FUNCTION_0   None
40	LOAD_ATTR         'getName'
43	CALL_FUNCTION_0   None
46	LOAD_CONST        'died'
49	COMPARE_OP        '=='
52	JUMP_IF_FALSE     '62'

55	LOAD_CONST        None
58	RETURN_VALUE      None
59	JUMP_FORWARD      '62'
62_0	COME_FROM         '59'

62	LOAD_CONST        1
65	LOAD_FAST         'self'
68	STORE_ATTR        'CountryClubDefeated'

71	LOAD_GLOBAL       'ZoneUtil'
74	LOAD_ATTR         'getHoodId'
77	LOAD_FAST         'self'
80	LOAD_ATTR         'zoneId'
83	CALL_FUNCTION_1   None
86	STORE_FAST        'zoneId'
89	JUMP_FORWARD      '113'

92	LOAD_GLOBAL       'ZoneUtil'
95	LOAD_ATTR         'getSafeZoneId'
98	LOAD_GLOBAL       'base'
101	LOAD_ATTR         'localAvatar'
104	LOAD_ATTR         'defaultZone'
107	CALL_FUNCTION_1   None
110	STORE_FAST        'zoneId'
113_0	COME_FROM         '89'

113	LOAD_FAST         'self'
116	LOAD_ATTR         'fsm'
119	LOAD_ATTR         'request'
122	LOAD_CONST        'teleportOut'
125	BUILD_MAP         None
128	DUP_TOP           None
129	LOAD_CONST        'loader'
132	LOAD_GLOBAL       'ZoneUtil'
135	LOAD_ATTR         'getLoaderName'
138	LOAD_FAST         'zoneId'
141	CALL_FUNCTION_1   None
144	ROT_THREE         None
145	STORE_SUBSCR      None
146	DUP_TOP           None
147	LOAD_CONST        'where'
150	LOAD_GLOBAL       'ZoneUtil'
153	LOAD_ATTR         'getToonWhereName'
156	LOAD_FAST         'zoneId'
159	CALL_FUNCTION_1   None
162	ROT_THREE         None
163	STORE_SUBSCR      None
164	DUP_TOP           None
165	LOAD_CONST        'how'
168	LOAD_CONST        'teleportIn'
171	ROT_THREE         None
172	STORE_SUBSCR      None
173	DUP_TOP           None
174	LOAD_CONST        'hoodId'
177	LOAD_FAST         'zoneId'
180	ROT_THREE         None
181	STORE_SUBSCR      None
182	DUP_TOP           None
183	LOAD_CONST        'zoneId'
186	LOAD_FAST         'zoneId'
189	ROT_THREE         None
190	STORE_SUBSCR      None
191	DUP_TOP           None
192	LOAD_CONST        'shardId'
195	LOAD_CONST        None
198	ROT_THREE         None
199	STORE_SUBSCR      None
200	DUP_TOP           None
201	LOAD_CONST        'avId'
204	LOAD_CONST        -1
207	ROT_THREE         None
208	STORE_SUBSCR      None
209	BUILD_LIST_1      None
212	CALL_FUNCTION_2   None
215	POP_TOP           None
216	LOAD_CONST        None
219	RETURN_VALUE      None

Syntax error at or near `LOAD_GLOBAL' token at offset 92

    def enterDied(self, requestStatus, callback = None):
        CountryClubInterior.notify.debug('enterDied')

        def diedDone(requestStatus, self = self, callback = callback):
            if callback is not None:
                callback()
            messenger.send('leavingCountryClub')
            self.doneStatus = requestStatus
            messenger.send(self.doneEvent)
            return

        BattlePlace.BattlePlace.enterDied(self, requestStatus, diedDone)

    def enterFLA(self, requestStatus):
        CountryClubInterior.notify.debug('enterFLA')
        self.flaDialog = TTDialog.TTGlobalDialog(message=TTLocalizer.ForcedLeaveCountryClubAckMsg, doneEvent='FLADone', style=TTDialog.Acknowledge, fadeScreen=1)

        def continueExit(self = self, requestStatus = requestStatus):
            self.__processLeaveRequest(requestStatus)

        self.accept('FLADone', continueExit)
        self.flaDialog.show()

    def exitFLA(self):
        CountryClubInterior.notify.debug('exitFLA')
        if hasattr(self, 'flaDialog'):
            self.flaDialog.cleanup()
            del self.flaDialog

    def detectedElevatorCollision(self, distElevator):
        self.fsm.request('elevator', [distElevator])

    def enterElevator(self, distElevator, skipDFABoard = 0):
        self.accept(self.elevatorDoneEvent, self.handleElevatorDone)
        self.elevator = Elevator.Elevator(self.fsm.getStateNamed('elevator'), self.elevatorDoneEvent, distElevator)
        if skipDFABoard:
            self.elevator.skipDFABoard = 1
        self.elevator.setReverseBoardingCamera(True)
        distElevator.elevatorFSM = self.elevator
        self.elevator.load()
        self.elevator.enter()

    def exitElevator(self):
        self.ignore(self.elevatorDoneEvent)
        self.elevator.unload()
        self.elevator.exit()

    def handleElevatorDone(self, doneStatus):
        self.notify.debug('handling elevator done event')
        where = doneStatus['where']
        if where == 'reject':
            if hasattr(base.localAvatar, 'elevatorNotifier') and base.localAvatar.elevatorNotifier.isNotifierOpen():
                pass
            else:
                self.fsm.request('walk')
        elif where == 'exit':
            self.fsm.request('walk')
        elif where == 'factoryInterior' or where == 'suitInterior':
            self.doneStatus = doneStatus
            self.doneEvent = 'lawOfficeFloorDone'
            messenger.send(self.doneEvent)
        else:
            self.notify.error('Unknown mode: ' + where + ' in handleElevatorDone')

# Can't uncompyle C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\coghq\CountryClubInterior.pyc
Traceback (most recent call last):
  File "C:\python27\lib\uncompyle2\__init__.py", line 206, in main
    uncompyle_file(infile, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 143, in uncompyle_file
    uncompyle(version, co, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 132, in uncompyle
    raise walk.ERROR
ParserError: --- This code section failed: ---

0	LOAD_GLOBAL       'CountryClubInterior'
3	LOAD_ATTR         'notify'
6	LOAD_ATTR         'debug'
9	LOAD_CONST        'handleCountryClubWinEvent'
12	CALL_FUNCTION_1   None
15	POP_TOP           None

16	LOAD_GLOBAL       'base'
19	LOAD_ATTR         'cr'
22	LOAD_ATTR         'playGame'
25	LOAD_ATTR         'getPlace'
28	CALL_FUNCTION_0   None
31	LOAD_ATTR         'fsm'
34	LOAD_ATTR         'getCurrentState'
37	CALL_FUNCTION_0   None
40	LOAD_ATTR         'getName'
43	CALL_FUNCTION_0   None
46	LOAD_CONST        'died'
49	COMPARE_OP        '=='
52	JUMP_IF_FALSE     '62'

55	LOAD_CONST        None
58	RETURN_VALUE      None
59	JUMP_FORWARD      '62'
62_0	COME_FROM         '59'

62	LOAD_CONST        1
65	LOAD_FAST         'self'
68	STORE_ATTR        'CountryClubDefeated'

71	LOAD_GLOBAL       'ZoneUtil'
74	LOAD_ATTR         'getHoodId'
77	LOAD_FAST         'self'
80	LOAD_ATTR         'zoneId'
83	CALL_FUNCTION_1   None
86	STORE_FAST        'zoneId'
89	JUMP_FORWARD      '113'

92	LOAD_GLOBAL       'ZoneUtil'
95	LOAD_ATTR         'getSafeZoneId'
98	LOAD_GLOBAL       'base'
101	LOAD_ATTR         'localAvatar'
104	LOAD_ATTR         'defaultZone'
107	CALL_FUNCTION_1   None
110	STORE_FAST        'zoneId'
113_0	COME_FROM         '89'

113	LOAD_FAST         'self'
116	LOAD_ATTR         'fsm'
119	LOAD_ATTR         'request'
122	LOAD_CONST        'teleportOut'
125	BUILD_MAP         None
128	DUP_TOP           None
129	LOAD_CONST        'loader'
132	LOAD_GLOBAL       'ZoneUtil'
135	LOAD_ATTR         'getLoaderName'
138	LOAD_FAST         'zoneId'
141	CALL_FUNCTION_1   None
144	ROT_THREE         None
145	STORE_SUBSCR      None
146	DUP_TOP           None
147	LOAD_CONST        'where'
150	LOAD_GLOBAL       'ZoneUtil'
153	LOAD_ATTR         'getToonWhereName'
156	LOAD_FAST         'zoneId'
159	CALL_FUNCTION_1   None
162	ROT_THREE         None
163	STORE_SUBSCR      None
164	DUP_TOP           None
165	LOAD_CONST        'how'
168	LOAD_CONST        'teleportIn'
171	ROT_THREE         None
172	STORE_SUBSCR      None
173	DUP_TOP           None
174	LOAD_CONST        'hoodId'
177	LOAD_FAST         'zoneId'
180	ROT_THREE         None
181	STORE_SUBSCR      None
182	DUP_TOP           None
183	LOAD_CONST        'zoneId'
186	LOAD_FAST         'zoneId'
189	ROT_THREE         None
190	STORE_SUBSCR      None
191	DUP_TOP           None
192	LOAD_CONST        'shardId'
195	LOAD_CONST        None
198	ROT_THREE         None
199	STORE_SUBSCR      None
200	DUP_TOP           None
201	LOAD_CONST        'avId'
204	LOAD_CONST        -1
207	ROT_THREE         None
208	STORE_SUBSCR      None
209	BUILD_LIST_1      None
212	CALL_FUNCTION_2   None
215	POP_TOP           None
216	LOAD_CONST        None
219	RETURN_VALUE      None

Syntax error at or near `LOAD_GLOBAL' token at offset 92

