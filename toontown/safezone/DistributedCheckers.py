# 2013.08.22 22:24:25 Pacific Daylight Time
# Embedded file name: toontown.safezone.DistributedCheckers
from pandac.PandaModules import *
from direct.distributed.ClockDelta import *
from direct.task.Task import Task
from direct.interval.IntervalGlobal import *
from TrolleyConstants import *
from direct.gui.DirectGui import *
from toontown.toonbase import TTLocalizer
from direct.distributed import DistributedNode
from direct.distributed.ClockDelta import globalClockDelta
from CheckersBoard import CheckersBoard
from direct.fsm import ClassicFSM, State
from direct.fsm import StateData
from toontown.toonbase.ToontownTimer import ToontownTimer
from toontown.toonbase import ToontownGlobals
from direct.distributed.ClockDelta import *
from otp.otpbase import OTPGlobals
from direct.showbase import PythonUtil

class DistributedCheckers(DistributedNode.DistributedNode):
    __module__ = __name__

    def __init__(self, cr):
        NodePath.__init__(self, 'DistributedCheckers')
        DistributedNode.DistributedNode.__init__(self, cr)
        self.cr = cr
        self.reparentTo(render)
        self.boardNode = loader.loadModel('phase_6/models/golf/regular_checker_game.bam')
        self.boardNode.reparentTo(self)
        self.board = CheckersBoard()
        self.exitButton = None
        self.inGame = False
        self.waiting = True
        self.startButton = None
        self.playerNum = None
        self.turnText = None
        self.isMyTurn = False
        self.wantTimer = True
        self.leaveButton = None
        self.screenText = None
        self.turnText = None
        self.exitButton = None
        self.numRandomMoves = 0
        self.blinker = Sequence()
        self.moveList = []
        self.mySquares = []
        self.myKings = []
        self.isRotated = False
        self.accept('mouse1', self.mouseClick)
        self.traverser = base.cTrav
        self.pickerNode = CollisionNode('mouseRay')
        self.pickerNP = camera.attachNewNode(self.pickerNode)
        self.pickerNode.setFromCollideMask(ToontownGlobals.WallBitmask)
        self.pickerRay = CollisionRay()
        self.pickerNode.addSolid(self.pickerRay)
        self.myHandler = CollisionHandlerQueue()
        self.traverser.addCollider(self.pickerNP, self.myHandler)
        self.buttonModels = loader.loadModel('phase_3.5/models/gui/inventory_gui')
        self.upButton = self.buttonModels.find('**//InventoryButtonUp')
        self.downButton = self.buttonModels.find('**/InventoryButtonDown')
        self.rolloverButton = self.buttonModels.find('**/InventoryButtonRollover')
        self.clockNode = ToontownTimer()
        self.clockNode.setPos(1.16, 0, -0.83)
        self.clockNode.setScale(0.3)
        self.clockNode.hide()
        self.playerColors = [Vec4(0, 0, 1, 1), Vec4(0, 1, 0, 1)]
        self.tintConstant = Vec4(0.25, 0.25, 0.25, 0.5)
        self.ghostConstant = Vec4(0, 0, 0, 0.8)
        self.startingPositions = [[0,
          1,
          2,
          3,
          4,
          5,
          6,
          7,
          8,
          9,
          10,
          11], [20,
          21,
          22,
          23,
          24,
          25,
          26,
          27,
          28,
          29,
          30,
          31]]
        self.knockSound = base.loadSfx('phase_5/audio/sfx/GUI_knock_1.mp3')
        self.clickSound = base.loadSfx('phase_3/audio/sfx/GUI_balloon_popup.mp3')
        self.moveSound = base.loadSfx('phase_6/audio/sfx/CC_move.mp3')
        self.accept('stoppedAsleep', self.handleSleep)
        self.fsm = ClassicFSM.ClassicFSM('ChineseCheckers', [State.State('waitingToBegin', self.enterWaitingToBegin, self.exitWaitingToBegin, ['playing', 'gameOver']), State.State('playing', self.enterPlaying, self.exitPlaying, ['gameOver']), State.State('gameOver', self.enterGameOver, self.exitGameOver, ['waitingToBegin'])], 'waitingToBegin', 'waitingToBegin')
        x = self.boardNode.find('**/locator*')
        self.locatorList = x.getChildren()
        tempList = []
        for x in range(0, 32):
            self.locatorList[x].setTag('GamePeiceLocator', '%d' % x)
            tempList.append(self.locatorList[x].attachNewNode(CollisionNode('picker%d' % x)))
            tempList[x].node().addSolid(CollisionSphere(0, 0, 0, 0.39))

        for z in self.locatorList:
            y = loader.loadModel('phase_6/models/golf/regular_checker_piecewhite.bam')
            y.find('**/checker_k*').hide()
            zz = loader.loadModel('phase_6/models/golf/regular_checker_pieceblack.bam')
            zz.find('**/checker_k*').hide()
            y.reparentTo(z)
            y.hide()
            zz.reparentTo(z)
            zz.hide()

        return

    def setName(self, name):
        self.name = name

    def announceGenerate(self):
        DistributedNode.DistributedNode.announceGenerate(self)
        if self.table.fsm.getCurrentState().getName() != 'observing':
            if base.localAvatar.doId in self.table.tableState:
                self.seatPos = self.table.tableState.index(base.localAvatar.doId)

    def handleSleep(self, task = None):
        if self.fsm.getCurrentState().getName() == 'waitingToBegin':
            self.exitButtonPushed()
        if task != None:
            task.done
        return

    def setTableDoId(self, doId):
        self.tableDoId = doId
        self.table = self.cr.doId2do[doId]
        self.table.setTimerFunc(self.startButtonPushed)
        self.fsm.enterInitialState()
        self.table.setGameDoId(self.doId)

    def disable(self):
        DistributedNode.DistributedNode.disable(self)
        if self.leaveButton:
            self.leaveButton.destroy()
            self.leavebutton = None
        if self.screenText:
            self.screenText.destroy()
            self.screenText = None
        if self.turnText:
            self.turnText.destroy()
            self.turnText = None
        self.clockNode.stop()
        self.clockNode.hide()
        self.ignore('mouse1')
        self.ignore('stoppedAsleep')
        self.fsm = None
        return

    def delete(self):
        DistributedNode.DistributedNode.delete(self)
        self.table.gameDoId = None
        self.table.game = None
        if self.exitButton:
            self.exitButton.destroy()
        if self.startButton:
            self.startButton.destroy()
        self.clockNode.stop()
        self.clockNode.hide()
        self.table.startButtonPushed = None
        self.ignore('mouse1')
        self.ignore('stoppedAsleep')
        self.fsm = None
        self.table = None
        return

    def getTimer(self):
        self.sendUpdate('requestTimer', [])

    def setTimer(self, timerEnd):
        if self.fsm.getCurrentState() != None and self.fsm.getCurrentState().getName() == 'waitingToBegin' and not self.table.fsm.getCurrentState().getName() == 'observing':
            self.clockNode.stop()
            time = globalClockDelta.networkToLocalTime(timerEnd)
            timeLeft = int(time - globalClock.getRealTime())
            if timeLeft > 0 and timerEnd != 0:
                if timeLeft > 60:
                    timeLeft = 60
                self.clockNode.setPos(1.16, 0, -0.83)
                self.clockNode.countdown(timeLeft, self.startButtonPushed)
                self.clockNode.show()
            else:
                self.clockNode.stop()
                self.clockNode.hide()
        return

    def setTurnTimer(self, turnEnd):
        if self.fsm.getCurrentState() != None and self.fsm.getCurrentState().getName() == 'playing':
            self.clockNode.stop()
            time = globalClockDelta.networkToLocalTime(turnEnd)
            timeLeft = int(time - globalClock.getRealTime())
            if timeLeft > 0:
                self.clockNode.setPos(-0.74, 0, -0.2)
                if self.isMyTurn:
                    self.clockNode.countdown(timeLeft, self.doNothing)
                else:
                    self.clockNode.countdown(timeLeft, self.doNothing)
                self.clockNode.show()
        return

    def gameStart(self, playerNum):
        if playerNum != 255:
            self.playerNum = playerNum
            if self.playerNum == 1:
                self.playerColorString = 'white'
            else:
                self.playerColorString = 'black'
            self.playerColor = self.playerColors[playerNum - 1]
            self.moveCameraForGame()
        self.fsm.request('playing')

    def sendTurn(self, playersTurn):
        if self.fsm.getCurrentState().getName() == 'playing':
            if playersTurn == self.playerNum:
                self.isMyTurn = True
            self.enableTurnScreenText(playersTurn)

    def illegalMove(self):
        self.exitButtonPushed()

    def moveCameraForGame(self):
        if self.table.cameraBoardTrack.isPlaying():
            self.table.cameraBoardTrack.finish()
        rotation = 0
        if self.seatPos > 2:
            if self.playerNum == 1:
                rotation = 180
            elif self.playerNum == 2:
                rotation = 0
            for x in self.locatorList:
                x.setH(180)

            self.isRotated = True
        elif self.playerNum == 1:
            rotation = 0
        elif self.playerNum == 2:
            rotation = 180
            for x in self.locatorList:
                x.setH(180)

            self.isRotated = True
        int = LerpHprInterval(self.boardNode, 4.2, Vec3(rotation, self.boardNode.getP(), self.boardNode.getR()), self.boardNode.getHpr())
        int.start()

    def enterWaitingToBegin(self):
        if self.table.fsm.getCurrentState().getName() != 'observing':
            self.enableExitButton()
            self.enableStartButton()

    def exitWaitingToBegin(self):
        if self.exitButton:
            self.exitButton.destroy()
            self.exitButton = None
        if self.startButton:
            self.startButton.destroy()
            self.exitButton = None
        self.clockNode.stop()
        self.clockNode.hide()
        return

    def enterPlaying(self):
        self.inGame = True
        self.enableScreenText()
        if self.table.fsm.getCurrentState().getName() != 'observing':
            self.enableLeaveButton()

    def exitPlaying(self):
        self.inGame = False
        if self.leaveButton:
            self.leaveButton.destroy()
            self.leavebutton = None
        self.playerNum = None
        if self.screenText:
            self.screenText.destroy()
            self.screenText = None
        if self.turnText:
            self.turnText.destroy()
            self.turnText = None
        self.clockNode.stop()
        self.clockNode.hide()
        return

    def enterGameOver(self):
        pass

    def exitGameOver(self):
        pass

    def exitWaitCountdown(self):
        self.__disableCollisions()
        self.ignore('trolleyExitButton')
        self.clockNode.reset()

    def enableExitButton(self):
        self.exitButton = DirectButton(relief=None, text=TTLocalizer.ChineseCheckersGetUpButton, text_fg=(1, 1, 0.65, 1), text_pos=(0, -0.23), text_scale=0.8, image=(self.upButton, self.downButton, self.rolloverButton), image_color=(1, 0, 0, 1), image_scale=(20, 1, 11), pos=(0.92, 0, 0.4), scale=0.15, command=lambda self = self: self.exitButtonPushed())
        return

    def enableScreenText(self):
        defaultPos = (-0.8, -0.4)
        if self.playerNum == 1:
            message = TTLocalizer.CheckersColorWhite
            color = Vec4(1, 1, 1, 1)
        elif self.playerNum == 2:
            message = TTLocalizer.CheckersColorBlack
            color = Vec4(0, 0, 0, 1)
        else:
            message = TTLocalizer.CheckersObserver
            color = Vec4(0, 0, 0, 1)
            defaultPos = (-0.8, -0.4)
        self.screenText = OnscreenText(text=message, pos=defaultPos, scale=0.1, fg=color, align=TextNode.ACenter, mayChange=1)

    def enableStartButton(self):
        self.startButton = DirectButton(relief=None, text=TTLocalizer.ChineseCheckersStartButton, text_fg=(1, 1, 0.65, 1), text_pos=(0, -0.23), text_scale=0.6, image=(self.upButton, self.downButton, self.rolloverButton), image_color=(1, 0, 0, 1), image_scale=(20, 1, 11), pos=(0.92, 0, 0.1), scale=0.15, command=lambda self = self: self.startButtonPushed())
        return

    def enableLeaveButton(self):
        self.leaveButton = DirectButton(relief=None, text=TTLocalizer.ChineseCheckersQuitButton, text_fg=(1, 1, 0.65, 1), text_pos=(0, -0.13), text_scale=0.5, image=(self.upButton, self.downButton, self.rolloverButton), image_color=(1, 0, 0, 1), image_scale=(20, 1, 11), pos=(0.92, 0, 0.4), scale=0.15, command=lambda self = self: self.exitButtonPushed())
        return

    def enableTurnScreenText(self, player):
        playerOrder = [1,
         4,
         2,
         5,
         3,
         6]
        message1 = TTLocalizer.CheckersIts
        if self.turnText != None:
            self.turnText.destroy()
        if player == self.playerNum:
            message2 = TTLocalizer.ChineseCheckersYourTurn
            color = (0, 0, 0, 1)
        elif player == 1:
            message2 = TTLocalizer.CheckersWhiteTurn
            color = (1, 1, 1, 1)
        elif player == 2:
            message2 = TTLocalizer.CheckersBlackTurn
            color = (0, 0, 0, 1)
        self.turnText = OnscreenText(text=message1 + message2, pos=(-0.8, -0.5), scale=0.092, fg=color, align=TextNode.ACenter, mayChange=1)
        return

    def startButtonPushed(self):
        self.sendUpdate('requestBegin')
        self.startButton.hide()
        self.clockNode.stop()
        self.clockNode.hide()

    def exitButtonPushed(self):
        self.fsm.request('gameOver')
        self.table.fsm.request('off')
        self.clockNode.stop()
        self.clockNode.hide()
        self.table.sendUpdate('requestExit')

    def mouseClick(self):
        messenger.send('wakeup')
        if self.isMyTurn == True and self.inGame == True:
            mpos = base.mouseWatcherNode.getMouse()
            self.pickerRay.setFromLens(base.camNode, mpos.getX(), mpos.getY())
            self.traverser.traverse(render)
            if self.myHandler.getNumEntries() > 0:
                self.myHandler.sortEntries()
                pickedObj = self.myHandler.getEntry(0).getIntoNodePath()
                pickedObj = pickedObj.getNetTag('GamePeiceLocator')
                if pickedObj:
                    self.handleClicked(int(pickedObj))

    def handleClicked(self, index):
        self.sound = Sequence(SoundInterval(self.clickSound))
        if self.moveList == []:
            if index not in self.mySquares and index not in self.myKings:
                return
            self.moveList.append(index)
            type = self.board.squareList[index].getState()
            if type == 3 or type == 4:
                self.moverType = 'king'
            else:
                self.moverType = 'normal'
            self.blinker = Sequence()
            col = self.locatorList[index].getColor()
            self.blinker.append(LerpColorInterval(self.locatorList[index], 0.7, self.tintConstant, col))
            self.blinker.append(LerpColorInterval(self.locatorList[index], 0.7, col, self.tintConstant))
            self.blinker.loop()
            self.sound.start()
        elif index in self.mySquares or index in self.myKings:
            for x in self.moveList:
                self.locatorList[x].setColor(1, 1, 1, 1)
                self.locatorList[x].hide()

            self.blinker.finish()
            self.blinker = Sequence()
            col = self.locatorList[index].getColor()
            self.blinker.append(LerpColorInterval(self.locatorList[index], 0.7, self.tintConstant, col))
            self.blinker.append(LerpColorInterval(self.locatorList[index], 0.7, col, self.tintConstant))
            self.blinker.loop()
            self.sound.start()
            self.locatorList[self.moveList[0]].show()
            self.moveList = []
            self.moveList.append(index)
            type = self.board.squareList[index].getState()
            if type == 3 or type == 4:
                self.moverType = 'king'
            else:
                self.moverType = 'normal'
        else:
            self.currentMove = index
            lastItem = self.board.squareList[self.moveList[len(self.moveList) - 1]]
            thisItem = self.board.squareList[index]
            if self.mustJump == True:
                if lastItem.getNum() == index:
                    self.blinker.finish()
                    self.d_requestMove(self.moveList)
                    self.isMyTurn = False
                    self.moveList = []
                    return
                if self.checkLegalJump(lastItem, thisItem, self.moverType) == True:
                    col = self.locatorList[index].getColor()
                    self.locatorList[index].show()
                    self.sound.start()
                    if self.existsLegalJumpsFrom(index, self.moverType) == False:
                        self.moveList.append(index)
                        self.blinker.finish()
                        self.d_requestMove(self.moveList)
                        self.moveList = []
                        self.isMyTurn = False
                    else:
                        self.moveList.append(index)
                        if self.playerColorString == 'white':
                            x = self.locatorList[index].getChildren()[1]
                            x.show()
                        else:
                            x = self.locatorList[index].getChildren()[2]
                            x.show()
                        if self.moverType == 'king':
                            x.find('**/checker_k*').show()
                        self.locatorList[index].setColor(Vec4(0.5, 0.5, 0.5, 0.5))
            elif self.checkLegalMove(lastItem, thisItem, self.moverType) == True:
                self.moveList.append(index)
                col = self.locatorList[index].getColor()
                self.locatorList[index].show()
                self.sound.start()
                self.blinker.finish()
                self.d_requestMove(self.moveList)
                self.moveList = []
                self.isMyTurn = False

    def existsLegalJumpsFrom--- This code section failed: ---

