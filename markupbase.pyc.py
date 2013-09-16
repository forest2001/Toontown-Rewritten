# 2013.08.22 22:13:10 Pacific Daylight Time
# Embedded file name: markupbase
import re
_declname_match = re.compile('[a-zA-Z][-_.a-zA-Z0-9]*\\s*').match
_declstringlit_match = re.compile('(\\\'[^\\\']*\\\'|"[^"]*")\\s*').match
_commentclose = re.compile('--\\s*>')
_markedsectionclose = re.compile(']\\s*]\\s*>')
_msmarkedsectionclose = re.compile(']\\s*>')
del re

class ParserBase():
    __module__ = __name__

    def __init__(self):
        if self.__class__ is ParserBase:
            raise RuntimeError('markupbase.ParserBase must be subclassed')

    def error(self, message):
        raise NotImplementedError('subclasses of ParserBase must override error()')

    def reset(self):
        self.lineno = 1
        self.offset = 0

    def getpos(self):
        return (self.lineno, self.offset)

    def updatepos(self, i, j):
        if i >= j:
            return j
        rawdata = self.rawdata
        nlines = rawdata.count('\n', i, j)
        if nlines:
            self.lineno = self.lineno + nlines
            pos = rawdata.rindex('\n', i, j)
            self.offset = j - (pos + 1)
        else:
            self.offset = self.offset + j - i
        return j

    _decl_otherchars = ''

    def parse_declaration(self, i):
        rawdata = self.rawdata
        j = i + 2
        if rawdata[j:j + 1] in ('-', ''):
            return -1
        n = len(rawdata)
        if rawdata[j:j + 1] == '--':
            return self.parse_comment(i)
        elif rawdata[j] == '[':
            return self.parse_marked_section(i)
        else:
            decltype, j = self._scan_name(j, i)
        if j < 0:
            return j
        if decltype == 'doctype':
            self._decl_otherchars = ''
        while j < n:
            c = rawdata[j]
            if c == '>':
                data = rawdata[i + 2:j]
                if decltype == 'doctype':
                    self.handle_decl(data)
                else:
                    self.unknown_decl(data)
                return j + 1
            if c in '"\'':
                m = _declstringlit_match(rawdata, j)
                if not m:
                    return -1
                j = m.end()
            elif c in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ':
                name, j = self._scan_name(j, i)
            elif c in self._decl_otherchars:
                j = j + 1
            elif c == '[':
                if decltype == 'doctype':
                    j = self._parse_doctype_subset(j + 1, i)
                elif decltype in ('attlist', 'linktype', 'link', 'element'):
                    self.error("unsupported '[' char in %s declaration" % decltype)
                else:
                    self.error("unexpected '[' char in declaration")
            else:
                self.error('unexpected %r char in declaration' % rawdata[j])
            if j < 0:
                return j

        return -1

    def parse_marked_section(self, i, report = 1):
        rawdata = self.rawdata
        sectName, j = self._scan_name(i + 3, i)
        if j < 0:
            return j
        if sectName in ('temp', 'cdata', 'ignore', 'include', 'rcdata'):
            match = _markedsectionclose.search(rawdata, i + 3)
        elif sectName in ('if', 'else', 'endif'):
            match = _msmarkedsectionclose.search(rawdata, i + 3)
        else:
            self.error('unknown status keyword %r in marked section' % rawdata[i + 3:j])
        if not match:
            return -1
        if report:
            j = match.start(0)
            self.unknown_decl(rawdata[i + 3:j])
        return match.end(0)

    def parse_comment(self, i, report = 1):
        rawdata = self.rawdata
        if rawdata[i:i + 4] != '<!--':
            self.error('unexpected call to parse_comment()')
        match = _commentclose.search(rawdata, i + 4)
        if not match:
            return -1
        if report:
            j = match.start(0)
            self.handle_comment(rawdata[i + 4:j])
        return match.end(0)

    def _parse_doctype_subset(self, i, declstartpos):
        rawdata = self.rawdata
        n = len(rawdata)
        j = i
        while j < n:
            c = rawdata[j]
            if c == '<':
                s = rawdata[j:j + 2]
                if s == '<':
                    return -1
                if s != '<!':
                    self.updatepos(declstartpos, j + 1)
                    self.error('unexpected char in internal subset (in %r)' % s)
                if j + 2 == n:
                    return -1
                if j + 4 > n:
                    return -1
                if rawdata[j:j + 4] == '<!--':
                    j = self.parse_comment(j, report=0)
                    if j < 0:
                        return j
                    continue
                name, j = self._scan_name(j + 2, declstartpos)
                if j == -1:
                    return -1
                if name not in ('attlist', 'element', 'entity', 'notation'):
                    self.updatepos(declstartpos, j + 2)
                    self.error('unknown declaration %r in internal subset' % name)
                meth = getattr(self, '_parse_doctype_' + name)
                j = meth(j, declstartpos)
                if j < 0:
                    return j
            elif c == '%':
                if j + 1 == n:
                    return -1
                s, j = self._scan_name(j + 1, declstartpos)
                if j < 0:
                    return j
                if rawdata[j] == ';':
                    j = j + 1
            elif c == ']':
                j = j + 1
                while j < n and rawdata[j].isspace():
                    j = j + 1

                if j < n:
                    if rawdata[j] == '>':
                        return j
                    self.updatepos(declstartpos, j)
                    self.error('unexpected char after internal subset')
                else:
                    return -1
            elif c.isspace():
                j = j + 1
            else:
                self.updatepos(declstartpos, j)
                self.error('unexpected char %r in internal subset' % c)

        return -1

    def _parse_doctype_element(self, i, declstartpos):
        name, j = self._scan_name(i, declstartpos)
        if j == -1:
            return -1
        rawdata = self.rawdata
        if '>' in rawdata[j:]:
            return rawdata.find('>', j) + 1
        return -1

    def _parse_doctype_attlist--- This code section failed: ---

