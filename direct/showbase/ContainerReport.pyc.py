# 2013.08.22 22:14:32 Pacific Daylight Time
# Embedded file name: direct.showbase.ContainerReport
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.showbase.PythonUtil import Queue, fastRepr, invertDictLossless
from direct.showbase.PythonUtil import itype, safeRepr
from direct.showbase.Job import Job
import types

class ContainerReport(Job):
    __module__ = __name__
    notify = directNotify.newCategory('ContainerReport')
    PrivateIds = set()

    def __init__(self, name, log = False, limit = None, threaded = False):
        Job.__init__(self, name)
        self._log = log
        self._limit = limit
        self._visitedIds = set()
        self._id2pathStr = {}
        self._id2container = {}
        self._type2id2len = {}
        self._instanceDictIds = set()
        self._queue = Queue()
        jobMgr.add(self)
        if threaded == False:
            jobMgr.finish(self)

    def destroy(self):
        del self._queue
        del self._instanceDictIds
        del self._type2id2len
        del self._id2container
        del self._id2pathStr
        del self._visitedIds
        del self._limit
        del self._log

    def finished(self):
        if self._log:
            self.destroy()

    def run--- This code section failed: ---

0	LOAD_GLOBAL       'ContainerReport'
3	LOAD_ATTR         'PrivateIds'
6	LOAD_ATTR         'update'
9	LOAD_GLOBAL       'set'
12	LOAD_GLOBAL       'id'
15	LOAD_GLOBAL       'ContainerReport'
18	LOAD_ATTR         'PrivateIds'
21	CALL_FUNCTION_1   None
24	LOAD_GLOBAL       'id'
27	LOAD_FAST         'self'
30	LOAD_ATTR         '_visitedIds'
33	CALL_FUNCTION_1   None
36	LOAD_GLOBAL       'id'
39	LOAD_FAST         'self'
42	LOAD_ATTR         '_id2pathStr'
45	CALL_FUNCTION_1   None
48	LOAD_GLOBAL       'id'
51	LOAD_FAST         'self'
54	LOAD_ATTR         '_id2container'
57	CALL_FUNCTION_1   None
60	LOAD_GLOBAL       'id'
63	LOAD_FAST         'self'
66	LOAD_ATTR         '_type2id2len'
69	CALL_FUNCTION_1   None
72	LOAD_GLOBAL       'id'
75	LOAD_FAST         'self'
78	LOAD_ATTR         '_queue'
81	CALL_FUNCTION_1   None
84	LOAD_GLOBAL       'id'
87	LOAD_FAST         'self'
90	LOAD_ATTR         '_instanceDictIds'
93	CALL_FUNCTION_1   None
96	BUILD_LIST_7      None
99	CALL_FUNCTION_1   None
102	CALL_FUNCTION_1   None
105	POP_TOP           None

106	SETUP_EXCEPT      '117'

109	LOAD_GLOBAL       'base'
112	POP_TOP           None
113	POP_BLOCK         None
114	JUMP_FORWARD      '124'
117_0	COME_FROM         '106'

117	POP_TOP           None
118	POP_TOP           None
119	POP_TOP           None

120	JUMP_FORWARD      '143'
123	END_FINALLY       None
124_0	COME_FROM         '114'

124	LOAD_FAST         'self'
127	LOAD_ATTR         '_enqueueContainer'
130	LOAD_GLOBAL       'base'
133	LOAD_ATTR         '__dict__'

136	LOAD_CONST        'base'
139	CALL_FUNCTION_2   None
142	POP_TOP           None
143_0	COME_FROM         '123'

143	SETUP_EXCEPT      '154'

146	LOAD_GLOBAL       'simbase'
149	POP_TOP           None
150	POP_BLOCK         None
151	JUMP_FORWARD      '161'
154_0	COME_FROM         '143'

154	POP_TOP           None
155	POP_TOP           None
156	POP_TOP           None

157	JUMP_FORWARD      '180'
160	END_FINALLY       None
161_0	COME_FROM         '151'

161	LOAD_FAST         'self'
164	LOAD_ATTR         '_enqueueContainer'
167	LOAD_GLOBAL       'simbase'
170	LOAD_ATTR         '__dict__'

173	LOAD_CONST        'simbase'
176	CALL_FUNCTION_2   None
179	POP_TOP           None
180_0	COME_FROM         '160'

180	LOAD_FAST         'self'
183	LOAD_ATTR         '_queue'
186	LOAD_ATTR         'push'
189	LOAD_GLOBAL       '__builtins__'
192	CALL_FUNCTION_1   None
195	POP_TOP           None

196	LOAD_CONST        ''
199	LOAD_FAST         'self'
202	LOAD_ATTR         '_id2pathStr'
205	LOAD_GLOBAL       'id'
208	LOAD_GLOBAL       '__builtins__'
211	CALL_FUNCTION_1   None
214	STORE_SUBSCR      None

