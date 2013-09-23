from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from BattleBase import *
from BattleProps import *
from BattleSounds import *
from toontown.toon.ToonDNA import *
from toontown.suit.SuitDNA import *
from direct.directnotify import DirectNotifyGlobal
import random
import MovieCamera
import MovieUtil
from MovieUtil import calcAvgSuitPos
notify = DirectNotifyGlobal.directNotify.newCategory('MovieThrow')
hitSoundFiles = ('AA_tart_only.mp3', 'AA_slice_only.mp3', 'AA_slice_only.mp3', 'AA_slice_only.mp3', 'AA_slice_only.mp3', 'AA_wholepie_only.mp3', 'AA_wholepie_only.mp3')
tPieLeavesHand = 2.7
tPieHitsSuit = 3.0
tSuitDodges = 2.45
ratioMissToHit = 1.5
tPieShrink = 0.7
pieFlyTaskName = 'MovieThrow-pieFly'

def addHit(dict, suitId, hitCount):
    if dict.has_key(suitId):
        dict[suitId] += hitCount
    else:
        dict[suitId] = hitCount


def doFires--- This code section failed: ---

0	LOAD_GLOBAL       'len'
3	LOAD_FAST         'fires'
6	CALL_FUNCTION_1   None
9	LOAD_CONST        0
12	COMPARE_OP        '=='
15	JUMP_IF_FALSE     '25'

18	LOAD_CONST        (None, None)
21	RETURN_VALUE      None
22	JUMP_FORWARD      '25'
25_0	COME_FROM         '22'

25	BUILD_MAP         None
28	STORE_FAST        'suitFiresDict'

31	SETUP_LOOP        '113'
34	LOAD_FAST         'fires'
37	GET_ITER          None
38	FOR_ITER          '112'
41	STORE_FAST        'fire'

44	LOAD_FAST         'fire'
47	LOAD_CONST        'target'
50	BINARY_SUBSCR     None
51	LOAD_CONST        'suit'
54	BINARY_SUBSCR     None
55	LOAD_ATTR         'doId'
58	STORE_FAST        'suitId'

61	LOAD_FAST         'suitFiresDict'
64	LOAD_ATTR         'has_key'
67	LOAD_FAST         'suitId'
70	CALL_FUNCTION_1   None
73	JUMP_IF_FALSE     '96'

76	LOAD_FAST         'suitFiresDict'
79	LOAD_FAST         'suitId'
82	BINARY_SUBSCR     None
83	LOAD_ATTR         'append'
86	LOAD_FAST         'fire'
89	CALL_FUNCTION_1   None
92	POP_TOP           None
93	JUMP_BACK         '38'

96	LOAD_FAST         'fire'
99	BUILD_LIST_1      None
102	LOAD_FAST         'suitFiresDict'
105	LOAD_FAST         'suitId'
108	STORE_SUBSCR      None
109	JUMP_BACK         '38'
112	POP_BLOCK         None
113_0	COME_FROM         '31'

113	LOAD_FAST         'suitFiresDict'
116	LOAD_ATTR         'values'
119	CALL_FUNCTION_0   None
122	STORE_FAST        'suitFires'

125	LOAD_CONST        '<code_object compFunc>'
128	MAKE_FUNCTION_0   None
131	STORE_FAST        'compFunc'

134	LOAD_FAST         'suitFires'
137	LOAD_ATTR         'sort'
140	LOAD_FAST         'compFunc'
143	CALL_FUNCTION_1   None
146	POP_TOP           None

147	BUILD_MAP         None
150	STORE_FAST        'totalHitDict'

153	BUILD_MAP         None
156	STORE_FAST        'singleHitDict'

159	BUILD_MAP         None
162	STORE_FAST        'groupHitDict'

165	SETUP_LOOP        '289'
168	LOAD_FAST         'fires'
171	GET_ITER          None
172	FOR_ITER          '288'
175	STORE_FAST        'fire'

178	LOAD_FAST         'fire'
181	LOAD_CONST        'target'
184	BINARY_SUBSCR     None
185	LOAD_CONST        'suit'
188	BINARY_SUBSCR     None
189	LOAD_ATTR         'doId'
192	STORE_FAST        'suitId'

195	LOAD_FAST         'fire'
198	LOAD_CONST        'target'
201	BINARY_SUBSCR     None
202	LOAD_CONST        'hp'
205	BINARY_SUBSCR     None
206	LOAD_CONST        0
209	COMPARE_OP        '>'
212	JUMP_IF_FALSE     '250'

