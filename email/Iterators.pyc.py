# 2013.08.22 22:15:00 Pacific Daylight Time
# Embedded file name: email.Iterators
import sys
from cStringIO import StringIO

def walk--- This code section failed: ---

0	LOAD_FAST         'self'
3	YIELD_VALUE       None

4	LOAD_FAST         'self'
7	LOAD_ATTR         'is_multipart'
10	CALL_FUNCTION_0   None
13	JUMP_IF_FALSE     '69'

16	SETUP_LOOP        '69'
19	LOAD_FAST         'self'
22	LOAD_ATTR         'get_payload'
25	CALL_FUNCTION_0   None
28	GET_ITER          None
29	FOR_ITER          '65'
32	STORE_FAST        'subpart'

35	SETUP_LOOP        '62'
38	LOAD_FAST         'subpart'
41	LOAD_ATTR         'walk'
44	CALL_FUNCTION_0   None
47	GET_ITER          None
48	FOR_ITER          '61'
51	STORE_FAST        'subsubpart'

54	LOAD_FAST         'subsubpart'
57	YIELD_VALUE       None
58	JUMP_BACK         '48'
61	POP_BLOCK         None
62_0	COME_FROM         '35'
62	JUMP_BACK         '29'
65	POP_BLOCK         None
66_0	COME_FROM         '16'
66	JUMP_FORWARD      '69'
69_0	COME_FROM         '66'

Syntax error at or near `SETUP_LOOP' token at offset 16


def body_line_iterator--- This code section failed: ---

0	SETUP_LOOP        '86'
3	LOAD_FAST         'msg'
6	LOAD_ATTR         'walk'
9	CALL_FUNCTION_0   None
12	GET_ITER          None
13	FOR_ITER          '85'
16	STORE_FAST        'subpart'

19	LOAD_FAST         'subpart'
22	LOAD_ATTR         'get_payload'
25	LOAD_CONST        'decode'
28	LOAD_FAST         'decode'
31	CALL_FUNCTION_256 None
34	STORE_FAST        'payload'

37	LOAD_GLOBAL       'isinstance'
40	LOAD_FAST         'payload'
43	LOAD_GLOBAL       'basestring'
46	CALL_FUNCTION_2   None
49	JUMP_IF_FALSE     '82'

52	SETUP_LOOP        '82'
55	LOAD_GLOBAL       'StringIO'
58	LOAD_FAST         'payload'
61	CALL_FUNCTION_1   None
64	GET_ITER          None
65	FOR_ITER          '78'
68	STORE_FAST        'line'

71	LOAD_FAST         'line'
74	YIELD_VALUE       None
75	JUMP_BACK         '65'
78	POP_BLOCK         None
79_0	COME_FROM         '52'
79	JUMP_BACK         '13'
82	JUMP_BACK         '13'
85	POP_BLOCK         None
86_0	COME_FROM         '0'

Syntax error at or near `POP_BLOCK' token at offset 78


def typed_subpart_iterator--- This code section failed: ---

0	SETUP_LOOP        '81'
3	LOAD_FAST         'msg'
6	LOAD_ATTR         'walk'
9	CALL_FUNCTION_0   None
12	GET_ITER          None
13	FOR_ITER          '80'
16	STORE_FAST        'subpart'

19	LOAD_FAST         'subpart'
22	LOAD_ATTR         'get_content_maintype'
25	CALL_FUNCTION_0   None
28	LOAD_FAST         'maintype'
31	COMPARE_OP        '=='
34	JUMP_IF_FALSE     '77'

37	LOAD_FAST         'subtype'
40	LOAD_CONST        None
43	COMPARE_OP        'is'
46	JUMP_IF_TRUE      '67'
49	LOAD_FAST         'subpart'
52	LOAD_ATTR         'get_content_subtype'
55	CALL_FUNCTION_0   None
58	LOAD_FAST         'subtype'
61	COMPARE_OP        '=='
64_0	COME_FROM         '46'
64	JUMP_IF_FALSE     '74'

67	LOAD_FAST         'subpart'
70	YIELD_VALUE       None
71	JUMP_ABSOLUTE     '77'
74	CONTINUE          '13'
77	JUMP_BACK         '13'
80	POP_BLOCK         None
81_0	COME_FROM         '0'
81	LOAD_CONST        None
84	RETURN_VALUE      None

Syntax error at or near `CONTINUE' token at offset 74


def _structure(msg, fp = None, level = 0, include_default = False):
    if fp is None:
        fp = sys.stdout
    tab = ' ' * (level * 4)
    print >> fp, tab + msg.get_content_type(),
    if include_default:
        print >> fp, '[%s]' % msg.get_default_type()
    else:
        print >> fp
    if msg.is_multipart():
        for subpart in msg.get_payload():
            _structure(subpart, fp, level + 1, include_default)

    return# decompiled 0 files: 0 okay, 1 failed, 0 verify failed
# 2013.08.22 22:15:00 Pacific Daylight Time

# Can't uncompyle C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\email\Iterators.pyc
Traceback (most recent call last):
  File "C:\python27\lib\uncompyle2\__init__.py", line 206, in main
    uncompyle_file(infile, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 143, in uncompyle_file
    uncompyle(version, co, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 132, in uncompyle
    raise walk.ERROR
ParserError: --- This code section failed: ---

0	SETUP_LOOP        '81'
3	LOAD_FAST         'msg'
6	LOAD_ATTR         'walk'
9	CALL_FUNCTION_0   None
12	GET_ITER          None
13	FOR_ITER          '80'
16	STORE_FAST        'subpart'

19	LOAD_FAST         'subpart'
22	LOAD_ATTR         'get_content_maintype'
25	CALL_FUNCTION_0   None
28	LOAD_FAST         'maintype'
31	COMPARE_OP        '=='
34	JUMP_IF_FALSE     '77'

37	LOAD_FAST         'subtype'
40	LOAD_CONST        None
43	COMPARE_OP        'is'
46	JUMP_IF_TRUE      '67'
49	LOAD_FAST         'subpart'
52	LOAD_ATTR         'get_content_subtype'
55	CALL_FUNCTION_0   None
58	LOAD_FAST         'subtype'
61	COMPARE_OP        '=='
64_0	COME_FROM         '46'
64	JUMP_IF_FALSE     '74'

67	LOAD_FAST         'subpart'
70	YIELD_VALUE       None
71	JUMP_ABSOLUTE     '77'
74	CONTINUE          '13'
77	JUMP_BACK         '13'
80	POP_BLOCK         None
81_0	COME_FROM         '0'
81	LOAD_CONST        None
84	RETURN_VALUE      None

Syntax error at or near `CONTINUE' token at offset 74

