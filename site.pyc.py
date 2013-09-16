# 2013.08.22 22:13:28 Pacific Daylight Time
# Embedded file name: site
import sys
import os
import __builtin__

def makepath(*paths):
    dir = os.path.abspath(os.path.join(*paths))
    return (dir, os.path.normcase(dir))


def abs__file__():
    for m in sys.modules.values():
        try:
            m.__file__ = os.path.abspath(m.__file__)
        except AttributeError:
            continue


def removeduppaths():
    L = []
    known_paths = set()
    for dir in sys.path:
        dir, dircase = makepath(dir)
        if dircase not in known_paths:
            L.append(dir)
            known_paths.add(dircase)

    sys.path[:] = L
    return known_paths


def addbuilddir():
    from distutils.util import get_platform
    s = 'build/lib.%s-%.3s' % (get_platform(), sys.version)
    s = os.path.join(os.path.dirname(sys.path[-1]), s)
    sys.path.append(s)


def _init_pathinfo():
    d = set()
    for dir in sys.path:
        try:
            if os.path.isdir(dir):
                dir, dircase = makepath(dir)
                d.add(dircase)
        except TypeError:
            continue

    return d


def addpackage(sitedir, name, known_paths):
    if known_paths is None:
        _init_pathinfo()
        reset = 1
    else:
        reset = 0
    fullname = os.path.join(sitedir, name)
    try:
        f = open(fullname, 'rU')
    except IOError:
        return

    try:
        for line in f:
            if line.startswith('#'):
                continue
            if line.startswith('import'):
                exec line
                continue
            line = line.rstrip()
            dir, dircase = makepath(sitedir, line)
            if dircase not in known_paths and os.path.exists(dir):
                sys.path.append(dir)
                known_paths.add(dircase)

    finally:
        f.close()

    if reset:
        known_paths = None
    return known_paths


def addsitedir(sitedir, known_paths = None):
    if known_paths is None:
        known_paths = _init_pathinfo()
        reset = 1
    else:
        reset = 0
    sitedir, sitedircase = makepath(sitedir)
    if sitedircase not in known_paths:
        sys.path.append(sitedir)
    try:
        names = os.listdir(sitedir)
    except os.error:
        return

    names.sort()
    for name in names:
        if name.endswith(os.extsep + 'pth'):
            addpackage(sitedir, name, known_paths)

    if reset:
        known_paths = None
    return known_paths


def addsitepackages(known_paths):
    prefixes = [sys.prefix]
    if sys.exec_prefix != sys.prefix:
        prefixes.append(sys.exec_prefix)
    for prefix in prefixes:
        if prefix:
            if sys.platform in ('os2emx', 'riscos'):
                sitedirs = [os.path.join(prefix, 'Lib', 'site-packages')]
            elif os.sep == '/':
                sitedirs = [os.path.join(prefix, 'lib', 'python' + sys.version[:3], 'site-packages'), os.path.join(prefix, 'lib', 'site-python')]
            else:
                sitedirs = [prefix, os.path.join(prefix, 'lib', 'site-packages')]
            if sys.platform == 'darwin':
                if 'Python.framework' in prefix:
                    home = os.environ.get('HOME')
                    if home:
                        sitedirs.append(os.path.join(home, 'Library', 'Python', sys.version[:3], 'site-packages'))
            for sitedir in sitedirs:
                if os.path.isdir(sitedir):
                    addsitedir(sitedir, known_paths)

    return None


def setBEGINLIBPATH():
    dllpath = os.path.join(sys.prefix, 'Lib', 'lib-dynload')
    libpath = os.environ['BEGINLIBPATH'].split(';')
    if libpath[-1]:
        libpath.append(dllpath)
    else:
        libpath[-1] = dllpath
    os.environ['BEGINLIBPATH'] = ';'.join(libpath)


def setquit():
    if os.sep == ':':
        exit = 'Use Cmd-Q to quit.'
    elif os.sep == '\\':
        exit = 'Use Ctrl-Z plus Return to exit.'
    else:
        exit = 'Use Ctrl-D (i.e. EOF) to exit.'
    __builtin__.quit = __builtin__.exit = exit


class _Printer(object):
    __module__ = __name__
    MAXLINES = 23

    def __init__(self, name, data, files = (), dirs = ()):
        self.__name = name
        self.__data = data
        self.__files = files
        self.__dirs = dirs
        self.__lines = None
        return

    def __setup(self):
        if self.__lines:
            return
        data = None
        for dir in self.__dirs:
            for filename in self.__files:
                filename = os.path.join(dir, filename)
                try:
                    fp = file(filename, 'rU')
                    data = fp.read()
                    fp.close()
                    break
                except IOError:
                    pass

            if data:
                break

        if not data:
            data = self.__data
        self.__lines = data.split('\n')
        self.__linecnt = len(self.__lines)
        return

    def __repr__(self):
        self.__setup()
        if len(self.__lines) <= self.MAXLINES:
            return '\n'.join(self.__lines)
        else:
            return 'Type %s() to see the full %s text' % ((self.__name,) * 2)

    def __call__--- This code section failed: ---

