# 2013.08.22 22:13:40 Pacific Daylight Time
# Embedded file name: uu
import binascii
import os
import sys
from types import StringType
__all__ = ['Error', 'encode', 'decode']

class Error(Exception):
    __module__ = __name__


def encode(in_file, out_file, name = None, mode = None):
    if in_file == '-':
        in_file = sys.stdin
    elif isinstance(in_file, StringType):
        if name is None:
            name = os.path.basename(in_file)
        if mode is None:
            try:
                mode = os.stat(in_file).st_mode
            except AttributeError:
                pass

        in_file = open(in_file, 'rb')
    if out_file == '-':
        out_file = sys.stdout
    elif isinstance(out_file, StringType):
        out_file = open(out_file, 'w')
    if name is None:
        name = '-'
    if mode is None:
        mode = 438
    out_file.write('begin %o %s\n' % (mode & 511, name))
    str = in_file.read(45)
    while len(str) > 0:
        out_file.write(binascii.b2a_uu(str))
        str = in_file.read(45)

    out_file.write(' \nend\n')
    return


def decode--- This code section failed: ---

0	LOAD_FAST         'in_file'
3	LOAD_CONST        '-'
6	COMPARE_OP        '=='
9	JUMP_IF_FALSE     '24'

12	LOAD_GLOBAL       'sys'
15	LOAD_ATTR         'stdin'
18	STORE_FAST        'in_file'
21	JUMP_FORWARD      '54'

24	LOAD_GLOBAL       'isinstance'
27	LOAD_FAST         'in_file'
30	LOAD_GLOBAL       'StringType'
33	CALL_FUNCTION_2   None
36	JUMP_IF_FALSE     '54'

39	LOAD_GLOBAL       'open'
42	LOAD_FAST         'in_file'
45	CALL_FUNCTION_1   None
48	STORE_FAST        'in_file'
51	JUMP_FORWARD      '54'
54_0	COME_FROM         '21'
54_1	COME_FROM         '51'

54	SETUP_LOOP        '210'

57	LOAD_FAST         'in_file'
60	LOAD_ATTR         'readline'
63	CALL_FUNCTION_0   None
66	STORE_FAST        'hdr'

69	LOAD_FAST         'hdr'
72	JUMP_IF_TRUE      '87'

75	LOAD_GLOBAL       'Error'
78	LOAD_CONST        'No valid begin line found in input file'
81	RAISE_VARARGS_2   None
84	JUMP_FORWARD      '87'
87_0	COME_FROM         '84'

87	LOAD_FAST         'hdr'
90	LOAD_CONST        5
93	SLICE+2           None
94	LOAD_CONST        'begin'
97	COMPARE_OP        '!='
100	JUMP_IF_FALSE     '109'

103	CONTINUE          '57'
106	JUMP_FORWARD      '109'
109_0	COME_FROM         '106'

109	LOAD_FAST         'hdr'
112	LOAD_ATTR         'split'
115	LOAD_CONST        ' '
118	LOAD_CONST        2
121	CALL_FUNCTION_2   None
124	STORE_FAST        'hdrfields'

127	LOAD_GLOBAL       'len'
130	LOAD_FAST         'hdrfields'
133	CALL_FUNCTION_1   None
136	LOAD_CONST        3
139	COMPARE_OP        '=='
142	JUMP_IF_FALSE     '206'
145	LOAD_FAST         'hdrfields'
148	LOAD_CONST        0
151	BINARY_SUBSCR     None
152	LOAD_CONST        'begin'
155	COMPARE_OP        '=='
158_0	COME_FROM         '142'
158	JUMP_IF_FALSE     '206'

161	SETUP_EXCEPT      '186'

164	LOAD_GLOBAL       'int'
167	LOAD_FAST         'hdrfields'
170	LOAD_CONST        1
173	BINARY_SUBSCR     None
174	LOAD_CONST        8
177	CALL_FUNCTION_2   None
180	POP_TOP           None

