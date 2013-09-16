# 2013.08.22 22:13:01 Pacific Daylight Time
# Embedded file name: ftplib
import os
import sys
try:
    import SOCKS
    socket = SOCKS
    del SOCKS
    from socket import getfqdn
    socket.getfqdn = getfqdn
    del getfqdn
except ImportError:
    import socket

__all__ = ['FTP', 'Netrc']
MSG_OOB = 1
FTP_PORT = 21

class Error(Exception):
    __module__ = __name__


class error_reply(Error):
    __module__ = __name__


class error_temp(Error):
    __module__ = __name__


class error_perm(Error):
    __module__ = __name__


class error_proto(Error):
    __module__ = __name__


all_errors = (Error,
 socket.error,
 IOError,
 EOFError)
CRLF = '\r\n'

class FTP():
    __module__ = __name__
    debugging = 0
    host = ''
    port = FTP_PORT
    sock = None
    file = None
    welcome = None
    passiveserver = 1

    def __init__(self, host = '', user = '', passwd = '', acct = ''):
        if host:
            self.connect(host)
            if user:
                self.login(user, passwd, acct)

    def connect(self, host = '', port = 0):
        if host:
            self.host = host
        if port:
            self.port = port
        msg = 'getaddrinfo returns an empty list'
        for res in socket.getaddrinfo(self.host, self.port, 0, socket.SOCK_STREAM):
            af, socktype, proto, canonname, sa = res
            try:
                self.sock = socket.socket(af, socktype, proto)
                self.sock.connect(sa)
            except socket.error as msg:
                if self.sock:
                    self.sock.close()
                self.sock = None
                continue

            break

        if not self.sock:
            raise socket.error, msg
        self.af = af
        self.file = self.sock.makefile('rb')
        self.welcome = self.getresp()
        return self.welcome

    def getwelcome(self):
        if self.debugging:
            print '*welcome*', self.sanitize(self.welcome)
        return self.welcome

    def set_debuglevel(self, level):
        self.debugging = level

    debug = set_debuglevel

    def set_pasv(self, val):
        self.passiveserver = val

    def sanitize(self, s):
        if s[:5] == 'pass ' or s[:5] == 'PASS ':
            i = len(s)
            while i > 5 and s[i - 1] in '\r\n':
                i = i - 1

            s = s[:5] + '*' * (i - 5) + s[i:]
        return repr(s)

    def putline(self, line):
        line = line + CRLF
        if self.debugging > 1:
            print '*put*', self.sanitize(line)
        self.sock.sendall(line)

    def putcmd(self, line):
        if self.debugging:
            print '*cmd*', self.sanitize(line)
        self.putline(line)

    def getline(self):
        line = self.file.readline()
        if self.debugging > 1:
            print '*get*', self.sanitize(line)
        if not line:
            raise EOFError
        if line[-2:] == CRLF:
            line = line[:-2]
        elif line[-1:] in CRLF:
            line = line[:-1]
        return line

    def getmultiline--- This code section failed: ---

0	LOAD_FAST         'self'
3	LOAD_ATTR         'getline'
6	CALL_FUNCTION_0   None
9	STORE_FAST        'line'

12	LOAD_FAST         'line'
15	LOAD_CONST        3
18	LOAD_CONST        4
21	SLICE+3           None
22	LOAD_CONST        '-'
25	COMPARE_OP        '=='
28	JUMP_IF_FALSE     '116'

31	LOAD_FAST         'line'
34	LOAD_CONST        3
37	SLICE+2           None
38	STORE_FAST        'code'

41	SETUP_LOOP        '116'

44	LOAD_FAST         'self'
47	LOAD_ATTR         'getline'
50	CALL_FUNCTION_0   None
53	STORE_FAST        'nextline'

56	LOAD_FAST         'line'
59	LOAD_CONST        '\n'
62	LOAD_FAST         'nextline'
65	BINARY_ADD        None
66	BINARY_ADD        None
67	STORE_FAST        'line'

70	LOAD_FAST         'nextline'
73	LOAD_CONST        3
76	SLICE+2           None
77	LOAD_FAST         'code'
80	COMPARE_OP        '=='
83	JUMP_IF_FALSE     '109'
86	LOAD_FAST         'nextline'
89	LOAD_CONST        3
92	LOAD_CONST        4
95	SLICE+3           None
96	LOAD_CONST        '-'
99	COMPARE_OP        '!='
102_0	COME_FROM         '83'
102	JUMP_IF_FALSE     '109'

105	BREAK_LOOP        None
106	JUMP_BACK         '44'
109	JUMP_BACK         '44'
112	POP_BLOCK         None
113_0	COME_FROM         '41'
113	JUMP_FORWARD      '116'
116_0	COME_FROM         '113'

116	LOAD_FAST         'line'
119	RETURN_VALUE      None
-1	RETURN_LAST       None

