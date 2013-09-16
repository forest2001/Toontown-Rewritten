# 2013.08.22 22:14:39 Pacific Daylight Time
# Embedded file name: direct.showbase.MessengerLeakDetector
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.showbase.DirectObject import DirectObject
from direct.showbase.Job import Job
import gc, __builtin__

class MessengerLeakObject(DirectObject):
    __module__ = __name__

    def __init__(self):
        self.accept('leakEvent', self._handleEvent)

    def _handleEvent(self):
        pass


def _leakMessengerObject():
    leakObject = MessengerLeakObject()


class MessengerLeakDetector(Job):
    __module__ = __name__
    notify = directNotify.newCategory('MessengerLeakDetector')

    def __init__(self, name):
        Job.__init__(self, name)
        self.setPriority(Job.Priorities.Normal * 2)
        jobMgr.add(self)

    def run--- This code section failed: ---

0	LOAD_GLOBAL       'set'
3	CALL_FUNCTION_0   None
6	STORE_FAST        'builtinIds'

9	LOAD_FAST         'builtinIds'
12	LOAD_ATTR         'add'
15	LOAD_GLOBAL       'id'
18	LOAD_GLOBAL       '__builtin__'
21	LOAD_ATTR         '__dict__'
24	CALL_FUNCTION_1   None
27	CALL_FUNCTION_1   None
30	POP_TOP           None

31	SETUP_EXCEPT      '104'

34	LOAD_FAST         'builtinIds'
37	LOAD_ATTR         'add'
40	LOAD_GLOBAL       'id'
43	LOAD_GLOBAL       'base'
46	CALL_FUNCTION_1   None
49	CALL_FUNCTION_1   None
52	POP_TOP           None

53	LOAD_FAST         'builtinIds'
56	LOAD_ATTR         'add'
59	LOAD_GLOBAL       'id'
62	LOAD_GLOBAL       'base'
65	LOAD_ATTR         'cr'
68	CALL_FUNCTION_1   None
71	CALL_FUNCTION_1   None
74	POP_TOP           None

75	LOAD_FAST         'builtinIds'
78	LOAD_ATTR         'add'
81	LOAD_GLOBAL       'id'
84	LOAD_GLOBAL       'base'
87	LOAD_ATTR         'cr'
90	LOAD_ATTR         'doId2do'
93	CALL_FUNCTION_1   None
96	CALL_FUNCTION_1   None
99	POP_TOP           None
100	POP_BLOCK         None
101	JUMP_FORWARD      '111'
104_0	COME_FROM         '31'

104	POP_TOP           None
105	POP_TOP           None
106	POP_TOP           None

107	JUMP_FORWARD      '111'
110	END_FINALLY       None
111_0	COME_FROM         '101'
111_1	COME_FROM         '110'

111	SETUP_EXCEPT      '184'

114	LOAD_FAST         'builtinIds'
117	LOAD_ATTR         'add'
120	LOAD_GLOBAL       'id'
123	LOAD_GLOBAL       'simbase'
126	CALL_FUNCTION_1   None
129	CALL_FUNCTION_1   None
132	POP_TOP           None

133	LOAD_FAST         'builtinIds'
136	LOAD_ATTR         'add'
139	LOAD_GLOBAL       'id'
142	LOAD_GLOBAL       'simbase'
145	LOAD_ATTR         'air'
148	CALL_FUNCTION_1   None
151	CALL_FUNCTION_1   None
154	POP_TOP           None

155	LOAD_FAST         'builtinIds'
158	LOAD_ATTR         'add'
161	LOAD_GLOBAL       'id'
164	LOAD_GLOBAL       'simbase'
167	LOAD_ATTR         'air'
170	LOAD_ATTR         'doId2do'
173	CALL_FUNCTION_1   None
176	CALL_FUNCTION_1   None
179	POP_TOP           None
180	POP_BLOCK         None
181	JUMP_FORWARD      '191'
184_0	COME_FROM         '111'

184	POP_TOP           None
185	POP_TOP           None
186	POP_TOP           None

187	JUMP_FORWARD      '191'
190	END_FINALLY       None
191_0	COME_FROM         '181'
191_1	COME_FROM         '190'

