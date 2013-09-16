# 2013.08.22 22:13:02 Pacific Daylight Time
# Embedded file name: getpass
import sys
__all__ = ['getpass', 'getuser']

def unix_getpass(prompt = 'Password: '):
    try:
        fd = sys.stdin.fileno()
    except:
        return default_getpass(prompt)

    old = termios.tcgetattr(fd)
    new = old[:]
    new[3] = new[3] & ~termios.ECHO
    try:
        termios.tcsetattr(fd, termios.TCSADRAIN, new)
        passwd = _raw_input(prompt)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)

    sys.stdout.write('\n')
    return passwd


def win_getpass--- This code section failed: ---

0	LOAD_GLOBAL       'sys'
3	LOAD_ATTR         'stdin'
6	LOAD_GLOBAL       'sys'
9	LOAD_ATTR         '__stdin__'
12	COMPARE_OP        'is not'
15	JUMP_IF_FALSE     '31'

18	LOAD_GLOBAL       'default_getpass'
21	LOAD_FAST         'prompt'
24	CALL_FUNCTION_1   None
27	RETURN_VALUE      None
28	JUMP_FORWARD      '31'
31_0	COME_FROM         '28'

31	LOAD_CONST        None
34	IMPORT_NAME       'msvcrt'
37	STORE_FAST        'msvcrt'

40	SETUP_LOOP        '70'
43	LOAD_FAST         'prompt'
46	GET_ITER          None
47	FOR_ITER          '69'
50	STORE_FAST        'c'

53	LOAD_FAST         'msvcrt'
56	LOAD_ATTR         'putch'
59	LOAD_FAST         'c'
62	CALL_FUNCTION_1   None
65	POP_TOP           None
66	JUMP_BACK         '47'
69	POP_BLOCK         None
70_0	COME_FROM         '40'

70	LOAD_CONST        ''
73	STORE_FAST        'pw'

76	SETUP_LOOP        '179'

79	LOAD_FAST         'msvcrt'
82	LOAD_ATTR         'getch'
85	CALL_FUNCTION_0   None
88	STORE_FAST        'c'

91	LOAD_FAST         'c'
94	LOAD_CONST        '\r'
97	COMPARE_OP        '=='
100	JUMP_IF_TRUE      '115'
103	LOAD_FAST         'c'
106	LOAD_CONST        '\n'
109	COMPARE_OP        '=='
112_0	COME_FROM         '100'
112	JUMP_IF_FALSE     '119'

115	BREAK_LOOP        None
116	JUMP_FORWARD      '119'
119_0	COME_FROM         '116'

119	LOAD_FAST         'c'
122	LOAD_CONST        '\x03'
125	COMPARE_OP        '=='
128	JUMP_IF_FALSE     '140'

131	LOAD_GLOBAL       'KeyboardInterrupt'
134	RAISE_VARARGS_1   None
137	JUMP_FORWARD      '140'
140_0	COME_FROM         '137'

140	LOAD_FAST         'c'
143	LOAD_CONST        '\x08'
146	COMPARE_OP        '=='
149	JUMP_IF_FALSE     '165'

152	LOAD_FAST         'pw'
155	LOAD_CONST        -1
158	SLICE+2           None
159	STORE_FAST        'pw'
162	JUMP_BACK         '79'

165	LOAD_FAST         'pw'
168	LOAD_FAST         'c'
171	BINARY_ADD        None
172	STORE_FAST        'pw'
175	JUMP_BACK         '79'
178	POP_BLOCK         None
179_0	COME_FROM         '76'

179	LOAD_FAST         'msvcrt'
182	LOAD_ATTR         'putch'
185	LOAD_CONST        '\r'
188	CALL_FUNCTION_1   None
191	POP_TOP           None

192	LOAD_FAST         'msvcrt'
195	LOAD_ATTR         'putch'
198	LOAD_CONST        '\n'
201	CALL_FUNCTION_1   None
204	POP_TOP           None

205	LOAD_FAST         'pw'
208	RETURN_VALUE      None
-1	RETURN_LAST       None

