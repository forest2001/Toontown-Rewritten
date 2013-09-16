# 2013.08.22 22:13:35 Pacific Daylight Time
# Embedded file name: tokenize
__author__ = 'Ka-Ping Yee <ping@lfw.org>'
__credits__ = 'GvR, ESR, Tim Peters, Thomas Wouters, Fred Drake, Skip Montanaro'
import string, re
from token import *
import token
__all__ = [ x for x in dir(token) if x[0] != '_' ] + ['COMMENT',
 'tokenize',
 'generate_tokens',
 'NL']
del x
del token
COMMENT = N_TOKENS
tok_name[COMMENT] = 'COMMENT'
NL = N_TOKENS + 1
tok_name[NL] = 'NL'
N_TOKENS += 2

def group(*choices):
    return '(' + '|'.join(choices) + ')'


def any(*choices):
    return group(*choices) + '*'


def maybe(*choices):
    return group(*choices) + '?'


Whitespace = '[ \\f\\t]*'
Comment = '#[^\\r\\n]*'
Ignore = Whitespace + any('\\\\\\r?\\n' + Whitespace) + maybe(Comment)
Name = '[a-zA-Z_]\\w*'
Hexnumber = '0[xX][\\da-fA-F]*[lL]?'
Octnumber = '0[0-7]*[lL]?'
Decnumber = '[1-9]\\d*[lL]?'
Intnumber = group(Hexnumber, Octnumber, Decnumber)
Exponent = '[eE][-+]?\\d+'
Pointfloat = group('\\d+\\.\\d*', '\\.\\d+') + maybe(Exponent)
Expfloat = '\\d+' + Exponent
Floatnumber = group(Pointfloat, Expfloat)
Imagnumber = group('\\d+[jJ]', Floatnumber + '[jJ]')
Number = group(Imagnumber, Floatnumber, Intnumber)
Single = "[^'\\\\]*(?:\\\\.[^'\\\\]*)*'"
Double = '[^"\\\\]*(?:\\\\.[^"\\\\]*)*"'
Single3 = "[^'\\\\]*(?:(?:\\\\.|'(?!''))[^'\\\\]*)*'''"
Double3 = '[^"\\\\]*(?:(?:\\\\.|"(?!""))[^"\\\\]*)*"""'
Triple = group("[uU]?[rR]?'''", '[uU]?[rR]?"""')
String = group("[uU]?[rR]?'[^\\n'\\\\]*(?:\\\\.[^\\n'\\\\]*)*'", '[uU]?[rR]?"[^\\n"\\\\]*(?:\\\\.[^\\n"\\\\]*)*"')
Operator = group('\\*\\*=?', '>>=?', '<<=?', '<>', '!=', '//=?', '[+\\-*/%&|^=<>]=?', '~')
Bracket = '[][(){}]'
Special = group('\\r?\\n', '[:;.,`@]')
Funny = group(Operator, Bracket, Special)
PlainToken = group(Number, Funny, String, Name)
Token = Ignore + PlainToken
ContStr = group("[uU]?[rR]?'[^\\n'\\\\]*(?:\\\\.[^\\n'\\\\]*)*" + group("'", '\\\\\\r?\\n'), '[uU]?[rR]?"[^\\n"\\\\]*(?:\\\\.[^\\n"\\\\]*)*' + group('"', '\\\\\\r?\\n'))
PseudoExtras = group('\\\\\\r?\\n', Comment, Triple)
PseudoToken = Whitespace + group(PseudoExtras, Number, Funny, ContStr, Name)
tokenprog, pseudoprog, single3prog, double3prog = map(re.compile, (Token,
 PseudoToken,
 Single3,
 Double3))
endprogs = {"'": re.compile(Single),
 '"': re.compile(Double),
 "'''": single3prog,
 '"""': double3prog,
 "r'''": single3prog,
 'r"""': double3prog,
 "u'''": single3prog,
 'u"""': double3prog,
 "ur'''": single3prog,
 'ur"""': double3prog,
 "R'''": single3prog,
 'R"""': double3prog,
 "U'''": single3prog,
 'U"""': double3prog,
 "uR'''": single3prog,
 'uR"""': double3prog,
 "Ur'''": single3prog,
 'Ur"""': double3prog,
 "UR'''": single3prog,
 'UR"""': double3prog,
 'r': None,
 'R': None,
 'u': None,
 'U': None}
triple_quoted = {}
for t in ("'''", '"""', "r'''", 'r"""', "R'''", 'R"""', "u'''", 'u"""', "U'''", 'U"""', "ur'''", 'ur"""', "Ur'''", 'Ur"""', "uR'''", 'uR"""', "UR'''", 'UR"""'):
    triple_quoted[t] = t

single_quoted = {}
for t in ("'", '"', "r'", 'r"', "R'", 'R"', "u'", 'u"', "U'", 'U"', "ur'", 'ur"', "Ur'", 'Ur"', "uR'", 'uR"', "UR'", 'UR"'):
    single_quoted[t] = t

tabsize = 8

class TokenError(Exception):
    __module__ = __name__


class StopTokenizing(Exception):
    __module__ = __name__


def printtoken(type, token, (srow, scol), (erow, ecol), line):
    print '%d,%d-%d,%d:\t%s\t%s' % (srow,
     scol,
     erow,
     ecol,
     tok_name[type],
     repr(token))


def tokenize(readline, tokeneater = printtoken):
    try:
        tokenize_loop(readline, tokeneater)
    except StopTokenizing:
        pass


def tokenize_loop(readline, tokeneater):
    for token_info in generate_tokens(readline):
        tokeneater(*token_info)


def generate_tokens--- This code section failed: ---

0	LOAD_CONST        0
3	DUP_TOP           None
4	STORE_FAST        'lnum'
7	DUP_TOP           None
8	STORE_FAST        'parenlev'
11	STORE_FAST        'continued'

14	LOAD_GLOBAL       'string'
17	LOAD_ATTR         'ascii_letters'
20	LOAD_CONST        '_'
23	BINARY_ADD        None
24	LOAD_CONST        '0123456789'
27	ROT_TWO           None
28	STORE_FAST        'namechars'
31	STORE_FAST        'numchars'

34	LOAD_CONST        ('', 0)
37	UNPACK_SEQUENCE_2 None
40	STORE_FAST        'contstr'
43	STORE_FAST        'needcont'

46	LOAD_CONST        None
49	STORE_FAST        'contline'

52	LOAD_CONST        0
55	BUILD_LIST_1      None
58	STORE_FAST        'indents'

61	SETUP_LOOP        '1509'

64	LOAD_FAST         'readline'
67	CALL_FUNCTION_0   None
70	STORE_FAST        'line'

73	LOAD_FAST         'lnum'
76	LOAD_CONST        1
79	BINARY_ADD        None
80	STORE_FAST        'lnum'

83	LOAD_CONST        0
86	LOAD_GLOBAL       'len'
89	LOAD_FAST         'line'
92	CALL_FUNCTION_1   None
95	ROT_TWO           None
96	STORE_FAST        'pos'
99	STORE_FAST        'max'

