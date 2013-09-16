# 2013.08.22 22:13:31 Pacific Daylight Time
# Embedded file name: sre_parse
import sys
from sre_constants import *
SPECIAL_CHARS = '.\\[{()*+?^$|'
REPEAT_CHARS = '*+?{'
DIGITS = tuple('0123456789')
OCTDIGITS = tuple('01234567')
HEXDIGITS = tuple('0123456789abcdefABCDEF')
WHITESPACE = tuple(' \t\n\r\x0b\x0c')
ESCAPES = {'\\a': (LITERAL, ord('\x07')),
 '\\b': (LITERAL, ord('\x08')),
 '\\f': (LITERAL, ord('\x0c')),
 '\\n': (LITERAL, ord('\n')),
 '\\r': (LITERAL, ord('\r')),
 '\\t': (LITERAL, ord('\t')),
 '\\v': (LITERAL, ord('\x0b')),
 '\\\\': (LITERAL, ord('\\'))}
CATEGORIES = {'\\A': (AT, AT_BEGINNING_STRING),
 '\\b': (AT, AT_BOUNDARY),
 '\\B': (AT, AT_NON_BOUNDARY),
 '\\d': (IN, [(CATEGORY, CATEGORY_DIGIT)]),
 '\\D': (IN, [(CATEGORY, CATEGORY_NOT_DIGIT)]),
 '\\s': (IN, [(CATEGORY, CATEGORY_SPACE)]),
 '\\S': (IN, [(CATEGORY, CATEGORY_NOT_SPACE)]),
 '\\w': (IN, [(CATEGORY, CATEGORY_WORD)]),
 '\\W': (IN, [(CATEGORY, CATEGORY_NOT_WORD)]),
 '\\Z': (AT, AT_END_STRING)}
FLAGS = {'i': SRE_FLAG_IGNORECASE,
 'L': SRE_FLAG_LOCALE,
 'm': SRE_FLAG_MULTILINE,
 's': SRE_FLAG_DOTALL,
 'x': SRE_FLAG_VERBOSE,
 't': SRE_FLAG_TEMPLATE,
 'u': SRE_FLAG_UNICODE}

class Pattern():
    __module__ = __name__

    def __init__(self):
        self.flags = 0
        self.open = []
        self.groups = 1
        self.groupdict = {}

    def opengroup(self, name = None):
        gid = self.groups
        self.groups = gid + 1
        if name is not None:
            ogid = self.groupdict.get(name, None)
            if ogid is not None:
                raise error, 'redefinition of group name %s as group %d; was group %d' % (repr(name), gid, ogid)
            self.groupdict[name] = gid
        self.open.append(gid)
        return gid

    def closegroup(self, gid):
        self.open.remove(gid)

    def checkgroup(self, gid):
        return gid < self.groups and gid not in self.open


class SubPattern():
    __module__ = __name__

    def __init__(self, pattern, data = None):
        self.pattern = pattern
        if data is None:
            data = []
        self.data = data
        self.width = None
        return

    def dump(self, level = 0):
        nl = 1
        seqtypes = (type(()), type([]))
        for op, av in self.data:
            print level * '  ' + op,
            nl = 0
            if op == 'in':
                print
                nl = 1
                for op, a in av:
                    print (level + 1) * '  ' + op, a

            elif op == 'branch':
                print
                nl = 1
                i = 0
                for a in av[1]:
                    if i > 0:
                        print level * '  ' + 'or'
                    a.dump(level + 1)
                    nl = 1
                    i = i + 1

            elif type(av) in seqtypes:
                for a in av:
                    if isinstance(a, SubPattern):
                        if not nl:
                            print
                        a.dump(level + 1)
                        nl = 1
                    else:
                        print a,
                        nl = 0

            else:
                print av,
                nl = 0
            if not nl:
                print

    def __repr__(self):
        return repr(self.data)

    def __len__(self):
        return len(self.data)

    def __delitem__(self, index):
        del self.data[index]

    def __getitem__(self, index):
        return self.data[index]

    def __setitem__(self, index, code):
        self.data[index] = code

    def __getslice__(self, start, stop):
        return SubPattern(self.pattern, self.data[start:stop])

    def insert(self, index, code):
        self.data.insert(index, code)

    def append(self, code):
        self.data.append(code)

    def getwidth(self):
        if self.width:
            return self.width
        lo = hi = 0L
        UNITCODES = (ANY,
         RANGE,
         IN,
         LITERAL,
         NOT_LITERAL,
         CATEGORY)
        REPEATCODES = (MIN_REPEAT, MAX_REPEAT)
        for op, av in self.data:
            if op is BRANCH:
                i = sys.maxint
                j = 0
                for av in av[1]:
                    l, h = av.getwidth()
                    i = min(i, l)
                    j = max(j, h)

                lo = lo + i
                hi = hi + j
            elif op is CALL:
                i, j = av.getwidth()
                lo = lo + i
                hi = hi + j
            elif op is SUBPATTERN:
                i, j = av[1].getwidth()
                lo = lo + i
                hi = hi + j
            elif op in REPEATCODES:
                i, j = av[2].getwidth()
                lo = lo + long(i) * av[0]
                hi = hi + long(j) * av[1]
            elif op in UNITCODES:
                lo = lo + 1
                hi = hi + 1
            elif op == SUCCESS:
                break

        self.width = (int(min(lo, sys.maxint)), int(min(hi, sys.maxint)))
        return self.width


class Tokenizer():
    __module__ = __name__

    def __init__(self, string):
        self.string = string
        self.index = 0
        self.__next()

    def __next(self):
        if self.index >= len(self.string):
            self.next = None
            return
        char = self.string[self.index]
        if char[0] == '\\':
            try:
                c = self.string[self.index + 1]
            except IndexError:
                raise error, 'bogus escape (end of line)'

            char = char + c
        self.index = self.index + len(char)
        self.next = char
        return

    def match(self, char, skip = 1):
        if char == self.next:
            if skip:
                self.__next()
            return 1
        return 0

    def get(self):
        this = self.next
        self.__next()
        return this

    def tell(self):
        return (self.index, self.next)

    def seek(self, index):
        self.index, self.next = index


def isident(char):
    return 'a' <= char <= 'z' or 'A' <= char <= 'Z' or char == '_'


def isdigit(char):
    return '0' <= char <= '9'


def isname(name):
    if not isident(name[0]):
        return False
    for char in name[1:]:
        if not isident(char) and not isdigit(char):
            return False

    return True


def _class_escape(source, escape):
    code = ESCAPES.get(escape)
    if code:
        return code
    code = CATEGORIES.get(escape)
    if code:
        return code
    try:
        c = escape[1:2]
        if c == 'x':
            while source.next in HEXDIGITS and len(escape) < 4:
                escape = escape + source.get()

            escape = escape[2:]
            if len(escape) != 2:
                raise error, 'bogus escape: %s' % repr('\\' + escape)
            return (LITERAL, int(escape, 16) & 255)
        elif c in OCTDIGITS:
            while source.next in OCTDIGITS and len(escape) < 4:
                escape = escape + source.get()

            escape = escape[1:]
            return (LITERAL, int(escape, 8) & 255)
        elif c in DIGITS:
            raise error, 'bogus escape: %s' % repr(escape)
        if len(escape) == 2:
            return (LITERAL, ord(escape[1]))
    except ValueError:
        pass

    raise error, 'bogus escape: %s' % repr(escape)


def _escape(source, escape, state):
    code = CATEGORIES.get(escape)
    if code:
        return code
    code = ESCAPES.get(escape)
    if code:
        return code
    try:
        c = escape[1:2]
        if c == 'x':
            while source.next in HEXDIGITS and len(escape) < 4:
                escape = escape + source.get()

            if len(escape) != 4:
                raise ValueError
            return (LITERAL, int(escape[2:], 16) & 255)
        elif c == '0':
            while source.next in OCTDIGITS and len(escape) < 4:
                escape = escape + source.get()

            return (LITERAL, int(escape[1:], 8) & 255)
        elif c in DIGITS:
            if source.next in DIGITS:
                escape = escape + source.get()
                if escape[1] in OCTDIGITS and escape[2] in OCTDIGITS and source.next in OCTDIGITS:
                    escape = escape + source.get()
                    return (LITERAL, int(escape[1:], 8) & 255)
            group = int(escape[1:])
            if group < state.groups:
                if not state.checkgroup(group):
                    raise error, 'cannot refer to open group'
                return (GROUPREF, group)
            raise ValueError
        if len(escape) == 2:
            return (LITERAL, ord(escape[1]))
    except ValueError:
        pass

    raise error, 'bogus escape: %s' % repr(escape)


def _parse_sub--- This code section failed: ---

0	BUILD_LIST_0      None
3	STORE_FAST        'items'

6	LOAD_FAST         'items'
9	LOAD_ATTR         'append'
12	STORE_FAST        'itemsappend'

15	LOAD_FAST         'source'
18	LOAD_ATTR         'match'
21	STORE_FAST        'sourcematch'

24	SETUP_LOOP        '116'

27	LOAD_FAST         'itemsappend'
30	LOAD_GLOBAL       '_parse'
33	LOAD_FAST         'source'
36	LOAD_FAST         'state'
39	CALL_FUNCTION_2   None
42	CALL_FUNCTION_1   None
45	POP_TOP           None

46	LOAD_FAST         'sourcematch'
49	LOAD_CONST        '|'
52	CALL_FUNCTION_1   None
55	JUMP_IF_FALSE     '64'

58	CONTINUE          '27'
61	JUMP_FORWARD      '64'
64_0	COME_FROM         '61'

64	LOAD_FAST         'nested'
67	JUMP_IF_TRUE      '74'

70	BREAK_LOOP        None
71	JUMP_FORWARD      '74'
74_0	COME_FROM         '71'

74	LOAD_FAST         'source'
77	LOAD_ATTR         'next'
80	UNARY_NOT         None
81	JUMP_IF_TRUE      '99'
84	LOAD_FAST         'sourcematch'
87	LOAD_CONST        ')'
90	LOAD_CONST        0
93	CALL_FUNCTION_2   None
96_0	COME_FROM         '81'
96	JUMP_IF_FALSE     '103'

99	BREAK_LOOP        None
100	JUMP_BACK         '27'

103	LOAD_GLOBAL       'error'
106	LOAD_CONST        'pattern not properly closed'
109	RAISE_VARARGS_2   None
112	JUMP_BACK         '27'
115	POP_BLOCK         None
116_0	COME_FROM         '24'

116	LOAD_GLOBAL       'len'
119	LOAD_FAST         'items'
122	CALL_FUNCTION_1   None
125	LOAD_CONST        1
128	COMPARE_OP        '=='
131	JUMP_IF_FALSE     '145'

134	LOAD_FAST         'items'
137	LOAD_CONST        0
140	BINARY_SUBSCR     None
141	RETURN_VALUE      None
142	JUMP_FORWARD      '145'
145_0	COME_FROM         '142'

145	LOAD_GLOBAL       'SubPattern'
148	LOAD_FAST         'state'
151	CALL_FUNCTION_1   None
154	STORE_FAST        'subpattern'

157	LOAD_FAST         'subpattern'
160	LOAD_ATTR         'append'
163	STORE_FAST        'subpatternappend'

166	SETUP_LOOP        '289'

169	LOAD_CONST        None
172	STORE_FAST        'prefix'

175	SETUP_LOOP        '284'
178	LOAD_FAST         'items'
181	GET_ITER          None
182	FOR_ITER          '246'
185	STORE_FAST        'item'