Syntax error at or near `POP_BLOCK' token at offset 112

    def getresp(self):
        resp = self.getmultiline()
        if self.debugging:
            print '*resp*', self.sanitize(resp)
        self.lastresp = resp[:3]
        c = resp[:1]
        if c == '4':
            raise error_temp, resp
        if c == '5':
            raise error_perm, resp
        if c not in '123':
            raise error_proto, resp
        return resp

    def voidresp(self):
        resp = self.getresp()
        if resp[0] != '2':
            raise error_reply, resp
        return resp

    def abort(self):
        line = 'ABOR' + CRLF
        if self.debugging > 1:
            print '*put urgent*', self.sanitize(line)
        self.sock.sendall(line, MSG_OOB)
        resp = self.getmultiline()
        if resp[:3] not in ('426', '226'):
            raise error_proto, resp

    def sendcmd(self, cmd):
        self.putcmd(cmd)
        return self.getresp()

    def voidcmd(self, cmd):
        self.putcmd(cmd)
        return self.voidresp()

    def sendport(self, host, port):
        hbytes = host.split('.')
        pbytes = [repr(port / 256), repr(port % 256)]
        bytes = hbytes + pbytes
        cmd = 'PORT ' + ','.join(bytes)
        return self.voidcmd(cmd)

    def sendeprt(self, host, port):
        af = 0
        if self.af == socket.AF_INET:
            af = 1
        if self.af == socket.AF_INET6:
            af = 2
        if af == 0:
            raise error_proto, 'unsupported address family'
        fields = ['',
         repr(af),
         host,
         repr(port),
         '']
        cmd = 'EPRT ' + '|'.join(fields)
        return self.voidcmd(cmd)

    def makeport(self):
        msg = 'getaddrinfo returns an empty list'
        sock = None
        for res in socket.getaddrinfo(None, 0, self.af, socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
            af, socktype, proto, canonname, sa = res
            try:
                sock = socket.socket(af, socktype, proto)
                sock.bind(sa)
            except socket.error as msg:
                if sock:
                    sock.close()
                sock = None
                continue

            break

        if not sock:
            raise socket.error, msg
        sock.listen(1)
        port = sock.getsockname()[1]
        host = self.sock.getsockname()[0]
        if self.af == socket.AF_INET:
            resp = self.sendport(host, port)
        else:
            resp = self.sendeprt(host, port)
        return sock

    def makepasv(self):
        if self.af == socket.AF_INET:
            host, port = parse227(self.sendcmd('PASV'))
        else:
            host, port = parse229(self.sendcmd('EPSV'), self.sock.getpeername())
        return (host, port)

    def ntransfercmd(self, cmd, rest = None):
        size = None
        if self.passiveserver:
            host, port = self.makepasv()
            af, socktype, proto, canon, sa = socket.getaddrinfo(host, port, 0, socket.SOCK_STREAM)[0]
            conn = socket.socket(af, socktype, proto)
            conn.connect(sa)
            if rest is not None:
                self.sendcmd('REST %s' % rest)
            resp = self.sendcmd(cmd)
            if resp[0] != '1':
                raise error_reply, resp
        else:
            sock = self.makeport()
            if rest is not None:
                self.sendcmd('REST %s' % rest)
            resp = self.sendcmd(cmd)
            if resp[0] != '1':
                raise error_reply, resp
            conn, sockaddr = sock.accept()
        if resp[:3] == '150':
            size = parse150(resp)
        return (conn, size)

    def transfercmd(self, cmd, rest = None):
        return self.ntransfercmd(cmd, rest)[0]

    def login(self, user = '', passwd = '', acct = ''):
        if not user:
            user = 'anonymous'
        if not passwd:
            passwd = ''
        if not acct:
            acct = ''
        if user == 'anonymous' and passwd in ('', '-'):
            passwd = passwd + 'anonymous@'
        resp = self.sendcmd('USER ' + user)
        if resp[0] == '3':
            resp = self.sendcmd('PASS ' + passwd)
        if resp[0] == '3':
            resp = self.sendcmd('ACCT ' + acct)
        if resp[0] != '2':
            raise error_reply, resp
        return resp

    def retrbinary--- This code section failed: ---

0	LOAD_FAST         'self'
3	LOAD_ATTR         'voidcmd'
6	LOAD_CONST        'TYPE I'
9	CALL_FUNCTION_1   None
12	POP_TOP           None

13	LOAD_FAST         'self'
16	LOAD_ATTR         'transfercmd'
19	LOAD_FAST         'cmd'
22	LOAD_FAST         'rest'
25	CALL_FUNCTION_2   None
28	STORE_FAST        'conn'

31	SETUP_LOOP        '73'

34	LOAD_FAST         'conn'
37	LOAD_ATTR         'recv'
40	LOAD_FAST         'blocksize'
43	CALL_FUNCTION_1   None
46	STORE_FAST        'data'

49	LOAD_FAST         'data'
52	JUMP_IF_TRUE      '59'

55	BREAK_LOOP        None
56	JUMP_FORWARD      '59'
59_0	COME_FROM         '56'

59	LOAD_FAST         'callback'
62	LOAD_FAST         'data'
65	CALL_FUNCTION_1   None
68	POP_TOP           None
69	JUMP_BACK         '34'
72	POP_BLOCK         None
73_0	COME_FROM         '31'

73	LOAD_FAST         'conn'
76	LOAD_ATTR         'close'
79	CALL_FUNCTION_0   None
82	POP_TOP           None

83	LOAD_FAST         'self'
86	LOAD_ATTR         'voidresp'
89	CALL_FUNCTION_0   None
92	RETURN_VALUE      None
-1	RETURN_LAST       None

Syntax error at or near `POP_BLOCK' token at offset 72

    def retrlines--- This code section failed: ---

0	LOAD_FAST         'callback'
3	LOAD_CONST        None
6	COMPARE_OP        'is'
9	JUMP_IF_FALSE     '21'
12	LOAD_GLOBAL       'print_line'
15	STORE_FAST        'callback'
18	JUMP_FORWARD      '21'
21_0	COME_FROM         '18'

21	LOAD_FAST         'self'
24	LOAD_ATTR         'sendcmd'
27	LOAD_CONST        'TYPE A'
30	CALL_FUNCTION_1   None
33	STORE_FAST        'resp'

36	LOAD_FAST         'self'
39	LOAD_ATTR         'transfercmd'
42	LOAD_FAST         'cmd'
45	CALL_FUNCTION_1   None
48	STORE_FAST        'conn'

51	LOAD_FAST         'conn'
54	LOAD_ATTR         'makefile'
57	LOAD_CONST        'rb'
60	CALL_FUNCTION_1   None
63	STORE_FAST        'fp'

66	SETUP_LOOP        '196'

69	LOAD_FAST         'fp'
72	LOAD_ATTR         'readline'
75	CALL_FUNCTION_0   None
78	STORE_FAST        'line'

