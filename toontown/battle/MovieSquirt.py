from direct.interval.IntervalGlobal import *
from BattleBase import *
from BattleProps import *
from BattleSounds import *
from toontown.toon.ToonDNA import *
from toontown.suit.SuitDNA import *
import MovieUtil
import MovieCamera
from direct.directnotify import DirectNotifyGlobal
import BattleParticles
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import ToontownBattleGlobals
import random
notify = DirectNotifyGlobal.directNotify.newCategory('MovieSquirt')
hitSoundFiles = ('AA_squirt_flowersquirt.mp3', 'AA_squirt_glasswater.mp3', 'AA_squirt_neonwatergun.mp3', 'AA_squirt_seltzer.mp3', 'firehose_spray.mp3', 'AA_throw_stormcloud.mp3', 'AA_squirt_Geyser.mp3')
missSoundFiles = ('AA_squirt_flowersquirt_miss.mp3', 'AA_squirt_glasswater_miss.mp3', 'AA_squirt_neonwatergun_miss.mp3', 'AA_squirt_seltzer_miss.mp3', 'firehose_spray.mp3', 'AA_throw_stormcloud_miss.mp3', 'AA_squirt_Geyser.mp3')
sprayScales = [0.2,
 0.3,
 0.1,
 0.6,
 0.8,
 1.0,
 2.0]
WaterSprayColor = Point4(0.75, 0.75, 1.0, 0.8)

def doSquirts--- This code section failed: ---

0	LOAD_GLOBAL       'len'
3	LOAD_FAST         'squirts'
6	CALL_FUNCTION_1   None
9	LOAD_CONST        0
12	COMPARE_OP        '=='
15	JUMP_IF_FALSE     '25'

18	LOAD_CONST        (None, None)
21	RETURN_VALUE      None
22	JUMP_FORWARD      '25'
25_0	COME_FROM         '22'

25	BUILD_MAP         None
28	STORE_FAST        'suitSquirtsDict'

31	LOAD_CONST        0
34	STORE_FAST        'doneUber'

37	LOAD_CONST        0
40	STORE_FAST        'skip'

43	SETUP_LOOP        '249'
46	LOAD_FAST         'squirts'
49	GET_ITER          None
50	FOR_ITER          '248'
53	STORE_FAST        'squirt'

56	LOAD_CONST        0
59	STORE_FAST        'skip'

62	LOAD_FAST         'skip'
65	JUMP_IF_FALSE     '71'

68	JUMP_BACK         '50'

71	LOAD_GLOBAL       'type'
74	LOAD_FAST         'squirt'
77	LOAD_CONST        'target'
80	BINARY_SUBSCR     None
81	CALL_FUNCTION_1   None
84	LOAD_GLOBAL       'type'
87	BUILD_LIST_0      None
90	CALL_FUNCTION_1   None
93	COMPARE_OP        '=='
96	JUMP_IF_FALSE     '180'

99	LOAD_FAST         'squirt'
102	LOAD_CONST        'target'
105	BINARY_SUBSCR     None
106	LOAD_CONST        0
109	BINARY_SUBSCR     None
110	STORE_FAST        'target'

113	LOAD_FAST         'target'
116	LOAD_CONST        'suit'
119	BINARY_SUBSCR     None
120	LOAD_ATTR         'doId'
123	STORE_FAST        'suitId'

126	LOAD_FAST         'suitSquirtsDict'
129	LOAD_ATTR         'has_key'
132	LOAD_FAST         'suitId'
135	CALL_FUNCTION_1   None
138	JUMP_IF_FALSE     '161'

141	LOAD_FAST         'suitSquirtsDict'
144	LOAD_FAST         'suitId'
147	BINARY_SUBSCR     None
148	LOAD_ATTR         'append'
151	LOAD_FAST         'squirt'
154	CALL_FUNCTION_1   None
157	POP_TOP           None
158	JUMP_ABSOLUTE     '177'

161	LOAD_FAST         'squirt'
164	BUILD_LIST_1      None
167	LOAD_FAST         'suitSquirtsDict'
170	LOAD_FAST         'suitId'
173	STORE_SUBSCR      None
174	JUMP_ABSOLUTE     '245'
177	JUMP_BACK         '50'

180	LOAD_FAST         'squirt'
183	LOAD_CONST        'target'
186	BINARY_SUBSCR     None
187	LOAD_CONST        'suit'
190	BINARY_SUBSCR     None
191	LOAD_ATTR         'doId'
194	STORE_FAST        'suitId'

197	LOAD_FAST         'suitSquirtsDict'
200	LOAD_ATTR         'has_key'
203	LOAD_FAST         'suitId'
206	CALL_FUNCTION_1   None
209	JUMP_IF_FALSE     '232'

212	LOAD_FAST         'suitSquirtsDict'
215	LOAD_FAST         'suitId'
218	BINARY_SUBSCR     None
219	LOAD_ATTR         'append'
222	LOAD_FAST         'squirt'
225	CALL_FUNCTION_1   None
228	POP_TOP           None
229	JUMP_BACK         '50'

232	LOAD_FAST         'squirt'
235	BUILD_LIST_1      None
238	LOAD_FAST         'suitSquirtsDict'
241	LOAD_FAST         'suitId'
244	STORE_SUBSCR      None
245	JUMP_BACK         '50'
248	POP_BLOCK         None
249_0	COME_FROM         '43'

249	LOAD_FAST         'suitSquirtsDict'
252	LOAD_ATTR         'values'
255	CALL_FUNCTION_0   None
258	STORE_FAST        'suitSquirts'

261	LOAD_CONST        '<code_object compFunc>'
264	MAKE_FUNCTION_0   None
267	STORE_FAST        'compFunc'

270	LOAD_FAST         'suitSquirts'
273	LOAD_ATTR         'sort'
276	LOAD_FAST         'compFunc'
279	CALL_FUNCTION_1   None
282	POP_TOP           None

283	LOAD_CONST        0.0
286	STORE_FAST        'delay'

289	LOAD_GLOBAL       'Parallel'
292	CALL_FUNCTION_0   None
295	STORE_FAST        'mtrack'

298	SETUP_LOOP        '395'
301	LOAD_FAST         'suitSquirts'
304	GET_ITER          None
305	FOR_ITER          '394'
308	STORE_FAST        'st'

311	LOAD_GLOBAL       'len'
314	LOAD_FAST         'st'
317	CALL_FUNCTION_1   None
320	LOAD_CONST        0
323	COMPARE_OP        '>'
326	JUMP_IF_FALSE     '391'

