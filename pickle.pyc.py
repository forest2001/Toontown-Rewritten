# 2013.08.22 22:13:15 Pacific Daylight Time
# Embedded file name: pickle
--- This code section failed: ---

0	LOAD_CONST        '$Revision: 1.1.1.1 $'
3	STORE_NAME        '__version__'

6	LOAD_CONST        ('*',)
9	IMPORT_NAME       'types'
12	IMPORT_STAR       None

13	LOAD_CONST        ('dispatch_table',)
16	IMPORT_NAME       'copy_reg'
19	IMPORT_FROM       'dispatch_table'
22	STORE_NAME        'dispatch_table'
25	POP_TOP           None

26	LOAD_CONST        ('_extension_registry', '_inverted_registry', '_extension_cache')
29	IMPORT_NAME       'copy_reg'
32	IMPORT_FROM       '_extension_registry'
35	STORE_NAME        '_extension_registry'
38	IMPORT_FROM       '_inverted_registry'
41	STORE_NAME        '_inverted_registry'
44	IMPORT_FROM       '_extension_cache'
47	STORE_NAME        '_extension_cache'
50	POP_TOP           None

51	LOAD_CONST        None
54	IMPORT_NAME       'marshal'
57	STORE_NAME        'marshal'

60	LOAD_CONST        None
63	IMPORT_NAME       'sys'
66	STORE_NAME        'sys'

69	LOAD_CONST        None
72	IMPORT_NAME       'struct'
75	STORE_NAME        'struct'

78	LOAD_CONST        None
81	IMPORT_NAME       're'
84	STORE_NAME        're'

87	LOAD_CONST        None
90	IMPORT_NAME       'warnings'
93	STORE_NAME        'warnings'

96	LOAD_CONST        'PickleError'
99	LOAD_CONST        'PicklingError'
102	LOAD_CONST        'UnpicklingError'
105	LOAD_CONST        'Pickler'
108	LOAD_CONST        'Unpickler'
111	LOAD_CONST        'dump'
114	LOAD_CONST        'dumps'
117	LOAD_CONST        'load'
120	LOAD_CONST        'loads'
123	BUILD_LIST_9      None
126	STORE_NAME        '__all__'

129	LOAD_CONST        '2.0'
132	STORE_NAME        'format_version'

135	LOAD_CONST        '1.0'
138	LOAD_CONST        '1.1'
141	LOAD_CONST        '1.2'
144	LOAD_CONST        '1.3'
147	LOAD_CONST        '2.0'
150	BUILD_LIST_5      None
153	STORE_NAME        'compatible_formats'

156	LOAD_CONST        2
159	STORE_NAME        'HIGHEST_PROTOCOL'

162	LOAD_NAME         'marshal'
165	LOAD_ATTR         'loads'
168	STORE_NAME        'mloads'

171	LOAD_CONST        'PickleError'
174	LOAD_NAME         'Exception'
177	BUILD_TUPLE_1     None
180	LOAD_CONST        '<code_object PickleError>'
183	MAKE_FUNCTION_0   None
186	CALL_FUNCTION_0   None
189	BUILD_CLASS       None
190	STORE_NAME        'PickleError'

193	LOAD_CONST        'PicklingError'
196	LOAD_NAME         'PickleError'
199	BUILD_TUPLE_1     None
202	LOAD_CONST        '<code_object PicklingError>'
205	MAKE_FUNCTION_0   None
208	CALL_FUNCTION_0   None
211	BUILD_CLASS       None
212	STORE_NAME        'PicklingError'

215	LOAD_CONST        'UnpicklingError'
218	LOAD_NAME         'PickleError'
221	BUILD_TUPLE_1     None
224	LOAD_CONST        '<code_object UnpicklingError>'
227	MAKE_FUNCTION_0   None
230	CALL_FUNCTION_0   None
233	BUILD_CLASS       None
234	STORE_NAME        'UnpicklingError'