191	SETUP_EXCEPT      '264'

194	LOAD_FAST         'builtinIds'
197	LOAD_ATTR         'add'
200	LOAD_GLOBAL       'id'
203	LOAD_GLOBAL       'uber'
206	CALL_FUNCTION_1   None
209	CALL_FUNCTION_1   None
212	POP_TOP           None

213	LOAD_FAST         'builtinIds'
216	LOAD_ATTR         'add'
219	LOAD_GLOBAL       'id'
222	LOAD_GLOBAL       'uber'
225	LOAD_ATTR         'air'
228	CALL_FUNCTION_1   None
231	CALL_FUNCTION_1   None
234	POP_TOP           None

235	LOAD_FAST         'builtinIds'
238	LOAD_ATTR         'add'
241	LOAD_GLOBAL       'id'
244	LOAD_GLOBAL       'uber'
247	LOAD_ATTR         'air'
250	LOAD_ATTR         'doId2do'
253	CALL_FUNCTION_1   None
256	CALL_FUNCTION_1   None
259	POP_TOP           None
260	POP_BLOCK         None
261	JUMP_FORWARD      '271'
264_0	COME_FROM         '191'

264	POP_TOP           None
265	POP_TOP           None
266	POP_TOP           None

267	JUMP_FORWARD      '271'
270	END_FINALLY       None
271_0	COME_FROM         '261'
271_1	COME_FROM         '270'

271	SETUP_LOOP        '690'
274	LOAD_GLOBAL       'True'
277	JUMP_IF_FALSE     '689'

280	LOAD_CONST        None
283	YIELD_VALUE       None

284	LOAD_GLOBAL       'messenger'
287	LOAD_ATTR         '_Messenger__objectEvents'
290	LOAD_ATTR         'keys'
293	CALL_FUNCTION_0   None
296	STORE_FAST        'objects'

299	SETUP_LOOP        '686'
302	LOAD_FAST         'objects'
305	GET_ITER          None
306	FOR_ITER          '685'
309	STORE_FAST        'object'

312	LOAD_CONST        None
315	YIELD_VALUE       None

316	BUILD_LIST_0      None
319	STORE_FAST        'objList1'

322	BUILD_LIST_0      None
325	STORE_FAST        'objList2'

328	LOAD_FAST         'objList1'
331	STORE_FAST        'curObjList'

334	LOAD_FAST         'objList2'
337	STORE_FAST        'nextObjList'

340	LOAD_GLOBAL       'set'
343	CALL_FUNCTION_0   None
346	STORE_FAST        'visitedObjIds'

349	LOAD_FAST         'visitedObjIds'
352	LOAD_ATTR         'add'
355	LOAD_GLOBAL       'id'
358	LOAD_FAST         'object'
361	CALL_FUNCTION_1   None
364	CALL_FUNCTION_1   None
367	POP_TOP           None

368	LOAD_FAST         'visitedObjIds'
371	LOAD_ATTR         'add'
374	LOAD_GLOBAL       'id'
377	LOAD_GLOBAL       'messenger'
380	LOAD_ATTR         '_Messenger__objectEvents'
383	CALL_FUNCTION_1   None
386	CALL_FUNCTION_1   None
389	POP_TOP           None

390	LOAD_FAST         'visitedObjIds'
393	LOAD_ATTR         'add'
396	LOAD_GLOBAL       'id'
399	LOAD_GLOBAL       'messenger'
402	LOAD_ATTR         '_Messenger__callbacks'
405	CALL_FUNCTION_1   None
408	CALL_FUNCTION_1   None
411	POP_TOP           None

412	LOAD_FAST         'nextObjList'
415	LOAD_ATTR         'append'
418	LOAD_FAST         'object'
421	CALL_FUNCTION_1   None
424	POP_TOP           None

425	LOAD_GLOBAL       'False'
428	STORE_FAST        'foundBuiltin'

431	SETUP_LOOP        '647'
434	LOAD_GLOBAL       'len'
437	LOAD_FAST         'nextObjList'
440	CALL_FUNCTION_1   None
443	JUMP_IF_FALSE     '646'

