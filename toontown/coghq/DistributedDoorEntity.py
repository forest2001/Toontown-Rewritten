from pandac.PandaModules import *
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.distributed.ClockDelta import *
from toontown.toonbase import ToontownGlobals
from direct.directnotify import DirectNotifyGlobal
import DistributedDoorEntityBase
from direct.fsm import FourState
from direct.fsm import ClassicFSM
from otp.level import DistributedEntity
from toontown.toonbase import TTLocalizer
from otp.level import BasicEntities
from direct.fsm import State
from otp.level import VisibilityBlocker

class DistributedDoorEntityLock(DistributedDoorEntityBase.LockBase, FourState.FourState):
    __module__ = __name__
    slideLeft = Vec3(-7.5, 0.0, 0.0)
    slideRight = Vec3(7.5, 0.0, 0.0)

    def __init__(self, door, lockIndex, lockedNodePath, leftNodePath, rightNodePath, stateIndex):
        self.door = door
        self.lockIndex = lockIndex
        self.lockedNodePath = lockedNodePath
        self.leftNodePath = leftNodePath
        self.rightNodePath = rightNodePath
        self.initialStateIndex = stateIndex
        FourState.FourState.__init__(self, self.stateNames, self.stateDurations)

    def delete(self):
        self.takedown()
        del self.door

    def setup(self):
        self.setLockState(self.initialStateIndex)
        del self.initialStateIndex

    def takedown(self):
        if self.track is not None:
            self.track.pause()
            self.track = None
        for i in self.states.keys():
            del self.states[i]

        self.states = []
        self.fsm = None
        return

    def setLockState(self, stateIndex):
        if self.stateIndex != stateIndex:
            state = self.states.get(stateIndex)
            if state is not None:
                self.fsm.request(state)
        return

    def isUnlocked(self):
        return self.isOn()

    def enterState1(self):
        FourState.FourState.enterState1(self)
        beat = self.duration * 0.05
        slideSfx = base.loadSfx('phase_9/audio/sfx/CHQ_FACT_arms_retracting.mp3')
        self.setTrack(Sequence(Wait(beat * 2.0), Parallel(SoundInterval(slideSfx, node=self.door.node, volume=0.8), Sequence(ShowInterval(self.leftNodePath), ShowInterval(self.rightNodePath), Parallel(LerpPosInterval(nodePath=self.leftNodePath, other=self.lockedNodePath, duration=beat * 16.0, pos=Vec3(0.0), blendType='easeIn'), LerpPosInterval(nodePath=self.rightNodePath, other=self.lockedNodePath, duration=beat * 16.0, pos=Vec3(0.0), blendType='easeIn')), HideInterval(self.leftNodePath), HideInterval(self.rightNodePath), ShowInterval(self.lockedNodePath)))))

    def enterState2(self):
        FourState.FourState.enterState2(self)
        self.setTrack(None)
        self.leftNodePath.setPos(self.lockedNodePath, Vec3(0.0))
        self.rightNodePath.setPos(self.lockedNodePath, Vec3(0.0))
        self.leftNodePath.hide()
        self.rightNodePath.hide()
        self.lockedNodePath.show()
        return

    def enterState3(self):
        FourState.FourState.enterState3(self)
        unlockSfx = base.loadSfx('phase_9/audio/sfx/CHQ_FACT_door_unlock.mp3')
        slideSfx = base.loadSfx('phase_9/audio/sfx/CHQ_FACT_arms_retracting.mp3')
        beat = self.duration * 0.05
        self.setTrack(Sequence(Wait(beat * 2), Parallel(SoundInterval(unlockSfx, node=self.door.node, volume=0.8), SoundInterval(slideSfx, node=self.door.node, volume=0.8), Sequence(HideInterval(self.lockedNodePath), ShowInterval(self.leftNodePath), ShowInterval(self.rightNodePath), Parallel(LerpPosInterval(nodePath=self.leftNodePath, other=self.lockedNodePath, duration=beat * 16, pos=self.slideLeft, blendType='easeOut'), LerpPosInterval(nodePath=self.rightNodePath, other=self.lockedNodePath, duration=beat * 16, pos=self.slideRight, blendType='easeOut')), HideInterval(self.leftNodePath), HideInterval(self.rightNodePath)))))

    def enterState4(self):
        FourState.FourState.enterState4(self)
        self.setTrack(None)
        self.leftNodePath.setPos(self.lockedNodePath, self.slideLeft)
        self.rightNodePath.setPos(self.lockedNodePath, self.slideRight)
        self.leftNodePath.hide()
        self.rightNodePath.hide()
        self.lockedNodePath.hide()
        return


class DistributedDoorEntity(DistributedDoorEntityBase.DistributedDoorEntityBase, DistributedEntity.DistributedEntity, BasicEntities.NodePathAttribsProxy, FourState.FourState, VisibilityBlocker.VisibilityBlocker):
    __module__ = __name__

    def __init__(self, cr):
        self.innerDoorsTrack = None
        self.isVisReady = 0
        self.isOuterDoorOpen = 0
        DistributedEntity.DistributedEntity.__init__(self, cr)
        FourState.FourState.__init__(self, self.stateNames, self.stateDurations)
        VisibilityBlocker.VisibilityBlocker.__init__(self)
        self.locks = []
        return

    def generate(self):
        DistributedEntity.DistributedEntity.generate(self)

    def announceGenerate(self):
        self.doorNode = hidden.attachNewNode('door-%s' % self.entId)
        DistributedEntity.DistributedEntity.announceGenerate(self)
        BasicEntities.NodePathAttribsProxy.initNodePathAttribs(self)
        self.setup()

    def disable(self):
        self.takedown()
        self.doorNode.removeNode()
        del self.doorNode
        DistributedEntity.DistributedEntity.disable(self)

    def delete(self):
        DistributedEntity.DistributedEntity.delete(self)

    def setup(self):
        self.setupDoor()
        for i in self.locks:
            i.setup()

        self.accept('exit%s' % (self.getName(),), self.exitTrigger)
        self.acceptAvatar()
        if __dev__:
            self.initWantDoors()

    def takedown(self):
        if __dev__:
            self.shutdownWantDoors()
        self.ignoreAll()
        if self.track is not None:
            self.track.finish()
        self.track = None
        if self.innerDoorsTrack is not None:
            self.innerDoorsTrack.finish()
        self.innerDoorsTrack = None
        for i in self.locks:
            i.takedown()

        self.locks = []
        self.fsm = None
        for i in self.states.keys():
            del self.states[i]

        self.states = []
        return

    setUnlock0Event = DistributedDoorEntityBase.stubFunction
    setUnlock1Event = DistributedDoorEntityBase.stubFunction
    setUnlock2Event = DistributedDoorEntityBase.stubFunction
    setUnlock3Event = DistributedDoorEntityBase.stubFunction
    setIsOpenEvent = DistributedDoorEntityBase.stubFunction
    setIsLock0Unlocked = DistributedDoorEntityBase.stubFunction
    setIsLock1Unlocked = DistributedDoorEntityBase.stubFunction
    setIsLock2Unlocked = DistributedDoorEntityBase.stubFunction
    setIsLock3Unlocked = DistributedDoorEntityBase.stubFunction
    setIsOpen = DistributedDoorEntityBase.stubFunction
    setSecondsOpen = DistributedDoorEntityBase.stubFunction

    def acceptAvatar(self):
        self.accept('enter%s' % (self.getName(),), self.enterTrigger)

    def rejectInteract(self):
        DistributedEntity.DistributedEntity.rejectInteract(self)
        self.acceptAvatar()

    def avatarExit(self, avatarId):
        DistributedEntity.DistributedEntity.avatarExit(self, avatarId)
        self.acceptAvatar()

    def enterTrigger(self, args = None):
        messenger.send('DistributedInteractiveEntity_enterTrigger')
        self.sendUpdate('requestOpen')

    def exitTrigger(self, args = None):
        messenger.send('DistributedInteractiveEntity_exitTrigger')

    def okToUnblockVis(self):
        VisibilityBlocker.VisibilityBlocker.okToUnblockVis(self)
        self.isVisReady = 1
        self.openInnerDoors()

    def changedOnState(self, isOn):
        messenger.send(self.getOutputEventName(), [not isOn])

    def setLocksState(self, stateBits):
        lock0 = stateBits & 15
        lock1 = (stateBits & 240) >> 4
        lock2 = (stateBits & 3840) >> 8
        if self.isGenerated():
            self.locks[0].setLockState(lock0)
            self.locks[1].setLockState(lock1)
            self.locks[2].setLockState(lock2)
        else:
            self.initialLock0StateIndex = lock0
            self.initialLock1StateIndex = lock1
            self.initialLock2StateIndex = lock2

    def setDoorState(self, stateIndex, timeStamp):
        self.stateTime = globalClockDelta.localElapsedTime(timeStamp)
        if self.isGenerated():
            if self.stateIndex != stateIndex:
                state = self.states.get(stateIndex)
                if state is not None:
                    self.fsm.request(state)
        else:
            self.initialState = stateIndex
            self.initialStateTimestamp = timeStamp
        return

    def getName(self):
        return 'switch-%s' % str(self.entId)

    def getNodePath(self):
        if hasattr(self, 'doorNode'):
            return self.doorNode
        return None

    def setupDoor--- This code section failed: ---

