# 2013.08.22 22:13:03 Pacific Daylight Time
# Embedded file name: gopherlib
__all__ = ['send_selector', 'send_query']
DEF_SELECTOR = '1/'
DEF_HOST = 'gopher.micro.umn.edu'
DEF_PORT = 70
A_TEXT = '0'
A_MENU = '1'
A_CSO = '2'
A_ERROR = '3'
A_MACBINHEX = '4'
A_PCBINHEX = '5'
A_UUENCODED = '6'
A_INDEX = '7'
A_TELNET = '8'
A_BINARY = '9'
A_DUPLICATE = '+'
A_SOUND = 's'
A_EVENT = 'e'
A_CALENDAR = 'c'
A_HTML = 'h'
A_TN3270 = 'T'
A_MIME = 'M'
A_IMAGE = 'I'
A_WHOIS = 'w'
A_QUERY = 'q'
A_GIF = 'g'
A_HTML = 'h'
A_WWW = 'w'
A_PLUS_IMAGE = ':'
A_PLUS_MOVIE = ';'
A_PLUS_SOUND = '<'
_names = dir()
_type_to_name_map = {}

def type_to_name(gtype):
    global _type_to_name_map
    if _type_to_name_map == {}:
        for name in _names:
            if name[:2] == 'A_':
                _type_to_name_map[eval(name)] = name[2:]

    if gtype in _type_to_name_map:
        return _type_to_name_map[gtype]
    return 'TYPE=%r' % (gtype,)


CRLF = '\r\n'
TAB = '\t'