0	LOAD_FAST         'peice'
3	LOAD_CONST        'king'
6	COMPARE_OP        '=='
9	JUMP_IF_FALSE     '315'

12	SETUP_LOOP        '308'
15	LOAD_GLOBAL       'range'
18	LOAD_CONST        4
21	CALL_FUNCTION_1   None
24	GET_ITER          None
25	FOR_ITER          '307'
28	STORE_FAST        'x'

31	LOAD_FAST         'self'
34	LOAD_ATTR         'board'
37	LOAD_ATTR         'squareList'
40	LOAD_FAST         'index'
43	BINARY_SUBSCR     None
44	LOAD_ATTR         'getAdjacent'
47	CALL_FUNCTION_0   None
50	LOAD_FAST         'x'
53	BINARY_SUBSCR     None
54	LOAD_CONST        None
57	COMPARE_OP        '!='
60	JUMP_IF_FALSE     '304'
63	LOAD_FAST         'self'
66	LOAD_ATTR         'board'
69	LOAD_ATTR         'squareList'
72	LOAD_FAST         'index'
75	BINARY_SUBSCR     None
76	LOAD_ATTR         'getJumps'
79	CALL_FUNCTION_0   None
82	LOAD_FAST         'x'
85	BINARY_SUBSCR     None
86	LOAD_CONST        None
89	COMPARE_OP        '!='
92_0	COME_FROM         '60'
92	JUMP_IF_FALSE     '304'