237	LOAD_CONST        '_Stop'
240	LOAD_NAME         'Exception'
243	BUILD_TUPLE_1     None
246	LOAD_CONST        '<code_object _Stop>'
249	MAKE_FUNCTION_0   None
252	CALL_FUNCTION_0   None
255	BUILD_CLASS       None
256	STORE_NAME        '_Stop'

259	SETUP_EXCEPT      '279'

262	LOAD_CONST        ('PyStringMap',)
265	IMPORT_NAME       'org.python.core'
268	IMPORT_FROM       'PyStringMap'
271	STORE_NAME        'PyStringMap'
274	POP_TOP           None
275	POP_BLOCK         None
276	JUMP_FORWARD      '302'
279_0	COME_FROM         '259'

279	DUP_TOP           None
280	LOAD_NAME         'ImportError'
283	COMPARE_OP        'exception match'
286	JUMP_IF_FALSE     '301'
289	POP_TOP           None
290	POP_TOP           None
291	POP_TOP           None

292	LOAD_NAME         'None'
295	STORE_NAME        'PyStringMap'
298	JUMP_FORWARD      '302'
301	END_FINALLY       None
302_0	COME_FROM         '276'
302_1	COME_FROM         '301'

302	SETUP_EXCEPT      '313'

305	LOAD_NAME         'UnicodeType'
308	POP_TOP           None
309	POP_BLOCK         None
310	JUMP_FORWARD      '336'
313_0	COME_FROM         '302'

313	DUP_TOP           None
314	LOAD_NAME         'NameError'
317	COMPARE_OP        'exception match'
320	JUMP_IF_FALSE     '335'
323	POP_TOP           None
324	POP_TOP           None
325	POP_TOP           None

326	LOAD_NAME         'None'
329	STORE_NAME        'UnicodeType'
332	JUMP_FORWARD      '336'
335	END_FINALLY       None
336_0	COME_FROM         '310'
336_1	COME_FROM         '335'

336	LOAD_CONST        '('
339	STORE_NAME        'MARK'

342	LOAD_CONST        '.'
345	STORE_NAME        'STOP'

348	LOAD_CONST        '0'
351	STORE_NAME        'POP'

354	LOAD_CONST        '1'
357	STORE_NAME        'POP_MARK'

360	LOAD_CONST        '2'
363	STORE_NAME        'DUP'

366	LOAD_CONST        'F'
369	STORE_NAME        'FLOAT'

372	LOAD_CONST        'I'
375	STORE_NAME        'INT'

378	LOAD_CONST        'J'
381	STORE_NAME        'BININT'

384	LOAD_CONST        'K'
387	STORE_NAME        'BININT1'

390	LOAD_CONST        'L'
393	STORE_NAME        'LONG'

396	LOAD_CONST        'M'
399	STORE_NAME        'BININT2'

402	LOAD_CONST        'N'
405	STORE_NAME        'NONE'

408	LOAD_CONST        'P'
411	STORE_NAME        'PERSID'

414	LOAD_CONST        'Q'
417	STORE_NAME        'BINPERSID'

420	LOAD_CONST        'R'
423	STORE_NAME        'REDUCE'

426	LOAD_CONST        'S'
429	STORE_NAME        'STRING'

432	LOAD_CONST        'T'
435	STORE_NAME        'BINSTRING'

438	LOAD_CONST        'U'
441	STORE_NAME        'SHORT_BINSTRING'

444	LOAD_CONST        'V'
447	STORE_NAME        'UNICODE'

450	LOAD_CONST        'X'
453	STORE_NAME        'BINUNICODE'

456	LOAD_CONST        'a'
459	STORE_NAME        'APPEND'

462	LOAD_CONST        'b'
465	STORE_NAME        'BUILD'

468	LOAD_CONST        'c'
471	STORE_NAME        'GLOBAL'

474	LOAD_CONST        'd'
477	STORE_NAME        'DICT'

480	LOAD_CONST        '}'
483	STORE_NAME        'EMPTY_DICT'

486	LOAD_CONST        'e'
489	STORE_NAME        'APPENDS'