102	LOAD_FAST         'contstr'
105	JUMP_IF_FALSE     '347'

108	LOAD_FAST         'line'
111	JUMP_IF_TRUE      '132'

114	LOAD_GLOBAL       'TokenError'
117	LOAD_CONST        'EOF in multi-line string'
120	LOAD_FAST         'strstart'
123	BUILD_TUPLE_2     None
126	RAISE_VARARGS_2   None
129	JUMP_FORWARD      '132'
132_0	COME_FROM         '129'

132	LOAD_FAST         'endprog'
135	LOAD_ATTR         'match'
138	LOAD_FAST         'line'
141	CALL_FUNCTION_1   None
144	STORE_FAST        'endmatch'

147	LOAD_FAST         'endmatch'
150	JUMP_IF_FALSE     '230'

153	LOAD_FAST         'endmatch'
156	LOAD_ATTR         'end'
159	LOAD_CONST        0
162	CALL_FUNCTION_1   None
165	DUP_TOP           None
166	STORE_FAST        'pos'
169	STORE_FAST        'end'

172	LOAD_GLOBAL       'STRING'
175	LOAD_FAST         'contstr'
178	LOAD_FAST         'line'
181	LOAD_FAST         'end'
184	SLICE+2           None
185	BINARY_ADD        None
186	LOAD_FAST         'strstart'
189	LOAD_FAST         'lnum'
192	LOAD_FAST         'end'
195	BUILD_TUPLE_2     None
198	LOAD_FAST         'contline'
201	LOAD_FAST         'line'
204	BINARY_ADD        None
205	BUILD_TUPLE_5     None
208	YIELD_VALUE       None

209	LOAD_CONST        ('', 0)
212	UNPACK_SEQUENCE_2 None
215	STORE_FAST        'contstr'
218	STORE_FAST        'needcont'

221	LOAD_CONST        None
224	STORE_FAST        'contline'
227	JUMP_ABSOLUTE     '772'

230	LOAD_FAST         'needcont'
233	JUMP_IF_FALSE     '321'
236	LOAD_FAST         'line'
239	LOAD_CONST        -2
242	SLICE+1           None
243	LOAD_CONST        '\\\n'
246	COMPARE_OP        '!='
249	JUMP_IF_FALSE     '321'
252	LOAD_FAST         'line'
255	LOAD_CONST        -3
258	SLICE+1           None
259	LOAD_CONST        '\\\r\n'
262	COMPARE_OP        '!='
265_0	COME_FROM         '233'
265_1	COME_FROM         '249'
265	JUMP_IF_FALSE     '321'

268	LOAD_GLOBAL       'ERRORTOKEN'
271	LOAD_FAST         'contstr'
274	LOAD_FAST         'line'
277	BINARY_ADD        None
278	LOAD_FAST         'strstart'
281	LOAD_FAST         'lnum'
284	LOAD_GLOBAL       'len'
287	LOAD_FAST         'line'
290	CALL_FUNCTION_1   None
293	BUILD_TUPLE_2     None
296	LOAD_FAST         'contline'
299	BUILD_TUPLE_5     None
302	YIELD_VALUE       None

303	LOAD_CONST        ''
306	STORE_FAST        'contstr'

309	LOAD_CONST        None
312	STORE_FAST        'contline'

315	CONTINUE          '64'
318	JUMP_ABSOLUTE     '772'

321	LOAD_FAST         'contstr'
324	LOAD_FAST         'line'
327	BINARY_ADD        None
328	STORE_FAST        'contstr'

331	LOAD_FAST         'contline'
334	LOAD_FAST         'line'
337	BINARY_ADD        None
338	STORE_FAST        'contline'

341	CONTINUE          '64'
344	JUMP_FORWARD      '772'

347	LOAD_FAST         'parenlev'
350	LOAD_CONST        0
353	COMPARE_OP        '=='
356	JUMP_IF_FALSE     '736'
359	LOAD_FAST         'continued'
362	UNARY_NOT         None
363_0	COME_FROM         '356'
363	JUMP_IF_FALSE     '736'

366	LOAD_FAST         'line'
369	JUMP_IF_TRUE      '376'
372	BREAK_LOOP        None
373	JUMP_FORWARD      '376'
376_0	COME_FROM         '373'

376	LOAD_CONST        0
379	STORE_FAST        'column'

382	SETUP_LOOP        '503'
385	LOAD_FAST         'pos'
388	LOAD_FAST         'max'
391	COMPARE_OP        '<'
394	JUMP_IF_FALSE     '502'

397	LOAD_FAST         'line'
400	LOAD_FAST         'pos'
403	BINARY_SUBSCR     None
404	LOAD_CONST        ' '
407	COMPARE_OP        '=='
410	JUMP_IF_FALSE     '426'
413	LOAD_FAST         'column'
416	LOAD_CONST        1
419	BINARY_ADD        None
420	STORE_FAST        'column'
423	JUMP_FORWARD      '489'

426	LOAD_FAST         'line'
429	LOAD_FAST         'pos'
432	BINARY_SUBSCR     None
433	LOAD_CONST        '\t'
436	COMPARE_OP        '=='
439	JUMP_IF_FALSE     '463'
442	LOAD_FAST         'column'
445	LOAD_GLOBAL       'tabsize'
448	BINARY_DIVIDE     None
449	LOAD_CONST        1
452	BINARY_ADD        None
453	LOAD_GLOBAL       'tabsize'
456	BINARY_MULTIPLY   None
457	STORE_FAST        'column'
460	JUMP_FORWARD      '489'

463	LOAD_FAST         'line'
466	LOAD_FAST         'pos'
469	BINARY_SUBSCR     None
470	LOAD_CONST        '\x0c'
473	COMPARE_OP        '=='
476	JUMP_IF_FALSE     '488'
479	LOAD_CONST        0
482	STORE_FAST        'column'
485	JUMP_FORWARD      '489'

488	BREAK_LOOP        None
489_0	COME_FROM         '423'
489_1	COME_FROM         '460'
489_2	COME_FROM         '485'

489	LOAD_FAST         'pos'
492	LOAD_CONST        1
495	BINARY_ADD        None
496	STORE_FAST        'pos'
499	JUMP_BACK         '385'
502	POP_BLOCK         None
503_0	COME_FROM         '382'

503	LOAD_FAST         'pos'
506	LOAD_FAST         'max'
509	COMPARE_OP        '=='
512	JUMP_IF_FALSE     '519'
515	BREAK_LOOP        None
516	JUMP_FORWARD      '519'
519_0	COME_FROM         '516'

519	LOAD_FAST         'line'
522	LOAD_FAST         'pos'
525	BINARY_SUBSCR     None
526	LOAD_CONST        '#\r\n'
529	COMPARE_OP        'in'
532	JUMP_IF_FALSE     '602'