95	LOAD_FAST         'self'
98	LOAD_ATTR         'board'
101	LOAD_ATTR         'squareList'
104	LOAD_FAST         'self'
107	LOAD_ATTR         'board'
110	LOAD_ATTR         'squareList'
113	LOAD_FAST         'index'
116	BINARY_SUBSCR     None
117	LOAD_ATTR         'getAdjacent'
120	CALL_FUNCTION_0   None
123	LOAD_FAST         'x'
126	BINARY_SUBSCR     None
127	BINARY_SUBSCR     None
128	STORE_FAST        'adj'

131	LOAD_FAST         'self'
134	LOAD_ATTR         'board'
137	LOAD_ATTR         'squareList'
140	LOAD_FAST         'self'
143	LOAD_ATTR         'board'
146	LOAD_ATTR         'squareList'
149	LOAD_FAST         'index'
152	BINARY_SUBSCR     None
153	LOAD_ATTR         'getJumps'
156	CALL_FUNCTION_0   None
159	LOAD_FAST         'x'
162	BINARY_SUBSCR     None
163	BINARY_SUBSCR     None
164	STORE_FAST        'jump'

167	LOAD_FAST         'adj'
170	LOAD_ATTR         'getState'
173	CALL_FUNCTION_0   None
176	LOAD_CONST        0
179	COMPARE_OP        '=='
182	JUMP_IF_FALSE     '188'