0	LOAD_FAST         'self'
3	LOAD_ATTR         'rawdata'
6	STORE_FAST        'rawdata'

9	LOAD_FAST         'self'
12	LOAD_ATTR         '_scan_name'
15	LOAD_FAST         'i'
18	LOAD_FAST         'declstartpos'
21	CALL_FUNCTION_2   None
24	UNPACK_SEQUENCE_2 None
27	STORE_FAST        'name'
30	STORE_FAST        'j'

33	LOAD_FAST         'rawdata'
36	LOAD_FAST         'j'
39	LOAD_FAST         'j'
42	LOAD_CONST        1
45	BINARY_ADD        None
46	SLICE+3           None
47	STORE_FAST        'c'

50	LOAD_FAST         'c'
53	LOAD_CONST        ''
56	COMPARE_OP        '=='
59	JUMP_IF_FALSE     '69'

62	LOAD_CONST        -1
65	RETURN_VALUE      None
66	JUMP_FORWARD      '69'
69_0	COME_FROM         '66'

69	LOAD_FAST         'c'
72	LOAD_CONST        '>'
75	COMPARE_OP        '=='
78	JUMP_IF_FALSE     '92'

81	LOAD_FAST         'j'
84	LOAD_CONST        1
87	BINARY_ADD        None
88	RETURN_VALUE      None
89	JUMP_FORWARD      '92'
92_0	COME_FROM         '89'

92	SETUP_LOOP        '572'

95	LOAD_FAST         'self'
98	LOAD_ATTR         '_scan_name'
101	LOAD_FAST         'j'
104	LOAD_FAST         'declstartpos'
107	CALL_FUNCTION_2   None
110	UNPACK_SEQUENCE_2 None
113	STORE_FAST        'name'
116	STORE_FAST        'j'

119	LOAD_FAST         'j'
122	LOAD_CONST        0
125	COMPARE_OP        '<'
128	JUMP_IF_FALSE     '138'

131	LOAD_FAST         'j'
134	RETURN_VALUE      None
135	JUMP_FORWARD      '138'
138_0	COME_FROM         '135'

138	LOAD_FAST         'rawdata'
141	LOAD_FAST         'j'
144	LOAD_FAST         'j'
147	LOAD_CONST        1
150	BINARY_ADD        None
151	SLICE+3           None
152	STORE_FAST        'c'