215	SETUP_LOOP        '1346'
218	LOAD_GLOBAL       'len'
221	LOAD_FAST         'self'
224	LOAD_ATTR         '_queue'
227	CALL_FUNCTION_1   None
230	LOAD_CONST        0
233	COMPARE_OP        '>'
236	JUMP_IF_FALSE     '1345'

239	LOAD_CONST        None
242	YIELD_VALUE       None

243	LOAD_FAST         'self'
246	LOAD_ATTR         '_queue'
249	LOAD_ATTR         'pop'
252	CALL_FUNCTION_0   None
255	STORE_FAST        'parentObj'

258	LOAD_GLOBAL       'False'
261	STORE_FAST        'isInstanceDict'

264	LOAD_GLOBAL       'id'
267	LOAD_FAST         'parentObj'
270	CALL_FUNCTION_1   None
273	LOAD_FAST         'self'
276	LOAD_ATTR         '_instanceDictIds'
279	COMPARE_OP        'in'
282	JUMP_IF_FALSE     '294'

285	LOAD_GLOBAL       'True'
288	STORE_FAST        'isInstanceDict'
291	JUMP_FORWARD      '294'
294_0	COME_FROM         '291'

294	SETUP_EXCEPT      '325'

297	LOAD_FAST         'parentObj'
300	LOAD_ATTR         '__class__'
303	LOAD_ATTR         '__name__'
306	LOAD_CONST        'method-wrapper'
309	COMPARE_OP        '=='
312	JUMP_IF_FALSE     '321'

315	CONTINUE_LOOP     '218'
318	JUMP_FORWARD      '321'
321_0	COME_FROM         '318'
321	POP_BLOCK         None
322	JUMP_FORWARD      '332'
325_0	COME_FROM         '294'

325	POP_TOP           None
326	POP_TOP           None
327	POP_TOP           None

328	JUMP_FORWARD      '332'
331	END_FINALLY       None
332_0	COME_FROM         '322'
332_1	COME_FROM         '331'

332	LOAD_GLOBAL       'type'
335	LOAD_FAST         'parentObj'
338	CALL_FUNCTION_1   None
341	LOAD_GLOBAL       'types'
344	LOAD_ATTR         'StringType'
347	LOAD_GLOBAL       'types'
350	LOAD_ATTR         'UnicodeType'
353	BUILD_TUPLE_2     None
356	COMPARE_OP        'in'
359	JUMP_IF_FALSE     '368'

362	CONTINUE          '218'
365	JUMP_FORWARD      '368'
368_0	COME_FROM         '365'

368	LOAD_GLOBAL       'type'
371	LOAD_FAST         'parentObj'
374	CALL_FUNCTION_1   None
377	LOAD_GLOBAL       'types'
380	LOAD_ATTR         'ModuleType'
383	LOAD_GLOBAL       'types'
386	LOAD_ATTR         'InstanceType'
389	BUILD_TUPLE_2     None
392	COMPARE_OP        'in'
395	JUMP_IF_FALSE     '491'

398	LOAD_FAST         'parentObj'
401	LOAD_ATTR         '__dict__'
404	STORE_FAST        'child'

407	LOAD_FAST         'self'
410	LOAD_ATTR         '_examine'
413	LOAD_FAST         'child'
416	CALL_FUNCTION_1   None
419	JUMP_IF_FALSE     '485'

422	LOAD_FAST         'self'
425	LOAD_ATTR         '_instanceDictIds'
428	LOAD_ATTR         'add'
431	LOAD_GLOBAL       'id'
434	LOAD_FAST         'child'
437	CALL_FUNCTION_1   None
440	CALL_FUNCTION_1   None
443	POP_TOP           None

444	LOAD_GLOBAL       'str'
447	LOAD_FAST         'self'
450	LOAD_ATTR         '_id2pathStr'
453	LOAD_GLOBAL       'id'
456	LOAD_FAST         'parentObj'
459	CALL_FUNCTION_1   None
462	BINARY_SUBSCR     None
463	CALL_FUNCTION_1   None
466	LOAD_FAST         'self'
469	LOAD_ATTR         '_id2pathStr'
472	LOAD_GLOBAL       'id'
475	LOAD_FAST         'child'
478	CALL_FUNCTION_1   None
481	STORE_SUBSCR      None
482	JUMP_BACK         '218'

485	CONTINUE          '218'
488	JUMP_FORWARD      '491'
491_0	COME_FROM         '488'

491	LOAD_GLOBAL       'type'
494	LOAD_FAST         'parentObj'
497	CALL_FUNCTION_1   None
500	LOAD_GLOBAL       'types'
503	LOAD_ATTR         'DictType'
506	COMPARE_OP        'is'
509	JUMP_IF_FALSE     '914'

