from direct.directnotify import DirectNotifyGlobal
from direct.showbase.PythonUtil import invertDictLossless
from toontown.coghq import CountryClubRoomSpecs
from toontown.toonbase import ToontownGlobals
from direct.showbase.PythonUtil import normalDistrib, lerp
import random

def printAllBossbotInfo():
    print 'roomId: roomName'
    for roomId, roomName in CountryClubRoomSpecs.BossbotCountryClubRoomId2RoomName.items():
        print '%s: %s' % (roomId, roomName)

    print '\nroomId: numBattles'
    for roomId, numBattles in CountryClubRoomSpecs.roomId2numBattles.items():
        print '%s: %s' % (roomId, numBattles)

    print '\ncountryClubId floor roomIds'
    printCountryClubRoomIds()
    print '\ncountryClubId floor numRooms'
    printNumRooms()
    print '\ncountryClubId floor numForcedBattles'
    printNumBattles()


def iterateBossbotCountryClubs(func):
    from toontown.toonbase import ToontownGlobals
    for countryClubId in [ToontownGlobals.BossbotCountryClubIntA, ToontownGlobals.BossbotCountryClubIntB, ToontownGlobals.BossbotCountryClubIntC]:
        for floorNum in xrange(ToontownGlobals.CountryClubNumFloors[countryClubId]):
            func(CountryClubLayout(countryClubId, floorNum))


def printCountryClubInfo():

    def func(ml):
        print ml

    iterateBossbotCountryClubs(func)


def printCountryClubRoomIds():

    def func(ml):
        print ml.getCountryClubId(), ml.getFloorNum(), ml.getRoomIds()

    iterateBossbotCountryClubs(func)


def printCountryClubRoomNames():

    def func(ml):
        print ml.getCountryClubId(), ml.getFloorNum(), ml.getRoomNames()

    iterateBossbotCountryClubs(func)


def printNumRooms():

    def func(ml):
        print ml.getCountryClubId(), ml.getFloorNum(), ml.getNumRooms()

    iterateBossbotCountryClubs(func)


def printNumBattles():

    def func(ml):
        print ml.getCountryClubId(), ml.getFloorNum(), ml.getNumBattles()

    iterateBossbotCountryClubs(func)


ClubLayout3_0 = [(0, 2, 5, 9, 17), (0, 2, 4, 9, 17), (0, 2, 5, 9, 18)]
ClubLayout3_1 = [(0, 2, 5, 9, 17), (0, 2, 4, 9, 17), (0, 2, 5, 9, 18)]
ClubLayout3_2 = [(0, 2, 4, 9, 17), (0, 2, 4, 9, 17), (0, 2, 6, 9, 18)]
ClubLayout6_0 = [(0, 22, 4, 29, 17),
 (0, 22, 5, 29, 17),
 (0, 22, 6, 29, 17),
 (0, 22, 5, 29, 17),
 (0, 22, 6, 29, 17),
 (0, 22, 5, 29, 18)]
ClubLayout6_1 = [(0, 22, 4, 29, 17),
 (0, 22, 6, 29, 17),
 (0, 22, 4, 29, 17),
 (0, 22, 6, 29, 17),
 (0, 22, 4, 29, 17),
 (0, 22, 6, 29, 18)]
ClubLayout6_2 = [(0, 22, 4, 29, 17),
 (0, 22, 6, 29, 17),
 (0, 22, 5, 29, 17),
 (0, 22, 6, 29, 17),
 (0, 22, 5, 29, 17),
 (0, 22, 7, 29, 18)]
ClubLayout9_0 = [(0, 32, 4, 39, 17),
 (0, 32, 5, 39, 17),
 (0, 32, 6, 39, 17),
 (0, 32, 7, 39, 17),
 (0, 32, 5, 39, 17),
 (0, 32, 6, 39, 17),
 (0, 32, 7, 39, 17),
 (0, 32, 7, 39, 17),
 (0, 32, 6, 39, 18)]
ClubLayout9_1 = [(0, 32, 4, 39, 17),
 (0, 32, 5, 39, 17),
 (0, 32, 6, 39, 17),
 (0, 32, 7, 39, 17),
 (0, 32, 5, 39, 17),
 (0, 32, 6, 39, 17),
 (0, 32, 7, 39, 17),
 (0, 32, 7, 39, 17),
 (0, 32, 7, 39, 18)]