81	LOAD_FAST         'self'
84	LOAD_ATTR         'debugging'
87	LOAD_CONST        2
90	COMPARE_OP        '>'
93	JUMP_IF_FALSE     '114'
96	LOAD_CONST        '*retr*'
99	PRINT_ITEM        None
100	LOAD_GLOBAL       'repr'
103	LOAD_FAST         'line'
106	CALL_FUNCTION_1   None
109	PRINT_ITEM_CONT   None
110	PRINT_NEWLINE_CONT None
111	JUMP_FORWARD      '114'
114_0	COME_FROM         '111'

114	LOAD_FAST         'line'
117	JUMP_IF_TRUE      '124'

120	BREAK_LOOP        None
121	JUMP_FORWARD      '124'
124_0	COME_FROM         '121'

124	LOAD_FAST         'line'
127	LOAD_CONST        -2
130	SLICE+1           None
131	LOAD_GLOBAL       'CRLF'
134	COMPARE_OP        '=='
137	JUMP_IF_FALSE     '153'

140	LOAD_FAST         'line'
143	LOAD_CONST        -2
146	SLICE+2           None
147	STORE_FAST        'line'
150	JUMP_FORWARD      '182'

153	LOAD_FAST         'line'
156	LOAD_CONST        -1
159	SLICE+1           None
160	LOAD_CONST        '\n'
163	COMPARE_OP        '=='
166	JUMP_IF_FALSE     '182'

169	LOAD_FAST         'line'
172	LOAD_CONST        -1
175	SLICE+2           None
176	STORE_FAST        'line'
179	JUMP_FORWARD      '182'
182_0	COME_FROM         '150'
182_1	COME_FROM         '179'

182	LOAD_FAST         'callback'
185	LOAD_FAST         'line'
188	CALL_FUNCTION_1   None
191	POP_TOP           None
192	JUMP_BACK         '69'
195	POP_BLOCK         None
196_0	COME_FROM         '66'

196	LOAD_FAST         'fp'
199	LOAD_ATTR         'close'
202	CALL_FUNCTION_0   None
205	POP_TOP           None

206	LOAD_FAST         'conn'
209	LOAD_ATTR         'close'
212	CALL_FUNCTION_0   None
215	POP_TOP           None

216	LOAD_FAST         'self'
219	LOAD_ATTR         'voidresp'
222	CALL_FUNCTION_0   None
225	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 195

    def storbinary--- This code section failed: ---

0	LOAD_FAST         'self'
3	LOAD_ATTR         'voidcmd'
6	LOAD_CONST        'TYPE I'
9	CALL_FUNCTION_1   None
12	POP_TOP           None

13	LOAD_FAST         'self'
16	LOAD_ATTR         'transfercmd'
19	LOAD_FAST         'cmd'
22	CALL_FUNCTION_1   None
25	STORE_FAST        'conn'

28	SETUP_LOOP        '73'

31	LOAD_FAST         'fp'
34	LOAD_ATTR         'read'
37	LOAD_FAST         'blocksize'
40	CALL_FUNCTION_1   None
43	STORE_FAST        'buf'

46	LOAD_FAST         'buf'
49	JUMP_IF_TRUE      '56'
52	BREAK_LOOP        None
53	JUMP_FORWARD      '56'
56_0	COME_FROM         '53'

56	LOAD_FAST         'conn'
59	LOAD_ATTR         'sendall'
62	LOAD_FAST         'buf'
65	CALL_FUNCTION_1   None
68	POP_TOP           None
69	JUMP_BACK         '31'
72	POP_BLOCK         None
73_0	COME_FROM         '28'

73	LOAD_FAST         'conn'
76	LOAD_ATTR         'close'
79	CALL_FUNCTION_0   None
82	POP_TOP           None

83	LOAD_FAST         'self'
86	LOAD_ATTR         'voidresp'
89	CALL_FUNCTION_0   None
92	RETURN_VALUE      None
-1	RETURN_LAST       None