512	LOAD_CONST        None
515	STORE_FAST        'key'

518	LOAD_CONST        None
521	STORE_FAST        'attr'

524	LOAD_FAST         'parentObj'
527	LOAD_ATTR         'keys'
530	CALL_FUNCTION_0   None
533	STORE_FAST        'keys'

536	SETUP_EXCEPT      '553'

539	LOAD_FAST         'keys'
542	LOAD_ATTR         'sort'
545	CALL_FUNCTION_0   None
548	POP_TOP           None
549	POP_BLOCK         None
550	JUMP_FORWARD      '617'
553_0	COME_FROM         '536'

553	DUP_TOP           None
554	LOAD_GLOBAL       'TypeError'
557	COMPARE_OP        'exception match'
560	JUMP_IF_FALSE     '616'
563	POP_TOP           None
564	STORE_FAST        'e'
567	POP_TOP           None

568	LOAD_FAST         'self'
571	LOAD_ATTR         'notify'
574	LOAD_ATTR         'warning'
577	LOAD_CONST        'non-sortable dict keys: %s: %s'
580	LOAD_FAST         'self'
583	LOAD_ATTR         '_id2pathStr'
586	LOAD_GLOBAL       'id'
589	LOAD_FAST         'parentObj'
592	CALL_FUNCTION_1   None
595	BINARY_SUBSCR     None
596	LOAD_GLOBAL       'repr'
599	LOAD_FAST         'e'
602	CALL_FUNCTION_1   None
605	BUILD_TUPLE_2     None
608	BINARY_MODULO     None
609	CALL_FUNCTION_1   None
612	POP_TOP           None
613	JUMP_FORWARD      '617'
616	END_FINALLY       None
617_0	COME_FROM         '550'
617_1	COME_FROM         '616'

617	SETUP_LOOP        '902'
620	LOAD_FAST         'keys'
623	GET_ITER          None
624	FOR_ITER          '901'
627	STORE_FAST        'key'

630	SETUP_EXCEPT      '647'

633	LOAD_FAST         'parentObj'
636	LOAD_FAST         'key'
639	BINARY_SUBSCR     None
640	STORE_FAST        'attr'
643	POP_BLOCK         None
644	JUMP_FORWARD      '705'
647_0	COME_FROM         '630'

647	DUP_TOP           None
648	LOAD_GLOBAL       'KeyError'
651	COMPARE_OP        'exception match'
654	JUMP_IF_FALSE     '704'
657	POP_TOP           None
658	STORE_FAST        'e'
661	POP_TOP           None

662	LOAD_FAST         'self'
665	LOAD_ATTR         'notify'
668	LOAD_ATTR         'warning'
671	LOAD_CONST        'could not index into %s with key %s'
674	LOAD_FAST         'self'
677	LOAD_ATTR         '_id2pathStr'
680	LOAD_GLOBAL       'id'
683	LOAD_FAST         'parentObj'
686	CALL_FUNCTION_1   None
689	BINARY_SUBSCR     None
690	LOAD_FAST         'key'
693	BUILD_TUPLE_2     None
696	BINARY_MODULO     None
697	CALL_FUNCTION_1   None
700	POP_TOP           None
701	JUMP_FORWARD      '705'
704	END_FINALLY       None
705_0	COME_FROM         '644'
705_1	COME_FROM         '704'

705	LOAD_GLOBAL       'id'
708	LOAD_FAST         'attr'
711	CALL_FUNCTION_1   None
714	LOAD_FAST         'self'
717	LOAD_ATTR         '_visitedIds'
720	COMPARE_OP        'not in'
723	JUMP_IF_FALSE     '898'

726	LOAD_FAST         'self'
729	LOAD_ATTR         '_visitedIds'
732	LOAD_ATTR         'add'
735	LOAD_GLOBAL       'id'
738	LOAD_FAST         'attr'
741	CALL_FUNCTION_1   None
744	CALL_FUNCTION_1   None
747	POP_TOP           None

748	LOAD_FAST         'self'
751	LOAD_ATTR         '_examine'
754	LOAD_FAST         'attr'
757	CALL_FUNCTION_1   None
760	JUMP_IF_FALSE     '895'

763	LOAD_FAST         'parentObj'
766	LOAD_GLOBAL       '__builtins__'
769	COMPARE_OP        'is'
772	JUMP_IF_FALSE     '797'

775	LOAD_FAST         'key'
778	LOAD_FAST         'self'
781	LOAD_ATTR         '_id2pathStr'
784	LOAD_GLOBAL       'id'
787	LOAD_FAST         'attr'
790	CALL_FUNCTION_1   None
793	STORE_SUBSCR      None
794	JUMP_ABSOLUTE     '895'

