# 2013.08.22 22:14:35 Pacific Daylight Time
# Embedded file name: direct.showbase.GarbageReport
__all__ = ['FakeObject',
 '_createGarbage',
 'GarbageReport',
 'GarbageLogger']
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.showbase.PythonUtil import safeRepr, fastRepr, printListEnumGen, printNumberedTypesGen
from direct.showbase.PythonUtil import AlphabetCounter
from direct.showbase.Job import Job
import gc
import types
GarbageCycleCountAnnounceEvent = 'announceGarbageCycleDesc2num'

class FakeObject():
    __module__ = __name__


class FakeDelObject():
    __module__ = __name__

    def __del__(self):
        pass


def _createGarbage(num = 1):
    for i in xrange(num):
        a = FakeObject()
        b = FakeObject()
        a.other = b
        b.other = a
        a = FakeDelObject()
        b = FakeDelObject()
        a.other = b
        b.other = a


class GarbageReport(Job):
    __module__ = __name__
    notify = directNotify.newCategory('GarbageReport')

    def __init__(self, name, log = True, verbose = False, fullReport = False, findCycles = True, threaded = False, doneCallback = None, autoDestroy = False, priority = None, safeMode = False, delOnly = False, collect = True):
        Job.__init__(self, name)
        self._args = ScratchPad(name=name, log=log, verbose=verbose, fullReport=fullReport, findCycles=findCycles, doneCallback=doneCallback, autoDestroy=autoDestroy, safeMode=safeMode, delOnly=delOnly, collect=collect)
        if priority is not None:
            self.setPriority(priority)
        jobMgr.add(self)
        if not threaded:
            jobMgr.finish(self)
        return

    def run--- This code section failed: ---

0	LOAD_GLOBAL       'gc'
3	LOAD_ATTR         'get_debug'
6	CALL_FUNCTION_0   None
9	STORE_FAST        'oldFlags'

12	LOAD_FAST         'self'
15	LOAD_ATTR         '_args'
18	LOAD_ATTR         'delOnly'
21	JUMP_IF_FALSE     '253'

24	LOAD_GLOBAL       'gc'
27	LOAD_ATTR         'set_debug'
30	LOAD_CONST        0
33	CALL_FUNCTION_1   None
36	POP_TOP           None

37	LOAD_FAST         'self'
40	LOAD_ATTR         '_args'
43	LOAD_ATTR         'collect'
46	JUMP_IF_FALSE     '62'

49	LOAD_GLOBAL       'gc'
52	LOAD_ATTR         'collect'
55	CALL_FUNCTION_0   None
58	POP_TOP           None
59	JUMP_FORWARD      '62'
62_0	COME_FROM         '59'

62	LOAD_GLOBAL       'gc'
65	LOAD_ATTR         'garbage'
68	SLICE+0           None
69	STORE_FAST        'garbageInstances'

72	LOAD_GLOBAL       'gc'
75	LOAD_ATTR         'garbage'
78	DELETE_SLICE+0    None

79	LOAD_GLOBAL       'len'
82	LOAD_FAST         'garbageInstances'
85	CALL_FUNCTION_1   None
88	LOAD_CONST        0
91	COMPARE_OP        '>'
94	JUMP_IF_FALSE     '104'

97	LOAD_CONST        None
100	YIELD_VALUE       None
101	JUMP_FORWARD      '104'
104_0	COME_FROM         '101'

104	LOAD_FAST         'self'
107	LOAD_ATTR         'notify'
110	LOAD_ATTR         'getDebug'
113	CALL_FUNCTION_0   None
116	JUMP_IF_FALSE     '148'

119	LOAD_FAST         'self'
122	LOAD_ATTR         'notify'
125	LOAD_ATTR         'debug'
128	LOAD_CONST        'garbageInstances == %s'
131	LOAD_GLOBAL       'fastRepr'
134	LOAD_FAST         'garbageInstances'
137	CALL_FUNCTION_1   None
140	BINARY_MODULO     None
141	CALL_FUNCTION_1   None
144	POP_TOP           None
145	JUMP_FORWARD      '148'
148_0	COME_FROM         '145'

148	LOAD_GLOBAL       'len'
151	LOAD_FAST         'garbageInstances'
154	CALL_FUNCTION_1   None
157	LOAD_FAST         'self'
160	STORE_ATTR        'numGarbageInstances'

163	LOAD_GLOBAL       'set'
166	CALL_FUNCTION_0   None
169	LOAD_FAST         'self'
172	STORE_ATTR        'garbageInstanceIds'

175	SETUP_LOOP        '247'
178	LOAD_GLOBAL       'xrange'
181	LOAD_GLOBAL       'len'
184	LOAD_FAST         'garbageInstances'
187	CALL_FUNCTION_1   None
190	CALL_FUNCTION_1   None
193	GET_ITER          None
194	FOR_ITER          '246'
197	STORE_FAST        'i'

200	LOAD_FAST         'self'
203	LOAD_ATTR         'garbageInstanceIds'
206	LOAD_ATTR         'add'
209	LOAD_GLOBAL       'id'
212	LOAD_FAST         'garbageInstances'
215	LOAD_FAST         'i'
218	BINARY_SUBSCR     None
219	CALL_FUNCTION_1   None
222	CALL_FUNCTION_1   None
225	POP_TOP           None

226	LOAD_FAST         'i'
229	LOAD_CONST        20
232	BINARY_MODULO     None
233	JUMP_IF_TRUE      '243'

236	LOAD_CONST        None
239_0	COME_FROM         '233'
239	YIELD_VALUE       None
240	CONTINUE          '194'
243	JUMP_BACK         '194'
246	POP_BLOCK         None
247_0	COME_FROM         '175'

247	DELETE_FAST       'garbageInstances'
250	JUMP_FORWARD      '265'

253	LOAD_GLOBAL       'set'
256	CALL_FUNCTION_0   None
259	LOAD_FAST         'self'
262	STORE_ATTR        'garbageInstanceIds'
265_0	COME_FROM         '250'

265	LOAD_GLOBAL       'gc'
268	LOAD_ATTR         'set_debug'
271	LOAD_GLOBAL       'gc'
274	LOAD_ATTR         'DEBUG_SAVEALL'
277	CALL_FUNCTION_1   None
280	POP_TOP           None

281	LOAD_FAST         'self'
284	LOAD_ATTR         '_args'
287	LOAD_ATTR         'collect'
290	JUMP_IF_FALSE     '306'

293	LOAD_GLOBAL       'gc'
296	LOAD_ATTR         'collect'
299	CALL_FUNCTION_0   None
302	POP_TOP           None
303	JUMP_FORWARD      '306'
306_0	COME_FROM         '303'

306	LOAD_GLOBAL       'gc'
309	LOAD_ATTR         'garbage'
312	SLICE+0           None
313	LOAD_FAST         'self'
316	STORE_ATTR        'garbage'

319	LOAD_GLOBAL       'gc'
322	LOAD_ATTR         'garbage'
325	DELETE_SLICE+0    None

326	LOAD_GLOBAL       'len'
329	LOAD_FAST         'self'
332	LOAD_ATTR         'garbage'
335	CALL_FUNCTION_1   None
338	LOAD_CONST        0
341	COMPARE_OP        '>'
344	JUMP_IF_FALSE     '354'

347	LOAD_CONST        None
350	YIELD_VALUE       None
351	JUMP_FORWARD      '354'
354_0	COME_FROM         '351'

354	LOAD_FAST         'self'
357	LOAD_ATTR         'notify'
360	LOAD_ATTR         'getDebug'
363	CALL_FUNCTION_0   None
366	JUMP_IF_FALSE     '401'

369	LOAD_FAST         'self'
372	LOAD_ATTR         'notify'
375	LOAD_ATTR         'debug'
378	LOAD_CONST        'self.garbage == %s'
381	LOAD_GLOBAL       'fastRepr'
384	LOAD_FAST         'self'
387	LOAD_ATTR         'garbage'
390	CALL_FUNCTION_1   None
393	BINARY_MODULO     None
394	CALL_FUNCTION_1   None
397	POP_TOP           None
398	JUMP_FORWARD      '401'
401_0	COME_FROM         '398'

401	LOAD_GLOBAL       'gc'
404	LOAD_ATTR         'set_debug'
407	LOAD_FAST         'oldFlags'
410	CALL_FUNCTION_1   None
413	POP_TOP           None

414	LOAD_GLOBAL       'len'
417	LOAD_FAST         'self'
420	LOAD_ATTR         'garbage'
423	CALL_FUNCTION_1   None
426	LOAD_FAST         'self'
429	STORE_ATTR        'numGarbage'

432	LOAD_FAST         'self'
435	LOAD_ATTR         'numGarbage'
438	LOAD_CONST        0
441	COMPARE_OP        '>'
444	JUMP_IF_FALSE     '454'

447	LOAD_CONST        None
450	YIELD_VALUE       None
451	JUMP_FORWARD      '454'
454_0	COME_FROM         '451'

454	LOAD_FAST         'self'
457	LOAD_ATTR         'notify'
460	LOAD_ATTR         'info'
463	LOAD_CONST        'found %s items in gc.garbage'
466	LOAD_FAST         'self'
469	LOAD_ATTR         'numGarbage'
472	BINARY_MODULO     None
473	CALL_FUNCTION_1   None
476	POP_TOP           None

477	BUILD_MAP         None
480	LOAD_FAST         'self'
483	STORE_ATTR        '_id2index'

486	BUILD_MAP         None
489	LOAD_FAST         'self'
492	STORE_ATTR        'referrersByReference'

495	BUILD_MAP         None
498	LOAD_FAST         'self'
501	STORE_ATTR        'referrersByNumber'

504	BUILD_MAP         None
507	LOAD_FAST         'self'
510	STORE_ATTR        'referentsByReference'

513	BUILD_MAP         None
516	LOAD_FAST         'self'
519	STORE_ATTR        'referentsByNumber'

522	BUILD_MAP         None
525	LOAD_FAST         'self'
528	STORE_ATTR        '_id2garbageInfo'

531	BUILD_LIST_0      None
534	LOAD_FAST         'self'
537	STORE_ATTR        'cycles'

540	BUILD_LIST_0      None
543	LOAD_FAST         'self'
546	STORE_ATTR        'cyclesBySyntax'

549	LOAD_GLOBAL       'set'
552	CALL_FUNCTION_0   None
555	LOAD_FAST         'self'
558	STORE_ATTR        'uniqueCycleSets'

561	LOAD_GLOBAL       'set'
564	CALL_FUNCTION_0   None
567	LOAD_FAST         'self'
570	STORE_ATTR        'cycleIds'

573	SETUP_LOOP        '642'
576	LOAD_GLOBAL       'xrange'
579	LOAD_FAST         'self'
582	LOAD_ATTR         'numGarbage'
585	CALL_FUNCTION_1   None
588	GET_ITER          None
589	FOR_ITER          '641'
592	STORE_FAST        'i'

595	LOAD_FAST         'i'
598	LOAD_FAST         'self'
601	LOAD_ATTR         '_id2index'
604	LOAD_GLOBAL       'id'
607	LOAD_FAST         'self'
610	LOAD_ATTR         'garbage'
613	LOAD_FAST         'i'
616	BINARY_SUBSCR     None
617	CALL_FUNCTION_1   None
620	STORE_SUBSCR      None

621	LOAD_FAST         'i'
624	LOAD_CONST        20
627	BINARY_MODULO     None
628	JUMP_IF_TRUE      '638'

631	LOAD_CONST        None
634_0	COME_FROM         '628'
634	YIELD_VALUE       None
635	CONTINUE          '589'
638	JUMP_BACK         '589'
641	POP_BLOCK         None
642_0	COME_FROM         '573'