155	LOAD_FAST         'c'
158	LOAD_CONST        ''
161	COMPARE_OP        '=='
164	JUMP_IF_FALSE     '174'

167	LOAD_CONST        -1
170	RETURN_VALUE      None
171	JUMP_FORWARD      '174'
174_0	COME_FROM         '171'

174	LOAD_FAST         'c'
177	LOAD_CONST        '('
180	COMPARE_OP        '=='
183	JUMP_IF_FALSE     '291'

186	LOAD_CONST        ')'
189	LOAD_FAST         'rawdata'
192	LOAD_FAST         'j'
195	SLICE+1           None
196	COMPARE_OP        'in'
199	JUMP_IF_FALSE     '227'

202	LOAD_FAST         'rawdata'
205	LOAD_ATTR         'find'
208	LOAD_CONST        ')'
211	LOAD_FAST         'j'
214	CALL_FUNCTION_2   None
217	LOAD_CONST        1
220	BINARY_ADD        None
221	STORE_FAST        'j'
224	JUMP_FORWARD      '231'

227	LOAD_CONST        -1
230	RETURN_VALUE      None
231_0	COME_FROM         '224'

231	SETUP_LOOP        '271'
234	LOAD_FAST         'rawdata'
237	LOAD_FAST         'j'
240	LOAD_FAST         'j'
243	LOAD_CONST        1
246	BINARY_ADD        None
247	SLICE+3           None
248	LOAD_ATTR         'isspace'
251	CALL_FUNCTION_0   None
254	JUMP_IF_FALSE     '270'

257	LOAD_FAST         'j'
260	LOAD_CONST        1
263	BINARY_ADD        None
264	STORE_FAST        'j'
267	JUMP_BACK         '234'
270	POP_BLOCK         None
271_0	COME_FROM         '231'

271	LOAD_FAST         'rawdata'
274	LOAD_FAST         'j'
277	SLICE+1           None
278	JUMP_IF_TRUE      '288'

281	LOAD_CONST        -1
284	RETURN_VALUE      None
285	JUMP_ABSOLUTE     '315'
288	JUMP_FORWARD      '315'

291	LOAD_FAST         'self'
294	LOAD_ATTR         '_scan_name'
297	LOAD_FAST         'j'
300	LOAD_FAST         'declstartpos'
303	CALL_FUNCTION_2   None
306	UNPACK_SEQUENCE_2 None
309	STORE_FAST        'name'
312	STORE_FAST        'j'
315_0	COME_FROM         '288'

315	LOAD_FAST         'rawdata'
318	LOAD_FAST         'j'
321	LOAD_FAST         'j'
324	LOAD_CONST        1
327	BINARY_ADD        None
328	SLICE+3           None
329	STORE_FAST        'c'

332	LOAD_FAST         'c'
335	JUMP_IF_TRUE      '345'

338	LOAD_CONST        -1
341	RETURN_VALUE      None
342	JUMP_FORWARD      '345'
345_0	COME_FROM         '342'

345	LOAD_FAST         'c'
348	LOAD_CONST        '\'"'
351	COMPARE_OP        'in'
354	JUMP_IF_FALSE     '430'

357	LOAD_GLOBAL       '_declstringlit_match'
360	LOAD_FAST         'rawdata'
363	LOAD_FAST         'j'
366	CALL_FUNCTION_2   None
369	STORE_FAST        'm'

372	LOAD_FAST         'm'
375	JUMP_IF_FALSE     '393'

378	LOAD_FAST         'm'
381	LOAD_ATTR         'end'
384	CALL_FUNCTION_0   None
387	STORE_FAST        'j'
390	JUMP_FORWARD      '397'

393	LOAD_CONST        -1
396	RETURN_VALUE      None
397_0	COME_FROM         '390'

397	LOAD_FAST         'rawdata'
400	LOAD_FAST         'j'
403	LOAD_FAST         'j'
406	LOAD_CONST        1
409	BINARY_ADD        None
410	SLICE+3           None
411	STORE_FAST        'c'

414	LOAD_FAST         'c'
417	JUMP_IF_TRUE      '427'