797	LOAD_FAST         'isInstanceDict'
800	JUMP_IF_FALSE     '846'

803	LOAD_FAST         'self'
806	LOAD_ATTR         '_id2pathStr'
809	LOAD_GLOBAL       'id'
812	LOAD_FAST         'parentObj'
815	CALL_FUNCTION_1   None
818	BINARY_SUBSCR     None
819	LOAD_CONST        '.%s'
822	LOAD_FAST         'key'
825	BINARY_MODULO     None
826	BINARY_ADD        None
827	LOAD_FAST         'self'
830	LOAD_ATTR         '_id2pathStr'
833	LOAD_GLOBAL       'id'
836	LOAD_FAST         'attr'
839	CALL_FUNCTION_1   None
842	STORE_SUBSCR      None
843	JUMP_ABSOLUTE     '895'

846	LOAD_FAST         'self'
849	LOAD_ATTR         '_id2pathStr'
852	LOAD_GLOBAL       'id'
855	LOAD_FAST         'parentObj'
858	CALL_FUNCTION_1   None
861	BINARY_SUBSCR     None
862	LOAD_CONST        '[%s]'
865	LOAD_GLOBAL       'safeRepr'
868	LOAD_FAST         'key'
871	CALL_FUNCTION_1   None
874	BINARY_MODULO     None
875	BINARY_ADD        None
876	LOAD_FAST         'self'
879	LOAD_ATTR         '_id2pathStr'
882	LOAD_GLOBAL       'id'
885	LOAD_FAST         'attr'
888	CALL_FUNCTION_1   None
891	STORE_SUBSCR      None
892	JUMP_ABSOLUTE     '898'
895	JUMP_BACK         '624'
898	JUMP_BACK         '624'
901	POP_BLOCK         None
902_0	COME_FROM         '617'

902	DELETE_FAST       'key'

905	DELETE_FAST       'attr'

908	CONTINUE          '218'
911	JUMP_FORWARD      '914'
914_0	COME_FROM         '911'

914	LOAD_GLOBAL       'type'
917	LOAD_FAST         'parentObj'
920	CALL_FUNCTION_1   None
923	LOAD_GLOBAL       'types'
926	LOAD_ATTR         'FileType'
929	COMPARE_OP        'is not'
932	JUMP_IF_FALSE     '1159'

935	SETUP_EXCEPT      '954'

938	LOAD_GLOBAL       'iter'
941	LOAD_FAST         'parentObj'
944	CALL_FUNCTION_1   None
947	STORE_FAST        'itr'
950	POP_BLOCK         None
951	JUMP_FORWARD      '961'
954_0	COME_FROM         '935'

954	POP_TOP           None
955	POP_TOP           None
956	POP_TOP           None

957	JUMP_ABSOLUTE     '1159'
960	END_FINALLY       None
961_0	COME_FROM         '951'

961	SETUP_EXCEPT      '1131'

964	LOAD_CONST        0
967	STORE_FAST        'index'

970	SETUP_LOOP        '1124'

973	SETUP_EXCEPT      '992'

976	LOAD_FAST         'itr'
979	LOAD_ATTR         'next'
982	CALL_FUNCTION_0   None
985	STORE_FAST        'attr'
988	POP_BLOCK         None
989	JUMP_FORWARD      '1006'
992_0	COME_FROM         '973'

992	POP_TOP           None
993	POP_TOP           None
994	POP_TOP           None

995	LOAD_CONST        None
998	STORE_FAST        'attr'

1001	BREAK_LOOP        None
1002	JUMP_FORWARD      '1006'
1005	END_FINALLY       None
1006_0	COME_FROM         '989'
1006_1	COME_FROM         '1005'

1006	LOAD_GLOBAL       'id'
1009	LOAD_FAST         'attr'
1012	CALL_FUNCTION_1   None
1015	LOAD_FAST         'self'
1018	LOAD_ATTR         '_visitedIds'
1021	COMPARE_OP        'not in'
1024	JUMP_IF_FALSE     '1110'

1027	LOAD_FAST         'self'
1030	LOAD_ATTR         '_visitedIds'
1033	LOAD_ATTR         'add'
1036	LOAD_GLOBAL       'id'
1039	LOAD_FAST         'attr'
1042	CALL_FUNCTION_1   None
1045	CALL_FUNCTION_1   None
1048	POP_TOP           None

1049	LOAD_FAST         'self'
1052	LOAD_ATTR         '_examine'
1055	LOAD_FAST         'attr'
1058	CALL_FUNCTION_1   None
1061	JUMP_IF_FALSE     '1107'