215	LOAD_GLOBAL       'addHit'
218	LOAD_FAST         'singleHitDict'
221	LOAD_FAST         'suitId'
224	LOAD_CONST        1
227	CALL_FUNCTION_3   None
230	POP_TOP           None

231	LOAD_GLOBAL       'addHit'
234	LOAD_FAST         'totalHitDict'
237	LOAD_FAST         'suitId'
240	LOAD_CONST        1
243	CALL_FUNCTION_3   None
246	POP_TOP           None
247	JUMP_ABSOLUTE     '285'

250	LOAD_GLOBAL       'addHit'
253	LOAD_FAST         'singleHitDict'
256	LOAD_FAST         'suitId'
259	LOAD_CONST        0
262	CALL_FUNCTION_3   None
265	POP_TOP           None

266	LOAD_GLOBAL       'addHit'
269	LOAD_FAST         'totalHitDict'
272	LOAD_FAST         'suitId'
275	LOAD_CONST        0
278	CALL_FUNCTION_3   None
281	POP_TOP           None
282	JUMP_BACK         '172'
285	JUMP_BACK         '172'
288	POP_BLOCK         None
289_0	COME_FROM         '165'

289	LOAD_GLOBAL       'notify'
292	LOAD_ATTR         'debug'
295	LOAD_CONST        'singleHitDict = %s'
298	LOAD_FAST         'singleHitDict'
301	BINARY_MODULO     None
302	CALL_FUNCTION_1   None
305	POP_TOP           None

306	LOAD_GLOBAL       'notify'
309	LOAD_ATTR         'debug'
312	LOAD_CONST        'groupHitDict = %s'
315	LOAD_FAST         'groupHitDict'
318	BINARY_MODULO     None
319	CALL_FUNCTION_1   None
322	POP_TOP           None

323	LOAD_GLOBAL       'notify'
326	LOAD_ATTR         'debug'
329	LOAD_CONST        'totalHitDict = %s'
332	LOAD_FAST         'totalHitDict'
335	BINARY_MODULO     None
336	CALL_FUNCTION_1   None
339	POP_TOP           None

340	LOAD_CONST        0.0
343	STORE_FAST        'delay'

346	LOAD_GLOBAL       'Parallel'
349	CALL_FUNCTION_0   None
352	STORE_FAST        'mtrack'

355	BUILD_LIST_0      None
358	STORE_FAST        'firedTargets'

361	SETUP_LOOP        '458'
364	LOAD_FAST         'suitFires'
367	GET_ITER          None
368	FOR_ITER          '457'
371	STORE_FAST        'sf'

374	LOAD_GLOBAL       'len'
377	LOAD_FAST         'sf'
380	CALL_FUNCTION_1   None
383	LOAD_CONST        0
386	COMPARE_OP        '>'
389	JUMP_IF_FALSE     '454'

392	LOAD_GLOBAL       '__doSuitFires'
395	LOAD_FAST         'sf'
398	CALL_FUNCTION_1   None
401	STORE_FAST        'ival'

404	LOAD_FAST         'ival'
407	JUMP_IF_FALSE     '441'

410	LOAD_FAST         'mtrack'
413	LOAD_ATTR         'append'
416	LOAD_GLOBAL       'Sequence'
419	LOAD_GLOBAL       'Wait'
422	LOAD_FAST         'delay'
425	CALL_FUNCTION_1   None
428	LOAD_FAST         'ival'
431	CALL_FUNCTION_2   None
434	CALL_FUNCTION_1   None
437	POP_TOP           None
438	JUMP_FORWARD      '441'
441_0	COME_FROM         '438'

441	LOAD_FAST         'delay'
444	LOAD_GLOBAL       'TOON_FIRE_SUIT_DELAY'
447	BINARY_ADD        None
448	STORE_FAST        'delay'
451	JUMP_BACK         '368'
454	JUMP_BACK         '368'
457	POP_BLOCK         None
458_0	COME_FROM         '361'

458	LOAD_GLOBAL       'Sequence'
461	CALL_FUNCTION_0   None
464	STORE_FAST        'retTrack'

467	LOAD_FAST         'retTrack'
470	LOAD_ATTR         'append'
473	LOAD_FAST         'mtrack'
476	CALL_FUNCTION_1   None
479	POP_TOP           None

