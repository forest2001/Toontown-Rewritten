from direct.directnotify import DirectNotifyGlobal
from direct.showbase.PythonUtil import invertDictLossless
from toontown.coghq import MintRoomSpecs
from toontown.toonbase import ToontownGlobals
from direct.showbase.PythonUtil import normalDistrib, lerp
import random

def printAllCashbotInfo():
    print 'roomId: roomName'
    for roomId, roomName in MintRoomSpecs.CashbotMintRoomId2RoomName.items():
        print '%s: %s' % (roomId, roomName)

    print '\nroomId: numBattles'
    for roomId, numBattles in MintRoomSpecs.roomId2numBattles.items():
        print '%s: %s' % (roomId, numBattles)

    print '\nmintId floor roomIds'
    printMintRoomIds()
    print '\nmintId floor numRooms'
    printNumRooms()
    print '\nmintId floor numForcedBattles'
    printNumBattles()


def iterateCashbotMints(func):
    from toontown.toonbase import ToontownGlobals
    for mintId in [ToontownGlobals.CashbotMintIntA, ToontownGlobals.CashbotMintIntB, ToontownGlobals.CashbotMintIntC]:
        for floorNum in xrange(ToontownGlobals.MintNumFloors[mintId]):
            func(MintLayout(mintId, floorNum))


def printMintInfo():

    def func(ml):
        print ml

    iterateCashbotMints(func)


def printMintRoomIds():

    def func(ml):
        print ml.getMintId(), ml.getFloorNum(), ml.getRoomIds()

    iterateCashbotMints(func)


def printMintRoomNames():

    def func(ml):
        print ml.getMintId(), ml.getFloorNum(), ml.getRoomNames()

    iterateCashbotMints(func)


def printNumRooms():

    def func(ml):
        print ml.getMintId(), ml.getFloorNum(), ml.getNumRooms()

    iterateCashbotMints(func)


def printNumBattles():

    def func(ml):
        print ml.getMintId(), ml.getFloorNum(), ml.getNumBattles()

    iterateCashbotMints(func)