492	LOAD_CONST        'g'
495	STORE_NAME        'GET'

498	LOAD_CONST        'h'
501	STORE_NAME        'BINGET'

504	LOAD_CONST        'i'
507	STORE_NAME        'INST'

510	LOAD_CONST        'j'
513	STORE_NAME        'LONG_BINGET'

516	LOAD_CONST        'l'
519	STORE_NAME        'LIST'

522	LOAD_CONST        ']'
525	STORE_NAME        'EMPTY_LIST'

528	LOAD_CONST        'o'
531	STORE_NAME        'OBJ'

534	LOAD_CONST        'p'
537	STORE_NAME        'PUT'

540	LOAD_CONST        'q'
543	STORE_NAME        'BINPUT'

546	LOAD_CONST        'r'
549	STORE_NAME        'LONG_BINPUT'

552	LOAD_CONST        's'
555	STORE_NAME        'SETITEM'

558	LOAD_CONST        't'
561	STORE_NAME        'TUPLE'

564	LOAD_CONST        ')'
567	STORE_NAME        'EMPTY_TUPLE'

570	LOAD_CONST        'u'
573	STORE_NAME        'SETITEMS'

576	LOAD_CONST        'G'
579	STORE_NAME        'BINFLOAT'

582	LOAD_CONST        'I01\n'
585	STORE_NAME        'TRUE'

588	LOAD_CONST        'I00\n'
591	STORE_NAME        'FALSE'

594	LOAD_CONST        '\x80'
597	STORE_NAME        'PROTO'

600	LOAD_CONST        '\x81'
603	STORE_NAME        'NEWOBJ'

606	LOAD_CONST        '\x82'
609	STORE_NAME        'EXT1'

612	LOAD_CONST        '\x83'
615	STORE_NAME        'EXT2'

618	LOAD_CONST        '\x84'
621	STORE_NAME        'EXT4'

624	LOAD_CONST        '\x85'
627	STORE_NAME        'TUPLE1'

630	LOAD_CONST        '\x86'
633	STORE_NAME        'TUPLE2'

636	LOAD_CONST        '\x87'
639	STORE_NAME        'TUPLE3'

642	LOAD_CONST        '\x88'
645	STORE_NAME        'NEWTRUE'

648	LOAD_CONST        '\x89'
651	STORE_NAME        'NEWFALSE'

654	LOAD_CONST        '\x8a'
657	STORE_NAME        'LONG1'

660	LOAD_CONST        '\x8b'
663	STORE_NAME        'LONG4'

666	LOAD_NAME         'EMPTY_TUPLE'
669	LOAD_NAME         'TUPLE1'
672	LOAD_NAME         'TUPLE2'
675	LOAD_NAME         'TUPLE3'
678	BUILD_LIST_4      None
681	STORE_NAME        '_tuplesize2code'