1064	LOAD_FAST         'self'
1067	LOAD_ATTR         '_id2pathStr'
1070	LOAD_GLOBAL       'id'
1073	LOAD_FAST         'parentObj'
1076	CALL_FUNCTION_1   None
1079	BINARY_SUBSCR     None
1080	LOAD_CONST        '[%s]'
1083	LOAD_FAST         'index'
1086	BINARY_MODULO     None
1087	BINARY_ADD        None
1088	LOAD_FAST         'self'
1091	LOAD_ATTR         '_id2pathStr'
1094	LOAD_GLOBAL       'id'
1097	LOAD_FAST         'attr'
1100	CALL_FUNCTION_1   None
1103	STORE_SUBSCR      None
1104	JUMP_ABSOLUTE     '1110'
1107	JUMP_FORWARD      '1110'
1110_0	COME_FROM         '1107'

1110	LOAD_FAST         'index'
1113	LOAD_CONST        1
1116	INPLACE_ADD       None
1117	STORE_FAST        'index'
1120	JUMP_BACK         '973'
1123	POP_BLOCK         None
1124_0	COME_FROM         '970'

1124	DELETE_FAST       'attr'
1127	POP_BLOCK         None
1128	JUMP_FORWARD      '1150'
1131_0	COME_FROM         '961'

1131	DUP_TOP           None
1132	LOAD_GLOBAL       'StopIteration'
1135	COMPARE_OP        'exception match'
1138	JUMP_IF_FALSE     '1149'
1141	POP_TOP           None
1142	STORE_FAST        'e'
1145	POP_TOP           None

1146	JUMP_FORWARD      '1150'
1149	END_FINALLY       None
1150_0	COME_FROM         '1128'
1150_1	COME_FROM         '1149'

1150	DELETE_FAST       'itr'

1153	CONTINUE          '218'
1156_0	COME_FROM         '960'
1156	JUMP_FORWARD      '1159'
1159_0	COME_FROM         '1156'

1159	SETUP_EXCEPT      '1178'

1162	LOAD_GLOBAL       'dir'
1165	LOAD_FAST         'parentObj'
1168	CALL_FUNCTION_1   None
1171	STORE_FAST        'childNames'
1174	POP_BLOCK         None
1175	JUMP_FORWARD      '1185'
1178_0	COME_FROM         '1159'

1178	POP_TOP           None
1179	POP_TOP           None
1180	POP_TOP           None

1181	JUMP_BACK         '218'
1184	END_FINALLY       None
1185_0	COME_FROM         '1175'

1185	LOAD_CONST        None
1188	STORE_FAST        'childName'

1191	LOAD_CONST        None
1194	STORE_FAST        'child'

1197	SETUP_LOOP        '1333'
1200	LOAD_FAST         'childNames'
1203	GET_ITER          None
1204	FOR_ITER          '1332'
1207	STORE_FAST        'childName'

1210	LOAD_GLOBAL       'getattr'
1213	LOAD_FAST         'parentObj'
1216	LOAD_FAST         'childName'
1219	CALL_FUNCTION_2   None
1222	STORE_FAST        'child'

1225	LOAD_GLOBAL       'id'
1228	LOAD_FAST         'child'
1231	CALL_FUNCTION_1   None
1234	LOAD_FAST         'self'
1237	LOAD_ATTR         '_visitedIds'
1240	COMPARE_OP        'not in'
1243	JUMP_IF_FALSE     '1329'

1246	LOAD_FAST         'self'
1249	LOAD_ATTR         '_visitedIds'
1252	LOAD_ATTR         'add'
1255	LOAD_GLOBAL       'id'
1258	LOAD_FAST         'child'
1261	CALL_FUNCTION_1   None
1264	CALL_FUNCTION_1   None
1267	POP_TOP           None

1268	LOAD_FAST         'self'
1271	LOAD_ATTR         '_examine'
1274	LOAD_FAST         'child'
1277	CALL_FUNCTION_1   None
1280	JUMP_IF_FALSE     '1326'

1283	LOAD_FAST         'self'
1286	LOAD_ATTR         '_id2pathStr'
1289	LOAD_GLOBAL       'id'
1292	LOAD_FAST         'parentObj'
1295	CALL_FUNCTION_1   None
1298	BINARY_SUBSCR     None
1299	LOAD_CONST        '.%s'
1302	LOAD_FAST         'childName'
1305	BINARY_MODULO     None
1306	BINARY_ADD        None
1307	LOAD_FAST         'self'
1310	LOAD_ATTR         '_id2pathStr'
1313	LOAD_GLOBAL       'id'
1316	LOAD_FAST         'child'
1319	CALL_FUNCTION_1   None
1322	STORE_SUBSCR      None
1323	JUMP_ABSOLUTE     '1329'
1326	JUMP_BACK         '1204'
1329	JUMP_BACK         '1204'
1332	POP_BLOCK         None
1333_0	COME_FROM         '1197'

1333	DELETE_FAST       'childName'