535	LOAD_GLOBAL       'NL'
538	LOAD_GLOBAL       'COMMENT'
541	BUILD_TUPLE_2     None
544	LOAD_FAST         'line'
547	LOAD_FAST         'pos'
550	BINARY_SUBSCR     None
551	LOAD_CONST        '#'
554	COMPARE_OP        '=='
557	BINARY_SUBSCR     None
558	LOAD_FAST         'line'
561	LOAD_FAST         'pos'
564	SLICE+1           None
565	LOAD_FAST         'lnum'
568	LOAD_FAST         'pos'
571	BUILD_TUPLE_2     None
574	LOAD_FAST         'lnum'
577	LOAD_GLOBAL       'len'
580	LOAD_FAST         'line'
583	CALL_FUNCTION_1   None
586	BUILD_TUPLE_2     None
589	LOAD_FAST         'line'
592	BUILD_TUPLE_5     None
595	YIELD_VALUE       None

596	CONTINUE          '64'
599	JUMP_FORWARD      '602'
602_0	COME_FROM         '599'

602	LOAD_FAST         'column'
605	LOAD_FAST         'indents'
608	LOAD_CONST        -1
611	BINARY_SUBSCR     None
612	COMPARE_OP        '>'
615	JUMP_IF_FALSE     '669'

618	LOAD_FAST         'indents'
621	LOAD_ATTR         'append'
624	LOAD_FAST         'column'
627	CALL_FUNCTION_1   None
630	POP_TOP           None

631	LOAD_GLOBAL       'INDENT'
634	LOAD_FAST         'line'
637	LOAD_FAST         'pos'
640	SLICE+2           None
641	LOAD_FAST         'lnum'
644	LOAD_CONST        0
647	BUILD_TUPLE_2     None
650	LOAD_FAST         'lnum'
653	LOAD_FAST         'pos'
656	BUILD_TUPLE_2     None
659	LOAD_FAST         'line'
662	BUILD_TUPLE_5     None
665	YIELD_VALUE       None
666	JUMP_FORWARD      '669'
669_0	COME_FROM         '666'

669	SETUP_LOOP        '772'
672	LOAD_FAST         'column'
675	LOAD_FAST         'indents'
678	LOAD_CONST        -1
681	BINARY_SUBSCR     None
682	COMPARE_OP        '<'
685	JUMP_IF_FALSE     '732'

688	LOAD_FAST         'indents'
691	LOAD_CONST        -1
694	SLICE+2           None
695	STORE_FAST        'indents'

698	LOAD_GLOBAL       'DEDENT'
701	LOAD_CONST        ''
704	LOAD_FAST         'lnum'
707	LOAD_FAST         'pos'
710	BUILD_TUPLE_2     None
713	LOAD_FAST         'lnum'
716	LOAD_FAST         'pos'
719	BUILD_TUPLE_2     None
722	LOAD_FAST         'line'
725	BUILD_TUPLE_5     None
728	YIELD_VALUE       None
729	JUMP_BACK         '672'
732	POP_BLOCK         None
733_0	COME_FROM         '669'
733	JUMP_FORWARD      '772'

736	LOAD_FAST         'line'
739	JUMP_IF_TRUE      '766'

742	LOAD_GLOBAL       'TokenError'
745	LOAD_CONST        'EOF in multi-line statement'
748	LOAD_FAST         'lnum'
751	LOAD_CONST        0
754	BUILD_TUPLE_2     None
757	BUILD_TUPLE_2     None
760	RAISE_VARARGS_2   None
763	JUMP_FORWARD      '766'
766_0	COME_FROM         '763'

766	LOAD_CONST        0
769	STORE_FAST        'continued'
772_0	COME_FROM         '344'
772_1	COME_FROM         '733'

772	SETUP_LOOP        '1505'
775	LOAD_FAST         'pos'
778	LOAD_FAST         'max'
781	COMPARE_OP        '<'
784	JUMP_IF_FALSE     '1504'

787	LOAD_GLOBAL       'pseudoprog'
790	LOAD_ATTR         'match'
793	LOAD_FAST         'line'
796	LOAD_FAST         'pos'
799	CALL_FUNCTION_2   None
802	STORE_FAST        'pseudomatch'

805	LOAD_FAST         'pseudomatch'
808	JUMP_IF_FALSE     '1452'

811	LOAD_FAST         'pseudomatch'
814	LOAD_ATTR         'span'
817	LOAD_CONST        1
820	CALL_FUNCTION_1   None
823	UNPACK_SEQUENCE_2 None
826	STORE_FAST        'start'
829	STORE_FAST        'end'

832	LOAD_FAST         'lnum'
835	LOAD_FAST         'start'
838	BUILD_TUPLE_2     None
841	LOAD_FAST         'lnum'
844	LOAD_FAST         'end'
847	BUILD_TUPLE_2     None
850	LOAD_FAST         'end'
853	ROT_THREE         None
854	ROT_TWO           None
855	STORE_FAST        'spos'
858	STORE_FAST        'epos'
861	STORE_FAST        'pos'

864	LOAD_FAST         'line'
867	LOAD_FAST         'start'
870	LOAD_FAST         'end'
873	SLICE+3           None
874	LOAD_FAST         'line'
877	LOAD_FAST         'start'
880	BINARY_SUBSCR     None
881	ROT_TWO           None
882	STORE_FAST        'token'
885	STORE_FAST        'initial'

888	LOAD_FAST         'initial'
891	LOAD_FAST         'numchars'
894	COMPARE_OP        'in'
897	JUMP_IF_TRUE      '924'
900	LOAD_FAST         'initial'
903	LOAD_CONST        '.'
906	COMPARE_OP        '=='
909	JUMP_IF_FALSE     '946'
912	LOAD_FAST         'token'
915	LOAD_CONST        '.'
918	COMPARE_OP        '!='
921_0	COME_FROM         '897'
921_1	COME_FROM         '909'
921	JUMP_IF_FALSE     '946'

924	LOAD_GLOBAL       'NUMBER'
927	LOAD_FAST         'token'
930	LOAD_FAST         'spos'
933	LOAD_FAST         'epos'
936	LOAD_FAST         'line'
939	BUILD_TUPLE_5     None
942	YIELD_VALUE       None
943	JUMP_ABSOLUTE     '1501'

946	LOAD_FAST         'initial'
949	LOAD_CONST        '\r\n'
952	COMPARE_OP        'in'
955	JUMP_IF_FALSE     '998'

958	LOAD_FAST         'parenlev'
961	LOAD_CONST        0
964	COMPARE_OP        '>'
967	JUMP_IF_FALSE     '976'
970	LOAD_GLOBAL       'NL'
973_0	COME_FROM         '967'
973	JUMP_IF_TRUE      '979'
976	LOAD_GLOBAL       'NEWLINE'
979	LOAD_FAST         'token'
982	LOAD_FAST         'spos'
985	LOAD_FAST         'epos'
988	LOAD_FAST         'line'
991	BUILD_TUPLE_5     None
994	YIELD_VALUE       None
995	JUMP_ABSOLUTE     '1501'

998	LOAD_FAST         'initial'
1001	LOAD_CONST        '#'
1004	COMPARE_OP        '=='
1007	JUMP_IF_FALSE     '1032'