188	LOAD_FAST         'item'
191	JUMP_IF_TRUE      '198'

194	BREAK_LOOP        None
195	JUMP_FORWARD      '198'
198_0	COME_FROM         '195'

198	LOAD_FAST         'prefix'
201	LOAD_CONST        None
204	COMPARE_OP        'is'
207	JUMP_IF_FALSE     '223'

210	LOAD_FAST         'item'
213	LOAD_CONST        0
216	BINARY_SUBSCR     None
217	STORE_FAST        'prefix'
220	JUMP_BACK         '182'

223	LOAD_FAST         'item'
226	LOAD_CONST        0
229	BINARY_SUBSCR     None
230	LOAD_FAST         'prefix'
233	COMPARE_OP        '!='
236	JUMP_IF_FALSE     '243'

239	BREAK_LOOP        None
240	JUMP_BACK         '182'
243	JUMP_BACK         '182'
246	POP_BLOCK         None

247	SETUP_LOOP        '271'
250	LOAD_FAST         'items'
253	GET_ITER          None
254	FOR_ITER          '270'
257	STORE_FAST        'item'

260	LOAD_FAST         'item'
263	LOAD_CONST        0
266	DELETE_SUBSCR     None
267	JUMP_BACK         '254'
270	POP_BLOCK         None
271_0	COME_FROM         '247'

271	LOAD_FAST         'subpatternappend'
274	LOAD_FAST         'prefix'
277	CALL_FUNCTION_1   None
280	POP_TOP           None

281	CONTINUE          '169'
284_0	COME_FROM         '175'

284	BREAK_LOOP        None
285	JUMP_BACK         '169'
288	POP_BLOCK         None
289_0	COME_FROM         '166'

289	SETUP_LOOP        '414'
292	LOAD_FAST         'items'
295	GET_ITER          None
296	FOR_ITER          '347'
299	STORE_FAST        'item'

302	LOAD_GLOBAL       'len'
305	LOAD_FAST         'item'
308	CALL_FUNCTION_1   None
311	LOAD_CONST        1
314	COMPARE_OP        '!='
317	JUMP_IF_TRUE      '340'
320	LOAD_FAST         'item'
323	LOAD_CONST        0
326	BINARY_SUBSCR     None
327	LOAD_CONST        0
330	BINARY_SUBSCR     None
331	LOAD_GLOBAL       'LITERAL'
334	COMPARE_OP        '!='
337_0	COME_FROM         '317'
337	JUMP_IF_FALSE     '344'

340	BREAK_LOOP        None
341	JUMP_BACK         '296'
344	JUMP_BACK         '296'
347	POP_BLOCK         None

348	BUILD_LIST_0      None
351	STORE_FAST        'set'

354	LOAD_FAST         'set'
357	LOAD_ATTR         'append'
360	STORE_FAST        'setappend'

363	SETUP_LOOP        '394'
366	LOAD_FAST         'items'
369	GET_ITER          None
370	FOR_ITER          '393'
373	STORE_FAST        'item'

376	LOAD_FAST         'setappend'
379	LOAD_FAST         'item'
382	LOAD_CONST        0
385	BINARY_SUBSCR     None
386	CALL_FUNCTION_1   None
389	POP_TOP           None
390	JUMP_BACK         '370'
393	POP_BLOCK         None
394_0	COME_FROM         '363'

394	LOAD_FAST         'subpatternappend'
397	LOAD_GLOBAL       'IN'
400	LOAD_FAST         'set'
403	BUILD_TUPLE_2     None
406	CALL_FUNCTION_1   None
409	POP_TOP           None

410	LOAD_FAST         'subpattern'
413	RETURN_VALUE      None
414_0	COME_FROM         '289'

414	LOAD_FAST         'subpattern'
417	LOAD_ATTR         'append'
420	LOAD_GLOBAL       'BRANCH'
423	LOAD_CONST        None
426	LOAD_FAST         'items'
429	BUILD_TUPLE_2     None
432	BUILD_TUPLE_2     None
435	CALL_FUNCTION_1   None
438	POP_TOP           None

439	LOAD_FAST         'subpattern'
442	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 115


def _parse_sub_cond(source, state, condgroup):
    item_yes = _parse(source, state)
    if source.match('|'):
        item_no = _parse(source, state)
        if source.match('|'):
            raise error, 'conditional backref with more than two branches'
    else:
        item_no = None
    if source.next and not source.match(')', 0):
        raise error, 'pattern not properly closed'
    subpattern = SubPattern(state)
    subpattern.append((GROUPREF_EXISTS, (condgroup, item_yes, item_no)))
    return subpattern


def _parse--- This code section failed: ---

0	LOAD_GLOBAL       'SubPattern'
3	LOAD_FAST         'state'
6	CALL_FUNCTION_1   None
9	STORE_FAST        'subpattern'

12	LOAD_FAST         'subpattern'
15	LOAD_ATTR         'append'
18	STORE_FAST        'subpatternappend'

21	LOAD_FAST         'source'
24	LOAD_ATTR         'get'
27	STORE_FAST        'sourceget'

30	LOAD_FAST         'source'
33	LOAD_ATTR         'match'
36	STORE_FAST        'sourcematch'

39	LOAD_GLOBAL       'len'
42	STORE_FAST        '_len'

45	LOAD_CONST        ('|', ')')
48	STORE_FAST        'PATTERNENDERS'

51	LOAD_CONST        ('=', '!', '<')
54	STORE_FAST        'ASSERTCHARS'

57	LOAD_CONST        ('=', '!')
60	STORE_FAST        'LOOKBEHINDASSERTCHARS'

63	LOAD_GLOBAL       'MIN_REPEAT'
66	LOAD_GLOBAL       'MAX_REPEAT'
69	BUILD_TUPLE_2     None
72	STORE_FAST        'REPEATCODES'

75	SETUP_LOOP        '2845'

78	LOAD_FAST         'source'
81	LOAD_ATTR         'next'
84	LOAD_FAST         'PATTERNENDERS'
87	COMPARE_OP        'in'
90	JUMP_IF_FALSE     '97'

93	BREAK_LOOP        None
94	JUMP_FORWARD      '97'
97_0	COME_FROM         '94'

97	LOAD_FAST         'sourceget'
100	CALL_FUNCTION_0   None
103	STORE_FAST        'this'

106	LOAD_FAST         'this'
109	LOAD_CONST        None
112	COMPARE_OP        'is'
115	JUMP_IF_FALSE     '122'

118	BREAK_LOOP        None
119	JUMP_FORWARD      '122'
122_0	COME_FROM         '119'

122	LOAD_FAST         'state'
125	LOAD_ATTR         'flags'
128	LOAD_GLOBAL       'SRE_FLAG_VERBOSE'
131	BINARY_AND        None
132	JUMP_IF_FALSE     '206'

135	LOAD_FAST         'this'
138	LOAD_GLOBAL       'WHITESPACE'
141	COMPARE_OP        'in'
144	JUMP_IF_FALSE     '153'

147	CONTINUE          '78'
150	JUMP_FORWARD      '153'
153_0	COME_FROM         '150'

153	LOAD_FAST         'this'
156	LOAD_CONST        '#'
159	COMPARE_OP        '=='
162	JUMP_IF_FALSE     '203'

165	SETUP_LOOP        '197'

168	LOAD_FAST         'sourceget'
171	CALL_FUNCTION_0   None
174	STORE_FAST        'this'

177	LOAD_FAST         'this'
180	LOAD_CONST        (None, '\n')
183	COMPARE_OP        'in'
186	JUMP_IF_FALSE     '193'

189	BREAK_LOOP        None
190	JUMP_BACK         '168'
193	JUMP_BACK         '168'
196	POP_BLOCK         None
197_0	COME_FROM         '165'

197	CONTINUE          '78'
200	JUMP_ABSOLUTE     '206'
203	JUMP_FORWARD      '206'
206_0	COME_FROM         '203'

206	LOAD_FAST         'this'
209	JUMP_IF_FALSE     '253'
212	LOAD_FAST         'this'
215	LOAD_CONST        0
218	BINARY_SUBSCR     None
219	LOAD_GLOBAL       'SPECIAL_CHARS'
222	COMPARE_OP        'not in'
225_0	COME_FROM         '209'
225	JUMP_IF_FALSE     '253'

228	LOAD_FAST         'subpatternappend'
231	LOAD_GLOBAL       'LITERAL'
234	LOAD_GLOBAL       'ord'
237	LOAD_FAST         'this'
240	CALL_FUNCTION_1   None
243	BUILD_TUPLE_2     None
246	CALL_FUNCTION_1   None
249	POP_TOP           None
250	JUMP_BACK         '78'

253	LOAD_FAST         'this'
256	LOAD_CONST        '['
259	COMPARE_OP        '=='
262	JUMP_IF_FALSE     '925'

265	BUILD_LIST_0      None
268	STORE_FAST        'set'

271	LOAD_FAST         'set'
274	LOAD_ATTR         'append'
277	STORE_FAST        'setappend'

280	LOAD_FAST         'sourcematch'
283	LOAD_CONST        '^'
286	CALL_FUNCTION_1   None
289	JUMP_IF_FALSE     '311'

292	LOAD_FAST         'setappend'
295	LOAD_GLOBAL       'NEGATE'
298	LOAD_CONST        None
301	BUILD_TUPLE_2     None
304	CALL_FUNCTION_1   None
307	POP_TOP           None
308	JUMP_FORWARD      '311'
311_0	COME_FROM         '308'

311	LOAD_FAST         'set'
314	SLICE+0           None
315	STORE_FAST        'start'

318	SETUP_LOOP        '766'

321	LOAD_FAST         'sourceget'
324	CALL_FUNCTION_0   None
327	STORE_FAST        'this'

330	LOAD_FAST         'this'
333	LOAD_CONST        ']'
336	COMPARE_OP        '=='
339	JUMP_IF_FALSE     '358'
342	LOAD_FAST         'set'
345	LOAD_FAST         'start'
348	COMPARE_OP        '!='
351_0	COME_FROM         '339'
351	JUMP_IF_FALSE     '358'

354	BREAK_LOOP        None
355	JUMP_FORWARD      '434'

358	LOAD_FAST         'this'
361	JUMP_IF_FALSE     '398'
364	LOAD_FAST         'this'
367	LOAD_CONST        0
370	BINARY_SUBSCR     None
371	LOAD_CONST        '\\'
374	COMPARE_OP        '=='
377_0	COME_FROM         '361'
377	JUMP_IF_FALSE     '398'

380	LOAD_GLOBAL       '_class_escape'
383	LOAD_FAST         'source'
386	LOAD_FAST         'this'
389	CALL_FUNCTION_2   None
392	STORE_FAST        'code1'
395	JUMP_FORWARD      '434'

398	LOAD_FAST         'this'
401	JUMP_IF_FALSE     '425'

404	LOAD_GLOBAL       'LITERAL'
407	LOAD_GLOBAL       'ord'
410	LOAD_FAST         'this'
413	CALL_FUNCTION_1   None
416	BUILD_TUPLE_2     None
419	STORE_FAST        'code1'
422	JUMP_FORWARD      '434'

425	LOAD_GLOBAL       'error'
428	LOAD_CONST        'unexpected end of regular expression'
431	RAISE_VARARGS_2   None
434_0	COME_FROM         '355'
434_1	COME_FROM         '395'
434_2	COME_FROM         '422'

434	LOAD_FAST         'sourcematch'
437	LOAD_CONST        '-'
440	CALL_FUNCTION_1   None
443	JUMP_IF_FALSE     '719'