480	LOAD_FAST         'retTrack'
483	LOAD_ATTR         'getDuration'
486	CALL_FUNCTION_0   None
489	STORE_FAST        'camDuration'

492	LOAD_GLOBAL       'MovieCamera'
495	LOAD_ATTR         'chooseFireShot'
498	LOAD_FAST         'fires'
501	LOAD_FAST         'suitFiresDict'

504	LOAD_FAST         'camDuration'
507	CALL_FUNCTION_3   None
510	STORE_FAST        'camTrack'

513	LOAD_FAST         'retTrack'
516	LOAD_FAST         'camTrack'
519	BUILD_TUPLE_2     None
522	RETURN_VALUE      None

Syntax error at or near `LOAD_GLOBAL' token at offset 250


def __doSuitFires(fires):
    toonTracks = Parallel()
    delay = 0.0
    hitCount = 0
    for fire in fires:
        if fire['target']['hp'] > 0:
            hitCount += 1
        else:
            break

    suitList = []
    for fire in fires:
        if fire['target']['suit'] not in suitList:
            suitList.append(fire['target']['suit'])

    for fire in fires:
        showSuitCannon = 1
        if fire['target']['suit'] not in suitList:
            showSuitCannon = 0
        else:
            suitList.remove(fire['target']['suit'])
        tracks = __throwPie(fire, delay, hitCount, showSuitCannon)
        if tracks:
            for track in tracks:
                toonTracks.append(track)

        delay = delay + TOON_THROW_DELAY

    return toonTracks


def __showProp(prop, parent, pos):
    prop.reparentTo(parent)
    prop.setPos(pos)


def __animProp(props, propName, propType):
    if 'actor' == propType:
        for prop in props:
            prop.play(propName)

    elif 'model' == propType:
        pass
    else:
        notify.error('No such propType as: %s' % propType)


def __billboardProp(prop):
    scale = prop.getScale()
    prop.setBillboardPointWorld()
    prop.setScale(scale)


def __suitMissPoint(suit, other = render):
    pnt = suit.getPos(other)
    pnt.setZ(pnt[2] + suit.getHeight() * 1.3)
    return pnt


def __propPreflight(props, suit, toon, battle):
    prop = props[0]
    toon.update(0)
    prop.wrtReparentTo(battle)
    props[1].reparentTo(hidden)
    for ci in range(prop.getNumChildren()):
        prop.getChild(ci).setHpr(0, -90, 0)

    targetPnt = MovieUtil.avatarFacePoint(suit, other=battle)
    prop.lookAt(targetPnt)


def __propPreflightGroup(props, suits, toon, battle):
    prop = props[0]
    toon.update(0)
    prop.wrtReparentTo(battle)
    props[1].reparentTo(hidden)
    for ci in range(prop.getNumChildren()):
        prop.getChild(ci).setHpr(0, -90, 0)

    avgTargetPt = Point3(0, 0, 0)
    for suit in suits:
        avgTargetPt += MovieUtil.avatarFacePoint(suit, other=battle)

    avgTargetPt /= len(suits)
    prop.lookAt(avgTargetPt)


def __piePreMiss(missDict, pie, suitPoint, other = render):
    missDict['pie'] = pie
    missDict['startScale'] = pie.getScale()
    missDict['startPos'] = pie.getPos(other)
    v = Vec3(suitPoint - missDict['startPos'])
    endPos = missDict['startPos'] + v * ratioMissToHit
    missDict['endPos'] = endPos


def __pieMissLerpCallback(t, missDict):
    pie = missDict['pie']
    newPos = missDict['startPos'] * (1.0 - t) + missDict['endPos'] * t
    if t < tPieShrink:
        tScale = 0.0001
    else:
        tScale = (t - tPieShrink) / (1.0 - tPieShrink)
    newScale = missDict['startScale'] * max(1.0 - tScale, 0.01)
    pie.setPos(newPos)
    pie.setScale(newScale)


def __piePreMissGroup(missDict, pies, suitPoint, other = render):
    missDict['pies'] = pies
    missDict['startScale'] = pies[0].getScale()
    missDict['startPos'] = pies[0].getPos(other)
    v = Vec3(suitPoint - missDict['startPos'])
    endPos = missDict['startPos'] + v * ratioMissToHit
    missDict['endPos'] = endPos
    notify.debug('startPos=%s' % missDict['startPos'])
    notify.debug('v=%s' % v)
    notify.debug('endPos=%s' % missDict['endPos'])


def __pieMissGroupLerpCallback(t, missDict):
    pies = missDict['pies']
    newPos = missDict['startPos'] * (1.0 - t) + missDict['endPos'] * t
    if t < tPieShrink:
        tScale = 0.0001
    else:
        tScale = (t - tPieShrink) / (1.0 - tPieShrink)
    newScale = missDict['startScale'] * max(1.0 - tScale, 0.01)
    for pie in pies:
        pie.setPos(newPos)
        pie.setScale(newScale)


def __getSoundTrack(level, hitSuit, node = None):
    throwSound = globalBattleSoundCache.getSound('AA_drop_trigger_box.mp3')
    throwTrack = Sequence(Wait(2.15), SoundInterval(throwSound, node=node))
    return throwTrack


def __throwPie(throw, delay, hitCount, showCannon = 1):
    toon = throw['toon']
    hpbonus = throw['hpbonus']
    target = throw['target']
    suit = target['suit']
    hp = target['hp']
    kbbonus = target['kbbonus']
    sidestep = throw['sidestep']
    died = target['died']
    revived = target['revived']
    leftSuits = target['leftSuits']
    rightSuits = target['rightSuits']
    level = throw['level']
    battle = throw['battle']
    suitPos = suit.getPos(battle)
    origHpr = toon.getHpr(battle)
    notify.debug('toon: %s throws tart at suit: %d for hp: %d died: %d' % (toon.getName(),
     suit.doId,
     hp,
     died))
    pieName = pieNames[0]
    hitSuit = hp > 0
    button = globalPropPool.getProp('button')
    buttonType = globalPropPool.getPropType('button')
    button2 = MovieUtil.copyProp(button)
    buttons = [button, button2]
    hands = toon.getLeftHands()
    toonTrack = Sequence()
    toonFace = Func(toon.headsUp, battle, suitPos)
    toonTrack.append(Wait(delay))
    toonTrack.append(toonFace)
    toonTrack.append(ActorInterval(toon, 'pushbutton'))
    toonTrack.append(ActorInterval(toon, 'wave', duration=2.0))
    toonTrack.append(ActorInterval(toon, 'duck'))
    toonTrack.append(Func(toon.loop, 'neutral'))
    toonTrack.append(Func(toon.setHpr, battle, origHpr))
    buttonTrack = Sequence()
    buttonShow = Func(MovieUtil.showProps, buttons, hands)
    buttonScaleUp = LerpScaleInterval(button, 1.0, button.getScale(), startScale=Point3(0.01, 0.01, 0.01))
    buttonScaleDown = LerpScaleInterval(button, 1.0, Point3(0.01, 0.01, 0.01), startScale=button.getScale())
    buttonHide = Func(MovieUtil.removeProps, buttons)
    buttonTrack.append(Wait(delay))
    buttonTrack.append(buttonShow)
    buttonTrack.append(buttonScaleUp)
    buttonTrack.append(Wait(2.5))
    buttonTrack.append(buttonScaleDown)
    buttonTrack.append(buttonHide)
    soundTrack = __getSoundTrack(level, hitSuit, toon)
    suitResponseTrack = Sequence()
    reactIval = Sequence()
    if showCannon:
        showDamage = Func(suit.showHpText, -hp, openEnded=0)
        updateHealthBar = Func(suit.updateHealthBar, hp)
        cannon = loader.loadModel('phase_4/models/minigames/toon_cannon')
        barrel = cannon.find('**/cannon')
        barrel.setHpr(0, 90, 0)
        cannonHolder = render.attachNewNode('CannonHolder')
        cannon.reparentTo(cannonHolder)
        cannon.setPos(0, 0, -8.6)
        cannonHolder.setPos(suit.getPos(render))
        cannonHolder.setHpr(suit.getHpr(render))
        cannonAttachPoint = barrel.attachNewNode('CannonAttach')
        kapowAttachPoint = barrel.attachNewNode('kapowAttach')
        scaleFactor = 1.6
        iScale = 1 / scaleFactor
        barrel.setScale(scaleFactor, 1, scaleFactor)
        cannonAttachPoint.setScale(iScale, 1, iScale)
        cannonAttachPoint.setPos(0, 6.7, 0)
        kapowAttachPoint.setPos(0, -0.5, 1.9)
        suit.reparentTo(cannonAttachPoint)
        suit.setPos(0, 0, 0)
        suit.setHpr(0, -90, 0)
        suitLevel = suit.getActualLevel()
        deep = 2.5 + suitLevel * 0.2
        suitScale = 0.9
        import math
        suitScale = 0.9 - math.sqrt(suitLevel) * 0.1
        sival = []
        posInit = cannonHolder.getPos()
        posFinal = Point3(posInit[0] + 0.0, posInit[1] + 0.0, posInit[2] + 7.0)
        kapow = globalPropPool.getProp('kapow')
        kapow.reparentTo(kapowAttachPoint)
        kapow.hide()
        kapow.setScale(0.25)
        kapow.setBillboardPointEye()
        smoke = loader.loadModel('phase_4/models/props/test_clouds')
        smoke.reparentTo(cannonAttachPoint)
        smoke.setScale(0.5)
        smoke.hide()
        smoke.setBillboardPointEye()
        soundBomb = base.loadSfx('phase_4/audio/sfx/MG_cannon_fire_alt.mp3')
        playSoundBomb = SoundInterval(soundBomb, node=cannonHolder)
        soundFly = base.loadSfx('phase_4/audio/sfx/firework_whistle_01.mp3')
        playSoundFly = SoundInterval(soundFly, node=cannonHolder)
        soundCannonAdjust = base.loadSfx('phase_4/audio/sfx/MG_cannon_adjust.mp3')
        playSoundCannonAdjust = SoundInterval(soundCannonAdjust, duration=0.6, node=cannonHolder)
        soundCogPanic = base.loadSfx('phase_5/audio/sfx/ENC_cogafssm.mp3')
        playSoundCogPanic = SoundInterval(soundCogPanic, node=cannonHolder)
        reactIval = Parallel(ActorInterval(suit, 'pie-small-react'), Sequence(Wait(0.0), LerpPosInterval(cannonHolder, 2.0, posFinal, startPos=posInit, blendType='easeInOut'), Parallel(LerpHprInterval(barrel, 0.6, Point3(0, 45, 0), startHpr=Point3(0, 90, 0), blendType='easeIn'), playSoundCannonAdjust), Wait(2.0), Parallel(LerpHprInterval(barrel, 0.6, Point3(0, 90, 0), startHpr=Point3(0, 45, 0), blendType='easeIn'), playSoundCannonAdjust), LerpPosInterval(cannonHolder, 1.0, posInit, startPos=posFinal, blendType='easeInOut')), Sequence(Wait(0.0), Parallel(ActorInterval(suit, 'flail'), suit.scaleInterval(1.0, suitScale), LerpPosInterval(suit, 0.25, Point3(0, -1.0, 0.0)), Sequence(Wait(0.25), Parallel(playSoundCogPanic, LerpPosInterval(suit, 1.5, Point3(0, -deep, 0.0), blendType='easeIn')))), Wait(2.5), Parallel(playSoundBomb, playSoundFly, Sequence(Func(smoke.show), Parallel(LerpScaleInterval(smoke, 0.5, 3), LerpColorScaleInterval(smoke, 0.5, Vec4(2, 2, 2, 0))), Func(smoke.hide)), Sequence(Func(kapow.show), ActorInterval(kapow, 'kapow'), Func(kapow.hide)), LerpPosInterval(suit, 3.0, Point3(0, 1
# Can't uncompyle C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\battle\MovieFire.pyc
Traceback (most recent call last):
  File "C:\python27\lib\uncompyle2\__init__.py", line 206, in main
    uncompyle_file(infile, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 143, in uncompyle_file
    uncompyle(version, co, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 132, in uncompyle
    raise walk.ERROR
ParserError: --- This code section failed: ---

0	LOAD_GLOBAL       'len'
3	LOAD_FAST         'fires'
6	CALL_FUNCTION_1   None
9	LOAD_CONST        0
12	COMPARE_OP        '=='
15	JUMP_IF_FALSE     '25'

18	LOAD_CONST        (None, None)
21	RETURN_VALUE      None
22	JUMP_FORWARD      '25'
25_0	COME_FROM         '22'

25	BUILD_MAP         None
28	STORE_FAST        'suitFiresDict'

31	SETUP_LOOP        '113'
34	LOAD_FAST         'fires'
37	GET_ITER          None
38	FOR_ITER          '112'
41	STORE_FAST        'fire'

44	LOAD_FAST         'fire'
47	LOAD_CONST        'target'
50	BINARY_SUBSCR     None
51	LOAD_CONST        'suit'
54	BINARY_SUBSCR     None
55	LOAD_ATTR         'doId'
58	STORE_FAST        'suitId'

61	LOAD_FAST         'suitFiresDict'
64	LOAD_ATTR         'has_key'
67	LOAD_FAST         'suitId'
70	CALL_FUNCTION_1   None
73	JUMP_IF_FALSE     '96'

76	LOAD_FAST         'suitFiresDict'
79	LOAD_FAST         'suitId'
82	BINARY_SUBSCR     None
83	LOAD_ATTR         'append'
86	LOAD_FAST         'fire'
89	CALL_FUNCTION_1   None
92	POP_TOP           None
93	JUMP_BACK         '38'

96	LOAD_FAST         'fire'
99	BUILD_LIST_1      None
102	LOAD_FAST         'suitFiresDict'
105	LOAD_FAST         'suitId'
108	STORE_SUBSCR      None
109	JUMP_BACK         '38'
112	POP_BLOCK         None
113_0	COME_FROM         '31'

113	LOAD_FAST         'suitFiresDict'
116	LOAD_ATTR         'values'
119	CALL_FUNCTION_0   None
122	STORE_FAST        'suitFires'

125	LOAD_CONST        '<code_object compFunc>'
128	MAKE_FUNCTION_0   None
131	STORE_FAST        'compFunc'

134	LOAD_FAST         'suitFires'
137	LOAD_ATTR         'sort'
140	LOAD_FAST         'compFunc'
143	CALL_FUNCTION_1   None
146	POP_TOP           None

147	BUILD_MAP         None
150	STORE_FAST        'totalHitDict'

153	BUILD_MAP         None
156	STORE_FAST        'singleHitDict'

159	BUILD_MAP         None
162	STORE_FAST        'groupHitDict'

165	SETUP_LOOP        '289'
168	LOAD_FAST         'fires'
171	GET_ITER          None
172	FOR_ITER          '288'
175	STORE_FAST        'fire'

178	LOAD_FAST         'fire'
181	LOAD_CONST        'target'
184	BINARY_SUBSCR     None
185	LOAD_CONST        'suit'
188	BINARY_SUBSCR     None
189	LOAD_ATTR         'doId'
192	STORE_FAST        'suitId'

195	LOAD_FAST         'fire'
198	LOAD_CONST        'target'
201	BINARY_SUBSCR     None
202	LOAD_CONST        'hp'
205	BINARY_SUBSCR     None
206	LOAD_CONST        0
209	COMPARE_OP        '>'
212	JUMP_IF_FALSE     '250'

215	LOAD_GLOBAL       'addHit'
218	LOAD_FAST         'singleHitDict'
221	LOAD_FAST         'suitId'
224	LOAD_CONST        1
227	CALL_FUNCTION_3   None
230	POP_TOP           None

231	LOAD_GLOBAL       'addHit'
234	LOAD_FAST         'totalHitDict'
237	LOAD_FAST         'suitId'
240	LOAD_CONST        1
243	CALL_FUNCTION_3   None
246	POP_TOP           None
247	JUMP_ABSOLUTE     '285'

250	LOAD_GLOBAL       'addHit'
253	LOAD_FAST         'singleHitDict'
256	LOAD_FAST         'suitId'
259	LOAD_CONST        0
262	CALL_FUNCTION_3   None
265	POP_TOP           None

266	LOAD_GLOBAL       'addHit'
269	LOAD_FAST         'totalHitDict'
272	LOAD_FAST         'suitId'
275	LOAD_CONST        0
278	CALL_FUNCTION_3   None
281	POP_TOP           None
282	JUMP_BACK         '172'
285	JUMP_BACK         '172'
288	POP_BLOCK         None
289_0	COME_FROM         '165'

289	LOAD_GLOBAL       'notify'
292	LOAD_ATTR         'debug'
295	LOAD_CONST        'singleHitDict = %s'
298	LOAD_FAST         'singleHitDict'
301	BINARY_MODULO     None
302	CALL_FUNCTION_1   None
305	POP_TOP           None

306	LOAD_GLOBAL       'notify'50.0, 0.0)), suit.scaleInterval(3.0, 0.01)), Func(suit.hide)))
        if hitCount == 1:
            sival = Sequence(Parallel(reactIval, MovieUtil.createSuitStunInterval(suit, 0.3, 1.3)), Wait(0.0), Func(cannonHolder.remove))
        else:
            sival = reactIval
        suitResponseTrack.append(Wait(delay + tPieHitsSuit))
        suitResponseTrack.append(showDamage)
        suitResponseTrack.append(updateHealthBar)
        suitResponseTrack.append(sival)
        bonusTrack = Sequence(Wait(delay + tPieHitsSuit))
        if kbbonus > 0:
            bonusTrack.append(Wait(0.75))
            bonusTrack.append(Func(suit.showHpText, -kbbonus, 2, openEnded=0))
        if hpbonus > 0:
            bonusTrack.append(Wait(0.75))
            bonusTrack.append(Func(suit.showHpText, -hpbonus, 1, openEnded=0))
        suitResponseTrack = Parallel(suitResponseTrack, bonusTrack)
    return [toonTrack,
     soundTrack,
     buttonTrack,
     suitResponseTrack]

309	LOAD_ATTR         'debug'
312	LOAD_CONST        'groupHitDict = %s'
315	LOAD_FAST         'groupHitDict'
318	BINARY_MODULO     None
319	CALL_FUNCTION_1   None
322	POP_TOP           None

323	LOAD_GLOBAL       'notify'
326	LOAD_ATTR         'debug'
329	LOAD_CONST        'totalHitDict = %s'
332	LOAD_FAST         'totalHitDict'
335	BINARY_MODULO     None
336	CALL_FUNCTION_1   None
339	POP_TOP           None

340	LOAD_CONST        0.0
343	STORE_FAST        'delay'

346	LOAD_GLOBAL       'Parallel'
349	CALL_FUNCTION_0   None
352	STORE_FAST        'mtrack'

355	BUILD_LIST_0      None
358	STORE_FAST        'firedTargets'

361	SETUP_LOOP        '458'
364	LOAD_FAST         'suitFires'
367	GET_ITER          None
368	FOR_ITER          '457'
371	STORE_FAST        'sf'

374	LOAD_GLOBAL       'len'
377	LOAD_FAST         'sf'
380	CALL_FUNCTION_1   None
383	LOAD_CONST        0
386	COMPARE_OP        '>'
389	JUMP_IF_FALSE     '454'

392	LOAD_GLOBAL       '__doSuitFires'
395	LOAD_FAST         'sf'
398	CALL_FUNCTION_1   None
401	STORE_FAST        'ival'

404	LOAD_FAST         'ival'
407	JUMP_IF_FALSE     '441'

410	LOAD_FAST         'mtrack'
413	LOAD_ATTR         'append'
416	LOAD_GLOBAL       'Sequence'
419	LOAD_GLOBAL       'Wait'
422	LOAD_FAST         'delay'
425	CALL_FUNCTION_1   None
428	LOAD_FAST         'ival'
431	CALL_FUNCTION_2   None
434	CALL_FUNCTION_1   None
437	POP_TOP           None
438	JUMP_FORWARD      '441'
441_0	COME_FROM         '438'

441	LOAD_FAST         'delay'
444	LOAD_GLOBAL       'TOON_FIRE_SUIT_DELAY'
447	BINARY_ADD        None
448	STORE_FAST        'delay'
451	JUMP_BACK         '368'
454	JUMP_BACK         '368'
457	POP_BLOCK         None
458_0	COME_FROM         '361'

458	LOAD_GLOBAL       'Sequence'
461	CALL_FUNCTION_0   None
464	STORE_FAST        'retTrack'

467	LOAD_FAST         'retTrack'
470	LOAD_ATTR         'append'
473	LOAD_FAST         'mtrack'
476	CALL_FUNCTION_1   None
479	POP_TOP           None

480	LOAD_FAST         'retTrack'
483	LOAD_ATTR         'getDuration'
486	CALL_FUNCTION_0   None
489	STORE_FAST        'camDuration'

492	LOAD_GLOBAL       'MovieCamera'
495	LOAD_ATTR         'chooseFireShot'
498	LOAD_FAST         'fires'
501	LOAD_FAST         'suitFiresDict'

504	LOAD_FAST         'camDuration'
507	CALL_FUNCTION_3   None
510	STORE_FAST        'camTrack'

513	LOAD_FAST         'retTrack'
516	LOAD_FAST         'camTrack'
519	BUILD_TUPLE_2     None
522	RETURN_VALUE      None

Syntax error at or near `LOAD_GLOBAL' token at offset 250