642	LOAD_FAST         'self'
645	LOAD_ATTR         '_args'
648	LOAD_ATTR         'fullReport'
651	JUMP_IF_FALSE     '808'
654	LOAD_FAST         'self'
657	LOAD_ATTR         'numGarbage'
660	LOAD_CONST        0
663	COMPARE_OP        '!='
666_0	COME_FROM         '651'
666	JUMP_IF_FALSE     '808'

669	LOAD_FAST         'self'
672	LOAD_ATTR         '_args'
675	LOAD_ATTR         'verbose'
678	JUMP_IF_FALSE     '700'

681	LOAD_FAST         'self'
684	LOAD_ATTR         'notify'
687	LOAD_ATTR         'info'
690	LOAD_CONST        'getting referrers...'
693	CALL_FUNCTION_1   None
696	POP_TOP           None
697	JUMP_FORWARD      '700'
700_0	COME_FROM         '697'

700	SETUP_LOOP        '808'
703	LOAD_GLOBAL       'xrange'
706	LOAD_FAST         'self'
709	LOAD_ATTR         'numGarbage'
712	CALL_FUNCTION_1   None
715	GET_ITER          None
716	FOR_ITER          '804'
719	STORE_FAST        'i'

722	LOAD_CONST        None
725	YIELD_VALUE       None

726	SETUP_LOOP        '763'
729	LOAD_FAST         'self'
732	LOAD_ATTR         '_getReferrers'
735	LOAD_FAST         'self'
738	LOAD_ATTR         'garbage'
741	LOAD_FAST         'i'
744	BINARY_SUBSCR     None
745	CALL_FUNCTION_1   None
748	GET_ITER          None
749	FOR_ITER          '762'
752	STORE_FAST        'result'

755	LOAD_CONST        None
758	YIELD_VALUE       None
759	JUMP_BACK         '749'
762	POP_BLOCK         None
763_0	COME_FROM         '726'

763	LOAD_FAST         'result'
766	UNPACK_SEQUENCE_2 None
769	STORE_FAST        'byNum'
772	STORE_FAST        'byRef'

775	LOAD_FAST         'byNum'
778	LOAD_FAST         'self'
781	LOAD_ATTR         'referrersByNumber'
784	LOAD_FAST         'i'
787	STORE_SUBSCR      None

788	LOAD_FAST         'byRef'
791	LOAD_FAST         'self'
794	LOAD_ATTR         'referrersByReference'
797	LOAD_FAST         'i'
800	STORE_SUBSCR      None
801	JUMP_BACK         '716'
804	POP_BLOCK         None
805_0	COME_FROM         '700'
805	JUMP_FORWARD      '808'
808_0	COME_FROM         '805'

808	LOAD_FAST         'self'
811	LOAD_ATTR         'numGarbage'
814	LOAD_CONST        0
817	COMPARE_OP        '>'
820	JUMP_IF_FALSE     '962'

823	LOAD_FAST         'self'
826	LOAD_ATTR         '_args'
829	LOAD_ATTR         'verbose'
832	JUMP_IF_FALSE     '854'

835	LOAD_FAST         'self'
838	LOAD_ATTR         'notify'
841	LOAD_ATTR         'info'
844	LOAD_CONST        'getting referents...'
847	CALL_FUNCTION_1   None
850	POP_TOP           None
851	JUMP_FORWARD      '854'
854_0	COME_FROM         '851'

854	SETUP_LOOP        '962'
857	LOAD_GLOBAL       'xrange'
860	LOAD_FAST         'self'
863	LOAD_ATTR         'numGarbage'
866	CALL_FUNCTION_1   None
869	GET_ITER          None
870	FOR_ITER          '958'
873	STORE_FAST        'i'

876	LOAD_CONST        None
879	YIELD_VALUE       None

880	SETUP_LOOP        '917'
883	LOAD_FAST         'self'
886	LOAD_ATTR         '_getReferents'
889	LOAD_FAST         'self'
892	LOAD_ATTR         'garbage'
895	LOAD_FAST         'i'
898	BINARY_SUBSCR     None
899	CALL_FUNCTION_1   None
902	GET_ITER          None
903	FOR_ITER          '916'
906	STORE_FAST        'result'

909	LOAD_CONST        None
912	YIELD_VALUE       None
913	JUMP_BACK         '903'
916	POP_BLOCK         None
917_0	COME_FROM         '880'

917	LOAD_FAST         'result'
920	UNPACK_SEQUENCE_2 None
923	STORE_FAST        'byNum'
926	STORE_FAST        'byRef'

929	LOAD_FAST         'byNum'
932	LOAD_FAST         'self'
935	LOAD_ATTR         'referentsByNumber'
938	LOAD_FAST         'i'
941	STORE_SUBSCR      None

942	LOAD_FAST         'byRef'
945	LOAD_FAST         'self'
948	LOAD_ATTR         'referentsByReference'
951	LOAD_FAST         'i'
954	STORE_SUBSCR      None
955	JUMP_BACK         '870'
958	POP_BLOCK         None
959_0	COME_FROM         '854'
959	JUMP_FORWARD      '962'
962_0	COME_FROM         '959'

962	SETUP_LOOP        '1139'
965	LOAD_GLOBAL       'xrange'
968	LOAD_FAST         'self'
971	LOAD_ATTR         'numGarbage'
974	CALL_FUNCTION_1   None
977	GET_ITER          None
978	FOR_ITER          '1138'
981	STORE_FAST        'i'

984	LOAD_GLOBAL       'hasattr'
987	LOAD_FAST         'self'
990	LOAD_ATTR         'garbage'
993	LOAD_FAST         'i'
996	BINARY_SUBSCR     None
997	LOAD_CONST        '_garbageInfo'
1000	CALL_FUNCTION_2   None
1003	JUMP_IF_FALSE     '1118'
1006	LOAD_GLOBAL       'callable'
1009	LOAD_FAST         'self'
1012	LOAD_ATTR         'garbage'
1015	LOAD_FAST         'i'
1018	BINARY_SUBSCR     None
1019	LOAD_ATTR         '_garbageInfo'
1022	CALL_FUNCTION_1   None
1025_0	COME_FROM         '1003'
1025	JUMP_IF_FALSE     '1118'

1028	SETUP_EXCEPT      '1054'

1031	LOAD_FAST         'self'
1034	LOAD_ATTR         'garbage'
1037	LOAD_FAST         'i'
1040	BINARY_SUBSCR     None
1041	LOAD_ATTR         '_garbageInfo'
1044	CALL_FUNCTION_0   None
1047	STORE_FAST        'info'
1050	POP_BLOCK         None
1051	JUMP_FORWARD      '1085'
1054_0	COME_FROM         '1028'

1054	DUP_TOP           None
1055	LOAD_GLOBAL       'Exception'
1058	COMPARE_OP        'exception match'
1061	JUMP_IF_FALSE     '1084'
1064	POP_TOP           None
1065	STORE_FAST        'e'
1068	POP_TOP           None

1069	LOAD_GLOBAL       'str'
1072	LOAD_FAST         'e'
1075	CALL_FUNCTION_1   None
1078	STORE_FAST        'info'
1081	JUMP_FORWARD      '1085'
1084	END_FINALLY       None
1085_0	COME_FROM         '1051'
1085_1	COME_FROM         '1084'

1085	LOAD_FAST         'info'
1088	LOAD_FAST         'self'
1091	LOAD_ATTR         '_id2garbageInfo'
1094	LOAD_GLOBAL       'id'
1097	LOAD_FAST         'self'
1100	LOAD_ATTR         'garbage'
1103	LOAD_FAST         'i'
1106	BINARY_SUBSCR     None
1107	CALL_FUNCTION_1   None
1110	STORE_SUBSCR      None

1111	LOAD_CONST        None
1114	YIELD_VALUE       None
1115	CONTINUE          '978'

1118	LOAD_FAST         'i'
1121	LOAD_CONST        20
1124	BINARY_MODULO     None
1125	JUMP_IF_TRUE      '1135'

1128	LOAD_CONST        None
1131_0	COME_FROM         '1125'
1131	YIELD_VALUE       None
1132	CONTINUE          '978'
1135	JUMP_BACK         '978'
1138	POP_BLOCK         None
1139_0	COME_FROM         '962'

1139	LOAD_FAST         'self'
1142	LOAD_ATTR         '_args'
1145	LOAD_ATTR         'findCycles'
1148	JUMP_IF_FALSE     '2163'
1151	LOAD_FAST         'self'
1154	LOAD_ATTR         'numGarbage'
1157	LOAD_CONST        0
1160	COMPARE_OP        '>'
1163_0	COME_FROM         '1148'
1163	JUMP_IF_FALSE     '2163'

1166	LOAD_FAST         'self'
1169	LOAD_ATTR         '_args'
1172	LOAD_ATTR         'verbose'
1175	JUMP_IF_FALSE     '1197'

1178	LOAD_FAST         'self'
1181	LOAD_ATTR         'notify'
1184	LOAD_ATTR         'info'
1187	LOAD_CONST        'calculating cycles...'
1190	CALL_FUNCTION_1   None
1193	POP_TOP           None
1194	JUMP_FORWARD      '1197'
1197_0	COME_FROM         '1194'

1197	SETUP_LOOP        '2163'
1200	LOAD_GLOBAL       'xrange'
1203	LOAD_FAST         'self'
1206	LOAD_ATTR         'numGarbage'
1209	CALL_FUNCTION_1   None
1212	GET_ITER          None
1213	FOR_ITER          '2159'
1216	STORE_FAST        'i'

1219	LOAD_CONST        None
1222	YIELD_VALUE       None

1223	SETUP_LOOP        '1259'
1226	LOAD_FAST         'self'
1229	LOAD_ATTR         '_getCycles'
1232	LOAD_FAST         'i'
1235	LOAD_FAST         'self'
1238	LOAD_ATTR         'uniqueCycleSets'
1241	CALL_FUNCTION_2   None
1244	GET_ITER          None
1245	FOR_ITER          '1258'
1248	STORE_FAST        'newCycles'

1251	LOAD_CONST        None
1254	YIELD_VALUE       None
1255	JUMP_BACK         '1245'
1258	POP_BLOCK         None
1259_0	COME_FROM         '1223'

1259	LOAD_FAST         'self'
1262	LOAD_ATTR         'cycles'
1265	LOAD_ATTR         'extend'
1268	LOAD_FAST         'newCycles'
1271	CALL_FUNCTION_1   None
1274	POP_TOP           None

1275	BUILD_LIST_0      None
1278	STORE_FAST        'newCyclesBySyntax'

1281	SETUP_LOOP        '2082'
1284	LOAD_FAST         'newCycles'
1287	GET_ITER          None
1288	FOR_ITER          '2081'
1291	STORE_FAST        'cycle'

1294	LOAD_CONST        ''
1297	STORE_FAST        'cycleBySyntax'

1300	BUILD_LIST_0      None
1303	STORE_FAST        'objs'

1306	SETUP_LOOP        '1351'
1309	LOAD_FAST         'cycle'
1312	LOAD_CONST        -1
1315	SLICE+2           None
1316	GET_ITER          None
1317	FOR_ITER          '1350'
1320	STORE_FAST        'index'

1323	LOAD_FAST         'objs'
1326	LOAD_ATTR         'append'
1329	LOAD_FAST         'self'
1332	LOAD_ATTR         'garbage'
1335	LOAD_FAST         'index'
1338	BINARY_SUBSCR     None
1339	CALL_FUNCTION_1   None
1342	POP_TOP           None

1343	LOAD_CONST        None
1346	YIELD_VALUE       None
1347	JUMP_BACK         '1317'
1350	POP_BLOCK         None
1351_0	COME_FROM         '1306'