0	LOAD_FAST         'self'
3	LOAD_ATTR         '__setup'
6	CALL_FUNCTION_0   None
9	POP_TOP           None

10	LOAD_CONST        'Hit Return for more, or q (and Return) to quit: '
13	STORE_FAST        'prompt'

16	LOAD_CONST        0
19	STORE_FAST        'lineno'

22	SETUP_LOOP        '186'

25	SETUP_EXCEPT      '77'

28	SETUP_LOOP        '73'
31	LOAD_GLOBAL       'range'
34	LOAD_FAST         'lineno'
37	LOAD_FAST         'lineno'
40	LOAD_FAST         'self'
43	LOAD_ATTR         'MAXLINES'
46	BINARY_ADD        None
47	CALL_FUNCTION_2   None
50	GET_ITER          None
51	FOR_ITER          '72'
54	STORE_FAST        'i'

57	LOAD_FAST         'self'
60	LOAD_ATTR         '__lines'
63	LOAD_FAST         'i'
66	BINARY_SUBSCR     None
67	PRINT_ITEM        None
68	PRINT_NEWLINE_CONT None
69	JUMP_BACK         '51'
72	POP_BLOCK         None
73_0	COME_FROM         '28'
73	POP_BLOCK         None
74	JUMP_FORWARD      '95'
77_0	COME_FROM         '25'

77	DUP_TOP           None
78	LOAD_GLOBAL       'IndexError'
81	COMPARE_OP        'exception match'
84	JUMP_IF_FALSE     '94'
87	POP_TOP           None
88	POP_TOP           None
89	POP_TOP           None

90	BREAK_LOOP        None
91	JUMP_BACK         '25'
94	END_FINALLY       None
95_0	COME_FROM         '74'

95	LOAD_FAST         'lineno'
98	LOAD_FAST         'self'
101	LOAD_ATTR         'MAXLINES'
104	INPLACE_ADD       None
105	STORE_FAST        'lineno'

108	LOAD_CONST        None
111	STORE_FAST        'key'

114	SETUP_LOOP        '166'
117	LOAD_FAST         'key'
120	LOAD_CONST        None
123	COMPARE_OP        'is'
126	JUMP_IF_FALSE     '165'

129	LOAD_GLOBAL       'raw_input'
132	LOAD_FAST         'prompt'
135	CALL_FUNCTION_1   None
138	STORE_FAST        'key'

141	LOAD_FAST         'key'
144	LOAD_CONST        ('', 'q')
147	COMPARE_OP        'not in'
150	JUMP_IF_FALSE     '162'

153	LOAD_CONST        None
156	STORE_FAST        'key'
159	JUMP_BACK         '117'
162	JUMP_BACK         '117'
165	POP_BLOCK         None
166_0	COME_FROM         '114'

166	LOAD_FAST         'key'
169	LOAD_CONST        'q'
172	COMPARE_OP        '=='
175	JUMP_IF_FALSE     '182'

178	BREAK_LOOP        None
179	JUMP_BACK         '25'
182_0	COME_FROM         '94'
182	JUMP_BACK         '25'
185	POP_BLOCK         None
186_0	COME_FROM         '22'
186	LOAD_CONST        None
189	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 185


def setcopyright():
    __builtin__.copyright = _Printer('copyright', sys.copyright)
    if sys.platform[:4] == 'java':
        __builtin__.credits = _Printer('credits', 'Jython is maintained by the Jython developers (www.jython.org).')
    else:
        __builtin__.credits = _Printer('credits', '    Thanks to CWI, CNRI, BeOpen.com, Zope Corporation and a cast of thousands\n    for supporting Python development.  See www.python.org for more information.')
    here = os.path.dirname(os.__file__)
    __builtin__.license = _Printer('license', 'See http://www.python.org/%.3s/license.html' % sys.version, ['LICENSE.txt', 'LICENSE'], [os.path.join(here, os.pardir), here, os.curdir])


class _Helper(object):
    __module__ = __name__

    def __repr__(self):
        return 'Type help() for interactive help, or help(object) for help about object.'

    def __call__(self, *args, **kwds):
        import pydoc
        return pydoc.help(*args, **kwds)


def sethelper():
    __builtin__.help = _Helper()


def aliasmbcs():
    if sys.platform == 'win32':
        import locale, codecs
        enc = locale.getdefaultlocale()[1]
        if enc.startswith('cp'):
            try:
                codecs.lookup(enc)
            except LookupError:
                import encodings
                encodings._cache[enc] = encodings._unknown
                encodings.aliases.aliases[enc] = 'mbcs'