1336	DELETE_FAST       'child'

1339	CONTINUE          '218'
1342_0	COME_FROM         '1184'
1342	JUMP_BACK         '218'
1345	POP_BLOCK         None
1346_0	COME_FROM         '215'

1346	LOAD_FAST         'self'
1349	LOAD_ATTR         '_log'
1352	JUMP_IF_FALSE     '1414'

1355	LOAD_FAST         'self'
1358	LOAD_ATTR         'printingBegin'
1361	CALL_FUNCTION_0   None
1364	POP_TOP           None

1365	SETUP_LOOP        '1401'
1368	LOAD_FAST         'self'
1371	LOAD_ATTR         '_output'
1374	LOAD_CONST        'limit'
1377	LOAD_FAST         'self'
1380	LOAD_ATTR         '_limit'
1383	CALL_FUNCTION_256 None
1386	GET_ITER          None
1387	FOR_ITER          '1400'
1390	STORE_FAST        'i'

1393	LOAD_CONST        None
1396	YIELD_VALUE       None
1397	JUMP_BACK         '1387'
1400	POP_BLOCK         None
1401_0	COME_FROM         '1365'

1401	LOAD_FAST         'self'
1404	LOAD_ATTR         'printingEnd'
1407	CALL_FUNCTION_0   None
1410	POP_TOP           None
1411	JUMP_FORWARD      '1414'
1414_0	COME_FROM         '1411'

1414	LOAD_GLOBAL       'Job'
1417	LOAD_ATTR         'Done'
1420	YIELD_VALUE       None
1421	LOAD_CONST        None
1424	RETURN_VALUE      None

Syntax error at or near `STORE_FAST' token at offset 255

    def _enqueueContainer(self, obj, pathStr = None):
        self._queue.push(obj)
        objId = id(obj)
        if pathStr is not None:
            self._id2pathStr[objId] = pathStr
        try:
            length = len(obj)
        except:
            length = None

        if length is not None and length > 0:
            self._id2container[objId] = obj
            self._type2id2len.setdefault(type(obj), {})
            self._type2id2len[type(obj)][objId] = length
        return

    def _examine(self, obj):
        if type(obj) in (types.BooleanType,
         types.BuiltinFunctionType,
         types.BuiltinMethodType,
         types.ComplexType,
         types.FloatType,
         types.IntType,
         types.LongType,
         types.NoneType,
         types.NotImplementedType,
         types.TypeType,
         types.CodeType,
         types.FunctionType):
            return False
        if id(obj) in ContainerReport.PrivateIds:
            return False
        self._enqueueContainer(obj)
        return True

    def _outputType--- This code section failed: ---

0	LOAD_FAST         'type'
3	LOAD_FAST         'self'
6	LOAD_ATTR         '_type2id2len'
9	COMPARE_OP        'not in'
12	JUMP_IF_FALSE     '22'

15	LOAD_CONST        None
18	RETURN_VALUE      None
19	JUMP_FORWARD      '22'
22_0	COME_FROM         '19'

22	LOAD_GLOBAL       'invertDictLossless'
25	LOAD_FAST         'self'
28	LOAD_ATTR         '_type2id2len'
31	LOAD_FAST         'type'
34	BINARY_SUBSCR     None
35	CALL_FUNCTION_1   None
38	STORE_FAST        'len2ids'

41	LOAD_FAST         'len2ids'
44	LOAD_ATTR         'keys'
47	CALL_FUNCTION_0   None
50	STORE_FAST        'lengths'

53	LOAD_FAST         'lengths'
56	LOAD_ATTR         'sort'
59	CALL_FUNCTION_0   None
62	POP_TOP           None

63	LOAD_FAST         'lengths'
66	LOAD_ATTR         'reverse'
69	CALL_FUNCTION_0   None
72	POP_TOP           None

73	LOAD_CONST        '====='
76	PRINT_ITEM        None
77	PRINT_NEWLINE_CONT None

78	LOAD_CONST        '===== %s'
81	LOAD_FAST         'type'
84	BINARY_MODULO     None
85	PRINT_ITEM        None
86	PRINT_NEWLINE_CONT None

87	LOAD_CONST        0
90	STORE_FAST        'count'

93	LOAD_GLOBAL       'False'
96	STORE_FAST        'stop'

99	SETUP_LOOP        '285'
102	LOAD_FAST         'lengths'
105	GET_ITER          None
106	FOR_ITER          '284'
109	STORE_FAST        'l'

112	LOAD_GLOBAL       'list'
115	CALL_FUNCTION_0   None
118	STORE_FAST        'pathStrList'

121	SETUP_LOOP        '208'
124	LOAD_FAST         'len2ids'
127	LOAD_FAST         'l'
130	BINARY_SUBSCR     None
131	GET_ITER          None
132	FOR_ITER          '207'
135	STORE_FAST        'id'

138	LOAD_FAST         'self'
141	LOAD_ATTR         '_id2container'
144	LOAD_FAST         'id'
147	BINARY_SUBSCR     None
148	STORE_FAST        'obj'

151	LOAD_FAST         'pathStrList'
154	LOAD_ATTR         'append'
157	LOAD_FAST         'self'
160	LOAD_ATTR         '_id2pathStr'
163	LOAD_FAST         'id'
166	BINARY_SUBSCR     None
167	CALL_FUNCTION_1   None
170	POP_TOP           None

171	LOAD_FAST         'count'
174	LOAD_CONST        1
177	INPLACE_ADD       None
178	STORE_FAST        'count'

181	LOAD_FAST         'count'
184	LOAD_CONST        127
187	BINARY_AND        None
188	LOAD_CONST        0
191	COMPARE_OP        '=='
194	JUMP_IF_FALSE     '204'

197	LOAD_CONST        None
200	YIELD_VALUE       None
201	JUMP_BACK         '132'
204	JUMP_BACK         '132'
207	POP_BLOCK         None
208_0	COME_FROM         '121'

208	LOAD_FAST         'pathStrList'
211	LOAD_ATTR         'sort'
214	CALL_FUNCTION_0   None
217	POP_TOP           None

218	SETUP_LOOP        '250'
221	LOAD_FAST         'pathStrList'
224	GET_ITER          None
225	FOR_ITER          '249'
228	STORE_FAST        'pathstr'

231	LOAD_CONST        '%s: %s'
234	LOAD_FAST         'l'
237	LOAD_FAST         'pathstr'
240	BUILD_TUPLE_2     None
243	BINARY_MODULO     None
244	PRINT_ITEM        None
245	PRINT_NEWLINE_CONT None
246	JUMP_BACK         '225'
249	POP_BLOCK         None
250_0	COME_FROM         '218'

250	LOAD_FAST         'limit'
253	LOAD_CONST        None
256	COMPARE_OP        'is not'
259	JUMP_IF_FALSE     '281'
262	LOAD_FAST         'count'
265	LOAD_FAST         'limit'
268	COMPARE_OP        '>='
271_0	COME_FROM         '259'
271	JUMP_IF_FALSE     '281'

274	LOAD_CONST        None
277	RETURN_VALUE      None
278	JUMP_BACK         '106'
281	JUMP_BACK         '106'
284	POP_BLOCK         None
285_0	COME_FROM         '99'
285	LOAD_CONST        None
288	RETURN_VALUE      None

Syntax error at or near `JUMP_BACK' token at offset 204

    def _output--- This code section failed: ---