420	LOAD_CONST        -1
423	RETURN_VALUE      None
424	JUMP_ABSOLUTE     '430'
427	JUMP_FORWARD      '430'
430_0	COME_FROM         '427'

430	LOAD_FAST         'c'
433	LOAD_CONST        '#'
436	COMPARE_OP        '=='
439	JUMP_IF_FALSE     '545'

442	LOAD_FAST         'rawdata'
445	LOAD_FAST         'j'
448	SLICE+1           None
449	LOAD_CONST        '#'
452	COMPARE_OP        '=='
455	JUMP_IF_FALSE     '465'

458	LOAD_CONST        -1
461	RETURN_VALUE      None
462	JUMP_FORWARD      '465'
465_0	COME_FROM         '462'

465	LOAD_FAST         'self'
468	LOAD_ATTR         '_scan_name'
471	LOAD_FAST         'j'
474	LOAD_CONST        1
477	BINARY_ADD        None
478	LOAD_FAST         'declstartpos'
481	CALL_FUNCTION_2   None
484	UNPACK_SEQUENCE_2 None
487	STORE_FAST        'name'
490	STORE_FAST        'j'

493	LOAD_FAST         'j'
496	LOAD_CONST        0
499	COMPARE_OP        '<'
502	JUMP_IF_FALSE     '512'

505	LOAD_FAST         'j'
508	RETURN_VALUE      None
509	JUMP_FORWARD      '512'
512_0	COME_FROM         '509'

512	LOAD_FAST         'rawdata'
515	LOAD_FAST         'j'
518	LOAD_FAST         'j'
521	LOAD_CONST        1
524	BINARY_ADD        None
525	SLICE+3           None
526	STORE_FAST        'c'

529	LOAD_FAST         'c'
532	JUMP_IF_TRUE      '542'

535	LOAD_CONST        -1
538	RETURN_VALUE      None
539	JUMP_ABSOLUTE     '545'
542	JUMP_FORWARD      '545'
545_0	COME_FROM         '542'

545	LOAD_FAST         'c'
548	LOAD_CONST        '>'
551	COMPARE_OP        '=='
554	JUMP_IF_FALSE     '568'

557	LOAD_FAST         'j'
560	LOAD_CONST        1
563	BINARY_ADD        None
564	RETURN_VALUE      None
565	JUMP_BACK         '95'
568	JUMP_BACK         '95'
571	POP_BLOCK         None
572_0	COME_FROM         '92'

Syntax error at or near `POP_BLOCK' token at offset 571

    def _parse_doctype_notation--- This code section failed: ---

0	LOAD_FAST         'self'
3	LOAD_ATTR         '_scan_name'
6	LOAD_FAST         'i'
9	LOAD_FAST         'declstartpos'
12	CALL_FUNCTION_2   None
15	UNPACK_SEQUENCE_2 None
18	STORE_FAST        'name'
21	STORE_FAST        'j'

24	LOAD_FAST         'j'
27	LOAD_CONST        0
30	COMPARE_OP        '<'
33	JUMP_IF_FALSE     '43'

36	LOAD_FAST         'j'
39	RETURN_VALUE      None
40	JUMP_FORWARD      '43'
43_0	COME_FROM         '40'

43	LOAD_FAST         'self'
46	LOAD_ATTR         'rawdata'
49	STORE_FAST        'rawdata'

52	SETUP_LOOP        '210'

55	LOAD_FAST         'rawdata'
58	LOAD_FAST         'j'
61	LOAD_FAST         'j'
64	LOAD_CONST        1
67	BINARY_ADD        None
68	SLICE+3           None
69	STORE_FAST        'c'

72	LOAD_FAST         'c'
75	JUMP_IF_TRUE      '85'

78	LOAD_CONST        -1
81	RETURN_VALUE      None
82	JUMP_FORWARD      '85'
85_0	COME_FROM         '82'

85	LOAD_FAST         'c'
88	LOAD_CONST        '>'
91	COMPARE_OP        '=='
94	JUMP_IF_FALSE     '108'

97	LOAD_FAST         'j'
100	LOAD_CONST        1
103	BINARY_ADD        None
104	RETURN_VALUE      None
105	JUMP_FORWARD      '108'
108_0	COME_FROM         '105'

108	LOAD_FAST         'c'
111	LOAD_CONST        '\'"'
114	COMPARE_OP        'in'
117	JUMP_IF_FALSE     '163'

120	LOAD_GLOBAL       '_declstringlit_match'
123	LOAD_FAST         'rawdata'
126	LOAD_FAST         'j'
129	CALL_FUNCTION_2   None
132	STORE_FAST        'm'

135	LOAD_FAST         'm'
138	JUMP_IF_TRUE      '148'

141	LOAD_CONST        -1
144	RETURN_VALUE      None
145	JUMP_FORWARD      '148'
148_0	COME_FROM         '145'

148	LOAD_FAST         'm'
151	LOAD_ATTR         'end'
154	CALL_FUNCTION_0   None
157	STORE_FAST        'j'
160	JUMP_BACK         '55'

163	LOAD_FAST         'self'
166	LOAD_ATTR         '_scan_name'
169	LOAD_FAST         'j'
172	LOAD_FAST         'declstartpos'
175	CALL_FUNCTION_2   None
178	UNPACK_SEQUENCE_2 None
181	STORE_FAST        'name'
184	STORE_FAST        'j'

187	LOAD_FAST         'j'
190	LOAD_CONST        0
193	COMPARE_OP        '<'
196	JUMP_IF_FALSE     '206'

199	LOAD_FAST         'j'
202	RETURN_VALUE      None
203	JUMP_BACK         '55'
206	JUMP_BACK         '55'
209	POP_BLOCK         None
210_0	COME_FROM         '52'

Syntax error at or near `POP_BLOCK' token at offset 209

    def _parse_doctype_entity--- This code section failed: ---