def send_selector(selector, host, port = 0):
    import socket
    if not port:
        i = host.find(':')
        if i >= 0:
            host, port = host[:i], int(host[i + 1:])
    if not port:
        port = DEF_PORT
    elif type(port) == type(''):
        port = int(port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.sendall(selector + CRLF)
    s.shutdown(1)
    return s.makefile('rb')


def send_query(selector, query, host, port = 0):
    return send_selector(selector + '\t' + query, host, port)


def path_to_selector(path):
    if path == '/':
        return '/'
    else:
        return path[2:]


def path_to_datatype_name(path):
    if path == '/':
        return "TYPE='unknown'"
    else:
        return type_to_name(path[1])


def get_directory--- This code section failed: ---

0	BUILD_LIST_0      None
3	STORE_FAST        'entries'

6	SETUP_LOOP        '298'

9	LOAD_FAST         'f'
12	LOAD_ATTR         'readline'
15	CALL_FUNCTION_0   None
18	STORE_FAST        'line'

21	LOAD_FAST         'line'
24	JUMP_IF_TRUE      '36'

27	LOAD_CONST        '(Unexpected EOF from server)'
30	PRINT_ITEM        None
31	PRINT_NEWLINE_CONT None

32	BREAK_LOOP        None
33	JUMP_FORWARD      '36'
36_0	COME_FROM         '33'

36	LOAD_FAST         'line'
39	LOAD_CONST        -2
42	SLICE+1           None
43	LOAD_GLOBAL       'CRLF'
46	COMPARE_OP        '=='
49	JUMP_IF_FALSE     '65'

52	LOAD_FAST         'line'
55	LOAD_CONST        -2
58	SLICE+2           None
59	STORE_FAST        'line'
62	JUMP_FORWARD      '94'

65	LOAD_FAST         'line'
68	LOAD_CONST        -1
71	SLICE+1           None
72	LOAD_GLOBAL       'CRLF'
75	COMPARE_OP        'in'
78	JUMP_IF_FALSE     '94'

81	LOAD_FAST         'line'
84	LOAD_CONST        -1
87	SLICE+2           None
88	STORE_FAST        'line'
91	JUMP_FORWARD      '94'
94_0	COME_FROM         '62'
94_1	COME_FROM         '91'

94	LOAD_FAST         'line'
97	LOAD_CONST        '.'
100	COMPARE_OP        '=='
103	JUMP_IF_FALSE     '110'

106	BREAK_LOOP        None
107	JUMP_FORWARD      '110'
110_0	COME_FROM         '107'

110	LOAD_FAST         'line'
113	JUMP_IF_TRUE      '127'

116	LOAD_CONST        '(Empty line from server)'
119	PRINT_ITEM        None
120	PRINT_NEWLINE_CONT None

121	CONTINUE          '9'
124	JUMP_FORWARD      '127'
127_0	COME_FROM         '124'

127	LOAD_FAST         'line'
130	LOAD_CONST        0
133	BINARY_SUBSCR     None
134	STORE_FAST        'gtype'

137	LOAD_FAST         'line'
140	LOAD_CONST        1
143	SLICE+1           None
144	LOAD_ATTR         'split'
147	LOAD_GLOBAL       'TAB'
150	CALL_FUNCTION_1   None
153	STORE_FAST        'parts'

156	LOAD_GLOBAL       'len'
159	LOAD_FAST         'parts'
162	CALL_FUNCTION_1   None
165	LOAD_CONST        4
168	COMPARE_OP        '<'
171	JUMP_IF_FALSE     '192'

174	LOAD_CONST        '(Bad line from server: %r)'
177	LOAD_FAST         'line'
180	BUILD_TUPLE_1     None
183	BINARY_MODULO     None
184	PRINT_ITEM        None
185	PRINT_NEWLINE_CONT None

186	CONTINUE          '9'
189	JUMP_FORWARD      '192'
192_0	COME_FROM         '189'

192	LOAD_GLOBAL       'len'
195	LOAD_FAST         'parts'
198	CALL_FUNCTION_1   None
201	LOAD_CONST        4
204	COMPARE_OP        '>'
207	JUMP_IF_FALSE     '252'

210	LOAD_FAST         'parts'
213	LOAD_CONST        4
216	SLICE+1           None
217	LOAD_CONST        '+'
220	BUILD_LIST_1      None
223	COMPARE_OP        '!='
226	JUMP_IF_FALSE     '249'

229	LOAD_CONST        '(Extra info from server:'
232	PRINT_ITEM        None

233	LOAD_FAST         'parts'
236	LOAD_CONST        4
239	SLICE+1           None
240	PRINT_ITEM        None
241	LOAD_CONST        ')'
244	PRINT_ITEM_CONT   None
245	PRINT_NEWLINE_CONT None
246	JUMP_ABSOLUTE     '265'
249	JUMP_FORWARD      '265'

252	LOAD_FAST         'parts'
255	LOAD_ATTR         'append'
258	LOAD_CONST        ''
261	CALL_FUNCTION_1   None
264	POP_TOP           None
265_0	COME_FROM         '249'

265	LOAD_FAST         'parts'
268	LOAD_ATTR         'insert'
271	LOAD_CONST        0
274	LOAD_FAST         'gtype'
277	CALL_FUNCTION_2   None
280	POP_TOP           None

281	LOAD_FAST         'entries'
284	LOAD_ATTR         'append'
287	LOAD_FAST         'parts'
290	CALL_FUNCTION_1   None
293	POP_TOP           None
294	JUMP_BACK         '9'
297	POP_BLOCK         None
298_0	COME_FROM         '6'

298	LOAD_FAST         'entries'
301	RETURN_VALUE      None
-1	RETURN_LAST       None

Syntax error at or near `POP_BLOCK' token at offset 297


def get_textfile(f):
    lines = []
    get_alt_textfile(f, lines.append)
    return lines


def get_alt_textfile--- This code section failed: ---

0	SETUP_LOOP        '147'

3	LOAD_FAST         'f'
6	LOAD_ATTR         'readline'
9	CALL_FUNCTION_0   None
12	STORE_FAST        'line'

15	LOAD_FAST         'line'
18	JUMP_IF_TRUE      '30'

21	LOAD_CONST        '(Unexpected EOF from server)'
24	PRINT_ITEM        None
25	PRINT_NEWLINE_CONT None

26	BREAK_LOOP        None
27	JUMP_FORWARD      '30'
30_0	COME_FROM         '27'

30	LOAD_FAST         'line'
33	LOAD_CONST        -2
36	SLICE+1           None
37	LOAD_GLOBAL       'CRLF'
40	COMPARE_OP        '=='
43	JUMP_IF_FALSE     '59'

46	LOAD_FAST         'line'
49	LOAD_CONST        -2
52	SLICE+2           None
53	STORE_FAST        'line'
56	JUMP_FORWARD      '88'

59	LOAD_FAST         'line'
62	LOAD_CONST        -1
65	SLICE+1           None
66	LOAD_GLOBAL       'CRLF'
69	COMPARE_OP        'in'
72	JUMP_IF_FALSE     '88'

75	LOAD_FAST         'line'
78	LOAD_CONST        -1
81	SLICE+2           None
82	STORE_FAST        'line'
85	JUMP_FORWARD      '88'
88_0	COME_FROM         '56'
88_1	COME_FROM         '85'

88	LOAD_FAST         'line'
91	LOAD_CONST        '.'
94	COMPARE_OP        '=='
97	JUMP_IF_FALSE     '104'

100	BREAK_LOOP        None
101	JUMP_FORWARD      '104'
104_0	COME_FROM         '101'

104	LOAD_FAST         'line'
107	LOAD_CONST        2
110	SLICE+2           None
111	LOAD_CONST        '..'
114	COMPARE_OP        '=='
117	JUMP_IF_FALSE     '133'

120	LOAD_FAST         'line'
123	LOAD_CONST        1
126	SLICE+1           None
127	STORE_FAST        'line'
130	JUMP_FORWARD      '133'
133_0	COME_FROM         '130'

133	LOAD_FAST         'func'
136	LOAD_FAST         'line'
139	CALL_FUNCTION_1   None
142	POP_TOP           None
143	JUMP_BACK         '3'
146	POP_BLOCK         None
147_0	COME_FROM         '0'

Syntax error at or near `POP_BLOCK' token at offset 146


def get_binary(f):
    data = f.read()
    return data


def get_alt_binary--- This code section failed: ---

0	SETUP_LOOP        '42'

3	LOAD_FAST         'f'
6	LOAD_ATTR         'read'
9	LOAD_FAST         'blocksize'
12	CALL_FUNCTION_1   None
15	STORE_FAST        'data'

18	LOAD_FAST         'data'
21	JUMP_IF_TRUE      '28'

24	BREAK_LOOP        None
25	JUMP_FORWARD      '28'
28_0	COME_FROM         '25'

28	LOAD_FAST         'func'
31	LOAD_FAST         'data'
34	CALL_FUNCTION_1   None
37	POP_TOP           None
38	JUMP_BACK         '3'
41	POP_BLOCK         None
42_0	COME_FROM         '0'

Syntax error at or near `POP_BLOCK' token at offset 41


def test():
    import sys
    import getopt
    opts, args = getopt.getopt(sys.argv[1:], '')
    selector = DEF_SELECTOR
    type = selector[0]
    host = DEF_HOST
    if args:
        host = args[0]
        args = args[1:]
    if args:
        type = args[0]
        args = args[1:]
        if len(type) > 1:
            type, selector = type[0], type
        else:
            selector = ''
            if args:
                selector = args[0]
                args = args[1:]
        query = ''
        if args:
            query = args[0]
            args = args[1:]
    if type == A_INDEX:
        f = send_query(selector, query, host)
    else:
        f = send_selector(selector, host)
    if type == A_TEXT:
        lines = get_textfile(f)
        for item in lines:
            print item

    elif type in (A_MENU, A_INDEX):
        entries = get_directory(f)
        for item in entries:
            print item

    else:
        data = get_binary(f)
        print 'binary data:', len(data), 'bytes:', repr(data[:100])[:40]


if __name__ == '__main__':
    test()# decompiled 0 files: 0 okay, 1 failed, 0 verify failed
# 2013.08.22 22:13:03 Pacific Daylight Time

# Can't uncompyle C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\gopherlib.pyc
Traceback (most recent call last):
  File "C:\python27\lib\uncompyle2\__init__.py", line 206, in main
    uncompyle_file(infile, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 143, in uncompyle_file
    uncompyle(version, co, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 132, in uncompyle
    raise walk.ERROR
ParserError: --- This code section failed: ---

0	SETUP_LOOP        '42'

3	LOAD_FAST         'f'
6	LOAD_ATTR         'read'
9	LOAD_FAST         'blocksize'
12	CALL_FUNCTION_1   None
15	STORE_FAST        'data'

18	LOAD_FAST         'data'
21	JUMP_IF_TRUE      '28'

24	BREAK_LOOP        None
25	JUMP_FORWARD      '28'
28_0	COME_FROM         '25'

28	LOAD_FAST         'func'
31	LOAD_FAST         'data'
34	CALL_FUNCTION_1   None
37	POP_TOP           None
38	JUMP_BACK         '3'
41	POP_BLOCK         None
42_0	COME_FROM         '0'

Syntax error at or near `POP_BLOCK' token at offset 41