1351	LOAD_GLOBAL       'len'
1354	LOAD_FAST         'objs'
1357	CALL_FUNCTION_1   None
1360	LOAD_CONST        1
1363	BINARY_SUBTRACT   None
1364	STORE_FAST        'numObjs'

1367	LOAD_FAST         'objs'
1370	LOAD_ATTR         'extend'
1373	LOAD_FAST         'objs'
1376	CALL_FUNCTION_1   None
1379	POP_TOP           None

1380	LOAD_CONST        0
1383	STORE_FAST        'numToSkip'

1386	LOAD_GLOBAL       'False'
1389	STORE_FAST        'objAlreadyRepresented'

1392	LOAD_CONST        0
1395	STORE_FAST        'startIndex'

1398	LOAD_FAST         'numObjs'
1401	LOAD_CONST        1
1404	BINARY_ADD        None
1405	STORE_FAST        'endIndex'

1408	LOAD_GLOBAL       'type'
1411	LOAD_FAST         'objs'
1414	LOAD_CONST        -1
1417	BINARY_SUBSCR     None
1418	CALL_FUNCTION_1   None
1421	LOAD_GLOBAL       'types'
1424	LOAD_ATTR         'InstanceType'
1427	COMPARE_OP        'is'
1430	JUMP_IF_FALSE     '1481'
1433	LOAD_GLOBAL       'type'
1436	LOAD_FAST         'objs'
1439	LOAD_CONST        0
1442	BINARY_SUBSCR     None
1443	CALL_FUNCTION_1   None
1446	LOAD_GLOBAL       'types'
1449	LOAD_ATTR         'DictType'
1452	COMPARE_OP        'is'
1455_0	COME_FROM         '1430'
1455	JUMP_IF_FALSE     '1481'

1458	LOAD_FAST         'startIndex'
1461	LOAD_CONST        1
1464	INPLACE_SUBTRACT  None
1465	STORE_FAST        'startIndex'

1468	LOAD_FAST         'endIndex'
1471	LOAD_CONST        1
1474	INPLACE_SUBTRACT  None
1475	STORE_FAST        'endIndex'
1478	JUMP_FORWARD      '1481'
1481_0	COME_FROM         '1478'

1481	SETUP_LOOP        '2061'
1484	LOAD_GLOBAL       'xrange'
1487	LOAD_FAST         'startIndex'
1490	LOAD_FAST         'endIndex'
1493	CALL_FUNCTION_2   None
1496	GET_ITER          None
1497	FOR_ITER          '2060'
1500	STORE_FAST        'index'

1503	LOAD_FAST         'numToSkip'
1506	JUMP_IF_FALSE     '1525'

1509	LOAD_FAST         'numToSkip'
1512	LOAD_CONST        1
1515	INPLACE_SUBTRACT  None
1516	STORE_FAST        'numToSkip'

1519	CONTINUE          '1497'
1522	JUMP_FORWARD      '1525'
1525_0	COME_FROM         '1522'

1525	LOAD_FAST         'objs'
1528	LOAD_FAST         'index'
1531	BINARY_SUBSCR     None
1532	STORE_FAST        'obj'

1535	LOAD_GLOBAL       'type'
1538	LOAD_FAST         'obj'
1541	CALL_FUNCTION_1   None
1544	LOAD_GLOBAL       'types'
1547	LOAD_ATTR         'InstanceType'
1550	COMPARE_OP        'is'
1553	JUMP_IF_FALSE     '1700'

1556	LOAD_FAST         'objAlreadyRepresented'
1559	JUMP_IF_TRUE      '1585'

1562	LOAD_FAST         'cycleBySyntax'
1565	LOAD_CONST        '%s'
1568	LOAD_FAST         'obj'
1571	LOAD_ATTR         '__class__'
1574	LOAD_ATTR         '__name__'
1577	BINARY_MODULO     None
1578	INPLACE_ADD       None
1579	STORE_FAST        'cycleBySyntax'
1582	JUMP_FORWARD      '1585'
1585_0	COME_FROM         '1582'

1585	LOAD_FAST         'cycleBySyntax'
1588	LOAD_CONST        '.'
1591	INPLACE_ADD       None
1592	STORE_FAST        'cycleBySyntax'

1595	LOAD_FAST         'numToSkip'
1598	LOAD_CONST        1
1601	INPLACE_ADD       None
1602	STORE_FAST        'numToSkip'

1605	LOAD_FAST         'objs'
1608	LOAD_FAST         'index'
1611	LOAD_CONST        2
1614	BINARY_ADD        None
1615	BINARY_SUBSCR     None
1616	STORE_FAST        'member'

1619	SETUP_LOOP        '1677'
1622	LOAD_FAST         'obj'
1625	LOAD_ATTR         '__dict__'
1628	LOAD_ATTR         'iteritems'
1631	CALL_FUNCTION_0   None
1634	GET_ITER          None
1635	FOR_ITER          '1670'
1638	UNPACK_SEQUENCE_2 None
1641	STORE_FAST        'key'
1644	STORE_FAST        'value'

1647	LOAD_FAST         'value'
1650	LOAD_FAST         'member'
1653	COMPARE_OP        'is'
1656	JUMP_IF_FALSE     '1663'

1659	BREAK_LOOP        None
1660	JUMP_FORWARD      '1663'
1663_0	COME_FROM         '1660'

1663	LOAD_CONST        None
1666	YIELD_VALUE       None
1667	JUMP_BACK         '1635'
1670	POP_BLOCK         None

1671	LOAD_CONST        '<unknown member name>'
1674	STORE_FAST        'key'
1677_0	COME_FROM         '1619'

1677	LOAD_FAST         'cycleBySyntax'
1680	LOAD_CONST        '%s'
1683	LOAD_FAST         'key'
1686	BINARY_MODULO     None
1687	INPLACE_ADD       None
1688	STORE_FAST        'cycleBySyntax'

1691	LOAD_GLOBAL       'True'
1694	STORE_FAST        'objAlreadyRepresented'
1697	JUMP_BACK         '1497'

1700	LOAD_GLOBAL       'type'
1703	LOAD_FAST         'obj'
1706	CALL_FUNCTION_1   None
1709	LOAD_GLOBAL       'types'
1712	LOAD_ATTR         'DictType'
1715	COMPARE_OP        'is'
1718	JUMP_IF_FALSE     '1829'

1721	LOAD_FAST         'cycleBySyntax'
1724	LOAD_CONST        '{'
1727	INPLACE_ADD       None
1728	STORE_FAST        'cycleBySyntax'

1731	LOAD_FAST         'objs'
1734	LOAD_FAST         'index'
1737	LOAD_CONST        1
1740	BINARY_ADD        None
1741	BINARY_SUBSCR     None
1742	STORE_FAST        'val'

1745	SETUP_LOOP        '1800'
1748	LOAD_FAST         'obj'
1751	LOAD_ATTR         'iteritems'
1754	CALL_FUNCTION_0   None
1757	GET_ITER          None
1758	FOR_ITER          '1793'
1761	UNPACK_SEQUENCE_2 None
1764	STORE_FAST        'key'
1767	STORE_FAST        'value'

1770	LOAD_FAST         'value'
1773	LOAD_FAST         'val'
1776	COMPARE_OP        'is'
1779	JUMP_IF_FALSE     '1786'

1782	BREAK_LOOP        None
1783	JUMP_FORWARD      '1786'
1786_0	COME_FROM         '1783'

1786	LOAD_CONST        None
1789	YIELD_VALUE       None
1790	JUMP_BACK         '1758'
1793	POP_BLOCK         None

1794	LOAD_CONST        '<unknown key>'
1797	STORE_FAST        'key'
1800_0	COME_FROM         '1745'

1800	LOAD_FAST         'cycleBySyntax'
1803	LOAD_CONST        '%s}'
1806	LOAD_GLOBAL       'fastRepr'
1809	LOAD_FAST         'key'
1812	CALL_FUNCTION_1   None
1815	BINARY_MODULO     None
1816	INPLACE_ADD       None
1817	STORE_FAST        'cycleBySyntax'

1820	LOAD_GLOBAL       'True'
1823	STORE_FAST        'objAlreadyRepresented'
1826	JUMP_BACK         '1497'

1829	LOAD_GLOBAL       'type'
1832	LOAD_FAST         'obj'
1835	CALL_FUNCTION_1   None
1838	LOAD_GLOBAL       'types'
1841	LOAD_ATTR         'TupleType'
1844	LOAD_GLOBAL       'types'
1847	LOAD_ATTR         'ListType'
1850	BUILD_TUPLE_2     None
1853	COMPARE_OP        'in'
1856	JUMP_IF_FALSE     '2031'

1859	BUILD_MAP         None
1862	DUP_TOP           None
1863	LOAD_GLOBAL       'types'
1866	LOAD_ATTR         'TupleType'
1869	LOAD_CONST        '()'
1872	ROT_THREE         None
1873	STORE_SUBSCR      None
1874	DUP_TOP           None
1875	LOAD_GLOBAL       'types'
1878	LOAD_ATTR         'ListType'
1881	LOAD_CONST        '[]'
1884	ROT_THREE         None
1885	STORE_SUBSCR      None
1886	LOAD_GLOBAL       'type'
1889	LOAD_FAST         'obj'
1892	CALL_FUNCTION_1   None
1895	BINARY_SUBSCR     None
1896	STORE_FAST        'brackets'

1899	LOAD_FAST         'objs'
1902	LOAD_FAST         'index'
1905	LOAD_CONST        1
1908	BINARY_ADD        None
1909	BINARY_SUBSCR     None
1910	STORE_FAST        'nextObj'

1913	LOAD_FAST         'cycleBySyntax'
1916	LOAD_FAST         'brackets'
1919	LOAD_CONST        0
1922	BINARY_SUBSCR     None
1923	INPLACE_ADD       None
1924	STORE_FAST        'cycleBySyntax'

1927	SETUP_LOOP        '1998'
1930	LOAD_GLOBAL       'xrange'
1933	LOAD_GLOBAL       'len'
1936	LOAD_FAST         'obj'
1939	CALL_FUNCTION_1   None
1942	CALL_FUNCTION_1   None
1945	GET_ITER          None
1946	FOR_ITER          '1991'
1949	STORE_FAST        'index'

1952	LOAD_FAST         'obj'
1955	LOAD_FAST         'index'
1958	BINARY_SUBSCR     None
1959	LOAD_FAST         'nextObj'
1962	COMPARE_OP        'is'
1965	JUMP_IF_FALSE     '1984'

1968	LOAD_GLOBAL       'str'
1971	LOAD_FAST         'index'
1974	CALL_FUNCTION_1   None
1977	STORE_FAST        'index'

1980	BREAK_LOOP        None
1981	JUMP_FORWARD      '1984'
1984_0	COME_FROM         '1981'

1984	LOAD_CONST        None
1987	YIELD_VALUE       None
1988	JUMP_BACK         '1946'
1991	POP_BLOCK         None

1992	LOAD_CONST        '<unknown index>'
1995	STORE_FAST        'index'
1998_0	COME_FROM         '1927'

1998	LOAD_FAST         'cycleBySyntax'
2001	LOAD_CONST        '%s%s'
2004	LOAD_FAST         'index'
2007	LOAD_FAST         'brackets'
2010	LOAD_CONST        1
2013	BINARY_SUBSCR     None
2014	BUILD_TUPLE_2     None
2017	BINARY_MODULO     None
2018	INPLACE_ADD       None
2019	STORE_FAST        'cycleBySyntax'

2022	LOAD_GLOBAL       'True'
2025	STORE_FAST        'objAlreadyRepresented'
2028	JUMP_BACK         '1497'