446	LOAD_FAST         'sourceget'
449	CALL_FUNCTION_0   None
452	STORE_FAST        'this'

455	LOAD_FAST         'this'
458	LOAD_CONST        ']'
461	COMPARE_OP        '=='
464	JUMP_IF_FALSE     '536'

467	LOAD_FAST         'code1'
470	LOAD_CONST        0
473	BINARY_SUBSCR     None
474	LOAD_GLOBAL       'IN'
477	COMPARE_OP        'is'
480	JUMP_IF_FALSE     '500'

483	LOAD_FAST         'code1'
486	LOAD_CONST        1
489	BINARY_SUBSCR     None
490	LOAD_CONST        0
493	BINARY_SUBSCR     None
494	STORE_FAST        'code1'
497	JUMP_FORWARD      '500'
500_0	COME_FROM         '497'

500	LOAD_FAST         'setappend'
503	LOAD_FAST         'code1'
506	CALL_FUNCTION_1   None
509	POP_TOP           None

510	LOAD_FAST         'setappend'
513	LOAD_GLOBAL       'LITERAL'
516	LOAD_GLOBAL       'ord'
519	LOAD_CONST        '-'
522	CALL_FUNCTION_1   None
525	BUILD_TUPLE_2     None
528	CALL_FUNCTION_1   None
531	POP_TOP           None

532	BREAK_LOOP        None
533	JUMP_ABSOLUTE     '762'

536	LOAD_FAST         'this'
539	JUMP_IF_FALSE     '707'

542	LOAD_FAST         'this'
545	LOAD_CONST        0
548	BINARY_SUBSCR     None
549	LOAD_CONST        '\\'
552	COMPARE_OP        '=='
555	JUMP_IF_FALSE     '576'

558	LOAD_GLOBAL       '_class_escape'
561	LOAD_FAST         'source'
564	LOAD_FAST         'this'
567	CALL_FUNCTION_2   None
570	STORE_FAST        'code2'
573	JUMP_FORWARD      '594'

576	LOAD_GLOBAL       'LITERAL'
579	LOAD_GLOBAL       'ord'
582	LOAD_FAST         'this'
585	CALL_FUNCTION_1   None
588	BUILD_TUPLE_2     None
591	STORE_FAST        'code2'
594_0	COME_FROM         '573'

594	LOAD_FAST         'code1'
597	LOAD_CONST        0
600	BINARY_SUBSCR     None
601	LOAD_GLOBAL       'LITERAL'
604	COMPARE_OP        '!='
607	JUMP_IF_TRUE      '626'
610	LOAD_FAST         'code2'
613	LOAD_CONST        0
616	BINARY_SUBSCR     None
617	LOAD_GLOBAL       'LITERAL'
620	COMPARE_OP        '!='
623_0	COME_FROM         '607'
623	JUMP_IF_FALSE     '638'

626	LOAD_GLOBAL       'error'
629	LOAD_CONST        'bad character range'
632	RAISE_VARARGS_2   None
635	JUMP_FORWARD      '638'
638_0	COME_FROM         '635'

638	LOAD_FAST         'code1'
641	LOAD_CONST        1
644	BINARY_SUBSCR     None
645	STORE_FAST        'lo'

648	LOAD_FAST         'code2'
651	LOAD_CONST        1
654	BINARY_SUBSCR     None
655	STORE_FAST        'hi'

658	LOAD_FAST         'hi'
661	LOAD_FAST         'lo'
664	COMPARE_OP        '<'
667	JUMP_IF_FALSE     '682'

670	LOAD_GLOBAL       'error'
673	LOAD_CONST        'bad character range'
676	RAISE_VARARGS_2   None
679	JUMP_FORWARD      '682'
682_0	COME_FROM         '679'

682	LOAD_FAST         'setappend'
685	LOAD_GLOBAL       'RANGE'
688	LOAD_FAST         'lo'
691	LOAD_FAST         'hi'
694	BUILD_TUPLE_2     None
697	BUILD_TUPLE_2     None
700	CALL_FUNCTION_1   None
703	POP_TOP           None
704	JUMP_ABSOLUTE     '762'

707	LOAD_GLOBAL       'error'
710	LOAD_CONST        'unexpected end of regular expression'
713	RAISE_VARARGS_2   None
716	JUMP_BACK         '321'

719	LOAD_FAST         'code1'
722	LOAD_CONST        0
725	BINARY_SUBSCR     None
726	LOAD_GLOBAL       'IN'
729	COMPARE_OP        'is'
732	JUMP_IF_FALSE     '752'

735	LOAD_FAST         'code1'
738	LOAD_CONST        1
741	BINARY_SUBSCR     None
742	LOAD_CONST        0
745	BINARY_SUBSCR     None
746	STORE_FAST        'code1'
749	JUMP_FORWARD      '752'
752_0	COME_FROM         '749'

752	LOAD_FAST         'setappend'
755	LOAD_FAST         'code1'
758	CALL_FUNCTION_1   None
761	POP_TOP           None
762	JUMP_BACK         '321'
765	POP_BLOCK         None
766_0	COME_FROM         '318'

766	LOAD_FAST         '_len'
769	LOAD_FAST         'set'
772	CALL_FUNCTION_1   None
775	LOAD_CONST        1
778	COMPARE_OP        '=='
781	JUMP_IF_FALSE     '821'
784	LOAD_FAST         'set'
787	LOAD_CONST        0
790	BINARY_SUBSCR     None
791	LOAD_CONST        0
794	BINARY_SUBSCR     None
795	LOAD_GLOBAL       'LITERAL'
798	COMPARE_OP        'is'
801_0	COME_FROM         '781'
801	JUMP_IF_FALSE     '821'

804	LOAD_FAST         'subpatternappend'
807	LOAD_FAST         'set'
810	LOAD_CONST        0
813	BINARY_SUBSCR     None
814	CALL_FUNCTION_1   None
817	POP_TOP           None
818	JUMP_ABSOLUTE     '2841'

821	LOAD_FAST         '_len'
824	LOAD_FAST         'set'
827	CALL_FUNCTION_1   None
830	LOAD_CONST        2
833	COMPARE_OP        '=='
836	JUMP_IF_FALSE     '906'
839	LOAD_FAST         'set'
842	LOAD_CONST        0
845	BINARY_SUBSCR     None
846	LOAD_CONST        0
849	BINARY_SUBSCR     None
850	LOAD_GLOBAL       'NEGATE'
853	COMPARE_OP        'is'
856	JUMP_IF_FALSE     '906'
859	LOAD_FAST         'set'
862	LOAD_CONST        1
865	BINARY_SUBSCR     None
866	LOAD_CONST        0
869	BINARY_SUBSCR     None
870	LOAD_GLOBAL       'LITERAL'
873	COMPARE_OP        'is'
876_0	COME_FROM         '836'
876_1	COME_FROM         '856'
876	JUMP_IF_FALSE     '906'

879	LOAD_FAST         'subpatternappend'
882	LOAD_GLOBAL       'NOT_LITERAL'
885	LOAD_FAST         'set'
888	LOAD_CONST        1
891	BINARY_SUBSCR     None
892	LOAD_CONST        1
895	BINARY_SUBSCR     None
896	BUILD_TUPLE_2     None
899	CALL_FUNCTION_1   None
902	POP_TOP           None
903	JUMP_ABSOLUTE     '2841'

906	LOAD_FAST         'subpatternappend'
909	LOAD_GLOBAL       'IN'
912	LOAD_FAST         'set'
915	BUILD_TUPLE_2     None
918	CALL_FUNCTION_1   None
921	POP_TOP           None
922	JUMP_BACK         '78'

925	LOAD_FAST         'this'
928	JUMP_IF_FALSE     '1484'
931	LOAD_FAST         'this'
934	LOAD_CONST        0
937	BINARY_SUBSCR     None
938	LOAD_GLOBAL       'REPEAT_CHARS'
941	COMPARE_OP        'in'
944_0	COME_FROM         '928'
944	JUMP_IF_FALSE     '1484'

947	LOAD_FAST         'this'
950	LOAD_CONST        '?'
953	COMPARE_OP        '=='
956	JUMP_IF_FALSE     '974'

959	LOAD_CONST        (0, 1)
962	UNPACK_SEQUENCE_2 None
965	STORE_FAST        'min'
968	STORE_FAST        'max'
971	JUMP_FORWARD      '1302'

974	LOAD_FAST         'this'
977	LOAD_CONST        '*'
980	COMPARE_OP        '=='
983	JUMP_IF_FALSE     '1002'

986	LOAD_CONST        0
989	LOAD_GLOBAL       'MAXREPEAT'
992	ROT_TWO           None
993	STORE_FAST        'min'
996	STORE_FAST        'max'
999	JUMP_FORWARD      '1302'

1002	LOAD_FAST         'this'
1005	LOAD_CONST        '+'
1008	COMPARE_OP        '=='
1011	JUMP_IF_FALSE     '1030'

1014	LOAD_CONST        1
1017	LOAD_GLOBAL       'MAXREPEAT'
1020	ROT_TWO           None
1021	STORE_FAST        'min'
1024	STORE_FAST        'max'
1027	JUMP_FORWARD      '1302'

1030	LOAD_FAST         'this'
1033	LOAD_CONST        '{'
1036	COMPARE_OP        '=='
1039	JUMP_IF_FALSE     '1293'

1042	LOAD_FAST         'source'
1045	LOAD_ATTR         'tell'
1048	CALL_FUNCTION_0   None
1051	STORE_FAST        'here'

1054	LOAD_CONST        0
1057	LOAD_GLOBAL       'MAXREPEAT'
1060	ROT_TWO           None
1061	STORE_FAST        'min'
1064	STORE_FAST        'max'

1067	LOAD_CONST        ''
1070	DUP_TOP           None
1071	STORE_FAST        'lo'
1074	STORE_FAST        'hi'

1077	SETUP_LOOP        '1115'
1080	LOAD_FAST         'source'
1083	LOAD_ATTR         'next'
1086	LOAD_GLOBAL       'DIGITS'
1089	COMPARE_OP        'in'
1092	JUMP_IF_FALSE     '1114'

1095	LOAD_FAST         'lo'
1098	LOAD_FAST         'source'
1101	LOAD_ATTR         'get'
1104	CALL_FUNCTION_0   None
1107	BINARY_ADD        None
1108	STORE_FAST        'lo'
1111	JUMP_BACK         '1080'
1114	POP_BLOCK         None
1115_0	COME_FROM         '1077'

1115	LOAD_FAST         'sourcematch'
1118	LOAD_CONST        ','
1121	CALL_FUNCTION_1   None
1124	JUMP_IF_FALSE     '1165'

1127	SETUP_LOOP        '1171'
1130	LOAD_FAST         'source'
1133	LOAD_ATTR         'next'
1136	LOAD_GLOBAL       'DIGITS'
1139	COMPARE_OP        'in'
1142	JUMP_IF_FALSE     '1161'

1145	LOAD_FAST         'hi'
1148	LOAD_FAST         'sourceget'
1151	CALL_FUNCTION_0   None
1154	BINARY_ADD        None
1155	STORE_FAST        'hi'
1158	JUMP_BACK         '1130'
1161	POP_BLOCK         None
1162_0	COME_FROM         '1127'
1162	JUMP_FORWARD      '1171'

1165	LOAD_FAST         'lo'
1168	STORE_FAST        'hi'
1171_0	COME_FROM         '1162'

1171	LOAD_FAST         'sourcematch'
1174	LOAD_CONST        '}'
1177	CALL_FUNCTION_1   None
1180	JUMP_IF_TRUE      '1224'

