from pandac.PandaModules import *
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.distributed.ClockDelta import *
import MovingPlatform
from toontown.toonbase import ToontownGlobals
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import ClassicFSM
import DistributedSwitch
from toontown.toonbase import TTLocalizer

class DistributedButton(DistributedSwitch.DistributedSwitch):
    __module__ = __name__
    countdownSeconds = 3.0

    def __init__(self, cr):
        self.countdownTrack = None
        DistributedSwitch.DistributedSwitch.__init__(self, cr)
        return

    def setSecondsOn(self, secondsOn):
        self.secondsOn = secondsOn

    def avatarExit(self, avatarId):
        DistributedSwitch.DistributedSwitch.avatarExit(self, avatarId)
        if self.secondsOn != -1.0 and self.secondsOn > 0.0 and self.countdownSeconds > 0.0 and self.countdownSeconds < self.secondsOn and self.fsm.getCurrentState().getName() == 'playing':
            track = self.switchCountdownTrack()
            if track is not None:
                track.start(0.0)
                self.countdownTrack = track
        return

    def setupSwitch--- This code section failed: ---

0	LOAD_GLOBAL       'loader'
3	LOAD_ATTR         'loadModel'
6	LOAD_CONST        'phase_9/models/cogHQ/CogDoor_Button'
9	CALL_FUNCTION_1   None
12	STORE_FAST        'model'

15	LOAD_FAST         'model'
18	JUMP_IF_FALSE     '683'

21	LOAD_FAST         'model'
24	LOAD_ATTR         'find'
27	LOAD_CONST        '**/buttonBase'
30	CALL_FUNCTION_1   None
33	STORE_FAST        'buttonBase'

36	LOAD_GLOBAL       'render'
39	LOAD_ATTR         'attachNewNode'
42	LOAD_CONST        'changePos'
45	CALL_FUNCTION_1   None
48	STORE_FAST        'change'

51	LOAD_FAST         'buttonBase'
54	LOAD_ATTR         'reparentTo'
57	LOAD_FAST         'change'
60	CALL_FUNCTION_1   None
63	POP_TOP           None

64	LOAD_GLOBAL       'render'
67	LOAD_ATTR         'attachNewNode'
70	LOAD_FAST         'self'
73	LOAD_ATTR         'getName'
76	CALL_FUNCTION_0   None
79	LOAD_CONST        '-buttonBase_root'
82	BINARY_ADD        None
83	CALL_FUNCTION_1   None
86	STORE_FAST        'rootNode'

89	LOAD_FAST         'change'
92	LOAD_ATTR         'reparentTo'
95	LOAD_FAST         'rootNode'
98	CALL_FUNCTION_1   None
101	POP_TOP           None

102	LOAD_FAST         'rootNode'
105	LOAD_FAST         'self'
108	STORE_ATTR        'buttonFrameNode'

111	LOAD_FAST         'self'
114	LOAD_ATTR         'buttonFrameNode'
117	LOAD_ATTR         'show'
120	CALL_FUNCTION_0   None
123	POP_TOP           None

124	LOAD_FAST         'model'
127	LOAD_ATTR         'find'
130	LOAD_CONST        '**/button'
133	CALL_FUNCTION_1   None
136	STORE_FAST        'button'

139	LOAD_GLOBAL       'render'
142	LOAD_ATTR         'attachNewNode'
145	LOAD_CONST        'change'
148	CALL_FUNCTION_1   None
151	STORE_FAST        'change'

154	LOAD_FAST         'button'
157	LOAD_ATTR         'reparentTo'
160	LOAD_FAST         'change'
163	CALL_FUNCTION_1   None
166	POP_TOP           None

167	LOAD_GLOBAL       'render'
170	LOAD_ATTR         'attachNewNode'
173	LOAD_FAST         'self'
176	LOAD_ATTR         'getName'
179	CALL_FUNCTION_0   None
182	LOAD_CONST        '-button_root'
185	BINARY_ADD        None
186	CALL_FUNCTION_1   None
189	STORE_FAST        'rootNode'

192	LOAD_FAST         'rootNode'
195	LOAD_ATTR         'setColor'
198	LOAD_FAST         'self'
201	LOAD_ATTR         'color'
204	CALL_FUNCTION_1   None
207	POP_TOP           None

208	LOAD_FAST         'change'
211	LOAD_ATTR         'reparentTo'
214	LOAD_FAST         'rootNode'
217	CALL_FUNCTION_1   None
220	POP_TOP           None

