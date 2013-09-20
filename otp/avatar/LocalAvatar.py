
# Can't uncompyle C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\otp\avatar\LocalAvatar.pyc
Traceback (most recent call last):
  File "C:\python27\lib\uncompyle2\__init__.py", line 206, in main
    uncompyle_file(infile, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 143, in uncompyle_file
    uncompyle(version, co, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 128, in uncompyle
    walk.gen_source(ast, customize)
  File "C:\python27\lib\uncompyle2\walker.py", line 1414, in gen_source
    self.print_(self.traverse(ast, isLambda=isLambda))
  File "C:\python27\lib\uncompyle2\walker.py", line 500, in traverse
    self.preorder(node)
  File "C:\python27\lib\uncompyle2\spark.py", line 694, in preorder
    self.preorder(kid)
  File "C:\python27\lib\uncompyle2\spark.py", line 694, in preorder
    self.preorder(kid)
  File "C:\python27\lib\uncompyle2\spark.py", line 694, in preorder
    self.preorder(kid)
  File "C:\python27\lib\uncompyle2\spark.py", line 687, in preorder
    func(node)
  File "C:\python27\lib\uncompyle2\walker.py", line 976, in n_classdef
    self.build_class(node[2][-2].attr)
  File "C:\python27\lib\uncompyle2\walker.py", line 1373, in build_class
    ast = self.build_ast(code._tokens, code._customize)
  File "C:\python27\lib\uncompyle2\walker.py", line 1444, in build_ast
    raise ParserError(e, tokens)
ParserError: --- This code section failed: ---

0	LOAD_GLOBAL       '__name__'
3	STORE_NAME        '__module__'

6	LOAD_NAME         'DirectNotifyGlobal'
9	LOAD_ATTR         'directNotify'
12	LOAD_ATTR         'newCategory'
15	LOAD_CONST        'LocalAvatar'
18	CALL_FUNCTION_1   None
21	STORE_NAME        'notify'

24	LOAD_NAME         'base'
27	LOAD_ATTR         'config'
30	LOAD_ATTR         'GetBool'
33	LOAD_CONST        'want-dev-camera-positions'
36	LOAD_CONST        0
39	CALL_FUNCTION_2   None
42	STORE_NAME        'wantDevCameraPositions'

45	LOAD_NAME         'base'
48	LOAD_ATTR         'config'
51	LOAD_ATTR         'GetBool'
54	LOAD_CONST        'want-mouse'
57	LOAD_CONST        0
60	CALL_FUNCTION_2   None
63	STORE_NAME        'wantMouse'

66	LOAD_NAME         'base'
69	LOAD_ATTR         'config'
72	LOAD_ATTR         'GetInt'
75	LOAD_CONST        'sleep-timeout'
78	LOAD_CONST        120
81	CALL_FUNCTION_2   None
84	STORE_NAME        'sleepTimeout'

87	LOAD_NAME         'base'
90	LOAD_ATTR         'config'
93	LOAD_ATTR         'GetInt'
96	LOAD_CONST        'afk-timeout'
99	LOAD_CONST        600
102	CALL_FUNCTION_2   None
105	STORE_NAME        'swimTimeout'

108	LOAD_NAME         'base'
111	LOAD_ATTR         'config'
114	LOAD_ATTR         'GetBool'
117	LOAD_CONST        'place-markers'
120	LOAD_CONST        0
123	CALL_FUNCTION_2   None
126	STORE_NAME        '__enableMarkerPlacement'

129	LOAD_NAME         'base'
132	LOAD_ATTR         'config'
135	LOAD_ATTR         'GetBool'
138	LOAD_CONST        'accepting-new-friends'
141	LOAD_CONST        1
144	CALL_FUNCTION_2   None
147	STORE_NAME        'acceptingNewFriends'

150	LOAD_NAME         'base'
153	LOAD_ATTR         'config'
156	LOAD_ATTR         'GetBool'
159	LOAD_CONST        'accepting-non-friend-whispers'
162	LOAD_CONST        0
165	CALL_FUNCTION_2   None
168	STORE_NAME        'acceptingNonFriendWhispers'

171	LOAD_CONST        None
174	LOAD_NAME         'False'
177	LOAD_CONST        '<code_object __init__>'
180	MAKE_FUNCTION_2   None
183	STORE_NAME        '__init__'

186	LOAD_CONST        '<code_object useSwimControls>'
189	MAKE_FUNCTION_0   None
192	STORE_NAME        'useSwimControls'

195	LOAD_CONST        '<code_object useGhostControls>'
198	MAKE_FUNCTION_0   None
201	STORE_NAME        'useGhostControls'

204	LOAD_CONST        '<code_object useWalkControls>'
207	MAKE_FUNCTION_0   None
210	STORE_NAME        'useWalkControls'

213	LOAD_CONST        '<code_object useTwoDControls>'
216	MAKE_FUNCTION_0   None
219	STORE_NAME        'useTwoDControls'

222	LOAD_CONST        '<code_object isLockedDown>'
225	MAKE_FUNCTION_0   None
228	STORE_NAME        'isLockedDown'

231	LOAD_CONST        '<code_object lock>'
234	MAKE_FUNCTION_0   None
237	STORE_NAME        'lock'

240	LOAD_CONST        '<code_object unlock>'
243	MAKE_FUNCTION_0   None
246	STORE_NAME        'unlock'

249	LOAD_CONST        '<code_object isInWater>'
252	MAKE_FUNCTION_0   None
255	STORE_NAME        'isInWater'

258	LOAD_CONST        '<code_object isTeleportAllowed>'
261	MAKE_FUNCTION_0   None
264	STORE_NAME        'isTeleportAllowed'

267	LOAD_CONST        '<code_object setTeleportAllowed>'
270	MAKE_FUNCTION_0   None
273	STORE_NAME        'setTeleportAllowed'

276	LOAD_CONST        '<code_object sendFriendsListEvent>'
279	MAKE_FUNCTION_0   None
282	STORE_NAME        'sendFriendsListEvent'

285	LOAD_CONST        '<code_object delete>'
288	MAKE_FUNCTION_0   None
291	STORE_NAME        'delete'

294	LOAD_CONST        '<code_object shadowReach>'
297	MAKE_FUNCTION_0   None
300	STORE_NAME        'shadowReach'

303	LOAD_CONST        '<code_object wantLegacyLifter>'
306	MAKE_FUNCTION_0   None
309	STORE_NAME        'wantLegacyLifter'

312	LOAD_CONST        1.4
315	LOAD_NAME         'OTPGlobals'
318	LOAD_ATTR         'FloorOffset'
321	LOAD_CONST        4.0
324	LOAD_NAME         'OTPGlobals'
327	LOAD_ATTR         'WallBitmask'
330	LOAD_NAME         'OTPGlobals'
333	LOAD_ATTR         'FloorBitmask'
336	LOAD_NAME         'OTPGlobals'
339	LOAD_ATTR         'GhostBitmask'
342	LOAD_CONST        '<code_object setupControls>'
345	MAKE_FUNCTION_6   None
348	STORE_NAME        'setupControls'

351	LOAD_CONST        '<code_object initializeCollisions>'
354	MAKE_FUNCTION_0   None
357	STORE_NAME        'initializeCollisions'

360	LOAD_CONST        '<code_object deleteCollisions>'
363	MAKE_FUNCTION_0   None
366	STORE_NAME        'deleteCollisions'

369	LOAD_CONST        '<code_object initializeSmartCameraCollisions>'
372	MAKE_FUNCTION_0   None
375	STORE_NAME        'initializeSmartCameraCollisions'

378	LOAD_CONST        '<code_object deleteSmartCameraCollisions>'
381	MAKE_FUNCTION_0   None
384	STORE_NAME        'deleteSmartCameraCollisions'

387	LOAD_CONST        '<code_object collisionsOff>'
390	MAKE_FUNCTION_0   None
393	STORE_NAME        'collisionsOff'

396	LOAD_CONST        '<code_object collisionsOn>'
399	MAKE_FUNCTION_0   None
402	STORE_NAME        'collisionsOn'

405	LOAD_CONST        '<code_object recalcCameraSphere>'
408	MAKE_FUNCTION_0   None
411	STORE_NAME        'recalcCameraSphere'

414	LOAD_CONST        '<code_object putCameraFloorRayOnAvatar>'
417	MAKE_FUNCTION_0   None
420	STORE_NAME        'putCameraFloorRayOnAvatar'

423	LOAD_CONST        '<code_object putCameraFloorRayOnCamera>'
426	MAKE_FUNCTION_0   None
429	STORE_NAME        'putCameraFloorRayOnCamera'

432	LOAD_CONST        '<code_object attachCamera>'
435	MAKE_FUNCTION_0   None
438	STORE_NAME        'attachCamera'

441	LOAD_CONST        '<code_object detachCamera>'
444	MAKE_FUNCTION_0   None
447	STORE_NAME        'detachCamera'

450	LOAD_CONST        '<code_object stopJumpLandTask>'
453	MAKE_FUNCTION_0   None
456	STORE_NAME        'stopJumpLandTask'

459	LOAD_CONST        '<code_object jumpStart>'
462	MAKE_FUNCTION_0   None
465	STORE_NAME        'jumpStart'

468	LOAD_CONST        '<code_object returnToWalk>'
471	MAKE_FUNCTION_0   None
474	STORE_NAME        'returnToWalk'

477	LOAD_CONST        '<code_object jumpLandAnimFix>'
480	MAKE_FUNCTION_0   None
483	STORE_NAME        'jumpLandAnimFix'

486	LOAD_CONST        '<code_object jumpHardLand>'
489	MAKE_FUNCTION_0   None
492	STORE_NAME        'jumpHardLand'

495	LOAD_CONST        '<code_object jumpLand>'
498	MAKE_FUNCTION_0   None
501	STORE_NAME        'jumpLand'
504	JUMP_FORWARD      '507'
507_0	COME_FROM         '504'

507	LOAD_CONST        '<code_object setupAnimationEvents>'
510	MAKE_FUNCTION_0   None
513	STORE_NAME        'setupAnimationEvents'

516	LOAD_CONST        '<code_object ignoreAnimationEvents>'
519	MAKE_FUNCTION_0   None
522	STORE_NAME        'ignoreAnimationEvents'

525	LOAD_CONST        '<code_object allowHardLand>'
528	MAKE_FUNCTION_0   None
531	STORE_NAME        'allowHardLand'

534	LOAD_CONST        '<code_object enableSmartCameraViews>'
537	MAKE_FUNCTION_0   None
540	STORE_NAME        'enableSmartCameraViews'

543	LOAD_CONST        '<code_object disableSmartCameraViews>'
546	MAKE_FUNCTION_0   None
549	STORE_NAME        'disableSmartCameraViews'

552	LOAD_CONST        '<code_object enableAvatarControls>'
555	MAKE_FUNCTION_0   None
558	STORE_NAME        'enableAvatarControls'

561	LOAD_CONST        '<code_object disableAvatarControls>'
564	MAKE_FUNCTION_0   None
567	STORE_NAME        'disableAvatarControls'

570	LOAD_CONST        '<code_object setWalkSpeedNormal>'
573	MAKE_FUNCTION_0   None
576	STORE_NAME        'setWalkSpeedNormal'

579	LOAD_CONST        '<code_object setWalkSpeedSlow>'
582	MAKE_FUNCTION_0   None
585	STORE_NAME        'setWalkSpeedSlow'

588	LOAD_CONST        '<code_object pageUp>'
591	MAKE_FUNCTION_0   None
594	STORE_NAME        'pageUp'

597	LOAD_CONST        '<code_object pageDown>'
600	MAKE_FUNCTION_0   None
603	STORE_NAME        'pageDown'

606	LOAD_CONST        '<code_object clearPageUpDown>'
609	MAKE_FUNCTION_0   None
612	STORE_NAME        'clearPageUpDown'

615	LOAD_CONST        '<code_object nextCameraPos>'
618	MAKE_FUNCTION_0   None
621	STORE_NAME        'nextCameraPos'

624	LOAD_CONST        '<code_object initCameraPositions>'
627	MAKE_FUNCTION_0   None
630	STORE_NAME        'initCameraPositions'

633	LOAD_CONST        None
636	LOAD_CONST        '<code_object addCameraPosition>'
639	MAKE_FUNCTION_1   None
642	STORE_NAME        'addCameraPosition'

645	LOAD_CONST        '<code_object resetCameraPosition>'
648	MAKE_FUNCTION_0   None
651	STORE_NAME        'resetCameraPosition'

654	LOAD_CONST        '<code_object removeCameraPosition>'
657	MAKE_FUNCTION_0   None
660	STORE_NAME        'removeCameraPosition'

663	LOAD_CONST        '<code_object printCameraPositions>'
666	MAKE_FUNCTION_0   None
669	STORE_NAME        'printCameraPositions'

672	LOAD_CONST        '<code_object printCameraPosition>'
675	MAKE_FUNCTION_0   None
678	STORE_NAME        'printCameraPosition'

681	LOAD_CONST        '<code_object posCamera>'
684	MAKE_FUNCTION_0   None
687	STORE_NAME        'posCamera'

690	LOAD_CONST        '<code_object getClampedAvatarHeight>'
693	MAKE_FUNCTION_0   None
696	STORE_NAME        'getClampedAvatarHeight'

699	LOAD_CONST        '<code_object getVisibilityPoint>'
702	MAKE_FUNCTION_0   None
705	STORE_NAME        'getVisibilityPoint'

708	LOAD_CONST        '<code_object setLookAtPoint>'
711	MAKE_FUNCTION_0   None
714	STORE_NAME        'setLookAtPoint'

717	LOAD_CONST        '<code_object getLookAtPoint>'
720	MAKE_FUNCTION_0   None
723	STORE_NAME        'getLookAtPoint'

726	LOAD_CONST        '<code_object setIdealCameraPos>'
729	MAKE_FUNCTION_0   None
732	STORE_NAME        'setIdealCameraPos'

735	LOAD_CONST        '<code_object getIdealCameraPos>'
738	MAKE_FUNCTION_0   None
741	STORE_NAME        'getIdealCameraPos'

744	LOAD_CONST        '<code_object setCameraPositionByIndex>'
747	MAKE_FUNCTION_0   None
750	STORE_NAME        'setCameraPositionByIndex'

753	LOAD_CONST        '<code_object setCameraPosForPetInteraction>'
756	MAKE_FUNCTION_0   None
759	STORE_NAME        'setCameraPosForPetInteraction'

762	LOAD_CONST        '<code_object unsetCameraPosForPetInteraction>'
765	MAKE_FUNCTION_0   None
768	STORE_NAME        'unsetCameraPosForPetInteraction'

771	LOAD_CONST        '<code_object setCameraSettings>'
774	MAKE_FUNCTION_0   None
777	STORE_NAME        'setCameraSettings'

780	LOAD_CONST        '<code_object getCompromiseCameraPos>'
783	MAKE_FUNCTION_0   None
786	STORE_NAME        'getCompromiseCameraPos'

789	LOAD_CONST        '<code_object updateSmartCameraCollisionLineSegment>'
792	MAKE_FUNCTION_0   None
795	STORE_NAME        'updateSmartCameraCollisionLineSegment'

798	LOAD_CONST        '<code_object initializeSmartCamera>'
801	MAKE_FUNCTION_0   None
804	STORE_NAME        'initializeSmartCamera'

807	LOAD_CONST        '<code_object shutdownSmartCamera>'
810	MAKE_FUNCTION_0   None
813	STORE_NAME        'shutdownSmartCamera'

816	LOAD_CONST        '<code_object setOnLevelGround>'
819	MAKE_FUNCTION_0   None
822	STORE_NAME        'setOnLevelGround'

825	LOAD_CONST        '<code_object setCameraCollisionsCanMove>'
828	MAKE_FUNCTION_0   None
831	STORE_NAME        'setCameraCollisionsCanMove'

834	LOAD_CONST        '<code_object setGeom>'
837	MAKE_FUNCTION_0   None
840	STORE_NAME        'setGeom'

843	LOAD_CONST        1
846	LOAD_CONST        '<code_object startUpdateSmartCamera>'
849	MAKE_FUNCTION_1   None
852	STORE_NAME        'startUpdateSmartCamera'

855	LOAD_CONST        '<code_object stopUpdateSmartCamera>'
858	MAKE_FUNCTION_0   None
861	STORE_NAME        'stopUpdateSmartCamera'

864	LOAD_CONST        '<code_object updateSmartCamera>'
867	MAKE_FUNCTION_0   None
870	STORE_NAME        'updateSmartCamera'

873	LOAD_CONST        '<code_object positionCameraWithPusher>'
876	MAKE_FUNCTION_0   None
879	STORE_NAME        'positionCameraWithPusher'

882	LOAD_CONST        '<code_object nudgeCamera>'
885	MAKE_FUNCTION_0   None
888	STORE_NAME        'nudgeCamera'

891	LOAD_CONST        '<code_object popCameraToDest>'
894	MAKE_FUNCTION_0   None
897	STORE_NAME        'popCameraToDest'

900	LOAD_CONST        '<code_object handleCameraObstruction>'
903	MAKE_FUNCTION_0   None
906	STORE_NAME        'handleCameraObstruction'

909	LOAD_CONST        '<code_object handleCameraFloorInteraction>'
912	MAKE_FUNCTION_0   None
915	STORE_NAME        'handleCameraFloorInteraction'

918	LOAD_CONST        '<code_object lerpCameraFov>'
921	MAKE_FUNCTION_0   None
924	STORE_NAME        'lerpCameraFov'

927	LOAD_CONST        '<code_object setCameraFov>'
930	MAKE_FUNCTION_0   None
933	STORE_NAME        'setCameraFov'

936	LOAD_CONST        3
939	LOAD_CONST        '<code_object gotoNode>'
942	MAKE_FUNCTION_1   None
945	STORE_NAME        'gotoNode'

948	LOAD_CONST        '<code_object setCustomMessages>'
951	MAKE_FUNCTION_0   None
954	STORE_NAME        'setCustomMessages'

957	LOAD_CONST        '<code_object displayWhisper>'
960	MAKE_FUNCTION_0   None
963	STORE_NAME        'displayWhisper'

966	LOAD_CONST        '<code_object displayWhisperPlayer>'
969	MAKE_FUNCTION_0   None
972	STORE_NAME        'displayWhisperPlayer'

975	LOAD_CONST        '<code_object setAnimMultiplier>'
978	MAKE_FUNCTION_0   None
981	STORE_NAME        'setAnimMultiplier'

984	LOAD_CONST        '<code_object getAnimMultiplier>'
987	MAKE_FUNCTION_0   None
990	STORE_NAME        'getAnimMultiplier'

993	LOAD_CONST        '<code_object enableRun>'
996	MAKE_FUNCTION_0   None
999	STORE_NAME        'enableRun'

1002	LOAD_CONST        '<code_object disableRun>'
1005	MAKE_FUNCTION_0   None
1008	STORE_NAME        'disableRun'

1011	LOAD_CONST        '<code_object startRunWatch>'
1014	MAKE_FUNCTION_0   None
1017	STORE_NAME        'startRunWatch'

1020	LOAD_CONST        '<code_object stopRunWatch>'
1023	MAKE_FUNCTION_0   None
1026	STORE_NAME        'stopRunWatch'

1029	LOAD_CONST        '<code_object runSound>'
1032	MAKE_FUNCTION_0   None
1035	STORE_NAME        'runSound'

1038	LOAD_CONST        '<code_object walkSound>'
1041	MAKE_FUNCTION_0   None
1044	STORE_NAME        'walkSound'

1047	LOAD_CONST        '<code_object stopSound>'
1050	MAKE_FUNCTION_0   None
1053	STORE_NAME        'stopSound'

1056	LOAD_CONST        '<code_object wakeUp>'
1059	MAKE_FUNCTION_0   None
1062	STORE_NAME        'wakeUp'

1065	LOAD_CONST        '<code_object gotoSleep>'
1068	MAKE_FUNCTION_0   None
1071	STORE_NAME        'gotoSleep'

1074	LOAD_CONST        '<code_object forceGotoSleep>'
1077	MAKE_FUNCTION_0   None
1080	STORE_NAME        'forceGotoSleep'

1083	LOAD_CONST        '<code_object startSleepWatch>'
1086	MAKE_FUNCTION_0   None
1089	STORE_NAME        'startSleepWatch'

1092	LOAD_CONST        '<code_object stopSleepWatch>'
1095	MAKE_FUNCTION_0   None
1098	STORE_NAME        'stopSleepWatch'

1101	LOAD_CONST        '<code_object startSleepSwimTest>'
1104	MAKE_FUNCTION_0   None
1107	STORE_NAME        'startSleepSwimTest'

1110	LOAD_CONST        '<code_object stopSleepSwimTest>'
1113	MAKE_FUNCTION_0   None
1116	STORE_NAME        'stopSleepSwimTest'

1119	LOAD_CONST        '<code_object sleepSwimTest>'
1122# 2013.08.22 22:15:11 Pacific Daylight Time
# Embedded file name: otp.avatar.LocalAvatar
# decompiled 0 files: 0 okay, 1 failed, 0 verify failed
# 2013.08.22 22:15:11 Pacific Daylight Time
	MAKE_FUNCTION_0   None
1125	STORE_NAME        'sleepSwimTest'

1128	LOAD_CONST        '<code_object swimTimeoutAction>'
1131	MAKE_FUNCTION_0   None
1134	STORE_NAME        'swimTimeoutAction'

1137	LOAD_CONST        '<code_object trackAnimToSpeed>'
1140	MAKE_FUNCTION_0   None
1143	STORE_NAME        'trackAnimToSpeed'

1146	LOAD_CONST        '<code_object hasTrackAnimToSpeed>'
1149	MAKE_FUNCTION_0   None
1152	STORE_NAME        'hasTrackAnimToSpeed'

1155	LOAD_CONST        '<code_object startTrackAnimToSpeed>'
1158	MAKE_FUNCTION_0   None
1161	STORE_NAME        'startTrackAnimToSpeed'

1164	LOAD_CONST        '<code_object stopTrackAnimToSpeed>'
1167	MAKE_FUNCTION_0   None
1170	STORE_NAME        'stopTrackAnimToSpeed'

1173	LOAD_CONST        '<code_object startChat>'
1176	MAKE_FUNCTION_0   None
1179	STORE_NAME        'startChat'

1182	LOAD_CONST        '<code_object stopChat>'
1185	MAKE_FUNCTION_0   None
1188	STORE_NAME        'stopChat'

1191	LOAD_CONST        '<code_object printCamPos>'
1194	MAKE_FUNCTION_0   None
1197	STORE_NAME        'printCamPos'

1200	LOAD_CONST        '<code_object d_broadcastPositionNow>'
1203	MAKE_FUNCTION_0   None
1206	STORE_NAME        'd_broadcastPositionNow'

1209	LOAD_CONST        None
1212	LOAD_CONST        '<code_object travCollisionsLOS>'
1215	MAKE_FUNCTION_1   None
1218	STORE_NAME        'travCollisionsLOS'

1221	LOAD_CONST        None
1224	LOAD_CONST        '<code_object travCollisionsFloor>'
1227	MAKE_FUNCTION_1   None
1230	STORE_NAME        'travCollisionsFloor'

1233	LOAD_CONST        None
1236	LOAD_CONST        '<code_object travCollisionsPusher>'
1239	MAKE_FUNCTION_1   None
1242	STORE_NAME        'travCollisionsPusher'

1245	LOAD_CONST        0
1248	LOAD_CONST        0
1251	LOAD_CONST        '<code_object __friendOnline>'
1254	MAKE_FUNCTION_2   None
1257	STORE_NAME        '__friendOnline'

1260	LOAD_CONST        '<code_object __friendOffline>'
1263	MAKE_FUNCTION_0   None
1266	STORE_NAME        '__friendOffline'

1269	LOAD_CONST        '<code_object __playerOnline>'
1272	MAKE_FUNCTION_0   None
1275	STORE_NAME        '__playerOnline'

1278	LOAD_CONST        '<code_object __playerOffline>'
1281	MAKE_FUNCTION_0   None
1284	STORE_NAME        '__playerOffline'

1287	LOAD_CONST        None
1290	LOAD_CONST        '<code_object clickedWhisper>'
1293	MAKE_FUNCTION_1   None
1296	STORE_NAME        'clickedWhisper'

1299	LOAD_CONST        '<code_object d_setParent>'
1302	MAKE_FUNCTION_0   None
1305	STORE_NAME        'd_setParent'

1308	LOAD_CONST        '<code_object handlePlayerFriendWhisper>'
1311	MAKE_FUNCTION_0   None
1314	STORE_NAME        'handlePlayerFriendWhisper'

1317	LOAD_CONST        '<code_object canChat>'
1320	MAKE_FUNCTION_0   None
1323	STORE_NAME        'canChat'
1326	LOAD_LOCALS       None
1327	RETURN_VALUE      None
-1	RETURN_LAST       None

Syntax error at or near `COME_FROM' token at offset 507_0