Syntax error at or near `POP_BLOCK' token at offset 72

    def storlines--- This code section failed: ---

0	LOAD_FAST         'self'
3	LOAD_ATTR         'voidcmd'
6	LOAD_CONST        'TYPE A'
9	CALL_FUNCTION_1   None
12	POP_TOP           None

13	LOAD_FAST         'self'
16	LOAD_ATTR         'transfercmd'
19	LOAD_FAST         'cmd'
22	CALL_FUNCTION_1   None
25	STORE_FAST        'conn'

28	SETUP_LOOP        '128'

31	LOAD_FAST         'fp'
34	LOAD_ATTR         'readline'
37	CALL_FUNCTION_0   None
40	STORE_FAST        'buf'

43	LOAD_FAST         'buf'
46	JUMP_IF_TRUE      '53'
49	BREAK_LOOP        None
50	JUMP_FORWARD      '53'
53_0	COME_FROM         '50'

53	LOAD_FAST         'buf'
56	LOAD_CONST        -2
59	SLICE+1           None
60	LOAD_GLOBAL       'CRLF'
63	COMPARE_OP        '!='
66	JUMP_IF_FALSE     '111'

69	LOAD_FAST         'buf'
72	LOAD_CONST        -1
75	BINARY_SUBSCR     None
76	LOAD_GLOBAL       'CRLF'
79	COMPARE_OP        'in'
82	JUMP_IF_FALSE     '98'
85	LOAD_FAST         'buf'
88	LOAD_CONST        -1
91	SLICE+2           None
92	STORE_FAST        'buf'
95	JUMP_FORWARD      '98'
98_0	COME_FROM         '95'

98	LOAD_FAST         'buf'
101	LOAD_GLOBAL       'CRLF'
104	BINARY_ADD        None
105	STORE_FAST        'buf'
108	JUMP_FORWARD      '111'
111_0	COME_FROM         '108'

111	LOAD_FAST         'conn'
114	LOAD_ATTR         'sendall'
117	LOAD_FAST         'buf'
120	CALL_FUNCTION_1   None
123	POP_TOP           None
124	JUMP_BACK         '31'
127	POP_BLOCK         None
128_0	COME_FROM         '28'

128	LOAD_FAST         'conn'
131	LOAD_ATTR         'close'
134	CALL_FUNCTION_0   None
137	POP_TOP           None

138	LOAD_FAST         'self'
141	LOAD_ATTR         'voidresp'
144	CALL_FUNCTION_0   None
147	RETURN_VALUE      None
-1	RETURN_LAST       None

Syntax error at or near `POP_BLOCK' token at offset 127

    def acct(self, password):
        cmd = 'ACCT ' + password
        return self.voidcmd(cmd)

    def nlst(self, *args):
        cmd = 'NLST'
        for arg in args:
            cmd = cmd + (' ' + arg)

        files = []
        self.retrlines(cmd, files.append)
        return files

    def dir(self, *args):
        cmd = 'LIST'
        func = None
        if args[-1:] and type(args[-1]) != type(''):
            args, func = args[:-1], args[-1]
        for arg in args:
            if arg:
                cmd = cmd + (' ' + arg)

        self.retrlines(cmd, func)
        return

    def rename(self, fromname, toname):
        resp = self.sendcmd('RNFR ' + fromname)
        if resp[0] != '3':
            raise error_reply, resp
        return self.voidcmd('RNTO ' + toname)

    def delete(self, filename):
        resp = self.sendcmd('DELE ' + filename)
        if resp[:3] in ('250', '200'):
            return resp
        elif resp[:1] == '5':
            raise error_perm, resp
        else:
            raise error_reply, resp

    def cwd(self, dirname):
        if dirname == '..':
            try:
                return self.voidcmd('CDUP')
            except error_perm as msg:
                if msg.args[0][:3] != '500':
                    raise

        elif dirname == '':
            dirname = '.'
        cmd = 'CWD ' + dirname
        return self.voidcmd(cmd)

    def size(self, filename):
        resp = self.sendcmd('SIZE ' + filename)
        if resp[:3] == '213':
            s = resp[3:].strip()
            try:
                return int(s)
            except (OverflowError, ValueError):
                return long(s)

    def mkd(self, dirname):
        resp = self.sendcmd('MKD ' + dirname)
        return parse257(resp)

    def rmd(self, dirname):
        return self.voidcmd('RMD ' + dirname)

    def pwd(self):
        resp = self.sendcmd('PWD')
        return parse257(resp)

    def quit(self):
        resp = self.voidcmd('QUIT')
        self.close()
        return resp

    def close(self):
        if self.file:
            self.file.close()
            self.sock.close()
            self.file = self.sock = None
        return


_150_re = None

def parse150(resp):
    global _150_re
    if resp[:3] != '150':
        raise error_reply, resp
    if _150_re is None:
        import re
        _150_re = re.compile('150 .* \\((\\d+) bytes\\)', re.IGNORECASE)
    m = _150_re.match(resp)
    if not m:
        return
    s = m.group(1)
    try:
        return int(s)
    except (OverflowError, ValueError):
        return long(s)

    return


_227_re = None

def parse227(resp):
    global _227_re
    if resp[:3] != '227':
        raise error_reply, resp
    if _227_re is None:
        import re
        _227_re = re.compile('(\\d+),(\\d+),(\\d+),(\\d+),(\\d+),(\\d+)')
    m = _227_re.search(resp)
    if not m:
        raise error_proto, resp
    numbers = m.groups()
    host = '.'.join(numbers[:4])
    port = (int(numbers[4]) << 8) + int(numbers[5])
    return (host, port)


def parse229(resp, peer):
    if resp[:3] != '229':
        raise error_reply, resp
    left = resp.find('(')
    if left < 0:
        raise error_proto, resp
    right = resp.find(')', left + 1)
    if right < 0:
        raise error_proto, resp
    if resp[left + 1] != resp[right - 1]:
        raise error_proto, resp
    parts = resp[left + 1:right].split(resp[left + 1])
    if len(parts) != 5:
        raise error_proto, resp
    host = peer[0]
    port = int(parts[3])
    return (host, port)


def parse257(resp):
    if resp[:3] != '257':
        raise error_reply, resp
    if resp[3:5] != ' "':
        return ''
    dirname = ''
    i = 5
    n = len(resp)
    while i < n:
        c = resp[i]
        i = i + 1
        if c == '"':
            if i >= n or resp[i] != '"':
                break
            i = i + 1
        dirname = dirname + c

    return dirname


def print_line(line):
    print line


def ftpcp(source, sourcename, target, targetname = '', type = 'I'):
    if not targetname:
        targetname = sourcename
    type = 'TYPE ' + type
    source.voidcmd(type)
    target.voidcmd(type)
    sourcehost, sourceport = parse227(source.sendcmd('PASV'))
    target.sendport(sourcehost, sourceport)
    treply = target.sendcmd('STOR ' + targetname)
    if treply[:3] not in ('125', '150'):
        raise error_proto
    sreply = source.sendcmd('RETR ' + sourcename)
    if sreply[:3] not in ('125', '150'):
        raise error_proto
    source.voidresp()
    target.voidresp()


class Netrc():
    __module__ = __name__
    __defuser = None
    __defpasswd = None
    __defacct = None

    def __init__--- This code section failed: ---

0	LOAD_FAST         'filename'
3	LOAD_CONST        None
6	COMPARE_OP        'is'
9	JUMP_IF_FALSE     '70'

12	LOAD_CONST        'HOME'
15	LOAD_GLOBAL       'os'
18	LOAD_ATTR         'environ'
21	COMPARE_OP        'in'
24	JUMP_IF_FALSE     '58'

27	LOAD_GLOBAL       'os'
30	LOAD_ATTR         'path'
33	LOAD_ATTR         'join'
36	LOAD_GLOBAL       'os'
39	LOAD_ATTR         'environ'
42	LOAD_CONST        'HOME'
45	BINARY_SUBSCR     None

46	LOAD_CONST        '.netrc'
49	CALL_FUNCTION_2   None
52	STORE_FAST        'filename'
55	JUMP_ABSOLUTE     '70'