684	LOAD_NAME         '__all__'
687	LOAD_ATTR         'extend'
690	BUILD_LIST_0      None
693	LOAD_NAME         'dir'
696	CALL_FUNCTION_0   None
699	GET_ITER          None
700	FOR_ITER          '736'
703	STORE_NAME        'x'
706	LOAD_NAME         're'
709	LOAD_ATTR         'match'
712	LOAD_CONST        '[A-Z][A-Z0-9_]+$'
715	LOAD_NAME         'x'
718	CALL_FUNCTION_2
# Can't uncompyle C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\pickle.pyc
Traceback (most recent call last):
  File "C:\python27\lib\uncompyle2\__init__.py", line 206, in main
    uncompyle_file(infile, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 143, in uncompyle_file
    uncompyle(version, co, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 110, in uncompyle
    ast = walk.build_ast(tokens, customize)
  File "C:\python27\lib\uncompyle2\walker.py", line 1444, in build_ast
    raise ParserError(e, tokens)
ParserError: --- This code section failed: ---

0	LOAD_CONST        '$Revision: 1.1.1.1 $'
3	STORE_NAME        '__version__'

6	LOAD_CONST        ('*',)
9	IMPORT_NAME       'types'
12	IMPORT_STAR       None

13	LOAD_CONST        ('dispatch_table',)
16	IMPORT_NAME       'copy_reg'
19	IMPORT_FROM       'dispatch_table'
22	STORE_NAME        'dispatch_table'
25	POP_TOP           None

26	LOAD_CONST        ('_extension_registry', '_inverted_registry', '_extension_cache')
29	IMPORT_NAME       'copy_reg'
32	IMPORT_FROM       '_extension_registry'
35	STORE_NAME        '_extension_registry'
38	IMPORT_FROM       '_inverted_registry'
41	STORE_NAME        '_inverted_registry'
44	IMPORT_FROM       '_extension_cache'
47	STORE_NAME        '_extension_cache'
50	POP_TOP           None

51	LOAD_CONST        None
54	IMPORT_NAME       'marshal'
57	STORE_NAME        'marshal'

60	LOAD_CONST        None
63	IMPORT_NAME       'sys'
66	STORE_NAME        'sys'

69	LOAD_CONST        None
72	IMPORT_NAME       'struct'
75	STORE_NAME        'struct'

78	LOAD_CONST        None
81	IMPORT_NAME       're'
84	STORE_NAME        're'

87	LOAD_CONST        None
90	IMPORT_NAME       'warnings'
93	STORE_NAME        'warnings'

96	LOAD_CONST        'PickleError'
99	LOAD_CONST        'PicklingError'
102	LOAD_CONST        'UnpicklingError'
105	LOAD_CONST        'Pickler'
108	LOAD_CONST        'Unpickler'
111	LOAD_CONST        'dump'
114	LOAD_CONST        'dumps'
117	LOAD_CONST        'load'
120	LOAD_CONST        'loads'
123	BUILD_LIST_9      None
126	STORE_NAME        '__all__'

129	LOAD_CONST        '2.0'
132	STORE_NAME        'format_version'

135	LOAD_CONST        '1.0'
138	LOAD_CONST        '1.1'
141	LOAD_CONST        '1.2'
144	LOAD_CONST        '1.3'
147	LOAD_CONST        '2.0'
150	BUILD_LIST_5      None
153	STORE_NAME        'compatible_formats'

156	LOAD_CONST        2
159	STORE_NAME        'HIGHEST_PROTOCOL'

162	LOAD_NAME         'marshal'
165	LOAD_ATTR         'loads'
168	STORE_NAME        'mloads'

171	LOAD_CONST        'PickleError'
174	LOAD_NAME         'Exception'
177	BUILD_TUPLE_1     None
180	LOAD_CONST        '<code_object PickleError>'
183	MAKE_FUNCTION_0   None
186	CALL_FUNCTION_0   None
189	BUILD_CLASS       None
190	STORE_NAME        'PickleError'

193	LOAD_CONST        'PicklingError'
196	LOAD_NAME         'PickleError'
199	BUILD_TUPLE_1     None
202	LOAD_CONST        '<code_object PicklingError>'
205	MAKE_FUNCTION_0   None
208	CALL_FUNCTION_0   None
211	BUILD_CLASS       None
212	STORE_NAME        'PicklingError'

215	LOAD_CONST        'UnpicklingError'
218	LOAD_NAME         'PickleError'
221	BUILD_TUPLE_1     None
224	LOAD_CONST        '<code_object UnpicklingError>'
227	MAKE_FUNCTION_0   None
230	CALL_FUNCTION_0   None
233	BUILD_CLASS       None
234	STORE_NAME        'UnpicklingError'

237	LOAD_CONST        '_Stop'
240	LOAD_NAME         'Exception'
243	BUILD_TUPLE_1     None
246	LOAD_CONST        '<code_object _Stop>'
249	MAKE_FUNCTION_0   None
252	CALL_FUNCTION_0   None
255	BUILD_CLASS       None
256	STORE_NAME        '_Stop'

259	SETUP_EXCEPT      '279'

262	LOAD_CONST        ('PyStringMap',)
265	IMPORT_NAME       'org.python.core'
268	IMPORT_FROM       'PyStringMap'
271	STORE_NAME        'PyStringMap'
274	POP_TOP           None
275	POP_BLOCK         None
276	JUMP_FORWARD      '302'
279_0	COME_FROM         '259'

279	DUP_TOP           None
280	LOAD_NAME         'ImportError'
283	COMPARE_OP        'exception match'
286	JUMP_IF_FALSE     '301'
289	POP_TOP           None
290	POP_TOP           None
291	POP_TOP           None

292	LOAD_NAME         'None'
295	STORE_NAME        'PyStringMap'
298	JUMP_FORWARD      '302'
301	END_FINALLY       None
302_0	COME_FROM         '276'
302_1	COME_FROM         '301'

302	SETUP_EXCEPT      '313'

305	LOAD_NAME         'UnicodeType'
308	POP_TOP           None
309	POP_BLOCK         None
310	JUMP_FORWARD      '336'
313_0	COME_FROM         '302'

313	DUP_TOP           None
314	LOAD_NAME         'NameError'
317	COMPARE_OP        'exception match'
320	JUMP_IF_FALSE     '335'
323	POP_TOP           None
324	POP_TOP           None
325	POP_TOP           None

326	LOAD_NAME         'None'
329	STORE_NAME        'UnicodeType'
332	JUMP_FORWARD      '336'
335	END_FINALLY       None
336_0	COME_FROM         '310'
336_1	COME_FROM         '335'

336	LOAD_CONST        '('
339	STORE_NAME        'MARK'

342	LOAD_CONST        '.'
345	STORE_NAME        'STOP'

348	LOAD_CONST        '0'
351	STORE_NAME        'POP'

354	LOAD_CONST        '1'
357	STORE_NAME        'POP_MARK'

360	LOAD_CONST        '2'
363	STORE_NAME        'DUP'

366	LOAD_CONST        'F'
369	STORE_NAME        'FLOAT'

372	LOAD_CONST        'I'
375	STORE_NAME        'INT'

378	LOAD_CONST        'J'
381	STORE_NAME        'BININT'

384	LOAD_CONST        'K'
387	STORE_NAME        'BININT1'

390	LOAD_CONST        'L'
393	STORE_NAME        'LONG'

396	LOAD_CONST        'M'
399	STORE_NAME        'BININT2'

402	LOAD_CONST        'N'
405	STORE_NAME        'NONE'

408	LOAD_CONST        'P'
411	STORE_NAME        'PERSID'

414	LOAD_CONST        'Q'
417	STORE_NAME        'BINPERSID'

420	LOAD_CONST        'R'
423	STORE_NAME        'REDUCE'

426	LOAD_CONST        'S'
429	STORE_NAME        'STRING'

432	LOAD_CONST        'T'
435	STORE_NAME        'BINSTRING'

438	LOAD_CONST        'U'
441	STORE_NAME        'SHORT_BINSTRING'

444	LOAD_CONST        'V'
447	STORE_NAME        'UNICODE'

450	LOAD_CONST        'X'
453	STORE_NAME        'BINUNICODE'

456	LOAD_CONST        'a'
459	STORE_NAME        'APPEND'

462	LOAD_CONST        'b'
465	STORE_NAME        'BUILD'

468	LOAD_CONST        'c'
471	STORE_NAME        'GLOBAL'

474	LOAD_CONST        'd'
477	STORE_NAME        'DICT'

480	LOAD_CONST        '}'
483	STORE_NAME        'EMPTY_DICT'

486	LOAD_CONST        'e'
489	STORE_NAME        'APPENDS'

492	LOAD_CONST        'g'
495	STORE_NAME        'GET'

498	LOAD_CONST        'h'
501	STORE_NAME        'BINGET'

504	LOAD_CONST        'i'
507	STORE_NAME        'INST'

510	LOAD_CONST        'j'
513	STORE_NAME        'LONG_BINGET'

516	LOAD_CONST        'l'
519	STORE_NAME        'LIST'

522	LOAD_CONST        ']'
525	STORE_NAME        'EMPTY_LIST'

528	LOAD_CONST        'o'
531	STORE_NAME        'OBJ'

534	LOAD_CONST        'p'
537	STORE_NAME        'PUT'

540	LOAD_CONST        'q'
543	STORE_NAME        'BINPUT'

546	LOAD_CONST        'r'
549	STORE_NAME        'LONG_BINPUT'

552	LOAD_CONST        's'
555	STORE_NAME        'SETITEM'

558	LOAD_CONST        't'
561	STORE_NAME        'TUPLE'

564	LOAD_CONST        ')'
567	STORE_NAME        'EMPTY_TUPLE'

570	LOAD_CONST        'u'
573	STORE_NAME        'SETITEMS'

576	LOAD_CONST        'G'
579	STORE_NAME        'BINFLOAT'

582	LOAD_CONST        'I01\n'
585	STORE_NAME        'TRUE'

588	LOAD_CONST        'I00\n'
591	STORE_NAME        'FALSE'

594	LOAD_CONST        '\x80'
597	STORE_NAME        'PROTO'

600	LOAD_CONST        '\x81'
603	STORE_NAME        'NEWOBJ'

606	LOAD_CONST        '\x82'
609	STORE_NAME        'EXT1'

612	LOAD_CONST        '\x83'
615	STORE_NAME        'EXT2'

618	LOAD_CONST        '\x84'
621	STORE_NAME        'EXT4'

624	LOAD_CONST        '\x85'
627	STORE_NAME        'TUPLE1'

630	LOAD_CONST        '\x86'
633	STORE_NAME        'TUPLE2'

636	LOAD_CONST        '\x87'
639	STORE_NAME        'TUPLE3'

642	LOAD_CONST        '\x88'
645	STORE_NAME        'NEWTRUE'

648	LOAD_CONST        '\x89'
651	STORE_NAME        'NEWFALSE'

654	LOAD_CONST        '\x8a'
657	STORE_NAME        'LONG1'

660	LOAD_CONST        '\x8b'
663	STORE_NAME        'LONG4'

666	LOAD_NAME     None
721	JUMP_IF_FALSE     '733'
724	LOAD_NAME         'x'
727	LIST_APPEND       None
730	JUMP_FORWARD      '733'
733_0	COME_FROM         '730'
733	CONTINUE          '700'
736	CALL_FUNCTION_1   None
739	POP_TOP           None

740	DELETE_NAME       'x'

743	LOAD_CONST        'Pickler'
746	BUILD_TUPLE_0     None
749	LOAD_CONST        '<code_object Pickler>'
752	MAKE_FUNCTION_0   None
755	CALL_FUNCTION_0   None
758	BUILD_CLASS       None
759	STORE_NAME        'Pickler'

762	LOAD_CONST        '<code_object _keep_alive>'
765	MAKE_FUNCTION_0   None
768	STORE_NAME        '_keep_alive'

771	BUILD_MAP         None
774	STORE_NAME        'classmap'

777	LOAD_CONST        '<code_object whichmodule>'
780	MAKE_FUNCTION_0   None
783	STORE_NAME        'whichmodule'

786	LOAD_CONST        'Unpickler'
789	BUILD_TUPLE_0     None
792	LOAD_CONST        '<code_object Unpickler>'
795	MAKE_FUNCTION_0   None
798	CALL_FUNCTION_0   None
801	BUILD_CLASS       None
802	STORE_NAME        'Unpickler'

805	LOAD_CONST        '_EmptyClass'
808	BUILD_TUPLE_0     None
811	LOAD_CONST        '<code_object _EmptyClass>'
814	MAKE_FUNCTION_0   None
817	CALL_FUNCTION_0   None
820	BUILD_CLASS       None
821	STORE_NAME        '_EmptyClass'

824	LOAD_CONST        None
827	IMPORT_NAME       'binascii'
830	STORE_NAME        '_binascii'

833	LOAD_CONST        '<code_object encode_long>'
836	MAKE_FUNCTION_0   None
839	STORE_NAME        'encode_long'

842	LOAD_CONST        '<code_object decode_long>'
845	MAKE_FUNCTION_0   None
848	STORE_NAME        'decode_long'

851	SETUP_EXCEPT      '871'

854	LOAD_CONST        ('StringIO',)
857	IMPORT_NAME       'cStringIO'
860	IMPORT_FROM       'StringIO'
863	STORE_NAME        'StringIO'
866	POP_TOP           None
867	POP_BLOCK         None
868	JUMP_FORWARD      '901'
871_0	COME_FROM         '851'

871	DUP_TOP           None
872	LOAD_NAME         'ImportError'
875	COMPARE_OP        'exception match'
878	JUMP_IF_FALSE     '900'
881	POP_TOP           None
882	POP_TOP           None
883	POP_TOP           None

884	LOAD_CONST        ('StringIO',)
887	IMPORT_NAME       'StringIO'
890	IMPORT_FROM       'StringIO'
893	STORE_NAME        'StringIO'
896	POP_TOP           None
897	JUMP_FORWARD      '901'
900	END_FINALLY       None
901_0	COME_FROM         '868'
901_1	COME_FROM         '900'

901	LOAD_NAME         'None'
904	LOAD_NAME         'None'
907	LOAD_CONST        '<code_object dump>'
910	MAKE_FUNCTION_2   None
913	STORE_NAME        'dump'

916	LOAD_NAME         'None'
919	LOAD_NAME         'None'
922	LOAD_CONST        '<code_object dumps>'
925	MAKE_FUNCTION_2   None
928	STORE_NAME        'dumps'

931	LOAD_CONST        '<code_object load>'
934	MAKE_FUNCTION_0   None
937	STORE_NAME        'load'

940	LOAD_CONST        '<code_object loads>'
943	MAKE_FUNCTION_0   None
946	STORE_NAME        'loads'

949	LOAD_CONST        '<code_object _test>'
952	MAKE_FUNCTION_0   None
955	STORE_NAME        '_test'

958	LOAD_NAME         '__name__'
961	LOAD_CONST        '__main__'
964	COMPARE_OP        '=='
967	JUMP_IF_FALSE     '980'

970	LOAD_NAME         '_test'
973	CALL_FUNCTION_0   None
976	POP_TOP           None
977	JUMP_FORWARD      '980'
980_0	COME_FROM         '977'

Syntax error at or near `JUMP_FORWARD' token at offset 730

# decompiled 0 files: 0 okay, 1 failed, 0 verify failed
# 2013.08.22 22:13:15 Pacific Daylight Time
       'EMPTY_TUPLE'
669	LOAD_NAME         'TUPLE1'
672	LOAD_NAME         'TUPLE2'
675	LOAD_NAME         'TUPLE3'
678	BUILD_LIST_4      None
681	STORE_NAME        '_tuplesize2code'

684	LOAD_NAME         '__all__'
687	LOAD_ATTR         'extend'
690	BUILD_LIST_0      None
693	LOAD_NAME         'dir'
696	CALL_FUNCTION_0   None
699	GET_ITER          None
700	FOR_ITER          '736'
703	STORE_NAME        'x'
706	LOAD_NAME         're'
709	LOAD_ATTR         'match'
712	LOAD_CONST        '[A-Z][A-Z0-9_]+$'
715	LOAD_NAME         'x'
718	CALL_FUNCTION_2   None
721	JUMP_IF_FALSE     '733'
724	LOAD_NAME         'x'
727	LIST_APPEND       None
730	JUMP_FORWARD      '733'
733_0	COME_FROM         '730'
733	CONTINUE          '700'
736	CALL_FUNCTION_1   None
739	POP_TOP           None

740	DELETE_NAME       'x'

743	LOAD_CONST        'Pickler'
746	BUILD_TUPLE_0     None
749	LOAD_CONST        '<code_object Pickler>'
752	MAKE_FUNCTION_0   None
755	CALL_FUNCTION_0   None
758	BUILD_CLASS       None
759	STORE_NAME        'Pickler'

762	LOAD_CONST        '<code_object _keep_alive>'
765	MAKE_FUNCTION_0   None
768	STORE_NAME        '_keep_alive'

771	BUILD_MAP         None
774	STORE_NAME        'classmap'

777	LOAD_CONST        '<code_object whichmodule>'
780	MAKE_FUNCTION_0   None
783	STORE_NAME        'whichmodule'

786	LOAD_CONST        'Unpickler'
789	BUILD_TUPLE_0     None
792	LOAD_CONST        '<code_object Unpickler>'
795	MAKE_FUNCTION_0   None
798	CALL_FUNCTION_0   None
801	BUILD_CLASS       None
802	STORE_NAME        'Unpickler'

805	LOAD_CONST        '_EmptyClass'
808	BUILD_TUPLE_0     None
811	LOAD_CONST        '<code_object _EmptyClass>'
814	MAKE_FUNCTION_0   None
817	CALL_FUNCTION_0   None
820	BUILD_CLASS       None
821	STORE_NAME        '_EmptyClass'

824	LOAD_CONST        None
827	IMPORT_NAME       'binascii'
830	STORE_NAME        '_binascii'

833	LOAD_CONST        '<code_object encode_long>'
836	MAKE_FUNCTION_0   None
839	STORE_NAME        'encode_long'

842	LOAD_CONST        '<code_object decode_long>'
845	MAKE_FUNCTION_0   None
848	STORE_NAME        'decode_long'

851	SETUP_EXCEPT      '871'

854	LOAD_CONST        ('StringIO',)
857	IMPORT_NAME       'cStringIO'
860	IMPORT_FROM       'StringIO'
863	STORE_NAME        'StringIO'
866	POP_TOP           None
867	POP_BLOCK         None
868	JUMP_FORWARD      '901'
871_0	COME_FROM         '851'

871	DUP_TOP           None
872	LOAD_NAME         'ImportError'
875	COMPARE_OP        'exception match'
878	JUMP_IF_FALSE     '900'
881	POP_TOP           None
882	POP_TOP           None
883	POP_TOP           None

884	LOAD_CONST        ('StringIO',)
887	IMPORT_NAME       'StringIO'
890	IMPORT_FROM       'StringIO'
893	STORE_NAME        'StringIO'
896	POP_TOP           None
897	JUMP_FORWARD      '901'
900	END_FINALLY       None
901_0	COME_FROM         '868'
901_1	COME_FROM         '900'

901	LOAD_NAME         'None'
904	LOAD_NAME         'None'
907	LOAD_CONST        '<code_object dump>'
910	MAKE_FUNCTION_2   None
913	STORE_NAME        'dump'

916	LOAD_NAME         'None'
919	LOAD_NAME         'None'
922	LOAD_CONST        '<code_object dumps>'
925	MAKE_FUNCTION_2   None
928	STORE_NAME        'dumps'

931	LOAD_CONST        '<code_object load>'
934	MAKE_FUNCTION_0   None
937	STORE_NAME        'load'

940	LOAD_CONST        '<code_object loads>'
943	MAKE_FUNCTION_0   None
946	STORE_NAME        'loads'

949	LOAD_CONST        '<code_object _test>'
952	MAKE_FUNCTION_0   None
955	STORE_NAME        '_test'

958	LOAD_NAME         '__name__'
961	LOAD_CONST        '__main__'
964	COMPARE_OP        '=='
967	JUMP_IF_FALSE     '980'

970	LOAD_NAME         '_test'
973	CALL_FUNCTION_0   None
976	POP_TOP           None
977	JUMP_FORWARD      '980'
980_0	COME_FROM         '977'

Syntax error at or near `JUMP_FORWARD' token at offset 730

