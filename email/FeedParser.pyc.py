# 2013.08.22 22:14:58 Pacific Daylight Time
# Embedded file name: email.FeedParser
import re
from email import Errors
from email import Message
NLCRE = re.compile('\r\n|\r|\n')
NLCRE_bol = re.compile('(\r\n|\r|\n)')
NLCRE_eol = re.compile('(\r\n|\r|\n)$')
NLCRE_crack = re.compile('(\r\n|\r|\n)')
headerRE = re.compile('^(From |[\\041-\\071\\073-\\176]{2,}:|[\\t ])')
EMPTYSTRING = ''
NL = '\n'
NeedMoreData = object()

class BufferedSubFile(object):
    __module__ = __name__

    def __init__(self):
        self._partial = ''
        self._lines = []
        self._eofstack = []
        self._closed = False

    def push_eof_matcher(self, pred):
        self._eofstack.append(pred)

    def pop_eof_matcher(self):
        return self._eofstack.pop()

    def close(self):
        self._lines.append(self._partial)
        self._partial = ''
        self._closed = True

    def readline(self):
        if not self._lines:
            if self._closed:
                return ''
            return NeedMoreData
        line = self._lines.pop()
        for ateof in self._eofstack[::-1]:
            if ateof(line):
                self._lines.append(line)
                return ''

        return line

    def unreadline(self, line):
        self._lines.append(line)

    def push(self, data):
        data, self._partial = self._partial + data, ''
        parts = NLCRE_crack.split(data)
        self._partial = parts.pop()
        lines = []
        for i in range(len(parts) // 2):
            lines.append(parts[i * 2] + parts[i * 2 + 1])

        self.pushlines(lines)

    def pushlines(self, lines):
        self._lines[:0] = lines[::-1]

    def is_closed(self):
        return self._closed

    def __iter__(self):
        return self

    def next(self):
        line = self.readline()
        if line == '':
            raise StopIteration
        return line


class FeedParser():
    __module__ = __name__

    def __init__(self, _factory = Message.Message):
        self._factory = _factory
        self._input = BufferedSubFile()
        self._msgstack = []
        self._parse = self._parsegen().next
        self._cur = None
        self._last = None
        self._headersonly = False
        return

    def _set_headersonly(self):
        self._headersonly = True

    def feed(self, data):
        self._input.push(data)
        self._call_parse()

    def _call_parse(self):
        try:
            self._parse()
        except StopIteration:
            pass

    def close(self):
        self._input.close()
        self._call_parse()
        root = self._pop_message()
        if root.get_content_maintype() == 'multipart' and not root.is_multipart():
            root.defects.append(Errors.MultipartInvariantViolationDefect())
        return root

    def _new_message(self):
        msg = self._factory()
        if self._cur and self._cur.get_content_type() == 'multipart/digest':
            msg.set_default_type('message/rfc822')
        if self._msgstack:
            self._msgstack[-1].attach(msg)
        self._msgstack.append(msg)
        self._cur = msg
        self._last = msg

    def _pop_message(self):
        retval = self._msgstack.pop()
        if self._msgstack:
            self._cur = self._msgstack[-1]
        else:
            self._cur = None
        return retval

    def _parsegen--- This code section failed: ---

0	LOAD_FAST         'self'
3	LOAD_ATTR         '_new_message'
6	CALL_FUNCTION_0   None
9	POP_TOP           None

10	BUILD_LIST_0      None
13	STORE_FAST        'headers'

16	SETUP_LOOP        '124'
19	LOAD_FAST         'self'
22	LOAD_ATTR         '_input'
25	GET_ITER          None
26	FOR_ITER          '123'
29	STORE_FAST        'line'

32	LOAD_FAST         'line'
35	LOAD_GLOBAL       'NeedMoreData'
38	COMPARE_OP        'is'
41	JUMP_IF_FALSE     '54'

44	LOAD_GLOBAL       'NeedMoreData'
47	YIELD_VALUE       None

48	CONTINUE          '26'
51	JUMP_FORWARD      '54'
54_0	COME_FROM         '51'

54	LOAD_GLOBAL       'headerRE'
57	LOAD_ATTR         'match'
60	LOAD_FAST         'line'
63	CALL_FUNCTION_1   None
66	JUMP_IF_TRUE      '107'

69	LOAD_GLOBAL       'NLCRE'
72	LOAD_ATTR         'match'
75	LOAD_FAST         'line'
78	CALL_FUNCTION_1   None
81	JUMP_IF_TRUE      '103'

84	LOAD_FAST         'self'
87	LOAD_ATTR         '_input'
90	LOAD_ATTR         'unreadline'
93	LOAD_FAST         'line'
96	CALL_FUNCTION_1   None
99	POP_TOP           None
100	JUMP_FORWARD      '103'
103_0	COME_FROM         '100'

103	BREAK_LOOP        None
104	JUMP_FORWARD      '107'
107_0	COME_FROM         '104'

107	LOAD_FAST         'headers'
110	LOAD_ATTR         'append'
113	LOAD_FAST         'line'
116	CALL_FUNCTION_1   None
119	POP_TOP           None
120	JUMP_BACK         '26'
123	POP_BLOCK         None
124_0	COME_FROM         '16'

124	LOAD_FAST         'self'
127	LOAD_ATTR         '_parse_headers'
130	LOAD_FAST         'headers'
133	CALL_FUNCTION_1   None
136	POP_TOP           None

137	LOAD_FAST         'self'
140	LOAD_ATTR         '_headersonly'
143	JUMP_IF_FALSE     '263'

146	BUILD_LIST_0      None
149	STORE_FAST        'lines'

152	SETUP_LOOP        '231'
155	LOAD_GLOBAL       'True'
158	JUMP_IF_FALSE     '230'

161	LOAD_FAST         'self'
164	LOAD_ATTR         '_input'
167	LOAD_ATTR         'readline'
170	CALL_FUNCTION_0   None
173	STORE_FAST        'line'

176	LOAD_FAST         'line'
179	LOAD_GLOBAL       'NeedMoreData'
182	COMPARE_OP        'is'
185	JUMP_IF_FALSE     '198'

188	LOAD_GLOBAL       'NeedMoreData'
191	YIELD_VALUE       None

192	CONTINUE          '155'
195	JUMP_FORWARD      '198'
198_0	COME_FROM         '195'

198	LOAD_FAST         'line'
201	LOAD_CONST        ''
204	COMPARE_OP        '=='
207	JUMP_IF_FALSE     '214'

210	BREAK_LOOP        None
211	JUMP_FORWARD      '214'
214_0	COME_FROM         '211'

214	LOAD_FAST         'lines'
217	LOAD_ATTR         'append'
220	LOAD_FAST         'line'
223	CALL_FUNCTION_1   None
226	POP_TOP           None
227	JUMP_BACK         '155'
230	POP_BLOCK         None
231_0	COME_FROM         '152'

231	LOAD_FAST         'self'
234	LOAD_ATTR         '_cur'
237	LOAD_ATTR         'set_payload'
240	LOAD_GLOBAL       'EMPTYSTRING'
243	LOAD_ATTR         'join'
246	LOAD_FAST         'lines'
249	CALL_FUNCTION_1   None
252	CALL_FUNCTION_1   None
255	POP_TOP           None

256	LOAD_CONST        None
259	RETURN_VALUE      None
260	JUMP_FORWARD      '263'
263_0	COME_FROM         '260'

263	LOAD_FAST         'self'
266	LOAD_ATTR         '_cur'
269	LOAD_ATTR         'get_content_type'
272	CALL_FUNCTION_0   None
275	LOAD_CONST        'message/delivery-status'
278	COMPARE_OP        '=='
281	JUMP_IF_FALSE     '528'

284	SETUP_LOOP        '521'
287	LOAD_GLOBAL       'True'
290	JUMP_IF_FALSE     '520'

293	LOAD_FAST         'self'
296	LOAD_ATTR         '_input'
299	LOAD_ATTR         'push_eof_matcher'
302	LOAD_GLOBAL       'NLCRE'
305	LOAD_ATTR         'match'
308	CALL_FUNCTION_1   None
311	POP_TOP           None

312	SETUP_LOOP        '358'
315	LOAD_FAST         'self'
318	LOAD_ATTR         '_parsegen'
321	CALL_FUNCTION_0   None
324	GET_ITER          None
325	FOR_ITER          '357'
328	STORE_FAST        'retval'

331	LOAD_FAST         'retval'
334	LOAD_GLOBAL       'NeedMoreData'
337	COMPARE_OP        'is'
340	JUMP_IF_FALSE     '353'

343	LOAD_GLOBAL       'NeedMoreData'
346	YIELD_VALUE       None

347	CONTINUE          '325'
350	JUMP_FORWARD      '353'
353_0	COME_FROM         '350'

353	BREAK_LOOP        None
354	JUMP_BACK         '325'
357	POP_BLOCK         None
358_0	COME_FROM         '312'

358	LOAD_FAST         'self'
361	LOAD_ATTR         '_pop_message'
364	CALL_FUNCTION_0   None
367	STORE_FAST        'msg'

370	LOAD_FAST         'self'
373	LOAD_ATTR         '_input'
376	LOAD_ATTR         'pop_eof_matcher'
379	CALL_FUNCTION_0   None
382	POP_TOP           None

383	SETUP_LOOP        '434'
386	LOAD_GLOBAL       'True'
389	JUMP_IF_FALSE     '433'

392	LOAD_FAST         'self'
395	LOAD_ATTR         '_input'
398	LOAD_ATTR         'readline'
401	CALL_FUNCTION_0   None
404	STORE_FAST        'line'

407	LOAD_FAST         'line'
410	LOAD_GLOBAL       'NeedMoreData'
413	COMPARE_OP        'is'
416	JUMP_IF_FALSE     '429'

419	LOAD_GLOBAL       'NeedMoreData'
422	YIELD_VALUE       None

423	CONTINUE          '386'
426	JUMP_FORWARD      '429'
429_0	COME_FROM         '426'

429	BREAK_LOOP        None
430	JUMP_BACK         '386'
433	POP_BLOCK         None
434_0	COME_FROM         '383'

434	SETUP_LOOP        '485'
437	LOAD_GLOBAL       'True'
440	JUMP_IF_FALSE     '484'

443	LOAD_FAST         'self'
446	LOAD_ATTR         '_input'
449	LOAD_ATTR         'readline'
452	CALL_FUNCTION_0   None
455	STORE_FAST        'line'

458	LOAD_FAST         'line'
461	LOAD_GLOBAL       'NeedMoreData'
464	COMPARE_OP        'is'
467	JUMP_IF_FALSE     '480'

470	LOAD_GLOBAL       'NeedMoreData'
473	YIELD_VALUE       None

474	CONTINUE          '437'
477	JUMP_FORWARD      '480'
480_0	COME_FROM         '477'

480	BREAK_LOOP        None
481	JUMP_BACK         '437'
484	POP_BLOCK         None
485_0	COME_FROM         '434'

485	LOAD_FAST         'line'
488	LOAD_CONST        ''
491	COMPARE_OP        '=='
494	JUMP_IF_FALSE     '501'

497	BREAK_LOOP        None
498	JUMP_FORWARD      '501'
501_0	COME_FROM         '498'

501	LOAD_FAST         'self'
504	LOAD_ATTR         '_input'
507	LOAD_ATTR         'unreadline'
510	LOAD_FAST         'line'
513	CALL_FUNCTION_1   None
516	POP_TOP           None
517	JUMP_BACK         '287'
520	POP_BLOCK         None
521_0	COME_FROM         '284'

521	LOAD_CONST        None
524	RETURN_VALUE      None
525	JUMP_FORWARD      '528'
528_0	COME_FROM         '525'

528	LOAD_FAST         'self'
531	LOAD_ATTR         '_cur'
534	LOAD_ATTR         'get_content_maintype'
537	CALL_FUNCTION_0   None
540	LOAD_CONST        'message'
543	COMPARE_OP        '=='
546	JUMP_IF_FALSE     '612'

549	SETUP_LOOP        '595'
552	LOAD_FAST         'self'
555	LOAD_ATTR         '_parsegen'
558	CALL_FUNCTION_0   None
561	GET_ITER          None
562	FOR_ITER          '594'
565	STORE_FAST        'retval'

568	LOAD_FAST         'retval'
571	LOAD_GLOBAL       'NeedMoreData'
574	COMPARE_OP        'is'
577	JUMP_IF_FALSE     '590'

580	LOAD_GLOBAL       'NeedMoreData'
583	YIELD_VALUE       None

584	CONTINUE          '562'
587	JUMP_FORWARD      '590'
590_0	COME_FROM         '587'

590	BREAK_LOOP        None
591	JUMP_BACK         '562'
594	POP_BLOCK         None
595_0	COME_FROM         '549'

595	LOAD_FAST         'self'
598	LOAD_ATTR         '_pop_message'
601	CALL_FUNCTION_0   None
604	POP_TOP           None

605	LOAD_CONST        None
608	RETURN_VALUE      None
609	JUMP_FORWARD      '612'
612_0	COME_FROM         '609'

612	LOAD_FAST         'self'
615	LOAD_ATTR         '_cur'
618	LOAD_ATTR         'get_content_maintype'
621	CALL_FUNCTION_0   None
624	LOAD_CONST        'multipart'
627	COMPARE_OP        '=='
630	JUMP_IF_FALSE     '1844'

633	LOAD_FAST         'self'
636	LOAD_ATTR         '_cur'
639	LOAD_ATTR         'get_boundary'
642	CALL_FUNCTION_0   None
645	STORE_FAST        'boundary'

648	LOAD_FAST         'boundary'
651	LOAD_CONST        None
654	COMPARE_OP        'is'
657	JUMP_IF_FALSE     '778'

660	LOAD_FAST         'self'
663	LOAD_ATTR         '_cur'
666	LOAD_ATTR         'defects'
669	LOAD_ATTR         'append'
672	LOAD_GLOBAL       'Errors'
675	LOAD_ATTR         'NoBoundaryInMultipartDefect'
678	CALL_FUNCTION_0   None
681	CALL_FUNCTION_1   None
684	POP_TOP           None

685	BUILD_LIST_0      None
688	STORE_FAST        'lines'

691	SETUP_LOOP        '746'
694	LOAD_FAST         'self'
697	LOAD_ATTR         '_input'
700	GET_ITER          None
701	FOR_ITER          '745'
704	STORE_FAST        'line'

707	LOAD_FAST         'line'
710	LOAD_GLOBAL       'NeedMoreData'
713	COMPARE_OP        'is'
716	JUMP_IF_FALSE     '729'

719	LOAD_GLOBAL       'NeedMoreData'
722	YIELD_VALUE       None

723	CONTINUE          '701'
726	JUMP_FORWARD      '729'
729_0	COME_FROM         '726'

729	LOAD_FAST         'lines'
732	LOAD_ATTR         'append'
735	LOAD_FAST         'line'
738	CALL_FUNCTION_1   None
741	POP_TOP           None
742	JUMP_BACK         '701'
745	POP_BLOCK         None
746_0	COME_FROM         '691'

746	LOAD_FAST         'self'
749	LOAD_ATTR         '_cur'
752	LOAD_ATTR         'set_payload'
755	LOAD_GLOBAL       'EMPTYSTRING'
758	LOAD_ATTR         'join'
761	LOAD_FAST         'lines'
764	CALL_FUNCTION_1   None
767	CALL_FUNCTION_1   None
770	POP_TOP           None

771	LOAD_CONST        None
774	RETURN_VALUE      None
775	JUMP_FORWARD      '778'
778_0	COME_FROM         '775'

778	LOAD_CONST        '--'
781	LOAD_FAST         'boundary'
784	BINARY_ADD        None
785	STORE_FAST        'separator'

788	LOAD_GLOBAL       're'
791	LOAD_ATTR         'compile'
794	LOAD_CONST        '(?P<sep>'
797	LOAD_GLOBAL       're'
800	LOAD_ATTR         'escape'
803	LOAD_FAST         'separator'
806	CALL_FUNCTION_1   None
809	BINARY_ADD        None
810	LOAD_CONST        ')(?P<end>--)?(?P<ws>[ \\t]*)(?P<linesep>\\r\\n|\\r|\\n)?$'
813	BINARY_ADD        None
814	CALL_FUNCTION_1   None
817	STORE_FAST        'boundaryre'

820	LOAD_GLOBAL       'True'
823	STORE_FAST        'capturing_preamble'

826	BUILD_LIST_0      None
829	STORE_FAST        'preamble'

832	LOAD_GLOBAL       'False'
835	STORE_FAST        'linesep'

838	SETUP_LOOP        '1533'
841	LOAD_GLOBAL       'True'
844	JUMP_IF_FALSE     '1532'

847	LOAD_FAST         'self'
850	LOAD_ATTR         '_input'
853	LOAD_ATTR         'readline'
856	CALL_FUNCTION_0   None
859	STORE_FAST        'line'

862	LOAD_FAST         'line'
865	LOAD_GLOBAL       'NeedMoreData'
868	COMPARE_OP        'is'
871	JUMP_IF_FALSE     '884'

874	LOAD_GLOBAL       'NeedMoreData'
877	YIELD_VALUE       None

878	CONTINUE          '841'
881	JUMP_FORWARD      '884'
884_0	COME_FROM         '881'

884	LOAD_FAST         'line'
887	LOAD_CONST        ''
890	COMPARE_OP        '=='
893	JUMP_IF_FALSE     '900'

896	BREAK_LOOP        None
897	JUMP_FORWARD      '900'
900_0	COME_FROM         '897'

900	LOAD_FAST         'boundaryre'
903	LOAD_ATTR         'match'
906	LOAD_FAST         'line'
909	CALL_FUNCTION_1   None
912	STORE_FAST        'mo'

915	LOAD_FAST         'mo'
918	JUMP_IF_FALSE     '1516'

921	LOAD_FAST         'mo'
924	LOAD_ATTR         'group'
927	LOAD_CONST        'end'
930	CALL_FUNCTION_1   None
933	JUMP_IF_FALSE     '955'

936	LOAD_FAST         'mo'
939	LOAD_ATTR         'group'
942	LOAD_CONST        'linesep'
945	CALL_FUNCTION_1   None
948	STORE_FAST        'linesep'

951	BREAK_LOOP        None
952	JUMP_FORWARD      '955'
955_0	COME_FROM         '952'

955	LOAD_FAST         'capturing_preamble'
958	JUMP_IF_FALSE     '1083'

961	LOAD_FAST         'preamble'
964	JUMP_IF_FALSE     '1055'

967	LOAD_FAST         'preamble'
970	LOAD_CONST        -1
973	BINARY_SUBSCR     None
974	STORE_FAST        'lastline'

977	LOAD_GLOBAL       'NLCRE_eol'
980	LOAD_ATTR         'search'
983	LOAD_FAST         'lastline'
986	CALL_FUNCTION_1   None
989	STORE_FAST        'eolmo'

992	LOAD_FAST         'eolmo'
995	JUMP_IF_FALSE     '1031'

998	LOAD_FAST         'lastline'
1001	LOAD_GLOBAL       'len'
1004	LOAD_FAST         'eolmo'
1007	LOAD_ATTR         'group'
1010	LOAD_CONST        0
1013	CALL_FUNCTION_1   None
1016	CALL_FUNCTION_1   None
1019	UNARY_NEGATIVE    None
1020	SLICE+2           None
1021	LOAD_FAST         'preamble'
1024	LOAD_CONST        -1
1027	STORE_SUBSCR      None
1028	JUMP_FORWARD      '1031'
1031_0	COME_FROM         '1028'

1031	LOAD_GLOBAL       'EMPTYSTRING'
1034	LOAD_ATTR         'join'
1037	LOAD_FAST         'preamble'
1040	CALL_FUNCTION_1   None
1043	LOAD_FAST         'self'
1046	LOAD_ATTR         '_cur'
1049	STORE_ATTR        'preamble'
1052	JUMP_FORWARD      '1055'
1055_0	COME_FROM         '1052'

1055	LOAD_GLOBAL       'False'
1058	STORE_FAST        'capturing_preamble'

1061	LOAD_FAST         'self'
1064	LOAD_ATTR         '_input'
1067	LOAD_ATTR         'unreadline'
1070	LOAD_FAST         'line'
1073	CALL_FUNCTION_1   None
1076	POP_TOP           None

1077	CONTINUE          '841'
1080	JUMP_FORWARD      '1083'
1083_0	COME_FROM         '1080'

1083	SETUP_LOOP        '1174'
1086	LOAD_GLOBAL       'True'
1089	JUMP_IF_FALSE     '1173'

1092	LOAD_FAST         'self'
1095	LOAD_ATTR         '_input'
1098	LOAD_ATTR         'readline'
1101	CALL_FUNCTION_0   None
1104	STORE_FAST        'line'

1107	LOAD_FAST         'line'
1110	LOAD_GLOBAL       'NeedMoreData'
1113	COMPARE_OP        'is'
1116	JUMP_IF_FALSE     '1129'

1119	LOAD_GLOBAL       'NeedMoreData'
1122	YIELD_VALUE       None

1123	CONTINUE          '1086'
1126	JUMP_FORWARD      '1129'
1129_0	COME_FROM         '1126'

1129	LOAD_FAST         'boundaryre'
1132	LOAD_ATTR         'match'
1135	LOAD_FAST         'line'
1138	CALL_FUNCTION_1   None
1141	STORE_FAST        'mo'

1144	LOAD_FAST         'mo'
1147	JUMP_IF_TRUE      '1170'

1150	LOAD_FAST         'self'
1153	LOAD_ATTR         '_input'
1156	LOAD_ATTR         'unreadline'
1159	LOAD_FAST         'line'
1162	CALL_FUNCTION_1   None
1165	POP_TOP           None

1166	BREAK_LOOP        None
1167	JUMP_BACK         '1086'
1170	JUMP_BACK         '1086'
1173	POP_BLOCK         None
1174_0	COME_FROM         '1083'

1174	LOAD_FAST         'self'
1177	LOAD_ATTR         '_input'
1180	LOAD_ATTR         'push_eof_matcher'
1183	LOAD_FAST         'boundaryre'
1186	LOAD_ATTR         'match'
1189	CALL_FUNCTION_1   None
1192	POP_TOP           None

1193	SETUP_LOOP        '1239'
1196	LOAD_FAST         'self'
1199	LOAD_ATTR         '_parsegen'
1202	CALL_FUNCTION_0   None
1205	GET_ITER          None
1206	FOR_ITER          '1238'
1209	STORE_FAST        'retval'

1212	LOAD_FAST         'retval'
1215	LOAD_GLOBAL       'NeedMoreData'
1218	COMPARE_OP        'is'
1221	JUMP_IF_FALSE     '1234'

1224	LOAD_GLOBAL       'NeedMoreData'
1227	YIELD_VALUE       None

1228	CONTINUE          '1206'
1231	JUMP_FORWARD      '1234'
1234_0	COME_FROM         '1231'

1234	BREAK_LOOP        None
1235	JUMP_BACK         '1206'
1238	POP_BLOCK         None
1239_0	COME_FROM         '1193'

1239	LOAD_FAST         'self'
1242	LOAD_ATTR         '_last'
1245	LOAD_ATTR         'get_content_maintype'
1248	CALL_FUNCTION_0   None
1251	LOAD_CONST        'multipart'
1254	COMPARE_OP        '=='
1257	JUMP_IF_FALSE     '1379'

1260	LOAD_FAST         'self'
1263	LOAD_ATTR         '_last'
1266	LOAD_ATTR         'epilogue'
1269	STORE_FAST        'epilogue'

1272	LOAD_FAST         'epilogue'
1275	LOAD_CONST        ''
1278	COMPARE_OP        '=='
1281	JUMP_IF_FALSE     '1299'

1284	LOAD_CONST        None
1287	LOAD_FAST         'self'
1290	LOAD_ATTR         '_last'
1293	STORE_ATTR        'epilogue'
1296	JUMP_ABSOLUTE     '1478'

1299	LOAD_FAST         'epilogue'
1302	LOAD_CONST        None
1305	COMPARE_OP        'is not'
1308	JUMP_IF_FALSE     '1376'

1311	LOAD_GLOBAL       'NLCRE_eol'
1314	LOAD_ATTR         'search'
1317	LOAD_FAST         'epilogue'
1320	CALL_FUNCTION_1   None
1323	STORE_FAST        'mo'

1326	LOAD_FAST         'mo'
1329	JUMP_IF_FALSE     '1373'

1332	LOAD_GLOBAL       'len'
1335	LOAD_FAST         'mo'
1338	LOAD_ATTR         'group'
1341	LOAD_CONST        0
1344	CALL_FUNCTION_1   None
1347	CALL_FUNCTION_1   None
1350	STORE_FAST        'end'

1353	LOAD_FAST         'epilogue'
1356	LOAD_FAST         'end'
1359	UNARY_NEGATIVE    None
1360	SLICE+2           None
1361	LOAD_FAST         'self'
1364	LOAD_ATTR         '_last'
1367	STORE_ATTR        'epilogue'
1370	JUMP_ABSOLUTE     '1376'
1373	JUMP_ABSOLUTE     '1478'
1376	JUMP_FORWARD      '1478'

1379	LOAD_FAST         'self'
1382	LOAD_ATTR         '_last'
1385	LOAD_ATTR         'get_payload'
1388	CALL_FUNCTION_0   None
1391	STORE_FAST        'payload'

1394	LOAD_GLOBAL       'isinstance'
1397	LOAD_FAST         'payload'
1400	LOAD_GLOBAL       'basestring'
1403	CALL_FUNCTION_2   None
1406	JUMP_IF_FALSE     '1478'

1409	LOAD_GLOBAL       'NLCRE_eol'
1412	LOAD_ATTR         'search'
1415	LOAD_FAST         'payload'
1418	CALL_FUNCTION_1   None
1421	STORE_FAST        'mo'

1424	LOAD_FAST         'mo'
1427	JUMP_IF_FALSE     '1475'

1430	LOAD_FAST         'payload'
1433	LOAD_GLOBAL       'len'
1436	LOAD_FAST         'mo'
1439	LOAD_ATTR         'group'
1442	LOAD_CONST        0
1445	CALL_FUNCTION_1   None
1448	CALL_FUNCTION_1   None
1451	UNARY_NEGATIVE    None
1452	SLICE+2           None
1453	STORE_FAST        'payload'

1456	LOAD_FAST         'self'
1459	LOAD_ATTR         '_last'
1462	LOAD_ATTR         'set_payload'
1465	LOAD_FAST         'payload'
1468	CALL_FUNCTION_1   None
1471	POP_TOP           None
1472	JUMP_ABSOLUTE     '1478'
1475	JUMP_FORWARD      '1478'
1478_0	COME_FROM         '1376'
1478_1	COME_FROM         '1475'

1478	LOAD_FAST         'self'
1481	LOAD_ATTR         '_input'
1484	LOAD_ATTR         'pop_eof_matcher'
1487	CALL_FUNCTION_0   None
1490	POP_TOP           None

1491	LOAD_FAST         'self'
1494	LOAD_ATTR         '_pop_message'
1497	CALL_FUNCTION_0   None
1500	POP_TOP           None

1501	LOAD_FAST         'self'
1504	LOAD_ATTR         '_cur'
1507	LOAD_FAST         'self'
1510	STORE_ATTR        '_last'
1513	JUMP_BACK         '841'

1516	LOAD_FAST         'preamble'
1519	LOAD_ATTR         'append'
1522	LOAD_FAST         'line'
1525	CALL_FUNCTION_1   None
1528	POP_TOP           None
1529	JUMP_BACK         '841'
1532	POP_BLOCK         None
1533_0	COME_FROM         '838'

1533	LOAD_FAST         'capturing_preamble'
1536	JUMP_IF_FALSE     '1665'

1539	LOAD_FAST         'self'
1542	LOAD_ATTR         '_cur'
1545	LOAD_ATTR         'defects'
1548	LOAD_ATTR         'append'
1551	LOAD_GLOBAL       'Errors'
1554	LOAD_ATTR         'StartBoundaryNotFoundDefect'
1557	CALL_FUNCTION_0   None
1560	CALL_FUNCTION_1   None
1563	POP_TOP           None

1564	LOAD_FAST         'self'
1567	LOAD_ATTR         '_cur'
1570	LOAD_ATTR         'set_payload'
1573	LOAD_GLOBAL       'EMPTYSTRING'
1576	LOAD_ATTR         'join'
1579	LOAD_FAST         'preamble'
1582	CALL_FUNCTION_1   None
1585	CALL_FUNCTION_1   None
1588	POP_TOP           None

1589	BUILD_LIST_0      None
1592	STORE_FAST        'epilogue'

1595	SETUP_LOOP        '1637'
1598	LOAD_FAST         'self'
1601	LOAD_ATTR         '_input'
1604	GET_ITER          None
1605	FOR_ITER          '1636'
1608	STORE_FAST        'line'

1611	LOAD_FAST         'line'
1614	LOAD_GLOBAL       'NeedMoreData'
1617	COMPARE_OP        'is'
1620	JUMP_IF_FALSE     '1633'

1623	LOAD_GLOBAL       'NeedMoreData'
1626	YIELD_VALUE       None

1627	CONTINUE          '1605'
1630	JUMP_BACK         '1605'
1633	JUMP_BACK         '1605'
1636	POP_BLOCK         None
1637_0	COME_FROM         '1595'

1637	LOAD_GLOBAL       'EMPTYSTRING'
1640	LOAD_ATTR         'join'
1643	LOAD_FAST         'epilogue'
1646	CALL_FUNCTION_1   None
1649	LOAD_FAST         'self'
1652	LOAD_ATTR         '_cur'
1655	STORE_ATTR        'epilogue'

1658	LOAD_CONST        None
1661	RETURN_VALUE      None
1662	JUMP_FORWARD      '1665'
1665_0	COME_FROM         '1662'

1665	LOAD_FAST         'linesep'
1668	JUMP_IF_FALSE     '1683'

1671	LOAD_CONST        ''
1674	BUILD_LIST_1      None
1677	STORE_FAST        'epilogue'
1680	JUMP_FORWARD      '1689'

1683	BUILD_LIST_0      None
1686	STORE_FAST        'epilogue'
1689_0	COME_FROM         '1680'

1689	SETUP_LOOP        '1744'
1692	LOAD_FAST         'self'
1695	LOAD_ATTR         '_input'
1698	GET_ITER          None
1699	FOR_ITER          '1743'
1702	STORE_FAST        'line'

1705	LOAD_FAST         'line'
1708	LOAD_GLOBAL       'NeedMoreData'
1711	COMPARE_OP        'is'
1714	JUMP_IF_FALSE     '1727'

1717	LOAD_GLOBAL       'NeedMoreData'
1720	YIELD_VALUE       None

1721	CONTINUE          '1699'
1724	JUMP_FORWARD      '1727'
1727_0	COME_FROM         '1724'

1727	LOAD_FAST         'epilogue'
1730	LOAD_ATTR         'append'
1733	LOAD_FAST         'line'
1736	CALL_FUNCTION_1   None
1739	POP_TOP           None
1740	JUMP_BACK         '1699'
1743	POP_BLOCK         None
1744_0	COME_FROM         '1689'

1744	LOAD_FAST         'epilogue'
1747	JUMP_IF_FALSE     '1816'

1750	LOAD_FAST         'epilogue'
1753	LOAD_CONST        0
1756	BINARY_SUBSCR     None
1757	STORE_FAST        'firstline'

1760	LOAD_GLOBAL       'NLCRE_bol'
1763	LOAD_ATTR         'match'
1766	LOAD_FAST         'firstline'
1769	CALL_FUNCTION_1   None
1772	STORE_FAST        'bolmo'

1775	LOAD_FAST         'bolmo'
1778	JUMP_IF_FALSE     '1813'

1781	LOAD_FAST         'firstline'
1784	LOAD_GLOBAL       'len'
1787	LOAD_FAST         'bolmo'
1790	LOAD_ATTR         'group'
1793	LOAD_CONST        0
1796	CALL_FUNCTION_1   None
1799	CALL_FUNCTION_1   None
1802	SLICE+1      
# Can't uncompyle C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\email\FeedParser.pyc
Traceback (most recent call last):
  File "C:\python27\lib\uncompyle2\__init__.py", line 206, in main
    uncompyle_file(infile, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 143, in uncompyle_file
    uncompyle(version, co, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 132, in uncompyle
    raise walk.ERROR
ParserError: --- This code section failed: ---

0	LOAD_FAST         'self'
3	LOAD_ATTR         '_new_message'
6	CALL_FUNCTION_0   None
9	POP_TOP           None

10	BUILD_LIST_0      None
13	STORE_FAST        'headers'

16	SETUP_LOOP        '124'
19	LOAD_FAST         'self'
22	LOAD_ATTR         '_input'
25	GET_ITER          None
26	FOR_ITER          '123'
29	STORE_FAST        'line'

32	LOAD_FAST         'line'
35	LOAD_GLOBAL       'NeedMoreData'
38	COMPARE_OP        'is'
41	JUMP_IF_FALSE     '54'

44	LOAD_GLOBAL       'NeedMoreData'
47	YIELD_VALUE       None

48	CONTINUE          '26'
51	JUMP_FORWARD      '54'
54_0	COME_FROM         '51'

54	LOAD_GLOBAL       'headerRE'
57	LOAD_ATTR         'match'
60	LOAD_FAST         'line'
63	CALL_FUNCTION_1   None
66	JUMP_IF_TRUE      '107'

69	LOAD_GLOBAL       'NLCRE'
72	LOAD_ATTR         'match'
75	LOAD_FAST         'line'
78	CALL_FUNCTION_1   None
81	JUMP_IF_TRUE      '103'

84	LOAD_FAST         'self'
87	LOAD_ATTR         '_input'
90	LOAD_ATTR         'unreadline'
93	LOAD_FAST         'line'
96	CALL_FUNCTION_1   None
99	POP_TOP           None
100	JUMP_FORWARD      '103'
103_0	COME_FROM         '100'

103	BREAK_LOOP        None
104	JUMP_FORWARD      '107'
107_0	COME_FROM         '104'

107	LOAD_FAST         'headers'
110	LOAD_ATTR         'append'
113	LOAD_FAST         'line'
116	CALL_FUNCTION_1   None
119	POP_TOP           None
120	JUMP_BACK         '26'
123	POP_BLOCK         None
124_0	COME_FROM         '16'

124	LOAD_FAST         'self'
127	LOAD_ATTR         '_parse_headers'
130	LOAD_FAST         'headers'
133	CALL_FUNCTION_1   None
136	POP_TOP           None

137	LOAD_FAST         'self'
140	LOAD_ATTR         '_headersonly'
143	JUMP_IF_FALSE     '263'

146	BUILD_LIST_0      None
149	STORE_FAST        'lines'

152	SETUP_LOOP        '231'
155	LOAD_GLOBAL       'True'
158	JUMP_IF_FALSE     '230'

161	LOAD_FAST         'self'
164	LOAD_ATTR         '_input'
167	LOAD_ATTR         'readline'
170	CALL_FUNCTION_0   None
173	STORE_FAST        'line'

176	LOAD_FAST         'line'
179	LOAD_GLOBAL       'NeedMoreData'
182	COMPARE_OP        'is'
185	JUMP_IF_FALSE     '198'

188	LOAD_GLOBAL       'NeedMoreData'
191	YIELD_VALUE       None

192	CONTINUE          '155'
195	JUMP_FORWARD      '198'
198_0	COME_FROM         '195'

198	LOAD_FAST         'line'
201	LOAD_CONST        ''
204	COMPARE_OP        '=='
207	JUMP_IF_FALSE     '214'

210	BREAK_LOOP        None
211	JUMP_FORWARD      '214'
214_0	COME_FROM         '211'

214	LOAD_FAST         'lines'
217	LOAD_ATTR         'append'
220	LOAD_FAST         'line'
223	CALL_FUNCTION_1   None
226	POP_TOP           None
227	JUMP_BACK         '155'
230	POP_BLOCK         None
231_0	COME_FROM         '152'

231	LOAD_FAST         'self'
234	LOAD_ATTR         '_cur'
237	LOAD_ATTR         'set_payload'
240	LOAD_GLOBAL       'EMPTYSTRING'
243	LOAD_ATTR         'join'
246	LOAD_FAST         'lines'
249	CALL_FUNCTION_1   None
252	CALL_FUNCTION_1   None
255	POP_TOP           None

256	LOAD_CONST        None
259	RETURN_VALUE      None
260	JUMP_FORWARD      '263'
263_0	COME_FROM         '260'

263	LOAD_FAST         'self'
266	LOAD_ATTR         '_cur'
269	LOAD_ATTR         'get_content_type'
272	CALL_FUNCTION_0   None
275	LOAD_CONST        'message/delivery-status'
278	COMPARE_OP        '=='
281	JUMP_IF_FALSE     '528'

284	SETUP_LOOP        '521'
287	LOAD_GLOBAL       'True'
290	JUMP_IF_FALSE     '520'

293	LOAD_FAST         'self'
296	LOAD_ATTR         '_input'
299	LOAD_ATTR         'push_eof_matcher'
302	LOAD_GLOBAL       'NLCRE'
305	LOAD_ATTR         'match'
308	CALL_FUNCTION_1   None
311	POP_TOP           None

312	SETUP_LOOP        '358'
315	LOAD_FAST         'self'
318	LOAD_ATTR         '_parsegen'
321	CALL_FUNCTION_0   None
324	GET_ITER          None
325	FOR_ITER          '357'
328	STORE_FAST        'retval'

331	LOAD_FAST         'retval'
334	LOAD_GLOBAL       'NeedMoreData'
337	COMPARE_OP        'is'
340	JUMP_IF_FALSE     '353'

343	LOAD_GLOBAL       'NeedMoreData'
346	YIELD_VALUE       None

347	CONTINUE          '325'
350	JUMP_FORWARD      '353'
353_0	COME_FROM         '350'

353	BREAK_LOOP        None
354	JUMP_BACK         '325'
357	POP_BLOCK         None
358_0	COME_FROM         '312'

358	LOAD_FAST         'self'
361	LOAD_ATTR         '_pop_message'
364	CALL_FUNCTION_0   None
367	STORE_FAST        'msg'

370	LOAD_FAST         'self'
373	LOAD_ATTR         '_input'
376	LOAD_ATTR         'pop_eof_matcher'
379	CALL_FUNCTION_0   None
382	POP_TOP           None

383	SETUP_LOOP        '434'
386	LOAD_GLOBAL       'True'
389	JUMP_IF_FALSE     '433'

392	LOAD_FAST         'self'
395	LOAD_ATTR         '_input'
398	LOAD_ATTR         'readline'
401	CALL_FUNCTION_0   None
404	STORE_FAST        'line'

407	LOAD_FAST         'line'
410	LOAD_GLOBAL       'NeedMoreData'
413	COMPARE_OP        'is'
416	JUMP_IF_FALSE     '429'

419	LOAD_GLOBAL       'NeedMoreData'
422	YIELD_VALUE       None

423	CONTINUE          '386'
426	JUMP_FORWARD      '429'
429_0	COME_FROM         '426'

429	BREAK_LOOP        None
430	JUMP_BACK         '386'
433	POP_BLOCK         None
434_0	COME_FROM         '383'

434	SETUP_LOOP        '485'
437	LOAD_GLOBAL       'True'
440	JUMP_IF_FALSE     '484'

443	LOAD_FAST         'self'
446	LOAD_ATTR         '_input'
449	LOAD_ATTR         'readline'
452	CALL_FUNCTION_0   None
455	STORE_FAST        'line'

458	LOAD_FAST         'line'
461	LOAD_GLOBAL       'NeedMoreData'
464	COMPARE_OP        'is'
467	JUMP_IF_FALSE     '480'

470	LOAD_GLOBAL       'NeedMoreData'
473	YIELD_VALUE       None

474	CONTINUE          '437'
477	JUMP_FORWARD      '480'
480_0	COME_FROM         '477'

480	BREAK_LOOP        None
481	JUMP_BACK         '437'
484	POP_BLOCK         None
485_0	COME_FROM         '434'

485	LOAD_FAST         'line'
488	LOAD_CONST        ''
491	COMPARE_OP        '=='
494	JUMP_IF_FALSE     '501'

497	BREAK_LOOP        None
498	JUMP_FORWARD      '501'
501_0	COME_FROM         '498'

501	LOAD_FAST         'self'
504	LOAD_ATTR         '_input'
507	LOAD_ATTR         'unreadline'
510	LOAD_FAST         'line'
513	CALL_FUNCTION_1   None
516	POP_TOP           None
517	JUMP_BACK         '287'
520	POP_BLOCK         None
521_0	COME_FROM         '284'

521	LOAD_CONST        None
524	RETURN_VALUE      None
525	JUMP_FORWARD      '528'
528_0	COME_FROM         '525'

528	LOAD_FAST         'self'
531	LOAD_ATTR         '_cur'
534	LOAD_ATTR         'get_content_maintype'
537	CALL_FUNCTION_0   None
540	LOAD_CONST        'message'
543	COMPARE_OP        '=='
546	JUMP_IF_FALSE     '612'

549	SETUP_LOOP        '595'
552	LOAD_FAST         'self'
555	LOAD_ATTR         '_parsegen'
558	CALL_FUNCTION_0   None
561	GET_ITER          None
562	FOR_ITER          '594'
565	STORE_FAST        'retval'

568	LOAD_FAST         'retval'
571	LOAD_GLOBAL       'NeedMoreData'
574	COMPARE_OP        'is'
577	JUMP_IF_FALSE     '590'

580	LOAD_GLOBAL       'NeedMoreData'
583	YIELD_VALUE       None

584	CONTINUE          '562'
587	JUMP_FORWARD      '590'
590_0	COME_FROM         '587'

590	BREAK_LOOP        None
591	JUMP_BACK         '562'
594	POP_BLOCK         None
595_0	COME_FROM         '549'

595	LOAD_FAST         'self'
598	LOAD_ATTR         '_pop_message'
601	CALL_FUNCTION_0   None
604	POP_TOP           None

605	LOAD_CONST        None
608	RETURN_VALUE      None
609	JUMP_FORWARD      '612'
612_0	COME_FROM         '609'

612	LOAD_FAST         'self'
615	LOAD_ATTR         '_cur'
618	LOAD_ATTR         'get_content_maintype'
621	CALL_FUNCTION_0   None
624	LOAD_CONST        'multipart'
627	COMPARE_OP        '=='
630	JUMP_IF_FALSE     '1844'

633	LOAD_FAST         'self'
636	LOAD_ATTR         '_cur'
639	LOAD_ATTR         'get_boundary'
642	CALL_FUNCTION_0   None
645	STORE_FAST        'boundary'

648	LOAD_FAST         'boundary'
651	LOAD_CONST        None
654	COMPARE_OP        'is'
657	JUMP_IF_FALSE     '778'

660	LOAD_FAST         'self'
663	LOAD_ATTR         '_cur'
666	LOAD_ATTR         'defects'
669	LOAD_ATTR         'append'
672	LOAD_GLOBAL       'Errors'
675	LOAD_ATTR         'NoBoundaryInMultipartDefect'
678	CALL_FUNCTION_0   None
681	CALL_FUNCTION_1   None
684	POP_TOP           None

685	BUILD_LIST_0      None
688	STORE_FAST        'lines'

691	SETUP_LOOP        '746'
694	LOAD_FAST         'self'
697	LOAD_ATTR         '_input'
700	GET_ITER          None
701	FOR_ITER          '745'
704	STORE_FAST        'line'

707	LOAD_FAST         'line'
710	LOAD_GLOBAL       'NeedMoreData'
713	COMPARE_OP        'is'
716	JUMP_IF_FALSE     '729'

719	LOAD_GLOBAL       'NeedMoreData'
722	YIELD_VALUE       None

723	CONTINUE          '701'
726	JUMP_FORWARD      '729'
729_0	COME_FROM         '726'

729	LOAD_FAST         'lines'
732	LOAD_ATTR         'append'
735	LOAD_FAST         'line'
738	CALL_FUNCTION_1   None
741	POP_TOP           None
742	JUMP_BACK         '701'
745	POP_BLOCK         None
746_0	COME_FROM         '691'

746	LOAD_FAST         'self'
749	LOAD_ATTR         '_cur'
752	LOAD_ATTR         'set_payload'
755	LOAD_GLOBAL       'EMPTYSTRING'
758	LOAD_ATTR         'join'
761	LOAD_FAST         'lines'
764	CALL_FUNCTION_1   None
767	CALL_FUNCTION_1   None
770	POP_TOP           None

771	LOAD_CONST        None
774	RETURN_VALUE      None
775	JUMP_FORWARD      '778'
778_0	COME_FROM         '775'

778	LOAD_CONST        '--'
781	LOAD_FAST         'boundary'
784	BINARY_ADD        None
785	STORE_FAST        'separator'

788	LOAD_GLOBAL       're'
791	LOAD_ATTR         'compile'
794	LOAD_CONST        '(?P<sep>'
797	LOAD_GLOBAL       're'
800	LOAD_ATTR         'escape'
803	LOAD_FAST         'separator'
806	CALL_FUNCTION_1   None
809	BINARY_ADD        None
810	LOAD_CONST        ')(?P<end>--)?(?P<ws>[ \\t]*)(?P<linesep>\\r\\n|\\r|\\n)?$'
813	BINARY_ADD        None
814	CALL_FUNCTION_1   None
817	STORE_FAST        'boundaryre'

820	LOAD_GLOBAL       'True'
823	STORE_FAST        'capturing_preamble'

826	BUILD_LIST_0      None
829	STORE_FAST        'preamble'

832	LOAD_GLOBAL       'False'
835	STORE_FAST        'linesep'

838	SETUP_LOOP        '1533'
841	LOAD_GLOBAL       'True'
844	JUMP_IF_FALSE     '1532'

847	LOAD_FAST         'self'
850	LOAD_ATTR         '_input'
853	LOAD_ATTR         'readline'
856	CALL_FUNCTION_0   None
859	STORE_FAST        'line'

862	LOAD_FAST         'line'
865	LOAD_GLOBAL       'NeedMoreData'
868	COMPARE_OP        'is'
871	JUMP_IF_FALSE     '884'

874	LOAD_GLOBAL       'NeedMoreData'
877	YIELD_VALUE       None

878	CONTINUE          '841'
881	JUMP_FORWARD      '884'
884_0	COME_FROM         '881'

884	LOAD_FAST         'line'
887	LOAD_CONST        ''
890	COMPARE_OP        '=='
893	JUMP_IF_FALSE     '900'

896	BREAK_LOOP        None
897	JUMP_FORWARD      '900'
900_0	COME_FROM         '897'

900	LOAD_FAST         'boundaryre'
903	LOAD_ATTR         'match'
906	LOAD_FAST         'line'
909	CALL_FUNCTION_1   None
912	STORE_FAST        'mo'

915	LOAD_FAST         'mo'
918	JUMP_IF_FALSE     '1516'

921	LOAD_FAST         'mo'
924	LOAD_ATTR         'group'
927	LOAD_CONST        'end'
930	CALL_FUNCTION_1   None
933	JUMP_IF_FALSE     '955'

936	LOAD_FAST         'mo'
939	LOAD_ATTR         'group'
942	LOAD_CONST        'linesep'
945	CALL_FUNCTION_1   None
948	STORE_FAST        'linesep'

951	BREAK_LOOP        None
952	JUMP_FORWARD      '955'
955_0	COME_FROM         '952'

955	LOAD_FAST         'capturing_preamble'
958	JUMP_IF_FALSE     '1083'

961	LOAD_FAST         'preamble'
964	JUMP_IF_FALSE     '1055'

967	LOAD_FAST         'preamble'
970	LOAD_CONST        -1
973	BINARY_SUBSCR     None
974	STORE_FAST        'lastline'

977	LOAD_GLOBAL       'NLCRE_eol'
980	LOAD_ATTR         'search'
983	LOAD_FAST         'lastline'
986	CALL_FUNCTION_1   None
989	STORE_FAST        'eolmo'

992	LOAD_FAST         'eolmo'
995	JUMP_IF_FALSE     '1031'

998	LOAD_FAST         'lastline'
1001	LOAD_GLOBAL       'len'
1004	LOAD_FAST         'eolmo'
1007	LOAD_ATTR         'group'
1010	LOAD_CONST        0
1013	CALL_FUNCTION_1   None
1016	CALL_FUNCTION_1   None
1019	UNARY_NEGATIVE    None
1020	SLICE+2           None
1021	LOAD_FAST         'preamble'
1024	LOAD_CONST        -1
1027	STORE_SUBSCR      None
1028	JUMP_FORWARD      '1031'
1031_0	COME_FROM         '1028'

1031	LOAD_GLOBAL       'EMPTYSTRING'
1034	LOAD_ATTR         'join'
1037	LOAD_FAST         'preamble'
1040	CALL_FUNCTION_1   None
1043	LOAD_FAST         'self'
1046	LOAD_ATTR         '_cur'
1049	STORE_ATTR        'preamble'
1052	JUMP_FORWARD      '1055'
1055_0	COME_FROM         '1052'

1055	LOAD_GLOBAL       'False'
1058	STORE_FAST        'capturing_preamble'

1061	LOAD_FAST         'self'
1064	LOAD_ATTR         '_input'
1067	LOAD_ATTR         'unreadline'
1070	LOAD_FAST         'line'
1073	CALL_FUNCTION_1   None
1076	POP_TOP           None

1077	CONTINUE          '841'
1080	JUMP_FORWARD      '1083'
1083_0	COME_FROM         '1080'

1083	SETUP_LOOP        '1174'
1086	LOAD_GLOBAL       'True'
1089	JUMP_IF_FALSE     '1173'

1092	LOAD_FAST         'self'
1095	LOAD_ATTR         '_input'
1098	LOAD_ATTR         'readline'
1101	CALL_FUNCTION_0   None
1104	STORE_FAST        'line'

1107	LOAD_FAST         'line'
1110	LOAD_GLOBAL       'NeedMoreData'
1113	COMPARE_OP        'is'
1116	JUMP_IF_FALSE     '1129'

1119	LOAD_GLOBAL       'NeedMoreData'
1122	YIELD_VALUE       None

1123	CONTINUE          '1086'
1126	JUMP_FORWARD      '1129'
1129_0	COME_FROM         '1126'

1129	LOAD_FAST         'boundaryre'
1132	LOAD_ATTR         'match'
1135	LOAD_FAST         'line'
1138	CALL_FUNCTION_1   None
1141	STORE_FAST        'mo'

1144	LOAD_FAST         'mo'
1147	JUMP_IF_TRUE      '1170'

1150	LOAD_FAST         'self'
1153	LOAD_ATTR         '_input'
1156	LOAD_ATTR         'unreadline'
1159	LOAD_FAST         'line'
1162	CALL_FUNCTION_1   None
1165	POP_TOP           None

1166	BREAK_LOOP        None
1167	JUMP_BACK         '1086'
1170	JUMP_BACK         '1086'
1173	POP_BLOCK         None
1174_0	COME_FROM         '1083'

1174	LOAD_FAST         'self'
1177	LOAD_ATTR         '_input'
1180	LOAD_ATTR         'push_eof_matcher'
1183	LOAD_FAST         'boundaryre'
1186	LOAD_ATTR         'match'
1189	CALL_FUNCTION_1   None
1192	POP_TOP           None

1193	SETUP_LOOP        '1239'
1196	LOAD_FAST         'self'
1199	LOAD_ATTR         '_parsegen'
1202	CALL_FUNCTION_0   None
1205	GET_ITER          None
1206	FOR_ITER          '1238'
1209	STORE_FAST        'retval'

1212	LOAD_FAST         'retval'
1215	LOAD_GLOBAL       'NeedMoreData'
1218	COMPARE_OP        'is'
1221	JUMP_IF_FALSE     '1234'

1224	LOAD_GLOBAL       'NeedMoreData'
1227	YIELD_VALUE       None

1228	CONTINUE          '1206'
1231	JUMP_FORWARD      '1234'
1234_0	COME_FROM         '1231'

1234	BREAK_LOOP        None
1235	JUMP_BACK         '1206'
1238	POP_BLOCK         None
1239_0	COME_FROM         '1193'

1239	LOAD_FAST         'self'
1242	LOAD_ATTR         '_last'
1245	LOAD_ATTR         'get_content_maintype'
1248	CALL_FUNCTION_0   None
1251	LOAD_CONST        'multipart'
1254	COMPARE_OP        '=='
1257	JUMP_IF_FALSE     '1379'

1260	LOAD_FAST         'self'
1263	LOAD_ATTR         '_last'
1266	LOAD_ATTR         'epilogue'
1269	STORE_FAST        'epilogue'

1272	LOAD_FAST         'epilogue'
1275	LOAD_CONST        ''
1278	COMPARE_OP        '=='
1281	JUMP_IF_FALSE     '1299'

1284	LOAD_CONST        None
1287	LOAD_FAST         'self'
1290	LOAD_ATTR         '_last'
1293	STORE_ATTR        'epilogue'
1296	JUMP_ABSOLUTE     '1478'

1299	LOAD_FAST         'epilogue'
1302	LOAD_CONST        None
1305	COMPARE_OP        'is not'
1308	JUMP_IF_FALSE     '1376'

1311	LOAD_GLOBAL       'NLCRE_eol'
1314	LOAD_ATTR         'search'
1317	LOAD_FAST         'epilogue'
1320	CALL_FUNCTION_1   None
1323	STORE_FAST        'mo'

1326	LOAD_FAST         'mo'
1329	JUMP_IF_FALSE     '1373'

1332	LOAD_GLOBAL       'len'
1335	LOAD_FAST         'mo'
1338	LOAD_ATTR         'group'
1341	LOAD_CONST        0
1344	CALL_FUNCTION_1   None
1347	CALL_FUNCTION_1   None
1350	STORE_FAST        'end'

1353	LOAD_FAST         'epilogue'
1356	LOAD_FAST         'end'
1359	UNARY_NEGATIVE    None
1360	SLICE+2           None
1361	LOAD_FAST         'self'
1364	LOAD_ATTR         '_last'
1367	STORE_ATTR        'epilogue'
1370	JUMP_ABSOLUTE     '1376'
1373	JUMP_ABSOLUTE     '1478'
1376	JUMP_FORWARD      '1478'

1379	LOAD_FAST         'self'
1382	LOAD_ATTR         '_last'
1385	LOAD_ATTR         'get_payload'
1388	CALL_FUNCTION_0   None
1391	STORE_FAST        'payload'

1394	LOAD_GLOBAL       'isinstance'
1397	LOAD_FAST         'payload'
1400	LOAD_GLOBAL       'basestring'
1403	CALL_FUNCTION_2   None
1406	JUMP_IF_FALSE     '1478'

1409	LOAD_GLOBAL       'NLCRE_eol'
1412	LOAD_ATTR         'search'
1415	LOAD_FAST         'payload'
1418	CALL_FUNCTION_1   None
1421	STORE_FAST        'mo'

1424	LOAD_FAST         'mo'
1427	JUMP_IF_FALSE     '1475'

1430	LOAD_FAST         'payload'
1433	LOAD_GLOBAL       'len'
1436	LOAD_FAST         'mo'
1439	LOAD_ATTR         'group'
1442	LOAD_CONST        0
1445	CALL_FUNCTION_1   None
1448	CALL_FUNCTION_1   None
1451	UNARY_NEGATIVE    None
1452	SLICE+2           None
1453	STORE_FAST        'payload'

1456	LOAD_FAST         'self'
1459	LOAD_ATTR         '_last'
1462	LOAD_ATTR         'set_payload'
1465	LOAD_FAST         'payload'
1468	CALL_FUNCTION_1   None
1471	POP_TOP           None
1472	JUMP_ABSOLUTE     '1478'
1475	JUMP_FORWARD      '1478'
1478_0	COME_FROM         '1376'
1478_1	COME_FROM         '1475'

1478	LOAD_FAST         'self'
1481	LOAD_ATTR         '_input'
1484	LOAD_ATTR         'pop_eof_matcher'
1487	CALL_FUNCTION_0   None
1490	POP_TOP           None

1491	LOAD_FAST         'self'
1494	LOAD_ATTR         '_pop_message'
1497	CALL_FUNCTION_0   None
1500	POP_TOP           None

1501	LOAD_FAST         'self'
1504	LOAD_ATTR         '_cur'
1507	LOAD_FAST         'self'
1510	STORE_ATTR        '_last'
1513	JUMP_BACK         '841'

1516	LOAD_FAST         'preamble'
1519	LOAD_ATTR         'append'
1522	LOAD_FAST         'line'
1525	CALL_FUNCTION_1   None
1528	POP_TOP           None
1529	JUMP_BACK         '841'
1532	POP_BLOCK         None
1533_0	COME_FROM         '838'

1533	LOAD_FAST         'capturing_preamble'
1536	JUMP_IF_FALSE     '1665'

1539	LOAD_FAST         'self'
1542	LOAD_ATTR         '_cur'
1545	LOAD_ATTR         'defects'
1548	LOAD_ATTR         'append'
1551	LOAD_GLOBAL       'Errors'
1554	LOAD_ATTR         'StartBoundaryNotFoundDefect'
1557	CALL_FUNCTION_0   None
1560	CALL_FUNCTION_1   None
1563	POP_TOP           None

1564	LOAD_FAST         'self'
1567	LOAD_ATTR         '_cur'
1570	LOAD_ATTR         'set_payload'
1573	LOAD_GLOBAL       'EMPTYSTRING'
1576	LOAD_ATTR         'join'
1579	LOAD_FAST         'preamble'
1582	CALL_FUNCTION_1   None
1585	CALL_FUNCTION_1   None
1588	POP_TOP           None

1589	BUILD_LIST_0      None
1592	STORE_FAST        'epilogue'

1595	SETUP_LOOP        '1637'
1598	LOAD_FAST         'self'
1601	LOAD_ATTR         '_input'
1604	GET_ITER          None
1605	FOR_ITER          '1636'
1608	STORE_FAST        'line'

1611	LOAD_FAST         'line'
1614	LOAD_GLOBAL       'NeedMoreData'
1617	COMPARE_OP        'is'
1620	JUMP_IF_FALSE     '1633'

1623	LOAD_GLOBAL       'NeedMoreData'
1626	YIELD_VALUE       None

1627	CONTINUE          '1605'
1630	JUMP_BACK         '1605'
1633	JUMP_BACK         '1605'
1636	POP_BLOCK         None
1637_0	COME_FROM         '1595'

1637	LOAD_GLOBAL       'EMPTYSTRING'
1640	LOAD_ATTR         'join'
1643	LOAD_FAST         'epilogue'
1646	CALL_FUNCTION_1   None
1649	LOAD_FAST         'self'
1652	LOAD_ATTR         '_cur'
1655	STORE_ATTR        'epilogue'

1658	LOAD_CONST        None
1661	RETURN_VALUE      None
1662	JUMP_FORWARD      '1665'
1665_0	COME_FROM         '1662'

1665	LOAD_FAST         'linesep'
1668	JUMP_IF_FALSE     '1683'

1671	LOAD_CONST        ''
1674	BUILD_LIST_1      None
1677	STORE_FAST        'epilogue'
1680	JUMP_FORWARD      '1689'

1683	BUILD_LIST_0      None
1686	STORE_FAST        'epilogue'
1689_0	COME_FROM         '1680'

1689	SETUP_LOOP        '1744'
1692	LOAD_FAST         'self'
1695	LOAD_ATTR             None
1803	LOAD_FAST         'epilogue'
1806	LOAD_CONST        0
1809	STORE_SUBSCR      None
1810	JUMP_ABSOLUTE     '1816'
1813	JUMP_FORWARD      '1816'
1816_0	COME_FROM         '1813'

1816	LOAD_GLOBAL       'EMPTYSTRING'
1819	LOAD_ATTR         'join'
1822	LOAD_FAST         'epilogue'
1825	CALL_FUNCTION_1   None
1828	LOAD_FAST         'self'
1831	LOAD_ATTR         '_cur'
1834	STORE_ATTR        'epilogue'

1837	LOAD_CONST        None
1840	RETURN_VALUE      None
1841	JUMP_FORWARD      '1844'
1844_0	COME_FROM         '1841'

1844	BUILD_LIST_0      None
1847	STORE_FAST        'lines'

1850	SETUP_LOOP        '1905'
1853	LOAD_FAST         'self'
1856	LOAD_ATTR         '_input'
1859	GET_ITER          None
1860	FOR_ITER          '1904'
1863	STORE_FAST        'line'

1866	LOAD_FAST         'line'
1869	LOAD_GLOBAL       'NeedMoreData'
1872	COMPARE_OP        'is'
1875	JUMP_IF_FALSE     '1888'

1878	LOAD_GLOBAL       'NeedMoreData'
1881	YIELD_VALUE       None

1882	CONTINUE          '1860'
1885	JUMP_FORWARD      '1888'
1888_0	COME_FROM         '1885'

1888	LOAD_FAST         'lines'
1891	LOAD_ATTR         'append'
1894	LOAD_FAST         'line'
1897	CALL_FUNCTION_1   None
1900	POP_TOP           None
1901	JUMP_BACK         '1860'
1904	POP_BLOCK         None
1905_0	COME_FROM         '1850'

1905	LOAD_FAST         'self'
1908	LOAD_ATTR         '_cur'
1911	LOAD_ATTR         'set_payload'
1914	LOAD_GLOBAL       'EMPTYSTRING'
1917	LOAD_ATTR         'join'
1920	LOAD_FAST         'lines'
1923	CALL_FUNCTION_1   None
1926	CALL_FUNCTION_1   None
1929	POP_TOP           None
1930	LOAD_CONST        None
1933	RETURN_VALUE      None

Syntax error at or near `CONTINUE' token at offset 48

    def _parse_headers(self, lines):
        lastheader = ''
        lastvalue = []
        for lineno, line in enumerate(lines):
            if line[0] in ' \t':
                if not lastheader:
                    defect = Errors.FirstHeaderLineIsContinuationDefect(line)
                    self._cur.defects.append(defect)
                    continue
                lastvalue.append(line)
                continue
            if lastheader:
                lhdr = EMPTYSTRING.join(lastvalue)[:-1].rstrip('\r\n')
                self._cur[lastheader] = lhdr
                lastheader, lastvalue = '', []
            if line.startswith('From '):
                if lineno == 0:
                    mo = NLCRE_eol.search(line)
                    if mo:
                        line = line[:-len(mo.group(0))]
                    self._cur.set_unixfrom(line)
                    continue
                elif lineno == len(lines) - 1:
                    self._input.unreadline(line)
                    return
                else:
                    defect = Errors.MisplacedEnvelopeHeaderDefect(line)
                    self._cur.defects.append(defect)
                    continue
            i = line.find(':')
            if i < 0:
                defect = Errors.MalformedHeaderDefect(line)
                self._cur.defects.append(defect)
                continue
            lastheader = line[:i]
            lastvalue = [line[i + 1:].lstrip()]

        if lastheader:
            self._cur[lastheader] = EMPTYSTRING.join(lastvalue).rstrip('\r\n')# decompiled 0 files: 0 okay, 1 failed, 0 verify failed
# 2013.08.22 22:14:58 Pacific Daylight Time
 '_input'
1698	GET_ITER          None
1699	FOR_ITER          '1743'
1702	STORE_FAST        'line'

1705	LOAD_FAST         'line'
1708	LOAD_GLOBAL       'NeedMoreData'
1711	COMPARE_OP        'is'
1714	JUMP_IF_FALSE     '1727'

1717	LOAD_GLOBAL       'NeedMoreData'
1720	YIELD_VALUE       None

1721	CONTINUE          '1699'
1724	JUMP_FORWARD      '1727'
1727_0	COME_FROM         '1724'

1727	LOAD_FAST         'epilogue'
1730	LOAD_ATTR         'append'
1733	LOAD_FAST         'line'
1736	CALL_FUNCTION_1   None
1739	POP_TOP           None
1740	JUMP_BACK         '1699'
1743	POP_BLOCK         None
1744_0	COME_FROM         '1689'

1744	LOAD_FAST         'epilogue'
1747	JUMP_IF_FALSE     '1816'

1750	LOAD_FAST         'epilogue'
1753	LOAD_CONST        0
1756	BINARY_SUBSCR     None
1757	STORE_FAST        'firstline'

1760	LOAD_GLOBAL       'NLCRE_bol'
1763	LOAD_ATTR         'match'
1766	LOAD_FAST         'firstline'
1769	CALL_FUNCTION_1   None
1772	STORE_FAST        'bolmo'

1775	LOAD_FAST         'bolmo'
1778	JUMP_IF_FALSE     '1813'

1781	LOAD_FAST         'firstline'
1784	LOAD_GLOBAL       'len'
1787	LOAD_FAST         'bolmo'
1790	LOAD_ATTR         'group'
1793	LOAD_CONST        0
1796	CALL_FUNCTION_1   None
1799	CALL_FUNCTION_1   None
1802	SLICE+1           None
1803	LOAD_FAST         'epilogue'
1806	LOAD_CONST        0
1809	STORE_SUBSCR      None
1810	JUMP_ABSOLUTE     '1816'
1813	JUMP_FORWARD      '1816'
1816_0	COME_FROM         '1813'

1816	LOAD_GLOBAL       'EMPTYSTRING'
1819	LOAD_ATTR         'join'
1822	LOAD_FAST         'epilogue'
1825	CALL_FUNCTION_1   None
1828	LOAD_FAST         'self'
1831	LOAD_ATTR         '_cur'
1834	STORE_ATTR        'epilogue'

1837	LOAD_CONST        None
1840	RETURN_VALUE      None
1841	JUMP_FORWARD      '1844'
1844_0	COME_FROM         '1841'

1844	BUILD_LIST_0      None
1847	STORE_FAST        'lines'

1850	SETUP_LOOP        '1905'
1853	LOAD_FAST         'self'
1856	LOAD_ATTR         '_input'
1859	GET_ITER          None
1860	FOR_ITER          '1904'
1863	STORE_FAST        'line'

1866	LOAD_FAST         'line'
1869	LOAD_GLOBAL       'NeedMoreData'
1872	COMPARE_OP        'is'
1875	JUMP_IF_FALSE     '1888'

1878	LOAD_GLOBAL       'NeedMoreData'
1881	YIELD_VALUE       None

1882	CONTINUE          '1860'
1885	JUMP_FORWARD      '1888'
1888_0	COME_FROM         '1885'

1888	LOAD_FAST         'lines'
1891	LOAD_ATTR         'append'
1894	LOAD_FAST         'line'
1897	CALL_FUNCTION_1   None
1900	POP_TOP           None
1901	JUMP_BACK         '1860'
1904	POP_BLOCK         None
1905_0	COME_FROM         '1850'

1905	LOAD_FAST         'self'
1908	LOAD_ATTR         '_cur'
1911	LOAD_ATTR         'set_payload'
1914	LOAD_GLOBAL       'EMPTYSTRING'
1917	LOAD_ATTR         'join'
1920	LOAD_FAST         'lines'
1923	CALL_FUNCTION_1   None
1926	CALL_FUNCTION_1   None
1929	POP_TOP           None
1930	LOAD_CONST        None
1933	RETURN_VALUE      None

Syntax error at or near `CONTINUE' token at offset 48