181	BREAK_LOOP        None
182	POP_BLOCK         None
183	JUMP_ABSOLUTE     '206'
186_0	COME_FROM         '161'

186	DUP_TOP           None
187	LOAD_GLOBAL       'ValueError'
190	COMPARE_OP        'exception match'
193	JUMP_IF_FALSE     '202'
196	POP_TOP           None
197	POP_TOP           None
198	POP_TOP           None

199	JUMP_ABSOLUTE     '206'
202	END_FINALLY       None
203_0	COME_FROM         '202'
203	JUMP_BACK         '57'
206	JUMP_BACK         '57'
209	POP_BLOCK         None
210_0	COME_FROM         '54'

210	LOAD_FAST         'out_file'
213	LOAD_CONST        None
216	COMPARE_OP        'is'
219	JUMP_IF_FALSE     '275'

222	LOAD_FAST         'hdrfields'
225	LOAD_CONST        2
228	BINARY_SUBSCR     None
229	LOAD_ATTR         'rstrip'
232	CALL_FUNCTION_0   None
235	STORE_FAST        'out_file'

238	LOAD_GLOBAL       'os'
241	LOAD_ATTR         'path'
244	LOAD_ATTR         'exists'
247	LOAD_FAST         'out_file'
250	CALL_FUNCTION_1   None
253	JUMP_IF_FALSE     '272'

256	LOAD_GLOBAL       'Error'
259	LOAD_CONST        'Cannot overwrite existing file: %s'
262	LOAD_FAST         'out_file'
265	BINARY_MODULO     None
266	RAISE_VARARGS_2   None
269	JUMP_ABSOLUTE     '275'
272	JUMP_FORWARD      '275'
275_0	COME_FROM         '272'

275	LOAD_FAST         'mode'
278	LOAD_CONST        None
281	COMPARE_OP        'is'
284	JUMP_IF_FALSE     '309'

287	LOAD_GLOBAL       'int'
290	LOAD_FAST         'hdrfields'
293	LOAD_CONST        1
296	BINARY_SUBSCR     None
297	LOAD_CONST        8
300	CALL_FUNCTION_2   None
303	STORE_FAST        'mode'
306	JUMP_FORWARD      '309'
309_0	COME_FROM         '306'

309	LOAD_FAST         'out_file'
312	LOAD_CONST        '-'
315	COMPARE_OP        '=='
318	JUMP_IF_FALSE     '333'

321	LOAD_GLOBAL       'sys'
324	LOAD_ATTR         'stdout'
327	STORE_FAST        'out_file'
330	JUMP_FORWARD      '415'

333	LOAD_GLOBAL       'isinstance'
336	LOAD_FAST         'out_file'
339	LOAD_GLOBAL       'StringType'
342	CALL_FUNCTION_2   None
345	JUMP_IF_FALSE     '415'

348	LOAD_GLOBAL       'open'
351	LOAD_FAST         'out_file'
354	LOAD_CONST        'wb'
357	CALL_FUNCTION_2   None
360	STORE_FAST        'fp'

363	SETUP_EXCEPT      '389'

366	LOAD_GLOBAL       'os'
369	LOAD_ATTR         'path'
372	LOAD_ATTR         'chmod'
375	LOAD_FAST         'out_file'
378	LOAD_FAST         'mode'
381	CALL_FUNCTION_2   None
384	POP_TOP           None
385	POP_BLOCK         None
386	JUMP_FORWARD      '406'
389_0	COME_FROM         '363'

389	DUP_TOP           None
390	LOAD_GLOBAL       'AttributeError'
393	COMPARE_OP        'exception match'
396	JUMP_IF_FALSE     '405'
399	POP_TOP           None
400	POP_TOP           None
401	POP_TOP           None

402	JUMP_FORWARD      '406'
405	END_FINALLY       None
406_0	COME_FROM         '386'
406_1	COME_FROM         '405'

406	LOAD_FAST         'fp'
409	STORE_FAST        'out_file'
412	JUMP_FORWARD      '415'
415_0	COME_FROM         '330'
415_1	COME_FROM         '412'

