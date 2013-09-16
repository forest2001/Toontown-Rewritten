# 2013.08.22 22:13:10 Pacific Daylight Time
# Embedded file name: mimetools
import os
import rfc822
import tempfile
__all__ = ['Message',
 'choose_boundary',
 'encode',
 'decode',
 'copyliteral',
 'copybinary']

class Message(rfc822.Message):
    __module__ = __name__

    def __init__(self, fp, seekable = 1):
        rfc822.Message.__init__(self, fp, seekable)
        self.encodingheader = self.getheader('content-transfer-encoding')
        self.typeheader = self.getheader('content-type')
        self.parsetype()
        self.parseplist()

    def parsetype(self):
        str = self.typeheader
        if str is None:
            str = 'text/plain'
        if ';' in str:
            i = str.index(';')
            self.plisttext = str[i:]
            str = str[:i]
        else:
            self.plisttext = ''
        fields = str.split('/')
        for i in range(len(fields)):
            fields[i] = fields[i].strip().lower()

        self.type = '/'.join(fields)
        self.maintype = fields[0]
        self.subtype = '/'.join(fields[1:])
        return

    def parseplist(self):
        str = self.plisttext
        self.plist = []
        while str[:1] == ';':
            str = str[1:]
            if ';' in str:
                end = str.index(';')
            else:
                end = len(str)
            f = str[:end]
            if '=' in f:
                i = f.index('=')
                f = f[:i].strip().lower() + '=' + f[i + 1:].strip()
            self.plist.append(f.strip())
            str = str[end:]

    def getplist(self):
        return self.plist

    def getparam(self, name):
        name = name.lower() + '='
        n = len(name)
        for p in self.plist:
            if p[:n] == name:
                return rfc822.unquote(p[n:])

        return None

    def getparamnames(self):
        result = []
        for p in self.plist:
            i = p.find('=')
            if i >= 0:
                result.append(p[:i].lower())

        return result

    def getencoding(self):
        if self.encodingheader is None:
            return '7bit'
        return self.encodingheader.lower()

    def gettype(self):
        return self.type

    def getmaintype(self):
        return self.maintype

    def getsubtype(self):
        return self.subtype


try:
    import thread
except ImportError:
    import dummy_thread as thread

_counter_lock = thread.allocate_lock()
del thread
_counter = 0

def _get_next_counter():
    global _counter
    _counter_lock.acquire()
    _counter += 1
    result = _counter
    _counter_lock.release()
    return result


_prefix = None

def choose_boundary():
    global _prefix
    import time
    if _prefix is None:
        import socket
        hostid = socket.gethostbyname(socket.gethostname())
        try:
            uid = repr(os.getuid())
        except AttributeError:
            uid = '1'

        try:
            pid = repr(os.getpid())
        except AttributeError:
            pid = '1'

        _prefix = hostid + '.' + uid + '.' + pid
    return '%s.%.3f.%d' % (_prefix, time.time(), _get_next_counter())


def decode(input, output, encoding):
    if encoding == 'base64':
        import base64
        return base64.decode(input, output)
    if encoding == 'quoted-printable':
        import quopri
        return quopri.decode(input, output)
    if encoding in ('uuencode', 'x-uuencode', 'uue', 'x-uue'):
        import uu
        return uu.decode(input, output)
    if encoding in ('7bit', '8bit'):
        return output.write(input.read())
    if encoding in decodetab:
        pipethrough(input, decodetab[encoding], output)
    else:
        raise ValueError, 'unknown Content-Transfer-Encoding: %s' % encoding


def encode(input, output, encoding):
    if encoding == 'base64':
        import base64
        return base64.encode(input, output)
    if encoding == 'quoted-printable':
        import quopri
        return quopri.encode(input, output, 0)
    if encoding in ('uuencode', 'x-uuencode', 'uue', 'x-uue'):
        import uu
        return uu.encode(input, output)
    if encoding in ('7bit', '8bit'):
        return output.write(input.read())
    if encoding in encodetab:
        pipethrough(input, encodetab[encoding], output)
    else:
        raise ValueError, 'unknown Content-Transfer-Encoding: %s' % encoding