0	LOAD_GLOBAL       'loader'
3	LOAD_ATTR         'loadModel'
6	LOAD_CONST        'phase_9/models/cogHQ/CogDoorHandShake'
9	CALL_FUNCTION_1   None
12	STORE_FAST        'model'

15	LOAD_FAST         'model'
18	JUMP_IF_FALSE     '1653'

21	LOAD_FAST         'model'
24	LOAD_ATTR         'find'
27	LOAD_CONST        '**/Doorway1'
30	CALL_FUNCTION_1   None
33	STORE_FAST        'doorway'

36	LOAD_FAST         'self'
39	LOAD_ATTR         'doorNode'
42	LOAD_ATTR         'attachNewNode'
45	LOAD_FAST         'self'
48	LOAD_ATTR         'getName'
51	CALL_FUNCTION_0   None
54	LOAD_CONST        '-root'
57	BINARY_ADD        None
58	CALL_FUNCTION_1   None
61	STORE_FAST        'rootNode'

64	LOAD_FAST         'rootNode'
67	LOAD_ATTR         'setPos'
70	LOAD_FAST         'self'
73	LOAD_ATTR         'pos'
76	CALL_FUNCTION_1   None
79	POP_TOP           None

80	LOAD_FAST         'rootNode'
83	LOAD_ATTR         'setHpr'
86	LOAD_FAST         'self'
89	LOAD_ATTR         'hpr'
92	CALL_FUNCTION_1   None
95	POP_TOP           None

96	LOAD_FAST         'rootNode'
99	LOAD_ATTR         'setScale'
102	LOAD_FAST         'self'
105	LOAD_ATTR         'scale'
108	CALL_FUNCTION_1   None
111	POP_TOP           None

112	LOAD_FAST         'rootNode'
115	LOAD_ATTR         'setColor'
118	LOAD_FAST         'self'
121	LOAD_ATTR         'color'
124	CALL_FUNCTION_1   None
127	POP_TOP           None

128	LOAD_FAST         'rootNode'
131	LOAD_ATTR         'attachNewNode'
134	LOAD_CONST        'changePos'
137	CALL_FUNCTION_1   None
140	STORE_FAST        'change'

143	LOAD_FAST         'doorway'
146	LOAD_ATTR         'reparentTo'
149	LOAD_FAST         'change'
152	CALL_FUNCTION_1   None
155	POP_TOP           None

156	LOAD_FAST         'rootNode'
159	LOAD_FAST         'self'
162	STORE_ATTR        'node'

165	LOAD_FAST         'self'
168	LOAD_ATTR         'node'
171	LOAD_ATTR         'show'
174	CALL_FUNCTION_0   None
177	POP_TOP           None

178	LOAD_FAST         'self'
181	LOAD_ATTR         'locks'
184	LOAD_ATTR         'append'
187	LOAD_GLOBAL       'DistributedDoorEntityLock'
190	LOAD_FAST         'self'

193	LOAD_CONST        0

196	LOAD_FAST         'doorway'
199	LOAD_ATTR         'find'
202	LOAD_CONST        '**/Slide_One_Closed'
205	CALL_FUNCTION_1   None

208	LOAD_FAST         'doorway'
211	LOAD_ATTR         'find'
214	LOAD_CONST        '**/Slide_One_Left_Open'
217	CALL_FUNCTION_1   None

220	LOAD_FAST         'doorway'
223	LOAD_ATTR         'find'
226	LOAD_CONST        '**/Slide_One_Right_Open'
229	CALL_FUNCTION_1   None

232	LOAD_FAST         'self'
235	LOAD_ATTR         'initialLock0StateIndex'
238	CALL_FUNCTION_6   None
241	CALL_FUNCTION_1   None
244	POP_TOP           None

245	LOAD_FAST         'self'
248	LOAD_ATTR         'locks'
251	LOAD_ATTR         'append'
254	LOAD_GLOBAL       'DistributedDoorEntityLock'
257	LOAD_FAST         'self'

260	LOAD_CONST        1

263	LOAD_FAST         'doorway'
266	LOAD_ATTR         'find'
269	LOAD_CONST        '**/Slide_Two_Closed'
272	CALL_FUNCTION_1   None

275	LOAD_FAST         'doorway'
278	LOAD_ATTR         'find'
281	LOAD_CONST        '**/Slide_Two_Left_Open'
284	CALL_FUNCTION_1   None

287	LOAD_FAST         'doorway'
290	LOAD_ATTR         'find'
293	LOAD_CONST        '**/Slide_Two_Right_Open'
296	CALL_FUNCTION_1   None

299	LOAD_FAST         'self'
302	LOAD_ATTR         'initialLock1StateIndex'
305	CALL_FUNCTION_6   None
308	CALL_FUNCTION_1   None
311	POP_TOP           None

312	LOAD_FAST         'self'
315	LOAD_ATTR         'locks'
318	LOAD_ATTR         'append'
321	LOAD_GLOBAL       'DistributedDoorEntityLock'
324	LOAD_FAST         'self'

327	LOAD_CONST        2

330	LOAD_FAST         'doorway'
333	LOAD_ATTR         'find'
336	LOAD_CONST        '**/Slide_Three_Closed'
339	CALL_FUNCTION_1   None

342	LOAD_FAST         'doorway'
345	LOAD_ATTR         'find'
348	LOAD_CONST        '**/Slide_Three_Left_Open'
351	CALL_FUNCTION_1   None

354	LOAD_FAST         'doorway'
357	LOAD_ATTR         'find'
360	LOAD_CONST        '**/Slide_Three_Right_Open'
363	CALL_FUNCTION_1   None

366	LOAD_FAST         'self'
369	LOAD_ATTR         'initialLock2StateIndex'
372	CALL_FUNCTION_6   None
375	CALL_FUNCTION_1   None
378	POP_TOP           None

379	LOAD_FAST         'self'
382	DELETE_ATTR       'initialLock0StateIndex'

385	LOAD_FAST         'self'
388	DELETE_ATTR       'initialLock1StateIndex'

391	LOAD_FAST         'self'
394	DELETE_ATTR       'initialLock2StateIndex'

397	LOAD_FAST         'doorway'
400	LOAD_ATTR         'find'
403	LOAD_CONST        'doortop'
406	CALL_FUNCTION_1   None
409	STORE_FAST        'door'

412	LOAD_FAST         'door'
415	LOAD_ATTR         'isEmpty'
418	CALL_FUNCTION_0   None
421	JUMP_IF_FALSE     '491'

424	LOAD_CONST        'doortop hack'
427	PRINT_ITEM        None
428	PRINT_NEWLINE_CONT None

429	LOAD_FAST         'doorway'
432	LOAD_ATTR         'attachNewNode'
435	LOAD_CONST        'doortop'
438	CALL_FUNCTION_1   None
441	STORE_FAST        'door'

444	LOAD_FAST         'doorway'
447	LOAD_ATTR         'find'
450	LOAD_CONST        'doortop1'
453	CALL_FUNCTION_1   None
456	LOAD_ATTR         'reparentTo'
459	LOAD_FAST         'door'
462	CALL_FUNCTION_1   None
465	POP_TOP           None

466	LOAD_FAST         'doorway'
469	LOAD_ATTR         'find'
472	LOAD_CONST        'doortop2'
475	CALL_FUNCTION_1   None
478	LOAD_ATTR         'reparentTo'
481	LOAD_FAST         'door'
484	CALL_FUNCTION_1   None
487	POP_TOP           None
488	JUMP_FORWARD      '491'
491_0	COME_FROM         '488'

491	LOAD_FAST         'self'
494	LOAD_ATTR         'doorNode'
497	LOAD_ATTR         'attachNewNode'
500	LOAD_FAST         'self'
503	LOAD_ATTR         'getName'
506	CALL_FUNCTION_0   None
509	LOAD_CONST        '-topDoor'
512	BINARY_ADD        None
513	CALL_FUNCTION_1   None
516	STORE_FAST        'rootNode'