1183	LOAD_FAST         'subpatternappend'
1186	LOAD_GLOBAL       'LITERAL'
1189	LOAD_GLOBAL       'ord'
1192	LOAD_FAST         'this'
1195	CALL_FUNCTION_1   None
1198	BUILD_TUPLE_2     None
1201	CALL_FUNCTION_1   None
1204	POP_TOP           None

1205	LOAD_FAST         'source'
1208	LOAD_ATTR         'seek'
1211	LOAD_FAST         'here'
1214	CALL_FUNCTION_1   None
1217	POP_TOP           None

1218	CONTINUE          '78'
1221	JUMP_FORWARD      '1224'
1224_0	COME_FROM         '1221'

1224	LOAD_FAST         'lo'
1227	JUMP_IF_FALSE     '1245'

1230	LOAD_GLOBAL       'int'
1233	LOAD_FAST         'lo'
1236	CALL_FUNCTION_1   None
1239	STORE_FAST        'min'
1242	JUMP_FORWARD      '1245'
1245_0	COME_FROM         '1242'

1245	LOAD_FAST         'hi'
1248	JUMP_IF_FALSE     '1266'

1251	LOAD_GLOBAL       'int'
1254	LOAD_FAST         'hi'
1257	CALL_FUNCTION_1   None
1260	STORE_FAST        'max'
1263	JUMP_FORWARD      '1266'
1266_0	COME_FROM         '1263'

1266	LOAD_FAST         'max'
1269	LOAD_FAST         'min'
1272	COMPARE_OP        '<'
1275	JUMP_IF_FALSE     '1290'

1278	LOAD_GLOBAL       'error'
1281	LOAD_CONST        'bad repeat interval'
1284	RAISE_VARARGS_2   None
1287	JUMP_ABSOLUTE     '1302'
1290	JUMP_FORWARD      '1302'

1293	LOAD_GLOBAL       'error'
1296	LOAD_CONST        'not supported'
1299	RAISE_VARARGS_2   None
1302_0	COME_FROM         '971'
1302_1	COME_FROM         '999'
1302_2	COME_FROM         '1027'
1302_3	COME_FROM         '1290'

1302	LOAD_FAST         'subpattern'
1305	JUMP_IF_FALSE     '1321'

1308	LOAD_FAST         'subpattern'
1311	LOAD_CONST        -1
1314	SLICE+1           None
1315	STORE_FAST        'item'
1318	JUMP_FORWARD      '1327'

1321	LOAD_CONST        None
1324	STORE_FAST        'item'
1327_0	COME_FROM         '1318'

1327	LOAD_FAST         'item'
1330	UNARY_NOT         None
1331	JUMP_IF_TRUE      '1372'
1334	LOAD_FAST         '_len'
1337	LOAD_FAST         'item'
1340	CALL_FUNCTION_1   None
1343	LOAD_CONST        1
1346	COMPARE_OP        '=='
1349	JUMP_IF_FALSE     '1384'
1352	LOAD_FAST         'item'
1355	LOAD_CONST        0
1358	BINARY_SUBSCR     None
1359	LOAD_CONST        0
1362	BINARY_SUBSCR     None
1363	LOAD_GLOBAL       'AT'
1366	COMPARE_OP        '=='
1369_0	COME_FROM         '1331'
1369_1	COME_FROM         '1349'
1369	JUMP_IF_FALSE     '1384'

1372	LOAD_GLOBAL       'error'
1375	LOAD_CONST        'nothing to repeat'
1378	RAISE_VARARGS_2   None
1381	JUMP_FORWARD      '1384'
1384_0	COME_FROM         '1381'

1384	LOAD_FAST         'item'
1387	LOAD_CONST        0
1390	BINARY_SUBSCR     None
1391	LOAD_CONST        0
1394	BINARY_SUBSCR     None
1395	LOAD_FAST         'REPEATCODES'
1398	COMPARE_OP        'in'
1401	JUMP_IF_FALSE     '1416'

1404	LOAD_GLOBAL       'error'
1407	LOAD_CONST        'multiple repeat'
1410	RAISE_VARARGS_2   None
1413	JUMP_FORWARD      '1416'
1416_0	COME_FROM         '1413'

1416	LOAD_FAST         'sourcematch'
1419	LOAD_CONST        '?'
1422	CALL_FUNCTION_1   None
1425	JUMP_IF_FALSE     '1456'

1428	LOAD_GLOBAL       'MIN_REPEAT'
1431	LOAD_FAST         'min'
1434	LOAD_FAST         'max'
1437	LOAD_FAST         'item'
1440	BUILD_TUPLE_3     None
1443	BUILD_TUPLE_2     None
1446	LOAD_FAST         'subpattern'
1449	LOAD_CONST        -1
1452	STORE_SUBSCR      None
1453	JUMP_ABSOLUTE     '2841'

1456	LOAD_GLOBAL       'MAX_REPEAT'
1459	LOAD_FAST         'min'
1462	LOAD_FAST         'max'
1465	LOAD_FAST         'item'
1468	BUILD_TUPLE_3     None
1471	BUILD_TUPLE_2     None
1474	LOAD_FAST         'subpattern'
1477	LOAD_CONST        -1
1480	STORE_SUBSCR      None
1481	JUMP_BACK         '78'

1484	LOAD_FAST         'this'
1487	LOAD_CONST        '.'
1490	COMPARE_OP        '=='
1493	JUMP_IF_FALSE     '1515'

1496	LOAD_FAST         'subpatternappend'
1499	LOAD_GLOBAL       'ANY'
1502	LOAD_CONST        None
1505	BUILD_TUPLE_2     None
1508	CALL_FUNCTION_1   None
1511	POP_TOP           None
1512	JUMP_BACK         '78'

1515	LOAD_FAST         'this'
1518	LOAD_CONST        '('
1521	COMPARE_OP        '=='
1524	JUMP_IF_FALSE     '2714'

1527	LOAD_CONST        1
1530	STORE_FAST        'group'

1533	LOAD_CONST        None
1536	STORE_FAST        'name'

1539	LOAD_CONST        None
1542	STORE_FAST        'condgroup'

1545	LOAD_FAST         'sourcematch'
1548	LOAD_CONST        '?'
1551	CALL_FUNCTION_1   None
1554	JUMP_IF_FALSE     '2485'

1557	LOAD_CONST        0
1560	STORE_FAST        'group'

1563	LOAD_FAST         'sourcematch'
1566	LOAD_CONST        'P'
1569	CALL_FUNCTION_1   None
1572	JUMP_IF_FALSE     '1913'

1575	LOAD_FAST         'sourcematch'
1578	LOAD_CONST        '<'
1581	CALL_FUNCTION_1   None
1584	JUMP_IF_FALSE     '1692'

1587	LOAD_CONST        ''
1590	STORE_FAST        'name'

1593	SETUP_LOOP        '1659'

1596	LOAD_FAST         'sourceget'
1599	CALL_FUNCTION_0   None
1602	STORE_FAST        'char'

1605	LOAD_FAST         'char'
1608	LOAD_CONST        None
1611	COMPARE_OP        'is'
1614	JUMP_IF_FALSE     '1629'

1617	LOAD_GLOBAL       'error'
1620	LOAD_CONST        'unterminated name'
1623	RAISE_VARARGS_2   None
1626	JUMP_FORWARD      '1629'
1629_0	COME_FROM         '1626'

1629	LOAD_FAST         'char'
1632	LOAD_CONST        '>'
1635	COMPARE_OP        '=='
1638	JUMP_IF_FALSE     '1645'

1641	BREAK_LOOP        None
1642	JUMP_FORWARD      '1645'
1645_0	COME_FROM         '1642'

1645	LOAD_FAST         'name'
1648	LOAD_FAST         'char'
1651	BINARY_ADD        None
1652	STORE_FAST        'name'
1655	JUMP_BACK         '1596'
1658	POP_BLOCK         None
1659_0	COME_FROM         '1593'

1659	LOAD_CONST        1
1662	STORE_FAST        'group'

1665	LOAD_GLOBAL       'isname'
1668	LOAD_FAST         'name'
1671	CALL_FUNCTION_1   None
1674	JUMP_IF_TRUE      '1689'

1677	LOAD_GLOBAL       'error'
1680	LOAD_CONST        'bad character in group name'
1683	RAISE_VARARGS_2   None
1686	JUMP_ABSOLUTE     '1910'
1689	JUMP_ABSOLUTE     '2482'

1692	LOAD_FAST         'sourcematch'
1695	LOAD_CONST        '='
1698	CALL_FUNCTION_1   None
1701	JUMP_IF_FALSE     '1864'

1704	LOAD_CONST        ''
1707	STORE_FAST        'name'

1710	SETUP_LOOP        '1776'

1713	LOAD_FAST         'sourceget'
1716	CALL_FUNCTION_0   None
1719	STORE_FAST        'char'

1722	LOAD_FAST         'char'
1725	LOAD_CONST        None
1728	COMPARE_OP        'is'
1731	JUMP_IF_FALSE     '1746'

1734	LOAD_GLOBAL       'error'
1737	LOAD_CONST        'unterminated name'
1740	RAISE_VARARGS_2   None
1743	JUMP_FORWARD      '1746'
1746_0	COME_FROM         '1743'

1746	LOAD_FAST         'char'
1749	LOAD_CONST        ')'
1752	COMPARE_OP        '=='
1755	JUMP_IF_FALSE     '1762'

1758	BREAK_LOOP        None
1759	JUMP_FORWARD      '1762'
1762_0	COME_FROM         '1759'

1762	LOAD_FAST         'name'
1765	LOAD_FAST         'char'
1768	BINARY_ADD        None
1769	STORE_FAST        'name'
1772	JUMP_BACK         '1713'
1775	POP_BLOCK         None
1776_0	COME_FROM         '1710'

1776	LOAD_GLOBAL       'isname'
1779	LOAD_FAST         'name'
1782	CALL_FUNCTION_1   None
1785	JUMP_IF_TRUE      '1800'

1788	LOAD_GLOBAL       'error'
1791	LOAD_CONST        'bad character in group name'
1794	RAISE_VARARGS_2   None
1797	JUMP_FORWARD      '1800'
1800_0	COME_FROM         '1797'

1800	LOAD_FAST         'state'
1803	LOAD_ATTR         'groupdict'
1806	LOAD_ATTR         'get'
1809	LOAD_FAST         'name'
1812	CALL_FUNCTION_1   None
1815	STORE_FAST        'gid'

1818	LOAD_FAST         'gid'
1821	LOAD_CONST        None
1824	COMPARE_OP        'is'
1827	JUMP_IF_FALSE     '1842'

1830	LOAD_GLOBAL       'error'
1833	LOAD_CONST        'unknown group name'
1836	RAISE_VARARGS_2   None
1839	JUMP_FORWARD      '1842'
1842_0	COME_FROM         '1839'

1842	LOAD_FAST         'subpatternappend'
1845	LOAD_GLOBAL       'GROUPREF'
1848	LOAD_FAST         'gid'
1851	BUILD_TUPLE_2     None
1854	CALL_FUNCTION_1   None
1857	POP_TOP           None

1858	CONTINUE          '78'
1861	JUMP_ABSOLUTE     '2482'

1864	LOAD_FAST         'sourceget'
1867	CALL_FUNCTION_0   None
1870	STORE_FAST        'char'

1873	LOAD_FAST         'char'
1876	LOAD_CONST        None
1879	COMPARE_OP        'is'
1882	JUMP_IF_FALSE     '1897'