uudecode_pipe = '(\nTEMP=/tmp/@uu.$$\nsed "s%^begin [0-7][0-7]* .*%begin 600 $TEMP%" | uudecode\ncat $TEMP\nrm $TEMP\n)'
decodetab = {'uuencode': uudecode_pipe,
 'x-uuencode': uudecode_pipe,
 'uue': uudecode_pipe,
 'x-uue': uudecode_pipe,
 'quoted-printable': 'mmencode -u -q',
 'base64': 'mmencode -u -b'}
encodetab = {'x-uuencode': 'uuencode tempfile',
 'uuencode': 'uuencode tempfile',
 'x-uue': 'uuencode tempfile',
 'uue': 'uuencode tempfile',
 'quoted-printable': 'mmencode -q',
 'base64': 'mmencode -b'}

def pipeto(input, command):
    pipe = os.popen(command, 'w')
    copyliteral(input, pipe)
    pipe.close()


def pipethrough(input, command, output):
    fd, tempname = tempfile.mkstemp()
    temp = os.fdopen(fd, 'w')
    copyliteral(input, temp)
    temp.close()
    pipe = os.popen(command + ' <' + tempname, 'r')
    copybinary(pipe, output)
    pipe.close()
    os.unlink(tempname)


def copyliteral--- This code section failed: ---

0	SETUP_LOOP        '42'

3	LOAD_FAST         'input'
6	LOAD_ATTR         'readline'
9	CALL_FUNCTION_0   None
12	STORE_FAST        'line'

15	LOAD_FAST         'line'
18	JUMP_IF_TRUE      '25'
21	BREAK_LOOP        None
22	JUMP_FORWARD      '25'
25_0	COME_FROM         '22'

25	LOAD_FAST         'output'
28	LOAD_ATTR         'write'
31	LOAD_FAST         'line'
34	CALL_FUNCTION_1   None
37	POP_TOP           None
38	JUMP_BACK         '3'
41	POP_BLOCK         None
42_0	COME_FROM         '0'

Syntax error at or near `POP_BLOCK' token at offset 41


def copybinary--- This code section failed: ---

0	LOAD_CONST        8192
3	STORE_FAST        'BUFSIZE'

6	SETUP_LOOP        '51'

9	LOAD_FAST         'input'
12	LOAD_ATTR         'read'
15	LOAD_FAST         'BUFSIZE'
18	CALL_FUNCTION_1   None
21	STORE_FAST        'line'

24	LOAD_FAST         'line'
27	JUMP_IF_TRUE      '34'
30	BREAK_LOOP        None
31	JUMP_FORWARD      '34'
34_0	COME_FROM         '31'

34	LOAD_FAST         'output'
37	LOAD_ATTR         'write'
40	LOAD_FAST         'line'
43	CALL_FUNCTION_1   None
46	POP_TOP           None
47	JUMP_BACK         '9'
50	POP_BLOCK         None
51_0	COME_FROM         '6'

Syntax error at or near `POP_BLOCK' token at offset 50# decompiled 0 files: 0 okay, 1 failed, 0 verify failed
# 2013.08.22 22:13:11 Pacific Daylight Time

# Can't uncompyle C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\mimetools.pyc
Traceback (most recent call last):
  File "C:\python27\lib\uncompyle2\__init__.py", line 206, in main
    uncompyle_file(infile, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 143, in uncompyle_file
    uncompyle(version, co, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 132, in uncompyle
    raise walk.ERROR
ParserError: --- This code section failed: ---

0	LOAD_CONST        8192
3	STORE_FAST        'BUFSIZE'

6	SETUP_LOOP        '51'

9	LOAD_FAST         'input'
12	LOAD_ATTR         'read'
15	LOAD_FAST         'BUFSIZE'
18	CALL_FUNCTION_1   None
21	STORE_FAST        'line'

24	LOAD_FAST         'line'
27	JUMP_IF_TRUE      '34'
30	BREAK_LOOP        None
31	JUMP_FORWARD      '34'
34_0	COME_FROM         '31'

34	LOAD_FAST         'output'
37	LOAD_ATTR         'write'
40	LOAD_FAST         'line'
43	CALL_FUNCTION_1   None
46	POP_TOP           None
47	JUMP_BACK         '9'
50	POP_BLOCK         None
51_0	COME_FROM         '6'

Syntax error at or near `POP_BLOCK' token at offset 50