BakedFloorLayouts = {12500: {0: (0,
             4,
             9,
             6,
             5,
             8,
             17),
         1: (0,
             15,
             13,
             16,
             7,
             6,
             22),
         2: (0,
             4,
             11,
             3,
             9,
             6,
             14,
             19),
         3: (0,
             1,
             3,
             4,
             16,
             14,
             15,
             24),
         4: (0,
             15,
             5,
             8,
             9,
             11,
             10,
             21),
         5: (0,
             13,
             12,
             8,
             7,
             16,
             10,
             18),
         6: (0,
             16,
             13,
             5,
             12,
             7,
             1,
             23),
         7: (0,
             10,
             12,
             7,
             3,
             13,
             16,
             8,
             20),
         8: (0,
             3,
             5,
             7,
             6,
             1,
             4,
             9,
             25),
         9: (0,
             6,
             9,
             10,
             13,
             16,
             8,
             4,
             22),
         10: (0,
              13,
              1,
              7,
              2,
              16,
              11,
              3,
              19),
         11: (0,
              3,
              1,
              6,
              4,
              14,
              8,
              9,
              24),
         12: (0,
              7,
              14,
              2,
              1,
              8,
              5,
              10,
              11,
              21),
         13: (0,
              13,
              6,
              4,
              11,
              3,
              9,
              10,
              8,
              17),
         14: (0,
              15,
              5,
              1,
              14,
              10,
              4,
              7,
              16,
              23),
         15: (0,
              16,
              10,
              11,
              2,
              1,
              3,
              14,
              5,
              20),
         16: (0,
              5,
              8,
              10,
              6,
              3,
              15,
              14,
              7,
              25),
         17: (0,
              12,
              13,
              5,
              8,
              14,
              11,
              7,
              16,
              10,
              22),
         18: (0,
              11,
              3,
              15,
              7,
              16,
              14,
              6,
              1,
              5,
              18),
         19: (0,
              10,
              16,
              11,
              3,
              5,
              12,
              13,
              7,
              14,
              24)},
 12600: {0: (0,
             8,
             1,
             6,
             14,
             2,
             5,
             9,
             17),
         1: (0,
             4,
             14,
             7,
             2,
             13,
             8,
             9,
             18),
         2: (0,
             7,
             9,
             6,
             5,
             14,
             12,
             3,
             20),
         3: (0,
             6,
             2,
             13,
             16,
             7,
             5,
             3,
             9,
             22),
         4: (0,
             15,
             4,
             9,
             8,
             6,
             13,
             5,
             11,
             23),
         5: (0,
             13,
             7,
             14,
             15,
             11,
             3,
             2,
             8,
             25),
         6: (0,
             5,
             14,
             2,
             11,
             7,
             16,
             10,
             15,
             18),
         7: (0,
             10,
             9,
             5,
             4,
             2,
             7,
             13,
             11,
             19),
         8: (0,
             11,
             4,
             12,
             6,
             1,
             13,
             7,
             3,
             21),
         9: (0,
             15,
             16,
             5,
             13,
             9,
             14,
             4,
             6,
             3,
             23),
         10: (0,
              16,
              15,
              7,
              6,
              8,
              3,
              4,
              9,
              10,
              24),
         11: (0,
              5,
              8,
              4,
              12,
              13,
              9,
              11,
              16,
              3,
              17),
         12: (0,
              13,
              16,
              7,
              4,
              12,
              3,
              6,
              5,
              1,
              19),
         13: (0,
              14,
              6,
              12,
              13,
              7,
              10,
              3,
              16,
              9,
              20),
         14: (0,
              9,
              15,
              13,
              5,
              6,
              3,
              14,
              11,
              4,
              22),
         15: (0,
              13,
              14,
              3,
              12,
              16,
              11,
              9,
              4,
              5,
              7,
              24),
         16: (0,
              3,
              6,
              1,
              7,
              5,
              10,
              9,
              4,
              13,
              15,
              25),
         17: (0,
              3,
              6,
              14,
              4,
              13,
              16,
              12,
              8,
              5,
              7,
              18),
         18: (0,
              11,
              13,
              4,
              1,
              15,
              6,
              3,
              8,
              9,
              16,
              20),
         19: (0,
              11,
              5,
              8,
              7,
              2,
              6,
              13,
              3,
              14,
              9,
              21)},
 12700: {0: (0,
             16,
             14,
             6,
             1,
             5,
             9,
             2,
             15,
             8,
             17),
         1: (0,
             3,
             2,
             12,
             14,
             8,
             13,
             6,
             10,
             7,
             23),
         2: (0,
             15,
             9,
             5,
             12,
             7,
             4,
             11,
             14,
             16,
             21),
         3: (0,
             2,
             13,
             7,
             6,
             8,
             15,
             4,
             1,
             11,
             19),
         4: (0,
             12,
             7,
             4,
             6,
             10,
             14,
             13,
             16,
             15,
             11,
             17),
         5: (0,
             10,
             2,
             9,
             13,
             4,
             8,
             1,
             15,
             14,
             11,
             23),
         6: (0,
             2,
             14,
             4,
             10,
             16,
             15,
             1,
             3,
             8,
             6,
             21),
         7: (0,
             14,
             11,
             1,
             7,
             9,
             10,
             12,
             8,
             5,
             2,
             19),
         8: (0,
             9,
             11,
             8,
             5,
             1,
             4,
             3,
             7,
             15,
             2,
             17),
         9: (0,
             2,
             9,
             7,
             11,
             16,
             10,
             15,
             3,
             8,
             6,
             23),
         10: (0,
              4,
              10,
              6,
              8,
              7,
              15,
              2,
              1,
              3,
              13,
              21),
         11: (0,
              10,
              14,
              8,
              6,
              9,
              15,
              5,
              1,
              2,
              13,
              19),
         12: (0,
              16,
              5,
              12,
              10,
              6,
              9,
              11,
              3,
              15,
              13,
              17),
         13: (0,
              1,
              3,
              6,
              14,
              4,
              10,
              12,
              15,
              13,
              16,
              24),
         14: (0,
              8,
              7,
              14,
              9,
              1,
              2,
              6,
              16,
              10,
              15,
              13,
              21),
         15: (0,
              4,
              1,
              8,
              11,
              12,
              3,
              10,
              16,
              13,
              6,
              15,
              19),
         16: (0,
              6,
              3,
              10,
              4,
              1,
              2,
              13,
              11,
              5,
              15,
              16,
              17),
         17: (0,
              6,
              16,
              5,
              12,
              11,
              1,
              8,
              14,
              15,
              9,
              10,
              24),
         18: (0,
              15,
              8,
              12,
              10,
              1,
              7,
              11,
              9,
              16,
              4,
              5,
              21),
         19: (0,
              10,
              2,
              16,
              5,
              6,
              11,
              13,
              7,
              12,
              1,
              3,
              19)}}