58	LOAD_GLOBAL       'IOError'
61	LOAD_CONST        'specify file to load or set $HOME'
64	RAISE_VARARGS_2   None
67	JUMP_FORWARD      '70'
70_0	COME_FROM         '67'

70	BUILD_MAP         None
73	LOAD_FAST         'self'
76	STORE_ATTR        '__hosts'

79	BUILD_MAP         None
82	LOAD_FAST         'self'
85	STORE_ATTR        '__macros'

88	LOAD_GLOBAL       'open'
91	LOAD_FAST         'filename'
94	LOAD_CONST        'r'
97	CALL_FUNCTION_2   None
100	STORE_FAST        'fp'

103	LOAD_CONST        0
106	STORE_FAST        'in_macro'

109	SETUP_LOOP        '726'

112	LOAD_FAST         'fp'
115	LOAD_ATTR         'readline'
118	CALL_FUNCTION_0   None
121	STORE_FAST        'line'

124	LOAD_FAST         'line'
127	JUMP_IF_TRUE      '134'
130	BREAK_LOOP        None
131	JUMP_FORWARD      '134'
134_0	COME_FROM         '131'

134	LOAD_FAST         'in_macro'
137	JUMP_IF_FALSE     '171'
140	LOAD_FAST         'line'
143	LOAD_ATTR         'strip'
146	CALL_FUNCTION_0   None
149_0	COME_FROM         '137'
149	JUMP_IF_FALSE     '171'

152	LOAD_FAST         'macro_lines'
155	LOAD_ATTR         'append'
158	LOAD_FAST         'line'
161	CALL_FUNCTION_1   None
164	POP_TOP           None

165	CONTINUE          '112'
168	JUMP_FORWARD      '205'

171	LOAD_FAST         'in_macro'
174	JUMP_IF_FALSE     '205'

177	LOAD_GLOBAL       'tuple'
180	LOAD_FAST         'macro_lines'
183	CALL_FUNCTION_1   None
186	LOAD_FAST         'self'
189	LOAD_ATTR         '__macros'
192	LOAD_FAST         'macro_name'
195	STORE_SUBSCR      None

196	LOAD_CONST        0
199	STORE_FAST        'in_macro'
202	JUMP_FORWARD      '205'
205_0	COME_FROM         '168'
205_1	COME_FROM         '202'

205	LOAD_FAST         'line'
208	LOAD_ATTR         'split'
211	CALL_FUNCTION_0   None
214	STORE_FAST        'words'

217	LOAD_CONST        None
220	DUP_TOP           None
221	STORE_FAST        'host'
224	DUP_TOP           None
225	STORE_FAST        'user'
228	DUP_TOP           None
229	STORE_FAST        'passwd'
232	STORE_FAST        'acct'

235	LOAD_CONST        0
238	STORE_FAST        'default'

241	LOAD_CONST        0
244	STORE_FAST        'i'

247	SETUP_LOOP        '552'
250	LOAD_FAST         'i'
253	LOAD_GLOBAL       'len'
256	LOAD_FAST         'words'
259	CALL_FUNCTION_1   None
262	COMPARE_OP        '<'
265	JUMP_IF_FALSE     '551'

268	LOAD_FAST         'words'
271	LOAD_FAST         'i'
274	BINARY_SUBSCR     None
275	STORE_FAST        'w1'

278	LOAD_FAST         'i'
281	LOAD_CONST        1
284	BINARY_ADD        None
285	LOAD_GLOBAL       'len'
288	LOAD_FAST         'words'
291	CALL_FUNCTION_1   None
294	COMPARE_OP        '<'
297	JUMP_IF_FALSE     '317'

300	LOAD_FAST         'words'
303	LOAD_FAST         'i'
306	LOAD_CONST        1
309	BINARY_ADD        None
310	BINARY_SUBSCR     None
311	STORE_FAST        'w2'
314	JUMP_FORWARD      '323'

317	LOAD_CONST        None
320	STORE_FAST        'w2'
323_0	COME_FROM         '314'

323	LOAD_FAST         'w1'
326	LOAD_CONST        'default'
329	COMPARE_OP        '=='
332	JUMP_IF_FALSE     '344'

335	LOAD_CONST        1
338	STORE_FAST        'default'
341	JUMP_FORWARD      '538'

344	LOAD_FAST         'w1'
347	LOAD_CONST        'machine'
350	COMPARE_OP        '=='
353	JUMP_IF_FALSE     '387'
356	LOAD_FAST         'w2'
359_0	COME_FROM         '353'
359	JUMP_IF_FALSE     '387'

362	LOAD_FAST         'w2'
365	LOAD_ATTR         'lower'
368	CALL_FUNCTION_0   None
371	STORE_FAST        'host'

374	LOAD_FAST         'i'
377	LOAD_CONST        1
380	BINARY_ADD        None
381	STORE_FAST        'i'
384	JUMP_FORWARD      '538'

387	LOAD_FAST         'w1'
390	LOAD_CONST        'login'
393	COMPARE_OP        '=='
396	JUMP_IF_FALSE     '424'
399	LOAD_FAST         'w2'
402_0	COME_FROM         '396'
402	JUMP_IF_FALSE     '424'

405	LOAD_FAST         'w2'
408	STORE_FAST        'user'

411	LOAD_FAST         'i'
414	LOAD_CONST        1
417	BINARY_ADD        None
418	STORE_FAST        'i'
421	JUMP_FORWARD      '538'

424	LOAD_FAST         'w1'
427	LOAD_CONST        'password'
430	COMPARE_OP        '=='
433	JUMP_IF_FALSE     '461'
436	LOAD_FAST         'w2'
439_0	COME_FROM         '433'
439	JUMP_IF_FALSE     '461'

442	LOAD_FAST         'w2'
445	STORE_FAST        'passwd'

448	LOAD_FAST         'i'
451	LOAD_CONST        1
454	BINARY_ADD        None
455	STORE_FAST        'i'
458	JUMP_FORWARD      '538'

