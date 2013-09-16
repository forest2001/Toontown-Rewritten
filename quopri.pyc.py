# 2013.08.22 22:13:23 Pacific Daylight Time
# Embedded file name: quopri
__all__ = ['encode',
 'decode',
 'encodestring',
 'decodestring']
ESCAPE = '='
MAXLINESIZE = 76
HEX = '0123456789ABCDEF'
EMPTYSTRING = ''
try:
    from binascii import a2b_qp, b2a_qp
except ImportError:
    a2b_qp = None
    b2a_qp = None

def needsquoting(c, quotetabs, header):
    if c in ' \t':
        return quotetabs
    if c == '_':
        return header
    return c == ESCAPE or not ' ' <= c <= '~'


def quote(c):
    i = ord(c)
    return ESCAPE + HEX[i // 16] + HEX[i % 16]


def encode--- This code section failed: ---

0	LOAD_GLOBAL       'b2a_qp'
3	LOAD_CONST        None
6	COMPARE_OP        'is not'
9	JUMP_IF_FALSE     '68'

12	LOAD_FAST         'input'
15	LOAD_ATTR         'read'
18	CALL_FUNCTION_0   None
21	STORE_FAST        'data'

24	LOAD_GLOBAL       'b2a_qp'
27	LOAD_FAST         'data'
30	LOAD_CONST        'quotetabs'
33	LOAD_FAST         'quotetabs'
36	LOAD_CONST        'header'
39	LOAD_FAST         'header'
42	CALL_FUNCTION_513 None
45	STORE_FAST        'odata'

48	LOAD_FAST         'output'
51	LOAD_ATTR         'write'
54	LOAD_FAST         'odata'
57	CALL_FUNCTION_1   None
60	POP_TOP           None

61	LOAD_CONST        None
64	RETURN_VALUE      None
65	JUMP_FORWARD      '68'
68_0	COME_FROM         '65'

68	LOAD_FAST         'output'
71	LOAD_CONST        '\n'
74	LOAD_CONST        '<code_object write>'
77	MAKE_FUNCTION_2   None
80	STORE_FAST        'write'

83	LOAD_CONST        None
86	STORE_FAST        'prevline'

89	SETUP_LOOP        '371'

92	LOAD_FAST         'input'
95	LOAD_ATTR         'readline'
98	CALL_FUNCTION_0   None
101	STORE_FAST        'line'

104	LOAD_FAST         'line'
107	JUMP_IF_TRUE      '114'

110	BREAK_LOOP        None
111	JUMP_FORWARD      '114'
114_0	COME_FROM         '111'

114	BUILD_LIST_0      None
117	STORE_FAST        'outline'

120	LOAD_CONST        ''
123	STORE_FAST        'stripped'

126	LOAD_FAST         'line'
129	LOAD_CONST        -1
132	SLICE+1           None
133	LOAD_CONST        '\n'
136	COMPARE_OP        '=='
139	JUMP_IF_FALSE     '161'

142	LOAD_FAST         'line'
145	LOAD_CONST        -1
148	SLICE+2           None
149	STORE_FAST        'line'

152	LOAD_CONST        '\n'
155	STORE_FAST        'stripped'
158	JUMP_FORWARD      '161'
161_0	COME_FROM         '158'

161	SETUP_LOOP        '258'
164	LOAD_FAST         'line'
167	GET_ITER          None
168	FOR_ITER          '257'
171	STORE_FAST        'c'

174	LOAD_GLOBAL       'needsquoting'
177	LOAD_FAST         'c'
180	LOAD_FAST         'quotetabs'
183	LOAD_FAST         'header'
186	CALL_FUNCTION_3   None
189	JUMP_IF_FALSE     '207'

192	LOAD_GLOBAL       'quote'
195	LOAD_FAST         'c'
198	CALL_FUNCTION_1   None
201	STORE_FAST        'c'
204	JUMP_FORWARD      '207'
207_0	COME_FROM         '204'

207	LOAD_FAST         'header'
210	JUMP_IF_FALSE     '241'
213	LOAD_FAST         'c'
216	LOAD_CONST        ' '
219	COMPARE_OP        '=='
222_0	COME_FROM         '210'
222	JUMP_IF_FALSE     '241'

225	LOAD_FAST         'outline'
228	LOAD_ATTR         'append'
231	LOAD_CONST        '_'
234	CALL_FUNCTION_1   None
237	POP_TOP           None
238	JUMP_BACK         '168'

241	LOAD_FAST         'outline'
244	LOAD_ATTR         'append'
247	LOAD_FAST         'c'
250	CALL_FUNCTION_1   None
253	POP_TOP           None
254	JUMP_BACK         '168'
257	POP_BLOCK         None
258_0	COME_FROM         '161'

258	LOAD_FAST         'prevline'
261	LOAD_CONST        None
264	COMPARE_OP        'is not'
267	JUMP_IF_FALSE     '283'

270	LOAD_FAST         'write'
273	LOAD_FAST         'prevline'
276	CALL_FUNCTION_1   None
279	POP_TOP           None
280	JUMP_FORWARD      '283'
283_0	COME_FROM         '280'

283	LOAD_GLOBAL       'EMPTYSTRING'
286	LOAD_ATTR         'join'
289	LOAD_FAST         'outline'
292	CALL_FUNCTION_1   None
295	STORE_FAST        'thisline'

298	SETUP_LOOP        '361'
301	LOAD_GLOBAL       'len'
304	LOAD_FAST         'thisline'
307	CALL_FUNCTION_1   None
310	LOAD_GLOBAL       'MAXLINESIZE'
313	COMPARE_OP        '>'
316	JUMP_IF_FALSE     '360'

319	LOAD_FAST         'write'
322	LOAD_FAST         'thisline'
325	LOAD_GLOBAL       'MAXLINESIZE'
328	LOAD_CONST        1
331	BINARY_SUBTRACT   None
332	SLICE+2           None
333	LOAD_CONST        'lineEnd'
336	LOAD_CONST        '=\n'
339	CALL_FUNCTION_257 None
342	POP_TOP           None

343	LOAD_FAST         'thisline'
346	LOAD_GLOBAL       'MAXLINESIZE'
349	LOAD_CONST        1
352	BINARY_SUBTRACT   None
353	SLICE+1           None
354	STORE_FAST        'thisline'
357	JUMP_BACK         '301'
360	POP_BLOCK         None
361_0	COME_FROM         '298'

361	LOAD_FAST         'thisline'
364	STORE_FAST        'prevline'
367	JUMP_BACK         '92'
370	POP_BLOCK         None
371_0	COME_FROM         '89'

371	LOAD_FAST         'prevline'
374	LOAD_CONST        None
377	COMPARE_OP        'is not'
380	JUMP_IF_FALSE     '402'

383	LOAD_FAST         'write'
386	LOAD_FAST         'prevline'
389	LOAD_CONST        'lineEnd'
392	LOAD_FAST         'stripped'
395	CALL_FUNCTION_257 None
398	POP_TOP           None
399	JUMP_FORWARD      '402'
402_0	COME_FROM         '399'
402	LOAD_CONST        None
405	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 370


def encodestring(s, quotetabs = 0, header = 0):
    if b2a_qp is not None:
        return b2a_qp(s, quotetabs=quotetabs, header=header)
    from cStringIO import StringIO
    infp = StringIO(s)
    outfp = StringIO()
    encode(infp, outfp, quotetabs, header)
    return outfp.getvalue()


def decode--- This code section failed: ---

0	LOAD_GLOBAL       'a2b_qp'
3	LOAD_CONST        None
6	COMPARE_OP        'is not'
9	JUMP_IF_FALSE     '62'

12	LOAD_FAST         'input'
15	LOAD_ATTR         'read'
18	CALL_FUNCTION_0   None
21	STORE_FAST        'data'

24	LOAD_GLOBAL       'a2b_qp'
27	LOAD_FAST         'data'
30	LOAD_CONST        'header'
33	LOAD_FAST         'header'
36	CALL_FUNCTION_257 None
39	STORE_FAST        'odata'

42	LOAD_FAST         'output'
45	LOAD_ATTR         'write'
48	LOAD_FAST         'odata'
51	CALL_FUNCTION_1   None
54	POP_TOP           None

55	LOAD_CONST        None
58	RETURN_VALUE      None
59	JUMP_FORWARD      '62'
62_0	COME_FROM         '59'

62	LOAD_CONST        ''
65	STORE_FAST        'new'

68	SETUP_LOOP        '577'

71	LOAD_FAST         'input'
74	LOAD_ATTR         'readline'
77	CALL_FUNCTION_0   None
80	STORE_FAST        'line'

83	LOAD_FAST         'line'
86	JUMP_IF_TRUE      '93'
89	BREAK_LOOP        None
90	JUMP_FORWARD      '93'
93_0	COME_FROM         '90'

93	LOAD_CONST        0
96	LOAD_GLOBAL       'len'
99	LOAD_FAST         'line'
102	CALL_FUNCTION_1   None
105	ROT_TWO           None
106	STORE_FAST        'i'
109	STORE_FAST        'n'

112	LOAD_FAST         'n'
115	LOAD_CONST        0
118	COMPARE_OP        '>'
121	JUMP_IF_FALSE     '212'
124	LOAD_FAST         'line'
127	LOAD_FAST         'n'
130	LOAD_CONST        1
133	BINARY_SUBTRACT   None
134	BINARY_SUBSCR     None
135	LOAD_CONST        '\n'
138	COMPARE_OP        '=='
141_0	COME_FROM         '121'
141	JUMP_IF_FALSE     '212'

144	LOAD_CONST        0
147	STORE_FAST        'partial'
150	LOAD_FAST         'n'
153	LOAD_CONST        1
156	BINARY_SUBTRACT   None
157	STORE_FAST        'n'

160	SETUP_LOOP        '218'
163	LOAD_FAST         'n'
166	LOAD_CONST        0
169	COMPARE_OP        '>'
172	JUMP_IF_FALSE     '208'
175	LOAD_FAST         'line'
178	LOAD_FAST         'n'
181	LOAD_CONST        1
184	BINARY_SUBTRACT   None
185	BINARY_SUBSCR     None
186	LOAD_CONST        ' \t\r'
189	COMPARE_OP        'in'
192_0	COME_FROM         '172'
192	JUMP_IF_FALSE     '208'

195	LOAD_FAST         'n'
198	LOAD_CONST        1
201	BINARY_SUBTRACT   None
202	STORE_FAST        'n'
205	JUMP_BACK         '163'
208	POP_BLOCK         None
209_0	COME_FROM         '160'
209	JUMP_FORWARD      '218'

212	LOAD_CONST        1
215	STORE_FAST        'partial'
218_0	COME_FROM         '209'

218	SETUP_LOOP        '541'
221	LOAD_FAST         'i'
224	LOAD_FAST         'n'
227	COMPARE_OP        '<'
230	JUMP_IF_FALSE     '540'

233	LOAD_FAST         'line'
236	LOAD_FAST         'i'
239	BINARY_SUBSCR     None
240	STORE_FAST        'c'

243	LOAD_FAST         'c'
246	LOAD_CONST        '_'
249	COMPARE_OP        '=='
252	JUMP_IF_FALSE     '284'
255	LOAD_FAST         'header'
258_0	COME_FROM         '252'
258	JUMP_IF_FALSE     '284'

261	LOAD_FAST         'new'
264	LOAD_CONST        ' '
267	BINARY_ADD        None
268	STORE_FAST        'new'
271	LOAD_FAST         'i'
274	LOAD_CONST        1
277	BINARY_ADD        None
278	STORE_FAST        'i'
281	JUMP_BACK         '221'

284	LOAD_FAST         'c'
287	LOAD_GLOBAL       'ESCAPE'
290	COMPARE_OP        '!='
293	JUMP_IF_FALSE     '319'

296	LOAD_FAST         'new'
299	LOAD_FAST         'c'
302	BINARY_ADD        None
303	STORE_FAST        'new'
306	LOAD_FAST         'i'
309	LOAD_CONST        1
312	BINARY_ADD        None
313	STORE_FAST        'i'
316	JUMP_BACK         '221'

319	LOAD_FAST         'i'
322	LOAD_CONST        1
325	BINARY_ADD        None
326	LOAD_FAST         'n'
329	COMPARE_OP        '=='
332	JUMP_IF_FALSE     '352'
335	LOAD_FAST         'partial'
338	UNARY_NOT         None
339_0	COME_FROM         '332'
339	JUMP_IF_FALSE     '352'

342	LOAD_CONST        1
345	STORE_FAST        'partial'
348	BREAK_LOOP        None
349	JUMP_BACK         '221'

352	LOAD_FAST         'i'
355	LOAD_CONST        1
358	BINARY_ADD        None
359	LOAD_FAST         'n'
362	COMPARE_OP        '<'
365	JUMP_IF_FALSE     '411'
368	LOAD_FAST         'line'
371	LOAD_FAST         'i'
374	LOAD_CONST        1
377	BINARY_ADD        None
378	BINARY_SUBSCR     None
379	LOAD_GLOBAL       'ESCAPE'
382	COMPARE_OP        '=='
385_0	COME_FROM         '365'
385	JUMP_IF_FALSE     '411'

388	LOAD_FAST         'new'
391	LOAD_GLOBAL       'ESCAPE'
394	BINARY_ADD        None
395	STORE_FAST        'new'
398	LOAD_FAST         'i'
401	LOAD_CONST        2
404	BINARY_ADD        None
405	STORE_FAST        'i'
408	JUMP_BACK         '221'

411	LOAD_FAST         'i'
414	LOAD_CONST        2
417	BINARY_ADD        None
418	LOAD_FAST         'n'
421	COMPARE_OP        '<'
424	JUMP_IF_FALSE     '517'
427	LOAD_GLOBAL       'ishex'
430	LOAD_FAST         'line'
433	LOAD_FAST         'i'
436	LOAD_CONST        1
439	BINARY_ADD        None
440	BINARY_SUBSCR     None
441	CALL_FUNCTION_1   None
444	JUMP_IF_FALSE     '517'
447	LOAD_GLOBAL       'ishex'
450	LOAD_FAST         'line'
453	LOAD_FAST         'i'
456	LOAD_CONST        2
459	BINARY_ADD        None
460	BINARY_SUBSCR     None
461	CALL_FUNCTION_1   None
464_0	COME_FROM         '424'
464_1	COME_FROM         '444'
464	JUMP_IF_FALSE     '517'

467	LOAD_FAST         'new'
470	LOAD_GLOBAL       'chr'
473	LOAD_GLOBAL       'unhex'
476	LOAD_FAST         'line'
479	LOAD_FAST         'i'
482	LOAD_CONST        1
485	BINARY_ADD        None
486	LOAD_FAST         'i'
489	LOAD_CONST        3
492	BINARY_ADD        None
493	SLICE+3           None
494	CALL_FUNCTION_1   None
497	CALL_FUNCTION_1   None
500	BINARY_ADD        None
501	STORE_FAST        'new'
504	LOAD_FAST         'i'
507	LOAD_CONST        3
510	BINARY_ADD        None
511	STORE_FAST        'i'
514	JUMP_BACK         '221'

517	LOAD_FAST         'new'
520	LOAD_FAST         'c'
523	BINARY_ADD        None
524	STORE_FAST        'new'
527	LOAD_FAST         'i'
530	LOAD_CONST        1
533	BINARY_ADD        None
534	STORE_FAST        'i'
537	JUMP_BACK         '221'
540	POP_BLOCK         None
541_0	COME_FROM         '218'

541	LOAD_FAST         'partial'
544	JUMP_IF_TRUE      '573'

547	LOAD_FAST         'output'
550	LOAD_ATTR         'write'
553	LOAD_FAST         'new'
556	LOAD_CONST        '\n'
559	BINARY_ADD        None
560	CALL_FUNCTION_1   None
563	POP_TOP           None

564	LOAD_CONST        ''
567	STORE_FAST        'new'
570	JUMP_BACK         '71'
573	JUMP_BACK         '71'
576	POP_BLOCK         None
577_0	COME_FROM         '68'

577	LOAD_FAST         'new'
580	JUMP_IF_FALSE     '599'

583	LOAD_FAST         'output'
586	LOAD_ATTR         'write'
589	LOAD_FAST         'new'
592	CALL_FUNCTION_1   None
595	POP_TOP           None
596	JUMP_FORWARD      '599'
599_0	COME_FROM         '596'
599	LOAD_CONST        None
602	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK
# Can't uncompyle C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\quopri.pyc
Traceback (most recent call last):
  File "C:\python27\lib\uncompyle2\__init__.py", line 206, in main
    uncompyle_file(infile, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 143, in uncompyle_file
    uncompyle(version, co, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 132, in uncompyle
    raise walk.ERROR
ParserError: --- This code section failed: ---

0	LOAD_GLOBAL       'a2b_qp'
3	LOAD_CONST        None
6	COMPARE_OP        'is not'
9	JUMP_IF_FALSE     '62'

12	LOAD_FAST         'input'
15	LOAD_ATTR         'read'
18	CALL_FUNCTION_0   None
21	STORE_FAST        'data'

24	LOAD_GLOBAL       'a2b_qp'
27	LOAD_FAST         'data'
30	LOAD_CONST        'header'
33	LOAD_FAST         'header'
36	CALL_FUNCTION_257 None
39	STORE_FAST        'odata'

42	LOAD_FAST         'output'
45	LOAD_ATTR         'write'
48	LOAD_FAST         'odata'
51	CALL_FUNCTION_1   None
54	POP_TOP           None

55	LOAD_CONST        None
58	RETURN_VALUE      None
59	JUMP_FORWARD      '62'
62_0	COME_FROM         '59'

62	LOAD_CONST        ''
65	STORE_FAST        'new'

68	SETUP_LOOP        '577'

71	LOAD_FAST         'input'
74	LOAD_ATTR         'readline'
77	CALL_FUNCTION_0   None
80	STORE_FAST        'line'

83	LOAD_FAST         'line'
86	JUMP_IF_TRUE      '93'
89	BREAK_LOOP        None
90	JUMP_FORWARD      '93'
93_0	COME_FROM         '90'

93	LOAD_CONST        0
96	LOAD_GLOBAL       'len'
99	LOAD_FAST         'line'
102	CALL_FUNCTION_1   None
105	ROT_TWO           None
106	STORE_FAST        'i'
109	STORE_FAST        'n'

112	LOAD_FAST         'n'
115	LOAD_CONST        0
118	COMPARE_OP        '>'
121	JUMP_IF_FALSE     '212'
124	LOAD_FAST         'line'
127	LOAD_FAST         'n'
130	LOAD_CONST        1
133	BINARY_SUBTRACT   None
134	BINARY_SUBSCR     None
135	LOAD_CONST        '\n'
138	COMPARE_OP        '=='
141_0	COME_FROM         '121'
141	JUMP_IF_FALSE     '212'

144	LOAD_CONST        0
147	STORE_FAST        'partial'
150	LOAD_FAST         'n'
153	LOAD_CONST        1
156	BINARY_SUBTRACT   None
157	STORE_FAST        'n'

160	SETUP_LOOP        '218'
163	LOAD_FAST         'n'
166	LOAD_CONST        0
169	COMPARE_OP        '>'
172	JUMP_IF_FALSE     '208'
175	LOAD_FAST         'line'
178	LOAD_FAST         'n'
181	LOAD_CONST        1
184	BINARY_SUBTRACT   None
185	BINARY_SUBSCR     None
186	LOAD_CONST        ' \t\r'
189	COMPARE_OP        'in'
192_0	COME_FROM         '172'
192	JUMP_IF_FALSE     '208'

195	LOAD_FAST         'n'
198	LOAD_CONST        1
201	BINARY_SUBTRACT   None
202	STORE_FAST        'n'
205	JUMP_BACK         '163'
208	POP_BLOCK         None
209_0	COME_FROM         '160'
209	JUMP_FORWARD      '218'

212	LOAD_CONST        1
215	STORE_FAST        'partial'
218_0	COME_FROM         '209'

218	SETUP_LOOP        '541'
221	LOAD_FAST         'i'
224	LOAD_FAST         'n'
227	COMPARE_OP        '<'
230	JUMP_IF_FALSE     '540'

233	LOAD_FAST         'line'
236	LOAD_FAST         'i'
239	BINARY_SUBSCR     None
240	STORE_FAST        'c'

243	LOAD_FAST         'c'
246	LOAD_CONST        '_'
249	COMPARE_OP        '=='
252	JUMP_IF_FALSE     '284'
255	LOAD_FAST         'header'
258_0	COME_FROM         '252'
258	JUMP_IF_FALSE     '284'

261	LOAD_FAST         'new'
264	LOAD_CONST        ' '
267	BINARY_ADD        None
268	STORE_FAST        'new'
271	LOAD_FAST         'i'
274	LOAD_CONST        1
277	BINARY_ADD        None
278	STORE_FAST        'i'
281	JUMP_BACK         '221'

284	LOAD_FAST         'c'
287	LOAD_GLOBAL       'ESCAPE'
290	COMPARE_OP        '!='
293	JUMP_IF_FALSE     '319'

296	LOAD_FAST         'new'
299	LOAD_FAST         'c'
302	BINARY_ADD        None
303	STORE_FAST        'new'
306	LOAD_FAST         'i'
309	LOAD_CONST        1
312	BINARY_ADD        None
313	STORE_FAST        'i'
316	JUMP_BACK         '221'

319	LOAD_FAST         'i'
322	LOAD_CONST        1
325	BINARY_ADD        None
326	LOAD_FAST         'n'
329	COMPARE_OP        '=='
332	JUMP_IF_FALSE     '352'
335	LOAD_FAST   ' token at offset 576


def decodestring(s, header = 0):
    if a2b_qp is not None:
        return a2b_qp(s, header=header)
    from cStringIO import StringIO
    infp = StringIO(s)
    outfp = StringIO()
    decode(infp, outfp, header=header)
    return outfp.getvalue()


def ishex(c):
    return ('0' <= c <= '9' or 'a' <= c <= 'f' or 'A') <= c <= 'F'


def unhex(s):
    bits = 0
    for c in s:
        if '0' <= c <= '9':
            i = ord('0')
        elif 'a' <= c <= 'f':
            i = ord('a') - 10
        elif 'A' <= c <= 'F':
            i = ord('A') - 10
        else:
            break
        bits = bits * 16 + (ord(c) - i)

    return bits


def main():
    import sys
    import getopt
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'td')
    except getopt.error as msg:
        sys.stdout = sys.stderr
        print msg
        print 'usage: quopri [-t | -d] [file] ...'
        print '-t: quote tabs'
        print '-d: decode; default encode'
        sys.exit(2)

    deco = 0
    tabs = 0
    for o, a in opts:
        if o == '-t':
            tabs = 1
        if o == '-d':
            deco = 1

    if tabs and deco:
        sys.stdout = sys.stderr
        print '-t and -d are mutually exclusive'
        sys.exit(2)
    if not args:
        args = ['-']
    sts = 0
    for file in args:
        if file == '-':
            fp = sys.stdin
        else:
            try:
                fp = open(file)
            except IOError as msg:
                sys.stderr.write("%s: can't open (%s)\n" % (file, msg))
                sts = 1
                continue

        if deco:
            decode(fp, sys.stdout)
        else:
            encode(fp, sys.stdout, tabs)
        if fp is not sys.stdin:
            fp.close()

    if sts:
        sys.exit(sts)


if __name__ == '__main__':
    main()# decompiled 0 files: 0 okay, 1 failed, 0 verify failed
# 2013.08.22 22:13:24 Pacific Daylight Time
      'partial'
338	UNARY_NOT         None
339_0	COME_FROM         '332'
339	JUMP_IF_FALSE     '352'

342	LOAD_CONST        1
345	STORE_FAST        'partial'
348	BREAK_LOOP        None
349	JUMP_BACK         '221'

352	LOAD_FAST         'i'
355	LOAD_CONST        1
358	BINARY_ADD        None
359	LOAD_FAST         'n'
362	COMPARE_OP        '<'
365	JUMP_IF_FALSE     '411'
368	LOAD_FAST         'line'
371	LOAD_FAST         'i'
374	LOAD_CONST        1
377	BINARY_ADD        None
378	BINARY_SUBSCR     None
379	LOAD_GLOBAL       'ESCAPE'
382	COMPARE_OP        '=='
385_0	COME_FROM         '365'
385	JUMP_IF_FALSE     '411'

388	LOAD_FAST         'new'
391	LOAD_GLOBAL       'ESCAPE'
394	BINARY_ADD        None
395	STORE_FAST        'new'
398	LOAD_FAST         'i'
401	LOAD_CONST        2
404	BINARY_ADD        None
405	STORE_FAST        'i'
408	JUMP_BACK         '221'

411	LOAD_FAST         'i'
414	LOAD_CONST        2
417	BINARY_ADD        None
418	LOAD_FAST         'n'
421	COMPARE_OP        '<'
424	JUMP_IF_FALSE     '517'
427	LOAD_GLOBAL       'ishex'
430	LOAD_FAST         'line'
433	LOAD_FAST         'i'
436	LOAD_CONST        1
439	BINARY_ADD        None
440	BINARY_SUBSCR     None
441	CALL_FUNCTION_1   None
444	JUMP_IF_FALSE     '517'
447	LOAD_GLOBAL       'ishex'
450	LOAD_FAST         'line'
453	LOAD_FAST         'i'
456	LOAD_CONST        2
459	BINARY_ADD        None
460	BINARY_SUBSCR     None
461	CALL_FUNCTION_1   None
464_0	COME_FROM         '424'
464_1	COME_FROM         '444'
464	JUMP_IF_FALSE     '517'

467	LOAD_FAST         'new'
470	LOAD_GLOBAL       'chr'
473	LOAD_GLOBAL       'unhex'
476	LOAD_FAST         'line'
479	LOAD_FAST         'i'
482	LOAD_CONST        1
485	BINARY_ADD        None
486	LOAD_FAST         'i'
489	LOAD_CONST        3
492	BINARY_ADD        None
493	SLICE+3           None
494	CALL_FUNCTION_1   None
497	CALL_FUNCTION_1   None
500	BINARY_ADD        None
501	STORE_FAST        'new'
504	LOAD_FAST         'i'
507	LOAD_CONST        3
510	BINARY_ADD        None
511	STORE_FAST        'i'
514	JUMP_BACK         '221'

517	LOAD_FAST         'new'
520	LOAD_FAST         'c'
523	BINARY_ADD        None
524	STORE_FAST        'new'
527	LOAD_FAST         'i'
530	LOAD_CONST        1
533	BINARY_ADD        None
534	STORE_FAST        'i'
537	JUMP_BACK         '221'
540	POP_BLOCK         None
541_0	COME_FROM         '218'

541	LOAD_FAST         'partial'
544	JUMP_IF_TRUE      '573'

547	LOAD_FAST         'output'
550	LOAD_ATTR         'write'
553	LOAD_FAST         'new'
556	LOAD_CONST        '\n'
559	BINARY_ADD        None
560	CALL_FUNCTION_1   None
563	POP_TOP           None

564	LOAD_CONST        ''
567	STORE_FAST        'new'
570	JUMP_BACK         '71'
573	JUMP_BACK         '71'
576	POP_BLOCK         None
577_0	COME_FROM         '68'

577	LOAD_FAST         'new'
580	JUMP_IF_FALSE     '599'

583	LOAD_FAST         'output'
586	LOAD_ATTR         'write'
589	LOAD_FAST         'new'
592	CALL_FUNCTION_1   None
595	POP_TOP           None
596	JUMP_FORWARD      '599'
599_0	COME_FROM         '596'
599	LOAD_CONST        None
602	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 576