2031	LOAD_FAST         'cycleBySyntax'
2034	LOAD_CONST        '%s --> '
2037	LOAD_GLOBAL       'itype'
2040	LOAD_FAST         'obj'
2043	CALL_FUNCTION_1   None
2046	BINARY_MODULO     None
2047	INPLACE_ADD       None
2048	STORE_FAST        'cycleBySyntax'

2051	LOAD_GLOBAL       'False'
2054	STORE_FAST        'objAlreadyRepresented'
2057	JUMP_BACK         '1497'
2060	POP_BLOCK         None
2061_0	COME_FROM         '1481'

2061	LOAD_FAST         'newCyclesBySyntax'
2064	LOAD_ATTR         'append'
2067	LOAD_FAST         'cycleBySyntax'
2070	CALL_FUNCTION_1   None
2073	POP_TOP           None

2074	LOAD_CONST        None
2077	YIELD_VALUE       None
2078	JUMP_BACK         '1288'
2081	POP_BLOCK         None
2082_0	COME_FROM         '1281'

2082	LOAD_FAST         'self'
2085	LOAD_ATTR         'cyclesBySyntax'
2088	LOAD_ATTR         'extend'
2091	LOAD_FAST         'newCyclesBySyntax'
2094	CALL_FUNCTION_1   None
2097	POP_TOP           None

2098	LOAD_FAST         'self'
2101	LOAD_ATTR         '_args'
2104	LOAD_ATTR         'fullReport'
2107	JUMP_IF_TRUE      '2156'

2110	SETUP_LOOP        '2156'
2113	LOAD_FAST         'newCycles'
2116	GET_ITER          None
2117	FOR_ITER          '2152'
2120	STORE_FAST        'cycle'

2123	LOAD_CONST        None
2126	YIELD_VALUE       None

2127	LOAD_FAST         'self'
2130	LOAD_ATTR         'cycleIds'
2133	LOAD_ATTR         'update'
2136	LOAD_GLOBAL       'set'
2139	LOAD_FAST         'cycle'
2142	CALL_FUNCTION_1   None
2145	CALL_FUNCTION_1   None
2148	POP_TOP           None
2149	JUMP_BACK         '2117'
2152	POP_BLOCK         None
2153_0	COME_FROM         '2110'
2153	JUMP_BACK         '1213'
2156	JUMP_BACK         '1213'
2159	POP_BLOCK         None
2160_0	COME_FROM         '1197'
2160	JUMP_FORWARD      '2163'
2163_0	COME_FROM         '2160'

2163	LOAD_GLOBAL       'len'
2166	LOAD_FAST         'self'
2169	LOAD_ATTR         'cycles'
2172	CALL_FUNCTION_1   None
2175	LOAD_FAST         'self'
2178	STORE_ATTR        'numCycles'

2181	LOAD_FAST         'self'
2184	LOAD_ATTR         '_args'
2187	LOAD_ATTR         'findCycles'
2190	JUMP_IF_FALSE     '2248'

2193	LOAD_CONST        "===== GarbageReport: '%s' (%s %s) ====="
2196	LOAD_FAST         'self'
2199	LOAD_ATTR         '_args'
2202	LOAD_ATTR         'name'
2205	LOAD_FAST         'self'
2208	LOAD_ATTR         'numCycles'
2211	LOAD_GLOBAL       'choice'
2214	LOAD_FAST         'self'
2217	LOAD_ATTR         'numCycles'
2220	LOAD_CONST        1
2223	COMPARE_OP        '=='
2226	LOAD_CONST        'cycle'
2229	LOAD_CONST        'cycles'
2232	CALL_FUNCTION_3   None
2235	BUILD_TUPLE_3     None
2238	BINARY_MODULO     None
2239	BUILD_LIST_1      None
2242	STORE_FAST        's'
2245	JUMP_FORWARD      '2267'

2248	LOAD_CONST        "===== GarbageReport: '%s' ====="
2251	LOAD_FAST         'self'
2254	LOAD_ATTR         '_args'
2257	LOAD_ATTR         'name'
2260	BINARY_MODULO     None
2261	BUILD_LIST_1      None
2264	STORE_FAST        's'
2267_0	COME_FROM         '2245'

2267	LOAD_FAST         'self'
2270	LOAD_ATTR         'numGarbage'
2273	LOAD_CONST        0
2276	COMPARE_OP        '>'
2279	JUMP_IF_FALSE     '3578'

2282	LOAD_FAST         'self'
2285	LOAD_ATTR         '_args'
2288	LOAD_ATTR         'fullReport'
2291	JUMP_IF_FALSE     '2312'

2294	LOAD_GLOBAL       'range'
2297	LOAD_FAST         'self'
2300	LOAD_ATTR         'numGarbage'
2303	CALL_FUNCTION_1   None
2306	STORE_FAST        'garbageIndices'
2309	JUMP_FORWARD      '2337'

2312	LOAD_GLOBAL       'list'
2315	LOAD_FAST         'self'
2318	LOAD_ATTR         'cycleIds'
2321	CALL_FUNCTION_1   None
2324	STORE_FAST        'garbageIndices'

2327	LOAD_FAST         'garbageIndices'
2330	LOAD_ATTR         'sort'
2333	CALL_FUNCTION_0   None
2336	POP_TOP           None
2337_0	COME_FROM         '2309'

2337	LOAD_GLOBAL       'len'
2340	LOAD_FAST         'garbageIndices'
2343	CALL_FUNCTION_1   None
2346	STORE_FAST        'numGarbage'

2349	LOAD_FAST         'self'
2352	LOAD_ATTR         '_args'
2355	LOAD_ATTR         'fullReport'
2358	JUMP_IF_TRUE      '2370'

2361	LOAD_CONST        '(abbreviated) '
2364	STORE_FAST        'abbrev'
2367	JUMP_FORWARD      '2376'

2370	LOAD_CONST        ''
2373	STORE_FAST        'abbrev'
2376_0	COME_FROM         '2367'

2376	LOAD_FAST         's'
2379	LOAD_ATTR         'append'
2382	LOAD_CONST        '===== Garbage Items %s====='
2385	LOAD_FAST         'abbrev'
2388	BINARY_MODULO     None
2389	CALL_FUNCTION_1   None
2392	POP_TOP           None

2393	LOAD_CONST        0
2396	STORE_FAST        'digits'

2399	LOAD_FAST         'numGarbage'
2402	STORE_FAST        'n'

2405	SETUP_LOOP        '2448'
2408	LOAD_FAST         'n'
2411	LOAD_CONST        0
2414	COMPARE_OP        '>'
2417	JUMP_IF_FALSE     '2447'

2420	LOAD_CONST        None
2423	YIELD_VALUE       None

2424	LOAD_FAST         'digits'
2427	LOAD_CONST        1
2430	INPLACE_ADD       None
2431	STORE_FAST        'digits'

2434	LOAD_FAST         'n'
2437	LOAD_CONST        10
2440	INPLACE_DIVIDE    None
2441	STORE_FAST        'n'
2444	JUMP_BACK         '2408'
2447	POP_BLOCK         None
2448_0	COME_FROM         '2405'

2448	LOAD_FAST         'digits'
2451	STORE_FAST        'digits'

2454	LOAD_CONST        '%0'
2457	LOAD_CONST        '%s'
2460	LOAD_FAST         'digits'
2463	BINARY_MODULO     None
2464	BINARY_ADD        None
2465	LOAD_CONST        'i:%s \t%s'
2468	BINARY_ADD        None
2469	STORE_FAST        'format'

2472	SETUP_LOOP        '2670'
2475	LOAD_GLOBAL       'xrange'
2478	LOAD_FAST         'numGarbage'
2481	CALL_FUNCTION_1   None
2484	GET_ITER          None
2485	FOR_ITER          '2669'
2488	STORE_FAST        'i'

2491	LOAD_CONST        None
2494	YIELD_VALUE       None

2495	LOAD_FAST         'garbageIndices'
2498	LOAD_FAST         'i'
2501	BINARY_SUBSCR     None
2502	STORE_FAST        'idx'

2505	LOAD_FAST         'self'
2508	LOAD_ATTR         '_args'
2511	LOAD_ATTR         'safeMode'
2514	JUMP_IF_FALSE     '2545'

2517	LOAD_GLOBAL       'repr'
2520	LOAD_GLOBAL       'itype'
2523	LOAD_FAST         'self'
2526	LOAD_ATTR         'garbage'
2529	LOAD_FAST         'idx'
2532	BINARY_SUBSCR     None
2533	CALL_FUNCTION_1   None
2536	CALL_FUNCTION_1   None
2539	STORE_FAST        'objStr'
2542	JUMP_FORWARD      '2564'

2545	LOAD_GLOBAL       'fastRepr'
2548	LOAD_FAST         'self'
2551	LOAD_ATTR         'garbage'
2554	LOAD_FAST         'idx'
2557	BINARY_SUBSCR     None
2558	CALL_FUNCTION_1   None
2561	STORE_FAST        'objStr'
2564_0	COME_FROM         '2542'

2564	LOAD_CONST        5000
2567	STORE_FAST        'maxLen'

2570	LOAD_GLOBAL       'len'
2573	LOAD_FAST         'objStr'
2576	CALL_FUNCTION_1   None
2579	LOAD_FAST         'maxLen'
2582	COMPARE_OP        '>'
2585	JUMP_IF_FALSE     '2627'

2588	LOAD_CONST        '<SNIP>'
2591	STORE_FAST        'snip'

2594	LOAD_CONST        '%s%s'
2597	LOAD_FAST         'objStr'
2600	LOAD_FAST         'maxLen'
2603	LOAD_GLOBAL       'len'
2606	LOAD_FAST         'snip'
2609	CALL_FUNCTION_1   None
2612	BINARY_SUBTRACT   None
2613	SLICE+2           None
2614	LOAD_FAST         'snip'
2617	BUILD_TUPLE_2     None
2620	BINARY_MODULO     None
2621	STORE_FAST        'objStr'
2624	JUMP_FORWARD      '2627'
2627_0	COME_FROM         '2624'

2627	LOAD_FAST         's'
2630	LOAD_ATTR         'append'
2633	LOAD_FAST         'format'
2636	LOAD_FAST         'idx'
2639	LOAD_GLOBAL       'itype'
2642	LOAD_FAST         'self'
2645	LOAD_ATTR         'garbage'
2648	LOAD_FAST         'idx'
2651	BINARY_SUBSCR     None
2652	CALL_FUNCTION_1   None
2655	LOAD_FAST         'objStr'
2658	BUILD_TUPLE_3     None
2661	BINARY_MODULO     None
2662	CALL_FUNCTION_1   None
2665	POP_TOP           None
2666	JUMP_BACK         '2485'
2669	POP_BLOCK         None
2670_0	COME_FROM         '2472'

2670	LOAD_FAST         's'
2673	LOAD_ATTR         'append'
2676	LOAD_CONST        '===== Garbage Item Types %s====='
2679	LOAD_FAST         'abbrev'
2682	BINARY_MODULO     None
2683	CALL_FUNCTION_1   None
2686	POP_TOP           None

2687	SETUP_LOOP        '2851'
2690	LOAD_GLOBAL       'xrange'
2693	LOAD_FAST         'numGarbage'
2696	CALL_FUNCTION_1   None
2699	GET_ITER          None
2700	FOR_ITER          '2850'
2703	STORE_FAST        'i'

2706	LOAD_CONST        None
2709	YIELD_VALUE       None

2710	LOAD_FAST         'garbageIndices'
2713	LOAD_FAST         'i'
2716	BINARY_SUBSCR     None
2717	STORE_FAST        'idx'