461	LOAD_FAST         'w1'
464	LOAD_CONST        'account'
467	COMPARE_OP        '=='
470	JUMP_IF_FALSE     '498'
473	LOAD_FAST         'w2'
476_0	COME_FROM         '470'
476	JUMP_IF_FALSE     '498'

479	LOAD_FAST         'w2'
482	STORE_FAST        'acct'

485	LOAD_FAST         'i'
488	LOAD_CONST        1
491	BINARY_ADD        None
492	STORE_FAST        'i'
495	JUMP_FORWARD      '538'

498	LOAD_FAST         'w1'
501	LOAD_CONST        'macdef'
504	COMPARE_OP        '=='
507	JUMP_IF_FALSE     '538'
510	LOAD_FAST         'w2'
513_0	COME_FROM         '507'
513	JUMP_IF_FALSE     '538'

516	LOAD_FAST         'w2'
519	STORE_FAST        'macro_name'

522	BUILD_LIST_0      None
525	STORE_FAST        'macro_lines'

528	LOAD_CONST        1
531	STORE_FAST        'in_macro'

534	BREAK_LOOP        None
535	JUMP_FORWARD      '538'
538_0	COME_FROM         '341'
538_1	COME_FROM         '384'
538_2	COME_FROM         '421'
538_3	COME_FROM         '458'
538_4	COME_FROM         '495'
538_5	COME_FROM         '535'

538	LOAD_FAST         'i'
541	LOAD_CONST        1
544	BINARY_ADD        None
545	STORE_FAST        'i'
548	JUMP_BACK         '250'
551	POP_BLOCK         None
552_0	COME_FROM         '247'

552	LOAD_FAST         'default'
555	JUMP_IF_FALSE     '615'

558	LOAD_FAST         'user'
561	JUMP_IF_TRUE      '570'
564	LOAD_FAST         'self'
567	LOAD_ATTR         '__defuser'
570	LOAD_FAST         'self'
573	STORE_ATTR        '__defuser'

576	LOAD_FAST         'passwd'
579	JUMP_IF_TRUE      '588'
582	LOAD_FAST         'self'
585	LOAD_ATTR         '__defpasswd'
588	LOAD_FAST         'self'
591	STORE_ATTR        '__defpasswd'

594	LOAD_FAST         'acct'
597	JUMP_IF_TRUE      '606'
600	LOAD_FAST         'self'
603	LOAD_ATTR         '__defacct'
606	LOAD_FAST         'self'
609	STORE_ATTR        '__defacct'
612	JUMP_FORWARD      '615'
615_0	COME_FROM         '612'

615	LOAD_FAST         'host'
618	JUMP_IF_FALSE     '722'

621	LOAD_FAST         'host'
624	LOAD_FAST         'self'
627	LOAD_ATTR         '__hosts'
630	COMPARE_OP        'in'
633	JUMP_IF_FALSE     '697'

636	LOAD_FAST         'self'
639	LOAD_ATTR         '__hosts'
642	LOAD_FAST         'host'
645	BINARY_SUBSCR     None
646	UNPACK_SEQUENCE_3 None
649	STORE_FAST        'ouser'
652	STORE_FAST        'opasswd'
655	STORE_FAST        'oacct'

658	LOAD_FAST         'user'
661	JUMP_IF_TRUE      '667'
664	LOAD_FAST         'ouser'
667	STORE_FAST        'user'

670	LOAD_FAST         'passwd'
673	JUMP_IF_TRUE      '679'
676	LOAD_FAST         'opasswd'
679	STORE_FAST        'passwd'

682	LOAD_FAST         'acct'
685	JUMP_IF_TRUE      '691'
688	LOAD_FAST         'oacct'
691	STORE_FAST        'acct'
694	JUMP_FORWARD      '697'
697_0	COME_FROM         '694'

697	LOAD_FAST         'user'
700	LOAD_FAST         'passwd'
703	LOAD_FAST         'acct'
706	BUILD_TUPLE_3     None
709	LOAD_FAST         'self'
712	LOAD_ATTR         '__hosts'
715	LOAD_FAST         'host'
718	STORE_SUBSCR      None
719	JUMP_BACK         '112'
722	JUMP_BACK         '112'
725	POP_BLOCK         None
726_0	COME_FROM         '109'

726	LOAD_FAST         'fp'
729	LOAD_ATTR         'close'
732	CALL_FUNCTION_0   None
735	POP_TOP           None
736	LOAD_CONST        None
739	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 725

    def get_hosts(self):
        return self.__hosts.keys()

    def get_account(self, host):
        host = host.lower()
        user = passwd = acct = None
        if host in self.__hosts:
            user, passwd, acct = self.__hosts[host]
        user = user o
