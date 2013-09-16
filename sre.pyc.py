# 2013.08.22 22:13:29 Pacific Daylight Time
# Embedded file name: sre
import sys
import sre_compile
import sre_parse
__all__ = ['match',
 'search',
 'sub',
 'subn',
 'split',
 'findall',
 'compile',
 'purge',
 'template',
 'escape',
 'I',
 'L',
 'M',
 'S',
 'X',
 'U',
 'IGNORECASE',
 'LOCALE',
 'MULTILINE',
 'DOTALL',
 'VERBOSE',
 'UNICODE',
 'error']
__version__ = '2.2.1'
I = IGNORECASE = sre_compile.SRE_FLAG_IGNORECASE
L = LOCALE = sre_compile.SRE_FLAG_LOCALE
U = UNICODE = sre_compile.SRE_FLAG_UNICODE
M = MULTILINE = sre_compile.SRE_FLAG_MULTILINE
S = DOTALL = sre_compile.SRE_FLAG_DOTALL
X = VERBOSE = sre_compile.SRE_FLAG_VERBOSE
T = TEMPLATE = sre_compile.SRE_FLAG_TEMPLATE
DEBUG = sre_compile.SRE_FLAG_DEBUG
error = sre_compile.error

def match(pattern, string, flags = 0):
    return _compile(pattern, flags).match(string)


def search(pattern, string, flags = 0):
    return _compile(pattern, flags).search(string)


def sub(pattern, repl, string, count = 0):
    return _compile(pattern, 0).sub(repl, string, count)


def subn(pattern, repl, string, count = 0):
    return _compile(pattern, 0).subn(repl, string, count)


def split(pattern, string, maxsplit = 0):
    return _compile(pattern, 0).split(string, maxsplit)


def findall(pattern, string, flags = 0):
    return _compile(pattern, flags).findall(string)


if sys.hexversion >= 33685504:
    __all__.append('finditer')

    def finditer(pattern, string, flags = 0):
        return _compile(pattern, flags).finditer(string)


def compile(pattern, flags = 0):
    return _compile(pattern, flags)


def purge():
    _cache.clear()
    _cache_repl.clear()


def template(pattern, flags = 0):
    return _compile(pattern, flags | T)


def escape(pattern):
    s = list(pattern)
    for i in range(len(pattern)):
        c = pattern[i]
        if not ('a' <= c <= 'z' or 'A') <= c <= 'Z':
            if not '0' <= c <= '9':
                s[i] = c == '\x00' and '\\000'
            else:
                s[i] = '\\' + c

    return pattern[:0].join(s)


_cache = {}
_cache_repl = {}
_pattern_type = type(sre_compile.compile('', 0))
_MAXCACHE = 100

def _compile(*key):
    cachekey = (type(key[0]),) + key
    p = _cache.get(cachekey)
    if p is not None:
        return p
    pattern, flags = key
    if isinstance(pattern, _pattern_type):
        return pattern
    if not sre_compile.isstring(pattern):
        raise TypeError, 'first argument must be string or compiled pattern'
    try:
        p = sre_compile.compile(pattern, flags)
    except error as v:
        raise error, v

    if len(_cache) >= _MAXCACHE:
        _cache.clear()
    _cache[cachekey] = p
    return p


def _compile_repl(*key):
    p = _cache_repl.get(key)
    if p is not None:
        return p
    repl, pattern = key
    try:
        p = sre_parse.parse_template(repl, pattern)
    except error as v:
        raise error, v

    if len(_cache_repl) >= _MAXCACHE:
        _cache_repl.clear()
    _cache_repl[key] = p
    return p


def _expand(pattern, match, template):
    template = sre_parse.parse_template(template, pattern)
    return sre_parse.expand_template(template, match)


def _subx(pattern, template):
    template = _compile_repl(template, pattern)
    if not template[0] and len(template[1]) == 1:
        return template[1][0]

    def filter(match, template = template):
        return sre_parse.expand_template(template, match)

    return filter


import copy_reg

def _pickle(p):
    return (_compile, (p.pattern, p.flags))


copy_reg.pickle(_pattern_type, _pickle, _compile)

class Scanner():
    __module__ = __name__

    def __init__(self, lexicon, flags = 0):
        from sre_constants import BRANCH, SUBPATTERN
        self.lexicon = lexicon
        p = []
        s = sre_parse.Pattern()
        s.flags = flags
        for phrase, action in lexicon:
            p.append(sre_parse.SubPattern(s, [(SUBPATTERN, (len(p) + 1, sre_parse.parse(phrase, flags)))]))

        p = sre_parse.SubPattern(s, [(BRANCH, (None, p))])
        s.groups = len(p)
        self.scanner = sre_compile.compile(p)
        return

    def scan--- This code section failed: ---

0	BUILD_LIST_0      None
3	STORE_FAST        'result'

6	LOAD_FAST         'result'
9	LOAD_ATTR         'append'
12	STORE_FAST        'append'

15	LOAD_FAST         'self'
18	LOAD_ATTR         'scanner'
21	LOAD_ATTR         'scanner'
24	LOAD_FAST         'string'
27	CALL_FUNCTION_1   None
30	LOAD_ATTR         'match'
33	STORE_FAST        'match'

36	LOAD_CONST        0
39	STORE_FAST        'i'

42	SETUP_LOOP        '196'

45	LOAD_FAST         'match'
48	CALL_FUNCTION_0   None
51	STORE_FAST        'm'

54	LOAD_FAST         'm'
57	JUMP_IF_TRUE      '64'

60	BREAK_LOOP        None
61	JUMP_FORWARD      '64'
64_0	COME_FROM         '61'

64	LOAD_FAST         'm'
67	LOAD_ATTR         'end'
70	CALL_FUNCTION_0   None
73	STORE_FAST        'j'