2720	LOAD_GLOBAL       'str'
2723	LOAD_GLOBAL       'deeptype'
2726	LOAD_FAST         'self'
2729	LOAD_ATTR         'garbage'
2732	LOAD_FAST         'idx'
2735	BINARY_SUBSCR     None
2736	CALL_FUNCTION_1   None
2739	CALL_FUNCTION_1   None
2742	STORE_FAST        'objStr'

2745	LOAD_CONST        5000
2748	STORE_FAST        'maxLen'

2751	LOAD_GLOBAL       'len'
2754	LOAD_FAST         'objStr'
2757	CALL_FUNCTION_1   None
2760	LOAD_FAST         'maxLen'
2763	COMPARE_OP        '>'
2766	JUMP_IF_FALSE     '2808'

2769	LOAD_CONST        '<SNIP>'
2772	STORE_FAST        'snip'

2775	LOAD_CONST        '%s%s'
2778	LOAD_FAST         'objStr'
2781	LOAD_FAST         'maxLen'
2784	LOAD_GLOBAL       'len'
2787	LOAD_FAST         'snip'
2790	CALL_FUNCTION_1   None
2793	BINARY_SUBTRACT   None
2794	SLICE+2           None
2795	LOAD_FAST         'snip'
2798	BUILD_TUPLE_2     None
2801	BINARY_MODULO     None
2802	STORE_FAST        'objStr'
2805	JUMP_FORWARD      '2808'
2808_0	COME_FROM         '2805'

2808	LOAD_FAST         's'
2811	LOAD_ATTR         'append'
2814	LOAD_FAST         'format'
2817	LOAD_FAST         'idx'
2820	LOAD_GLOBAL       'itype'
2823	LOAD_FAST         'self'
2826	LOAD_ATTR         'garbage'
2829	LOAD_FAST         'idx'
2832	BINARY_SUBSCR     None
2833	CALL_FUNCTION_1   None
2836	LOAD_FAST         'objStr'
2839	BUILD_TUPLE_3     None
2842	BINARY_MODULO     None
2843	CALL_FUNCTION_1   None
2846	POP_TOP           None
2847	JUMP_BACK         '2700'
2850	POP_BLOCK         None
2851_0	COME_FROM         '2687'

2851	LOAD_FAST         'self'
2854	LOAD_ATTR         '_args'
2857	LOAD_ATTR         'findCycles'
2860	JUMP_IF_FALSE     '2954'

2863	LOAD_FAST         's'
2866	LOAD_ATTR         'append'
2869	LOAD_CONST        '===== Garbage Cycles (Garbage Item Numbers) ====='
2872	CALL_FUNCTION_1   None
2875	POP_TOP           None

2876	LOAD_GLOBAL       'AlphabetCounter'
2879	CALL_FUNCTION_0   None
2882	STORE_FAST        'ac'

2885	SETUP_LOOP        '2954'
2888	LOAD_GLOBAL       'xrange'
2891	LOAD_FAST         'self'
2894	LOAD_ATTR         'numCycles'
2897	CALL_FUNCTION_1   None
2900	GET_ITER          None
2901	FOR_ITER          '2950'
2904	STORE_FAST        'i'

2907	LOAD_CONST        None
2910	YIELD_VALUE       None

2911	LOAD_FAST         's'
2914	LOAD_ATTR         'append'
2917	LOAD_CONST        '%s:%s'
2920	LOAD_FAST         'ac'
2923	LOAD_ATTR         'next'
2926	CALL_FUNCTION_0   None
2929	LOAD_FAST         'self'
2932	LOAD_ATTR         'cycles'
2935	LOAD_FAST         'i'
2938	BINARY_SUBSCR     None
2939	BUILD_TUPLE_2     None
2942	BINARY_MODULO     None
2943	CALL_FUNCTION_1   None
2946	POP_TOP           None
2947	JUMP_BACK         '2901'
2950	POP_BLOCK         None
2951_0	COME_FROM         '2885'
2951	JUMP_FORWARD      '2954'
2954_0	COME_FROM         '2951'

2954	LOAD_FAST         'self'
2957	LOAD_ATTR         '_args'
2960	LOAD_ATTR         'findCycles'
2963	JUMP_IF_FALSE     '3063'

2966	LOAD_FAST         's'
2969	LOAD_ATTR         'append'
2972	LOAD_CONST        '===== Garbage Cycles (Python Syntax) ====='
2975	CALL_FUNCTION_1   None
2978	POP_TOP           None

2979	LOAD_GLOBAL       'AlphabetCounter'
2982	CALL_FUNCTION_0   None
2985	STORE_FAST        'ac'

2988	SETUP_LOOP        '3063'
2991	LOAD_GLOBAL       'xrange'
2994	LOAD_GLOBAL       'len'
2997	LOAD_FAST         'self'
3000	LOAD_ATTR         'cyclesBySyntax'
3003	CALL_FUNCTION_1   None
3006	CALL_FUNCTION_1   None
3009	GET_ITER          None
3010	FOR_ITER          '3059'
3013	STORE_FAST        'i'

3016	LOAD_CONST        None
3019	YIELD_VALUE       None

3020	LOAD_FAST         's'
3023	LOAD_ATTR         'append'
3026	LOAD_CONST        '%s:%s'
3029	LOAD_FAST         'ac'
3032	LOAD_ATTR         'next'
3035	CALL_FUNCTION_0   None
3038	LOAD_FAST         'self'
3041	LOAD_ATTR         'cyclesBySyntax'
3044	LOAD_FAST         'i'
3047	BINARY_SUBSCR     None
3048	BUILD_TUPLE_2     None
3051	BINARY_MODULO     None
3052	CALL_FUNCTION_1   None
3055	POP_TOP           None
3056	JUMP_BACK         '3010'
3059	POP_BLOCK         None
3060_0	COME_FROM         '2988'
3060	JUMP_FORWARD      '3063'
3063_0	COME_FROM         '3060'

3063	LOAD_GLOBAL       'len'
3066	LOAD_FAST         'self'
3069	LOAD_ATTR         '_id2garbageInfo'
3072	CALL_FUNCTION_1   None
3075	JUMP_IF_FALSE     '3262'

3078	LOAD_CONST        '%0'
3081	LOAD_CONST        '%s'
3084	LOAD_FAST         'digits'
3087	BINARY_MODULO     None
3088	BINARY_ADD        None
3089	LOAD_CONST        'i:%s'
3092	BINARY_ADD        None
3093	STORE_FAST        'format'

3096	LOAD_FAST         's'
3099	LOAD_ATTR         'append'
3102	LOAD_CONST        '===== Garbage Custom Info ====='
3105	CALL_FUNCTION_1   None
3108	POP_TOP           None

3109	LOAD_FAST         'self'
3112	LOAD_ATTR         '_id2garbageInfo'
3115	LOAD_ATTR         'keys'
3118	CALL_FUNCTION_0   None
3121	STORE_FAST        'ids'

3124	LOAD_CONST        None
3127	YIELD_VALUE       None

3128	BUILD_LIST_0      None
3131	STORE_FAST        'indices'

3134	SETUP_LOOP        '3175'
3137	LOAD_FAST         'ids'
3140	GET_ITER          None
3141	FOR_ITER          '3174'
3144	STORE_FAST        '_id'

3147	LOAD_FAST         'indices'
3150	LOAD_ATTR         'append'
3153	LOAD_FAST         'self'
3156	LOAD_ATTR         '_id2index'
3159	LOAD_FAST         '_id'
3162	BINARY_SUBSCR     None
3163	CALL_FUNCTION_1   None
3166	POP_TOP           None

3167	LOAD_CONST        None
3170	YIELD_VALUE       None
3171	JUMP_BACK         '3141'
3174	POP_BLOCK         None
3175_0	COME_FROM         '3134'

3175	LOAD_FAST         'indices'
3178	LOAD_ATTR         'sort'
3181	CALL_FUNCTION_0   None
3184	POP_TOP           None

3185	LOAD_CONST        None
3188	YIELD_VALUE       None

3189	SETUP_LOOP        '3262'
3192	LOAD_FAST         'indices'
3195	GET_ITER          None
3196	FOR_ITER          '3258'
3199	STORE_FAST        'i'

3202	LOAD_GLOBAL       'id'
3205	LOAD_FAST         'self'
3208	LOAD_ATTR         'garbage'
3211	LOAD_FAST         'i'
3214	BINARY_SUBSCR     None
3215	CALL_FUNCTION_1   None
3218	STORE_FAST        '_id'

3221	LOAD_FAST         's'
3224	LOAD_ATTR         'append'
3227	LOAD_FAST         'format'
3230	LOAD_FAST         'i'
3233	LOAD_FAST         'self'
3236	LOAD_ATTR         '_id2garbageInfo'
3239	LOAD_FAST         '_id'
3242	BINARY_SUBSCR     None
3243	BUILD_TUPLE_2     None
3246	BINARY_MODULO     None
3247	CALL_FUNCTION_1   None
3250	POP_TOP           None

3251	LOAD_CONST        None
3254	YIELD_VALUE       None
3255	JUMP_BACK         '3196'
3258	POP_BLOCK         None
3259_0	COME_FROM         '3189'
3259	JUMP_FORWARD      '3262'
3262_0	COME_FROM         '3259'

3262	LOAD_FAST         'self'
3265	LOAD_ATTR         '_args'
3268	LOAD_ATTR         'fullReport'
3271	JUMP_IF_FALSE     '3575'

3274	LOAD_CONST        '%0'
3277	LOAD_CONST        '%s'
3280	LOAD_FAST         'digits'
3283	BINARY_MODULO     None
3284	BINARY_ADD        None
3285	LOAD_CONST        'i:%s'
3288	BINARY_ADD        None
3289	STORE_FAST        'format'

3292	LOAD_FAST         's'
3295	LOAD_ATTR         'append'
3298	LOAD_CONST        '===== Referrers By Number (what is referring to garbage item?) ====='
3301	CALL_FUNCTION_1   None
3304	POP_TOP           None

3305	SETUP_LOOP        '3362'
3308	LOAD_GLOBAL       'xrange'
3311	LOAD_FAST         'numGarbage'
3314	CALL_FUNCTION_1   None
3317	GET_ITER          None
3318	FOR_ITER          '3361'
3321	STORE_FAST        'i'

3324	LOAD_CONST        None
3327	YIELD_VALUE       None

3328	LOAD_FAST         's'
3331	LOAD_ATTR         'append'
3334	LOAD_FAST         'format'
3337	LOAD_FAST         'i'
3340	LOAD_FAST         'self'
3343	LOAD_ATTR         'referrersByNumber'
3346	LOAD_FAST         'i'
3349	BINARY_SUBSCR     None
3350	BUILD_TUPLE_2     None
3353	BINARY_MODULO     None
3354	CALL_FUNCTION_1   None
3357	POP_TOP           None
3358	JUMP_BACK         '3318'
3361	POP_BLOCK         None
3362_0	COME_FROM         '3305'

3362	LOAD_FAST         's'
3365	LOAD_ATTR         'append'
3368	LOAD_CONST        '===== Referents By Number (what is garbage item referring to?) ====='
3371	CALL_FUNCTION_1   None
3374	POP_TOP           None

3375	SETUP_LOOP        '3432'
3378	LOAD_GLOBAL       'xrange'
3381	LOAD_FAST         'numGarbage'
3384	CALL_FUNCTION_1   None
3387	GET_ITER          None
3388	FOR_ITER          '3431'
3391	STORE_FAST        'i'

3394	LOAD_CONST        None
3397	YIELD_VALUE       None