class MintLayout():
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('MintLayout')

    def __init__(self, mintId, floorNum):
        self.mintId = mintId
        self.floorNum = floorNum
        self.roomIds = []
        self.hallways = []
        self.numRooms = 1 + ToontownGlobals.MintNumRooms[self.mintId][self.floorNum]
        self.numHallways = self.numRooms - 1
        if self.mintId in BakedFloorLayouts and self.floorNum in BakedFloorLayouts[self.mintId]:
            self.roomIds = list(BakedFloorLayouts[self.mintId][self.floorNum])
        else:
            self.roomIds = self._genFloorLayout()
        hallwayRng = self.getRng()
        connectorRoomNames = MintRoomSpecs.CashbotMintConnectorRooms
        for i in xrange(self.numHallways):
            self.hallways.append(hallwayRng.choice(connectorRoomNames))

    def _genFloorLayout--- This code section failed: ---

0	LOAD_FAST         'self'
3	LOAD_ATTR         'getRng'
6	CALL_FUNCTION_0   None
9	STORE_FAST        'rng'

12	LOAD_GLOBAL       'MintRoomSpecs'
15	LOAD_ATTR         'CashbotMintEntranceIDs'
18	STORE_FAST        'startingRoomIDs'

21	LOAD_GLOBAL       'MintRoomSpecs'
24	LOAD_ATTR         'CashbotMintMiddleRoomIDs'
27	STORE_FAST        'middleRoomIDs'

30	LOAD_GLOBAL       'MintRoomSpecs'
33	LOAD_ATTR         'CashbotMintFinalRoomIDs'
36	STORE_FAST        'finalRoomIDs'

39	LOAD_GLOBAL       'ToontownGlobals'
42	LOAD_ATTR         'MintNumBattles'
45	LOAD_FAST         'self'
48	LOAD_ATTR         'mintId'
51	BINARY_SUBSCR     None
52	STORE_FAST        'numBattlesLeft'

55	LOAD_FAST         'rng'
58	LOAD_ATTR         'choice'
61	LOAD_FAST         'finalRoomIDs'
64	CALL_FUNCTION_1   None
67	STORE_FAST        'finalRoomId'

70	LOAD_FAST         'numBattlesLeft'
73	LOAD_GLOBAL       'MintRoomSpecs'
76	LOAD_ATTR         'getNumBattles'
79	LOAD_FAST         'finalRoomId'
82	CALL_FUNCTION_1   None
85	INPLACE_SUBTRACT  None
86	STORE_FAST        'numBattlesLeft'

89	BUILD_LIST_0      None
92	STORE_FAST        'middleRoomIds'

95	LOAD_FAST         'self'
98	LOAD_ATTR         'numRooms'
101	LOAD_CONST        2
104	BINARY_SUBTRACT   None
105	STORE_FAST        'middleRoomsLeft'