185	JUMP_ABSOLUTE     '304'

188	LOAD_FAST         'adj'
191	LOAD_ATTR         'getState'
194	CALL_FUNCTION_0   None
197	LOAD_FAST         'self'
200	LOAD_ATTR         'playerNum'
203	COMPARE_OP        '=='
206	JUMP_IF_TRUE      '234'
209	LOAD_FAST         'adj'
212	LOAD_ATTR         'getState'
215	CALL_FUNCTION_0   None
218	LOAD_FAST         'self'
221	LOAD_ATTR         'playerNum'
224	LOAD_CONST        2
227	BINARY_ADD        None
228	COMPARE_OP        '=='
231_0	COME_FROM         '206'
231	JUMP_IF_FALSE     '237'

234	JUMP_ABSOLUTE     '304'

237	LOAD_FAST         'jump'
240	LOAD_ATTR         'getState'
243	CALL_FUNCTION_0   None
246	LOAD_CONST        0
249	COMPARE_OP        '=='
252	JUMP_IF_FALSE     '301'

255	LOAD_FAST         'index'
258	LOAD_FAST         'self'
261	LOAD_ATTR         'moveList'
264	COMPARE_OP        'not in'
267	JUMP_IF_FALSE     '298'
270	LOAD_FAST         'jump'
273	LOAD_ATTR         'getNum'
276	CALL_FUNCTION_0   None
279	LOAD_FAST         'self'
282	LOAD_ATTR         'moveList'
285	COMPARE_OP        'not in'
288_0	COME_FROM         '267'
288	JUMP_IF_FALSE     '298'

291	LOAD_GLOBAL       'True'
294	RETURN_END_IF     None
295	JUMP_ABSOLUTE     '301'
298	JUMP_ABSOLUTE     '304'

301	CONTINUE          '25'
304	JUMP_BACK         '25'
307	POP_BLOCK         None
308_0	COME_FROM         '12'

308	LOAD_GLOBAL       'False'
311	RETURN_VALUE      None
312	JUMP_FORWARD      '663'

315	LOAD_FAST         'peice'
318	LOAD_CONST        'normal'
321	COMPARE_OP        '=='
324	JUMP_IF_FALSE     '663'

327	LOAD_FAST         'self'
330	LOAD_ATTR         'playerNum'
333	LOAD_CONST        1
336	COMPARE_OP        '=='
339	JUMP_IF_FALSE     '357'

342	LOAD_CONST        1
345	LOAD_CONST        2
348	BUILD_LIST_2      None
351	STORE_FAST        'moveForward'
354	JUMP_FORWARD      '387'

357	LOAD_FAST         'self'
360	LOAD_ATTR         'playerNum'
363	LOAD_CONST        2
366	COMPARE_OP        '=='
369	JUMP_IF_FALSE     '387'

372	LOAD_CONST        0
375	LOAD_CONST        3
378	BUILD_LIST_2      None
381	STORE_FAST        'moveForward'
384	JUMP_FORWARD      '387'
387_0	COME_FROM         '354'
387_1	COME_FROM         '384'

387	SETUP_LOOP        '656'
390	LOAD_FAST         'moveForward'
393	GET_ITER          None
394	FOR_ITER          '655'
397	STORE_FAST        'x'