3398	LOAD_FAST         's'
3401	LOAD_ATTR         'append'
3404	LOAD_FAST         'format'
3407	LOAD_FAST         'i'
3410	LOAD_FAST         'self'
3413	LOAD_ATTR         'referentsByNumber'
3416	LOAD_FAST         'i'
3419	BINARY_SUBSCR     None
3420	BUILD_TUPLE_2     None
3423	BINARY_MODULO     None
3424	CALL_FUNCTION_1   None
3427	POP_TOP           None
3428	JUMP_BACK         '3388'
3431	POP_BLOCK         None
3432_0	COME_FROM         '3375'

3432	LOAD_FAST         's'
3435	LOAD_ATTR         'append'
3438	LOAD_CONST        '===== Referrers (what is referring to garbage item?) ====='
3441	CALL_FUNCTION_1   None
3444	POP_TOP           None

3445	SETUP_LOOP        '3502'
3448	LOAD_GLOBAL       'xrange'
3451	LOAD_FAST         'numGarbage'
3454	CALL_FUNCTION_1   None
3457	GET_ITER          None
3458	FOR_ITER          '3501'
3461	STORE_FAST        'i'

3464	LOAD_CONST        None
3467	YIELD_VALUE       None

3468	LOAD_FAST         's'
3471	LOAD_ATTR         'append'
3474	LOAD_FAST         'format'
3477	LOAD_FAST         'i'
3480	LOAD_FAST         'self'
3483	LOAD_ATTR         'referrersByReference'
3486	LOAD_FAST         'i'
3489	BINARY_SUBSCR     None
3490	BUILD_TUPLE_2     None
3493	BINARY_MODULO     None
3494	CALL_FUNCTION_1   None
3497	POP_TOP           None
3498	JUMP_BACK         '3458'
3501	POP_BLOCK         None
3502_0	COME_FROM         '3445'

3502	LOAD_FAST         's'
3505	LOAD_ATTR         'append'
3508	LOAD_CONST        '===== Referents (what is garbage item referring to?) ====='
3511	CALL_FUNCTION_1   None
3514	POP_TOP           None

3515	SETUP_LOOP        '3575'
3518	LOAD_GLOBAL       'xrange'
3521	LOAD_FAST         'numGarbage'
3524	CALL_FUNCTION_1   None
3527	GET_ITER          None
3528	FOR_ITER          '3571'
3531	STORE_FAST        'i'

3534	LOAD_CONST        None
3537	YIELD_VALUE       None

3538	LOAD_FAST         's'
3541	LOAD_ATTR         'append'
3544	LOAD_FAST         'format'
3547	LOAD_FAST         'i'
3550	LOAD_FAST         'self'
3553	LOAD_ATTR         'referentsByReference'
3556	LOAD_FAST         'i'
3559	BINARY_SUBSCR     None
3560	BUILD_TUPLE_2     None
3563	BINARY_MODULO     None
3564	CALL_FUNCTION_1   None
3567	POP_TOP           None
3568	JUMP_BACK         '3528'
3571	POP_BLOCK         None
3572_0	COME_FROM         '3515'
3572	JUMP_ABSOLUTE     '3578'
3575	JUMP_FORWARD      '3578'
3578_0	COME_FROM         '3575'

3578	LOAD_FAST         's'
3581	LOAD_FAST         'self'
3584	STORE_ATTR        '_report'

3587	LOAD_FAST         'self'
3590	LOAD_ATTR         '_args'
3593	LOAD_ATTR         'log'
3596	JUMP_IF_FALSE     '3715'

3599	LOAD_FAST         'self'
3602	LOAD_ATTR         'printingBegin'
3605	CALL_FUNCTION_0   None
3608	POP_TOP           None

3609	SETUP_LOOP        '3686'
3612	LOAD_GLOBAL       'xrange'
3615	LOAD_GLOBAL       'len'
3618	LOAD_FAST         'self'
3621	LOAD_ATTR         '_report'
3624	CALL_FUNCTION_1   None
3627	CALL_FUNCTION_1   None
3630	GET_ITER          None
3631	FOR_ITER          '3685'
3634	STORE_FAST        'i'

3637	LOAD_FAST         'self'
3640	LOAD_ATTR         'numGarbage'
3643	LOAD_CONST        0
3646	COMPARE_OP        '>'
3649	JUMP_IF_FALSE     '3659'

3652	LOAD_CONST        None
3655	YIELD_VALUE       None
3656	JUMP_FORWARD      '3659'
3659_0	COME_FROM         '3656'

3659	LOAD_FAST         'self'
3662	LOAD_ATTR         'notify'
3665	LOAD_ATTR         'info'
3668	LOAD_FAST         'self'
3671	LOAD_ATTR         '_report'
3674	LOAD_FAST         'i'
3677	BINARY_SUBSCR     None
3678	CALL_FUNCTION_1   None
3681	POP_TOP           None
3682	JUMP_BACK         '3631'
3685	POP_BLOCK         None
3686_0	COME_FROM         '3609'

3686	LOAD_FAST         'self'
3689	LOAD_ATTR         'notify'
3692	LOAD_ATTR         'info'
3695	LOAD_CONST        '===== Garbage Report Done ====='
3698	CALL_FUNCTION_1   None
3701	POP_TOP           None

3702	LOAD_FAST         'self'
3705	LOAD_ATTR         'printingEnd'
3708	CALL_FUNCTION_0   None
3711	POP_TOP           None
3712	JUMP_FORWARD      '3715'
3715_0	COME_FROM         '3712'

3715	LOAD_GLOBAL       'Job'
3718	LOAD_ATTR         'Done'
3721	YIELD_VALUE       None
3722	LOAD_CONST        None
3725	RETURN_VALUE      None

Syntax error at or near `COME_FROM' token at offset 104_0

    def finished(self):
        if self._args.doneCallback:
            self._args.doneCallback(self)
        if self._args.autoDestroy:
            self.destroy()

    def destroy(self):
        del self._args
        del self.garbage
        del self.referrersByReference
        del self.referrersByNumber
        del self.referentsByReference
        del self.referentsByNumber
        if hasattr(self, 'cycles'):
            del self.cycles
        del self._report
        if hasattr(self, '_reportStr'):
            del self._reportStr
        Job.destroy(self)

    def getNumCycles(self):
        return self.numCycles

    def getDesc2numDict(self):
        desc2num = {}
        for cycleBySyntax in self.cyclesBySyntax:
            desc2num.setdefault(cycleBySyntax, 0)
            desc2num[cycleBySyntax] += 1

        return desc2num

    def getGarbage(self):
        return self.garbage

    def getReport(self):
        if not hasattr(self, '_reportStr'):
            self._reportStr = ''
            for str in self._report:
                self._reportStr += '\n' + str

        return self._reportStr

    def _getReferrers--- This code section failed: ---

0	LOAD_CONST        None
3	YIELD_VALUE       None

4	LOAD_GLOBAL       'gc'
7	LOAD_ATTR         'get_referrers'
10	LOAD_FAST         'obj'
13	CALL_FUNCTION_1   None
16	STORE_FAST        'byRef'

19	LOAD_CONST        None
22	YIELD_VALUE       None

23	BUILD_LIST_0      None
26	STORE_FAST        'byNum'

29	SETUP_LOOP        '125'
32	LOAD_GLOBAL       'xrange'
35	LOAD_GLOBAL       'len'
38	LOAD_FAST         'byRef'
41	CALL_FUNCTION_1   None
44	CALL_FUNCTION_1   None
47	GET_ITER          None
48	FOR_ITER          '124'
51	STORE_FAST        'i'

54	LOAD_FAST         'i'
57	LOAD_CONST        20
60	BINARY_MODULO     None
61	JUMP_IF_TRUE      '71'

64	LOAD_CONST        None
67	YIELD_VALUE       None
68	JUMP_FORWARD      '71'
71_0	COME_FROM         '68'

71	LOAD_FAST         'byRef'
74	LOAD_FAST         'i'
77	BINARY_SUBSCR     None
78	STORE_FAST        'referrer'

81	LOAD_FAST         'self'
84	LOAD_ATTR         '_id2index'
87	LOAD_ATTR         'get'
90	LOAD_GLOBAL       'id'
93	LOAD_FAST         'referrer'
96	CALL_FUNCTION_1   None
99	LOAD_CONST        None
102	CALL_FUNCTION_2   None
105	STORE_FAST        'num'

108	LOAD_FAST         'byNum'
111	LOAD_ATTR         'append'
114	LOAD_FAST         'num'
117	CALL_FUNCTION_1   None
120	POP_TOP           None
121	JUMP_BACK         '48'
124	POP_BLOCK         None
125_0	COME_FROM         '29'

125	LOAD_FAST         'byNum'
128	LOAD_FAST         'byRef'
131	BUILD_TUPLE_2     None
134	YIELD_VALUE       None
135	LOAD_CONST        None
138	RETURN_VALUE      None

Syntax error at or near `STORE_FAST' token at offset 16

    def _getReferents--- This code section failed: ---

0	LOAD_CONST        None
3	YIELD_VALUE       None

4	LOAD_GLOBAL       'gc'
7	LOAD_ATTR         'get_referents'
10	LOAD_FAST         'obj'
13	CALL_FUNCTION_1   None
16	STORE_FAST        'byRef'

19	LOAD_CONST        None
22	YIELD_VALUE       None

23	BUILD_LIST_0      None
26	STORE_FAST        'byNum'

29	SETUP_LOOP        '125'
32	LOAD_GLOBAL       'xrange'
35	LOAD_GLOBAL       'len'
38	LOAD_FAST         'byRef'
41	CALL_FUNCTION_1   None
44	CALL_FUNCTION_1   None
47	GET_ITER          None
48	FOR_ITER          '124'
51	STORE_FAST        'i'

54	LOAD_FAST         'i'
57	LOAD_CONST        20
60	BINARY_MODULO     None
61	JUMP_IF_TRUE      '71'

64	LOAD_CONST        None
67	YIELD_VALUE       None
68	JUMP_FORWARD      '71'
71_0	COME_FROM         '68'

71	LOAD_FAST         'byRef'
74	LOAD_FAST         'i'
77	BINARY_SUBSCR     None
78	STORE_FAST        'referent'

81	LOAD_FAST         'self'
84	LOAD_ATTR         '_id2index'
87	LOAD_ATTR         'get'
90	LOAD_GLOBAL       'id'
93	LOAD_FAST         'referent'
96	CALL_FUNCTION_1   None
99	LOAD_CONST        None
102	CALL_FUNCTION_2   None
105	STORE_FAST        'num'

108	LOAD_FAST         'byNum'
111	LOAD_ATTR         'append'
114	LOAD_FAST         'num'
117	CALL_FUNCTION_1   None
120	POP_TOP           None
121	JUMP_BACK         '48'
124	POP_BLOCK         None
125_0	COME_FROM         '29'

125	LOAD_FAST         'byNum'
128	LOAD_FAST         'byRef'
131	BUILD_TUPLE_2     None
134	YIELD_VALUE       None
135	LOAD_CONST        None
138	RETURN_VALUE      None