221	LOAD_FAST         'rootNode'
224	LOAD_FAST         'self'
227	STORE_ATTR        'buttonNode'

230	LOAD_FAST         'self'
233	LOAD_ATTR         'buttonNode'
236	LOAD_ATTR         'show'
239	CALL_FUNCTION_0   None
242	POP_TOP           None

243	LOAD_FAST         'self'
246	LOAD_ATTR         'buttonFrameNode'
249	LOAD_ATTR         'reparentTo'
252	LOAD_FAST         'self'
255	CALL_FUNCTION_1   None
258	POP_TOP           None

259	LOAD_FAST         'self'
262	LOAD_ATTR         'buttonNode'
265	LOAD_ATTR         'reparentTo'
268	LOAD_FAST         'self'
271	CALL_FUNCTION_1   None
274	POP_TOP           None

275	LOAD_CONST        0.5
278	STORE_FAST        'radius'

281	LOAD_GLOBAL       'CollisionSphere'
284	LOAD_CONST        0.0
287	LOAD_CONST        0.0
290	LOAD_FAST         'radius'
293	LOAD_FAST         'radius'
296	CALL_FUNCTION_4   None
299	STORE_FAST        'cSphere'

302	LOAD_FAST         'cSphere'
305	LOAD_ATTR         'setTangible'
308	LOAD_CONST        0
311	CALL_FUNCTION_1   None
314	POP_TOP           None

315	LOAD_GLOBAL       'CollisionNode'
318	LOAD_FAST         'self'
321	LOAD_ATTR         'getName'
324	CALL_FUNCTION_0   None
327	CALL_FUNCTION_1   None
330	STORE_FAST        'cSphereNode'

333	LOAD_FAST         'cSphereNode'
336	LOAD_ATTR         'addSolid'
339	LOAD_FAST         'cSphere'
342	CALL_FUNCTION_1   None
345	POP_TOP           None

346	LOAD_FAST         'cSphereNode'
349	LOAD_ATTR         'setCollideMask'
352	LOAD_GLOBAL       'ToontownGlobals'
355	LOAD_ATTR         'WallBitmask'
358	CALL_FUNCTION_1   None
361	POP_TOP           None

362	LOAD_FAST         'rootNode'
365	LOAD_ATTR         'attachNewNode'
368	LOAD_FAST         'cSphereNode'
371	CALL_FUNCTION_1   None
374	LOAD_FAST         'self'
377	STORE_ATTR        'cSphereNodePath'
380	JUMP_FORWARD      '383'
383_0	COME_FROM         '380'

383	LOAD_FAST         'button'
386	LOAD_ATTR         'find'
389	LOAD_CONST        '**/collision_floor'
392	CALL_FUNCTION_1   None
395	STORE_FAST        'collisionFloor'

398	LOAD_FAST         'collisionFloor'
401	LOAD_ATTR         'isEmpty'
404	CALL_FUNCTION_0   None
407	JUMP_IF_FALSE     '551'

410	LOAD_CONST        0.475
413	STORE_FAST        'top'

416	LOAD_CONST        0.5
419	STORE_FAST        'size'

422	LOAD_GLOBAL       'CollisionPolygon'
425	LOAD_GLOBAL       'Point3'
428	LOAD_FAST         'size'
431	UNARY_NEGATIVE    None
432	LOAD_FAST         'size'
435	UNARY_NEGATIVE    None
436	LOAD_FAST         'top'
439	CALL_FUNCTION_3   None

442	LOAD_GLOBAL       'Point3'
445	LOAD_FAST         'size'
448	LOAD_FAST         'size'
451	UNARY_NEGATIVE    None
452	LOAD_FAST         'top'
455	CALL_FUNCTION_3   None

458	LOAD_GLOBAL       'Point3'
461	LOAD_FAST         'size'
464	LOAD_FAST         'size'
467	LOAD_FAST         'top'
470	CALL_FUNCTION_3   None

473	LOAD_GLOBAL       'Point3'
476	LOAD_FAST         'size'
479	UNARY_NEGATIVE    None
480	LOAD_FAST         'size'
483	LOAD_FAST         'top'
486	CALL_FUNCTION_3   None
489	CALL_FUNCTION_4   None
492	STORE_FAST        'floor'

495	LOAD_FAST         'floor'
498	LOAD_ATTR         'setTangible'
501	LOAD_CONST        1
504	CALL_FUNCTION_1   None
507	POP_TOP           None