400	LOAD_FAST         'self'
403	LOAD_ATTR         'board'
406	LOAD_ATTR         'squareList'
409	LOAD_FAST         'index'
412	BINARY_SUBSCR     None
413	LOAD_ATTR         'getAdjacent'
416	CALL_FUNCTION_0   None
419	LOAD_FAST         'x'
422	BINARY_SUBSCR     None
423	LOAD_CONST        None
426	COMPARE_OP        '!='
429	JUMP_IF_FALSE     '652'
432	LOAD_FAST         'self'
435	LOAD_ATTR         'board'
438	LOAD_ATTR         'squareList'
441	LOAD_FAST         'index'
444	BINARY_SUBSCR     None
445	LOAD_ATTR         'getJumps'
448	CALL_FUNCTION_0   None
451	LOAD_FAST         'x'
454	BINARY_SUBSCR     None
455	LOAD_CONST        None
458	COMPARE_OP        '!='
461_0	COME_FROM         '429'
461	JUMP_IF_FALSE     '652'

464	LOAD_FAST         'self'
467	LOAD_ATTR         'board'
470	LOAD_ATTR         'squareList'
473	LOAD_FAST         'self'
476	LOAD_ATTR         'board'
479	LOAD_ATTR         'squareList'
482	LOAD_FAST         'index'
485	BINARY_SUBSCR     None
486	LOAD_ATTR         'getAdjacent'
489	CALL_FUNCTION_0   None
492	LOAD_FAST         'x'
495	BINARY_SUBSCR     None
496	BINARY_SUBSCR     None
497	STORE_FAST        'adj'

500	LOAD_FAST         'self'
503	LOAD_ATTR         'board'
506	LOAD_ATTR         'squareList'
509	LOAD_FAST         'self'
512	LOAD_ATTR         'board'
515	LOAD_ATTR         'squareList'
518	LOAD_FAST         'index'
521	BINARY_SUBSCR     None
522	LOAD_ATTR         'getJumps'
525	CALL_FUNCTION_0   None
528	LOAD_FAST         'x'
531	BINARY_SUBSCR     None
532	BINARY_SUBSCR     None
533	STORE_FAST        'jump'

536	LOAD_FAST         'adj'
539	LOAD_ATTR         'getState'
542	CALL_FUNCTION_0   None
545	LOAD_CONST        0
548	COMPARE_OP        '=='
551	JUMP_IF_FALSE     '557'

554	JUMP_ABSOLUTE     '652'

557	LOAD_FAST         'adj'
560	LOAD_ATTR         'getState'
563	CALL_FUNCTION_0   None
566	LOAD_FAST         'self'
569	LOAD_ATTR         'playerNum'
572	COMPARE_OP        '=='
575	JUMP_IF_TRUE      '603'
578	LOAD_FAST         'adj'
581	LOAD_ATTR         'getState'
584	CALL_FUNCTION_0   None
587	LOAD_FAST         'self'
590	LOAD_ATTR         'playerNum'
593	LOAD_CONST        2
596	BINARY_ADD        None
597	COMPARE_OP        '=='
600_0	COME_FROM         '575'
600	JUMP_IF_FALSE     '606'

603	JUMP_ABSOLUTE     '652'

606	LOAD_FAST         'jump'
609	LOAD_ATTR         'getState'
612	CALL_FUNCTION_0   None
615	LOAD_CONST        0
618	COMPARE_OP        '=='
621	JUMP_IF_FALSE     '649'

624	LOAD_FAST         'index'
627	LOAD_FAST         'self'
630	LOAD_ATTR         'moveList'
633	COMPARE_OP        'not in'
636	JUMP_IF_FALSE     '646'

639	LOAD_GLOBAL       'True'
642	RETURN_VALUE      None
643	JUMP_ABSOLUTE     '649'
646	JUMP_ABSOLUTE     '652'
649	JUMP_BACK         '394'
652	JUMP_BACK         '394'
655	POP_BLOCK         None
656_0	COME_FROM         '387'

656	LOAD_GLOBAL       'False'
659	RETURN_VALUE      None
660	JUMP_FORWARD      '663'
663_0	COME_FROM         '312'
663_1	COME_FROM         '660'
663	LOAD_CONST        None
666	RETURN_VALUE      None