Syntax error at or near `STORE_FAST' token at offset 16

    def _getNormalizedCycle(self, cycle):
        if len(cycle) == 0:
            return cycle
        min = 1 << 30
        minIndex = None
        for i in xrange(len(cycle)):
            elem = cycle[i]
            if elem < min:
                min = elem
                minIndex = i

        return cycle[minIndex:] + cycle[:minIndex]

    def _getCycles--- This code section failed: ---

0	BUILD_LIST_0      None
3	STORE_FAST        'cycles'

6	LOAD_FAST         'uniqueCycleSets'
9	LOAD_CONST        None
12	COMPARE_OP        'is'
15	JUMP_IF_FALSE     '30'

18	LOAD_GLOBAL       'set'
21	CALL_FUNCTION_0   None
24	STORE_FAST        'uniqueCycleSets'
27	JUMP_FORWARD      '30'
30_0	COME_FROM         '27'

30	LOAD_GLOBAL       'Stack'
33	CALL_FUNCTION_0   None
36	STORE_FAST        'stateStack'

39	LOAD_FAST         'index'
42	STORE_FAST        'rootId'

45	LOAD_GLOBAL       'id'
48	LOAD_FAST         'self'
51	LOAD_ATTR         'garbage'
54	LOAD_FAST         'rootId'
57	BINARY_SUBSCR     None
58	CALL_FUNCTION_1   None
61	STORE_FAST        'objId'

64	LOAD_GLOBAL       'choice'
67	LOAD_FAST         'objId'
70	LOAD_FAST         'self'
73	LOAD_ATTR         'garbageInstanceIds'
76	COMPARE_OP        'in'
79	LOAD_CONST        1
82	LOAD_CONST        0
85	CALL_FUNCTION_3   None
88	STORE_FAST        'numDelInstances'

91	LOAD_FAST         'stateStack'
94	LOAD_ATTR         'push'
97	LOAD_FAST         'rootId'
100	BUILD_LIST_1      None
103	LOAD_FAST         'rootId'
106	LOAD_FAST         'numDelInstances'
109	LOAD_CONST        0
112	BUILD_TUPLE_4     None
115	CALL_FUNCTION_1   None
118	POP_TOP           None

119	SETUP_LOOP        '667'
122	LOAD_GLOBAL       'True'
125	JUMP_IF_FALSE     '666'

128	LOAD_CONST        None
131	YIELD_VALUE       None

132	LOAD_GLOBAL       'len'
135	LOAD_FAST         'stateStack'
138	CALL_FUNCTION_1   None
141	LOAD_CONST        0
144	COMPARE_OP        '=='
147	JUMP_IF_FALSE     '154'

150	BREAK_LOOP        None
151	JUMP_FORWARD      '154'
154_0	COME_FROM         '151'

154	LOAD_FAST         'stateStack'
157	LOAD_ATTR         'pop'
160	CALL_FUNCTION_0   None
163	UNPACK_SEQUENCE_4 None
166	STORE_FAST        'candidateCycle'
169	STORE_FAST        'curId'
172	STORE_FAST        'numDelInstances'
175	STORE_FAST        'resumeIndex'

178	LOAD_FAST         'self'
181	LOAD_ATTR         'notify'
184	LOAD_ATTR         'getDebug'
187	CALL_FUNCTION_0   None
190	JUMP_IF_FALSE     '256'

193	LOAD_FAST         'self'
196	LOAD_ATTR         '_args'
199	LOAD_ATTR         'delOnly'
202	JUMP_IF_FALSE     '232'

205	LOAD_CONST        'restart: %s root=%s cur=%s numDelInstances=%s resume=%s'
208	LOAD_FAST         'candidateCycle'
211	LOAD_FAST         'rootId'
214	LOAD_FAST         'curId'
217	LOAD_FAST         'numDelInstances'
220	LOAD_FAST         'resumeIndex'
223	BUILD_TUPLE_5     None
226	BINARY_MODULO     None
227	PRINT_ITEM        None
228	PRINT_NEWLINE_CONT None
229	JUMP_ABSOLUTE     '256'

232	LOAD_CONST        'restart: %s root=%s cur=%s resume=%s'
235	LOAD_FAST         'candidateCycle'
238	LOAD_FAST         'rootId'
241	LOAD_FAST         'curId'
244	LOAD_FAST         'resumeIndex'
247	BUILD_TUPLE_4     None
250	BINARY_MODULO     None
251	PRINT_ITEM        None
252	PRINT_NEWLINE_CONT None
253	JUMP_FORWARD      '256'
256_0	COME_FROM         '253'

256	SETUP_LOOP        '663'
259	LOAD_GLOBAL       'xrange'
262	LOAD_FAST         'resumeIndex'
265	LOAD_GLOBAL       'len'
268	LOAD_FAST         'self'
271	LOAD_ATTR         'referentsByNumber'
274	LOAD_FAST         'curId'
277	BINARY_SUBSCR     None
278	CALL_FUNCTION_1   None
281	CALL_FUNCTION_2   None
284	GET_ITER          None
285	FOR_ITER          '662'
288	STORE_FAST        'index'

291	LOAD_CONST        None
294	YIELD_VALUE       None

295	LOAD_FAST         'self'
298	LOAD_ATTR         'referentsByNumber'
301	LOAD_FAST         'curId'
304	BINARY_SUBSCR     None
305	LOAD_FAST         'index'
308	BINARY_SUBSCR     None
309	STORE_FAST        'refId'

312	LOAD_FAST         'self'
315	LOAD_ATTR         'notify'
318	LOAD_ATTR         'getDebug'
321	CALL_FUNCTION_0   None
324	JUMP_IF_FALSE     '345'

327	LOAD_CONST        '       : %s -> %s'
330	LOAD_FAST         'curId'
333	LOAD_FAST         'refId'
336	BUILD_TUPLE_2     None
339	BINARY_MODULO     None
340	PRINT_ITEM        None
341	PRINT_NEWLINE_CONT None
342	JUMP_FORWARD      '345'
345_0	COME_FROM         '342'

345	LOAD_FAST         'refId'
348	LOAD_FAST         'rootId'
351	COMPARE_OP        '=='
354	JUMP_IF_FALSE     '505'

357	LOAD_FAST         'self'
360	LOAD_ATTR         '_getNormalizedCycle'
363	LOAD_FAST         'candidateCycle'
366	CALL_FUNCTION_1   None
369	STORE_FAST        'normCandidateCycle'

372	LOAD_GLOBAL       'tuple'
375	LOAD_FAST         'normCandidateCycle'
378	CALL_FUNCTION_1   None
381	STORE_FAST        'normCandidateCycleTuple'

384	LOAD_FAST         'normCandidateCycleTuple'
387	LOAD_FAST         'uniqueCycleSets'
390	COMPARE_OP        'not in'
393	JUMP_IF_FALSE     '502'

396	LOAD_FAST         'self'
399	LOAD_ATTR         '_args'
402	LOAD_ATTR         'delOnly'
405	UNARY_NOT         None
406	JUMP_IF_TRUE      '421'
409	LOAD_FAST         'numDelInstances'
412	LOAD_CONST        1
415	COMPARE_OP        '>='
418_0	COME_FROM         '406'
418	JUMP_IF_FALSE     '499'

421	LOAD_FAST         'self'
424	LOAD_ATTR         'notify'
427	LOAD_ATTR         'getDebug'
430	CALL_FUNCTION_0   None
433	JUMP_IF_FALSE     '459'

436	LOAD_CONST        '  FOUND: '
439	PRINT_ITEM        None
440	LOAD_FAST         'normCandidateCycle'
443	LOAD_FAST         'normCandidateCycle'
446	LOAD_CONST        0
449	BINARY_SUBSCR     None
450	BUILD_LIST_1      None
453	BINARY_ADD        None
454	PRINT_ITEM_CONT   None
455	PRINT_NEWLINE_CONT None
456	JUMP_FORWARD      '459'
459_0	COME_FROM         '456'

459	LOAD_FAST         'cycles'
462	LOAD_ATTR         'append'
465	LOAD_FAST         'normCandidateCycle'
468	LOAD_FAST         'normCandidateCycle'

# Can't uncompyle C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\showbase\GarbageReport.pyc
Traceback (most recent call last):
  File "C:\python27\lib\uncompyle2\__init__.py", line 206, in main
    uncompyle_file(infile, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 143, in uncompyle_file
    uncompyle(version, co, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 132, in uncompyle
    raise walk.ERROR
ParserError: --- This code section failed: ---

0	BUILD_LIST_0      None
3	STORE_FAST        'cycles'

6	LOAD_FAST         'uniqueCycleSets'
9	LOAD_CONST        None
12	COMPARE_OP        'is'
15	JUMP_IF_FALSE     '30'

18	LOAD_GLOBAL       'set'
21	CALL_FUNCTION_0   None
24	STORE_FAST        'uniqueCycleSets'
27	JUMP_FORWARD      '30'
30_0	COME_FROM         '27'

30	LOAD_GLOBAL       'Stack'
33	CALL_FUNCTION_0   None
36	STORE_FAST        'stateStack'

39	LOAD_FAST         'index'
42	STORE_FAST        'rootId'

45	LOAD_GLOBAL       'id'
48	LOAD_FAST         'self'
51	LOAD_ATTR         'garbage'
54	LOAD_FAST         'rootId'
57	BINARY_SUBSCR     None
58	CALL_FUNCTION_1   None
61	STORE_FAST        'objId'

64	LOAD_GLOBAL       'choice'
67	LOAD_FAST         'objId'
70	LOAD_FAST         'self'
73	LOAD_ATTR         'garbageInstanceIds'
76	COMPARE_OP        'in'
79	LOAD_CONST        1
82	LOAD_CONST        0
85	CALL_FUNCTION_3   None
88	STORE_FAST        'numDelInstances'

91	LOAD_FAST         'stateStack'
94	LOAD_ATTR         'push'
97	LOAD_FAST         'rootId'
100	BUILD_LIST_1      None
103	LOAD_FAST         'rootId'
106	LOAD_FAST         'numDelInstances'
109	LOAD_CONST        0
112	BUILD_TUPLE_4     None
115	CALL_FUNCTION_1   None
118	POP_TOP           None

119	SETUP_LOOP        '667'
122	LOAD_GLOBAL       'True'
125	JUMP_IF_FALSE     '666'

128	LOAD_CONST        None
131	YIELD_VALUE       None

132	LOAD_GLOBAL       'len'
135	LOAD_FAST         'stateStack'
138	CALL_FUNCTION_1   None
141	LOAD_CONST        0
144	COMPARE_OP        '=='
147	JUMP_IF_FALSE     '154'

150	BREAK_LOOP        None
151	JUMP_FORWARD      '154'
154_0	COME_FROM         '151'

154	LOAD_FAST         'stateStack'
157	LOAD_ATTR         'pop'
160	CALL_FUNCTION_0   None
163	UNPACK_SEQUENCE_4 None
166	STORE_FAST        'candidateCycle'
169	STORE_FAST        'curId'
172	STORE_FAST        'numDelInstances'
175	STORE_FAST        'resumeIndex'

178	LOAD_FAST         'self'
181	LOAD_ATTR         'notify'
184	LOAD_ATTR         'getDebug'
187	CALL_FUNCTION_0   None
190	JUMP_IF_FALSE     '256'

193	LOAD_FAST         'self'
196	LOAD_ATTR         '_args'
199	LOAD_ATTR         'delOnly'
202	JUMP_IF_FALSE     '232'

205	LOAD_CONST        'restart: %s root=%s cur=%s numDelInstances=%s resume=%s'
208	LOAD_FAST         'candidateCycle'
211	LOAD_FAST         'rootId'
214	LOAD_FAST         'curId'
217	LOAD_FAST         'numDelInstances'
220	LOAD_FAST         'resumeIndex'
223	BUILD_TUPLE_5     None
226	BINARY_MODULO     None
227	PRINT_ITEM        None
228	PRINT_NEWLINE_CONT None
229	JUMP_ABSOLUTE     '256'

232	LOAD_CONST        'restart: %s root=%s cur=%s resume=%s'
235	LOAD_FAST         'candidateCycle'
238	LOAD_FAST         'rootId'
241	LOAD_FAST         'curId'
244	LOAD_FAST         'resumeIndex'
247	BUILD_TUPLE_4     None
250	BINARY_MODULO     None
251	PRINT_ITEM        None
252	PRINT_NEWLINE_CONT None
253	JUMP_FORWARD      '256'
256_0	COME_FROM         '253'

256	SETUP_LOOP        '663'
259	LOAD_GLOBAL       'xrange'
262	LOAD_FAST         'resumeIndex'
265	LOAD_GLOBAL       'len'
268	LOAD_FAST         'self'
271	LOAD_ATTR         'referentsByNumber'
274	LOAD_FAST         'curId'
277	BINARY_SUBSCR     None
278	CALL_FUNCTION_1   None
281	CALL_FUNCTION_2   None
284	GET_ITER          None
285	FOR_ITER          '662'
288	STORE_FAST        'index'

291	LOAD_CONST        None
294	YIELD_VALUE       None

295	LOAD_FAST         'self'
298	LOAD_ATTR         'referentsByNumber'
301	LOAD_FAST         'curId'
304	BINARY_SUBSCR     None
305	LOAD_FAST         'index'
308	BINARY_SUBSCR     None
309	STORE_FAST        'refId'

312	LOAD_FAST         'self'
315	LOAD_ATTR         'notify'
318	LOAD_ATTR         'getDebug'
321	CALL_FUNCTION_0   None
324	JUMP_IF_FALSE     '345'

327	LOAD_CONST        '       : %s -> %s'
330	LOAD_FAST         'curId'
333	LOAD_FAST         'refId'
336	BUILD_TUPLE_2     None
339	BINARY_MODULO     None
340	PRINT_ITEM        None
341	PRINT_NEWLINE_CONT None
342	JUMP_FORWARD      '345'
345_0	COME_FROM         '342'

345	LOAD_FAST         'refId'
348	LOAD_FAST         'rootId'
351	COMPARE_OP        '=='
354	JUMP_IF_FALSE     '505'

357	LOAD_FAST         'self'
360	LOAD_ATTR         '_getNormalizedCycle'
363	LOAD_FAST         'candidateCycle'
366	CALL_FUNCTION_1   None
369	STORE_FAST        'normCandidateCycle'

372	LOAD_GLOBAL       'tuple'
375	LOAD_FAST         'normCandidateCycle'
378	CALL_FUNCTION_1   None
381	STORE_FAST        'normCandidateCycleTuple'

384	LOAD_FAST         'normCandidateCycleTuple'
387	LOAD_FAST         'uniqueCycleSets'
390	COMPARE_OP        'not in'
393	JUMP_IF_FALSE     '502'

396	LOAD_FAST         'self'
399	LOAD_ATTR         '_args'
402	LOAD_ATTR         'delOnly'
405	UNARY_NOT         None
406	JUMP_IF_TRUE      '421'
409	LOAD_FAST         'numDelInstances'
412	LOAD_CONST        1
415	COMPARE_OP        '>='
418_0	COME_FROM         '406'
418	JUMP_IF_FALSE     '499'

421	LOAD_FAST         'self'
424	LOAD_ATTR         'notify'
427	LOAD_ATTR         'getDebug'
430	CALL_FUNCTION_0   None
433	JUMP_IF_FALSE     '459'

436	LOAD_CONST        '  FOUND: '
439	PRINT_ITEM        None
440	LOAD_FAST         'normCandidateCycle'
443	LOAD_FAST         'normCandidateCycle'
446	LOAD_CONST        0
449	BINARY_SUBSCR     None
450	BUILD_LIST_1      None
453	BINARY_ADD        None
454	PRINT_ITEM_CONT   None
455	PRINT_NEWLINE_CONT None
456	JUMP_FORWARD      '459'
459_0	COME_FROM         '456'

459	LOAD_FAST         'cycles'
462	LOAD_ATTR         'append'
465	LOAD_FAST         'normCandidateCycle'
468	LOAD_FAST         'normCandidateCycle'
471	LOAD_CONST        0
474	BINARY_SUBSCR     None
475	BUILD_LIST_1      None
478	BINARY_ADD        None
479	CALL_FUNCTION_1   None
482	POP_TOP           None

483	LOAD_FAST         'uniqueCycleSets'
486	LOAD_ATTR         'add'
489	LOAD_FAST         'normCandidateCycleTuple'
492	CALL_FUNCTION_1   None
495	POP_TOP           None
496	JUMP_ABSOLUTE     '502'
499	JUMP_ABSOLUTE     '659'
502	JUMP_BACK         '285'

505	LOAD_FAST         'refId'
508	LOAD_FAST         'candidateCycle'
511	COMPARE_OP        'in'
514	JUMP_IF_FALSE     '520'

517	JUMP_BACK         '285'

520	LOAD_FAST         'refId'
523	LOAD_CONST        None
526	COMPARE_OP        'is not'
529	JUMP_IF_FALSE     '659'

532	LOAD_GLOBAL       'id'
535	LOAD_FAST         'self'
538	LOAD_ATTR         'garbage'
541	LOAD_FAST         'refId'
544	BINARY_SUBSCR     None
545	CALL_FUNCTION_1   None
548	STORE_FAST        'objId'

551	LOAD_FAST         'numDelInstances'
554	LOAD_GLOBAL       'choice'
557	LOAD_FAST         'objId'
560	LOAD_FAST         'self'
563	LOAD_ATTR         'garbageInstanceIds'
566	COMPARE_OP        'in'
569	LOAD_CONST        1
572	LOAD_CONST        0
575	CALL_FUNCTION_3   None
578	INPLACE_ADD       None
579	STORE_FAST        'numDelInstances'

582	LOAD_FAST         'stateStack'
585	LOAD_ATTR         'push'
588	LOAD_GLOBAL       'list'
591	LOAD_FAST         'candidateCycle'
594	CALL_FUNCTION_1   None
597	LOAD_FAST         'curId'
600	LOAD_FAST         'numDelInstances'
603	LOAD_FAST         'index'
606	LOAD_CONST        1
609	BINARY_ADD        None
610	BUILD_TUPLE_4     None
613	CALL_FUNCTION_1   None
616	POP_TOP           None

617	LOAD_FAST         'stateStack'
620	LOAD_ATTR         'push'
623	LOAD_GLOBAL       'list'
626	LOAD_FAST         'candidateCycle'
629	CALL_FUNCTION_1   None
632	LOAD_FAST         'refId'
635	BUILD_LIST_1      None
638	BINARY_ADD        None
639	LOAD_FAST         'refId'
642	LOAD_FAST         'numDelInstances'
645	LOAD_CONST        0
648	BUILD_TUPLE_4     None
651	CALL_FUNCTION_1   None
654	POP_TOP           None

655	BREAK_LOOP        None
656	JUMP_BACK 471	LOAD_CONST        0
474	BINARY_SUBSCR     None
475	BUILD_LIST_1      None
478	BINARY_ADD        None
479	CALL_FUNCTION_1   None
482	POP_TOP           None

483	LOAD_FAST         'uniqueCycleSets'
486	LOAD_ATTR         'add'
489	LOAD_FAST         'normCandidateCycleTuple'
492	CALL_FUNCTION_1   None
495	POP_TOP           None
496	JUMP_ABSOLUTE     '502'
499	JUMP_ABSOLUTE     '659'
502	JUMP_BACK         '285'

505	LOAD_FAST         'refId'
508	LOAD_FAST         'candidateCycle'
511	COMPARE_OP        'in'
514	JUMP_IF_FALSE     '520'

517	JUMP_BACK         '285'

520	LOAD_FAST         'refId'
523	LOAD_CONST        None
526	COMPARE_OP        'is not'
529	JUMP_IF_FALSE     '659'

532	LOAD_GLOBAL       'id'
535	LOAD_FAST         'self'
538	LOAD_ATTR         'garbage'
541	LOAD_FAST         'refId'
544	BINARY_SUBSCR     None
545	CALL_FUNCTION_1   None
548	STORE_FAST        'objId'

551	LOAD_FAST         'numDelInstances'
554	LOAD_GLOBAL       'choice'
557	LOAD_FAST         'objId'
560	LOAD_FAST         'self'
563	LOAD_ATTR         'garbageInstanceIds'
566	COMPARE_OP        'in'
569	LOAD_CONST        1
572	LOAD_CONST        0
575	CALL_FUNCTION_3   None
578	INPLACE_ADD       None
579	STORE_FAST        'numDelInstances'

582	LOAD_FAST         'stateStack'
585	LOAD_ATTR         'push'
588	LOAD_GLOBAL       'list'
591	LOAD_FAST         'candidateCycle'
594	CALL_FUNCTION_1   None
597	LOAD_FAST         'curId'
600	LOAD_FAST         'numDelInstances'
603	LOAD_FAST         'index'
606	LOAD_CONST        1
609	BINARY_ADD        None
610	BUILD_TUPLE_4     None
613	CALL_FUNCTION_1   None
616	POP_TOP           None

617	LOAD_FAST         'stateStack'
620	LOAD_ATTR         'push'
623	LOAD_GLOBAL       'list'
626	LOAD_FAST         'candidateCycle'
629	CALL_FUNCTION_1   None
632	LOAD_FAST         'refId'
635	BUILD_LIST_1      None
638	BINARY_ADD        None
639	LOAD_FAST         'refId'
642	LOAD_FAST         'numDelInstances'
645	LOAD_CONST        0
648	BUILD_TUPLE_4     None
651	CALL_FUNCTION_1   None
654	POP_TOP           None

655	BREAK_LOOP        None
656	JUMP_BACK         '285'
659	JUMP_BACK         '285'
662	POP_BLOCK         None
663_0	COME_FROM         '256'
663	JUMP_BACK         '122'
666	POP_BLOCK         None
667_0	COME_FROM         '119'

667	LOAD_FAST         'cycles'
670	YIELD_VALUE       None
671	LOAD_CONST        None
674	RETURN_VALUE      None

Syntax error at or near `BREAK_LOOP' token at offset 150