446	LOAD_FAST         'foundBuiltin'
449	JUMP_IF_FALSE     '456'

452	BREAK_LOOP        None
453	JUMP_FORWARD      '456'
456_0	COME_FROM         '453'

456	LOAD_FAST         'nextObjList'
459	STORE_FAST        'curObjList'

462	BUILD_LIST_0      None
465	STORE_FAST        'nextObjList'

468	SETUP_LOOP        '643'
471	LOAD_FAST         'curObjList'
474	GET_ITER          None
475	FOR_ITER          '642'
478	STORE_FAST        'curObj'

481	LOAD_FAST         'foundBuiltin'
484	JUMP_IF_FALSE     '491'

487	BREAK_LOOP        None
488	JUMP_FORWARD      '491'
491_0	COME_FROM         '488'

491	LOAD_CONST        None
494	YIELD_VALUE       None

495	LOAD_GLOBAL       'gc'
498	LOAD_ATTR         'get_referrers'
501	LOAD_FAST         'curObj'
504	CALL_FUNCTION_1   None
507	STORE_FAST        'referrers'

510	SETUP_LOOP        '639'
513	LOAD_FAST         'referrers'
516	GET_ITER          None
517	FOR_ITER          '638'
520	STORE_FAST        'referrer'

523	LOAD_CONST        None
526	YIELD_VALUE       None

527	LOAD_GLOBAL       'id'
530	LOAD_FAST         'referrer'
533	CALL_FUNCTION_1   None
536	STORE_FAST        'refId'

539	LOAD_FAST         'refId'
542	LOAD_FAST         'visitedObjIds'
545	COMPARE_OP        'in'
548	JUMP_IF_FALSE     '557'

551	CONTINUE          '517'
554	JUMP_FORWARD      '557'
557_0	COME_FROM         '554'

557	LOAD_FAST         'referrer'
560	LOAD_FAST         'curObjList'
563	COMPARE_OP        'is'
566	JUMP_IF_TRUE      '581'
569	LOAD_FAST         'referrer'
572	LOAD_FAST         'nextObjList'
575	COMPARE_OP        'is'
578_0	COME_FROM         '566'
578	JUMP_IF_FALSE     '587'

581	CONTINUE          '517'
584	JUMP_FORWARD      '587'
587_0	COME_FROM         '584'

587	LOAD_FAST         'refId'
590	LOAD_FAST         'builtinIds'
593	COMPARE_OP        'in'
596	JUMP_IF_FALSE     '609'

599	LOAD_GLOBAL       'True'
602	STORE_FAST        'foundBuiltin'

605	BREAK_LOOP        None
606	JUMP_BACK         '517'