Syntax error at or near `CONTINUE' token at offset 301

    def existsLegalMovesFrom(self, index, peice):
        if peice == 'king':
            for x in self.board.squareList[index].getAdjacent():
                if x != None:
                    if self.board.squareList[x].getState() == 0:
                        return True

            return False
        elif peice == 'normal':
            if self.playerNum == 1:
                moveForward = [1, 2]
            elif self.playerNum == 2:
                moveForward = [0, 3]
            for x in moveForward:
                if self.board.squareList[index].getAdjacent()[x] != None:
                    adj = self.board.squareList[self.board.squareList[index].getAdjacent()[x]]
                    if adj.getState() == 0:
                        return True

            return False
        return

    def checkLegalMove(self, firstSquare, secondSquare, peice):
        if firstSquare.getNum() not in self.mySquares and firstSquare.getNum() not in self.myKings:
            return False
        if self.playerNum == 1:
            moveForward = [1, 2]
        else:
            moveForward = [0, 3]
        if peice == 'king':
            for x in range(4):
                if firstSquare.getAdjacent()[x] != None:
                    if self.board.squareList[firstSquare.getAdjacent()[x]].getState() == 0 and secondSquare.getNum() in firstSquare.getAdjacent():
                        return True

            return False
        elif peice == 'normal':
            for x in moveForward:
                if firstSquare.getAdjacent()[x] != None and secondSquare.getNum() in firstSquare.getAdjacent():
                    if self.board.squareList[firstSquare.getAdjacent()[x]].getState() == 0 and firstSquare.getAdjacent().index(secondSquare.getNum()) == x:
                        return True

            return False
        return

    def checkLegalJump(self, firstSquare, secondSquare, peice):
        if firstSquare.getNum() not in self.mySquares and firstSquare.getNum() not in self.myKings and len(self.moveList) == 1:
            return False
        if self.playerNum == 1:
            moveForward = [1, 2]
            opposingPeices = [2, 4]
        else:
            moveForward = [0, 3]
            opposingPeices = [1, 3]
        if peice == 'king':
            if secondSquare.getNum() in firstSquare.getJumps():
                index = firstSquare.getJumps().index(secondSquare.getNum())
                if self.board.squareList[firstSquare.getAdjacent()[index]].getState() in opposingPeices:
                    return True
                else:
                    return False
        elif peice == 'normal':
            if secondSquare.getNum() in firstSquare.getJumps():
                index = firstSquare.getJumps().index(secondSquare.getNum())
                if index in moveForward:
                    if self.board.squareList[firstSquare.getAdjacent()[index]].getState() in opposingPeices:
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False

    def d_requestMove(self, moveList):
        self.sendUpdate('requestMove', [moveList])

    def setGameState(self, tableState, moveList):
        if moveList != []:
            if self.board.squareList[moveList[0]].getState() == 1 or self.board.squareList[moveList[0]].getState() == 3:
                playerColor = 'white'
            else:
                playerColor = 'black'
            if self.board.squareList[moveList[0]].getState() <= 2:
                self.animatePeice(tableState, moveList, 'normal', playerColor)
            else:
                self.animatePeice(tableState, moveList, 'king', playerColor)
        else:
            self.updateGameState(tableState)

    def updateGameState(self, squares):
        self.board.setStates(squares)
        self.mySquares = []
        self.myKings = []
        messenger.send('wakeup')
        isObserve = False
        if self.playerNum == None:
            self.playerNum = 1
            self.playerColorString = 'white'
            isObserve = True
        for xx in range(32):
            for blah in self.locatorList[xx].getChildren():
                blah.hide()
                if self.locatorList[xx].getChildren().index(blah) != 0:
                    blah1 = blah.find('**/checker_k*')

            owner = self.board.squareList[xx].getState()
            if owner == self.playerNum:
                if self.playerColorString == 'white':
                    x = self.locatorList[xx].getChildren()[1]
                    x.show()
                    x.find('**/checker_k*').hide()
                else:
                    x = self.locatorList[xx].getChildren()[2]
                    x.show()
                    x.find('**/checker_k*').hide()
                self.mySquares.append(xx)
            elif owner == 0:
                self.hideChildren(self.locatorList[xx].getChildren())
            elif owner == self.playerNum + 2:
                if self.playerColorString == 'white':
                    x = self.locatorList[xx].getChildren()[1]
                    x.show()
                    x.find('**/checker_k*').show()
                else:
                    x = self.locatorList[xx].getChildren()[2]
                    x.show()
                    x.find('**/checker_k*').show()
                self.myKings.append(xx)
            elif owner <= 2:
                if self.playerColorString == 'white':
                    x = self.locatorList[xx].getChildren()[2]
                    x.show()
                    x.find('**/checker_k*').hide()
                else:
                    x = self.locatorList[xx].getChildren()[1]
                    x.show()
                    x.find('**/checker_k*').hide()
            elif self.playerColorString == 'white':
                x = self.locatorList[xx].getChildren()[2]
                x.show()
                x.find('**/checker_k*').show()
            else:
                x = self.locatorList[xx].getChildren()[1]
                x.show()
                x.find('**/checker_k*').show()

        if isObserve == True:
            self.playerNum = None
            self.playerColorString = None
            return
        self.mustJump = False
        self.hasNormalMoves = False
        for x in self.myKings:
            if self.existsLegalJumpsFrom(x, 'king') == True:
                self.mustJump = True
                break
            else:
                self.mustJump = False

        if self.mustJump == False:
            for x in self.mySquares:
                if self.existsLegalJumpsFrom(x, 'normal') == True:
                    self.mustJump = True
                    break
                else:
                    self.mustJump = False

        if self.mustJump != True:
            for x in self.mySquares:
                if self.existsLegalMovesFrom(x, 'normal') == True:
                    self.hasNormalMoves = True
                    break
                else:
                    self.hasNormalM
# Can't uncompyle C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\safezone\DistributedCheckers.pyc
Traceback (most recent call last):
  File "C:\python27\lib\uncompyle2\__init__.py", line 206, in main
    uncompyle_file(infile, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 143, in uncompyle_file
    uncompyle(version, co, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 132, in uncompyle
    raise walk.ERROR
ParserError: --- This code section failed: ---

0	LOAD_FAST         'peice'
3	LOAD_CONST        'king'
6	COMPARE_OP        '=='
9	JUMP_IF_FALSE     '315'

12	SETUP_LOOP        '308'
15	LOAD_GLOBAL       'range'
18	LOAD_CONST        4
21	CALL_FUNCTION_1   None
24	GET_ITER          None
25	FOR_ITER          '307'
28	STORE_FAST        'x'

31	LOAD_FAST         'self'
34	LOAD_ATTR         'board'
37	LOAD_ATTR         'squareList'
40	LOAD_FAST         'index'
43	BINARY_SUBSCR     None
44	LOAD_ATTR         'getAdjacent'
47	CALL_FUNCTION_0   None
50	LOAD_FAST         'x'
53	BINARY_SUBSCR     None
54	LOAD_CONST        None
57	COMPARE_OP        '!='
60	JUMP_IF_FALSE     '304'
63	LOAD_FAST         'self'
66	LOAD_ATTR         'board'
69	LOAD_ATTR         'squareList'
72	LOAD_FAST         'index'
75	BINARY_SUBSCR     None
76	LOAD_ATTR         'getJumps'
79	CALL_FUNCTION_0   None
82	LOAD_FAST         'x'
85	BINARY_SUBSCR     None
86	LOAD_CONST        None
89	COMPARE_OP        '!='
92_0	COME_FROM         '60'
92	JUMP_IF_FALSE     '304'

95	LOAD_FAST         'self'
98	LOAD_ATTR         'board'
101	LOAD_ATTR         'squareList'
104	LOAD_FAST         'self'
107	LOAD_ATTR         'board'
110	LOAD_ATTR         'squareList'
113	LOAD_FAST         'index'
116	BINARY_SUBSCR     None
117	LOAD_ATTR         'getAdjacent'
120	CALL_FUNCTION_0   None
123	LOAD_FAST         'x'
126	BINARY_SUBSCR     None
127	BINARY_SUBSCR     None
128	STORE_FAST        'adj'

131	LOAD_FAST         'self'
134	LOAD_ATTR         'board'
137	LOAD_ATTR         'squareList'
140	LOAD_FAST         'self'
143	LOAD_ATTR         'board'
146	LOAD_ATTR         'squareList'
149	LOAD_FAST         'index'
152	BINARY_SUBSCR     None
153	LOAD_ATTR         'getJumps'
156	CALL_FUNCTION_0   None
159	LOAD_FAST         'x'
162	BINARY_SUBSCR     None
163	BINARY_SUBSCR     None
164	STORE_FAST        'jump'

167	LOAD_FAST         'adj'
170	LOAD_ATTR         'getState'
173	CALL_FUNCTION_0   None
176	LOAD_CONST        0
179	COMPARE_OP        '=='
182	JUMP_IF_FALSE     '188'

185	JUMP_ABSOLUTE     '304'

188	LOAD_FAST         'adj'
191	LOAD_ATTR         'getState'
194	CALL_FUNCTION_0   None
197	LOAD_FAST         'self'
200	LOAD_ATTR         'playerNum'
203	COMPARE_OP        '=='
206	JUMP_IF_TRUE      '234'
209	LOAD_FAST         'adj'
212	LOAD_ATTR         'getState'
215	CALL_FUNCTION_0   None
218	LOAD_FAST         'self'
221	LOAD_ATTR         'playerNum'
224	LOAD_CONST        2
227	BINARY_ADD        None
228	COMPARE_OP        '=='
231_0	COME_FROM         '206'
231	JUMP_IF_FALSE     '237'

234	JUMP_ABSOLUTE     '304'

237	LOAD_FAST         'jump'
240	LOAD_ATTR         'getState'
243	CALL_FUNCTION_0   None
246	LOAD_CONST        0
249	COMPARE_OP        '=='
252	JUMP_IF_FALSE     '301'

255	LOAD_FAST         'index'
258	LOAD_FAST         'self'
261	LOAD_ATTR         'moveList'
264	COMPARE_OP        'not in'
267	JUMP_IF_FALSE     '298'
270	LOAD_FAST         'jump'
273	LOAD_ATTR         'getNum'
276	CALL_FUNCTION_0   None
279	LOAD_FAST         'self'
282	LOAD_ATTR         'moveList'
285	COMPARE_OP        'not in'
288_0	COME_FROM         '267'
288	JUMP_IF_FALSE     '298'

291	LOAD_GLOBAL       'True'
294	RETURN_END_IF     None
295	JUMP_ABSOLUTE     '301'
298	JUMP_ABSOLUTE     '304'

301	CONTINUE          '25'
304	JUMP_BACK         '25'
307	POP_BLOCK         None
308_0	COME_FROM         '12'

308	LOAD_GLOBAL       'False'
311	RETURN_VALUE      None
312	JUMP_FORWARD      '663'

315	LOAD_FAST         'peice'
318	LOAD_CONST        'normal'
321	COMPARE_OP        '=='
324	JUMP_IF_FALSE     '663'

327	LOoves = False
                if self.hasNormalMoves == False:
                    for x in self.myKings:
                        if self.existsLegalMovesFrom(x, 'king') == True:
                            self.hasNormalMoves = True
                            break
                        else:
                            self.hasNormalMoves = False

        if self.mustJump == False and self.hasNormalMoves == False:
            pass
        return

    def hideChildren(self, nodeList):
        for x in range(1, 2):
            nodeList[x].hide()

    def animatePeice(self, tableState, moveList, type, playerColor):
        messenger.send('wakeup')
        if playerColor == 'white':
            gamePeiceForAnimation = loader.loadModel('phase_6/models/golf/regular_checker_piecewhite.bam')
        else:
            gamePeiceForAnimation = loader.loadModel('phase_6/models/golf/regular_checker_pieceblack.bam')
        if type == 'king':
            gamePeiceForAnimation.find('**/checker_k*').show()
        else:
            gamePeiceForAnimation.find('**/checker_k*').hide()
        gamePeiceForAnimation.reparentTo(self.boardNode)
        gamePeiceForAnimation.setPos(self.locatorList[moveList[0]].getPos())
        if self.isRotated == True:
            gamePeiceForAnimation.setH(180)
        for x in self.locatorList[moveList[0]].getChildren():
            x.hide()

        checkersPeiceTrack = Sequence()
        length = len(moveList)
        for x in range(length - 1):
            checkersPeiceTrack.append(Parallel(SoundInterval(self.moveSound), ProjectileInterval(gamePeiceForAnimation, endPos=self.locatorList[moveList[x + 1]].getPos(), duration=0.5)))

        checkersPeiceTrack.append(Func(gamePeiceForAnimation.removeNode))
        checkersPeiceTrack.append(Func(self.updateGameState, tableState))
        checkersPeiceTrack.append(Func(self.unAlpha, moveList))
        checkersPeiceTrack.start()

    def announceWin(self, avId):
        self.fsm.request('gameOver')

    def unAlpha(self, moveList):
        for x in moveList:
            self.locatorList[x].setColorOff()

    def doRandomMove(self):
        import random
        move = []
        foundLegal = False
        self.blinker.pause()
        self.numRandomMoves += 1
        while not foundLegal:
            x = random.randint(0, 9)
            for y in self.board.getAdjacent(self.mySquares[x]):
                if y != None and self.board.getState(y) == 0:
                    move.append(self.mySquares[x])
                    move.append(y)
                    foundLegal = True
                    break

        if move == []:
            pass
        playSound = Sequence(SoundInterval(self.knockSound))
        playSound.start()
        self.d_requestMove(move)
        self.moveList = []
        self.isMyTurn = False
        if self.numRandomMoves >= 5:
            self.exitButtonPushed()
        return

    def doNothing(self):
        pass# decompiled 0 files: 0 okay, 1 failed, 0 verify failed
# 2013.08.22 22:24:27 Pacific Daylight Time
AD_FAST         'self'
330	LOAD_ATTR         'playerNum'
333	LOAD_CONST        1
336	COMPARE_OP        '=='
339	JUMP_IF_FALSE     '357'

342	LOAD_CONST        1
345	LOAD_CONST        2
348	BUILD_LIST_2      None
351	STORE_FAST        'moveForward'
354	JUMP_FORWARD      '387'

357	LOAD_FAST         'self'
360	LOAD_ATTR         'playerNum'
363	LOAD_CONST        2
366	COMPARE_OP        '=='
369	JUMP_IF_FALSE     '387'

372	LOAD_CONST        0
375	LOAD_CONST        3
378	BUILD_LIST_2      None
381	STORE_FAST        'moveForward'
384	JUMP_FORWARD      '387'
387_0	COME_FROM         '354'
387_1	COME_FROM         '384'

387	SETUP_LOOP        '656'
390	LOAD_FAST         'moveForward'
393	GET_ITER          None
394	FOR_ITER          '655'
397	STORE_FAST        'x'

400	LOAD_FAST         'self'
403	LOAD_ATTR         'board'
406	LOAD_ATTR         'squareList'
409	LOAD_FAST         'index'
412	BINARY_SUBSCR     None
413	LOAD_ATTR         'getAdjacent'
416	CALL_FUNCTION_0   None
419	LOAD_FAST         'x'
422	BINARY_SUBSCR     None
423	LOAD_CONST        None
426	COMPARE_OP        '!='
429	JUMP_IF_FALSE     '652'
432	LOAD_FAST         'self'
435	LOAD_ATTR         'board'
438	LOAD_ATTR         'squareList'
441	LOAD_FAST         'index'
444	BINARY_SUBSCR     None
445	LOAD_ATTR         'getJumps'
448	CALL_FUNCTION_0   None
451	LOAD_FAST         'x'
454	BINARY_SUBSCR     None
455	LOAD_CONST        None
458	COMPARE_OP        '!='
461_0	COME_FROM         '429'
461	JUMP_IF_FALSE     '652'

464	LOAD_FAST         'self'
467	LOAD_ATTR         'board'
470	LOAD_ATTR         'squareList'
473	LOAD_FAST         'self'
476	LOAD_ATTR         'board'
479	LOAD_ATTR         'squareList'
482	LOAD_FAST         'index'
485	BINARY_SUBSCR     None
486	LOAD_ATTR         'getAdjacent'
489	CALL_FUNCTION_0   None
492	LOAD_FAST         'x'
495	BINARY_SUBSCR     None
496	BINARY_SUBSCR     None
497	STORE_FAST        'adj'

500	LOAD_FAST         'self'
503	LOAD_ATTR         'board'
506	LOAD_ATTR         'squareList'
509	LOAD_FAST         'self'
512	LOAD_ATTR         'board'
515	LOAD_ATTR         'squareList'
518	LOAD_FAST         'index'
521	BINARY_SUBSCR     None
522	LOAD_ATTR         'getJumps'
525	CALL_FUNCTION_0   None
528	LOAD_FAST         'x'
531	BINARY_SUBSCR     None
532	BINARY_SUBSCR     None
533	STORE_FAST        'jump'

536	LOAD_FAST         'adj'
539	LOAD_ATTR         'getState'
542	CALL_FUNCTION_0   None
545	LOAD_CONST        0
548	COMPARE_OP        '=='
551	JUMP_IF_FALSE     '557'

554	JUMP_ABSOLUTE     '652'

557	LOAD_FAST         'adj'
560	LOAD_ATTR         'getState'
563	CALL_FUNCTION_0   None
566	LOAD_FAST         'self'
569	LOAD_ATTR         'playerNum'
572	COMPARE_OP        '=='
575	JUMP_IF_TRUE      '603'
578	LOAD_FAST         'adj'
581	LOAD_ATTR         'getState'
584	CALL_FUNCTION_0   None
587	LOAD_FAST         'self'
590	LOAD_ATTR         'playerNum'
593	LOAD_CONST        2
596	BINARY_ADD        None
597	COMPARE_OP        '=='
600_0	COME_FROM         '575'
600	JUMP_IF_FALSE     '606'

603	JUMP_ABSOLUTE     '652'

606	LOAD_FAST         'jump'
609	LOAD_ATTR         'getState'
612	CALL_FUNCTION_0   None
615	LOAD_CONST        0
618	COMPARE_OP        '=='
621	JUMP_IF_FALSE     '649'

624	LOAD_FAST         'index'
627	LOAD_FAST         'self'
630	LOAD_ATTR         'moveList'
633	COMPARE_OP        'not in'
636	JUMP_IF_FALSE     '646'

639	LOAD_GLOBAL       'True'
642	RETURN_VALUE      None
643	JUMP_ABSOLUTE     '649'
646	JUMP_ABSOLUTE     '652'
649	JUMP_BACK         '394'
652	JUMP_BACK         '394'
655	POP_BLOCK         None
656_0	COME_FROM         '387'

656	LOAD_GLOBAL       'False'
659	RETURN_VALUE      None
660	JUMP_FORWARD      '663'
663_0	COME_FROM         '312'
663_1	COME_FROM         '660'
663	LOAD_CONST        None
666	RETURN_VALUE      None

Syntax error at or near `CONTINUE' token at offset 301