class GarbageLogger(GarbageReport):
    __module__ = __name__

    def __init__(self, name, *args, **kArgs):
        kArgs['log'] = True
        kArgs['autoDestroy'] = True
        GarbageReport.__init__(self, name, *args, **kArgs)


class _CFGLGlobals():
    __module__ = __name__
    LastNumGarbage = 0
    LastNumCycles = 0


def checkForGarbageLeaks():
    gc.collect()
    numGarbage = len(gc.garbage)
    if numGarbage > 0 and config.GetBool('auto-garbage-logging', 0):
        if numGarbage != _CFGLGlobals.LastNumGarbage:
            print
            gr = GarbageReport('found garbage', threaded=False, collect=False)
            print
            _CFGLGlobals.LastNumGarbage = numGarbage
            _CFGLGlobals.LastNumCycles = gr.getNumCycles()
            messenger.send(GarbageCycleCountAnnounceEvent, [gr.getDesc2numDict()])
            gr.destroy()
        notify = directNotify.newCategory('GarbageDetect')
        if config.GetBool('allow-garbage-cycles', 1):
            func = notify.warning
        else:
            func = notify.error
        func('%s garbage cycles found, see info above' % _CFGLGlobals.LastNumCycles)
    return numGarbage


def b_checkForGarbageLeaks(wantReply = False):
    if not __dev__:
        return 0
    try:
        base.cr.timeManager
    except:
        pass
    else:
        if base.cr.timeManager:
            base.cr.timeManager.d_checkForGarbageLeaks(wantReply=wantReply)

    return checkForGarbageLeaks()# decompiled 0 files: 0 okay, 1 failed, 0 verify failed
# 2013.08.22 22:14:35 Pacific Daylight Time
        '285'
659	JUMP_BACK         '285'
662	POP_BLOCK         None
663_0	COME_FROM         '256'
663	JUMP_BACK         '122'
666	POP_BLOCK         None
667_0	COME_FROM         '119'

667	LOAD_FAST         'cycles'
670	YIELD_VALUE       None
671	LOAD_CONST        None
674	RETURN_VALUE      None

Syntax error at or near `BREAK_LOOP' token at offset 150