519	LOAD_FAST         'rootNode'
522	LOAD_ATTR         'setPos'
525	LOAD_FAST         'self'
528	LOAD_ATTR         'pos'
531	CALL_FUNCTION_1   None
534	POP_TOP           None

535	LOAD_FAST         'rootNode'
538	LOAD_ATTR         'setHpr'
541	LOAD_FAST         'self'
544	LOAD_ATTR         'hpr'
547	CALL_FUNCTION_1   None
550	POP_TOP           None

551	LOAD_FAST         'rootNode'
554	LOAD_ATTR         'setScale'
557	LOAD_FAST         'self'
560	LOAD_ATTR         'scale'
563	CALL_FUNCTION_1   None
566	POP_TOP           None

567	LOAD_FAST         'rootNode'
570	LOAD_ATTR         'setColor'
573	LOAD_FAST         'self'
576	LOAD_ATTR         'color'
579	CALL_FUNCTION_1   None
582	POP_TOP           None

583	LOAD_FAST         'rootNode'
586	LOAD_ATTR         'attachNewNode'
589	LOAD_CONST        'changePos'
592	CALL_FUNCTION_1   None
595	STORE_FAST        'change'

598	LOAD_FAST         'door'
601	LOAD_ATTR         'reparentTo'
604	LOAD_FAST         'change'
607	CALL_FUNCTION_1   None
610	POP_TOP           None

611	LOAD_FAST         'rootNode'
614	LOAD_FAST         'self'
617	STORE_ATTR        'doorTop'

620	LOAD_FAST         'self'
623	LOAD_ATTR         'doorTop'
626	LOAD_ATTR         'show'
629	CALL_FUNCTION_0   None
632	POP_TOP           None

633	LOAD_FAST         'self'
636	LOAD_ATTR         'doorTop'
639	LOAD_ATTR         'getParent'
642	CALL_FUNCTION_0   None
645	LOAD_ATTR         'attachNewNode'
648	LOAD_FAST         'self'
651	LOAD_ATTR         'getName'
654	CALL_FUNCTION_0   None
657	LOAD_CONST        '-leftDoor'
660	BINARY_ADD        None
661	CALL_FUNCTION_1   None
664	STORE_FAST        'rootNode'

667	LOAD_FAST         'rootNode'
670	LOAD_ATTR         'attachNewNode'
673	LOAD_CONST        'change'
676	CALL_FUNCTION_1   None
679	STORE_FAST        'change'

682	LOAD_FAST         'doorway'
685	LOAD_ATTR         'find'
688	LOAD_CONST        '**/doorLeft'
691	CALL_FUNCTION_1   None
694	STORE_FAST        'door'

697	LOAD_FAST         'door'
700	LOAD_ATTR         'reparentTo'
703	LOAD_FAST         'change'
706	CALL_FUNCTION_1   None
709	STORE_FAST        'door'

712	LOAD_FAST         'rootNode'
715	LOAD_FAST         'self'
718	STORE_ATTR        'doorLeft'

721	LOAD_FAST         'self'
724	LOAD_ATTR         'doorLeft'
727	LOAD_ATTR         'show'
730	CALL_FUNCTION_0   None
733	POP_TOP           None

734	LOAD_FAST         'change'
737	LOAD_ATTR         'setPos'
740	LOAD_FAST         'self'
743	LOAD_ATTR         'pos'
746	CALL_FUNCTION_1   None
749	POP_TOP           None

750	LOAD_FAST         'change'
753	LOAD_ATTR         'setHpr'
756	LOAD_FAST         'self'
759	LOAD_ATTR         'hpr'
762	CALL_FUNCTION_1   None
765	POP_TOP           None

766	LOAD_FAST         'change'
769	LOAD_ATTR         'setScale'
772	LOAD_FAST         'self'
775	LOAD_ATTR         'scale'
778	CALL_FUNCTION_1   None
781	POP_TOP           None

782	LOAD_FAST         'change'
785	LOAD_ATTR         'setColor'
788	LOAD_FAST         'self'
791	LOAD_ATTR         'color'
794	CALL_FUNCTION_1   None
797	POP_TOP           None

798	LOAD_FAST         'doorway'
801	LOAD_ATTR         'find'
804	LOAD_CONST        'doorbottom'
807	CALL_FUNCTION_1   None
810	STORE_FAST        'door'

813	LOAD_FAST         'door'
816	LOAD_ATTR         'isEmpty'
819	CALL_FUNCTION_0   None
822	JUMP_IF_FALSE     '892'

825	LOAD_CONST        'doorbottom hack'
828	PRINT_ITEM        None
829	PRINT_NEWLINE_CONT None

830	LOAD_FAST         'doorway'
833	LOAD_ATTR         'attachNewNode'
836	LOAD_CONST        'doorbottom'
839	CALL_FUNCTION_1   None
842	STORE_FAST        'door'

845	LOAD_FAST         'doorway'
848	LOAD_ATTR         'find'
851	LOAD_CONST        'doorbottom1'
854	CALL_FUNCTION_1   None
857	LOAD_ATTR         'reparentTo'
860	LOAD_FAST         'door'
863	CALL_FUNCTION_1   None
866	POP_TOP           None

867	LOAD_FAST         'doorway'
870	LOAD_ATTR         'find'
873	LOAD_CONST        'doorbottom2'
876	CALL_FUNCTION_1   None
879	LOAD_ATTR         'reparentTo'
882	LOAD_FAST         'door'
885	CALL_FUNCTION_1   None
888	POP_TOP           None
889	JUMP_FORWARD      '892'
892_0	COME_FROM         '889'

892	LOAD_GLOBAL       'render'
895	LOAD_ATTR         'attachNewNode'
898	LOAD_CONST        'changePos'
901	CALL_FUNCTION_1   None
904	STORE_FAST        'change'

907	LOAD_FAST         'door'
910	LOAD_ATTR         'reparentTo'
913	LOAD_FAST         'change'
916	CALL_FUNCTION_1   None
919	POP_TOP           None

920	LOAD_FAST         'self'
923	LOAD_ATTR         'doorNode'
926	LOAD_ATTR         'attachNewNode'
929	LOAD_FAST         'self'
932	LOAD_ATTR         'getName'
935	CALL_FUNCTION_0   None
938	LOAD_CONST        '-bottomDoor'
941	BINARY_ADD        None
942	CALL_FUNCTION_1   None
945	STORE_FAST        'rootNode'

948	LOAD_FAST         'rootNode'
951	LOAD_ATTR         'setPos'
954	LOAD_FAST         'self'
957	LOAD_ATTR         'pos'
960	CALL_FUNCTION_1   None
963	POP_TOP           None

964	LOAD_FAST         'rootNode'
967	LOAD_ATTR         'setHpr'
970	LOAD_FAST         'self'
973	LOAD_ATTR         'hpr'
976	CALL_FUNCTION_1   None
979	POP_TOP           None

980	LOAD_FAST         'rootNode'
983	LOAD_ATTR         'setScale'
986	LOAD_FAST         'self'
989	LOAD_ATTR         'scale'
992	CALL_FUNCTION_1   None
995	POP_TOP           None

996	LOAD_FAST         'rootNode'
999	LOAD_ATTR         'setColor'
1002	LOAD_FAST         'self'
1005	LOAD_ATTR         'color'
1008	CALL_FUNCTION_1   None
1011	POP_TOP           None

1012	LOAD_FAST         'change'
1015	LOAD_ATTR         'reparentTo'
1018	LOAD_FAST         'rootNode'
1021	CALL_FUNCTION_1   None
1024	POP_TOP           None

1025	LOAD_FAST         'rootNode'
1028	LOAD_FAST         'self'
1031	STORE_ATTR        'doorBottom'

1034	LOAD_FAST         'self'
1037	LOAD_ATTR         'doorBottom'
1040	LOAD_ATTR         'show'
1043	CALL_FUNCTION_0   None
1046	POP_TOP           None

1047	LOAD_FAST         'self'
1050	LOAD_ATTR         'doorTop'
1053	LOAD_ATTR         'getParent'
1056	CALL_FUNCTION_0   None
1059	LOAD_ATTR         'attachNewNode'
1062	LOAD_FAST         'self'
1065	LOAD_ATTR         'getName'
1068	CALL_FUNCTION_0   None
1071	LOAD_CONST        '-rightDoor'
1074	BINARY_ADD        None
1075	CALL_FUNCTION_1   None
1078	STORE_FAST        'rootNode'