0	LOAD_CONST        "===== ContainerReport: '%s' ====="
3	LOAD_FAST         'self'
6	LOAD_ATTR         '_name'
9	BUILD_TUPLE_1     None
12	BINARY_MODULO     None
13	PRINT_ITEM        None
14	PRINT_NEWLINE_CONT None

15	LOAD_GLOBAL       'types'
18	LOAD_ATTR         'DictType'
21	LOAD_GLOBAL       'types'
24	LOAD_ATTR         'ListType'
27	LOAD_GLOBAL       'types'
30	LOAD_ATTR         'TupleType'
33	BUILD_TUPLE_3     None
36	STORE_FAST        'initialTypes'

39	SETUP_LOOP        '89'
42	LOAD_FAST         'initialTypes'
45	GET_ITER          None
46	FOR_ITER          '88'
49	STORE_FAST        'type'

52	SETUP_LOOP        '85'
55	LOAD_FAST         'self'
58	LOAD_ATTR         '_outputType'
61	LOAD_FAST         'type'
64	LOAD_FAST         'kArgs'
67	CALL_FUNCTION_KW_1 None
70	GET_ITER          None
71	FOR_ITER          '84'
74	STORE_FAST        'i'

77	LOAD_CONST        None
80	YIELD_VALUE       None
81	JUMP_BACK         '71'
84	POP_BLOCK         None
85_0	COME_FROM         '52'
85	JUMP_BACK         '46'
88	POP_BLOCK         None
89_0	COME_FROM         '39'

89	LOAD_GLOBAL       'list'
92	LOAD_GLOBAL       'set'
95	LOAD_FAST         'self'
98	LOAD_ATTR         '_type2id2len'
101	LOAD_ATTR         'keys'
104	CALL_FUNCTION_0   None
107	CALL_FUNCTION_1   None
110	LOAD_ATTR         'difference'
113	LOAD_GLOBAL       'set'
116	LOAD_FAST         'initialTypes'
119	CALL_FUNCTION_1   None
122	CALL_FUNCTION_1   None
125	CALL_FUNCTION_1   None
128	STORE_FAST        'otherTypes'