108	LOAD_GLOBAL       'invertDictLossless'
111	LOAD_GLOBAL       'MintRoomSpecs'
114	LOAD_ATTR         'middleRoomId2numBattles'
117	CALL_FUNCTION_1   None
120	STORE_FAST        'numBattles2middleRoomIds'

123	BUILD_LIST_0      None
126	STORE_FAST        'allBattleRooms'

129	SETUP_LOOP        '186'
132	LOAD_FAST         'numBattles2middleRoomIds'
135	LOAD_ATTR         'items'
138	CALL_FUNCTION_0   None
141	GET_ITER          None
142	FOR_ITER          '185'
145	UNPACK_SEQUENCE_2 None
148	STORE_FAST        'num'
151	STORE_FAST        'roomIds'

154	LOAD_FAST         'num'
157	LOAD_CONST        0
160	COMPARE_OP        '>'
163	JUMP_IF_FALSE     '182'

166	LOAD_FAST         'allBattleRooms'
169	LOAD_ATTR         'extend'
172	LOAD_FAST         'roomIds'
175	CALL_FUNCTION_1   None
178	POP_TOP           None
179	JUMP_BACK         '142'
182	JUMP_BACK         '142'
185	POP_BLOCK         None
186_0	COME_FROM         '129'

186	SETUP_LOOP        '268'

189	LOAD_GLOBAL       'list'
192	LOAD_FAST         'allBattleRooms'
195	CALL_FUNCTION_1   None
198	STORE_FAST        'allBattleRoomIds'

201	LOAD_FAST         'rng'
204	LOAD_ATTR         'shuffle'
207	LOAD_FAST         'allBattleRoomIds'
210	CALL_FUNCTION_1   None
213	POP_TOP           None

214	LOAD_FAST         'self'
217	LOAD_ATTR         '_chooseBattleRooms'
220	LOAD_FAST         'numBattlesLeft'

223	LOAD_FAST         'allBattleRoomIds'
226	CALL_FUNCTION_2   None
229	STORE_FAST        'battleRoomIds'

232	LOAD_FAST         'battleRoomIds'
235	LOAD_CONST        None
238	COMPARE_OP        'is not'
241	JUMP_IF_FALSE     '248'

244	BREAK_LOOP        None
245	JUMP_FORWARD      '248'
248_0	COME_FROM         '245'

248	LOAD_GLOBAL       'MintLayout'
251	LOAD_ATTR         'notify'
254	LOAD_ATTR         'info'
257	LOAD_CONST        'could not find a valid set of battle rooms, trying again'
260	CALL_FUNCTION_1   None
263	POP_TOP           None
264	JUMP_BACK         '189'
267	POP_BLOCK         None
268_0	COME_FROM         '186'

268	LOAD_FAST         'middleRoomIds'
271	LOAD_ATTR         'extend'
274	LOAD_FAST         'battleRoomIds'
277	CALL_FUNCTION_1   None
280	POP_TOP           None

281	LOAD_FAST         'middleRoomsLeft'
284	LOAD_GLOBAL       'len'
287	LOAD_FAST         'battleRoomIds'
290	CALL_FUNCTION_1   None
293	INPLACE_SUBTRACT  None
294	STORE_FAST        'middleRoomsLeft'

297	LOAD_FAST         'middleRoomsLeft'
300	LOAD_CONST        0
303	COMPARE_OP        '>'
306	JUMP_IF_FALSE     '386'

309	LOAD_FAST         'numBattles2middleRoomIds'
312	LOAD_CONST        0
315	BINARY_SUBSCR     None
316	STORE_FAST        'actionRoomIds'

319	SETUP_LOOP        '386'
322	LOAD_GLOBAL       'xrange'
325	LOAD_FAST         'middleRoomsLeft'
328	CALL_FUNCTION_1   None
331	GET_ITER          None
332	FOR_ITER          '382'
335	STORE_FAST        'i'

338	LOAD_FAST         'rng'
341	LOAD_ATTR         'choice'
344	LOAD_FAST         'actionRoomIds'
347	CALL_FUNCTION_1   None
350	STORE_FAST        'roomId'