1885	LOAD_GLOBAL       'error'
1888	LOAD_CONST        'unexpected end of pattern'
1891	RAISE_VARARGS_2   None
1894	JUMP_FORWARD      '1897'
1897_0	COME_FROM         '1894'

1897	LOAD_GLOBAL       'error'
1900	LOAD_CONST        'unknown specifier: ?P%s'
1903	LOAD_FAST         'char'
1906	BINARY_MODULO     None
1907	RAISE_VARARGS_2   None
1910	JUMP_ABSOLUTE     '2485'

1913	LOAD_FAST         'sourcematch'
1916	LOAD_CONST        ':'
1919	CALL_FUNCTION_1   None
1922	JUMP_IF_FALSE     '1934'

1925	LOAD_CONST        2
1928	STORE_FAST        'group'
1931	JUMP_ABSOLUTE     '2485'

1934	LOAD_FAST         'sourcematch'
1937	LOAD_CONST        '#'
1940	CALL_FUNCTION_1   None
1943	JUMP_IF_FALSE     '2024'

1946	SETUP_LOOP        '1994'

1949	LOAD_FAST         'source'
1952	LOAD_ATTR         'next'
1955	LOAD_CONST        None
1958	COMPARE_OP        'is'
1961	JUMP_IF_TRUE      '1979'
1964	LOAD_FAST         'source'
1967	LOAD_ATTR         'next'
1970	LOAD_CONST        ')'
1973	COMPARE_OP        '=='
1976_0	COME_FROM         '1961'
1976	JUMP_IF_FALSE     '1983'

1979	BREAK_LOOP        None
1980	JUMP_FORWARD      '1983'
1983_0	COME_FROM         '1980'

1983	LOAD_FAST         'sourceget'
1986	CALL_FUNCTION_0   None
1989	POP_TOP           None
1990	JUMP_BACK         '1949'
1993	POP_BLOCK         None
1994_0	COME_FROM         '1946'

1994	LOAD_FAST         'sourcematch'
1997	LOAD_CONST        ')'
2000	CALL_FUNCTION_1   None
2003	JUMP_IF_TRUE      '2018'

2006	LOAD_GLOBAL       'error'
2009	LOAD_CONST        'unbalanced parenthesis'
2012	RAISE_VARARGS_2   None
2015	JUMP_BACK         '78'

2018	CONTINUE          '78'
2021	JUMP_ABSOLUTE     '2485'

2024	LOAD_FAST         'source'
2027	LOAD_ATTR         'next'
2030	LOAD_FAST         'ASSERTCHARS'
2033	COMPARE_OP        'in'
2036	JUMP_IF_FALSE     '2215'

2039	LOAD_FAST         'sourceget'
2042	CALL_FUNCTION_0   None
2045	STORE_FAST        'char'

2048	LOAD_CONST        1
2051	STORE_FAST        'dir'

2054	LOAD_FAST         'char'
2057	LOAD_CONST        '<'
2060	COMPARE_OP        '=='
2063	JUMP_IF_FALSE     '2111'

2066	LOAD_FAST         'source'
2069	LOAD_ATTR         'next'
2072	LOAD_FAST         'LOOKBEHINDASSERTCHARS'
2075	COMPARE_OP        'not in'
2078	JUMP_IF_FALSE     '2093'

2081	LOAD_GLOBAL       'error'
2084	LOAD_CONST        'syntax error'
2087	RAISE_VARARGS_2   None
2090	JUMP_FORWARD      '2093'
2093_0	COME_FROM         '2090'

2093	LOAD_CONST        -1
2096	STORE_FAST        'dir'

2099	LOAD_FAST         'sourceget'
2102	CALL_FUNCTION_0   None
2105	STORE_FAST        'char'
2108	JUMP_FORWARD      '2111'
2111_0	COME_FROM         '2108'

2111	LOAD_GLOBAL       '_parse_sub'
2114	LOAD_FAST         'source'
2117	LOAD_FAST         'state'
2120	CALL_FUNCTION_2   None
2123	STORE_FAST        'p'

2126	LOAD_FAST         'sourcematch'
2129	LOAD_CONST        ')'
2132	CALL_FUNCTION_1   None
2135	JUMP_IF_TRUE      '2150'

2138	LOAD_GLOBAL       'error'
2141	LOAD_CONST        'unbalanced parenthesis'
2144	RAISE_VARARGS_2   None
2147	JUMP_FORWARD      '2150'
2150_0	COME_FROM         '2147'

2150	LOAD_FAST         'char'
2153	LOAD_CONST        '='
2156	COMPARE_OP        '=='
2159	JUMP_IF_FALSE     '2187'

2162	LOAD_FAST         'subpatternappend'
2165	LOAD_GLOBAL       'ASSERT'
2168	LOAD_FAST         'dir'
2171	LOAD_FAST         'p'
2174	BUILD_TUPLE_2     None
2177	BUILD_TUPLE_2     None
2180	CALL_FUNCTION_1   None
2183	POP_TOP           None
2184	JUMP_BACK         '78'

2187	LOAD_FAST         'subpatternappend'
2190	LOAD_GLOBAL       'ASSERT_NOT'
2193	LOAD_FAST         'dir'
2196	LOAD_FAST         'p'
2199	BUILD_TUPLE_2     None
2202	BUILD_TUPLE_2     None
2205	CALL_FUNCTION_1   None
2208	POP_TOP           None

2209	CONTINUE          '78'
2212	JUMP_ABSOLUTE     '2485'

2215	LOAD_FAST         'sourcematch'
2218	LOAD_CONST        '('
2221	CALL_FUNCTION_1   None
2224	JUMP_IF_FALSE     '2410'

2227	LOAD_CONST        ''
2230	STORE_FAST        'condname'

2233	SETUP_LOOP        '2299'

2236	LOAD_FAST         'sourceget'
2239	CALL_FUNCTION_0   None
2242	STORE_FAST        'char'

2245	LOAD_FAST         'char'
2248	LOAD_CONST        None
2251	COMPARE_OP        'is'
2254	JUMP_IF_FALSE     '2269'

2257	LOAD_GLOBAL       'error'
2260	LOAD_CONST        'unterminated name'
2263	RAISE_VARARGS_2   None
2266	JUMP_FORWARD      '2269'
2269_0	COME_FROM         '2266'

2269	LOAD_FAST         'char'
2272	LOAD_CONST        ')'
2275	COMPARE_OP        '=='
2278	JUMP_IF_FALSE     '2285'

2281	BREAK_LOOP        None
2282	JUMP_FORWARD      '2285'
2285_0	COME_FROM         '2282'

2285	LOAD_FAST         'condname'
2288	LOAD_FAST         'char'
2291	BINARY_ADD        None
2292	STORE_FAST        'condname'
2295	JUMP_BACK         '2236'
2298	POP_BLOCK         None
2299_0	COME_FROM         '2233'

2299	LOAD_CONST        2
2302	STORE_FAST        'group'

2305	LOAD_GLOBAL       'isname'
2308	LOAD_FAST         'condname'
2311	CALL_FUNCTION_1   None
2314	JUMP_IF_FALSE     '2362'

2317	LOAD_FAST         'state'
2320	LOAD_ATTR         'groupdict'
2323	LOAD_ATTR         'get'
2326	LOAD_FAST         'condname'
2329	CALL_FUNCTION_1   None
2332	STORE_FAST        'condgroup'

2335	LOAD_FAST         'condgroup'
2338	LOAD_CONST        None
2341	COMPARE_OP        'is'
2344	JUMP_IF_FALSE     '2359'

2347	LOAD_GLOBAL       'error'
2350	LOAD_CONST        'unknown group name'
2353	RAISE_VARARGS_2   None
2356	JUMP_ABSOLUTE     '2407'
2359	JUMP_ABSOLUTE     '2482'

2362	SETUP_EXCEPT      '2381'

2365	LOAD_GLOBAL       'int'
2368	LOAD_FAST         'condname'
2371	CALL_FUNCTION_1   None
2374	STORE_FAST        'condgroup'
2377	POP_BLOCK         None
2378	JUMP_ABSOLUTE     '2482'
2381_0	COME_FROM         '2362'

2381	DUP_TOP           None
2382	LOAD_GLOBAL       'ValueError'
2385	COMPARE_OP        'exception match'
2388	JUMP_IF_FALSE     '2406'
2391	POP_TOP           None
2392	POP_TOP           None
2393	POP_TOP           None

2394	LOAD_GLOBAL       'error'
2397	LOAD_CONST        'bad character in group name'
2400	RAISE_VARARGS_2   None
2403	JUMP_ABSOLUTE     '2482'
2406	END_FINALLY       None
2407_0	COME_FROM         '2406'
2407	JUMP_ABSOLUTE     '2485'

2410	LOAD_FAST         'source'
2413	LOAD_ATTR         'next'
2416	LOAD_GLOBAL       'FLAGS'
2419	COMPARE_OP        'not in'
2422	JUMP_IF_FALSE     '2437'

2425	LOAD_GLOBAL       'error'
2428	LOAD_CONST        'unexpected end of pattern'
2431	RAISE_VARARGS_2   None
2434	JUMP_FORWARD      '2437'
2437_0	COME_FROM         '2434'

2437	SETUP_LOOP        '2485'
2440	LOAD_FAST         'source'
2443	LOAD_ATTR         'next'
2446	LOAD_GLOBAL       'FLAGS'
2449	COMPARE_OP        'in'
2452	JUMP_IF_FALSE     '2481'

2455	LOAD_FAST         'state'
2458	LOAD_ATTR         'flags'
2461	LOAD_GLOBAL       'FLAGS'
2464	LOAD_FAST         'sourceget'
2467	CALL_FUNCTION_0   None
2470	BINARY_SUBSCR     None
2471	BINARY_OR         None
2472	LOAD_FAST         'state'
2475	STORE_ATTR        'flags'
2478	JUMP_BACK         '2440'
2481	POP_BLOCK         None
2482_0	COME_FROM         '2437'
2482	JUMP_FORWARD      '2485'
2485_0	COME_FROM         '2482'

2485	LOAD_FAST         'group'
2488	JUMP_IF_FALSE     '2646'

2491	LOAD_FAST         'group'
2494	LOAD_CONST        2
2497	COMPARE_OP        '=='
2500	JUMP_IF_FALSE     '2512'

2503	LOAD_CONST        None
2506	STORE_FAST        'group'
2509	JUMP_FORWARD      '2527'

2512	LOAD_FAST         'state'
2515	LOAD_ATTR         'opengroup'
2518	LOAD_FAST         'name'
2521	CALL_FUNCTION_1   None
2524	STORE_FAST        'group'
2527_0	COME_FROM         '2509'

2527	LOAD_FAST         'condgroup'
2530	JUMP_IF_FALSE     '2554'

2533	LOAD_GLOBAL       '_parse_sub_cond'
2536	LOAD_FAST         'source'
2539	LOAD_FAST         'state'
2542	LOAD_FAST         'condgroup'
2545	CALL_FUNCTION_3   None
2548	STORE_FAST        'p'
2551	JUMP_FORWARD      '2569'

2554	LOAD_GLOBAL       '_parse_sub'
2557	LOAD_FAST         'source'
2560	LOAD_FAST         'state'
2563	CALL_FUNCTION_2   None
2566	STORE_FAST        'p'
2569_0	COME_FROM         '2551'

2569	LOAD_FAST         'sourcematch'
2572	LOAD_CONST        ')'
2575	CALL_FUNCTION_1   None
2578	JUMP_IF_TRUE      '2593'