0	LOAD_FAST         'self'
3	LOAD_ATTR         'rawdata'
6	STORE_FAST        'rawdata'

9	LOAD_FAST         'rawdata'
12	LOAD_FAST         'i'
15	LOAD_FAST         'i'
18	LOAD_CONST        1
21	BINARY_ADD        None
22	SLICE+3           None
23	LOAD_CONST        '%'
26	COMPARE_OP        '=='
29	JUMP_IF_FALSE     '108'

32	LOAD_FAST         'i'
35	LOAD_CONST        1
38	BINARY_ADD        None
39	STORE_FAST        'j'

42	SETUP_LOOP        '114'

45	LOAD_FAST         'rawdata'
48	LOAD_FAST         'j'
51	LOAD_FAST         'j'
54	LOAD_CONST        1
57	BINARY_ADD        None
58	SLICE+3           None
59	STORE_FAST        'c'

62	LOAD_FAST         'c'
65	JUMP_IF_TRUE      '75'

68	LOAD_CONST        -1
71	RETURN_VALUE      None
72	JUMP_FORWARD      '75'
75_0	COME_FROM         '72'

75	LOAD_FAST         'c'
78	LOAD_ATTR         'isspace'
81	CALL_FUNCTION_0   None
84	JUMP_IF_FALSE     '100'

87	LOAD_FAST         'j'
90	LOAD_CONST        1
93	BINARY_ADD        None
94	STORE_FAST        'j'
97	JUMP_BACK         '45'

100	BREAK_LOOP        None
101	JUMP_BACK         '45'
104	POP_BLOCK         None
105_0	COME_FROM         '42'
105	JUMP_FORWARD      '114'

108	LOAD_FAST         'i'
111	STORE_FAST        'j'
114_0	COME_FROM         '105'

114	LOAD_FAST         'self'
117	LOAD_ATTR         '_scan_name'
120	LOAD_FAST         'j'
123	LOAD_FAST         'declstartpos'
126	CALL_FUNCTION_2   None
129	UNPACK_SEQUENCE_2 None
132	STORE_FAST        'name'
135	STORE_FAST        'j'

138	LOAD_FAST         'j'
141	LOAD_CONST        0
144	COMPARE_OP        '<'
147	JUMP_IF_FALSE     '157'

150	LOAD_FAST         'j'
153	RETURN_VALUE      None
154	JUMP_FORWARD      '157'
157_0	COME_FROM         '154'

157	SETUP_LOOP        '318'