415	LOAD_FAST         'in_file'
418	LOAD_ATTR         'readline'
421	CALL_FUNCTION_0   None
424	STORE_FAST        's'

427	SETUP_LOOP        '617'
430	LOAD_FAST         's'
433	JUMP_IF_FALSE     '616'
436	LOAD_FAST         's'
439	LOAD_ATTR         'strip'
442	CALL_FUNCTION_0   None
445	LOAD_CONST        'end'
448	COMPARE_OP        '!='
451_0	COME_FROM         '433'
451	JUMP_IF_FALSE     '616'

454	SETUP_EXCEPT      '476'

457	LOAD_GLOBAL       'binascii'
460	LOAD_ATTR         'a2b_uu'
463	LOAD_FAST         's'
466	CALL_FUNCTION_1   None
469	STORE_FAST        'data'
472	POP_BLOCK         None
473	JUMP_FORWARD      '588'
476_0	COME_FROM         '454'

476	DUP_TOP           None
477	LOAD_GLOBAL       'binascii'
480	LOAD_ATTR         'Error'
483	COMPARE_OP        'exception match'
486	JUMP_IF_FALSE     '587'
489	POP_TOP           None
490	STORE_FAST        'v'
493	POP_TOP           None

494	LOAD_GLOBAL       'ord'
497	LOAD_FAST         's'
500	LOAD_CONST        0
503	BINARY_SUBSCR     None
504	CALL_FUNCTION_1   None
507	LOAD_CONST        32
510	BINARY_SUBTRACT   None
511	LOAD_CONST        63
514	BINARY_AND        None
515	LOAD_CONST        4
518	BINARY_MULTIPLY   None
519	LOAD_CONST        5
522	BINARY_ADD        None
523	LOAD_CONST        3
526	BINARY_DIVIDE     None
527	STORE_FAST        'nbytes'

530	LOAD_GLOBAL       'binascii'
533	LOAD_ATTR         'a2b_uu'
536	LOAD_FAST         's'
539	LOAD_FAST         'nbytes'
542	SLICE+2           None
543	CALL_FUNCTION_1   None
546	STORE_FAST        'data'

549	LOAD_FAST         'quiet'
552	JUMP_IF_TRUE      '584'

555	LOAD_GLOBAL       'sys'
558	LOAD_ATTR         'stderr'
561	LOAD_ATTR         'write'
564	LOAD_CONST        'Warning: %s\n'
567	LOAD_GLOBAL       'str'
570	LOAD_FAST         'v'
573	CALL_FUNCTION_1   None
576	BINARY_MODULO     None
577	CALL_FUNCTION_1   None
580	POP_TOP           None
581	JUMP_ABSOLUTE     '588'
584	JUMP_FORWARD      '588'
587	END_FINALLY       None
588_0	COME_FROM         '473'
588_1	COME_FROM         '587'

588	LOAD_FAST         'out_file'
591	LOAD_ATTR         'write'
594	LOAD_FAST         'data'
597	CALL_FUNCTION_1   None
600	POP_TOP           None