2581	LOAD_GLOBAL       'error'
2584	LOAD_CONST        'unbalanced parenthesis'
2587	RAISE_VARARGS_2   None
2590	JUMP_FORWARD      '2593'
2593_0	COME_FROM         '2590'

2593	LOAD_FAST         'group'
2596	LOAD_CONST        None
2599	COMPARE_OP        'is not'
2602	JUMP_IF_FALSE     '2621'

2605	LOAD_FAST         'state'
2608	LOAD_ATTR         'closegroup'
2611	LOAD_FAST         'group'
2614	CALL_FUNCTION_1   None
2617	POP_TOP           None
2618	JUMP_FORWARD      '2621'
2621_0	COME_FROM         '2618'

2621	LOAD_FAST         'subpatternappend'
2624	LOAD_GLOBAL       'SUBPATTERN'
2627	LOAD_FAST         'group'
2630	LOAD_FAST         'p'
2633	BUILD_TUPLE_2     None
2636	BUILD_TUPLE_2     None
2639	CALL_FUNCTION_1   None
2642	POP_TOP           None
2643	JUMP_ABSOLUTE     '2841'

2646	SETUP_LOOP        '2841'

2649	LOAD_FAST         'sourceget'
2652	CALL_FUNCTION_0   None
2655	STORE_FAST        'char'

2658	LOAD_FAST         'char'
2661	LOAD_CONST        None
2664	COMPARE_OP        'is'
2667	JUMP_IF_FALSE     '2682'

2670	LOAD_GLOBAL       'error'
2673	LOAD_CONST        'unexpected end of pattern'
2676	RAISE_VARARGS_2   None
2679	JUMP_FORWARD      '2682'
2682_0	COME_FROM         '2679'

2682	LOAD_FAST         'char'
2685	LOAD_CONST        ')'
2688	COMPARE_OP        '=='
2691	JUMP_IF_FALSE     '2698'

2694	BREAK_LOOP        None
2695	JUMP_FORWARD      '2698'
2698_0	COME_FROM         '2695'

2698	LOAD_GLOBAL       'error'
2701	LOAD_CONST        'unknown extension'
2704	RAISE_VARARGS_2   None
2707	JUMP_BACK         '2649'
2710	POP_BLOCK         None
2711_0	COME_FROM         '2646'
2711	JUMP_BACK         '78'

2714	LOAD_FAST         'this'
2717	LOAD_CONST        '^'
2720	COMPARE_OP        '=='
2723	JUMP_IF_FALSE     '2745'

2726	LOAD_FAST         'subpatternappend'
2729	LOAD_GLOBAL       'AT'
2732	LOAD_GLOBAL       'AT_BEGINNING'
2735	BUILD_TUPLE_2     None
2738	CALL_FUNCTION_1   None
2741	POP_TOP           None
2742	JUMP_BACK         '78'

2745	LOAD_FAST         'this'
2748	LOAD_CONST        '$'
2751	COMPARE_OP        '=='
2754	JUMP_IF_FALSE     '2779'

2757	LOAD_FAST         'subpattern'
2760	LOAD_ATTR         'append'
2763	LOAD_GLOBAL       'AT'
2766	LOAD_GLOBAL       'AT_END'
2769	BUILD_TUPLE_2     None
2772	CALL_FUNCTION_1   None
2775	POP_TOP           None
2776	JUMP_BACK         '78'

2779	LOAD_FAST         'this'
2782	JUMP_IF_FALSE     '2832'
2785	LOAD_FAST         'this'
2788	LOAD_CONST        0
2791	BINARY_SUBSCR     None
2792	LOAD_CONST        '\\'
2795	COMPARE_OP        '=='
2798_0	COME_FROM         '2782'
2798	JUMP_IF_FALSE     '2832'

2801	LOAD_GLOBAL       '_escape'
2804	LOAD_FAST         'source'
2807	LOAD_FAST         'this'
2810	LOAD_FAST         'state'
2813	CALL_FUNCTION_3   None
2816	STORE_FAST        'code'

2819	LOAD_FAST         'subpatternappend'
2822	LOAD_FAST         'code'
2825	CALL_FUNCTION_1   None
2828	POP_TOP           None
2829	JUMP_BACK         '78'

2832	LOAD_GLOBAL       'error'
2835	LOAD_CONST        'parser error'
2838	RAISE_VARARGS_2   None
2841	JUMP_BACK         '78'
2844	POP_BLOCK         None
2845_0	COME_FROM         '75'

2845	LOAD_FAST         'subpattern'
2848	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 196


def parse(str, flags = 0, pattern = None):
    source = Tokenizer(str)
    if pattern is None:
        pattern = Pattern()
    pattern.flags = flags
    pattern.str = str
    p = _parse_sub(source, pattern, 0)
    tail = source.get()
    if tail == ')':
        raise error, 'unbalanced parenthesis'
    elif tail:
        raise error, 'bogus characters at end of regular expression'
    if flags & SRE_FLAG_DEBUG:
        p.dump()
    if not flags & SRE_FLAG_VERBOSE and p.pattern.flags & SRE_FLAG_VERBOSE:
        return parse(str, p.pattern.flags)
    return p


def parse_template--- This code section failed: ---

0	LOAD_GLOBAL       'Tokenizer'
3	LOAD_FAST         'source'
6	CALL_FUNCTION_1   None
9	STORE_FAST        's'

12	LOAD_FAST         's'
15	LOAD_ATTR         'get'
18	STORE_FAST        'sget'

21	BUILD_LIST_0      None
24	STORE_FAST        'p'

27	LOAD_FAST         'p'
30	LOAD_ATTR         'append'
33	STORE_FAST        'a'

36	LOAD_FAST         'p'
39	LOAD_FAST         'a'
42	LOAD_CONST        '<code_object literal>'
45	MAKE_FUNCTION_2   None
48	STORE_FAST        'literal'

51	LOAD_FAST         'source'
54	LOAD_CONST        0
57	SLICE+2           None
58	STORE_FAST        'sep'

61	LOAD_GLOBAL       'type'
64	LOAD_FAST         'sep'
67	CALL_FUNCTION_1   None
70	LOAD_GLOBAL       'type'
73	LOAD_CONST        ''
76	CALL_FUNCTION_1   None
79	COMPARE_OP        'is'
82	JUMP_IF_FALSE     '94'

85	LOAD_GLOBAL       'chr'
88	STORE_FAST        'makechar'
91	JUMP_FORWARD      '100'

94	LOAD_GLOBAL       'unichr'
97	STORE_FAST        'makechar'
100_0	COME_FROM         '91'

100	SETUP_LOOP        '798'

103	LOAD_FAST         'sget'
106	CALL_FUNCTION_0   None
109	STORE_FAST        'this'

112	LOAD_FAST         'this'
115	LOAD_CONST        None
118	COMPARE_OP        'is'
121	JUMP_IF_FALSE     '128'

124	BREAK_LOOP        None
125	JUMP_FORWARD      '128'
128_0	COME_FROM         '125'

128	LOAD_FAST         'this'
131	JUMP_IF_FALSE     '784'
134	LOAD_FAST         'this'
137	LOAD_CONST        0
140	BINARY_SUBSCR     None
141	LOAD_CONST        '\\'
144	COMPARE_OP        '=='
147_0	COME_FROM         '131'
147	JUMP_IF_FALSE     '784'

150	LOAD_FAST         'this'
153	LOAD_CONST        1
156	LOAD_CONST        2
159	SLICE+3           None
160	STORE_FAST        'c'

163	LOAD_FAST         'c'
166	LOAD_CONST        'g'
169	COMPARE_OP        '=='
172	JUMP_IF_FALSE     '432'

175	LOAD_CONST        ''
178	STORE_FAST        'name'

181	LOAD_FAST         's'
184	LOAD_ATTR         'match'
187	LOAD_CONST        '<'
190	CALL_FUNCTION_1   None
193	JUMP_IF_FALSE     '265'

196	SETUP_LOOP        '265'

199	LOAD_FAST         'sget'
202	CALL_FUNCTION_0   None
205	STORE_FAST        'char'

208	LOAD_FAST         'char'
211	LOAD_CONST        None
214	COMPARE_OP        'is'
217	JUMP_IF_FALSE     '232'

220	LOAD_GLOBAL       'error'
223	LOAD_CONST        'unterminated group name'
226	RAISE_VARARGS_2   None
229	JUMP_FORWARD      '232'
232_0	COME_FROM         '229'

232	LOAD_FAST         'char'
235	LOAD_CONST        '>'
238	COMPARE_OP        '=='
241	JUMP_IF_FALSE     '248'

244	BREAK_LOOP        None
245	JUMP_FORWARD      '248'
248_0	COME_FROM         '245'

248	LOAD_FAST         'name'
251	LOAD_FAST         'char'
254	BINARY_ADD        None
255	STORE_FAST        'name'
258	JUMP_BACK         '199'
261	POP_BLOCK         None
262_0	COME_FROM         '196'
262	JUMP_FORWARD      '265'
265_0	COME_FROM         '262'

265	LOAD_FAST         'name'
268	JUMP_IF_TRUE      '283'

271	LOAD_GLOBAL       'error'
274	LOAD_CONST        'bad group name'
277	RAISE_VARARGS_2   None
280	JUMP_FORWARD      '283'
283_0	COME_FROM         '280'

283	SETUP_EXCEPT      '326'

286	LOAD_GLOBAL       'int'
289	LOAD_FAST         'name'
292	CALL_FUNCTION_1   None
295	STORE_FAST        'index'

298	LOAD_FAST         'index'
301	LOAD_CONST        0
304	COMPARE_OP        '<'
307	JUMP_IF_FALSE     '322'

310	LOAD_GLOBAL       'error'
313	LOAD_CONST        'negative group number'
316	RAISE_VARARGS_2   None
319	JUMP_FORWARD      '322'
322_0	COME_FROM         '319'
322	POP_BLOCK         None
323	JUMP_FORWARD      '413'
326_0	COME_FROM         '283'

326	DUP_TOP           None
327	LOAD_GLOBAL       'ValueError'
330	COMPARE_OP        'exception match'
333	JUMP_IF_FALSE     '412'
336	POP_TOP           None
337	POP_TOP           None
338	POP_TOP           None

339	LOAD_GLOBAL       'isname'
342	LOAD_FAST         'name'
345	CALL_FUNCTION_1   None
348	JUMP_IF_TRUE      '363'

351	LOAD_GLOBAL       'error'
354	LOAD_CONST        'bad character in group name'
357	RAISE_VARARGS_2   None
360	JUMP_FORWARD      '363'
363_0	COME_FROM         '360'

363	SETUP_EXCEPT      '383'

366	LOAD_FAST         'pattern'
369	LOAD_ATTR         'groupindex'
372	LOAD_FAST         'name'
375	BINARY_SUBSCR     None
376	STORE_FAST        'index'
379	POP_BLOCK         None
380	JUMP_ABSOLUTE     '413'
383_0	COME_FROM         '363'

383	DUP_TOP           None
384	LOAD_GLOBAL       'KeyError'
387	COMPARE_OP        'exception match'
390	JUMP_IF_FALSE     '408'
393	POP_TOP           None
394	POP_TOP           None
395	POP_TOP           None

396	LOAD_GLOBAL       'IndexError'
399	LOAD_CONST        'unknown group name'
402	RAISE_VARARGS_2   None
405	JUMP_ABSOLUTE     '413'
408	END_FINALLY       None
409_0	COME_FROM         '408'
409	JUMP_FORWARD      '413'
412	END_FINALLY       None
413_0	COME_FROM         '323'
413_1	COME_FROM         '412'