131	LOAD_FAST         'otherTypes'
134	LOAD_ATTR         'sort'
137	CALL_FUNCTION_0   None
140	POP_TOP           None

141	SETUP_LOOP        '191'
144	LOAD_FAST         'otherTypes'
147	GET_ITER          None
148	FOR_ITER          '190'
151	STORE_FAST        'type'

154	SETUP_LOOP        '187'
157	LOAD_FAST         'self'
160	LOAD_ATTR         '_outputType'
163	LOAD_FAST         'type'
166	LOAD_FAST         'kArgs'
169	CALL_FUNCTION_KW_1 None
172	GET_ITER          None
173	FOR_ITER          '186'
176	STORE_FAST        'i'

179	LOAD_CONST        None
182	YIELD_VALUE       None
183	JUMP_BACK         '173'
186	POP_BLOCK         None
187_0	COME_FROM         '154'
187	JUMP_BACK         '148'
190	POP_BLOCK         None
191_0	COME_FROM         '141'
191	LOAD_CONST        None
194	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 84

    def log(self, **kArgs):
        self._output(**kArgs)# decompiled 0 files: 0 okay, 1 failed, 0 verify failed
# 2013.08.22 22:14:32 Pacific Daylight Time

# Can't uncompyle C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\showbase\ContainerReport.pyc
Traceback (most recent call last):
  File "C:\python27\lib\uncompyle2\__init__.py", line 206, in main
    uncompyle_file(infile, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 143, in uncompyle_file
    uncompyle(version, co, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 132, in uncompyle
    raise walk.ERROR
ParserError: --- This code section failed: ---

0	LOAD_CONST        "===== ContainerReport: '%s' ====="
3	LOAD_FAST         'self'
6	LOAD_ATTR         '_name'
9	BUILD_TUPLE_1     None
12	BINARY_MODULO     None
13	PRINT_ITEM        None
14	PRINT_NEWLINE_CONT None

15	LOAD_GLOBAL       'types'
18	LOAD_ATTR         'DictType'
21	LOAD_GLOBAL       'types'
24	LOAD_ATTR         'ListType'
27	LOAD_GLOBAL       'types'
30	LOAD_ATTR         'TupleType'
33	BUILD_TUPLE_3     None
36	STORE_FAST        'initialTypes'

39	SETUP_LOOP        '89'
42	LOAD_FAST         'initialTypes'
45	GET_ITER          None
46	FOR_ITER          '88'
49	STORE_FAST        'type'

52	SETUP_LOOP        '85'
55	LOAD_FAST         'self'
58	LOAD_ATTR         '_outputType'
61	LOAD_FAST         'type'
64	LOAD_FAST         'kArgs'
67	CALL_FUNCTION_KW_1 None
70	GET_ITER          None
71	FOR_ITER          '84'
74	STORE_FAST        'i'

77	LOAD_CONST        None
80	YIELD_VALUE       None
81	JUMP_BACK         '71'
84	POP_BLOCK         None
85_0	COME_FROM         '52'
85	JUMP_BACK         '46'
88	POP_BLOCK         None
89_0	COME_FROM         '39'

89	LOAD_GLOBAL       'list'
92	LOAD_GLOBAL       'set'
95	LOAD_FAST         'self'
98	LOAD_ATTR         '_type2id2len'
101	LOAD_ATTR         'keys'
104	CALL_FUNCTION_0   None
107	CALL_FUNCTION_1   None
110	LOAD_ATTR         'difference'
113	LOAD_GLOBAL       'set'
116	LOAD_FAST         'initialTypes'
119	CALL_FUNCTION_1   None
122	CALL_FUNCTION_1   None
125	CALL_FUNCTION_1   None
128	STORE_FAST        'otherTypes'

131	LOAD_FAST         'otherTypes'
134	LOAD_ATTR         'sort'
137	CALL_FUNCTION_0   None
140	POP_TOP           None

141	SETUP_LOOP        '191'
144	LOAD_FAST         'otherTypes'
147	GET_ITER          None
148	FOR_ITER          '190'
151	STORE_FAST        'type'

154	SETUP_LOOP        '187'
157	LOAD_FAST         'self'
160	LOAD_ATTR         '_outputType'
163	LOAD_FAST         'type'
166	LOAD_FAST         'kArgs'
169	CALL_FUNCTION_KW_1 None
172	GET_ITER          None
173	FOR_ITER          '186'
176	STORE_FAST        'i'

179	LOAD_CONST        None
182	YIELD_VALUE       None
183	JUMP_BACK         '173'
186	POP_BLOCK         None
187_0	COME_FROM         '154'
187	JUMP_BACK         '148'
190	POP_BLOCK         None
191_0	COME_FROM         '141'
191	LOAD_CONST        None
194	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 84