160	LOAD_FAST         'self'
163	LOAD_ATTR         'rawdata'
166	LOAD_FAST         'j'
169	LOAD_FAST         'j'
172	LOAD_CONST        1
175	BINARY_ADD        None
176	SLICE+3           None
177	STORE_FAST        'c'

180	LOAD_FAST         'c'
183	JUMP_IF_TRUE      '193'

186	LOAD_CONST        -1
189	RETURN_VALUE      None
190	JUMP_FORWARD      '193'
193_0	COME_FROM         '190'

193	LOAD_FAST         'c'
196	LOAD_CONST        '\'"'
199	COMPARE_OP        'in'
202	JUMP_IF_FALSE     '248'

205	LOAD_GLOBAL       '_declstringlit_match'
208	LOAD_FAST         'rawdata'
211	LOAD_FAST         'j'
214	CALL_FUNCTION_2   None
217	STORE_FAST        'm'

220	LOAD_FAST         'm'
223	JUMP_IF_FALSE     '241'

226	LOAD_FAST         'm'
229	LOAD_ATTR         'end'
232	CALL_FUNCTION_0   None
235	STORE_FAST        'j'
238	JUMP_ABSOLUTE     '314'

241	LOAD_CONST        -1
244	RETURN_VALUE      None
245	JUMP_BACK         '160'

248	LOAD_FAST         'c'
251	LOAD_CONST        '>'
254	COMPARE_OP        '=='
257	JUMP_IF_FALSE     '271'

260	LOAD_FAST         'j'
263	LOAD_CONST        1
266	BINARY_ADD        None
267	RETURN_VALUE      None
268	JUMP_BACK         '160'

271	LOAD_FAST         'self'
274	LOAD_ATTR         '_scan_name'
277	LOAD_FAST         'j'
280	LOAD_FAST         'declstartpos'
283	CALL_FUNCTION_2   None
286	UNPACK_SEQUENCE_2 None
289	STORE_FAST        'name'
292	STORE_FAST        'j'

295	LOAD_FAST         'j'
298	LOAD_CONST        0
301	COMPARE_OP        '<'
304	JUMP_IF_FALSE     '314'

307	LOAD_FAST         'j'
310	RETURN_VALUE      None
311	JUMP_BACK         '160'
314	JUMP_BACK         '160'
317	POP_BLOCK         None
318_0	COME_FROM         '157'