601	
# Can't uncompyle C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\uu.pyc
Traceback (most recent call last):
  File "C:\python27\lib\uncompyle2\__init__.py", line 206, in main
    uncompyle_file(infile, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 143, in uncompyle_file
    uncompyle(version, co, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 132, in uncompyle
    raise walk.ERROR
ParserError: --- This code section failed: ---

0	LOAD_FAST         'in_file'
3	LOAD_CONST        '-'
6	COMPARE_OP        '=='
9	JUMP_IF_FALSE     '24'

12	LOAD_GLOBAL       'sys'
15	LOAD_ATTR         'stdin'
18	STORE_FAST        'in_file'
21	JUMP_FORWARD      '54'

24	LOAD_GLOBAL       'isinstance'
27	LOAD_FAST         'in_file'
30	LOAD_GLOBAL       'StringType'
33	CALL_FUNCTION_2   None
36	JUMP_IF_FALSE     '54'

39	LOAD_GLOBAL       'open'
42	LOAD_FAST         'in_file'
45	CALL_FUNCTION_1   None
48	STORE_FAST        'in_file'
51	JUMP_FORWARD      '54'
54_0	COME_FROM         '21'
54_1	COME_FROM         '51'

54	SETUP_LOOP        '210'

57	LOAD_FAST         'in_file'
60	LOAD_ATTR         'readline'
63	CALL_FUNCTION_0   None
66	STORE_FAST        'hdr'

69	LOAD_FAST         'hdr'
72	JUMP_IF_TRUE      '87'

75	LOAD_GLOBAL       'Error'
78	LOAD_CONST        'No valid begin line found in input file'
81	RAISE_VARARGS_2   None
84	JUMP_FORWARD      '87'
87_0	COME_FROM         '84'

87	LOAD_FAST         'hdr'
90	LOAD_CONST        5
93	SLICE+2           None
94	LOAD_CONST        'begin'
97	COMPARE_OP        '!='
100	JUMP_IF_FALSE     '109'

103	CONTINUE          '57'
106	JUMP_FORWARD      '109'
109_0	COME_FROM         '106'

109	LOAD_FAST         'hdr'
112	LOAD_ATTR         'split'
115	LOAD_CONST        ' '
118	LOAD_CONST        2
121	CALL_FUNCTION_2   None
124	STORE_FAST        'hdrfields'

127	LOAD_GLOBAL       'len'
130	LOAD_FAST         'hdrfields'
133	CALL_FUNCTION_1   None
136	LOAD_CONST        3
139	COMPARE_OP        '=='
142	JUMP_IF_FALSE     '206'
145	LOAD_FAST         'hdrfields'
148	LOAD_CONST        0
151	BINARY_SUBSCR     None
152	LOAD_CONST        'begin'
155	COMPARE_OP        '=='
158_0	COME_FROM         '142'
158	JUMP_IF_FALSE     '206'

161	SETUP_EXCEPT      '186'

164	LOAD_GLOBAL       'int'
167	LOAD_FAST         'hdrfields'
170	LOAD_CONST        1
173	BINARY_SUBSCR     None
174	LOAD_CONST        8
177	CALL_FUNCTION_2   None
180	POP_TOP           None

181	BREAK_LOOP        None
182	POP_BLOCK         None
183	JUMP_ABSOLUTE     '206'
186_0	COME_FROM         '161'

186	DUP_TOP           None
187	LOAD_GLOBAL       'ValueError'
190	COMPARE_OP        'exception match'
193	JUMP_IF_FALSE     '202'
196	POP_TOP           None
197	POP_TOP           None
198	POP_TOP           None

199	JUMP_ABSOLUTE     '206'
202	END_FINALLY       None
203_0	COME_FROM         '202'
203	JUMP_BACK         '57'
206	JUMP_BACK         '57'
209	POP_BLOCK         None
210_0	COME_FROM         '54'

210	LOAD_FAST         'out_file'
213	LOAD_CONST        None
216	COMPARE_OP        'is'
219	JUMP_IF_FALSE     '275'

222	LOAD_FAST         'hdrfields'
225	LOAD_CONST        2
228	BINARY_SUBSCR     None
229	LOAD_ATTR         'rstrip'
232	CALL_FUNCTION_0   None
235	STORE_FAST        'out_file'

238	LOAD_GLOBAL       'os'
241	LOAD_ATTR         'path'
244	LOAD_ATTR         'exists'
247	LOAD_FAST         'out_file'
250	CALL_FUNCTION_1   None
253	JUMP_IF_FALSE     '272'

256	LOAD_GLOBAL       'Error'
259	LOAD_CONST        'Cannot overwrite existing file: %s'
262	LOAD_FAST         'out_file'
265	BINARY_MODULO     None
266	RAISE_VARARGS_2   None
269	JUMP_ABSOLUTE     '275'
272	JUMP_FORWARD      '275'
275_0	COME_FROM         '272'

275	LOAD_FAST         'mode'
278	LOAD_CONST        None
281	COMPARE_OP        'is'
284	JUMP_IF_FALSE     '309'

287	LOAD_GLOBAL       'int'
290	LOAD_FAST         'hdrfields'
293	LOAD_CONST        1
296	BINARY_SUBSCR     None
297	LOAD_CONST        8
300	CALL_FUNCTION_2   None
303	STORE_FAST        'mode'
306	JUMP_FORWARD      '309'
309_0	COME_FROM         '306'

309LOAD_FAST         'in_file'
604	LOAD_ATTR         'readline'
607	CALL_FUNCTION_0   None
610	STORE_FAST        's'
613	JUMP_BACK         '430'
616	POP_BLOCK         None
617_0	COME_FROM         '427'

617	LOAD_FAST         's'
620	JUMP_IF_TRUE      '635'

623	LOAD_GLOBAL       'Error'
626	LOAD_CONST        'Truncated input file'
629	RAISE_VARARGS_2   None
632	JUMP_FORWARD      '635'
635_0	COME_FROM         '632'
635	LOAD_CONST        None
638	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 209


def test():
    import getopt
    dopt = 0
    topt = 0
    input = sys.stdin
    output = sys.stdout
    ok = 1
    try:
        optlist, args = getopt.getopt(sys.argv[1:], 'dt')
    except getopt.error:
        ok = 0

    if not ok or len(args) > 2:
        print 'Usage:', sys.argv[0], '[-d] [-t] [input [output]]'
        print ' -d: Decode (in stead of encode)'
        print ' -t: data is text, encoded format unix-compatible text'
        sys.exit(1)
    for o, a in optlist:
        if o == '-d':
            dopt = 1
        if o == '-t':
            topt = 1

    if len(args) > 0:
        input = args[0]
    if len(args) > 1:
        output = args[1]
    if dopt:
        if topt:
            if isinstance(output, StringType):
                output = open(output, 'w')
            else:
                print sys.argv[0], ': cannot do -t to stdout'
                sys.exit(1)
        decode(input, output)
    else:
        if topt:
            if isinstance(input, StringType):
                input = open(input, 'r')
            else:
                print sys.argv[0], ': cannot do -t from stdin'
                sys.exit(1)
        encode(input, output)


if __name__ == '__main__':
    test()# decompiled 0 files: 0 okay, 1 failed, 0 verify failed
# 2013.08.22 22:13:40 Pacific Daylight Time
	LOAD_FAST         'out_file'
312	LOAD_CONST        '-'
315	COMPARE_OP        '=='
318	JUMP_IF_FALSE     '333'

321	LOAD_GLOBAL       'sys'
324	LOAD_ATTR         'stdout'
327	STORE_FAST        'out_file'
330	JUMP_FORWARD      '415'

333	LOAD_GLOBAL       'isinstance'
336	LOAD_FAST         'out_file'
339	LOAD_GLOBAL       'StringType'
342	CALL_FUNCTION_2   None
345	JUMP_IF_FALSE     '415'

348	LOAD_GLOBAL       'open'
351	LOAD_FAST         'out_file'
354	LOAD_CONST        'wb'
357	CALL_FUNCTION_2   None
360	STORE_FAST        'fp'

363	SETUP_EXCEPT      '389'

366	LOAD_GLOBAL       'os'
369	LOAD_ATTR         'path'
372	LOAD_ATTR         'chmod'
375	LOAD_FAST         'out_file'
378	LOAD_FAST         'mode'
381	CALL_FUNCTION_2   None
384	POP_TOP           None
385	POP_BLOCK         None
386	JUMP_FORWARD      '406'
389_0	COME_FROM         '363'

389	DUP_TOP           None
390	LOAD_GLOBAL       'AttributeError'
393	COMPARE_OP        'exception match'
396	JUMP_IF_FALSE     '405'
399	POP_TOP           None
400	POP_TOP           None
401	POP_TOP           None

402	JUMP_FORWARD      '406'
405	END_FINALLY       None
406_0	COME_FROM         '386'
406_1	COME_FROM         '405'

406	LOAD_FAST         'fp'
409	STORE_FAST        'out_file'
412	JUMP_FORWARD      '415'
415_0	COME_FROM         '330'
415_1	COME_FROM         '412'

415	LOAD_FAST         'in_file'
418	LOAD_ATTR         'readline'
421	CALL_FUNCTION_0   None
424	STORE_FAST        's'

427	SETUP_LOOP        '617'
430	LOAD_FAST         's'
433	JUMP_IF_FALSE     '616'
436	LOAD_FAST         's'
439	LOAD_ATTR         'strip'
442	CALL_FUNCTION_0   None
445	LOAD_CONST        'end'
448	COMPARE_OP        '!='
451_0	COME_FROM         '433'
451	JUMP_IF_FALSE     '616'

454	SETUP_EXCEPT      '476'

457	LOAD_GLOBAL       'binascii'
460	LOAD_ATTR         'a2b_uu'
463	LOAD_FAST         's'
466	CALL_FUNCTION_1   None
469	STORE_FAST        'data'
472	POP_BLOCK         None
473	JUMP_FORWARD      '588'
476_0	COME_FROM         '454'

476	DUP_TOP           None
477	LOAD_GLOBAL       'binascii'
480	LOAD_ATTR         'Error'
483	COMPARE_OP        'exception match'
486	JUMP_IF_FALSE     '587'
489	POP_TOP           None
490	STORE_FAST        'v'
493	POP_TOP           None

494	LOAD_GLOBAL       'ord'
497	LOAD_FAST         's'
500	LOAD_CONST        0
503	BINARY_SUBSCR     None
504	CALL_FUNCTION_1   None
507	LOAD_CONST        32
510	BINARY_SUBTRACT   None
511	LOAD_CONST        63
514	BINARY_AND        None
515	LOAD_CONST        4
518	BINARY_MULTIPLY   None
519	LOAD_CONST        5
522	BINARY_ADD        None
523	LOAD_CONST        3
526	BINARY_DIVIDE     None
527	STORE_FAST        'nbytes'

530	LOAD_GLOBAL       'binascii'
533	LOAD_ATTR         'a2b_uu'
536	LOAD_FAST         's'
539	LOAD_FAST         'nbytes'
542	SLICE+2           None
543	CALL_FUNCTION_1   None
546	STORE_FAST        'data'

549	LOAD_FAST         'quiet'
552	JUMP_IF_TRUE      '584'

555	LOAD_GLOBAL       'sys'
558	LOAD_ATTR         'stderr'
561	LOAD_ATTR         'write'
564	LOAD_CONST        'Warning: %s\n'
567	LOAD_GLOBAL       'str'
570	LOAD_FAST         'v'
573	CALL_FUNCTION_1   None
576	BINARY_MODULO     None
577	CALL_FUNCTION_1   None
580	POP_TOP           None
581	JUMP_ABSOLUTE     '588'
584	JUMP_FORWARD      '588'
587	END_FINALLY       None
588_0	COME_FROM         '473'
588_1	COME_FROM         '587'

588	LOAD_FAST         'out_file'
591	LOAD_ATTR         'write'
594	LOAD_FAST         'data'
597	CALL_FUNCTION_1   None
600	POP_TOP           None

601	LOAD_FAST         'in_file'
604	LOAD_ATTR         'readline'
607	CALL_FUNCTION_0   None
610	STORE_FAST        's'
613	JUMP_BACK         '430'
616	POP_BLOCK         None
617_0	COME_FROM         '427'

617	LOAD_FAST         's'
620	JUMP_IF_TRUE      '635'

623	LOAD_GLOBAL       'Error'
626	LOAD_CONST        'Truncated input file'
629	RAISE_VARARGS_2   None
632	JUMP_FORWARD      '635'
635_0	COME_FROM         '632'
635	LOAD_CONST        None
638	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 209