508	LOAD_GLOBAL       'CollisionNode'
511	LOAD_CONST        'collision_floor'
514	CALL_FUNCTION_1   None
517	STORE_FAST        'floorNode'

520	LOAD_FAST         'floorNode'
523	LOAD_ATTR         'addSolid'
526	LOAD_FAST         'floor'
529	CALL_FUNCTION_1   None
532	POP_TOP           None

533	LOAD_FAST         'button'
536	LOAD_ATTR         'attachNewNode'
539	LOAD_FAST         'floorNode'
542	CALL_FUNCTION_1   None
545	STORE_FAST        'collisionFloor'
548	JUMP_FORWARD      '604'

551	LOAD_FAST         'collisionFloor'
554	LOAD_ATTR         'getParent'
557	CALL_FUNCTION_0   None
560	LOAD_ATTR         'attachNewNode'
563	LOAD_CONST        'changeFloor'
566	CALL_FUNCTION_1   None
569	STORE_FAST        'change'

572	LOAD_FAST         'change'
575	LOAD_ATTR         'setScale'
578	LOAD_CONST        0.5
581	LOAD_CONST        0.5
584	LOAD_CONST        1.0
587	CALL_FUNCTION_3   None
590	POP_TOP           None

591	LOAD_FAST         'collisionFloor'
594	LOAD_ATTR         'reparentTo'
597	LOAD_FAST         'change'
600	CALL_FUNCTION_1   None
603	POP_TOP           None
604_0	COME_FROM         '548'

604	LOAD_FAST         'collisionFloor'
607	LOAD_ATTR         'node'
610	CALL_FUNCTION_0   None
613	LOAD_ATTR         'setFromCollideMask'
616	LOAD_GLOBAL       'BitMask32'
619	LOAD_ATTR         'allOff'
622	CALL_FUNCTION_0   None
625	CALL_FUNCTION_1   None
628	POP_TOP           None

629	LOAD_FAST         'collisionFloor'
632	LOAD_ATTR         'node'
635	CALL_FUNCTION_0   None
638	LOAD_ATTR         'setIntoCollideMask'
641	LOAD_GLOBAL       'ToontownGlobals'
644	LOAD_ATTR         'FloorBitmask'
647	CALL_FUNCTION_1   None
650	POP_TOP           None
651	JUMP_FORWARD      '654'
654_0	COME_FROM         '651'

654	LOAD_FAST         'self'
657	LOAD_ATTR         'buttonFrameNode'
660	LOAD_ATTR         'flattenMedium'
663	CALL_FUNCTION_0   None
666	POP_TOP           None

667	LOAD_FAST         'self'
670	LOAD_ATTR         'buttonNode'
673	LOAD_ATTR         'flattenMedium'
676	CALL_FUNCTION_0   None
679	POP_TOP           None
680	JUMP_FORWARD      '683'
683_0	COME_FROM         '680'