ClubLayout9_2 = [(0, 32, 5, 39, 17),
 (0, 32, 5, 39, 17),
 (0, 32, 6, 39, 17),
 (0, 32, 6, 39, 17),
 (0, 32, 5, 39, 17),
 (0, 32, 5, 39, 17),
 (0, 32, 6, 39, 17),
 (0, 32, 6, 39, 17),
 (0, 32, 7, 39, 18)]
countryClubLayouts = [ClubLayout3_0,
 ClubLayout3_1,
 ClubLayout3_2,
 ClubLayout6_0,
 ClubLayout6_1,
 ClubLayout6_2,
 ClubLayout9_0,
 ClubLayout9_1,
 ClubLayout9_2]
testLayout = [ClubLayout3_0,
 ClubLayout3_0,
 ClubLayout3_0,
 ClubLayout6_0,
 ClubLayout6_0,
 ClubLayout6_0,
 ClubLayout9_0,
 ClubLayout9_0,
 ClubLayout9_0]
countryClubLayouts = testLayout

class CountryClubLayout():
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('CountryClubLayout')

    def __init__(self, countryClubId, floorNum, layoutIndex):
        self.countryClubId = countryClubId
        self.floorNum = floorNum
        self.layoutIndex = layoutIndex
        self.roomIds = []
        self.hallways = []
        self.numRooms = 1 + ToontownGlobals.CountryClubNumRooms[self.countryClubId][0]
        self.numHallways = self.numRooms - 1 + 1
        self.roomIds = countryClubLayouts[layoutIndex][floorNum]
        hallwayRng = self.getRng()
        connectorRoomNames = CountryClubRoomSpecs.BossbotCountryClubConnectorRooms
        for i in xrange(self.numHallways):
            self.hallways.append(hallwayRng.choice(connectorRoomNames))

    def _genFloorLayout--- This code section failed: ---

0	LOAD_FAST         'self'
3	LOAD_ATTR         'getRng'
6	CALL_FUNCTION_0   None
9	STORE_FAST        'rng'

12	LOAD_GLOBAL       'CountryClubRoomSpecs'
15	LOAD_ATTR         'BossbotCountryClubEntranceIDs'
18	STORE_FAST        'startingRoomIDs'

21	LOAD_GLOBAL       'CountryClubRoomSpecs'
24	LOAD_ATTR         'BossbotCountryClubMiddleRoomIDs'
27	STORE_FAST        'middleRoomIDs'

30	LOAD_GLOBAL       'CountryClubRoomSpecs'
33	LOAD_ATTR         'BossbotCountryClubFinalRoomIDs'
36	STORE_FAST        'finalRoomIDs'

39	LOAD_GLOBAL       'ToontownGlobals'
42	LOAD_ATTR         'CountryClubNumBattles'
45	LOAD_FAST         'self'
48	LOAD_ATTR         'countryClubId'
51	BINARY_SUBSCR     None
52	STORE_FAST        'numBattlesLeft'

55	LOAD_FAST         'rng'
58	LOAD_ATTR         'choice'
61	LOAD_FAST         'finalRoomIDs'
64	CALL_FUNCTION_1   None
67	STORE_FAST        'finalRoomId'

70	LOAD_FAST         'numBattlesLeft'
73	LOAD_GLOBAL       'CountryClubRoomSpecs'
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
111	LOAD_GLOBAL       'CountryClubRoomSpecs'
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

248	LOAD_GLOBAL       'CountryClubLayout'
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

414	LOAD_FAST         'middleRoomIds'
417	LOAD_ATTR         'sort'
420	CALL_FUNCTION_0   None
423	POP_TOP           None

424	LOAD_CONST        'middleRoomIds=%s'
427	LOAD_FAST         'middleRoomIds'
430	BINARY_MODULO     None
431	PRINT_ITEM        None
432	PRINT_NEWLINE_CONT None

433	LOAD_FAST         'roomIds'
436	LOAD_ATTR         'extend'
439	LOAD_FAST         'middleRoomIds'
442	CALL_FUNCTION_1   None
445	POP_TOP           None