Syntax error at or near `POP_BLOCK' token at offset 104

    def _scan_name(self, i, declstartpos):
        rawdata = self.rawdata
        n = len(rawdata)
        if i == n:
            return (None, -1)
        m = _declname_match(rawdata, i)
        if m:
            s = m.group()
            name = s.strip()
            if i + len(s) == n:
                return (None, -1)
            return (name.lower(), m.end())
        else:
            self.updatepos(declstartpos, i)
            self.error('expected name token at %r' % rawdata[declstartpos:declstartpos + 20])
        return None

    def unknown_decl(self, data):
        pass# decompiled 0 files: 0 okay, 1 failed, 0 verify failed
# 2013.08.22 22:13:10 Pacific Daylight Time

# Can't uncompyle C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\markupbase.pyc
Traceback (most recent call last):
  File "C:\python27\lib\uncompyle2\__init__.py", line 206, in main
    uncompyle_file(infile, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 143, in uncompyle_file
    uncompyle(version, co, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 132, in uncompyle
    raise walk.ERROR
ParserError: --- This code section failed: ---

0	LOAD_FAST         'self'
3	LOAD_ATTR         'rawdata'
6	STORE_FAST        'rawdata'

9	LOAD_FAST         'rawdata'
12	LOAD_FAST         'i'
15	LOAD_FAST         'i'
18	LOAD_CONST        1
21	BINARY_ADD        None
22	SLICE+3           None
23	LOAD_CONST        '%'
26	COMPARE_OP        '=='
29	JUMP_IF_FALSE     '108'

32	LOAD_FAST         'i'
35	LOAD_CONST        1
38	BINARY_ADD        None
39	STORE_FAST        'j'

42	SETUP_LOOP        '114'

45	LOAD_FAST         'rawdata'
48	LOAD_FAST         'j'
51	LOAD_FAST         'j'
54	LOAD_CONST        1
57	BINARY_ADD        None
58	SLICE+3           None
59	STORE_FAST        'c'

62	LOAD_FAST         'c'
65	JUMP_IF_TRUE      '75'

68	LOAD_CONST        -1
71	RETURN_VALUE      None
72	JUMP_FORWARD      '75'
75_0	COME_FROM         '72'

75	LOAD_FAST         'c'
78	LOAD_ATTR         'isspace'
81	CALL_FUNCTION_0   None
84	JUMP_IF_FALSE     '100'

87	LOAD_FAST         'j'
90	LOAD_CONST        1
93	BINARY_ADD        None
94	STORE_FAST        'j'
97	JUMP_BACK         '45'

100	BREAK_LOOP        None
101	JUMP_BACK         '45'
104	POP_BLOCK         None
105_0	COME_FROM         '42'
105	JUMP_FORWARD      '114'

108	LOAD_FAST         'i'
111	STORE_FAST        'j'
114_0	COME_FROM         '105'

114	LOAD_FAST         'self'
117	LOAD_ATTR         '_scan_name'
120	LOAD_FAST         'j'
123	LOAD_FAST         'declstartpos'
126	CALL_FUNCTION_2   None
129	UNPACK_SEQUENCE_2 None
132	STORE_FAST        'name'
135	STORE_FAST        'j'

138	LOAD_FAST         'j'
141	LOAD_CONST        0
144	COMPARE_OP        '<'
147	JUMP_IF_FALSE     '157'

150	LOAD_FAST         'j'
153	RETURN_VALUE      None
154	JUMP_FORWARD      '157'
157_0	COME_FROM         '154'

157	SETUP_LOOP        '318'

160	LOAD_FAST         'self'
163	LOAD_ATTR         'rawdata'
166	LOAD_FAST         'j'
169	LOAD_FAST         'j'
172	LOAD_CONST        1
175	BINARY_ADD        None
176	SLICE+3           None
177	STORE_FAST        'c'

180	LOAD_FAST         'c'
183	JUMP_IF_TRUE      '193'

186	LOAD_CONST        -1
189	RETURN_VALUE      None
190	JUMP_FORWARD      '193'
193_0	COME_FROM         '190'

193	LOAD_FAST         'c'
196	LOAD_CONST        '\'"'
199	COMPARE_OP        'in'
202	JUMP_IF_FALSE     '248'

205	LOAD_GLOBAL       '_declstringlit_match'
208	LOAD_FAST         'rawdata'
211	LOAD_FAST         'j'
214	CALL_FUNCTION_2   None
217	STORE_FAST        'm'

220	LOAD_FAST         'm'
223	JUMP_IF_FALSE     '241'

226	LOAD_FAST         'm'
229	LOAD_ATTR         'end'
232	CALL_FUNCTION_0   None
235	STORE_FAST        'j'
238	JUMP_ABSOLUTE     '314'

241	LOAD_CONST        -1
244	RETURN_VALUE      None
245	JUMP_BACK         '160'

248	LOAD_FAST         'c'
251	LOAD_CONST        '>'
254	COMPARE_OP        '=='
257	JUMP_IF_FALSE     '271'

260	LOAD_FAST         'j'
263	LOAD_CONST        1
266	BINARY_ADD        None
267	RETURN_VALUE      None
268	JUMP_BACK         '160'

271	LOAD_FAST         'self'
274	LOAD_ATTR         '_scan_name'
277	LOAD_FAST         'j'
280	LOAD_FAST         'declstartpos'
283	CALL_FUNCTION_2   None
286	UNPACK_SEQUENCE_2 None
289	STORE_FAST        'name'
292	STORE_FAST        'j'

295	LOAD_FAST         'j'
298	LOAD_CONST        0
301	COMPARE_OP        '<'
304	JUMP_IF_FALSE     '314'

307	LOAD_FAST         'j'
310	RETURN_VALUE      None
311	JUMP_BACK         '160'
314	JUMP_BACK         '160'
317	POP_BLOCK         None
318_0	COME_FROM         '157'

Syntax error at or near `POP_BLOCK' token at offset 104