Syntax error at or near `COME_FROM' token at offset 654_0

    def delete(self):
        DistributedSwitch.DistributedSwitch.delete(self)

    def enterTrigger(self, args = None):
        DistributedSwitch.DistributedSwitch.enterTrigger(self, args)

    def exitTrigger(self, args = None):
        DistributedSwitch.DistributedSwitch.exitTrigger(self, args)

    def switchOnTrack(self):
        onSfx = base.loadSfx('phase_9/audio/sfx/CHQ_FACT_switch_pressed.mp3')
        duration = 0.8
        halfDur = duration * 0.5
        pos = Vec3(0.0, 0.0, -0.2)
        color = Vec4(0.0, 1.0, 0.0, 1.0)
        track = Sequence(Func(self.setIsOn, 1), Parallel(SoundInterval(onSfx, node=self.node, volume=0.9), LerpPosInterval(nodePath=self.buttonNode, duration=duration, pos=pos, blendType='easeInOut'), Sequence(Wait(halfDur), LerpColorInterval(nodePath=self.buttonNode, duration=halfDur, color=color, override=1, blendType='easeOut'))))
        return track

    def switchCountdownTrack(self):
        wait = self.secondsOn - self.countdownSeconds
        countDownSfx = base.loadSfx('phase_9/audio/sfx/CHQ_FACT_switch_depressed.mp3')
        track = Parallel(SoundInterval(countDownSfx), Sequence(Wait(wait), Wait(0.5), LerpColorInterval(nodePath=self.buttonNode, duration=0.1, color=self.color, override=1, blendType='easeIn'), LerpColorInterval(nodePath=self.buttonNode, duration=0.1, color=Vec4(0.0, 1.0, 0.0, 1.0), override=1, blendType='easeOut'), Wait(0.5), LerpColorInterval(nodePath=self.buttonNode, duration=0.1, color=self.color, override=1, blendType='easeIn'), LerpColorInterval(nodePath=self.buttonNode, duration=0.1, color=Vec4(0.0, 1.0, 0.0, 1.0), override=1, blendType='easeOut'), Wait(0.4), LerpColorInterval(nodePath=self.buttonNode, duration=0.1, color=self.color, override=1, blendType='easeIn'), LerpColorInterval(nodePath=self.buttonNode, duration=0.1, color=Vec4(0.0, 1.0, 0.0, 1.0), override=1, blendType='easeOut'), Wait(0.3), LerpColorInterval(nodePath=self.buttonNode, duration=0.1, color=self.color, override=1, blendType='easeIn'), LerpColorInterval(nodePath=self.buttonNode, duration=0.1, color=Vec4(0.0, 1.0, 0.0, 1.0), override=1, blendType='easeOut'), Wait(0.2), LerpColorInterval(nodePath=self.buttonNode, duration=0.1, color=self.color, override=1, blendType='easeIn'), LerpColorInterval(nodePath=self.buttonNode, duration=0.1, override=1, color=Vec4(0.0, 1.0, 0.0, 1.0), blendType='easeOut'), Wait(0.1)))
        return track

    def switchOffTrack(self):
        offSfx = base.loadSfx('phase_9/audio/sfx/CHQ_FACT_switch_popup.mp3')
        duration = 1.0
        halfDur = duration * 0.5
        pos = Vec3(0.0)
        track = Sequence(Parallel(SoundInterval(offSfx, node=self.node, volume=1.0), LerpPosInterval(nodePath=self.buttonNode, duration=duration, pos=pos, blendType='easeInOut'), Sequence(Wait(halfDur), LerpColorInterval(nodePath=self.buttonNode, duration=halfDur, color=self.color, override=1, blendType='easeIn'))), Func(self.setIsOn, 0))
        return track

    def exitPlaying(self):
        if self.countdownTrack:
            self.countdownTrack.finish()
        self.countdownTrack = None
        DistributedSwitch.DistributedSwitch.exitPlaying(sel
# Can't uncompyle C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\coghq\DistributedButton.pyc
Traceback (most recent call last):
  File "C:\python27\lib\uncompyle2\__init__.py", line 206, in main
    uncompyle_file(infile, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 143, in uncompyle_file
    uncompyle(version, co, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 132, in uncompyle
    raise walk.ERROR
ParserError: --- This code section failed: ---

0	LOAD_GLOBAL       'loader'
3	LOAD_ATTR         'loadModel'
6	LOAD_CONST        'phase_9/models/cogHQ/CogDoor_Button'
9	CALL_FUNCTION_1   None
12	STORE_FAST        'model'

15	LOAD_FAST         'model'
18	JUMP_IF_FALSE     '683'

21	LOAD_FAST         'model'
24	LOAD_ATTR         'find'
27	LOAD_CONST        '**/buttonBase'
30	CALL_FUNCTION_1   None
33	STORE_FAST        'buttonBase'

36	LOAD_GLOBAL       'render'
39	LOAD_ATTR         'attachNewNode'
42	LOAD_CONST        'changePos'
45	CALL_FUNCTION_1   None
48	STORE_FAST        'change'

51	LOAD_FAST         'buttonBase'
54	LOAD_ATTR         'reparentTo'
57	LOAD_FAST         'change'
60	CALL_FUNCTION_1   None
63	POP_TOP           None

64	LOAD_GLOBAL       'render'
67	LOAD_ATTR         'attachNewNode'
70	LOAD_FAST         'self'
73	LOAD_ATTR         'getName'
76	CALL_FUNCTION_0   None
79	LOAD_CONST        '-buttonBase_root'
82	BINARY_ADD        None
83	CALL_FUNCTION_1   None
86	STORE_FAST        'rootNode'

89	LOAD_FAST         'change'
92	LOAD_ATTR         'reparentTo'
95	LOAD_FAST         'rootNode'
98	CALL_FUNCTION_1   None
101	POP_TOP           None

102	LOAD_FAST         'rootNode'
105	LOAD_FAST         'self'
108	STORE_ATTR        'buttonFrameNode'

111	LOAD_FAST         'self'
114	LOAD_ATTR         'buttonFrameNode'
117	LOAD_ATTR         'show'
120	CALL_FUNCTION_0   None
123	POP_TOP           None

124	LOAD_FAST         'model'
127	LOAD_ATTR         'find'
130	LOAD_CONST        '**/button'
133	CALL_FUNCTION_1   None
136	STORE_FAST        'button'

139	LOAD_GLOBAL       'render'
142	LOAD_ATTR         'attachNewNode'
145	LOAD_CONST        'change'
148	CALL_FUNCTION_1   None
151	STORE_FAST        'change'

154	LOAD_FAST         'button'
157	LOAD_ATTR         'reparentTo'
160	LOAD_FAST         'change'
163	CALL_FUNCTION_1   None
166	POP_TOP           None

167	LOAD_GLOBAL       'render'
170	LOAD_ATTR         'attachNewNode'
173	LOAD_FAST         'self'
176	LOAD_ATTR         'getName'
179	CALL_FUNCTION_0   None
182	LOAD_CONST        '-button_root'
185	BINARY_ADD        None
186	CALL_FUNCTION_1   None
189	STORE_FAST        'rootNode'

192	LOAD_FAST         'rootNode'
195	LOAD_ATTR         'setColor'
198	LOAD_FAST         'self'
201	LOAD_ATTR         'color'
204	CALL_FUNCTION_1   None
207	POP_TOP           None

208	LOAD_FAST         'change'
211	LOAD_ATTR         'reparentTo'
214	LOAD_FAST         'rootNode'
217	CALL_FUNCTION_1   None
220	POP_TOP           None

221	LOAD_FAST         'rootNode'
224	LOAD_FAST         'self'
227	STORE_ATTR        'buttonNode'

230	LOAD_FAST         'self'
233	LOAD_ATTR         'buttonNode'
236	LOAD_ATTR         'show'
239	CALL_FUNCTION_0   None
242	POP_TOP           None

243	LOAD_FAST         'self'
246	LOAD_ATTR         'buttonFrameNode'
249	LOAD_ATTR         'reparentTo'
252	LOAD_FAST         'self'
255	CALL_FUNCTION_1   None
258	POP_TOP           None

259	LOAD_FAST         'self'
262	LOAD_ATTR         'buttonNode'
265	LOAD_ATTR         'reparentTo'
268	LOAD_FAST         'self'
271	CALL_FUNCTION_1   None
274	POP_TOP           None

275	LOAD_CONST        0.5
278	STORE_FAST        'radius'

281	LOAD_GLOBAL       'CollisionSphere'
284	LOAD_CONST        0.0
287	LOAD_CONST        0.0
290	LOAD_FAST         'radius'
293	LOAD_FAST         'radius'
296	CALL_FUNCTION_4   None
299	STORE_FAST        'cSphere'

302	LOAD_FAST         'cSphere'
305	LOAD_ATTR         'setTangible'
308	LOAD_CONST        0
311	CALL_FUNCTION_1   None
314	POP_TOP           None

315	LOAD_GLOBAL       'CollisionNode'
318	LOAD_FAST         'self'
321	LOAD_ATTR         'getName'
324	CALL_FUNCTION_0   None
327	CALL_FUNCTION_1   None
330	STORE_FAST        'cSphereNode'

333	LOAD_FAST         'cSphereNode'
336	LOAD_ATTR         'addSolid'
339	LOAD_FAST         'cSphere'
342	CALL_FUNCTION_1   None
345	POP_TOP           None

346	LOAD_FAST         'cSphereNode'
349	LOAD_ATTR         'setCollideMask'
352	LOAD_GLOBAL       'ToontownGlobals'
355	LOAD_ATTR         'WallBitmask'
358	CALL_FUNCTION_1   None
361	POP_TOP           None

362	LOAD_FAST         'rootNode'
365	LOAD_ATTR         'attachNewNode'
368	LOAD_FAST         'cSphereNode'
371	CALL_FUNCTION_1   None
374	LOAD_FAST         'self'
377	STORE_ATTR        'cSphereNodePath'
380	JUMP_FORWARD      '383'
383_0	COME_FROM         '380'

383	LOAD_FAST         'button'
386	LOAD_ATTR         'find'
389	LOAD_CONST        '**/collision_floor'
392	CALL_FUNCTION_1   None
395	STORE_FAST        'collisionFloor'

398	LOAD_FAST         'collisionFloor'
401	LOAD_ATTR         'isEmpty'
404	CALL_FUNCTION_0   None
407	JUMP_IF_FALSE     '551'

410	LOAD_CONST        0.475
413	STORE_FAST        'top'

416	LOAD_CONST        0.5
419	STORE_FAST        'size'

422	LOAD_GLOBAL       'CollisionPolygon'
425	LOAD_GLOBAL       'Point3'
428	LOAD_FAST         'size'
431	UNARY_NEGATIVE    None
432	LOAD_FAST         'size'
435	UNARY_NEGATIVE    None
436	LOAD_FAST         'top'
439	CALL_FUNCTION_3   None

442	LOAD_GLOBAL       'Point3'
445	LOAD_FAST         'size'
448	LOAD_FAST         'size'
451	UNARY_NEGATIVE    None
452	LOAD_FAST         'top'
455	CALL_FUNCTION_3   None

458	LOAD_GLOBAL       'Point3'
461	LOAD_FAST         'size'
464	LOAD_FAST         'size'
467	LOAD_FAST         'top'
470	CALL_FUNCTION_3   None

473	LOAD_GLOBAL       'Point3'
476	LOAD_FAST         'size'
479	UNARY_NEGATIVE    None
480	LOAD_FAST         'size'
483	LOAD_FAST         'top'
486	CALL_FUNCTION_3   None
489	CALL_FUNCTION_4   None
492	STORE_FAST        'floor'

495	LOAD_FAST         'floor'
498	LOAD_ATTR         'setTangible'
501	LOAD_CONST        1
504	CALL_FUNCTION_1   None
507	POP_TOP           None

508	LOAD_GLOBAL       'CollisionNode'
511	LOAD_CONST        'collision_floor'
514	CALL_FUNCTION_1   None
517	STORE_FAST        'floorNode'

520	LOAD_FAST         'floorNode'
523	LOAD_ATTR         'addSolid'
526	LOAD_FAST         'floor'
529	CALL_FUNCTION_1   None
532	POP_TOP           None

533	LOAD_FAST         'button'
536	LOAD_ATTR         'attachNewNode'
539	LOAD_FAST         'floorNode'
542	CALL_FUNCTION_1   None
545	STORE_FAST        'collisionFloor'
548	JUMP_FORWARD      '604'

551	LOAD_FAST         'collisionFloor'
554	LOAD_ATTR         'getParent'
557	CALL_FUNCTION_0   None
560	LOAD_ATTR         'attachNewNode'
563	LOAD_CONST        'changeFloor'
566	CALL_FUNCTION_1   None
569	STORE_FAST        'change'

572	LOAD_FAST         'change'
575	LOAD_ATTR         'setScale'
578	LOAD_CONST        0.5
581	LOAD_CONST        0.5
584	LOAD_CONST        1.0
587	CALL_FUNCTION_3   None
590	POP_TOP           None

591	LOAD_FAST         'collisionFloor'
594	LOAD_ATTR         'reparentTo'
597	LOAD_FAST         'change'
600	CALL_FUNCTION_1   None
603	POP_TOP           None
604_0	COME_FROM         '548'

604	LOAD_FAST         'collisionFloor'
607	LOAD_ATTR         'node'
610	CALL_FUNCTION_0   None
613	LOAD_ATTR         'setFromCollideMask'
616	LOAD_GLOBAL       'BitMask32'
619	LOAD_ATTR         'allOff'
622	CALL_FUNCTION_0   None
625	CALL_FUNCTION_1   None
628	POP_TOP           None

629	LOAD_FAST         'collisionFloor'
632	LOAD_ATTR         'node'
635	CALL_FUNCTION_0   None
638	LOAD_ATTR         'setIntoCollideMask'
641	LOAD_GLOBAL       'ToontownGlobals'
644	LOAD_ATTR         'FloorBitmask'
647	CALL_FUNCTION_1   None
650	POP_TOP           None
651	JUMP_FORWARD      '654'
654_0	COME_FROM         '651'

654	LOAD_FAST         'self'
657	LOAD_ATTR         'buttonFrameNode'
660	LOAD_ATTR         'flattenMedium'
663	CALL_FUNCTION_0   None
666	POP_TOP           None

667	LOAD_FAST         'self'
670	LOAD_ATTR         'buttonNode'
673	LOAD_ATTR         'flattenMedium'
f)
        return# decompiled 0 files: 0 okay, 1 failed, 0 verify failed
676	CALL_FUNCTION_0   None
679	POP_TOP           None
680	JUMP_FORWARD      '683'
683_0	COME_FROM         '680'

Syntax error at or near `COME_FROM' token at offset 654_0