353	LOAD_FAST         'actionRoomIds'
356	LOAD_ATTR         'remove'
359	LOAD_FAST         'roomId'
362	CALL_FUNCTION_1   None
365	POP_TOP           None

366	LOAD_FAST         'middleRoomIds'
369	LOAD_ATTR         'append'
372	LOAD_FAST         'roomId'
375	CALL_FUNCTION_1   None
378	POP_TOP           None
379	JUMP_BACK         '332'
382	POP_BLOCK         None
383_0	COME_FROM         '319'
383	JUMP_FORWARD      '386'
386_0	COME_FROM         '383'

386	BUILD_LIST_0      None
389	STORE_FAST        'roomIds'

392	LOAD_FAST         'roomIds'
395	LOAD_ATTR         'append'
398	LOAD_FAST         'rng'
401	LOAD_ATTR         'choice'
404	LOAD_FAST         'startingRoomIDs'
407	CALL_FUNCTION_1   None
410	CALL_FUNCTION_1   None
413	POP_TOP           None

414	LOAD_FAST         'rng'
417	LOAD_ATTR         'shuffle'
420	LOAD_FAST         'middleRoomIds'
423	CALL_FUNCTION_1   None
426	POP_TOP           None

427	LOAD_FAST         'roomIds'
430	LOAD_ATTR         'extend'
433	LOAD_FAST         'middleRoomIds'
436	CALL_FUNCTION_1   None
439	POP_TOP           None

440	LOAD_FAST         'roomIds'
443	LOAD_ATTR         'append'
446	LOAD_FAST         'finalRoomId'
449	CALL_FUNCTION_1   None
452	POP_TOP           None

453	LOAD_FAST         'roomIds'
456	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 267

    def getNumRooms(self):
        return len(self.roomIds)

    def getRoomId(self, n):
        return self.roomIds[n]

    def getRoomIds(self):
        return self.roomIds[:]

    def getRoomNames(self):
        names = []
        for roomId in self.roomIds:
            names.append(MintRoomSpecs.CashbotMintRoomId2RoomName[roomId])

        return names

    def getNumHallways(self):
        return len(self.hallways)

    def getHallwayModel(self, n):
        return self.hallways[n]

    def getNumBattles(self):
        numBattles = 0
        for roomId in self.getRoomIds():
            numBattles += MintRoomSpecs.roomId2numBattles[roomId]

        return numBattles

    def getMintId(self):
        return self.mintId

    def getFloorNum(self):
        return self.floorNum

    def getRng(self):
        return random.Random(self.mintId * self.floorNum)

    def _chooseBattleRooms(self, numBattlesLeft, allBattleRoomIds, baseIndex = 0, chosenBattleRooms = None):
        if chosenBattleRooms is None:
            chosenBattleRooms = []
        while baseIndex < len(allBattleRoomIds):
            nextRoomId = allBattleRoomIds[baseIndex]
            baseIndex += 1
            newNumBattlesLef