Syntax error at or near `POP_BLOCK' token at offset 178


def default_getpass(prompt = 'Password: '):
    print 'Warning: Problem with getpass. Passwords may be echoed.'
    return _raw_input(prompt)


def _raw_input(prompt = ''):
    prompt = str(prompt)
    if prompt:
        sys.stdout.write(prompt)
    line = sys.stdin.readline()
    if not line:
        raise EOFError
    if line[-1] == '\n':
        line = line[:-1]
    return line


def getuser():
    import os
    for name in ('LOGNAME', 'USER', 'LNAME', 'USERNAME'):
        user = os.environ.get(name)
        if user:
            return user

    import pwd
    return pwd.getpwuid(os.getuid())[0]


try:
    import termios
    (termios.tcgetattr, termios.tcsetattr)
except (ImportError, AttributeError):
    try:
        import msvcrt
    except ImportError:
        try:
            from EasyDialogs import AskPassword
        except ImportError:
            getpass = default_getpass
        else:
            getpass = AskPassword

    else:
        getpass = win_getpass

else:
    getpass = unix_getpass# decompiled 0 files: 0 okay, 1 failed, 0 verify failed
# 2013.08.22 22:13:02 Pacific Daylight Time

# Can't uncompyle C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\getpass.pyc
Traceback (most recent call last):
  File "C:\python27\lib\uncompyle2\__init__.py", line 206, in main
    uncompyle_file(infile, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 143, in uncompyle_file
    uncompyle(version, co, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 132, in uncompyle
    raise walk.ERROR
ParserError: --- This code section failed: ---

0	LOAD_GLOBAL       'sys'
3	LOAD_ATTR         'stdin'
6	LOAD_GLOBAL       'sys'
9	LOAD_ATTR         '__stdin__'
12	COMPARE_OP        'is not'
15	JUMP_IF_FALSE     '31'

18	LOAD_GLOBAL       'default_getpass'
21	LOAD_FAST         'prompt'
24	CALL_FUNCTION_1   None
27	RETURN_VALUE      None
28	JUMP_FORWARD      '31'
31_0	COME_FROM         '28'

31	LOAD_CONST        None
34	IMPORT_NAME       'msvcrt'
37	STORE_FAST        'msvcrt'

40	SETUP_LOOP        '70'
43	LOAD_FAST         'prompt'
46	GET_ITER          None
47	FOR_ITER          '69'
50	STORE_FAST        'c'

53	LOAD_FAST         'msvcrt'
56	LOAD_ATTR         'putch'
59	LOAD_FAST         'c'
62	CALL_FUNCTION_1   None
65	POP_TOP           None
66	JUMP_BACK         '47'
69	POP_BLOCK         None
70_0	COME_FROM         '40'

70	LOAD_CONST        ''
73	STORE_FAST        'pw'

76	SETUP_LOOP        '179'

79	LOAD_FAST         'msvcrt'
82	LOAD_ATTR         'getch'
85	CALL_FUNCTION_0   None
88	STORE_FAST        'c'

91	LOAD_FAST         'c'
94	LOAD_CONST        '\r'
97	COMPARE_OP        '=='
100	JUMP_IF_TRUE      '115'
103	LOAD_FAST         'c'
106	LOAD_CONST        '\n'
109	COMPARE_OP        '=='
112_0	COME_FROM         '100'
112	JUMP_IF_FALSE     '119'

115	BREAK_LOOP        None
116	JUMP_FORWARD      '119'
119_0	COME_FROM         '116'

119	LOAD_FAST         'c'
122	LOAD_CONST        '\x03'
125	COMPARE_OP        '=='
128	JUMP_IF_FALSE     '140'

131	LOAD_GLOBAL       'KeyboardInterrupt'
134	RAISE_VARARGS_1   None
137	JUMP_FORWARD      '140'
140_0	COME_FROM         '137'

140	LOAD_FAST         'c'
143	LOAD_CONST        '\x08'
146	COMPARE_OP        '=='
149	JUMP_IF_FALSE     '165'

152	LOAD_FAST         'pw'
155	LOAD_CONST        -1
158	SLICE+2           None
159	STORE_FAST        'pw'
162	JUMP_BACK         '79'

165	LOAD_FAST         'pw'
168	LOAD_FAST         'c'
171	BINARY_ADD        None
172	STORE_FAST        'pw'
175	JUMP_BACK         '79'
178	POP_BLOCK         None
179_0	COME_FROM         '76'

179	LOAD_FAST         'msvcrt'
182	LOAD_ATTR         'putch'
185	LOAD_CONST        '\r'
188	CALL_FUNCTION_1   None
191	POP_TOP           None

192	LOAD_FAST         'msvcrt'
195	LOAD_ATTR         'putch'
198	LOAD_CONST        '\n'
201	CALL_FUNCTION_1   None
204	POP_TOP           None

205	LOAD_FAST         'pw'
208	RETURN_VALUE      None
-1	RETURN_LAST       None

Syntax error at or near `POP_BLOCK' token at offset 178