413	LOAD_FAST         'a'
416	LOAD_GLOBAL       'MARK'
419	LOAD_FAST         'index'
422	BUILD_TUPLE_2     None
425	CALL_FUNCTION_1   None
428	POP_TOP           None
429	JUMP_ABSOLUTE     '794'

432	LOAD_FAST         'c'
435	LOAD_CONST        '0'
438	COMPARE_OP        '=='
441	JUMP_IF_FALSE     '542'

444	LOAD_FAST         's'
447	LOAD_ATTR         'next'
450	LOAD_GLOBAL       'OCTDIGITS'
453	COMPARE_OP        'in'
456	JUMP_IF_FALSE     '506'

459	LOAD_FAST         'this'
462	LOAD_FAST         'sget'
465	CALL_FUNCTION_0   None
468	BINARY_ADD        None
469	STORE_FAST        'this'

472	LOAD_FAST         's'
475	LOAD_ATTR         'next'
478	LOAD_GLOBAL       'OCTDIGITS'
481	COMPARE_OP        'in'
484	JUMP_IF_FALSE     '503'

487	LOAD_FAST         'this'
490	LOAD_FAST         'sget'
493	CALL_FUNCTION_0   None
496	BINARY_ADD        None
497	STORE_FAST        'this'
500	JUMP_ABSOLUTE     '506'
503	JUMP_FORWARD      '506'
506_0	COME_FROM         '503'

506	LOAD_FAST         'literal'
509	LOAD_FAST         'makechar'
512	LOAD_GLOBAL       'int'
515	LOAD_FAST         'this'
518	LOAD_CONST        1
521	SLICE+1           None
522	LOAD_CONST        8
525	CALL_FUNCTION_2   None
528	LOAD_CONST        255
531	BINARY_AND        None
532	CALL_FUNCTION_1   None
535	CALL_FUNCTION_1   None
538	POP_TOP           None
539	JUMP_ABSOLUTE     '794'

542	LOAD_FAST         'c'
545	LOAD_GLOBAL       'DIGITS'
548	COMPARE_OP        'in'
551	JUMP_IF_FALSE     '727'

554	LOAD_GLOBAL       'False'
557	STORE_FAST        'isoctal'

560	LOAD_FAST         's'
563	LOAD_ATTR         'next'
566	LOAD_GLOBAL       'DIGITS'
569	COMPARE_OP        'in'
572	JUMP_IF_FALSE     '689'

575	LOAD_FAST         'this'
578	LOAD_FAST         'sget'
581	CALL_FUNCTION_0   None
584	BINARY_ADD        None
585	STORE_FAST        'this'

588	LOAD_FAST         'c'
591	LOAD_GLOBAL       'OCTDIGITS'
594	COMPARE_OP        'in'
597	JUMP_IF_FALSE     '686'
600	LOAD_FAST         'this'
603	LOAD_CONST        2
606	BINARY_SUBSCR     None
607	LOAD_GLOBAL       'OCTDIGITS'
610	COMPARE_OP        'in'
613	JUMP_IF_FALSE     '686'
616	LOAD_FAST         's'
619	LOAD_ATTR         'next'
622	LOAD_GLOBAL       'OCTDIGITS'
625	COMPARE_OP        'in'
628_0	COME_FROM         '597'
628_1	COME_FROM         '613'
628	JUMP_IF_FALSE     '686'

631	LOAD_FAST         'this'
634	LOAD_FAST         'sget'
637	CALL_FUNCTION_0   None
640	BINARY_ADD        None
641	STORE_FAST        'this'

644	LOAD_GLOBAL       'True'
647	STORE_FAST        'isoctal'

650	LOAD_FAST         'literal'
653	LOAD_FAST         'makechar'
656	LOAD_GLOBAL       'int'
659	LOAD_FAST         'this'
662	LOAD_CONST        1
665	SLICE+1           None
666	LOAD_CONST        8
669	CALL_FUNCTION_2   None
672	LOAD_CONST        255
675	BINARY_AND        None
676	CALL_FUNCTION_1   None
679	CALL_FUNCTION_1   None
682	POP_TOP           None
683	JUMP_ABSOLUTE     '689'
686	JUMP_FORWARD      '689'
689_0	COME_FROM         '686'

689	LOAD_FAST         'isoctal'
692	JUMP_IF_TRUE      '724'

695	LOAD_FAST         'a'
698	LOAD_GLOBAL       'MARK'
701	LOAD_GLOBAL       'int'
704	LOAD_FAST         'this'
707	LOAD_CONST        1
710	SLICE+1           None
711	CALL_FUNCTION_1   None
714	BUILD_TUPLE_2     None
717	CALL_FUNCTION_1   None
720	POP_TOP           None
721	JUMP_ABSOLUTE     '781'
724	JUMP_ABSOLUTE     '794'

727	SETUP_EXCEPT      '754'

730	LOAD_FAST         'makechar'
733	LOAD_GLOBAL       'ESCAPES'
736	LOAD_FAST         'this'
739	BINARY_SUBSCR     None
740	LOAD_CONST        1
743	BINARY_SUBSCR     None
744	CALL_FUNCTION_1   None
747	STORE_FAST        'this'
750	POP_BLOCK         None
751	JUMP_FORWARD      '771'
754_0	COME_FROM         '727'

754	DUP_TOP           None
755	LOAD_GLOBAL       'KeyError'
758	COMPARE_OP        'exception match'
761	JUMP_IF_FALSE     '770'
764	POP_TOP           None
765	POP_TOP           None
766	POP_TOP           None

767	JUMP_FORWARD      '771'
770	END_FINALLY       None
771_0	COME_FROM         '751'
771_1	COME_FROM         '770'

771	LOAD_FAST         'literal'
774	LOAD_FAST         'this'
777	CALL_FUNCTION_1   None
780	POP_TOP           None
781	JUMP_BACK         '103'

784	LOAD_FAST         'literal'
787	LOAD_FAST         'this'
790	CALL_FUNCTION_1   None
793	POP_TOP           None
794	JUMP_BACK         '103'
797	POP_BLOCK         None
798_0	COME_FROM         '100'

798	LOAD_CONST        0
801	STORE_FAST        'i'

804	BUILD_LIST_0      None
807	STORE_FAST        'groups'

810	LOAD_FAST         'groups'
813	LOAD_ATTR         'append'
816	STORE_FAST        'groupsappend'