1010	LOAD_GLOBAL       'COMMENT'
1013	LOAD_FAST         'token'
1016	LOAD_FAST         'spos'
1019	LOAD_FAST         'epos'
1022	LOAD_FAST         'line'
1025	BUILD_TUPLE_5     None
1028	YIELD_VALUE       None
1029	JUMP_ABSOLUTE     '1501'

1032	LOAD_FAST         'token'
1035	LOAD_GLOBAL       'triple_quoted'
1038	COMPARE_OP        'in'
1041	JUMP_IF_FALSE     '1166'

1044	LOAD_GLOBAL       'endprogs'
1047	LOAD_FAST         'token'
1050	BINARY_SUBSCR     None
1051	STORE_FAST        'endprog'

1054	LOAD_FAST         'endprog'
1057	LOAD_ATTR         'match'
1060	LOAD_FAST         'line'
1063	LOAD_FAST         'pos'
1066	CALL_FUNCTION_2   None
1069	STORE_FAST        'endmatch'

1072	LOAD_FAST         'endmatch'
1075	JUMP_IF_FALSE     '1134'

1078	LOAD_FAST         'endmatch'
1081	LOAD_ATTR         'end'
1084	LOAD_CONST        0
1087	CALL_FUNCTION_1   None
1090	STORE_FAST        'pos'

1093	LOAD_FAST         'line'
1096	LOAD_FAST         'start'
1099	LOAD_FAST         'pos'
1102	SLICE+3           None
1103	STORE_FAST        'token'

1106	LOAD_GLOBAL       'STRING'
1109	LOAD_FAST         'token'
1112	LOAD_FAST         'spos'
1115	LOAD_FAST         'lnum'
1118	LOAD_FAST         'pos'
1121	BUILD_TUPLE_2     None
1124	LOAD_FAST         'line'
1127	BUILD_TUPLE_5     None
1130	YIELD_VALUE       None
1131	JUMP_ABSOLUTE     '1449'

1134	LOAD_FAST         'lnum'
1137	LOAD_FAST         'start'
1140	BUILD_TUPLE_2     None
1143	STORE_FAST        'strstart'

1146	LOAD_FAST         'line'
1149	LOAD_FAST         'start'
1152	SLICE+1           None
1153	STORE_FAST        'contstr'

1156	LOAD_FAST         'line'
1159	STORE_FAST        'contline'

1162	BREAK_LOOP        None
1163	JUMP_ABSOLUTE     '1501'

1166	LOAD_FAST         'initial'
1169	LOAD_GLOBAL       'single_quoted'
1172	COMPARE_OP        'in'
1175	JUMP_IF_TRUE      '1210'
1178	LOAD_FAST         'token'
1181	LOAD_CONST        2
1184	SLICE+2           None
1185	LOAD_GLOBAL       'single_quoted'
1188	COMPARE_OP        'in'
1191	JUMP_IF_TRUE      '1210'
1194	LOAD_FAST         'token'
1197	LOAD_CONST        3
1200	SLICE+2           None
1201	LOAD_GLOBAL       'single_quoted'
1204	COMPARE_OP        'in'
1207_0	COME_FROM         '1175'
1207_1	COME_FROM         '1191'
1207	JUMP_IF_FALSE     '1325'

1210	LOAD_FAST         'token'
1213	LOAD_CONST        -1
1216	BINARY_SUBSCR     None
1217	LOAD_CONST        '\n'
1220	COMPARE_OP        '=='
1223	JUMP_IF_FALSE     '1303'

1226	LOAD_FAST         'lnum'
1229	LOAD_FAST         'start'
1232	BUILD_TUPLE_2     None
1235	STORE_FAST        'strstart'

1238	LOAD_GLOBAL       'endprogs'
1241	LOAD_FAST         'initial'
1244	BINARY_SUBSCR     None
1245	JUMP_IF_TRUE      '1273'
1248	LOAD_GLOBAL       'endprogs'
1251	LOAD_FAST         'token'
1254	LOAD_CONST        1
1257	BINARY_SUBSCR     None
1258	BINARY_SUBSCR     None
1259	JUMP_IF_TRUE      '1273'
1262	LOAD_GLOBAL       'endprogs'
1265	LOAD_FAST         'token'
1268	LOAD_CONST        2
1271	BINARY_SUBSCR     None
1272	BINARY_SUBSCR     None
1273	STORE_FAST        'endprog'

1276	LOAD_FAST         'line'
1279	LOAD_FAST         'start'
1282	SLICE+1           None
1283	LOAD_CONST        1
1286	ROT_TWO           None
1287	STORE_FAST        'contstr'
1290	STORE_FAST        'needcont'

1293	LOAD_FAST         'line'
1296	STORE_FAST        'contline'

1299	BREAK_LOOP        None
1300	JUMP_ABSOLUTE     '1449'

1303	LOAD_GLOBAL       'STRING'
1306	LOAD_FAST         'token'
1309	LOAD_FAST         'spos'
1312	LOAD_FAST         'epos'
1315	LOAD_FAST         'line'
1318	BUILD_TUPLE_5     None
1321	YIELD_VALUE       None
1322	JUMP_ABSOLUTE     '1501'

1325	LOAD_FAST         'initial'
1328	LOAD_FAST         'namechars'
1331	COMPARE_OP        'in'
1334	JUMP_IF_FALSE     '1359'

1337	LOAD_GLOBAL       'NAME'
1340	LOAD_FAST         'token'
1343	LOAD_FAST         'spos'
1346	LOAD_FAST         'epos'
1349	LOAD_FAST         'line'
1352	BUILD_TUPLE_5     None
1355	YIELD_VALUE       None
1356	JUMP_ABSOLUTE     '1501'

1359	LOAD_FAST         'initial'
1362	LOAD_CONST        '\\'
1365	COMPARE_OP        '=='
1368	JUMP_IF_FALSE     '1380'

1371	LOAD_CONST        1
1374	STORE_FAST        'continued'
1377	JUMP_ABSOLUTE     '1501'

1380	LOAD_FAST         'initial'
1383	LOAD_CONST        '([{'
1386	COMPARE_OP        'in'
1389	JUMP_IF_FALSE     '1405'
1392	LOAD_FAST         'parenlev'
1395	LOAD_CONST        1
1398	BINARY_ADD        None
1399	STORE_FAST        'parenlev'
1402	JUMP_FORWARD      '1430'

1405	LOAD_FAST         'initial'
1408	LOAD_CONST        ')]}'
1411	COMPARE_OP        'in'
1414	JUMP_IF_FALSE     '1430'
1417	LOAD_FAST         'parenlev'
1420	LOAD_CONST        1
1423	BINARY_SUBTRACT   None
1424	STORE_FAST        'parenlev'
1427	JUMP_FORWARD      '1430'
1430_0	COME_FROM         '1402'
1430_1	COME_FROM         '1427'

1430	LOAD_GLOBAL       'OP'
1433	LOAD_FAST         'token'
1436	LOAD_FAST         'spos'
1439	LOAD_FAST         'epos'
1442	LOAD_FAST         'line'
1445	BUILD_TUPLE_5     None
1448	YIELD_VALUE       None
1449	CONTINUE          '775'