# Can't uncompyle C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\coghq\MintLayout.pyc
Traceback (most recent call last):
  File "C:\python27\lib\uncompyle2\__init__.py", line 206, in main
    uncompyle_file(infile, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 143, in uncompyle_file
    uncompyle(version, co, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 132, in uncompyle
    raise walk.ERROR
ParserError: --- This code section failed: ---

0	LOAD_FAST         'self'
3	LOAD_ATTR         'getRng'
6	CALL_FUNCTION_0   None
9	STORE_FAST        'rng'

12	LOAD_GLOBAL       'MintRoomSpecs'
15	LOAD_ATTR         'CashbotMintEntranceIDs'
18	STORE_FAST        'startingRoomIDs'

21	LOAD_GLOBAL       'MintRoomSpecs'
24	LOAD_ATTR         'CashbotMintMiddleRoomIDs'
27	STORE_FAST        'middleRoomIDs'

30	LOAD_GLOBAL       'MintRoomSpecs'
33	LOAD_ATTR         'CashbotMintFinalRoomIDs'
36	STORE_FAST        'finalRoomIDs'

39	LOAD_GLOBAL       'ToontownGlobals'
42	LOAD_ATTR         'MintNumBattles'
45	LOAD_FAST         'self'
48	LOAD_ATTR         'mintId'
51	BINARY_SUBSCR     None
52	STORE_FAST        'numBattlesLeft'

55	LOAD_FAST         'rng'
58	LOAD_ATTR         'choice'
61	LOAD_FAST         'finalRoomIDs'
64	CALL_FUNCTION_1   None
67	STORE_FAST        'finalRoomId'

70	LOAD_FAST         'numBattlesLeft'
73	LOAD_GLOBAL       'MintRoomSpecs'
76	LOAD_ATTR         'getNumBattles'
79	LOAD_FAST         'finalRoomId'
82	CALL_FUNCTION_1   None
85	INPLACE_SUBTRACT  None
86	STORE_FAST        'numBattlesLeft'

89	BUILD_LIST_0      None
92	STORE_FAST        'middleRoomIds'

95	LOAD_FAST         'self'
98	LOAD_ATTR         'numRooms'
101	LOAD_CONST        2
104	BINARY_SUBTRACT   None
105	STORE_FAST        'middleRoomsLeft'

108	LOAD_GLOBAL       'invertDictLossless'
111	LOAD_GLOBAL       'MintRoomSpecs'
114	LOAD_ATTR         'middleRoomId2numBattles'
117	CALL_FUNCTION_1   None
120	STORE_FAST        'numBattles2middleRoomIds'

123	BUILD_LIST_0      None
126	STORE_FAST        'allBattleRooms'

129	SETUP_LOOP        '186'
132	LOAD_FAST         'numBattles2middleRoomIds'
135	LOAD_ATTR         'items'
138	CALL_FUNCTION_0   None
141	GET_ITER          None
142	FOR_ITER          '185'
145	UNPACK_SEQUENCE_2 None
148	STORE_FAST        'num'
151	STORE_FAST        'roomIds'

154	LOAD_FAST         'num'
157	LOAD_CONST        0
160	COMPARE_OP        '>'
163	JUMP_IF_FALSE     '182'

166	LOAD_FAST         'allBattleRooms'
169	LOAD_ATTR         'extend'
172	LOAD_FAST         'roomIds'
175	CALL_FUNCTION_1   None
178	POP_TOP           None
179	JUMP_BACK         '142'
182	JUMP_BACK         '142'
185	POP_BLOCK         None
186_0	COME_FROM         '129'

186	SETUP_LOOP        '268'

189	LOAD_GLOBAL       'list'
192	LOAD_FAST         'allBattleRooms'
195	CALL_FUNCTION_1   None
198	STORE_FAST        'allBattleRoomIds'

201	LOAD_FAST         'rng'
204	LOAD_ATTR         'shuffle'
207	LOAD_FAST         'allBattleRoomIds'
210	CALL_FUNCTION_1   None
213	POP_TOP           None

214	LOAD_FAST         'self'
217	LOAD_ATTR         '_chooseBattleRooms'
220	LOAD_FAST         'numBattlesLeft'

223	LOAD_FAST         'allBattleRoomIds'
226	CALL_FUNCTION_2   None
229	STORE_FAST        'battleRoomIds'

232	LOAD_FAST         'battleRoomIds'
235	LOAD_CONST        None
238	COMPARE_OP        'is not'
241	JUMP_IF_FALSE     '248'

244	BREAK_LOOP        None
245	JUMP_FORWARD      '248'
248_0	COME_FROM         '245'

248	LOAD_GLOBAL       'MintLayout'
251	LOAD_ATTR         'notify'
254	LOAD_ATTR         'info'
257	LOAD_CONST        'could not find a valid set of battle rooms, trying again'
260	CALL_FUNCTION_1   None
263	POP_TOP           None
264	JUMP_BACK         '189'
267	POP_BLOCK         None
268_0	COME_FROM         '186'

268	LOAD_FAST         'middleRoomIds'
271	LOAD_ATTR         'extend'
274	LOAD_FAST         'battleRoomIds'
277	CALL_FUNCTION_1   None
280	POP_TOP           None

281	LOAD_FAST         'middleRoomsLeft'
284	LOAD_GLOBAL       'len'
287	LOAD_FAST         'battleRoomIdst = numBattlesLeft - MintRoomSpecs.middleRoomId2numBattles[nextRoomId]
            if newNumBattlesLeft < 0:
                continue
            elif newNumBattlesLeft == 0:
                chosenBattleRooms.append(nextRoomId)
                return chosenBattleRooms
            chosenBattleRooms.append(nextRoomId)
            result = self._chooseBattleRooms(newNumBattlesLeft, allBattleRoomIds, baseIndex, chosenBattleRooms)
            if result is not None:
                return result
            else:
                del chosenBattleRooms[-1:]
        else:
            return

        return

    def __str__(self):
        return 'MintLayout: id=%s, floor=%s, numRooms=%s, numBattles=%s' % (self.mintId,
         self.floorNum,
         self.getNumRooms(),
         self.getNumBattles())

    def __repr__(self):
        return str(self)# decompiled 0 files: 0 okay, 1 failed, 0 verify failed
'
290	CALL_FUNCTION_1   None
293	INPLACE_SUBTRACT  None
294	STORE_FAST        'middleRoomsLeft'

297	LOAD_FAST         'middleRoomsLeft'
300	LOAD_CONST        0
303	COMPARE_OP        '>'
306	JUMP_IF_FALSE     '386'

309	LOAD_FAST         'numBattles2middleRoomIds'
312	LOAD_CONST        0
315	BINARY_SUBSCR     None
316	STORE_FAST        'actionRoomIds'

319	SETUP_LOOP        '386'
322	LOAD_GLOBAL       'xrange'
325	LOAD_FAST         'middleRoomsLeft'
328	CALL_FUNCTION_1   None
331	GET_ITER          None
332	FOR_ITER          '382'
335	STORE_FAST        'i'

338	LOAD_FAST         'rng'
341	LOAD_ATTR         'choice'
344	LOAD_FAST         'actionRoomIds'
347	CALL_FUNCTION_1   None
350	STORE_FAST        'roomId'

353	LOAD_FAST         'actionRoomIds'
356	LOAD_ATTR         'remove'
359	LOAD_FAST         'roomId'
362	CALL_FUNCTION_1   None
365	POP_TOP           None

366	LOAD_FAST         'middleRoomIds'
369	LOAD_ATTR         'append'
372	LOAD_FAST         'roomId'
375	CALL_FUNCTION_1   None
378	POP_TOP           None
379	JUMP_BACK         '332'
382	POP_BLOCK         None
383_0	COME_FROM         '319'
383	JUMP_FORWARD      '386'
386_0	COME_FROM         '383'

386	BUILD_LIST_0      None
389	STORE_FAST        'roomIds'

392	LOAD_FAST         'roomIds'
395	LOAD_ATTR         'append'
398	LOAD_FAST         'rng'
401	LOAD_ATTR         'choice'
404	LOAD_FAST         'startingRoomIDs'
407	CALL_FUNCTION_1   None
410	CALL_FUNCTION_1   None
413	POP_TOP           None

414	LOAD_FAST         'rng'
417	LOAD_ATTR         'shuffle'
420	LOAD_FAST         'middleRoomIds'
423	CALL_FUNCTION_1   None
426	POP_TOP           None

427	LOAD_FAST         'roomIds'
430	LOAD_ATTR         'extend'
433	LOAD_FAST         'middleRoomIds'
436	CALL_FUNCTION_1   None
439	POP_TOP           None

440	LOAD_FAST         'roomIds'
443	LOAD_ATTR         'append'
446	LOAD_FAST         'finalRoomId'
449	CALL_FUNCTION_1   None
452	POP_TOP           None

453	LOAD_FAST         'roomIds'
456	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 267