819	LOAD_CONST        None
822	BUILD_LIST_1      None
825	L
# Can't uncompyle C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\sre_parse.pyc
Traceback (most recent call last):
  File "C:\python27\lib\uncompyle2\__init__.py", line 206, in main
    uncompyle_file(infile, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 143, in uncompyle_file
    uncompyle(version, co, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 132, in uncompyle
    raise walk.ERROR
ParserError: --- This code section failed: ---

0	LOAD_GLOBAL       'Tokenizer'
3	LOAD_FAST         'source'
6	CALL_FUNCTION_1   None
9	STORE_FAST        's'

12	LOAD_FAST         's'
15	LOAD_ATTR         'get'
18	STORE_FAST        'sget'

21	BUILD_LIST_0      None
24	STORE_FAST        'p'

27	LOAD_FAST         'p'
30	LOAD_ATTR         'append'
33	STORE_FAST        'a'

36	LOAD_FAST         'p'
39	LOAD_FAST         'a'
42	LOAD_CONST        '<code_object literal>'
45	MAKE_FUNCTION_2   None
48	STORE_FAST        'literal'

51	LOAD_FAST         'source'
54	LOAD_CONST        0
57	SLICE+2           None
58	STORE_FAST        'sep'

61	LOAD_GLOBAL       'type'
64	LOAD_FAST         'sep'
67	CALL_FUNCTION_1   None
70	LOAD_GLOBAL       'type'
73	LOAD_CONST        ''
76	CALL_FUNCTION_1   None
79	COMPARE_OP        'is'
82	JUMP_IF_FALSE     '94'

85	LOAD_GLOBAL       'chr'
88	STORE_FAST        'makechar'
91	JUMP_FORWARD      '100'

94	LOAD_GLOBAL       'unichr'
97	STORE_FAST        'makechar'
100_0	COME_FROM         '91'

100	SETUP_LOOP        '798'

103	LOAD_FAST         'sget'
106	CALL_FUNCTION_0   None
109	STORE_FAST        'this'

112	LOAD_FAST         'this'
115	LOAD_CONST        None
118	COMPARE_OP        'is'
121	JUMP_IF_FALSE     '128'

124	BREAK_LOOP        None
125	JUMP_FORWARD      '128'
128_0	COME_FROM         '125'

128	LOAD_FAST         'this'
131	JUMP_IF_FALSE     '784'
134	LOAD_FAST         'this'
137	LOAD_CONST        0
140	BINARY_SUBSCR     None
141	LOAD_CONST        '\\'
144	COMPARE_OP        '=='
147_0	COME_FROM         '131'
147	JUMP_IF_FALSE     '784'

150	LOAD_FAST         'this'
153	LOAD_CONST        1
156	LOAD_CONST        2
159	SLICE+3           None
160	STORE_FAST        'c'

163	LOAD_FAST         'c'
166	LOAD_CONST        'g'
169	COMPARE_OP        '=='
172	JUMP_IF_FALSE     '432'

175	LOAD_CONST        ''
178	STORE_FAST        'name'

181	LOAD_FAST         's'
184	LOAD_ATTR         'match'
187	LOAD_CONST        '<'
190	CALL_FUNCTION_1   None
193	JUMP_IF_FALSE     '265'

196	SETUP_LOOP        '265'

199	LOAD_FAST         'sget'
202	CALL_FUNCTION_0   None
205	STORE_FAST        'char'

208	LOAD_FAST         'char'
211	LOAD_CONST        None
214	COMPARE_OP        'is'
217	JUMP_IF_FALSE     '232'

220	LOAD_GLOBAL       'error'
223	LOAD_CONST        'unterminated group name'
226	RAISE_VARARGS_2   None
229	JUMP_FORWARD      '232'
232_0	COME_FROM         '229'

232	LOAD_FAST         'char'
235	LOAD_CONST        '>'
238	COMPARE_OP        '=='
241	JUMP_IF_FALSE     '248'

244	BREAK_LOOP        None
245	JUMP_FORWARD      '248'
248_0	COME_FROM         '245'

248	LOAD_FAST         'name'
251	LOAD_FAST         'char'
254	BINARY_ADD        None
255	STORE_FAST        'name'
258	JUMP_BACK         '199'
261	POP_BLOCK         None
262_0	COME_FROM         '196'
262	JUMP_FORWARD      '265'
265_0	COME_FROM         '262'

265	LOAD_FAST         'name'
268	JUMP_IF_TRUE      '283'

271	LOAD_GLOBAL       'error'
274	LOAD_CONST        'bad group name'
277	RAISE_VARARGS_2   None
280	JUMP_FORWARD      '283'
283_0	COME_FROM         '280'

283	SETUP_EXCEPT      '326'

286	LOAD_GLOBAL       'int'
289	LOAD_FAST         'name'
292	CALL_FUNCTION_1   None
295	STORE_FAST        'index'

298	LOAD_FAST         'index'
301	LOAD_CONST        0
304	COMPARE_OP        '<'
307	JUMP_IF_FALSE     '322'

310	LOAD_GLOBAL       'error'
313	LOAD_CONST        'negative group number'
316	RAISE_VARARGS_2   None
319	JUMP_FORWARD      '322'
322_0	COME_FROM         '319'
322	POP_BLOCK         None
323	JUMP_FORWARD      '413'
326_0	COME_FROM         '283'

326	DUP_TOP           None
327	LOAD_GLOBAL       'ValueError'
330	COMPARE_OP        'exception match'
333	JUMP_IF_FALSE     '412'
336	POP_TOP           None
337	POP_TOP           None
338	POP_TOP           None

339	LOAD_GLOBAL       'isname'
342	LOAD_FAST         'name'
345	CALL_FUNCTION_1   None
348	JUMP_IF_TRUE      '363'

351	LOAD_GLOBAL       'error'
354	LOAD_CONST        'bad character in group name'
357	RAISE_VARARGS_2   None
360	JUMP_FORWARD      '363'
363_0	COME_FROM         '360'

363	SETUP_EXCEPT      '383'

366	LOAD_FAST         'pattern'
369	LOAD_ATTR         'groupindex'
372	LOAD_FAST         'name'
375	BINARY_SUBSCR     None
376	STORE_FAST        'index'
379	POP_BLOCK         None
380	JUMP_ABSOLUTE     '413'
383_0	COME_FROM         '363'

383	DUP_TOP           None
384	LOAD_GLOBAL       'KeyError'
387	COMPARE_OP        'exception match'
390	JUMP_IF_FALSE     '408'
393	POP_TOP           None
394	POP_TOP           None
395	POP_TOP           None

396	LOAD_GLOBAL       'IndexError'
399	LOAD_CONST        'unknown group name'
402	RAISE_VARARGS_2   None
405	JUMP_ABSOLUTE     '413'
408	END_FINALLY       None
409_0	COME_FROM         '408'
409	JUMP_FORWARD      '413'
412	END_FINALLY       None
413_0	COME_FROM         '323'
413_1	COME_FROM         '412'

413	LOAD_FAST         'a'
416	LOAD_GLOBAL       'MARK'
419	LOAD_FAST         'index'
422	BUILD_TUPLE_2     None
425	CALL_FUNCTION_1   None
428	POP_TOP           None
429	JUMP_ABSOLUTE     '794'

432	LOAD_FAST         'c'
435	LOAD_CONST        '0'
438	COMPARE_OP        '=='
441	JUMP_IF_FALSE     '542'

444	LOAD_FAST         's'
447	LOAD_ATTR         'next'
450	LOAD_GLOBAL       'OCTDIGITS'
453	COMPARE_OP        'in'
456	JUMP_IF_FALSE     '506'

459	LOAD_FAST         'this'
462	LOAD_FAST         'sget'
465	CALL_FUNCTION_0   None
468	BINARY_ADD        None
469	STORE_FAST        'this'

472	LOAD_FAST         's'
475	LOAD_ATTR         'next'
478	LOAD_GLOBAL       'OCTDIGITS'
481	COMPARE_OP        'in'
484	JUMP_IF_FALSE     '503'

487	LOAD_FAST         'this'
490	LOAD_FAST         'sget'
493	CALL_FUNCTION_0   None
496	BINARY_ADD        None
497	STORE_FAST        'this'
500	JUMP_ABSOLUTE     '506'
503	JUMP_FORWARD      '506'
506_0	COME_FROM         '503'

506	LOAD_FAST         'literal'
509	LOAD_FAST         'makechar'
512	LOAD_GLOBAL       'int'
515	LOAD_FAST         'this'
518	LOAD_CONST        1
521	SLICE+1           None
522	LOAD_CONST        8
525	CALL_FUNCTION_2   None
528	LOAD_CONST        255
531	BINARY_AND        None
532	CALL_FUNCTION_1   None
535	CALL_FUNCTION_1   None
538	POP_TOP           None
539	JUMP_ABSOLUTE     '794'

542	LOAD_FAST         'c'
545	LOAD_GLOBAL       'DIGITS'
548	COMPARE_OP        'in'
551	JUMP_IF_FALSE     '727'

554	LOAD_GLOBAL       'False'
557	STORE_FAST        'isoctal'

560	LOAD_FAST         's'
563	LOAD_ATTR         'next'
566	LOAD_GLOBAL       'DIGITS'
569	COMPARE_OP        'in'
572	JUMP_IF_FALSE     '689'

575	LOAD_FAST         'this'
578	LOAD_FAST         'sget'
581	CALL_FUNCTION_0   None
584	BINARY_ADD        None
585	STORE_FAST        'this'

588	LOAD_FAST         'c'
591	LOAD_GLOBAL       'OCTDIGITS'
594	COMPARE_OP        'in'
597	JUMP_IF_FALSE     '686'
600	LOAD_FAST         'this'
603	LOAD_CONST        2
606	BINARY_SUBSCR     None
607	LOAD_GLOBAL       'OCTDIGITS'
610	COMPARE_OP        'in'
613	JUMP_IF_FALSE     '686'
616	LOAD_FAST         's'
619	LOAD_ATTR         'next'
622	LOAD_GLOBAL       'OCTDIGITS'
625	COMPARE_OP        'in'
628_0	COME_FROM         '597'
628_1	COME_FROM         '613'
628	JUMP_IF_FALSE     '686'

631	LOAD_FAST         'this'
634	LOAD_FAST         'sget'
637	CALL_FUNCTION_0   None
640	BINARY_ADD        None
641	STORE_FAST        'this'

644	LOAD_GLOBAL       'True'
647	STORE_FAST        'isoctal'

650	LOAD_FAST         'literal'
653	LOAD_FAST         'makechar'
656	LOAD_GLOBAL       'int'
659	LOAD_FAST         'this'
662	LOAD_CONST        1
665	SLICE+1           None
666	LOAD_CONST        8
669	CALL_FUNCTION_2   None
672	LOAD_CONST        255
675	BINARY_AND        None
676	CALL_FUNCTION_1   None
679	CALL_FUNCTION_1   None
682	POP_TOP  OAD_GLOBAL       'len'
828	LOAD_FAST         'p'
831	CALL_FUNCTION_1   None
834	BINARY_MULTIPLY   None
835	STORE_FAST        'literals'

838	SETUP_LOOP        '912'
841	LOAD_FAST         'p'
844	GET_ITER          None
845	FOR_ITER          '911'
848	UNPACK_SEQUENCE_2 None
851	STORE_FAST        'c'
854	STORE_FAST        's'

857	LOAD_FAST         'c'
860	LOAD_GLOBAL       'MARK'
863	COMPARE_OP        'is'
866	JUMP_IF_FALSE     '888'

869	LOAD_FAST         'groupsappend'
872	LOAD_FAST         'i'
875	LOAD_FAST         's'
878	BUILD_TUPLE_2     None
881	CALL_FUNCTION_1   None
884	POP_TOP           None
885	JUMP_FORWARD      '898'

888	LOAD_FAST         's'
891	LOAD_FAST         'literals'
894	LOAD_FAST         'i'
897	STORE_SUBSCR      None
898_0	COME_FROM         '885'

898	LOAD_FAST         'i'
901	LOAD_CONST        1
904	BINARY_ADD        None
905	STORE_FAST        'i'
908	JUMP_BACK         '845'
911	POP_BLOCK         None
912_0	COME_FROM         '838'

912	LOAD_FAST         'groups'
915	LOAD_FAST         'literals'
918	BUILD_TUPLE_2     None
921	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 261


def expand_template(template, match):
    g = match.group
    sep = match.string[:0]
    groups, literals = template
    literals = literals[:]
    try:
        for index, group in groups:
            literals[index] = s = g(group)
            if s is None:
                raise error, 'unmatched group'

    except IndexError:
        raise error, 'invalid group reference'

    return sep.join(literals)# decompiled 0 files: 0 okay, 1 failed, 0 verify failed
# 2013.08.22 22:13:32 Pacific Daylight Time
         None
683	JUMP_ABSOLUTE     '689'
686	JUMP_FORWARD      '689'
689_0	COME_FROM         '686'

689	LOAD_FAST         'isoctal'
692	JUMP_IF_TRUE      '724'

695	LOAD_FAST         'a'
698	LOAD_GLOBAL       'MARK'
701	LOAD_GLOBAL       'int'
704	LOAD_FAST         'this'
707	LOAD_CONST        1
710	SLICE+1           None
711	CALL_FUNCTION_1   None
714	BUILD_TUPLE_2     None
717	CALL_FUNCTION_1   None
720	POP_TOP           None
721	JUMP_ABSOLUTE     '781'
724	JUMP_ABSOLUTE     '794'

727	SETUP_EXCEPT      '754'

730	LOAD_FAST         'makechar'
733	LOAD_GLOBAL       'ESCAPES'
736	LOAD_FAST         'this'
739	BINARY_SUBSCR     None
740	LOAD_CONST        1
743	BINARY_SUBSCR     None
744	CALL_FUNCTION_1   None
747	STORE_FAST        'this'
750	POP_BLOCK         None
751	JUMP_FORWARD      '771'
754_0	COME_FROM         '727'

754	DUP_TOP           None
755	LOAD_GLOBAL       'KeyError'
758	COMPARE_OP        'exception match'
761	JUMP_IF_FALSE     '770'
764	POP_TOP           None
765	POP_TOP           None
766	POP_TOP           None

767	JUMP_FORWARD      '771'
770	END_FINALLY       None
771_0	COME_FROM         '751'
771_1	COME_FROM         '770'

771	LOAD_FAST         'literal'
774	LOAD_FAST         'this'
777	CALL_FUNCTION_1   None
780	POP_TOP           None
781	JUMP_BACK         '103'

784	LOAD_FAST         'literal'
787	LOAD_FAST         'this'
790	CALL_FUNCTION_1   None
793	POP_TOP           None
794	JUMP_BACK         '103'
797	POP_BLOCK         None
798_0	COME_FROM         '100'

798	LOAD_CONST        0
801	STORE_FAST        'i'

804	BUILD_LIST_0      None
807	STORE_FAST        'groups'

810	LOAD_FAST         'groups'
813	LOAD_ATTR         'append'
816	STORE_FAST        'groupsappend'

819	LOAD_CONST        None
822	BUILD_LIST_1      None
825	LOAD_GLOBAL       'len'
828	LOAD_FAST         'p'
831	CALL_FUNCTION_1   None
834	BINARY_MULTIPLY   None
835	STORE_FAST        'literals'

838	SETUP_LOOP        '912'
841	LOAD_FAST         'p'
844	GET_ITER          None
845	FOR_ITER          '911'
848	UNPACK_SEQUENCE_2 None
851	STORE_FAST        'c'
854	STORE_FAST        's'

857	LOAD_FAST         'c'
860	LOAD_GLOBAL       'MARK'
863	COMPARE_OP        'is'
866	JUMP_IF_FALSE     '888'

869	LOAD_FAST         'groupsappend'
872	LOAD_FAST         'i'
875	LOAD_FAST         's'
878	BUILD_TUPLE_2     None
881	CALL_FUNCTION_1   None
884	POP_TOP           None
885	JUMP_FORWARD      '898'

888	LOAD_FAST         's'
891	LOAD_FAST         'literals'
894	LOAD_FAST         'i'
897	STORE_SUBSCR      None
898_0	COME_FROM         '885'

898	LOAD_FAST         'i'
901	LOAD_CONST        1
904	BINARY_ADD        None
905	STORE_FAST        'i'
908	JUMP_BACK         '845'
911	POP_BLOCK         None
912_0	COME_FROM         '838'

912	LOAD_FAST         'groups'
915	LOAD_FAST         'literals'
918	BUILD_TUPLE_2     None
921	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 261