1081	LOAD_FAST         'rootNode'
1084	LOAD_ATTR         'attachNewNode'
1087	LOAD_CONST        'change'
1090	CALL_FUNCTION_1   None
1093	STORE_FAST        'change'

1096	LOAD_FAST         'doorway'
1099	LOAD_ATTR         'find'
1102	LOAD_CONST        '**/doorRight'
1105	CALL_FUNCTION_1   None
1108	STORE_FAST        'door'

1111	LOAD_FAST         'door'
1114	LOAD_ATTR         'reparentTo'
1117	LOAD_FAST         'change'
1120	CALL_FUNCTION_1   None
1123	STORE_FAST        'door'

1126	LOAD_FAST         'rootNode'
1129	LOAD_FAST         'self'
1132	STORE_ATTR        'doorRight'

1135	LOAD_FAST         'self'
1138	LOAD_ATTR         'doorRight'
1141	LOAD_ATTR         'show'
1144	CALL_FUNCTION_0   None
1147	POP_TOP           None

1148	LOAD_FAST         'change'
1151	LOAD_ATTR         'setPos'
1154	LOAD_FAST         'self'
1157	LOAD_ATTR         'pos'
1160	CALL_FUNCTION_1   None
1163	POP_TOP           None

1164	LOAD_FAST         'change'
1167	LOAD_ATTR         'setHpr'
1170	LOAD_FAST         'self'
1173	LOAD_ATTR         'hpr'
1176	CALL_FUNCTION_1   None
1179	POP_TOP           None

1180	LOAD_FAST         'change'
1183	LOAD_ATTR         'setScale'
1186	LOAD_FAST         'self'
1189	LOAD_ATTR         'scale'
1192	CALL_FUNCTION_1   None
1195	POP_TOP           None

1196	LOAD_FAST         'change'
1199	LOAD_ATTR         'setColor'
1202	LOAD_FAST         'self'
1205	LOAD_ATTR         'color'
1208	CALL_FUNCTION_1   None
1211	POP_TOP           None

1212	LOAD_FAST         'self'
1215	LOAD_ATTR         'doorLeft'
1218	LOAD_ATTR         'find'
1221	LOAD_CONST        '**/doorLeft_collision1'
1224	CALL_FUNCTION_1   None
1227	STORE_FAST        'collision'

1230	LOAD_FAST         'collision'
1233	LOAD_ATTR         'setName'
1236	LOAD_FAST         'self'
1239	LOAD_ATTR         'getName'
1242	CALL_FUNCTION_0   None
1245	CALL_FUNCTION_1   None
1248	POP_TOP           None

1249	LOAD_FAST         'self'
1252	LOAD_ATTR         'doorLeft'
1255	LOAD_ATTR         'find'
1258	LOAD_CONST        '**/doorLeft_collision2'
1261	CALL_FUNCTION_1   None
1264	STORE_FAST        'collision'

1267	LOAD_FAST         'collision'
1270	LOAD_ATTR         'setName'
1273	LOAD_FAST         'self'
1276	LOAD_ATTR         'getName'
1279	CALL_FUNCTION_0   None
1282	CALL_FUNCTION_1   None
1285	POP_TOP           None

1286	LOAD_FAST         'self'
1289	LOAD_ATTR         'doorRight'
1292	LOAD_ATTR         'find'
1295	LOAD_CONST        '**/doorRight_collision1'
1298	CALL_FUNCTION_1   None
1301	STORE_FAST        'collision'

1304	LOAD_FAST         'collision'
1307	LOAD_ATTR         'setName'
1310	LOAD_FAST         'self'
1313	LOAD_ATTR         'getName'
1316	CALL_FUNCTION_0   None
1319	CALL_FUNCTION_1   None
1322	POP_TOP           None

1323	LOAD_FAST         'self'
1326	LOAD_ATTR         'doorRight'
1329	LOAD_ATTR         'find'
1332	LOAD_CONST        '**/doorRight_collision2'
1335	CALL_FUNCTION_1   None
1338	STORE_FAST        'collision'

1341	LOAD_FAST         'collision'
1344	LOAD_ATTR         'setName'
1347	LOAD_FAST         'self'
1350	LOAD_ATTR         'getName'
1353	CALL_FUNCTION_0   None
1356	CALL_FUNCTION_1   None
1359	POP_TOP           None

1360	LOAD_FAST         'self'
1363	LOAD_ATTR         'doorLeft'
1366	LOAD_ATTR         'find'
1369	LOAD_CONST        '**/doorLeft_innerCollision'
1372	CALL_FUNCTION_1   None
1375	STORE_FAST        'collision'

1378	LOAD_FAST         'collision'
1381	LOAD_ATTR         'setName'
1384	LOAD_FAST         'self'
1387	LOAD_ATTR         'getName'
1390	CALL_FUNCTION_0   None
1393	CALL_FUNCTION_1   None
1396	POP_TOP           None

1397	LOAD_FAST         'collision'
1400	LOAD_FAST         'self'
1403	STORE_ATTR        'leftInnerCollision'

1406	LOAD_FAST         'self'
1409	LOAD_ATTR         'doorRight'
1412	LOAD_ATTR         'find'
1415	LOAD_CONST        '**/doorRight_innerCollision'
1418	CALL_FUNCTION_1   None
1421	STORE_FAST        'collision'

1424	LOAD_FAST         'collision'
1427	LOAD_ATTR         'setName'
1430	LOAD_FAST         'self'
1433	LOAD_ATTR         'getName'
1436	CALL_FUNCTION_0   None
1439	CALL_FUNCTION_1   None
1442	POP_TOP           None

1443	LOAD_FAST         'collision'
1446	LOAD_FAST         'self'
1449	STORE_ATTR        'rightInnerCollision'
1452	JUMP_FORWARD      '1582'

1455	LOAD_CONST        8.0
1458	STORE_FAST        'radius'

1461	LOAD_GLOBAL       'CollisionSphere'
1464	LOAD_CONST        0.0
1467	LOAD_CONST        0.0
1470	LOAD_CONST        0.0
1473	LOAD_FAST         'radius'
1476	CALL_FUNCTION_4   None
1479	STORE_FAST        'cSphere'

1482	LOAD_FAST         'cSphere'
1485	LOAD_ATTR         'setTangible'
1488	LOAD_CONST        0
1491	CALL_FUNCTION_1   None
1494	POP_TOP           None

1495	LOAD_GLOBAL       'CollisionNode'
1498	LOAD_FAST         'self'
1501	LOAD_ATTR         'getName'
1504	CALL_FUNCTION_0   None
1507	CALL_FUNCTION_1   None
1510	STORE_FAST        'cSphereNode'

1513	LOAD_FAST         'cSphereNode'
1516	LOAD_ATTR         'addSolid'
1519	LOAD_FAST         'cSphere'
1522	CALL_FUNCTION_1   None
1525	POP_TOP           None

1526	LOAD_FAST         'cSphereNode'
1529	LOAD_ATTR         'setFromCollideMask'
1532	LOAD_GLOBAL       'BitMask32'
1535	LOAD_ATTR         'allOff'
1538	CALL_FUNCTION_0   None
1541	CALL_FUNCTION_1   None
1544	POP_TOP           None

1545	LOAD_FAST         'cSphereNode'
1548	LOAD_ATTR         'setIntoCollideMask'
1551	LOAD_GLOBAL       'ToontownGlobals'
1554	LOAD_ATTR         'WallBitmask'
1557	CALL_FUNCTION_1   None
1560	POP_TOP           None

1561	LOAD_FAST         'self'
1564	LOAD_ATTR         'node'
1567	LOAD_ATTR         'attachNewNode'
1570	LOAD_FAST         'cSphereNode'
1573	CALL_FUNCTION_1   None
1576	LOAD_FAST         'self'
1579	STORE_ATTR        'cSphereNodePath'
1582_0	COME_FROM         '1452'

1582	LOAD_FAST         'self'
1585	LOAD_ATTR         'node'
1588	LOAD_ATTR         'flattenMedium'
1591	CALL_FUNCTION_0   None
1594	POP_TOP           None

1595	LOAD_FAST         'self'
1598	LOAD_ATTR         'doorTop'
1601	LOAD_ATTR         'flattenMedium'
1604	CALL_FUNCTION_0   None
1607	POP_TOP           None

1608	LOAD_FAST         'self'
1611	LOAD_ATTR         'doorBottom'
1614	LOAD_ATTR         'flattenMedium'
1617	CALL_FUNCTION_0   None
1620	POP_TOP           None