329	LOAD_GLOBAL       '__doSuitSquirts'
332	LOAD_FAST         'st'
335	CALL_FUNCTION_1   None
338	STORE_FAST        'ival'

341	LOAD_FAST         'ival'
344	JUMP_IF_FALSE     '378'

347	LOAD_FAST         'mtrack'
350	LOAD_ATTR         'append'
353	LOAD_GLOBAL       'Sequence'
356	LOAD_GLOBAL       'Wait'
359	LOAD_FAST         'delay'
362	CALL_FUNCTION_1   None
365	LOAD_FAST         'ival'
368	CALL_FUNCTION_2   None
371	CALL_FUNCTION_1   None
374	POP_TOP           None
375	JUMP_FORWARD      '378'
378_0	COME_FROM         '375'

378	LOAD_FAST         'delay'
381	LOAD_GLOBAL       'TOON_SQUIRT_SUIT_DELAY'
384	BINARY_ADD        None
385	STORE_FAST        'delay'
388	JUMP_BACK         '305'
391	JUMP_BACK         '305'
394	POP_BLOCK         None
395_0	COME_FROM         '298'

395	LOAD_FAST         'mtrack'
398	LOAD_ATTR         'getDuration'
401	CALL_FUNCTION_0   None
404	STORE_FAST        'camDuration'

407	LOAD_GLOBAL       'MovieCamera'
410	LOAD_ATTR         'chooseSquirtShot'
413	LOAD_FAST         'squirts'
416	LOAD_FAST         'suitSquirtsDict'

419	LOAD_FAST         'camDuration'
422	CALL_FUNCTION_3   None
425	STORE_FAST        'camTrack'

428	LOAD_FAST         'mtrack'
431	LOAD_FAST         'camTrack'
434	BUILD_TUPLE_2     None
437	RETURN_VALUE      None