def setencoding():
    encoding = 'ascii'
    if encoding != 'ascii':
        sys.setdefaultencoding(encoding)


def execsitecustomize():
    try:
        import sitecustomize
    except ImportError:
        pass


def main():
    abs__file__()
    paths_in_sys = removeduppaths()
    if os.name == 'posix' and sys.path and os.path.basename(sys.path[-1]) == 'Modules':
        addbuilddir()
    paths_in_sys = addsitepackages(paths_in_sys)
    if sys.platform == 'os2emx':
        setBEGINLIBPATH()
    setquit()
    setcopyright()
    sethelper()
    aliasmbcs()
    setencoding()
    execsitecustomize()
    if hasattr(sys, 'setdefaultencoding'):
        del sys.setdefaultencoding


main()

def _test():
    print 'sys.path = ['
    for dir in sys.path:
        print '    %r,' % (dir,)

    print ']'


if __name__ == '__main__':
    _test()# decompiled 0 files: 0 okay, 1 failed, 0 verify failed
# 2013.08.22 22:13:28 Pacific Daylight Time

# Can't uncompyle C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\site.pyc
Traceback (most recent call last):
  File "C:\python27\lib\uncompyle2\__init__.py", line 206, in main
    uncompyle_file(infile, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 143, in uncompyle_file
    uncompyle(version, co, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 132, in uncompyle
    raise walk.ERROR
ParserError: --- This code section failed: ---

0	LOAD_FAST         'self'
3	LOAD_ATTR         '__setup'
6	CALL_FUNCTION_0   None
9	POP_TOP           None

10	LOAD_CONST        'Hit Return for more, or q (and Return) to quit: '
13	STORE_FAST        'prompt'

16	LOAD_CONST        0
19	STORE_FAST        'lineno'

22	SETUP_LOOP        '186'

25	SETUP_EXCEPT      '77'

28	SETUP_LOOP        '73'
31	LOAD_GLOBAL       'range'
34	LOAD_FAST         'lineno'
37	LOAD_FAST         'lineno'
40	LOAD_FAST         'self'
43	LOAD_ATTR         'MAXLINES'
46	BINARY_ADD        None
47	CALL_FUNCTION_2   None
50	GET_ITER          None
51	FOR_ITER          '72'
54	STORE_FAST        'i'

57	LOAD_FAST         'self'
60	LOAD_ATTR         '__lines'
63	LOAD_FAST         'i'
66	BINARY_SUBSCR     None
67	PRINT_ITEM        None
68	PRINT_NEWLINE_CONT None
69	JUMP_BACK         '51'
72	POP_BLOCK         None
73_0	COME_FROM         '28'
73	POP_BLOCK         None
74	JUMP_FORWARD      '95'
77_0	COME_FROM         '25'

77	DUP_TOP           None
78	LOAD_GLOBAL       'IndexError'
81	COMPARE_OP        'exception match'
84	JUMP_IF_FALSE     '94'
87	POP_TOP           None
88	POP_TOP           None
89	POP_TOP           None

90	BREAK_LOOP        None
91	JUMP_BACK         '25'
94	END_FINALLY       None
95_0	COME_FROM         '74'

95	LOAD_FAST         'lineno'
98	LOAD_FAST         'self'
101	LOAD_ATTR         'MAXLINES'
104	INPLACE_ADD       None
105	STORE_FAST        'lineno'

108	LOAD_CONST        None
111	STORE_FAST        'key'

114	SETUP_LOOP        '166'
117	LOAD_FAST         'key'
120	LOAD_CONST        None
123	COMPARE_OP        'is'
126	JUMP_IF_FALSE     '165'

129	LOAD_GLOBAL       'raw_input'
132	LOAD_FAST         'prompt'
135	CALL_FUNCTION_1   None
138	STORE_FAST        'key'

141	LOAD_FAST         'key'
144	LOAD_CONST        ('', 'q')
147	COMPARE_OP        'not in'
150	JUMP_IF_FALSE     '162'

153	LOAD_CONST        None
156	STORE_FAST        'key'
159	JUMP_BACK         '117'
162	JUMP_BACK         '117'
165	POP_BLOCK         None
166_0	COME_FROM         '114'

166	LOAD_FAST         'key'
169	LOAD_CONST        'q'
172	COMPARE_OP        '=='
175	JUMP_IF_FALSE     '182'

178	BREAK_LOOP        None
179	JUMP_BACK         '25'
182_0	COME_FROM         '94'
182	JUMP_BACK         '25'
185	POP_BLOCK         None
186_0	COME_FROM         '22'
186	LOAD_CONST        None
189	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 185