1452	LOAD_GLOBAL       'ERRORTOKEN'
1455	LOAD_FAST         'line'
1458	LOAD_FAST         'pos'
1461	BINARY_SUBSCR     None
1462	LOAD_FAST         'lnum'
1465	LOAD_FAST         'pos'
1468	BUILD_TUPLE_2     None
1471	LOAD_FAST         'lnum'
1474	LOAD_FAST         'pos'
1477	LOAD_CONST        1
1480	BINARY_ADD        None
1481	BUILD_TUPLE_2     None
1484	LOAD_FAST         'line'
1487	BUILD_TUPLE_5     None
1490	YIELD_VALUE       None

1491	LOAD_FAST         'pos'
1494	LO
# Can't uncompyle C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\tokenize.pyc
Traceback (most recent call last):
  File "C:\python27\lib\uncompyle2\__init__.py", line 206, in main
    uncompyle_file(infile, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 143, in uncompyle_file
    uncompyle(version, co, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 132, in uncompyle
    raise walk.ERROR
ParserError: --- This code section failed: ---

0	LOAD_CONST        0
3	DUP_TOP           None
4	STORE_FAST        'lnum'
7	DUP_TOP           None
8	STORE_FAST        'parenlev'
11	STORE_FAST        'continued'

14	LOAD_GLOBAL       'string'
17	LOAD_ATTR         'ascii_letters'
20	LOAD_CONST        '_'
23	BINARY_ADD        None
24	LOAD_CONST        '0123456789'
27	ROT_TWO           None
28	STORE_FAST        'namechars'
31	STORE_FAST        'numchars'

34	LOAD_CONST        ('', 0)
37	UNPACK_SEQUENCE_2 None
40	STORE_FAST        'contstr'
43	STORE_FAST        'needcont'

46	LOAD_CONST        None
49	STORE_FAST        'contline'

52	LOAD_CONST        0
55	BUILD_LIST_1      None
58	STORE_FAST        'indents'

61	SETUP_LOOP        '1509'

64	LOAD_FAST         'readline'
67	CALL_FUNCTION_0   None
70	STORE_FAST        'line'

73	LOAD_FAST         'lnum'
76	LOAD_CONST        1
79	BINARY_ADD        None
80	STORE_FAST        'lnum'

83	LOAD_CONST        0
86	LOAD_GLOBAL       'len'
89	LOAD_FAST         'line'
92	CALL_FUNCTION_1   None
95	ROT_TWO           None
96	STORE_FAST        'pos'
99	STORE_FAST        'max'

102	LOAD_FAST         'contstr'
105	JUMP_IF_FALSE     '347'

108	LOAD_FAST         'line'
111	JUMP_IF_TRUE      '132'

114	LOAD_GLOBAL       'TokenError'
117	LOAD_CONST        'EOF in multi-line string'
120	LOAD_FAST         'strstart'
123	BUILD_TUPLE_2     None
126	RAISE_VARARGS_2   None
129	JUMP_FORWARD      '132'
132_0	COME_FROM         '129'

132	LOAD_FAST         'endprog'
135	LOAD_ATTR         'match'
138	LOAD_FAST         'line'
141	CALL_FUNCTION_1   None
144	STORE_FAST        'endmatch'

147	LOAD_FAST         'endmatch'
150	JUMP_IF_FALSE     '230'

153	LOAD_FAST         'endmatch'
156	LOAD_ATTR         'end'
159	LOAD_CONST        0
162	CALL_FUNCTION_1   None
165	DUP_TOP           None
166	STORE_FAST        'pos'
169	STORE_FAST        'end'

172	LOAD_GLOBAL       'STRING'
175	LOAD_FAST         'contstr'
178	LOAD_FAST         'line'
181	LOAD_FAST         'end'
184	SLICE+2           None
185	BINARY_ADD        None
186	LOAD_FAST         'strstart'
189	LOAD_FAST         'lnum'
192	LOAD_FAST         'end'
195	BUILD_TUPLE_2     None
198	LOAD_FAST         'contline'
201	LOAD_FAST         'line'
204	BINARY_ADD        None
205	BUILD_TUPLE_5     None
208	YIELD_VALUE       None

209	LOAD_CONST        ('', 0)
212	UNPACK_SEQUENCE_2 None
215	STORE_FAST        'contstr'
218	STORE_FAST        'needcont'

221	LOAD_CONST        None
224	STORE_FAST        'contline'
227	JUMP_ABSOLUTE     '772'

230	LOAD_FAST         'needcont'
233	JUMP_IF_FALSE     '321'
236	LOAD_FAST         'line'
239	LOAD_CONST        -2
242	SLICE+1           None
243	LOAD_CONST        '\\\n'
246	COMPARE_OP        '!='
249	JUMP_IF_FALSE     '321'
252	LOAD_FAST         'line'
255	LOAD_CONST        -3
258	SLICE+1           None
259	LOAD_CONST        '\\\r\n'
262	COMPARE_OP        '!='
265_0	COME_FROM         '233'
265_1	COME_FROM         '249'
265	JUMP_IF_FALSE     '321'

268	LOAD_GLOBAL       'ERRORTOKEN'
271	LOAD_FAST         'contstr'
274	LOAD_FAST         'line'
277	BINARY_ADD        None
278	LOAD_FAST         'strstart'
281	LOAD_FAST         'lnum'
284	LOAD_GLOBAL       'len'
287	LOAD_FAST         'line'
290	CALL_FUNCTION_1   None
293	BUILD_TUPLE_2     None
296	LOAD_FAST         'contline'
299	BUILD_TUPLE_5     None
302	YIELD_VALUE       None

303	LOAD_CONST        ''
306	STORE_FAST        'contstr'

309	LOAD_CONST        None
312	STORE_FAST        'contline'

315	CONTINUE          '64'
318	JUMP_ABSOLUTE     '772'

321	LOAD_FAST         'contstr'
324	LOAD_FAST         'line'
327	BINARY_ADD        None
328	STORE_FAST        'contstr'

331	LOAD_FAST         'contline'
334	LOAD_FAST         'line'
337	BINARY_ADD        None
338	STORE_FAST        'contline'

341	CONTINUE          '64'
344	JUMP_FORWARD      '772'

347	LOAD_FAST         'parenlev'
350	LOAD_CONST        0
353	COMPARE_OP        '=='
356	JUMP_IF_FALSE     '736'
359	LOAD_FAST         'continued'
362	UNARY_NOT         None
363_0	COME_FROM         '356'
363	JUMP_IF_FALSE     '736'

366	LOAD_FAST         'line'
369	JUMP_IF_TRUE      '376'
372	BREAK_LOOP        None
373	JUMP_FORWARD      '376'
376_0	COME_FROM         '373'

376	LOAD_CONST        0
379	STORE_FAST        'column'

382	SETUP_LOOP        '503'
385	LOAD_FAST         'pos'
388	LOAD_FAST         'max'
391	COMPARE_OP        '<'
394	JUMP_IF_FALSE     '502'

397	LOAD_FAST         'line'
400	LOAD_FAST         'pos'
403	BINARY_SUBSCR     None
404	LOAD_CONST        ' '
407	COMPARE_OP        '=='
410	JUMP_IF_FALSE     '426'
413	LOAD_FAST         'column'
416	LOAD_CONST        1
419	BINARY_ADD        None
420	STORE_FAST        'column'
423	JUMP_FORWARD      '489'

426	LOAD_FAST         'line'
429	LOAD_FAST         'pos'
432	BINARY_SUBSCR     None
433	LOAD_CONST        '\t'
436	COMPARE_OP        '=='
439	JUMP_IF_FALSE     '463'
442	LOAD_FAST         'column'
445	LOAD_GLOBAL       'tabsize'
448	BINARY_DIVIDE     None
449	LOAD_CONST        1
452	BINARY_ADD        None
453	LOAD_GLOBAL       'tabsize'
456	BINARY_MULTIPLY   None
457	STORE_FAST        'column'
460	JUMP_FORWARD      '489'

463	LOAD_FAST         'line'
466	LOAD_FAST         'pos'
469	BINARY_SUBSCR     None
470	LOAD_CONST        '\x0c'
473	COMPARE_OP        '=='
476	JUMP_IF_FALSE     '488'
479	LOAD_CONST        0
482	STORE_FAST        'column'
485	JUMP_FORWARD      '489'

488	BREAK_LOOP        None
489_0	COME_FROM         '423'
489_1	COME_FROM         '460'
489_2	COME_FROM         '485'

489	LOAD_FAST         'pos'
492	LOAD_CONST        1
495	BINARY_ADD        None
496	STORE_FAST        'pos'
499	JUMP_BACK         '385'
502	POP_BLOCK         None
503_0	COME_FROM         '382'

503	LOAD_FAST         'pos'
506	LOAD_FAST         'max'
509	COMPARE_OP        '=='
512	JUMP_IF_FALSE     '519'
515	BREAK_LOOP        None
516	JUMP_FORWARD      '519'
519_0	COME_FROM         '516'

519	LOAD_FAST         'line'
522	LOAD_FAST         'pos'
525	BINARY_SUBSCR     None
526	LOAD_CONST        '#\r\n'
529	COMPARE_OP        'in'
532	JUMP_IF_FALSE     '602'

535	LOAD_GLOBAL       'NL'
538	LOAD_GLOBAL       'COMMENT'
541	BUILD_TUPLE_2     None
544	LOAD_FAST         'line'
547	LOAD_FAST         'pos'
550	BINARY_SUBSCR     None
551	LOAD_CONST        '#'
554	COMPARE_OP        '=='
557	BINARY_SUBSCR     None
558	LOAD_FAST         'line'
561	LOAD_FAST         'pos'
564	SLICE+1           None
565	LOAD_FAST         'lnum'
568	LOAD_FAST         'pos'
571	BUILD_TUPLE_2     None
574	LOAD_FAST         'lnum'
577	LOAD_GLOBAL       'len'
580	LOAD_FAST         'line'
583	CALL_FUNCTION_1   None
586	BUILD_TUPLE_2     None
589	LOAD_FAST         'line'
592	BUILD_TUPLE_5     None
595	YIELD_VALUE       None

596	CONTINUE          '64'
599	JUMP_FORWARD      '602'
602_0	COME_FROM         '599'

602	LOAD_FAST         'column'
605	LOAD_FAST         'indents'
608	LOAD_CONST        -1
611	BINARY_SUBSCR     None
612	COMPARE_OP        '>'
615	JUMP_IF_FALSE     '669'

618	LOAD_FAST         'indents'
621	LOAD_ATTR         'append'
624	LOAD_FAST         'column'
627	CALL_FUNCTION_1   None
630	POP_TOP           None

631	LOAD_GLOBAL       'INDENT'
634	LOAD_FAST         'line'
637	LOAD_FAST         'pos'
640	SLICE+2           None
641	LOAD_FAST         'lnum'
644	LOAD_CONST        0
647	BUILD_TUPLE_2     None
650	LOAD_FAST         'lnum'
653	LOAD_FAST         'pos'
656	BUILD_TUPLE_2     None
659	LOAD_FAST         'line'
662	BUILD_TUPLE_5     None
665	YIELD_VALUE       None
666	JUMP_FORWARD      '669'
669_0	COME_FROM         '666'

669	SETUP_LOOP        '772'
672	LOAD_FAST         'column'
675	LOAD_FAST         'indents'
678	LOAD_CONST        -1
681	BINARY_SUBSCR     None
682	COMPARE_OP        '<'
685	JUMP_IF_FALSE     '732'

688	LOAD_FAST         'indents'
691	LOAD_CONST        -1
694	SLICE+2           None
695	STORE_FAST        'indents'

698	LOAD_GLOBAL       'DEDENT'
701	LOAD_CONST        ''
704	LOAD_FAST         'lnum'
707	LOAD_FAST         'pos'
710	BUILD_TUPLE_2     None
713	LOAD_FAST         'lnum'
716	LOAD_FAST         'pos'
719	BUILD_TUPLE_2     None
722	LOAD_FAST         'line'
725	BUILD_TUPLE_5     None
728	YIELD_VALUE       None
729	JUMP_BACK         '672'
732	POP_BLOCK         None
733_0	COME_FROM         '669'
733	JUMP_FORWARD      '772'

736	LOAD_FAST         'line'
739	JUMP_IF_TRUE      '766'

742	LOAD_GLOBAL       'TokenError'
745	LOAD_CONST        'EOF in multi-line statement'
748	LOAD_FAST         'lnum'
751	LOAD_CONST        0
754	BUILD_TUPLE_2     None
757	BUILD_TUPLE_2     None
760	RAISE_VARARGS_2   None
763	JUMP_FORWARD      '766'
766_0	COME_FROM         '763'

766	LOAD_CONST        0
769	STORE_FAST        'continued'
772_0	COME_FROM         '344'
772_1	COME_FROM         '733'

772	SETUP_LOOP        '1505'
775	LOAD_FAST         'pos'
778	LOAD_FAST         'max'
781	COMPARE_OP        '<'
784	JUMP_IF_FALSE     '1504'

787	LOAD_GLOBAL       'pseudoprog'
790	LOAD_ATTR         'match'
793	LOAD_FAST         'line'
796	LOAD_FAST         'pos'
799	CALL_FUNCTION_2   None
802	STORE_FAST        'pseudomatch'

805	LOAD_FAST         'pseudomatch'
808	JUMP_IF_FALSE     '1452'

811	LOAD_FAST         'pseudomatch'
814	LOAD_ATTR         'span'
817	LOAD_CONST        1
820	CALL_FUNCTION_1   None
823	UNPACK_SEQUENCE_2 None
826	STORE_FAST        'start'
829	STORE_FAST        'end'

832	LOAD_FAST         'lnum'
835	LOAD_FAST         'start'
838	BUILD_TUPLE_2     None
841	LOAD_FAST         'lnum'
844	LOAD_FAST         'end'
847	BUILD_TUPLE_2     None
850	LOAD_FAST         'end'
853	ROT_THREE         None
854	ROT_TWO           None
855	STORE_FAST        'spos'
858	STORE_FAST        'epos'
861	STORE_FAST        'pos'

864	LOAD_FAST         'line'
867	LOAD_FAST         'start'
870	LOAD_FAST         'end'
873	SLICE+3           None
874	LOAD_FAST         'line'
877	LOAD_FAST         'start'
880	BINARY_SUBSCR     None
881	ROT_TWO           None
882	STORE_FAST        'token'
885	STORE_FAST        'initial'

888	LOAD_FAST         'initial'
891	LOAD_FAST         'numchars'
894	COMPARE_OP        'in'
897	JUMP_IF_TRUE      '924'
900	LOAD_FAST         'initial'
903	LOAD_CONST        '.'
906	COMPARE_OP        '=='
909	JUMP_IF_FALSE     '946'
912	LOAD_FAST         'token'
915	LOAD_CONST        '.'
918	COMPARE_OP        '!='
921_0	COME_FROM         '897'
921_1	COME_FROM         '909'
921	JUMP_IF_FALSE     '946'

924	LOAD_GLOBAL       'NUMBER'
927	LOAD_FAST         'token'
930	LOAD_FAST         'spos'
933	LOAD_FAST         'epos'
936	LOAD_FAST         'line'
939	BUILD_TUPLE_5     None
942	YIELD_VALUE       None
943	JUMP_ABSOLUTE     '1501'

946	LOAD_FAST         'initial'
949	LOAD_CONST        '\r\n'
952	COMPARE_OP        'in'
955	JUMP_IF_FALSE     '998'

958	LOAD_FAST         'parenlev'
961	LOAD_CONST        0
964	COMPARE_OP        '>'
967	JUMP_IF_FALSE     '976'
970	LOAD_GLOBAL       'NL'
973_0	COME_FROM         '967'
973	JUMP_IF_TRUE      '979'
976	LOAD_GLOBAL       'NEWLINE'
979	LOAD_FAST         'token'
982	LOAD_FAST         'spos'
985	LOAD_FAST         'epos'
988	LOAD_FAST         'line'
991	BUILD_TUPLE_5     None
994	YIELD_VALUE       None
995	JUMP_ABSOLUTE     '1501'

998	LOAD_FAST         'initial'
1001	LOAD_CONST        '#'
1004	COMPARE_OP        '=='
1007	JUMP_IF_FALSE     '1032'

1010	LOAD_GLOBAL       'COMMENT'
1013	LOAD_FAST         'token'
1016	LOAD_FAST         'spos'
1019	LOAD_FAST         'epos'
1022	LOAD_FAST         'line'
1025	BUILD_TUPLE_5     None
1028	YIELD_VALUE       None
1029	JUMP_ABSOLUTE     '1501'

1032	LOAD_FAST         'token'
1035	LOAD_GLOBAL       'triple_quoted'
1038	COMPARE_OP        'in'
1041	JUMP_IF_FALSE     '1166'

1044	LOAD_GLOBAL       'endprogs'
1047	LOAD_FAST         'token'
1050	BINARY_SUBSCR     None
1051	STORE_FAST        'endprog'

1054	LOAD_FAST         'endprog'
1057	LOAD_ATTR         'match'
1060	LOAD_FAST         'line'
1063	LOAD_FAST         'pos'
1066	CALL_FUNCTION_2   None
1069	STORE_FAST        'endmatch'

1072	LOAD_FAST         'endmatch'
1075	JUMP_IF_FALSE     '1134'

1078	LOAD_FAST         'endmatch'
1081	LOAD_ATTR         'end'
1084	LOAD_CONST        0
1087	CALL_FUNCTION_1   None
1090	STORE_FAST        'pos'

1093	LOAD_FAST         'line'
1096	LOAD_FAST         'start'
1099	LOAD_FAST         'pos'
1102	SLICE+3           None
1103	STORE_FAST        'token'

1106	LOAD_GLOBAL       'STRING'
1109	LOAD_FAST         'token'
1112	LOAD_FAST         'spos'
1115	LOAD_FAST         'lnum'
1118	LOAD_FAST         'pos'
1121	BUILD_TUPLE_2     None
1124	LOAD_FAST         'line'
1127	BUILD_TUPLE_5     None
1130	YIELD_VALUE       None
1131	JUMP_ABSOLUTE     '1449'

1134	LOAD_FAST         'lnum'
1137	LOAD_FAST         'start'
1140	BUILD_TUPLE_2     None
1143	STORE_FAST        'strstart'

1146	LOAD_FAST         'line'
1149	LOAD_FAST         'start'
1152	SLICE+1           None
1153	STORE_FAST        'contstr'

1156	LOAD_FAST         'line'
1159	STORE_FAST        'contline'

1162	BREAK_LOOP        None
1163	JUMP_ABSOLUTE     '1501'

1166	LOAD_FAST         'initial'
1169	LOAD_GLOBAL       'single_quoted'
1172	COMPARE_OP        'in'
1175	JUMP_IF_TRUE      '1210'
1178	LOAD_FAST         'token'
1181	LOAD_CONST        2
1184	SLICE+2           None
1185	LOAD_GLOBAL       'single_quoted'
1188	COMPARE_OP        'in'
1191	JUMP_IF_TRUE      '1210'
1194	LOAD_FAST         'token'
1197	LOAD_CONST        3
1200	SLICE+2           None
1201	LOAD_GLOBAL       'single_quoted'
1204	COMPARE_OP        'in'
1207_0	COME_FROM         '1175'
1207_1	COME_FROM         '1191'
1207	JUMP_IF_FALSE     '1325'

1210	LOAD_FAST         'token'
1213	LOAD_CONST        -1
1216	BINARY_SUBSCR     None
1217	LOAD_CONST        '\n'
1220	COMPARE_OP        '=='
1223	JUMP_IF_FALSE     '1303'

1226	LOAD_FAST         'lnum'
1229	LOAD_FAST         'start'
1232	BUILD_TUPLE_2     None
1235	STORE_FAST        'strstart'

1238	LOAD_GLOBAL       'endprogs'
1241	LOAD_FAST         'initial'
1244	BINARY_SUBSCR     None
1245	JUMP_IF_TRUE      '1273'
1248	LOAD_GLOBAL       'endprogs'
1251	LOAD_FAST         'token'
1254	LOAD_CONST        1
1257	BINARY_SUBSCR     None
1258	BINARY_SUBSCR     None
1259	JUMP_IF_TRUE      '1273'
1262	LOAD_GLOBAL       'endprogs'
1265	LOAD_FAST         'token'
1268	LOAD_CONST        2
1271	BINARY_SUBSCR     None
1272	BINARY_SUBSCR     None
1273	STORE_FAST        'endprog'

1276	LOAD_FAST         'line'
1279	LOAD_FAST         'start'
1282	SLICE+1           None
1283	LOAD_CONST        1
1286	ROT_TWO           None
1287	STORE_FAST        'contstr'
1290	STORE_FAST        'needcont'

1293	LOAD_FAST         'line'
1296	STORE_FAST        'contline'

1299	BREAK_LOOP        None
1300	JUMP_ABSOLUTE     '1449'

1303	LOAD_GLOBAL       'STRING'
1306	LOAD_FAST         'token'
1309	LOAD_FAST         'spos'
1312	LOAD_FAST         'epos'
1315	LOAD_FAST         'line'
1318	BUILD_TUPLE_5     None
1321	YIELD_VALUE       None
1322	JUMP_ABSOLUTE     '1501'

1325	LOAD_FAST         'initial'
1328	LOAD_FAST         'namechars'
1331	COMPARE_OP        'in'
1334	JUMP_IF_FALSE     '1359'

1337	LOAD_GLOBAL       'NAME'
1340	LOAD_FAST         'token'
1343	LOAD_FAST         'spos'
1346	LOAD_FAST         'epos'
1349	LOAD_FAST         'line'
1352	BUILD_TUPLE_5     None
1355	YIELD_VALUE       None
1356	JUMP_ABSOLUTE     '1501'

1359	LOAD_FAST         'initial'
1362	LOAD_CONST        '\\'
1365	COMPARE_OP        '=='
1368	JUMP_IF_FALSE     '1380'

1371	LOAD_CONST        1
1374	STORE_FAST        'continued'
1377	JUMP_ABSOLUTE     '1501'

1380	LOAD_FAST         'initial'
1383	LOAD_CONST        '([{'
1386	COMPARE_OP        'in'
1389	JUMP_IF_FALSE     '1405'
1392	LOAD_FAST         'parenlev'
1395	LOAD_CONST        1
1398	BINARY_ADD        None
1399	STORE_FAST        'parenlev'
1402	JUMP_FORWARD      '1430'

1405	LOAD_FAST         'initial'
1408	LOAD_CONST        ')]}'
1411	COMPARE_OP        'in'
1414	JUMP_IF_FALSE     '1430'
1417	LOAD_FAST         'parenlev'
1420	LOAD_CONST AD_CONST        1
1497	BINARY_ADD        None
1498	STORE_FAST        'pos'
1501	JUMP_BACK         '775'
1504	POP_BLOCK         None
1505_0	COME_FROM         '772'
1505	JUMP_BACK         '64'
1508	POP_BLOCK         None
1509_0	COME_FROM         '61'

1509	SETUP_LOOP        '1561'
1512	LOAD_FAST         'indents'
1515	LOAD_CONST        1
1518	SLICE+1           None
1519	GET_ITER          None
1520	FOR_ITER          '1560'
1523	STORE_FAST        'indent'

1526	LOAD_GLOBAL       'DEDENT'
1529	LOAD_CONST        ''
1532	LOAD_FAST         'lnum'
1535	LOAD_CONST        0
1538	BUILD_TUPLE_2     None
1541	LOAD_FAST         'lnum'
1544	LOAD_CONST        0
1547	BUILD_TUPLE_2     None
1550	LOAD_CONST        ''
1553	BUILD_TUPLE_5     None
1556	YIELD_VALUE       None
1557	JUMP_BACK         '1520'
1560	POP_BLOCK         None
1561_0	COME_FROM         '1509'

1561	LOAD_GLOBAL       'ENDMARKER'
1564	LOAD_CONST        ''
1567	LOAD_FAST         'lnum'
1570	LOAD_CONST        0
1573	BUILD_TUPLE_2     None
1576	LOAD_FAST         'lnum'
1579	LOAD_CONST        0
1582	BUILD_TUPLE_2     None
1585	LOAD_CONST        ''
1588	BUILD_TUPLE_5     None
1591	YIELD_VALUE       None
1592	LOAD_CONST        None
1595	RETURN_VALUE      None

Syntax error at or near `UNPACK_SEQUENCE_2' token at offset 212


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        tokenize(open(sys.argv[1]).readline)
    else:
        tokenize(sys.stdin.readline)# decompiled 0 files: 0 okay, 1 failed, 0 verify failed
# 2013.08.22 22:13:35 Pacific Daylight Time
       1
1423	BINARY_SUBTRACT   None
1424	STORE_FAST        'parenlev'
1427	JUMP_FORWARD      '1430'
1430_0	COME_FROM         '1402'
1430_1	COME_FROM         '1427'

1430	LOAD_GLOBAL       'OP'
1433	LOAD_FAST         'token'
1436	LOAD_FAST         'spos'
1439	LOAD_FAST         'epos'
1442	LOAD_FAST         'line'
1445	BUILD_TUPLE_5     None
1448	YIELD_VALUE       None
1449	CONTINUE          '775'

1452	LOAD_GLOBAL       'ERRORTOKEN'
1455	LOAD_FAST         'line'
1458	LOAD_FAST         'pos'
1461	BINARY_SUBSCR     None
1462	LOAD_FAST         'lnum'
1465	LOAD_FAST         'pos'
1468	BUILD_TUPLE_2     None
1471	LOAD_FAST         'lnum'
1474	LOAD_FAST         'pos'
1477	LOAD_CONST        1
1480	BINARY_ADD        None
1481	BUILD_TUPLE_2     None
1484	LOAD_FAST         'line'
1487	BUILD_TUPLE_5     None
1490	YIELD_VALUE       None

1491	LOAD_FAST         'pos'
1494	LOAD_CONST        1
1497	BINARY_ADD        None
1498	STORE_FAST        'pos'
1501	JUMP_BACK         '775'
1504	POP_BLOCK         None
1505_0	COME_FROM         '772'
1505	JUMP_BACK         '64'
1508	POP_BLOCK         None
1509_0	COME_FROM         '61'

1509	SETUP_LOOP        '1561'
1512	LOAD_FAST         'indents'
1515	LOAD_CONST        1
1518	SLICE+1           None
1519	GET_ITER          None
1520	FOR_ITER          '1560'
1523	STORE_FAST        'indent'

1526	LOAD_GLOBAL       'DEDENT'
1529	LOAD_CONST        ''
1532	LOAD_FAST         'lnum'
1535	LOAD_CONST        0
1538	BUILD_TUPLE_2     None
1541	LOAD_FAST         'lnum'
1544	LOAD_CONST        0
1547	BUILD_TUPLE_2     None
1550	LOAD_CONST        ''
1553	BUILD_TUPLE_5     None
1556	YIELD_VALUE       None
1557	JUMP_BACK         '1520'
1560	POP_BLOCK         None
1561_0	COME_FROM         '1509'

1561	LOAD_GLOBAL       'ENDMARKER'
1564	LOAD_CONST        ''
1567	LOAD_FAST         'lnum'
1570	LOAD_CONST        0
1573	BUILD_TUPLE_2     None
1576	LOAD_FAST         'lnum'
1579	LOAD_CONST        0
1582	BUILD_TUPLE_2     None
1585	LOAD_CONST        ''
1588	BUILD_TUPLE_5     None
1591	YIELD_VALUE       None
1592	LOAD_CONST        None
1595	RETURN_VALUE      None

Syntax error at or near `UNPACK_SEQUENCE_2' token at offset 212