446	LOAD_FAST         'roomIds'
449	LOAD_ATTR         'append'
452	LOAD_FAST         'finalRoomId'
455	CALL_FUNCTION_1   None
458	POP_TOP           None

459	LOAD_FAST         'roomIds'
462	RETURN_VALUE      None

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
            names.append(CountryClubRoomSpecs.BossbotCountryClubRoomId2RoomName[roomId])

        return names

    def getNumHallways(self):
        return len(self.hallways)

    def getHallwayModel(self, n):
        return self.hallways[n]

    def getNumBattles(self):
        numBattles = 0
        for roomId in self.getRoomIds():
            numBattles += CountryClubRoomSpecs.roomId2numBattles[roomId]

        return numBattles

    def getCountryClubId(self):
        return self.countryClubId

    def getFloorNum(self):
        return self.floorNum

    def getRng(self):
        return random.Random(self.countryClubId * self.floorNum)

    def _chooseBattleRooms(self, numBattlesLeft, allBattleRoomIds, baseIndex = 0, chosenBattleRooms = None):
        if chosenBattleRooms is None:
            chosenBattleRooms = []
        while baseIndex < len(allBattleRoomIds):
            nextRoomId = allBattleRoomIds[baseIndex]
            baseIndex += 1
            newNumBattlesLeft = numBattlesLeft - CountryClubRoomSpecs.middleRoomId2numBattles[nextRoomId]
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
        return 'CountryClubLayout: id=%s, layoutIndex=%s, floor=%s, nu
# Can't uncompyle C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\coghq\CountryClubLayout.pyc
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

12	LOAD_GLOBAL       'CountryClubRoomSpecs'
15	LOAD_ATTR         'BossbotCountryClubEntranceIDs'
18	STORE_FAST        'startingRoomIDs'

21	LOAD_GLOBAL       'CountryClubRoomSpecs'
24	LOAD_ATTR         'BossbotCountryClubMiddleRoomIDs'
27	STORE_FAST        'middleRoomIDs'

30	LOAD_GLOBAL       'CountryClubRoomSpecs'
33	LOAD_ATTR         'BossbotCountryClubFinalRoomIDs'
36	STORE_FAST        'finalRoomIDs'

39	LOAD_GLOBAL       'ToontownGlobals'
42	LOAD_ATTR         'CountryClubNumBattles'
45	LOAD_FAST         'self'
48	LOAD_ATTR         'countryClubId'
51	BINARY_SUBSCR     None
52	STORE_FAST        'numBattlesLeft'

55	LOAD_FAST         'rng'
58	LOAD_ATTR         'choice'
61	LOAD_FAST         'finalRoomIDs'
64	CALL_FUNCTION_1   None
67	STORE_FAST        'finalRoomId'

70	LOAD_FAST         'numBattlesLeft'
73	LOAD_GLOBAL       'CountryClubRoomSpecs'
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
111	LOAD_GLOBAL       'CountryClubRoomSpecs'
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

248	LOAD_GLOBAL       'CountryClubLayout'
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

281	LOAD_FAST       mRooms=%s, numBattles=%s' % (self.countryClubId,
         self.layoutIndex,
         self.floorNum,
         self.getNumRooms(),
         self.getNumBattles())

    def __repr__(self):
        return str(self)# decompiled 0 files: 0 okay, 1 failed, 0 verify failed
  'middleRoomsLeft'
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

414	LOAD_FAST         'middleRoomIds'
417	LOAD_ATTR         'sort'
420	CALL_FUNCTION_0   None
423	POP_TOP           None

424	LOAD_CONST        'middleRoomIds=%s'
427	LOAD_FAST         'middleRoomIds'
430	BINARY_MODULO     None
431	PRINT_ITEM        None
432	PRINT_NEWLINE_CONT None

433	LOAD_FAST         'roomIds'
436	LOAD_ATTR         'extend'
439	LOAD_FAST         'middleRoomIds'
442	CALL_FUNCTION_1   None
445	POP_TOP           None

446	LOAD_FAST         'roomIds'
449	LOAD_ATTR         'append'
452	LOAD_FAST         'finalRoomId'
455	CALL_FUNCTION_1   None
458	POP_TOP           None

459	LOAD_FAST         'roomIds'
462	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 267