609	LOAD_FAST         'visitedObjIds'
612	LOAD_ATTR         'add'
615	LOAD_FAST         'refId'
618	CALL_FUNCTION_1   None
621	POP
# Can't uncompyle C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\showbase\MessengerLeakDetector.pyc
Traceback (most recent call last):
  File "C:\python27\lib\uncompyle2\__init__.py", line 206, in main
    uncompyle_file(infile, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 143, in uncompyle_file
    uncompyle(version, co, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 132, in uncompyle
    raise walk.ERROR
ParserError: --- This code section failed: ---

0	LOAD_GLOBAL       'set'
3	CALL_FUNCTION_0   None
6	STORE_FAST        'builtinIds'

9	LOAD_FAST         'builtinIds'
12	LOAD_ATTR         'add'
15	LOAD_GLOBAL       'id'
18	LOAD_GLOBAL       '__builtin__'
21	LOAD_ATTR         '__dict__'
24	CALL_FUNCTION_1   None
27	CALL_FUNCTION_1   None
30	POP_TOP           None

31	SETUP_EXCEPT      '104'

34	LOAD_FAST         'builtinIds'
37	LOAD_ATTR         'add'
40	LOAD_GLOBAL       'id'
43	LOAD_GLOBAL       'base'
46	CALL_FUNCTION_1   None
49	CALL_FUNCTION_1   None
52	POP_TOP           None

53	LOAD_FAST         'builtinIds'
56	LOAD_ATTR         'add'
59	LOAD_GLOBAL       'id'
62	LOAD_GLOBAL       'base'
65	LOAD_ATTR         'cr'
68	CALL_FUNCTION_1   None
71	CALL_FUNCTION_1   None
74	POP_TOP           None

75	LOAD_FAST         'builtinIds'
78	LOAD_ATTR         'add'
81	LOAD_GLOBAL       'id'
84	LOAD_GLOBAL       'base'
87	LOAD_ATTR         'cr'
90	LOAD_ATTR         'doId2do'
93	CALL_FUNCTION_1   None
96	CALL_FUNCTION_1   None
99	POP_TOP           None
100	POP_BLOCK         None
101	JUMP_FORWARD      '111'
104_0	COME_FROM         '31'

104	POP_TOP           None
105	POP_TOP           None
106	POP_TOP           None

107	JUMP_FORWARD      '111'
110	END_FINALLY       None
111_0	COME_FROM         '101'
111_1	COME_FROM         '110'

111	SETUP_EXCEPT      '184'

114	LOAD_FAST         'builtinIds'
117	LOAD_ATTR         'add'
120	LOAD_GLOBAL       'id'
123	LOAD_GLOBAL       'simbase'
126	CALL_FUNCTION_1   None
129	CALL_FUNCTION_1   None
132	POP_TOP           None

133	LOAD_FAST         'builtinIds'
136	LOAD_ATTR         'add'
139	LOAD_GLOBAL       'id'
142	LOAD_GLOBAL       'simbase'
145	LOAD_ATTR         'air'
148	CALL_FUNCTION_1   None
151	CALL_FUNCTION_1   None
154	POP_TOP           None

155	LOAD_FAST         'builtinIds'
158	LOAD_ATTR         'add'
161	LOAD_GLOBAL       'id'
164	LOAD_GLOBAL       'simbase'
167	LOAD_ATTR         'air'
170	LOAD_ATTR         'doId2do'
173	CALL_FUNCTION_1   None
176	CALL_FUNCTION_1   None
179	POP_TOP           None
180	POP_BLOCK         None
181	JUMP_FORWARD      '191'
184_0	COME_FROM         '111'

184	POP_TOP           None
185	POP_TOP           None
186	POP_TOP           None

187	JUMP_FORWARD      '191'
190	END_FINALLY       None
191_0	COME_FROM         '181'
191_1	COME_FROM         '190'

191	SETUP_EXCEPT      '264'

194	LOAD_FAST         'builtinIds'
197	LOAD_ATTR         'add'
200	LOAD_GLOBAL       'id'
203	LOAD_GLOBAL       'uber'
206	CALL_FUNCTION_1   None
209	CALL_FUNCTION_1   None
212	POP_TOP           None

213	LOAD_FAST         'builtinIds'
216	LOAD_ATTR         'add'
219	LOAD_GLOBAL       'id'
222	LOAD_GLOBAL       'uber'
225	LOAD_ATTR         'air'
228	CALL_FUNCTION_1   None
231	CALL_FUNCTION_1   None
234	POP_TOP           None

235	LOAD_FAST         'builtinIds'
238	LOAD_ATTR         'add'
241	LOAD_GLOBAL       'id'
244	LOAD_GLOBAL       'uber'
247	LOAD_ATTR         'air'
250	LOAD_ATTR         'doId2do'
253	CALL_FUNCTION_1   None
256	CALL_FUNCTION_1   None
259	POP_TOP           None
260	POP_BLOCK         None
261	JUMP_FORWARD      '271'
264_0	COME_FROM         '191'

264	POP_TOP           None
265	POP_TOP           None
266	POP_TOP           None

267	JUMP_FORWARD      '271'
270	END_FINALLY       None
271_0	COME_FROM         '261'
271_1	COME_FROM         '270'

271	SETUP_LOOP        '690'
274	LOAD_GLOBAL       'True'
277	JUMP_IF_FALSE     '689'

280	LOAD_CONST        None
283	YIELD_VALUE       None

284	LOAD_GLOBAL       'messenger'
287	LOAD_ATTR         '_Messenger__objectEvents'
290	LOAD_ATTR         'keys'
293	CALL_FUNCTION_0   None
296	STORE_FAST        'objects'

299	SETUP_LOOP        '686'
302	LOAD_FAST         'objects'
305	GET_ITER          None
306	FOR_ITER          '685'
309	STORE_FAST        'object'

312	LOAD_CONST        None
315	YIELD_VALUE       None

316	BUILD_LIST_0      None
319	STORE_FAST        'objList1'

322	BUILD_LIST_0      None
325	STORE_FAST        'objList2'

328	LOAD_FAST         'objList1'
331	STORE_FAST        'curObjList'

334	LOAD_FAST         'objList2'
337	STORE_FAST        'nextObjList'

340	LOAD_GLOBAL       'set'
343	CALL_FUNCTION_0   None
346	STORE_FAST        'visitedObjIds'

349	LOAD_FAST         'visitedObjIds'
352	LOAD_ATTR         'add'
355	LOAD_GLOBAL       'id'
358	LOAD_FAST         'object'
361	CALL_FUNCTION_1   None
364	CALL_FUNCTION_1   None
367	POP_TOP           None

368	LOAD_FAST         'visitedObjIds'
371	LOAD_ATTR         'add'
374	LOAD_GLOBAL       'id'
377	LOAD_GLOBAL       'messenger'
380	LOAD_ATTR         '_Messenger__objectEvents'
383	CALL_FUNCTION_1   None
386	CALL_FUNCTION_1   None
389	POP_TOP           None

390	LOAD_FAST         'visitedObjIds'
393	LOAD_ATTR         'add'
396	LOAD_GLOBAL       'id'
399	LOAD_GLOBAL       'messenger'
402	LOAD_ATTR         '_Messenger__callbacks'
405	CALL_FUNCTION_1   None
408	CALL_FUNCTION_1   None
411	POP_TOP           None

412	LOAD_FAST         'nextObjList'
415	LOAD_ATTR         'append'
418	LOAD_FAST         'object'
421	CALL_FUNCTION_1   None
424	POP_TOP           None

425	LOAD_GLOBAL       'False'
428	STORE_FAST        'foundBuiltin'

431	SETUP_LOOP        '647'
434	LOAD_GLOBAL       'len'
437	LOAD_FAST         'nextObjList'
440	CALL_FUNCTION_1   None
443	JUMP_IF_FALSE     '646'

446	LOAD_FAST         'foundBuiltin'
449	JUMP_IF_FALSE     '456'

452	BREAK_LOOP        None
453	JUMP_FORWARD      '456'
456_0	COME_FROM         '453'

456	LOAD_FAST         'nextObjList'
459	STORE_FAST        'curObjList'

462	BUILD_LIST_0      None
465	STORE_FAST        'nextObjList'

468	SETUP_LOOP        '643'
471	LOAD_FAST         'curObjList'
474	GET_ITER          None
475	FOR_ITER          '642'
478	STORE_FAST        'curObj'

481	LOAD_FAST         'foundBuiltin'
484	JUMP_IF_FALSE     '491'

487	BREAK_LOOP        None
488	JUMP_FORWARD      '491'
491_0	COME_FROM         '488'

491	LOAD_CONST        None
494	YIELD_VALUE       None

495	LOAD_GLOBAL       'gc'
498	LOAD_ATTR         'get_referrers'
501	LOAD_FAST         'curObj'
504	CALL_FUNCTION_1   None
507	STORE_FAST        'referrers'

510	SETUP_LOOP        '639'
513	LOAD_FAST         'referrers'
516	GET_ITER          None
517	FOR_ITER          '638'
520	STORE_FAST        'referrer'

523	LOAD_CONST        None
526	YIELD_VALUE       None

527	LOAD_GLOBAL       'id'
530	LOAD_FAST         'referrer'
533	CALL_FUNCTION_1   None
536	STORE_FAST        'refId'

539	LOAD_FAST         'refId'
542	LOAD_FAST         'visitedObjIds'
545	COMPARE_OP        'in'
548	JUMP_IF_FALSE     '557'

551	CONTINUE          '517'
554	JUMP_FORWARD      '557'
557_0	COME_FROM         '554'

557	LOAD_FAST         'referrer'
560	LOAD_FAST         'curObjList'
563	COMPARE_OP        'is'
566	JUMP_IF_TRUE      '581'
569	LOAD_FAST         'referrer'
572	LOAD_FAST         'nextObjList'
575	COMPARE_OP        'is'
578_0	COME_FROM         '566'
578	JUMP_IF_FALSE     '587'

581	CONTINUE          '517'
584	JUMP_FORWARD      '587'
587_0	COME_FROM         '584'

587	LOAD_FAST         'refId'
590	LOAD_FAST         'builtinIds'
593	COMPARE_OP        'in'
596	JUMP_IF_FALSE     '609'

599	LOAD_GLOBAL       'True'
602	STORE_FAST        'foundBuiltin'

605	BREAK_LOOP        None
606	JUMP_BACK         '517'

609	LOAD_FAST         'visitedObjIds'
612	LOAD_ATTR         'add'
615	LOAD_FAST         'refId'
618	CALL_FUNCTION_1   None
621	POP_TOP           None

622	LOAD_FAST         'nextObjList'
625	LOAD_ATTR         'append'
628	LOAD_FAST         'referrer'
631	CALL_FUNCTION_1   None
634	POP_TOP           None
635	JUMP_BACK         '517'
638	POP_BLOCK         None
639_0	COME_FROM         '510'
639	JUMP_BACK         '475'_TOP           None

622	LOAD_FAST         'nextObjList'
625	LOAD_ATTR         'append'
628	LOAD_FAST         'referrer'
631	CALL_FUNCTION_1   None
634	POP_TOP           None
635	JUMP_BACK         '517'
638	POP_BLOCK         None
639_0	COME_FROM         '510'
639	JUMP_BACK         '475'
642	POP_BLOCK         None
643_0	COME_FROM         '468'
643	JUMP_BACK         '434'
646	POP_BLOCK         None
647_0	COME_FROM         '431'

647	LOAD_FAST         'foundBuiltin'
650	JUMP_IF_TRUE      '682'

653	LOAD_FAST         'self'
656	LOAD_ATTR         'notify'
659	LOAD_ATTR         'warning'
662	LOAD_CONST        '%s is referenced only by the messenger'
665	LOAD_GLOBAL       'itype'
668	LOAD_FAST         'object'
671	CALL_FUNCTION_1   None
674	BINARY_MODULO     None
675	CALL_FUNCTION_1   None
678	POP_TOP           None
679	JUMP_BACK         '306'
682	JUMP_BACK         '306'
685	POP_BLOCK         None
686_0	COME_FROM         '299'
686	JUMP_BACK         '274'
689	POP_BLOCK         None
690_0	COME_FROM         '271'
690	LOAD_CONST        None
693	RETURN_VALUE      None

Syntax error at or near `STORE_FAST' token at offset 296# decompiled 0 files: 0 okay, 1 failed, 0 verify failed
# 2013.08.22 22:14:39 Pacific Daylight Time

642	POP_BLOCK         None
643_0	COME_FROM         '468'
643	JUMP_BACK         '434'
646	POP_BLOCK         None
647_0	COME_FROM         '431'

647	LOAD_FAST         'foundBuiltin'
650	JUMP_IF_TRUE      '682'

653	LOAD_FAST         'self'
656	LOAD_ATTR         'notify'
659	LOAD_ATTR         'warning'
662	LOAD_CONST        '%s is referenced only by the messenger'
665	LOAD_GLOBAL       'itype'
668	LOAD_FAST         'object'
671	CALL_FUNCTION_1   None
674	BINARY_MODULO     None
675	CALL_FUNCTION_1   None
678	POP_TOP           None
679	JUMP_BACK         '306'
682	JUMP_BACK         '306'
685	POP_BLOCK         None
686_0	COME_FROM         '299'
686	JUMP_BACK         '274'
689	POP_BLOCK         None
690_0	COME_FROM         '271'
690	LOAD_CONST        None
693	RETURN_VALUE      None

Syntax error at or near `STORE_FAST' token at offset 296