1621	LOAD_FAST         'self'
1624	LOAD_ATTR         'doorLeft'
1627	LOAD_ATTR         'flattenMedium'
1630	CALL_FUNCTION_0   None
1633	POP_TOP           None

1634	LOAD_FAST         'self'
1637	LOAD_ATTR         'doorRight'
1640	LOAD_ATTR         'flattenMedium'
1643	CALL_FUNCTION_0   None
1646	POP_TOP           None
1647	JUMP_ABSOLUTE     '1653'
1650	JUMP_FORWARD      '1653'
1653_0	COME_FROM         '1650'

1653	LOAD_FAST         'self'
1656	LOAD_ATTR         'setDoorState'
1659	LOAD_FAST         'self'
1662	LOAD_ATTR         'initialState'
1665	LOAD_FAST         'self'
1668	LOAD_ATTR         'initialStateTimestamp'
1671	CALL_FUNCTION_2   None
1674	POP_TOP           None

1675	LOAD_FAST         'self'
1678	DELETE_ATTR       'initialState'

1681	LOAD_FAST         'self'
1684	DELETE_ATTR       'initialStateTimestamp'

Syntax error at or near `JUMP_FORWARD' token at offset 1650

    def setInnerDoorsTrack(self, track):
        if self.innerDoorsTrack is not None:
            self.innerDoorsTrack.pause()
            self.innerDoorsTrack = None
        if track is not None:
            track.start(0.0)
            self.innerDoorsTrack = track
        return

    def openInnerDoors(self):
        print 'openInnerDoors'
        if not self.level.complexVis() or self.isOuterDoorOpen and (not self.isVisBlocker or self.isVisReady):
            print 'openInnerDoors stage Two'
            duration = self.duration
            slideSfx = base.loadSfx('phase_9/audio/sfx/CHQ_FACT_door_open_sliding.mp3')
            finalSfx = base.loadSfx('phase_9/audio/sfx/CHQ_FACT_door_open_final.mp3')
            moveDistance = 8.0
            self.setInnerDoorsTrack(Sequence(Func(self.leftInnerCollision.unstash), Func(self.rightInnerCollision.unstash), Parallel(SoundInterval(slideSfx, node=self.node, duration=duration * 0.4, volume=0.8), LerpPosInterval(nodePath=self.doorLeft, duration=duration * 0.4, pos=Vec3(-moveDistance, 0.0, 0.0), blendType='easeOut'), LerpPosInterval(nodePath=self.doorRight, duration=duration * 0.4, pos=Vec3(moveDistance, 0.0, 0.0), blendType='easeOut'), Sequence(Wait(duration * 0.375), SoundInterval(finalSfx, node=self.node, duration=1.0, volume=0.8))), Func(self.doorLeft.stash), Func(self.doorRight.stash)))

    def closeInnerDoors(self):
        duration = self.duration
        slideSfx = base.loadSfx('phase_9/audio/sfx/CHQ_FACT_door_open_sliding.mp3')
        finalSfx = base.loadSfx('phase_9/audio/sfx/CHQ_FACT_door_open_final.mp3')
        moveDistance = 8.0
        self.setInnerDoorsTrack(Sequence(Func(self.doorLeft.unstash), Func(self.doorRight.unstash), Parallel(SoundInterval(slideSfx, node=self.node, duration=duration * 0.4, volume=0.8), LerpPosInterval(nodePath=self.doorLeft, duration=duration * 0.4, pos=Vec3(0.0), blendType='easeIn'), LerpPosInterval(nodePath=self.doorRight, duration=duration * 0.4, pos=Vec3(0.0), blendType='easeIn'), Sequence(Wait(duration * 0.375), SoundInterval(finalSfx, node=self.node, duration=1.0, volume=0.8))), Func(self.leftInnerCollision.stash), Func(self.rightInnerCollision.stash)))

    def setisOuterDoorOpen(self, isOpen):
        self.isOuterDoorOpen = isOpen

    def enterState1(self):
        print 'doors enter state 1'
        FourState.FourState.enterState1(self)
        self.isOuterDoorOpen = 0
        if self.isVisBlocker:
            if not self.isVisReady:
                self.requestUnblockVis()
        else:
            self.okToUnblockVis()
        duration = self.duration
        slideSfx = base.loadSfx('phase_9/audio/sfx/CHQ_FACT_door_open_sliding.mp3')
        finalSfx = base.loadSfx('phase_9/audio/sfx/CHQ_FACT_door_open_final.mp3')
        moveDistance = 8.0
        self.setTrack(Sequence(Wait(duration * 0.1), Parallel(SoundInterval(slideSfx, node=self.node, duration=duration * 0.4, volume=0.8), LerpPosInterval(nodePath=self.doorTop, duration=duration * 0.4, pos=Vec3(0.0, 0.0, moveDistance), blendType='easeOut'), LerpPosInterval(nodePath=self.doorBottom, duration=duration * 0.4, pos=Vec3(0.0, 0.0, -moveDistance), blendType='easeOut'), Sequence(Wait(duration * 0.375), SoundInterval(finalSfx, node=self.node, duration=1.0, volume=0.8))), Func(self.doorTop.stash), Func(self.doorBottom.stash), Func(self.setisOuterDoorOpen, 1), Func(self.openInnerDoors)))

    def enterState2(self):
        FourState.FourState.enterState2(self)
        self.isOuterDoorOpen = 1
        self.setTrack(None)
        moveDistance = 7.5
        (self.doorTop.setPos(Vec3(0.0, 0.0, moveDistance)),)
        (self.doorBottom.setPos(Vec3(0.0, 0.0, -moveDistance)),)
        self.doorTop.stash()
        self.doorBottom.stash()
        if not self.isVisBlocker or not self.isWaitingForUnblockVis():
            self.setInnerDoorsTrack(None)
            self.doorLeft.setPos(Vec3(-moveDistance, 0.0, 0.0))
            self.doorRight.setPos(Vec3(moveDistance, 0.0, 0.0))
            self.doorLeft.stash()
            self.doorRight.stash()
        return

    def exitState2(self):
        FourState.FourState.exitState2(self)
        self.cancelUnblockVis()

    def enterState3(self):
        FourState.FourState.enterState3(self)
        duration = self.duration
        slideSfx = base.loadSfx('phase_9/audio/sfx/CHQ_FACT_door_open_sliding.mp3')
        finalSfx = base.loadSfx('phase_9/audio/sfx/CHQ_FACT_door_open_final.mp3')
        self.setTrack(Sequence(Wait(duration * 0.1), Func(self.closeInnerDoors), Wait(duration * 0.4), Fun
# Can't uncompyle C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\coghq\DistributedDoorEntity.pyc
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
6	LOAD_CONST        'phase_9/models/cogHQ/CogDoorHandShake'
9	CALL_FUNCTION_1   None
12	STORE_FAST        'model'

15	LOAD_FAST         'model'
18	JUMP_IF_FALSE     '1653'

21	LOAD_FAST         'model'
24	LOAD_ATTR         'find'
27	LOAD_CONST        '**/Doorway1'
30	CALL_FUNCTION_1   None
33	STORE_FAST        'doorway'

36	LOAD_FAST         'self'
39	LOAD_ATTR         'doorNode'
42	LOAD_ATTR         'attachNewNode'
45	LOAD_FAST         'self'
48	LOAD_ATTR         'getName'
51	CALL_FUNCTION_0   None
54	LOAD_CONST        '-root'
57	BINARY_ADD        None
58	CALL_FUNCTION_1   None
61	STORE_FAST        'rootNode'

64	LOAD_FAST         'rootNode'
67	LOAD_ATTR         'setPos'
70	LOAD_FAST         'self'
73	LOAD_ATTR         'pos'
76	CALL_FUNCTION_1   None
79	POP_TOP           None

80	LOAD_FAST         'rootNode'
83	LOAD_ATTR         'setHpr'
86	LOAD_FAST         'self'
89	LOAD_ATTR         'hpr'
92	CALL_FUNCTION_1   None
95	POP_TOP           None

96	LOAD_FAST         'rootNode'
99	LOAD_ATTR         'setScale'
102	LOAD_FAST         'self'
105	LOAD_ATTR         'scale'
108	CALL_FUNCTION_1   None
111	POP_TOP           None

112	LOAD_FAST         'rootNode'
115	LOAD_ATTR         'setColor'
118	LOAD_FAST         'self'
121	LOAD_ATTR         'color'
124	CALL_FUNCTION_1   None
127	POP_TOP           None

128	LOAD_FAST         'rootNode'
131	LOAD_ATTR         'attachNewNode'
134	LOAD_CONST        'changePos'
137	CALL_FUNCTION_1   None
140	STORE_FAST        'change'

143	LOAD_FAST         'doorway'
146	LOAD_ATTR         'reparentTo'
149	LOAD_FAST         'change'
152	CALL_FUNCTION_1   None
155	POP_TOP           None

156	LOAD_FAST         'rootNode'
159	LOAD_FAST         'self'
162	STORE_ATTR        'node'

165	LOAD_FAST         'self'
168	LOAD_ATTR         'node'
171	LOAD_ATTR         'show'
174	CALL_FUNCTION_0   None
177	POP_TOP           None

178	LOAD_FAST         'self'
181	LOAD_ATTR         'locks'
184	LOAD_ATTR         'append'
187	LOAD_GLOBAL       'DistributedDoorEntityLock'
190	LOAD_FAST         'self'

193	LOAD_CONST        0

196	LOAD_FAST         'doorway'
199	LOAD_ATTR         'find'
202	LOAD_CONST        '**/Slide_One_Closed'
205	CALL_FUNCTION_1   None

208	LOAD_FAST         'doorway'
211	LOAD_ATTR         'find'
214	LOAD_CONST        '**/Slide_One_Left_Open'
217	CALL_FUNCTION_1   None

220	LOAD_FAST         'doorway'
223	LOAD_ATTR         'find'
226	LOAD_CONST        '**/Slide_One_Right_Open'
229	CALL_FUNCTION_1   None

232	LOAD_FAST         'self'
235	LOAD_ATTR         'initialLock0StateIndex'
238	CALL_FUNCTION_6   None
241	CALL_FUNCTION_1   None
244	POP_TOP           None

245	LOAD_FAST         'self'
248	LOAD_ATTR         'locks'
251	LOAD_ATTR         'append'
254	LOAD_GLOBAL       'DistributedDoorEntityLock'
257	LOAD_FAST         'self'

260	LOAD_CONST        1

263	LOAD_FAST         'doorway'
266	LOAD_ATTR         'find'
269	LOAD_CONST        '**/Slide_Two_Closed'
272	CALL_FUNCTION_1   None

275	LOAD_FAST         'doorway'
278	LOAD_ATTR         'find'
281	LOAD_CONST        '**/Slide_Two_Left_Open'
284	CALL_FUNCTION_1   None

287	LOAD_FAST         'doorway'
290	LOAD_ATTR         'find'
293	LOAD_CONST        '**/Slide_Two_Right_Open'
296	CALL_FUNCTION_1   None

299	LOAD_FAST         'self'
302	LOAD_ATTR         'initialLock1StateIndex'
305	CALL_FUNCTION_6   None
308	CALL_FUNCTION_1   None
311	POP_TOP           None

312	LOAD_FAST         'self'
315	LOAD_ATTR         'locks'
318	LOAD_ATTR         'append'
321	LOAD_GLOBAL       'DistributedDoorEntityLock'
324	LOAD_FAST         'self'

327	LOAD_CONST        2

330	LOAD_FAST         'doorway'
333	LOAD_ATTR         'find'
336	LOAD_CONST        '**/Slide_Three_Closed'
339	CALL_FUNCTION_1   None

342	LOAD_FAST         'doorway'
345	LOAD_ATTR         'find'
348	LOAD_CONST        '**/Slide_Three_Left_Open'
351	CALL_FUNCTION_1   None

354	LOAD_FAST         'doorway'
357	LOAD_ATTR         'find'
360	LOAD_CONST        '**/Slide_Three_Right_Open'
363	CALL_FUNCTION_1   None

366	LOAD_FAST         'self'
369	LOAD_ATTR         'initialLock2StateIndex'
372	CALL_FUNCTION_6   None
375	CALL_FUNCTION_1   None
378	POP_TOP           None

379	LOAD_FAST         'self'
382	DELETE_ATTR       'initialLock0StateIndex'

385	LOAD_FAST         'self'
388	DELETE_ATTR       'initialLock1StateIndex'

391	LOAD_FAST         'self'
394	DELETE_ATTR       'initialLock2StateIndex'

397	LOAD_FAST         'doorway'
400	LOAD_ATTR         'find'
403	LOAD_CONST        'doortop'
406	CALL_FUNCTION_1   None
409	STORE_FAST        'door'

412	LOAD_FAST         'door'
415	LOAD_ATTR         'isEmpty'
418	CALL_FUNCTION_0   None
421	JUMP_IF_FALSE     '491'

424	LOAD_CONST        'doortop hack'
427	PRINT_ITEM        None
428	PRINT_NEWLINE_CONT None

429	LOAD_FAST         'doorway'
432	LOAD_ATTR         'attachNewNode'
435	LOAD_CONST        'doortop'
438	CALL_FUNCTION_1   None
441	STORE_FAST        'door'

444	LOAD_FAST         'doorway'
447	LOAD_ATTR         'find'
450	LOAD_CONST        'doortop1'
453	CALL_FUNCTION_1   None
456	LOAD_ATTR         'reparentTo'
459	LOAD_FAST         'door'
462	CALL_FUNCTION_1   None
465	POP_TOP           None

466	LOAD_FAST         'doorway'
469	LOAD_ATTR         'find'
472	LOAD_CONST        'doortop2'
475	CALL_FUNCTION_1   None
478	LOAD_ATTR         'reparentTo'
481	LOAD_FAST         'door'
484	CALL_FUNCTION_1   None
487	POP_TOP           None
488	JUMP_FORWARD      '491'
491_0	COME_FROM         '488'

491	LOAD_FAST         'self'
494	LOAD_ATTR         'doorNode'
497	LOAD_ATTR         'attachNewNode'
500	LOAD_FAST         'self'
503	LOAD_ATTR         'getName'
506	CALL_FUNCTION_0   None
509	LOAD_CONST        '-topDoor'
512	BINARY_ADD        None
513	CALL_FUNCTION_1   None
516	STORE_FAST        'rootNode'

519	LOAD_FAST         'rootNode'
522	LOAD_ATTR         'setPos'
525	LOAD_FAST         'self'
528	LOAD_ATTR         'pos'
531	CALL_FUNCTION_1   None
534	POP_TOP           None

535	LOAD_FAST         'rootNode'
538	LOAD_ATTR         'setHpr'
541	LOAD_FAST         'self'
544	LOAD_ATTR         'hpr'
547	CALL_FUNCTION_1   None
550	POP_TOP           None

551	LOAD_FAST         'rootNode'
554	LOAD_ATTR         'setScale'
557	LOAD_FAST         'self'
560	LOAD_ATTR         'scale'
563	CALL_FUNCTION_1   None
566	POP_TOP           None

567	LOAD_FAST         'rootNode'
570	LOAD_ATTR         'setColor'
573	LOAD_FAST         'self'
576	LOAD_ATTR         'color'
579	CALL_FUNCTION_1   None
582	POP_TOP           None

583	LOAD_FAST         'rootNode'
586	LOAD_ATTR         'attachNewNode'
589	LOAD_CONST        'changePos'
592	CALL_FUNCTION_1   None
595	STORE_FAST        'change'

598	LOAD_FAST         'door'
601	LOAD_ATTR         'reparentTo'
604	LOAD_FAST         'change'
607	CALL_FUNCTION_1   None
610	POP_TOP           None

611	LOAD_FAST         'rootNode'
614	LOAD_FAST         'self'
617	STORE_ATTR        'doorTop'

620	LOAD_FAST         'self'
623	LOAD_ATTR         'doorTop'
626	LOAD_ATTR         'show'
629	CALL_FUNCTION_0   None
632	POP_TOP           None

633	LOAD_FAST         'self'
636	LOAD_ATTR         'doorTop'
639	LOAD_ATTR         'getParent'
642	CALL_FUNCTION_0   None
645	LOAD_ATTR         'attachNewNode'
648	LOAD_FAST         'self'
651	LOAD_ATTR         'getName'
654	CALL_FUNCTION_0   None
657	LOAD_CONST        '-leftDoor'
660	BINARY_ADD        None
661	CALL_FUNCTION_1   None
664	STORE_FAST        'rootNode'

667	LOAD_FAST         'rootNode'
670	LOAD_ATTR         'attachNewNode'
673	LOAD_CONST        'change'
676	CALL_FUNCTION_1   None
679	STORE_FAST        'change'

682	LOAD_FAST         'doorway'
685	LOAD_ATTR         'find'
688	LOAD_CONST        '**/doorLeft'
691	CALL_FUNCTION_1   None
694	STORE_FAST        'door'

697	LOAD_FAST         'door'
700	LOAD_ATTR         'reparentTo'
703	LOAD_FAST         'change'
706	CALL_FUNCTION_1   None
709	STORE_FAST        'door'

712	LOAD_FAST         'rootNode'
715	LOAD_FAST         'self'
718	STORE_ATTR        'doorLeft'

721	LOAD_FAST         'self'
724	LOAD_ATTR         'doorLeft'
727	LOAD_ATTR         'show'
730	CALL_FUNCTION_0   None
733	POP_TOP           None

734	LOAD_FAST         'change'
737	LOAD_ATTR         'setPos'
740	LOAD_FAST         'self'
743	LOAD_ATTR         'pos'
746	CALL_FUNCTION_1   None
749	POP_TOP           None

750	LOAD_FAST         'change'
753	LOAD_ATTR         'setHpr'
756	LOAD_FAST         'self'
759	LOAD_ATTR         'hpr'
762	CALL_FUNCTION_1   None
765	POP_TOP           None

766	LOAD_FAST         'change'
769	LOAD_ATTR         'setScale'
772	LOAD_FAST         'self'
775	LOAD_ATTR         'scale'
778	CALL_FUNCTION_1   None
781	POP_TOP           None

782	LOAD_FAST         'change'
785	LOAD_ATTR         'setColor'
788	LOAD_FAST         'self'
791	LOAD_ATTR         'color'
794	CALL_FUNCTION_1   None
797	POP_TOP           None

798	LOAD_FAST         'doorway'
801	LOAD_ATTR         'find'
804	LOAD_CONST        'doorbottom'
807	CALL_FUNCTION_1   None
810	STORE_FAST        'door'

813	LOAD_FAST         'door'
816	LOAD_ATTR         'isEmpty'
819	CALL_FUNCTION_0   None
822	JUMP_IF_FALSE     '892'

825	LOAD_CONST        'doorbottom hack'
828	PRINT_ITEM        None
829	PRINT_NEWLINE_CONT None

830	LOAD_FAST         'doorway'
833	LOAD_ATTR         'attachNewNode'
836	LOAD_CONST        'doorbottom'
839	CALL_FUNCTION_1   None
842	STORE_FAST        'door'

845	LOAD_FAST         'doorway'
848	LOAD_ATTR         'find'
851	LOAD_CONST        'doorbottom1'
854	CALL_FUNCTION_1   None
857	LOAD_ATTR         'reparentTo'
860	LOAD_FAST         'door'
863	CALL_FUNCTION_1   None
866	POP_TOP           None

867	LOAD_FAST         'doorway'
870	LOAD_ATTR         'find'
873	LOAD_CONST        'doorbottom2'
876	CALL_FUNCTION_1   None
879	LOAD_ATTR         'reparentTo'
882	LOAD_FAST         'door'
885	CALL_FUNCTION_1   None
888	POP_TOP           None
889	JUMP_FORWARD      '892'
892_0	COME_FROM         '889'

892	LOAD_GLOBAL       'render'
895	LOAD_ATTR         'attachNewNode'
898	LOAD_CONST        'changePos'
901	CALL_FUNCTION_1   None
904	STORE_FAST        'change'

907	LOAD_FAST         'door'
910	LOAD_ATTR         'reparentTo'
913	LOAD_FAST         'change'
916	CALL_FUNCTION_1   None
919	POP_TOP           None

920	LOAD_FAST         'self'
923	LOAD_ATTR         'doorNode'
926	LOAD_ATTR         'attachNewNode'
929	LOAD_FAST         'self'
932	LOAD_ATTR         'getName'
935	CALL_FUNCTION_0   None
938	LOAD_CONST        '-bottomDoor'
941	BINARY_ADD        None
942	CALL_FUNCTION_1   None
945	STORE_FAST        'rootNode'

948	LOAD_FAST         'rootNode'
951	LOAD_ATTR         'setPos'
954	LOAD_FAST         'self'
957	LOAD_ATTR         'pos'
960	CALL_FUNCTION_1   None
963	POP_TOP           None

964	LOAD_FAST         'rootNode'
967	LOAD_ATTR         'setHpr'
970	LOAD_FAST         'self'
973	LOAD_ATTR         'hpr'
976	CALL_FUNCTION_1   None
979	POP_TOP           None

980	LOAD_FAST         'rootNode'
983	LOAD_ATTR         'setScale'
986	LOAD_FAST         'self'
989	LOAD_ATTR         'scale'
992	CALL_FUNCTION_1   None
995	POP_TOP           None

996	LOAD_FAST         'rootNode'
999	LOAD_ATTR         'setColor'
1002	LOAD_FAST         'self'
1005	LOAD_ATTR         'color'
1008	CALL_FUNCTION_1   None
1011	POP_TOP           None

1012	LOAD_FAST         'change'
1015	LOAD_ATTR         'reparentTo'
1018	LOAD_FAST         'rootNode'
1021	CALL_FUNCTION_1   None
1024	POP_TOP           None

1025	LOAD_FAST         'rootNode'
1028	LOAD_FAST         'self'
1031	STORE_ATTR        'doorBottom'

1034	LOAD_FAST         'self'
1037	LOAD_ATTR         'doorBottom'
1040	LOAD_ATTR         'show'
1043	CALL_FUNCTION_0   None
1046	POP_TOP           None

1047	LOAD_FAST         'self'
1050	LOAD_ATTR         'doorTop'
1053	LOAD_ATTR         'getParent'
1056	CALL_FUNCTION_0   None
1059	LOAD_ATTR         'attachNewNode'
1062	LOAD_FAST         'self'
1065	LOAD_ATTR         'getName'
1068	CALL_FUNCTION_0   None
1071	LOAD_CONST        '-rightDoor'
1074	BINARY_ADD        None
1075	CALL_FUNCTION_1   None
1078	STORE_FAST        'rootNode'

1081	LOAD_FAST         'rootNode'
1084	LOAD_ATTR         'attachNewNode'
1087	LOAD_CONST        'change'
1090	CALL_FUNCTION_1   None
1093	STORE_FAST        'change'

1096	LOAD_FAST         'doorway'
1099	LOAD_ATTR         'find'
1102	LOAD_CONST        '**/doorRight'
1105	CALL_FUNCTION_1   None
1108	STORE_FAST        'door'

1111	LOAD_FAST         'door'
1114	LOAD_ATTR         'reparentTo'
1117	LOAD_FAST         'change'
1120	CALL_FUNCTION_1   None
1123	STORE_FAST        'door'

1126	LOAD_FAST         'rootNode'
1129	LOAD_FAST         'self'
1132	STORE_ATTR        'doorRight'

1135	LOAD_FAST         'self'
1138	LOAD_ATTR         'doorRight'
1141	LOAD_ATTR         'show'
1144	CALL_FUNCTION_0   None
1147	POP_TOP           None

1148	LOAD_FAST         'change'
1151	LOAD_ATTR         'setPos'
1154	LOAD_FAST         'self'
1157	LOAD_ATTR         'pos'
1160	CALL_FUNCTION_1   None
1163	POP_TOP           None

1164	LOAD_FAST         'change'
1167	LOAD_ATTR         'setHpr'
1170	LOAD_FAST         'self'
1173	LOAD_ATTR         'hpr'
1176	CALL_FUNCTION_1   None
1179	POP_TOP           None

1180	LOAD_FAST         'change'
1183	LOAD_ATTR         'setScale'
1186	LOAD_FAST         'self'
1189	LOAD_ATTR         'scale'
1192	CALL_FUNCTION_1   None
1195	POP_TOP           None

1196	LOAD_FAST         'change'
1199	LOAD_ATTR         'setColor'
1202	LOAD_FAST         'self'
1205	LOAD_ATTR         'color'
1208	CALL_FUNCTION_1   None
1211	POP_TOP           None

1212	LOAD_FAST         'self'
1215	LOAD_ATTR         'doorLeft'
1218	LOAD_ATTR         'find'
1221	LOAD_CONST        '**/doorLeft_collision1'
1224	CALL_FUNCTION_1   None
1227	STORE_FAST        'collision'

1230	LOAD_FAST         'collision'
1233	LOAD_ATTR         'setName'
1236	LOAD_FAST         'self'
1239	LOAD_ATTR         'getName'
1242	CALL_FUNCTION_0   None
1245	CALL_FUNCTION_1   None
1248	POP_TOP           None

1249	LOAD_FAST         'self'
1252	LOAD_ATTR         'doorLeft'
1255	LOAD_ATTR         'find'
1258	LOAD_CONST        '**/doorLeft_collision2'
1261	CALL_FUNCTION_1   None
1264	STORE_FAST        'collision'

1267	LOAD_FAST         'collision'
1270	LOAD_ATTR         'setName'
1273	LOAD_FAST         'self'
1276	LOAD_ATTR         'getName'
1279	CALL_FUNCTION_0   None
1282	CALL_FUNCTION_1   None
1285	POP_TOP           None

1286	LOAD_FAST         'self'
1289	LOAD_ATTR         'doorRight'
1292	LOAD_ATTR         'find'
1295	LOAD_CONST        '**/doorRight_collision1'
1298	CALL_FUNCTION_1   None
1301	STORE_FAST        'collision'

1304	LOAD_FAST         'collision'
1307	LOAD_ATTR         'setName'
1310	LOAD_FAST         'self'
1313	LOAD_ATTR         'getName'
1316	CALL_FUNCTION_0   None
1319	CALL_FUNCTION_1   None
1322	POP_TOP           None

1323	LOAD_FAST         'self'
1326	LOAD_ATTR         'doorRight'
1329	LOAD_ATTR         'find'
1332	LOAD_CONST        '**/doorRight_collision2'
1335	CALL_FUNCTION_1   None
1338	STORE_FAST        'collision'

1341	LOAD_FAST         'collision'
1344	LOAD_ATTR         'setName'
1347	LOAD_FAST         'self'
1350	LOAD_ATTR         'getName'
1353	CALL_FUNCTION_0   None
1356	CALL_FUNCTION_1   None
1359	POP_TOP           None

1360	LOAD_FAST         'self'
1363	LOAD_ATTR         'doorLeft'
1366	LOAD_ATTR         'find'
1369	LOAD_CONST        '**/doorLeft_innerCollision'
1372	CALL_FUNCTION_1   None
1375	STORE_FAST        'collision'

1378	LOAD_FAST         'collision'
1381	LOAD_ATTR         'setName'
1384	LOAD_FAST         'self'
1387	LOAD_ATTR         'getName'
1390	CALL_FUNCTION_0   None
1393	CALL_FUNCTION_1   None
1396	POP_TOP           None

1397	LOAD_FAST         'collision'
1400	LOAD_FAST         'self'
1403	STORE_ATTR        'leftInnerCollision'

1406	LOAD_FAST         'self'
1409	LOAD_ATTR         'doorRight'
c(self.doorTop.unstash), Func(self.doorBottom.unstash), Parallel(SoundInterval(slideSfx, node=self.node, duration=duration * 0.4, volume=0.8), LerpPosInterval(nodePath=self.doorTop, duration=duration * 0.4, pos=Vec3(0.0), blendType='easeIn'), LerpPosInterval(nodePath=self.doorBottom, duration=duration * 0.4, pos=Vec3(0.0), blendType='easeIn'), Sequence(Wait(duration * 0.375), SoundInterval(finalSfx, node=self.node, duration=duration * 0.4, volume=0.8))), Func(self.setisOuterDoorOpen, 0)))

    def enterState4(self):
        FourState.FourState.enterState4(self)
        self.setisOuterDoorOpen(0)
        self.isVisReady = 0
        self.setTrack(None)
        self.doorTop.unstash()
        self.doorBottom.unstash()
        self.doorTop.setPos(Vec3(0.0))
        self.doorBottom.setPos(Vec3(0.0))
        self.setInnerDoorsTrack(None)
        self.leftInnerCollision.stash()
        self.rightInnerCollision.stash()
        self.doorLeft.unstash()
        self.doorRight.unstash()
        self.doorLeft.setPos(Vec3(0.0))
        self.doorRight.setPos(Vec3(0.0))
        return

    if __dev__:

        def initWantDoors(self):
            self.accept('wantDoorsChanged', self.onWantDoorsChanged)
            self.onWantDoorsChanged()

        def shutdownWantDoors(self):
            self.ignore('wantDoorsChanged')

        def onWantDoorsChanged(self):
            if self.level.levelMgrEntity.wantDoors:
                self.getNodePath().unstash()
            else:
                self.getNodePath().stash()

        def attribChanged(self, attrib, value):
            self.takedown()
            self.setup()
1412	LOAD_ATTR         'find'
1415	LOAD_CONST        '**/doorRight_innerCollision'
1418	CALL_FUNCTION_1   None
1421	STORE_FAST        'collision'

1424	LOAD_FAST         'collision'
1427	LOAD_ATTR         'setName'
1430	LOAD_FAST         'self'
1433	LOAD_ATTR         'getName'
1436	CALL_FUNCTION_0   None
1439	CALL_FUNCTION_1   None
1442	POP_TOP           None

1443	LOAD_FAST         'collision'
1446	LOAD_FAST         'self'
1449	STORE_ATTR        'rightInnerCollision'
1452	JUMP_FORWARD      '1582'

1455	LOAD_CONST        8.0
1458	STORE_FAST        'radius'

1461	LOAD_GLOBAL       'CollisionSphere'
1464	LOAD_CONST        0.0
1467	LOAD_CONST        0.0
1470	LOAD_CONST        0.0
1473	LOAD_FAST         'radius'
1476	CALL_FUNCTION_4   None
1479	STORE_FAST        'cSphere'

1482	LOAD_FAST         'cSphere'
1485	LOAD_ATTR         'setTangible'
1488	LOAD_CONST        0
1491	CALL_FUNCTION_1   None
1494	POP_TOP           None

1495	LOAD_GLOBAL       'CollisionNode'
1498	LOAD_FAST         'self'
1501	LOAD_ATTR         'getName'
1504	CALL_FUNCTION_0   None
1507	CALL_FUNCTION_1   None
1510	STORE_FAST        'cSphereNode'

1513	LOAD_FAST         'cSphereNode'
1516	LOAD_ATTR         'addSolid'
1519	LOAD_FAST         'cSphere'
1522	CALL_FUNCTION_1   None
1525	POP_TOP           None

1526	LOAD_FAST         'cSphereNode'
1529	LOAD_ATTR         'setFromCollideMask'
1532	LOAD_GLOBAL       'BitMask32'
1535	LOAD_ATTR         'allOff'
1538	CALL_FUNCTION_0   None
1541	CALL_FUNCTION_1   None
1544	POP_TOP           None

1545	LOAD_FAST         'cSphereNode'
1548	LOAD_ATTR         'setIntoCollideMask'
1551	LOAD_GLOBAL       'ToontownGlobals'
1554	LOAD_ATTR         'WallBitmask'
1557	CALL_FUNCTION_1   None
1560	POP_TOP           None

1561	LOAD_FAST         'self'
1564	LOAD_ATTR         'node'
1567	LOAD_ATTR         'attachNewNode'
1570	LOAD_FAST         'cSphereNode'
1573	CALL_FUNCTION_1   None
1576	LOAD_FAST         'self'
1579	STORE_ATTR        'cSphereNodePath'
1582_0	COME_FROM         '1452'

1582	LOAD_FAST         'self'
1585	LOAD_ATTR         'node'
1588	LOAD_ATTR         'flattenMedium'
1591	CALL_FUNCTION_0   None
1594	POP_TOP           None

1595	LOAD_FAST         'self'
1598	LOAD_ATTR         'doorTop'
1601	LOAD_ATTR         'flattenMedium'
1604	CALL_FUNCTION_0   None
1607	POP_TOP           None

1608	LOAD_FAST         'self'
1611	LOAD_ATTR         'doorBottom'
1614	LOAD_ATTR         'flattenMedium'
1617	CALL_FUNCTION_0   None
1620	POP_TOP           None

1621	LOAD_FAST         'self'
1624	LOAD_ATTR         'doorLeft'
1627	LOAD_ATTR         'flattenMedium'
1630	CALL_FUNCTION_0   None
1633	POP_TOP           None

1634	LOAD_FAST         'self'
1637	LOAD_ATTR         'doorRight'
1640	LOAD_ATTR         'flattenMedium'
1643	CALL_FUNCTION_0   None
1646	POP_TOP           None
1647	JUMP_ABSOLUTE     '1653'
1650	JUMP_FORWARD      '1653'
1653_0	COME_FROM         '1650'

1653	LOAD_FAST         'self'
1656	LOAD_ATTR         'setDoorState'
1659	LOAD_FAST         'self'
1662	LOAD_ATTR         'initialState'
1665	LOAD_FAST         'self'
1668	LOAD_ATTR         'initialStateTimestamp'
1671	CALL_FUNCTION_2   None
1674	POP_TOP           None

1675	LOAD_FAST         'self'
1678	DELETE_ATTR       'initialState'

1681	LOAD_FAST         'self'
1684	DELETE_ATTR       'initialStateTimestamp'

Syntax error at or near `JUMP_FORWARD' token at offset 1650