# Can't uncompyle C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\ftplib.pyc
Traceback (most recent call last):
  File "C:\python27\lib\uncompyle2\__init__.py", line 206, in main
    uncompyle_file(infile, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 143, in uncompyle_file
    uncompyle(version, co, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 132, in uncompyle
    raise walk.ERROR
ParserError: --- This code section failed: ---

0	LOAD_FAST         'filename'
3	LOAD_CONST        None
6	COMPARE_OP        'is'
9	JUMP_IF_FALSE     '70'

12	LOAD_CONST        'HOME'
15	LOAD_GLOBAL       'os'
18	LOAD_ATTR         'environ'
21	COMPARE_OP        'in'
24	JUMP_IF_FALSE     '58'

27	LOAD_GLOBAL       'os'
30	LOAD_ATTR         'path'
33	LOAD_ATTR         'join'
36	LOAD_GLOBAL       'os'
39	LOAD_ATTR         'environ'
42	LOAD_CONST        'HOME'
45	BINARY_SUBSCR     None

46	LOAD_CONST        '.netrc'
49	CALL_FUNCTION_2   None
52	STORE_FAST        'filename'
55	JUMP_ABSOLUTE     '70'

58	LOAD_GLOBAL       'IOError'
61	LOAD_CONST        'specify file to load or set $HOME'
64	RAISE_VARARGS_2   None
67	JUMP_FORWARD      '70'
70_0	COME_FROM         '67'

70	BUILD_MAP         None
73	LOAD_FAST         'self'
76	STORE_ATTR        '__hosts'

79	BUILD_MAP         None
82	LOAD_FAST         'self'
85	STORE_ATTR        '__macros'

88	LOAD_GLOBAL       'open'
91	LOAD_FAST         'filename'
94	LOAD_CONST        'r'
97	CALL_FUNCTION_2   None
100	STORE_FAST        'fp'

103	LOAD_CONST        0
106	STORE_FAST        'in_macro'

109	SETUP_LOOP        '726'

112	LOAD_FAST         'fp'
115	LOAD_ATTR         'readline'
118	CALL_FUNCTION_0   None
121	STORE_FAST        'line'

124	LOAD_FAST         'line'
127	JUMP_IF_TRUE      '134'
130	BREAK_LOOP        None
131	JUMP_FORWARD      '134'
134_0	COME_FROM         '131'

134	LOAD_FAST         'in_macro'
137	JUMP_IF_FALSE     '171'
140	LOAD_FAST         'line'
143	LOAD_ATTR         'strip'
146	CALL_FUNCTION_0   None
149_0	COME_FROM         '137'
149	JUMP_IF_FALSE     '171'

152	LOAD_FAST         'macro_lines'
155	LOAD_ATTR         'append'
158	LOAD_FAST         'line'
161	CALL_FUNCTION_1   None
164	POP_TOP           None

165	CONTINUE          '112'
168	JUMP_FORWARD      '205'

171	LOAD_FAST         'in_macro'
174	JUMP_IF_FALSE     '205'

177	LOAD_GLOBAL       'tuple'
180	LOAD_FAST         'macro_lines'
183	CALL_FUNCTION_1   None
186	LOAD_FAST         'self'
189	LOAD_ATTR         '__macros'
192	LOAD_FAST         'macro_name'
195	STORE_SUBSCR      None

196	LOAD_CONST        0
199	STORE_FAST        'in_macro'
202	JUMP_FORWARD      '205'
205_0	COME_FROM         '168'
205_1	COME_FROM         '202'

205	LOAD_FAST         'line'
208	LOAD_ATTR         'split'
211	CALL_FUNCTION_0   None
214	STORE_FAST        'words'

217	LOAD_CONST        None
220	DUP_TOP           None
221	STORE_FAST        'host'
224	DUP_TOP           None
225	STORE_FAST        'user'
228	DUP_TOP           None
229	STORE_FAST        'passwd'
232	STORE_FAST        'acct'

235	LOAD_CONST        0
238	STORE_FAST        'default'

241	LOAD_CONST        0
244	STORE_FAST        'i'

247	SETUP_LOOP        '552'
250	LOAD_FAST         'i'
253	LOAD_GLOBAL       'len'
256	LOAD_FAST         'words'
259	CALL_FUNCTION_1   None
262	COMPARE_OP        '<'
265	JUMP_IF_FALSE     '551'

268	LOAD_FAST         'words'
271	LOAD_FAST         'i'
274	BINARY_SUBSCR     None
275	STORE_FAST        'w1'

278	LOAD_FAST         'i'
281	LOAD_CONST        1
284	BINARY_ADD        None
285	LOAD_GLOBAL       'len'
288	LOAD_FAST         'words'
291	CALL_FUNCTION_1   None
294	COMPARE_OP        '<'
297	JUMP_IF_FALSE     '317'

300	LOAD_FAST         'words'
303	LOAD_FAST         'i'
306	LOAD_CONST        1
309	BINARY_ADD        None
310	BINARY_SUBSCR     None
311	STORE_FAST        'w2'
314	JUMP_FORWARD      '323'

317	LOAD_CONST        None
320	STORE_FAST        'w2'
323_0	COME_FROM         '314'

323	LOAD_FAST         'w1'
326	LOAD_CONST        'default'
329	COMPARE_OP        '=='
332	JUMP_IF_FALSE     '344'

335	LOAD_CONST        1
338	STORE_FAST        'default'
341	JUMP_FORWARD      '538'

344	LOAD_FAST         'w1'
347	LOAD_CONST        'machine'
350	COMPARE_OP        '=='
353	JUMP_IF_FALSE     '387'
356	LOAD_FAST         'w2'
359_0	COME_FROM         '353'
359	JUMP_IF_FALSE     '387'

362	LOAD_FAST         'w2'
365	LOAD_ATTR         'lower'
368	CALL_FUNCTION_0   None
371	STORE_FAST        'host'

374	LOAD_FAST         'i'
377	LOAD_CONST        1
380	BINARY_ADD        None
381	STORE_FAST        'i'
384	JUMP_FORWARD      '538'

387	LOAD_FAST         'w1'
390	LOAD_CONST        'login'
393	COMPARE_OP        '=='
396	JUMP_IF_FALSE     '424'
399	LOAD_FAST         'w2'
402_0	COME_FROM         '396'
402	JUMP_IF_FALSE     '424'

405	LOAD_FAST         'w2'
408	STORE_FAST        'user'

411	LOAD_FAST         'i'
414	LOAD_CONST        1
417	BINARY_ADD        None
418	STORE_FAST        'i'
421	JUMP_FORWARD      '538'

424	LOAD_FAST         'w1'
427	LOAD_CONST        'password'
430	COMPARE_OP        '=='
433	JUMP_IF_FALSE     '461'
436	LOAD_FAST         'w2'
439_0	COME_FROM         '433'
439	JUMP_IF_FALSE     '461'

442	LOAD_FAST         'w2'
445	STORE_FAST        'passwd'

448	LOAD_FAST         'i'
451	LOAD_CONST        1
454	BINARY_ADD        None
455	STORE_FAST        'i'
458	JUMP_FORWARD      '538'

461	LOAD_FAST         'w1'
464	LOAD_CONST        'account'
467	COMPARE_OP        '=='
470	JUMP_IF_FALSE     '498'
473	LOAD_FAST         'w2'
476_0	COME_FROM         '470'
476	JUMP_IF_FALSE     '498'

479	LOAD_FAST         'w2'
482	STORE_FAST        'acct'

485	LOAD_FAST         'i'
488	LOAD_CONST        1
491	BINARY_ADD        None
492	STORE_FAST        'i'
495	JUMP_FORWARD      '538'

498	LOAD_FAST         'w1'
501	LOAD_CONST        'macdef'
504	COMPARE_OP        '=='
507	JUMP_IF_FALSE     '538'
510	LOAD_FAST         'w2'
513_0	COME_FROM         '507'
513	JUMP_IF_FALSE     '538'

516	LOAD_FAST         'w2'
519	STORE_FAST        'macro_name'

522	BUILD_LIST_0      None
525	STORE_FAST        'macro_lines'

528	LOAD_CONST        1
531	STORE_FAST        'in_macro'

534	BREAK_LOOP        None
535	JUMP_FORWARD      '538'
538_0	COME_FROM         '341'
538_1	COME_FROM         '384'
538_2	COME_FROM         '421'
538_3	COME_FROM         '458'
538_4	COME_FROM         '495'
538_5	COME_FROM         '535'

538	LOAD_FAST         'i'
541	LOAD_CONST        1
544	BINARY_ADD        None
545	STORE_FAST        'i'
548	JUMP_BACK         '250'
551	POP_BLOCK         None
552_0	COME_FROM         '247'

552	LOAD_FAST         'default'
555	JUMP_IF_FALSE     '615'

558	LOAD_FAST         'user'
561	JUMP_IF_TRUE      '570'
564	LOAD_FAST         'self'
567	LOAD_ATTR         '__defuser'
570	LOAD_FAST         'self'
573	STORE_ATTR        '__defuser'

576	LOAD_FAST         'passwd'
579	JUMP_IF_TRUE      '588'
582	LOAD_FAST         'self'
585	LOAD_ATTR         '__defpasswd'
588	LOAD_FAST         'self'
591	STORE_ATTR        '__defpasswd'

594	LOAD_FAST         'acct'
597	JUMP_IF_TRUE      '606'
600	LOAD_FAST         'self'
603	LOAD_ATTR         '__defacct'
606	LOAD_FAST         'self'
609	STORE_ATTR        '__defacct'
612	JUMP_FORWARD      '615'
615_0	COME_FROM         '612'

615	LOAD_FAST         'host'
618	JUMP_IF_FALSE     '722'

621	LOAD_FAST         'host'
624	LOAD_FAST         'self'
627	LOAD_ATTR         '__hosts'
630	COMPARE_OP        'in'
633	JUMP_IF_FALSE     '697'

636	LOAD_FAST         'self'
639	LOAD_ATTR         '__hosts'
642	LOAD_FAST         'host'
645	BINARY_SUBSCR     None
646	UNPACK_SEQUENCE_3 None
649	STORE_FAST        'ouser'
652	STORE_FAST        'opasswd'
655	STORE_FAST        'oacct'

658	LOAD_FAST         'user'
661	JUMP_IF_TRUE      '667'
664	LOAD_FAST         'ouser'
667	STORE_FAST        'user'

670	LOAD_FAST         'passwd'
673	JUMP_IF_TRUE      '679'
676	LOAD_FAST         'opasswd'
679	STORE_FAST        'passwd'

682	LOAD_FAST         'acct'
685	JUMP_IF_TRUE      '691'
688	LOAD_FAST         'oacct'
691	STORE_FAST        'acct'
694	JUMP_FORWARD      '697'
697_0	COME_FROM         '694'

697	LOAD_FAST         'user'
700	r self.__defuser
        passwd = passwd or self.__defpasswd
        acct = acct or self.__defacct
        return (user, passwd, acct)

    def get_macros(self):
        return self.__macros.keys()

    def get_macro(self, macro):
        return self.__macros[macro]


def test():
    debugging = 0
    rcfile = None
    while sys.argv[1] == '-d':
        debugging = debugging + 1
        del sys.argv[1]

    if sys.argv[1][:2] == '-r':
        rcfile = sys.argv[1][2:]
        del sys.argv[1]
    host = sys.argv[1]
    ftp = FTP(host)
    ftp.set_debuglevel(debugging)
    userid = passwd = acct = ''
    try:
        netrc = Netrc(rcfile)
    except IOError:
        if rcfile is not None:
            sys.stderr.write('Could not open account file -- using anonymous login.')
    else:
        try:
            userid, passwd, acct = netrc.get_account(host)
        except KeyError:
            sys.stderr.write('No account -- using anonymous login.')

    ftp.login(userid, passwd, acct)
    for file in sys.argv[2:]:
        if file[:2] == '-l':
            ftp.dir(file[2:])
        elif file[:2] == '-d':
            cmd = 'CWD'
            if file[2:]:
                cmd = cmd + ' ' + file[2:]
            resp = ftp.sendcmd(cmd)
        elif file == '-p':
            ftp.set_pasv(not ftp.passiveserver)
        else:
            ftp.retrbinary('RETR ' + file, sys.stdout.write, 1024)

    ftp.quit()
    return


if __name__ == '__main__':
    test()# decompiled 0 files: 0 okay, 1 failed, 0 verify failed
# 2013.08.22 22:13:02 Pacific Daylight Time
LOAD_FAST         'passwd'
703	LOAD_FAST         'acct'
706	BUILD_TUPLE_3     None
709	LOAD_FAST         'self'
712	LOAD_ATTR         '__hosts'
715	LOAD_FAST         'host'
718	STORE_SUBSCR      None
719	JUMP_BACK         '112'
722	JUMP_BACK         '112'
725	POP_BLOCK         None
726_0	COME_FROM         '109'

726	LOAD_FAST         'fp'
729	LOAD_ATTR         'close'
732	CALL_FUNCTION_0   None
735	POP_TOP           None
736	LOAD_CONST        None
739	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 725