Syntax error at or near `JUMP_BACK' token at offset 177


def __doSuitSquirts(squirts):
    uberClone = 0
    toonTracks = Parallel()
    delay = 0.0
    if type(squirts[0]['target']) == type([]):
        for target in squirts[0]['target']:
            if len(squirts) == 1 and target['hp'] > 0:
                fShowStun = 1
            else:
                fShowStun = 0

    elif len(squirts) == 1 and squirts[0]['target']['hp'] > 0:
        fShowStun = 1
    else:
        fShowStun = 0
    for s in squirts:
        tracks = __doSquirt(s, delay, fShowStun, uberClone)
        if s['level'] >= ToontownBattleGlobals.UBER_GAG_LEVEL_INDEX:
            uberClone = 1
        if tracks:
            for track in tracks:
                toonTracks.append(track)

        delay = delay + TOON_SQUIRT_DELAY

    return toonTracks


def __doSquirt(squirt, delay, fShowStun, uberClone = 0):
    squirtSequence = Sequence(Wait(delay))
    if type(squirt['target']) == type([]):
        for target in squirt['target']:
            notify.debug('toon: %s squirts prop: %d at suit: %d for hp: %d' % (squirt['toon'].getName(),
             squirt['level'],
             target['suit'].doId,
             target['hp']))

    else:
        notify.debug('toon: %s squirts prop: %d at suit: %d for hp: %d' % (squirt['toon'].getName(),
         squirt['level'],
         squirt['target']['suit'].doId,
         squirt['target']['hp']))
    if uberClone:
        ival = squirtfn_array[squirt['level']](squirt, delay, fShowStun, uberClone)
        if ival:
            squirtSequence.append(ival)
    else:
        ival = squirtfn_array[squirt['level']](squirt, delay, fShowStun)
        if ival:
            squirtSequence.append(ival)
    return [squirtSequence]


def __suitTargetPoint(suit):
    pnt = suit.getPos(render)
    pnt.setZ(pnt[2] + suit.getHeight() * 0.66)
    return Point3(pnt)


def __getSplashTrack(point, scale, delay, battle, splashHold = 0.01):

    def prepSplash(splash, point):
        if callable(point):
            point = point()
        splash.reparentTo(render)
        splash.setPos(point)
        scale = splash.getScale()
        splash.setBillboardPointWorld()
        splash.setScale(scale)

    splash = globalPropPool.getProp('splash-from-splat')
    splash.setScale(scale)
    return Sequence(Func(battle.movie.needRestoreRenderProp, splash), Wait(delay), Func(prepSplash, splash, point), ActorInterval(splash, 'splash-from-splat'), Wait(splashHold), Func(MovieUtil.removeProp, splash), Func(battle.movie.clearRenderProp, splash))


def __getSuitTrack(suit, tContact, tDodge, hp, hpbonus, kbbonus, anim, died, leftSuits, rightSuits, battle, toon, fShowStun, beforeStun = 0.5, afterStun = 1.8, geyser = 0, uberRepeat = 0, revived = 0):
    if hp > 0:
        suitTrack = Sequence()
        sival = ActorInterval(suit, anim)
        sival = []
        if kbbonus > 0 and not geyser:
            suitPos, suitHpr = battle.getActorPosHpr(suit)
            suitType = getSuitBodyType(suit.getStyleName())
            animTrack = Sequence()
            animTrack.append(ActorInterval(suit, anim, duration=0.2))
            if suitType == 'a':
                animTrack.append(ActorInterval(suit, 'slip-forward', startTime=2.43))
            elif suitType == 'b':
                animTrack.append(ActorInterval(suit, 'slip-forward', startTime=1.94))
            elif suitType == 'c':
                animTrack.append(ActorInterval(suit, 'slip-forward', startTime=2.58))
            animTrack.append(Func(battle.unlureSuit, suit))
            moveTrack = Sequence(Wait(0.2), LerpPosInterval(suit, 0.6, pos=suitPos, other=battle))
            sival = Parallel(animTrack, moveTrack)
        elif geyser:
            suitStartPos = suit.getPos()
            suitFloat = Point3(0, 0, 14)
            suitEndPos = Point3(suitStartPos[0] + suitFloat[0], suitStartPos[1] + suitFloat[1], suitStartPos[2] + suitFloat[2])
            suitType = getSuitBodyType(suit.getStyleName())
            if suitType == 'a':
                startFlailFrame = 16
                endFlailFrame = 16
            elif suitType == 'b':
                startFlailFrame = 15
                endFlailFrame = 15
            else:
                startFlailFrame = 15
                endFlailFrame = 15
            sival = Sequence(ActorInterval(suit, 'slip-backward', playRate=0.5, startFrame=0, endFrame=startFlailFrame - 1), Func(suit.pingpong, 'slip-backward', fromFrame=startFlailFrame, toFrame=endFlailFrame), Wait(0.5), ActorInterval(suit, 'slip-backward', playRate=1.0, startFrame=endFlailFrame))
            sUp = LerpPosInterval(suit, 1.1, suitEndPos, startPos=suitStartPos, fluid=1)
            sDown = LerpPosInterval(suit, 0.6, suitStartPos, startPos=suitEndPos, fluid=1)
        elif fShowStun == 1:
            sival = Parallel(ActorInterval(suit, anim), MovieUtil.createSuitStunInterval(suit, beforeStun, afterStun))
        else:
            sival = ActorInterval(suit, anim)
        showDamage = Func(suit.showHpText, -hp, openEnded=0, attackTrack=SQUIRT_TRACK)
        updateHealthBar = Func(suit.updateHealthBar, hp)
        suitTrack.append(Wait(tContact))
        suitTrack.append(showDamage)
        suitTrack.append(updateHealthBar)
        if not geyser:
            suitTrack.append(sival)
        elif not uberRepeat:
            geyserMotion = Sequence(sUp, Wait(0.0), sDown)
            suitLaunch = Parallel(sival, geyserMotion)
            suitTrack.append(suitLaunch)
        else:
            suitTrack.append(Wait(5.5))
        bonusTrack = Sequence(Wait(tContact))
        if kbbonus > 0:
            bonusTrack.append(Wait(0.75))
            bonusTrack.append(Func(suit.showHpText, -kbbonus, 2, openEnded=0, attackTrack=SQUIRT_TRACK))
        if hpbonus > 0:
            bonusTrack.append(Wait(0.75))
            bonusTrack.append(Func(suit.showHpText, -hpbonus, 1, openEnded=0, attackTrack=SQUIRT_TRACK))
        if died != 0:
            suitTrack.append(MovieUtil.createSuitDeathTrack(suit, toon, battle))
        else:
            suitTrack.append(Func(suit.loop, 'neutral'))
        if revived != 0:
            suitTrack.append(MovieUtil.createSuitReviveTrack(suit, toon, battle))
        return Parallel(suitTrack, bonusTrack)
    else:
        return MovieUtil.createSuitDodgeMultitrack(tDodge, suit, leftSuits, rightSuits)


def say(statement):
    print statement


def __getSoundTrack(level, hitSuit, delay, node = None):
    if hitSuit:
        soundEffect = globalBattleSoundCache.getSound(hitSoundFiles[level])
    else:
        soundEffect = globalBattleSoundCache.getSound(missSoundFiles[level])
    soundTrack = Sequence()
    if soundEffect:
        soundTrack.append(Wait(delay))
        soundTrack.append(SoundInterval(soundEffect, node=node))
    return soundTrack


def __doFlower(squirt, delay, fShowStun):
    toon = squirt['toon']
    level = squirt['level']
    hpbonus = squirt['hpbonus']
    target = squirt['target']
    suit = target['suit']
    hp = target['hp']
    kbbonus = target['kbbonus']
    died = target['died']
    revived = target['revived']
    leftSuits = target['leftSuits']
    rightSuits = target['rightSuits']
    battle = squirt['battle']
    suitPos = suit.getPos(battle)
    origHpr = toon.getHpr(battle)
    hitSuit = hp > 0
    scale = sprayScales[level]
    tTotalFlowerToonAnimationTime = 2.5
    tFlowerFirstAppears = 1.0
    dFlowerScaleTime = 0.5
    tSprayStarts = tTotalFlowerToonAnimationTime
    dSprayScale = 0.2
    dSprayHold = 0.1
    tContact = tSprayStarts + dSprayScale
    tSuitDodges = tTotalFlowerToonAnimationTime
    tracks = Parallel()
    button = globalPropPool.getProp('button')
    button2 = MovieUtil.copyProp(button)
    buttons = [button, button2]
    hands = toon.getLeftHands()
    toonTrack = Sequence(Func(MovieUtil.showProps, buttons, hands), Func(toon.headsUp, battle, suitPos), ActorInterval(toon, 'pushbutton'), Func(MovieUtil.removeProps, buttons), Func(toon.loop, 'neutral'), Func(toon.setHpr, battle, origHpr))
    tracks.append(toonTrack)
    tracks.append(__getSoundTrack(level, hitSuit, tTotalFlowerToonAnimationTime - 0.4, toon))
    flower = globalPropPool.getProp('squirting-flower')
    flower.setScale(1.5, 1.5, 1.5)
    targetPoint = lambda suit = suit: __suitTargetPoint(suit)

    def getSprayStartPos(flower = flower):
        toon.update(0)
        return flower.getPos(render)

    sprayTrack = MovieUtil.getSprayTrack(battle, WaterSprayColor, getSprayStartPos, targetPoint, dSprayScale, dSprayHold, dSprayScale, horizScale=scale, vertScale=scale)
    lodnames = toon.getLODNames()
    toonlod0 = toon.getLOD(lodnames[0])
    toonlod1 = toon.getLOD(lodnames[1])
    if base.config.GetBool('want-new-anims', 1):
        if not toonlod0.find('**/def_joint_attachFlower').isEmpty():
            flower_joint0 = toonlod0.find('**/def_joint_attachFlower')
    else:
        flower_joint0 = toonlod0.find('**/joint_attachFlower')
    if base.config.GetBool('want-new-anims', 1):
        if not toonlod1.find('**/def_joint_attachFlower').isEmpty():
            flower_joint1 = toonlod1.find('**/def_joint_attachFlower')
    else:
        flower_joint1 = toonlod1.find('**/joint_attachFlower')
    flower_jointpath0 = flower_joint0.attachNewNode('attachFlower-InstanceNode')
    flower_jointpath1 = flower_jointpath0.instanceTo(flower_joint1)
    flowerTrack = Sequence(Wait(tFlowerFirstAppears), Func(flower.reparentTo, flower_jointpath0), LerpScaleInterval(flower, dFlowerScaleTime, flower.getScale(), startScale=MovieUtil.PNT3_NEARZERO), Wait(tTotalFlowerToonAnimationTime - dFlowerScaleTime - tFlowerFirstAppears))
    if hp <= 0:
        flowerTrack.append(Wait(0.5))
    flowerTrack.append(sprayTrack)
    flowerTrack.append(LerpScaleInterval(flower, dFlowerScaleTime, MovieUtil.PNT3_NEARZERO))
    flowerTrack.append(Func(flower_jointpath1.removeNode))
    flowerTrack.append(Func(flower_jointpath0.removeNode))
    flowerTrack.append(Func(MovieUtil.removeProp, flower))
    tracks.append(flowerTrack)
    if hp > 0:
        tracks.append(__getSplashTrack(targetPoint, scale, tSprayStarts + dSprayScale, battle))
    if hp > 0 or delay <= 0:
        tracks.append(__getSuitTrack(suit, tContact, tSuitDodges, hp, hpbonus, kbbonus, 'squirt-small-react', died, leftSuits, rightSuits, battle, toon, fShowStun, revived=revived))
    return tracks


def __doWaterGlass(squirt, delay, fShowStun):
    toon = squirt['toon']
    level = squirt['level']
    hpbonus = squirt['hpbonus']
    target = squirt['target']
    suit = target['suit']
    hp = target['hp']
    kbbonus = target['kbbonus']
    died = target['died']
    revived = target['revived']
    leftSuits = target['leftSuits']
    rightSuits = target['rightSuits']
    battle = squirt['battle']
    suitPos = suit.getPos(battle)
    origHpr = toon.getHpr(battle)
    hitSuit = hp > 0
    scale = sprayScales[level]
    dGlassHold = 5.0
    dGlassScale = 0.5
    tSpray = 82.0 / toon.getFrameRate('spit')
    sprayPoseFrame = 88
    dSprayScale = 0.1
    dSprayHold = 0.1
    tContact = tSpray + dSprayScale
    tSuitDodges = max(tSpray - 0.5, 0.0)
    tracks = Parallel()
    tracks.append(ActorInterval(toon, 'spit'))
    soundTrack = __getSoundTrack(level, hitSuit, 1.7, toon)
    tracks.append(soundTrack)
    glass = globalPropPool.getProp('glass')
    hands = toon.getRightHands()
    hand_jointpath0 = hands[0].attachNewNode('handJoint0-path')
    hand_jointpath1 = hand_jointpath0.instanceTo(hands[1])
    glassTrack = Sequence(Func(MovieUtil.showProp, glass, hand_jointpath0), ActorInterval(glass, 'glass'), Func(hand_jointpath1.removeNode), Func(hand_jointpath0.removeNode), Func(MovieUtil.removeProp, glass))
    tracks.append(glassTrack)
    targetPoint = lambda suit = suit: __suitTargetPoint(suit)

    def getSprayStartPos(toon = toon):
        toon.update(0)
        lod0 = toon.getLOD(toon.getLODNames()[0])
        if base.config.GetBool('want-new-anims', 1):
            if not lod0.find('**/def_head').isEmpty():
                joint = lod0.find('**/def_head')
            else:
                joint = lod0.find('**/joint_head')
        else:
            joint = lod0.find('**/joint_head')
        n = hidden.attachNewNode('pointInFrontOfHead')
        n.reparentTo(toon)
        n.setPos(joint.getPos(toon) + Point3(0, 0.3, -0.2))
        p = n.getPos(render)
        n.removeNode()
        del n
        return p

    sprayTrack = MovieUtil.getSprayTrack(battle, WaterSprayColor, getSprayStartPos, targetPoint, dSprayScale, dSprayHold, dSprayScale, horizScale=scale, vertScale=scale)
    tracks.append(Sequence(Wait(tSpray), sprayTrack))
    if hp > 0:
        tracks.append(__getSplashTrack(targetPoint, scale, tSpray + dSprayScale, battle))
    if hp > 0 or delay <= 0:
        tracks.append(__getSuitTrack(suit, tContact, tSuitDodges, hp, hpbonus, kbbonus, 'squirt-small-react', died, leftSuits, rightSuits, battle, toon, fShowStun, revived=revived))
    return tracks


def __doWaterGun(squirt, delay, fShowStun):
    toon = squirt['toon']
    level = squirt['level']
    hpbonus = squirt['hpbonus']
    target = squirt['target']
    suit = target['suit']
    hp = target['hp']
    kbbonus = target['kbbonus']
    died = target['died']
    revived = target['revived']
    leftSuits = target['leftSuits']
    rightSuits = target['rightSuits']
    battle = squirt['battle']
    suitPos = suit.getPos(battle)
    origHpr = toon.getHpr(battle)
    hitSuit = hp > 0
    scale = sprayScales[level]
    tPistol = 0.0
    dPistolScale = 0.5
    dPistolHold = 1.8
    tSpray = 48.0 / toon.getFrameRate('water-gun')
    sprayPoseFrame = 63
    dSprayScale = 0.1
    dSprayHold = 0.3
    tContact = tSpray + dSprayScale
    tSuitDodges = 1.1
    tracks = Parallel()
    toonTrack = Sequence(Func(toon.headsUp, battle, suitPos), ActorInterval(toon, 'water-gun'), Func(toon.loop, 'neutral'), Func(toon.setHpr, battle, origHpr))
    tracks.append(toonTrack)
    soundTrack = __getSoundTrack(level, hitSuit, 1.8, toon)
    tracks.append(soundTrack)
    pistol = globalPropPool.getProp('water-gun')
    hands = toon.getRightHands()
    hand_jointpath0 = hands[0].attachNewNode('handJoint0-path')
    hand_jointpath1 = hand_jointpath0.instanceTo(hands[1])
    targetPoint = lambda suit = suit: __suitTargetPoint(suit)

    def getSprayStartPos(pistol = pistol, toon = toon):
        toon.update(0)
        joint = pistol.find('**/joint_nozzle')
        p = joint.getPos(render)
        return p

    sprayTrack = MovieUtil.getSprayTrack(battle, WaterSprayColor, getSprayStartPos, targetPoint, dSprayScale, dSprayHold, dSprayScale, horizScale=scale, vertScale=scale)
    pistolPos = Point3(0.28, 0.1, 0.08)
    pistolHpr = VBase3(85.6, -4.44, 94.43)
    pistolTrack = Sequence(Func(MovieUtil.showProp, pistol, hand_jointpath0, pistolPos, pistolHpr), LerpScaleInterval(pistol, dPistolScale, pistol.getScale(), startScale=MovieUtil.PNT3_NEARZERO), Wait(tSpray - dPistolScale))
    pistolTrack.append(sprayTrack)
    pistolTrack.append(Wait(dPistolHold))
    pistolTrack.append(LerpScaleInterval(pistol, dPistolScale, MovieUtil.PNT3_NEARZERO))
    pistolTrack.append(Func(hand_jointpath1.removeNode))
    pistolTrack.append(Func(hand_jointpath0.removeNode))
    pistolTrack.append(Func(MovieUtil.removeProp, pistol))
    tracks.append(pistolTrack)
    if hp > 0:
        tracks.append(__getSplashTrack(targetPoint, 0.3, tSpray + dSprayScale, battle))
    if hp > 0 or delay <= 0:
        tracks.append(__getSuitTrack(suit, tContact, tSuitDodges, hp, hpbonus, kbbonus, 'squirt-small-react', died, leftSuits, rightSuits, battle, toon, fShowStun, revived=revived))
    return tracks


def __doSeltzerBottle(squirt, delay, fShowStun):
    toon = squirt['toon']
    level = squirt['level']
    hpbonus = squirt['hpbonus']
    target = squirt['target']
    suit = target['suit']
    hp = target['hp']
    kbbonus = target['kbbonus']
    died = target['died']
    revived = target['revived']
    leftSuits = target['leftSuits']
    rightSuits = target['rightSuits']
    battle = squirt['battle']
    suitPos = suit.getPos(battle)
    origHpr = toon.getHpr(battle)
    hitSuit = hp > 0
    scale = sprayScales[level]
    tBottle = 0.0
    dBottleScale = 0.5
    dBottleHold = 3.0
    tSpray = 53.0 / toon.getFrameRate('hold-bottle') + 0.05
    dSprayScale = 0.2
    dSprayHold = 0.1
    tContact = tSpray + dSprayScale
    tSuitDodges = max(tContact - 0.7, 0.0)
    tracks = Parallel()
    toonTrack = Sequence(Func(toon.headsUp, battle, suitPos), ActorInterval(toon, 'hold-bottle'), Func(toon.loop, 'neutral'), Func(toon.setHpr, battle, origHpr))
    tracks.append(toonTrack)
    soundTrack = __getSoundTrack(level, hitSuit, tSpray - 0.1, toon)
    tracks.append(soundTrack)
    bottle = globalPropPool.getProp('bottle')
    hands = toon.getRightHands()
    targetPoint = lambda suit = suit: __suitTargetPoint(suit)

    def getSprayStartPos(bottle = bottle, toon = toon):
        toon.update(0)
        joint = bottle.find('**/joint_toSpray')
        n = hidden.attachNewNode('pointBehindSprayProp')
        n.reparentTo(toon)
        n.setPos(joint.getPos(toon) + Point3(0, -0.4, 0))
        p = n.getPos(render)
        n.removeNode()
        del n
        return p

    sprayTrack = MovieUtil.getSprayTrack(battle, WaterSprayColor, getSprayStartPos, targetPoint, dSprayScale, dSprayHold, dSprayScale, horizScale=scale, vertScale=scale)
    hand_jointpath0 = hands[0].attachNewNode('handJoint0-path')
    hand_jointpath1 = hand_jointpath0.instanceTo(hands[1])
    bottleTrack = Sequence(Func(MovieUtil.showProp, bottle, hand_jointpath0), LerpScaleInterval(bottle, dBottleScale, bottle.getScale(), startScale=MovieUtil.PNT3_NEARZERO), Wait(tSpray - dBottleScale))
    bottleTrack.append(sprayTrack)
    bottleTrack.append(Wait(dBottleHold))
    bottleTrack.append(LerpScaleInterval(bottle, dBottleScale, MovieUtil.PNT3_NEARZERO))
    bottleTrack.append(Func(hand_jointpath1.removeNode))
    bottleTrack.append(Func(hand_jointpath0.removeNode))
    bottleTrack.append(Func(MovieUtil.removeProp, bottle))
    tracks.append(bottleTrack)
    if hp > 0:
        tracks.append(__getSplashTrack(targetPoint, scale, tSpray + dSprayScale, battle))
    if (hp > 0 or delay <= 0) and suit:
        tracks.append(__getSuitTrack(suit, tContact, tSuitDodges, hp, hpbonus, kbbonus, 'squirt-small-react', died, leftSuits, rightSuits, battle, toon, fShowStun, revived=revived))
    return tracks


def __doFireHose(squirt, delay, fShowStun):
    toon = squirt['toon']
    level = squirt['level']
    hpbonus = squirt['hpbonus']
    target = squirt['target']
    suit = target['suit']
    hp = target['hp']
    kbbonus = target['kbbonus']
    died = target['died']
    revived = target['revived']
    leftSuits = target['leftSuits']
    rightSuits = target['rightSuits']
    battle = squirt['battle']
    suitPos = suit.getPos(battle)
    origHpr = toon.getHpr(battle)
    hitSuit = hp > 0
    scale = 0.3
    tAppearDelay = 0.7
    dHoseHold = 0.7
    dAnimHold = 5.1
    tSprayDelay = 2.8
    tSpray = 0.2
    dSprayScale = 0.1
    dSprayHold = 1.8
    tContact = 2.9
    tSuitDodges = 2.1
    tracks = Parallel()
    toonTrack = Sequence(Wait(tAppearDelay), Func(toon.headsUp, battle, suitPos), ActorInterval(toon, 'firehose'), Func(toon.loop, 'neutral'), Func(toon.setHpr, battle, origHpr))
    tracks.append(toonTrack)
    soundTrack = __getSoundTrack(level, hitSuit, tSprayDelay, toon)
    tracks.append(soundTrack)
    hose = globalPropPool.getProp('firehose')
    hydrant = globalPropPool.getProp('hydrant')
    hose.reparentTo(hydrant)
    (hose.pose('firehose', 2),)
    hydrantNode = toon.attachNewNode('hydrantNode')
    hydrantNode.clearTransform(toon.getGeomNode().getChild(0))
    hydrantScale = hydrantNode.attachNewNode('hydrantScale')
    hydrant.reparentTo(hydrantScale)
    toon.pose('firehose', 30)
    toon.update(0)
    torso = toon.getPart('torso', '1000')
    if toon.style.torso[0] == 'm':
        hydrant.setPos(torso, 0, 0, -1.85)
    else:
        hydrant.setPos(torso, 0, 0, -1.45)
    hydrant.setPos(0, 0, hydrant.getZ())
    base = hydrant.find('**/base')
    base.setColor(1, 1, 1, 0.5)
    base.setPos(toon, 0, 0, 0)
    toon.loop('neutral')
    targetPoint = lambda suit = suit: __suitTargetPoint(suit)

    def getSprayStartPos(hose = hose, toon = toon, targetPoint = targetPoint):
        toon.update(0)
        if hose.isEmpty() == 1:
            if callable(targetPoint):
                return targetPoint()
            else:
                return targetPoint
        joint = hose.find('**/joint_water_stream')
        n = hidden.attachNewNode('pointBehindSprayProp')
        n.reparentTo(toon)
        n.setPos(joint.getPos(toon) + Point3(0, -0.55, 0))
        p = n.getPos(render)
        n.removeNode()
        del n
        return p

    sprayTrack = Sequence()
    sprayTrack.append(Wait(tSprayDelay))
    sprayTrack.append(MovieUtil.getSprayTrack(battle, WaterSprayColor, getSprayStartPos, targetPoint, dSprayScale, dSprayHold, dSprayScale, horizScale=scale, vertScale=scale))
    tracks.append(sprayTrack)
    hydrantNode.detachNode()
    propTrack = Sequence(Func(battle.movie.needRestoreRenderProp, hydrantNode), Func(hydrantNode.reparentTo, toon), LerpScaleInterval(hydrantScale, tAppearDelay * 0.5, Point3(1, 1, 1.4), startScale=Point3(1, 1, 0.01)), LerpScaleInterval(hydrantScale, tAppearDelay * 0.3, Point3(1, 1, 0.8), startScale=Point3(1, 1, 1.4)), LerpScaleInterval(hydrantScale, tAppearDelay * 0.1, Point3(1, 1, 1.2), startScale=Point3(1, 1, 0.8)), LerpScaleInterval(hydrantScale, tAppearDelay * 0.1, Point3(1, 1, 1), startScale=Point3(1, 1, 1.2)), ActorInterval(hose, 'firehose', duration=dAnimHold), Wait(dHoseHold - 0.2), LerpScaleInterval(hydrantScale, 0.2, Point3(1, 1, 0.01), startScale=Point3(1, 1, 1)), Func(MovieUtil.removeProps, [hydrantNode, hose]), Func(battle.movie.clearRenderProp, hydrantNode))
    tracks.append(propTrack)
    if hp > 0:
        tracks.append(__getSplashTrack(targetPoint, 0.4, 2.7, battle, splashHold=1.5))
    if hp > 0 or delay <= 0:
        tracks.append(__getSuitTrack(suit, tContact, tSuitDodges, hp, hpbonus, kbbonus, 'squirt-small-react', died, leftSuits, rightSuits, battle, toon, fShowStun, revived=revived))
    return tracks


def __doStormCloud(squirt, delay, fShowStun):
    toon = squirt['toon']
    level = squirt['level']
    hpbonus = squirt['hpbonus']
    target = squirt['target']
    suit = target['suit']
    hp = target['hp']
    kbbonus = target['kbbonus']
    died = target['died']
    revived = target['revived']
    leftSuits = target['leftSuits']
    rightSuits = target['rightSuits']
    battle = squirt['battle']
    suitPos = suit.getPos(battle)
    origHpr = toon.getHpr(battle)
    hitSuit = hp > 0
    scale = sprayScales[level]
    tButton = 0.0
    dButtonScale = 0.5
    dButtonHold = 3.0
    tContact = 2.9
    tSpray = 1
    tSuitDodges = 1.8
    tracks = Parallel()
    soundTrack = __getSoundTrack(level, hitSuit, 2.3, toon)
    soundTrack2 = __getSoundTrack(level, hitSuit, 4.6, toon)
    tracks.append(soundTrack)
    tracks.append(soundTrack2)
    button = globalPropPool.getProp('button')
    button2 = MovieUtil.copyProp(button)
    buttons = [button, button2]
    hands = toon.getLeftHands()
    toonTrack = Sequence(Func(MovieUtil.showProps, buttons, hands), Func(toon.headsUp, battle, suitPos), ActorInterval(toon, 'pushbutton'), Func(MovieUtil.removeProps, buttons), Func(toon.loop, 'neutral'), Func(toon.setHpr, battle, origHpr))
    tracks.append(toonTrack)
    cloud = globalPropPool.getProp('stormcloud')
    cloud2 = MovieUtil.copyProp(cloud)
    BattleParticles.loadParticles()
    trickleEffect = BattleParticles.createParticleEffect(file='trickleLiquidate')
    rainEffect = BattleParticles.createParticleEffect(file='liquidate')
    rainEffect2 = BattleParticles.createParticleEffect(file='liquidate')
    rainEffect3 = BattleParticles.createParticleEffect(file='liquidate')
    cloudHeight = suit.height + 3
    cloudPosPoint = Point3(0, 0, cloudHeight)
    scaleUpPoint = Point3(3, 3, 3)
    rainEffects = [rainEffect, rainEffect2, rainEffect3]
    rainDelay = 1
    effectDelay = 0.3
    if hp > 0:
        cloudHold = 4.7
    else:
        cloudHold = 1.7

    def getCloudTrack(cloud, suit, cloudPosPoint, scaleUpPoint, rainEffects, rainDelay, effectDelay, cloudHold, useEffect, battle = battle, trickleEffect = trickleEffect):
        track = Sequence(Func(MovieUtil.showProp, cloud, suit, cloudPosPoint), Func(cloud.pose, 'stormcloud', 0), LerpScaleInterval(cloud, 1.5, scaleUpPoint, startScale=MovieUtil.PNT3_NEARZERO), Wait(rainDelay))
        if useEffect == 1:
            ptrack = Parallel()
            delay = trickleDuration = cloudHold * 0.25
            trickleTrack = Sequence(Func(battle.movie.needRestoreParticleEffect, trickleEffect), ParticleInterval(trickleEffect, cloud, worldRelative=0, duration=trickleDuration, cleanup=True), Func(battle.movie.clearRestoreParticleEffect, trickleEffect))
            track.append(trickleTrack)
            for i in range(0, 3):
                dur = cloudHold - 2 * trickleDuration
                ptrack.append(Sequence(Func(battle.movie.needRestoreParticleEffect, rainEffects[i]), Wait(delay), ParticleInterval(rainEffects[i], cloud, worldRelative=0, duration=dur, cleanup=True), Func(battle.movie.clearRestoreParticleEffect, rainEffects[i])))
                delay += effectDelay

            ptrack.append(Sequence(Wait(3 * effectDelay), ActorInterval(cloud, 'stormcloud', startTime=1, duration=cloudHold)))
            track.append(ptrack)
        else:
            track.append(ActorInterval(cloud, 'stormcloud', startTime=1, duration=cloudHold))
        track.append(LerpScaleInterval(cloud, 0.5, MovieUtil.PNT3_NEARZERO))
        track.append(Func(MovieUtil.removeProp, cloud))
        return track

    tracks.append(getCloudTrack(cloud, suit, cloudPosPoint, scaleUpPoint, rainEffects, rainDelay, effectDelay, cloudHold, useEffect=1))
    tracks.append(getCloudTrack(cloud2, suit, cloudPosPoint, scaleUpPoint, rainEffects, rainDelay, effectDelay, cloudHold, useEffect=0))
    if hp > 0 or delay <= 0:
        tracks.append(__getSuitTrack(suit, tContact, tSuitDodges, hp, hpbonus, kbbonus, 'soak', died, leftSuits, rightSuits, battle, toon, fShowStun, beforeStun=2.6, afterStun=2.3, revived=revived))
    return tracks


def __doGeyser(squirt, delay, fShowStun, uberClone = 0):
    toon = squirt['toon']
    level = squirt['level']
    hpbonus = squirt['hpbonus']
    tracks = Parallel()
    tButton = 0.0
    dButtonScale = 0.5
    dButtonHold = 3.0
    tContact = 2.9
    tSpray = 1
    tSuitDodges = 1.8
    button = 
# Can't uncompyle C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\battle\MovieSquirt.pyc
Traceback (most recent call last):
  File "C:\python27\lib\uncompyle2\__init__.py", line 206, in main
    uncompyle_file(infile, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 143, in uncompyle_file
    uncompyle(version, co, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 132, in uncompyle
    raise walk.ERROR
ParserError: --- This code section failed: ---

0	LOAD_GLOBAL       'len'
3	LOAD_FAST         'squirts'
6	CALL_FUNCTION_1   None
9	LOAD_CONST        0
12	COMPARE_OP        '=='
15	JUMP_IF_FALSE     '25'

18	LOAD_CONST        (None, None)
21	RETURN_VALUE      None
22	JUMP_FORWARD      '25'
25_0	COME_FROM         '22'

25	BUILD_MAP         None
28	STORE_FAST        'suitSquirtsDict'

31	LOAD_CONST        0
34	STORE_FAST        'doneUber'

37	LOAD_CONST        0
40	STORE_FAST        'skip'

43	SETUP_LOOP        '249'
46	LOAD_FAST         'squirts'
49	GET_ITER          None
50	FOR_ITER          '248'
53	STORE_FAST        'squirt'

56	LOAD_CONST        0
59	STORE_FAST        'skip'

62	LOAD_FAST         'skip'
65	JUMP_IF_FALSE     '71'

68	JUMP_BACK         '50'

71	LOAD_GLOBAL       'type'
74	LOAD_FAST         'squirt'
77	LOAD_CONST        'target'
80	BINARY_SUBSCR     None
81	CALL_FUNCTION_1   None
84	LOAD_GLOBAL       'type'
87	BUILD_LIST_0      None
90	CALL_FUNCTION_1   None
93	COMPARE_OP        '=='
96	JUMP_IF_FALSE     '180'

99	LOAD_FAST         'squirt'
102	LOAD_CONST        'target'
105	BINARY_SUBSCR     None
106	LOAD_CONST        0
109	BINARY_SUBSCR     None
110	STORE_FAST        'target'

113	LOAD_FAST         'target'
116	LOAD_CONST        'suit'
119	BINARY_SUBSCR     None
120	LOAD_ATTR         'doId'
123	STORE_FAST        'suitId'

126	LOAD_FAST         'suitSquirtsDict'
129	LOAD_ATTR         'has_key'
132	LOAD_FAST         'suitId'
135	CALL_FUNCTION_1   None
138	JUMP_IF_FALSE     '161'

141	LOAD_FAST         'suitSquirtsDict'
144	LOAD_FAST         'suitId'
147	BINARY_SUBSCR     None
148	LOAD_ATTR         'append'
151	LOAD_FAST         'squirt'
154	CALL_FUNCTION_1   None
157	POP_TOP           None
158	JUMP_ABSOLUTE     '177'

161	LOAD_FAST         'squirt'
164	BUILD_LIST_1      None
167	LOAD_FAST         'suitSquirtsDict'
170	LOAD_FAST         'suitId'
173	STORE_SUBSCR      None
174	JUMP_ABSOLUTE     '245'
177	JUMP_BACK         '50'

180	LOAD_FAST         'squirt'
183	LOAD_CONST        'target'
186	BINARY_SUBSCR     None
187	LOAD_CONST        'suit'
190	BINARY_SUBSCR     None
191	LOAD_ATTR         'doId'
194	STORE_FAST        'suitId'

197	LOAD_FAST         'suitSquirtsDict'
200	LOAD_ATTR         'has_key'
203	LOAD_FAST         'suitId'
206	CALL_FUNCTION_1   None
209	JUMP_IF_FALSE     '232'

212	LOAD_FAST         'suitSquirtsDict'
215	LOAD_FAST         'suitId'
218	BINARY_SUBSCR     None
219	LOAD_ATTR         'append'
222	LOAD_FAST         'squirt'
225	CALL_FUNCTION_1   None
228	POP_TOP           None
229	JUMP_BACK         '50'

232	LOAD_FAST         'squirt'
235	BUILD_LIST_1      None
238	LOAD_FAST         'suitSquirtsDict'
241	LOAD_FAST         'suitId'
244	STORE_SUBSCR      None
245	JUMP_BACK         '50'
248	POP_BLOCK         None
249_0	COME_FROM         '43'

249	LOAD_FAST         'suitSquirtsDict'
252	LOAD_ATTR         'values'
255	CALL_FUNCTION_0   None
258	STORE_FAST        'suitSquirts'

261	LOAD_CONST        '<code_object compFunc>'
264	MAKE_FUNCTION_0   None
267	STORE_FAST        'compFunc'

270	LOAD_FAST         'suitSquirts'
273	LOAD_ATTR         'sort'
276	LOAD_FAST         'compFunc'
279	CALL_FUNCTION_1   None
282	POP_TOP           None

283	LOAD_CONST        0.0
286	STORE_FAST        'delay'

289	LOAD_GLOBAL       'Parallel'
292	CALL_FUNCTION_0   None
295	STORE_FAST        'mtrack'

298	SETUP_LOOP        '395'
301	LOAD_FAST         'suitSquirts'
304	GET_ITER          None
305	FOR_ITER          '394'
308	STORE_FAST        'st'

311	LOAD_GLOBAL       'len'
314	LOAD_FAST         'st'
317	CALL_FUNCTION_1  globalPropPool.getProp('button')
    button2 = MovieUtil.copyProp(button)
    buttons = [button, button2]
    hands = toon.getLeftHands()
    battle = squirt['battle']
    origHpr = toon.getHpr(battle)
    suit = squirt['target'][0]['suit']
    suitPos = suit.getPos(battle)
    toonTrack = Sequence(Func(MovieUtil.showProps, buttons, hands), Func(toon.headsUp, battle, suitPos), ActorInterval(toon, 'pushbutton'), Func(MovieUtil.removeProps, buttons), Func(toon.loop, 'neutral'), Func(toon.setHpr, battle, origHpr))
    tracks.append(toonTrack)
    for target in squirt['target']:
        suit = target['suit']
        hp = target['hp']
        kbbonus = target['kbbonus']
        died = target['died']
        revived = target['revived']
        leftSuits = target['leftSuits']
        rightSuits = target['rightSuits']
        suitPos = suit.getPos(battle)
        hitSuit = hp > 0
        scale = sprayScales[level]
        soundTrack = __getSoundTrack(level, hitSuit, 1.8, toon)
        delayTime = random.random()
        tracks.append(Wait(delayTime))
        tracks.append(soundTrack)
        cloud = globalPropPool.getProp('geyser')
        cloud2 = MovieUtil.copyProp(cloud)
        BattleParticles.loadParticles()
        geyserHeight = battle.getH()
        geyserPosPoint = Point3(0, 0, geyserHeight)
        scaleUpPoint = Point3(1.8, 1.8, 1.8)
        rainEffects = []
        rainDelay = 2.5
        effectDelay = 0.3
        if hp > 0:
            geyserHold = 1.5
        else:
            geyserHold = 0.5

        def getGeyserTrack(geyser, suit, geyserPosPoint, scaleUpPoint, rainEffects, rainDelay, effectDelay, geyserHold, useEffect, battle = battle):
            geyserMound = MovieUtil.copyProp(geyser)
            geyserRemoveM = geyserMound.findAllMatches('**/Splash*')
            geyserRemoveM.addPathsFrom(geyserMound.findAllMatches('**/spout'))
            for i in range(geyserRemoveM.getNumPaths()):
                geyserRemoveM[i].removeNode()

            geyserWater = MovieUtil.copyProp(geyser)
            geyserRemoveW = geyserWater.findAllMatches('**/hole')
            geyserRemoveW.addPathsFrom(geyserWater.findAllMatches('**/shadow'))
            for i in range(geyserRemoveW.getNumPaths()):
                geyserRemoveW[i].removeNode()

            track = Sequence(Wait(rainDelay), Func(MovieUtil.showProp, geyserMound, battle, suit.getPos(battle)), Func(MovieUtil.showProp, geyserWater, battle, suit.getPos(battle)), LerpScaleInterval(geyserWater, 1.0, scaleUpPoint, startScale=MovieUtil.PNT3_NEARZERO), Wait(geyserHold * 0.5), LerpScaleInterval(geyserWater, 0.5, MovieUtil.PNT3_NEARZERO, startScale=scaleUpPoint))
            track.append(LerpScaleInterval(geyserMound, 0.5, MovieUtil.PNT3_NEARZERO))
            track.append(Func(MovieUtil.removeProp, geyserMound))
            track.append(Func(MovieUtil.removeProp, geyserWater))
            track.append(Func(MovieUtil.removeProp, geyser))
            return track

        if not uberClone:
            tracks.append(Sequence(Wait(delayTime), getGeyserTrack(cloud, suit, geyserPosPoint, scaleUpPoint, rainEffects, rainDelay, effectDelay, geyserHold, useEffect=1)))
        if hp > 0 or delay <= 0:
            tracks.append(Sequence(Wait(delayTime), __getSuitTrack(suit, tContact, tSuitDodges, hp, hpbonus, kbbonus, 'soak', died, leftSuits, rightSuits, battle, toon, fShowStun, beforeStun=2.6, afterStun=2.3, geyser=1, uberRepeat=uberClone, revived=revived)))

    return tracks


squirtfn_array = (__doFlower,
 __doWaterGlass,
 __doWaterGun,
 __doSeltzerBottle,
 __doFireHose,
 __doStormCloud,
 __doGeyser)# decompiled 0 files: 0 okay, 1 failed, 0 verify failed
 None
320	LOAD_CONST        0
323	COMPARE_OP        '>'
326	JUMP_IF_FALSE     '391'

329	LOAD_GLOBAL       '__doSuitSquirts'
332	LOAD_FAST         'st'
335	CALL_FUNCTION_1   None
338	STORE_FAST        'ival'

341	LOAD_FAST         'ival'
344	JUMP_IF_FALSE     '378'

347	LOAD_FAST         'mtrack'
350	LOAD_ATTR         'append'
353	LOAD_GLOBAL       'Sequence'
356	LOAD_GLOBAL       'Wait'
359	LOAD_FAST         'delay'
362	CALL_FUNCTION_1   None
365	LOAD_FAST         'ival'
368	CALL_FUNCTION_2   None
371	CALL_FUNCTION_1   None
374	POP_TOP           None
375	JUMP_FORWARD      '378'
378_0	COME_FROM         '375'

378	LOAD_FAST         'delay'
381	LOAD_GLOBAL       'TOON_SQUIRT_SUIT_DELAY'
384	BINARY_ADD        None
385	STORE_FAST        'delay'
388	JUMP_BACK         '305'
391	JUMP_BACK         '305'
394	POP_BLOCK         None
395_0	COME_FROM         '298'

395	LOAD_FAST         'mtrack'
398	LOAD_ATTR         'getDuration'
401	CALL_FUNCTION_0   None
404	STORE_FAST        'camDuration'

407	LOAD_GLOBAL       'MovieCamera'
410	LOAD_ATTR         'chooseSquirtShot'
413	LOAD_FAST         'squirts'
416	LOAD_FAST         'suitSquirtsDict'

419	LOAD_FAST         'camDuration'
422	CALL_FUNCTION_3   None
425	STORE_FAST        'camTrack'

428	LOAD_FAST         'mtrack'
431	LOAD_FAST         'camTrack'
434	BUILD_TUPLE_2     None
437	RETURN_VALUE      None

Syntax error at or near `JUMP_BACK' token at offset 177