76	LOAD_FAST         'i'
79	LOAD_FAST         'j'
82	COMPARE_OP        '=='
85	JUMP_IF_FALSE     '92'

88	BREAK_LOOP        None
89	JUMP_FORWARD      '92'
92_0	COME_FROM         '89'

92	LOAD_FAST         'self'
95	LOAD_ATTR         'lexicon'
98	LOAD_FAST         'm'
101	LOAD_ATTR         'lastindex'
104	LOAD_CONST        1
107	BINARY_SUBTRACT   None
108	BINARY_SUBSCR     None
109	LOAD_CONST        1
112	BINARY_SUBSCR     None
113	STORE_FAST        'action'

116	LOAD_GLOBAL       'callable'
119	LOAD_FAST         'action'
122	CALL_FUNCTION_1   None
125	JUMP_IF_FALSE     '161'

128	LOAD_FAST         'm'
131	LOAD_FAST         'self'
134	STORE_ATTR        'match'

137	LOAD_FAST         'action'
140	LOAD_FAST         'self'
143	LOAD_FAST         'm'
146	LOAD_ATTR         'group'
149	CALL_FUNCTION_0   None
152	CALL_FUNCTION_2   None
155	STORE_FAST        'action'
158	JUMP_FORWARD      '161'
161_0	COME_FROM         '158'

161	LOAD_FAST         'action'
164	LOAD_CONST        None
167	COMPARE_OP        'is not'
170	JUMP_IF_FALSE     '186'

173	LOAD_FAST         'append'
176	LOAD_FAST         'action'
179	CALL_FUNCTION_1   None
182	POP_TOP           None
183	JUMP_FORWARD      '186'
186_0	COME_FROM         '183'

186	LOAD_FAST         'j'
189	STORE_FAST        'i'
192	JUMP_BACK         '45'
195	POP_BLOCK         None
196_0	COME_FROM         '42'

196	LOAD_FAST         'result'
199	LOAD_FAST         'string'
202	LOAD_FAST         'i'
205	SLICE+1           None
206	BUILD_TUPLE_2     None
209	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 195# decompiled 0 files: 0 okay, 1 failed, 0 verify failed
# 2013.08.22 22:13:30 Pacific Daylight Time

# Can't uncompyle C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\sre.pyc
Traceback (most recent call last):
  File "C:\python27\lib\uncompyle2\__init__.py", line 206, in main
    uncompyle_file(infile, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 143, in uncompyle_file
    uncompyle(version, co, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 132, in uncompyle
    raise walk.ERROR
ParserError: --- This code section failed: ---

0	BUILD_LIST_0      None
3	STORE_FAST        'result'

6	LOAD_FAST         'result'
9	LOAD_ATTR         'append'
12	STORE_FAST        'append'

15	LOAD_FAST         'self'
18	LOAD_ATTR         'scanner'
21	LOAD_ATTR         'scanner'
24	LOAD_FAST         'string'
27	CALL_FUNCTION_1   None
30	LOAD_ATTR         'match'
33	STORE_FAST        'match'

36	LOAD_CONST        0
39	STORE_FAST        'i'

42	SETUP_LOOP        '196'

45	LOAD_FAST         'match'
48	CALL_FUNCTION_0   None
51	STORE_FAST        'm'

54	LOAD_FAST         'm'
57	JUMP_IF_TRUE      '64'

60	BREAK_LOOP        None
61	JUMP_FORWARD      '64'
64_0	COME_FROM         '61'

64	LOAD_FAST         'm'
67	LOAD_ATTR         'end'
70	CALL_FUNCTION_0   None
73	STORE_FAST        'j'

76	LOAD_FAST         'i'
79	LOAD_FAST         'j'
82	COMPARE_OP        '=='
85	JUMP_IF_FALSE     '92'

88	BREAK_LOOP        None
89	JUMP_FORWARD      '92'
92_0	COME_FROM         '89'

92	LOAD_FAST         'self'
95	LOAD_ATTR         'lexicon'
98	LOAD_FAST         'm'
101	LOAD_ATTR         'lastindex'
104	LOAD_CONST        1
107	BINARY_SUBTRACT   None
108	BINARY_SUBSCR     None
109	LOAD_CONST        1
112	BINARY_SUBSCR     None
113	STORE_FAST        'action'

116	LOAD_GLOBAL       'callable'
119	LOAD_FAST         'action'
122	CALL_FUNCTION_1   None
125	JUMP_IF_FALSE     '161'

128	LOAD_FAST         'm'
131	LOAD_FAST         'self'
134	STORE_ATTR        'match'

137	LOAD_FAST         'action'
140	LOAD_FAST         'self'
143	LOAD_FAST         'm'
146	LOAD_ATTR         'group'
149	CALL_FUNCTION_0   None
152	CALL_FUNCTION_2   None
155	STORE_FAST        'action'
158	JUMP_FORWARD      '161'
161_0	COME_FROM         '158'

161	LOAD_FAST         'action'
164	LOAD_CONST        None
167	COMPARE_OP        'is not'
170	JUMP_IF_FALSE     '186'

173	LOAD_FAST         'append'
176	LOAD_FAST         'action'
179	CALL_FUNCTION_1   None
182	POP_TOP           None
183	JUMP_FORWARD      '186'
186_0	COME_FROM         '183'

186	LOAD_FAST         'j'
189	STORE_FAST        'i'
192	JUMP_BACK         '45'
195	POP_BLOCK         None
196_0	COME_FROM         '42'

196	LOAD_FAST         'result'
199	LOAD_FAST         'string'
202	LOAD_FAST         'i'
205	SLICE+1           None
206	BUILD_TUPLE_2     None
209	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 195

