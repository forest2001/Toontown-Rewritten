# 2013.08.22 22:13:14 Pacific Daylight Time
# Embedded file name: os
import sys
_names = sys.builtin_module_names
__all__ = ['altsep',
 'curdir',
 'pardir',
 'sep',
 'pathsep',
 'linesep',
 'defpath',
 'name',
 'path',
 'devnull']

def _get_exports_list(module):
    try:
        return list(module.__all__)
    except AttributeError:
        return [ n for n in dir(module) if n[0] != '_' ]


if 'posix' in _names:
    name = 'posix'
    linesep = '\n'
    from posix import *
    try:
        from posix import _exit
    except ImportError:
        pass

    import posixpath as path
    import posix
    __all__.extend(_get_exports_list(posix))
    del posix
elif 'nt' in _names:
    name = 'nt'
    linesep = '\r\n'
    from nt import *
    try:
        from nt import _exit
    except ImportError:
        pass

    import ntpath as path
    import nt
    __all__.extend(_get_exports_list(nt))
    del nt
elif 'os2' in _names:
    name = 'os2'
    linesep = '\r\n'
    from os2 import *
    try:
        from os2 import _exit
    except ImportError:
        pass

    if sys.version.find('EMX GCC') == -1:
        import ntpath as path
    else:
        import os2emxpath as path
        from _emx_link import link
    import os2
    __all__.extend(_get_exports_list(os2))
    del os2
elif 'mac' in _names:
    name = 'mac'
    linesep = '\r'
    from mac import *
    try:
        from mac import _exit
    except ImportError:
        pass

    import macpath as path
    import mac
    __all__.extend(_get_exports_list(mac))
    del mac
elif 'ce' in _names:
    name = 'ce'
    linesep = '\r\n'
    from ce import *
    try:
        from ce import _exit
    except ImportError:
        pass

    import ntpath as path
    import ce
    __all__.extend(_get_exports_list(ce))
    del ce
elif 'riscos' in _names:
    name = 'riscos'
    linesep = '\n'
    from riscos import *
    try:
        from riscos import _exit
    except ImportError:
        pass

    import riscospath as path
    import riscos
    __all__.extend(_get_exports_list(riscos))
    del riscos
else:
    raise ImportError, 'no os specific module found'
sys.modules['os.path'] = path
from os.path import curdir, pardir, sep, pathsep, defpath, extsep, altsep, devnull
del _names

def makedirs(name, mode = 511):
    head, tail = path.split(name)
    if not tail:
        head, tail = path.split(head)
    if head and tail and not path.exists(head):
        makedirs(head, mode)
        if tail == curdir:
            return
    mkdir(name, mode)


def removedirs(name):
    rmdir(name)
    head, tail = path.split(name)
    if not tail:
        head, tail = path.split(head)
    while head and tail:
        try:
            rmdir(head)
        except error:
            break

        head, tail = path.split(head)


def renames(old, new):
    head, tail = path.split(new)
    if head and tail and not path.exists(head):
        makedirs(head)
    rename(old, new)
    head, tail = path.split(old)
    if head and tail:
        try:
            removedirs(head)
        except error:
            pass


__all__.extend(['makedirs', 'removedirs', 'renames'])

def walk--- This code section failed: ---

0	LOAD_CONST        ('join', 'isdir', 'islink')
3	IMPORT_NAME       'os.path'
6	IMPORT_FROM       'join'
9	STORE_FAST        'join'
12	IMPORT_FROM       'isdir'
15	STORE_FAST        'isdir'
18	IMPORT_FROM       'islink'
21	STORE_FAST        'islink'
24	POP_TOP           None

25	SETUP_EXCEPT      '44'

28	LOAD_GLOBAL       'listdir'
31	LOAD_FAST         'top'
34	CALL_FUNCTION_1   None
37	STORE_FAST        'names'
40	POP_BLOCK         None
41	JUMP_FORWARD      '92'
44_0	COME_FROM         '25'

44	DUP_TOP           None
45	LOAD_GLOBAL       'error'
48	COMPARE_OP        'exception match'
51	JUMP_IF_FALSE     '91'
54	POP_TOP           None
55	STORE_FAST        'err'
58	POP_TOP           None

59	LOAD_FAST         'onerror'
62	LOAD_CONST        None
65	COMPARE_OP        'is not'
68	JUMP_IF_FALSE     '84'

71	LOAD_FAST         'onerror'
74	LOAD_FAST         'err'
77	CALL_FUNCTION_1   None
80	POP_TOP           None
81	JUMP_FORWARD      '84'
84_0	COME_FROM         '81'

84	LOAD_CONST        None
87	RETURN_VALUE      None
88	JUMP_FORWARD      '92'
91	END_FINALLY       None
92_0	COME_FROM         '41'
92_1	COME_FROM         '91'

92	BUILD_LIST_0      None
95	BUILD_LIST_0      None
98	ROT_TWO           None
99	STORE_FAST        'dirs'
102	STORE_FAST        'nondirs'

105	SETUP_LOOP        '172'
108	LOAD_FAST         'names'
111	GET_ITER          None
112	FOR_ITER          '171'
115	STORE_FAST        'name'

118	LOAD_FAST         'isdir'
121	LOAD_FAST         'join'
124	LOAD_FAST         'top'
127	LOAD_FAST         'name'
130	CALL_FUNCTION_2   None
133	CALL_FUNCTION_1   None
136	JUMP_IF_FALSE     '155'

139	LOAD_FAST         'dirs'
142	LOAD_ATTR         'append'
145	LOAD_FAST         'name'
148	CALL_FUNCTION_1   None
151	POP_TOP           None
152	JUMP_BACK         '112'

155	LOAD_FAST         'nondirs'
158	LOAD_ATTR         'append'
161	LOAD_FAST         'name'
164	CALL_FUNCTION_1   None
167	POP_TOP           None
168	JUMP_BACK         '112'
171	POP_BLOCK         None
172_0	COME_FROM         '105'

172	LOAD_FAST         'topdown'
175	JUMP_IF_FALSE     '194'

178	LOAD_FAST         'top'
181	LOAD_FAST         'dirs'
184	LOAD_FAST         'nondirs'
187	BUILD_TUPLE_3     None
190	YIELD_VALUE       None
191	JUMP_FORWARD      '194'
194_0	COME_FROM         '191'

194	SETUP_LOOP        '274'
197	LOAD_FAST         'dirs'
200	GET_ITER          None
201	FOR_ITER          '273'
204	STORE_FAST        'name'

207	LOAD_FAST         'join'
210	LOAD_FAST         'top'
213	LOAD_FAST         'name'
216	CALL_FUNCTION_2   None
219	STORE_FAST        'path'

222	LOAD_FAST         'islink'
225	LOAD_FAST         'path'
228	CALL_FUNCTION_1   None
231	JUMP_IF_TRUE      '270'

234	SETUP_LOOP        '270'
237	LOAD_GLOBAL       'walk'
240	LOAD_FAST         'path'
243	LOAD_FAST         'topdown'
246	LOAD_FAST         'onerror'
249	CALL_FUNCTION_3   None
252	GET_ITER          None
253	FOR_ITER          '266'
256	STORE_FAST        'x'

259	LOAD_FAST         'x'
262	YIELD_VALUE       None
263	JUMP_BACK         '253'
266	POP_BLOCK         None
267_0	COME_FROM         '234'
267	JUMP_BACK         '201'
270	JUMP_BACK         '201'
273	POP_BLOCK         None
274_0	COME_FROM         '194'

274	LOAD_FAST         'topdown'
277	JUMP_IF_TRUE      '296'

280	LOAD_FAST         'top'
283	LOAD_FAST         'dirs'
286	LOAD_FAST         'nondirs'
289	BUILD_TUPLE_3     None
292	YIELD_VALUE       None
293	JUMP_FORWARD      '296'
296_0	COME_FROM         '293'
296	LOAD_CONST        None
299	RETURN_VALUE      None

Syntax error at or near `COME_FROM' token at offset 194_0


__all__.append('walk')
try:
    environ
except NameError:
    environ = {}

def execl(file, *args):
    execv(file, args)


def execle(file, *args):
    env = args[-1]
    execve(file, args[:-1], env)


def execlp(file, *args):
    execvp(file, args)


def execlpe(file, *args):
    env = args[-1]
    execvpe(file, args[:-1], env)


def execvp(file, args):
    _execvpe(file, args)


def execvpe(file, args, env):
    _execvpe(file, args, env)


__all__.extend(['execl',
 'execle',
 'execlp',
 'execlpe',
 'execvp',
 'execvpe'])

def _execvpe(file, args, env = None):
    from errno import ENOENT, ENOTDIR
    if env is not None:
        func = execve
        argrest = (args, env)
    else:
        func = execv
        argrest = (args,)
        env = environ
    head, tail = path.split(file)
    if head:
        func(file, *argrest)
        return
    if 'PATH' in env:
        envpath = env['PATH']
    else:
        envpath = defpath
    PATH = envpath.split(pathsep)
    saved_exc = None
    saved_tb = None
    for dir in PATH:
        fullname = path.join(dir, file)
        try:
            func(fullname, *argrest)
        except error as e:
            tb = sys.exc_info()[2]
            if e.errno != ENOENT and e.errno != ENOTDIR and saved_exc is None:
                saved_exc = e
                saved_tb = tb

    if saved_exc:
        raise error, saved_exc, saved_tb
    raise error, e, tb
    return


try:
    putenv
except NameError:
    pass
else:
    import UserDict
    if name in ('os2', 'nt'):

        def unsetenv(key):
            putenv(key, '')


    if name == 'riscos':
        from riscosenviron import _Environ
    elif name in ('os2', 'nt'):

        class _Environ(UserDict.IterableUserDict):
            __module__ = __name__

            def __init__(self, environ):
                UserDict.UserDict.__init__(self)
                data = self.data
                for k, v in environ.items():
                    data[k.upper()] = v

            def __setitem__(self, key, item):
                putenv(key, item)
                self.data[key.upper()] = item

            def __getitem__(self, key):
                return self.data[key.upper()]

            try:
                unsetenv
            except NameError:

                def __delitem__(self, key):
                    del self.data[key.upper()]

            else:

                def __delitem__(self, key):
                    unsetenv(key)
                    del self.data[key.upper()]

            def has_key(self, key):
                return key.upper() in self.data

            def __contains__(self, key):
                return key.upper() in self.data

            def get(self, key, failobj = None):
                return self.data.get(key.upper(), failobj)

            def update(self, dict = None, **kwargs):
                if dict:
                    try:
                        keys = dict.keys()
                    except AttributeError:
                        for k, v in dict:
                            self[k] = v

                    else:
                        for k in keys:
                            self[k] = dict[k]

                if kwargs:
                    self.update(kwargs)

            def copy(self):
                return dict(self)


    else:

        class _Environ(UserDict.IterableUserDict):
            __module__ = __name__

            def __init__(self, environ):
                UserDict.UserDict.__init__(self)
                self.data = environ

            def __setitem__(self, key, item):
                putenv(key, item)
                self.data[key] = item

            def update(self, dict = None, **kwargs):
                if dict:
                    try:
                        keys = dict.keys()
                    except AttributeError:
                        for k, v in dict:
                            self[k] = v

                    else:
                        for k in keys:
                            self[k] = dict[k]

                if kwargs:
                    self.update(kwargs)

            try:
                unsetenv
            except NameError:
                pass
            else:

                def __delitem__(self, key):
                    unsetenv(key)
                    del self.data[key]

            def copy(self):
                return dict(self)


    environ = _Environ(environ)

def getenv(key, default = None):
    return environ.get(key, default)


__all__.append('getenv')

def _exists(name):
    try:
        eval(name)
        return True
    except NameError:
        return False


if _exists('fork') and not _exists('spawnv') and _exists('execv'):
    P_WAIT = 0
    P_NOWAIT = P_NOWAITO = 1

    def _spawnvef--- This code section failed: ---

0	LOAD_GLOBAL       'fork'
3	CALL_FUNCTION_0   None
6	STORE_FAST        'pid'

9	LOAD_FAST         'pid'
12	JUMP_IF_TRUE      '86'

15	SETUP_EXCEPT      '66'

18	LOAD_FAST         'env'
21	LOAD_CONST        None
24	COMPARE_OP        'is'
27	JUMP_IF_FALSE     '46'

30	LOAD_FAST         'func'
33	LOAD_FAST         'file'
36	LOAD_FAST         'args'
39	CALL_FUNCTION_2   None
42	POP_TOP           None
43	JUMP_FORWARD      '62'

46	LOAD_FAST         'func'
49	LOAD_FAST         'file'
52	LOAD_FAST         'args'
55	LOAD_FAST         'env'
58	CALL_FUNCTION_3   None
61	POP_TOP           None
62_0	COME_FROM         '43'
62	POP_BLOCK         None
63	JUMP_ABSOLUTE     '211'
66_0	COME_FROM         '15'

66	POP_TOP           None
67	POP_TOP           None
68	POP_TOP           None

69	LOAD_GLOBAL       '_exit'
72	LOAD_CONST        127
75	CALL_FUNCTION_1   None
78	POP_TOP           None
79	JUMP_ABSOLUTE     '211'
82	END_FINALLY       None
83_0	COME_FROM         '82'
83	JUMP_FORWARD      '211'

86	LOAD_FAST         'mode'
89	LOAD_GLOBAL       'P_NOWAIT'
92	COMPARE_OP        '=='
95	JUMP_IF_FALSE     '105'

98	LOAD_FAST         'pid'
101	RETURN_VALUE      None
102	JUMP_FORWARD      '105'
105_0	COME_FROM         '102'

105	SETUP_LOOP        '211'

108	LOAD_GLOBAL       'waitpid'
111	LOAD_FAST         'pid'
114	LOAD_CONST        0
117	CALL_FUNCTION_2   None
120	UNPACK_SEQUENCE_2 None
123	STORE_FAST        'wpid'
126	STORE_FAST        'sts'

129	LOAD_GLOBAL       'WIFSTOPPED'
132	LOAD_FAST         'sts'
135	CALL_FUNCTION_1   None
138	JUMP_IF_FALSE     '147'

141	CONTINUE          '108'
144	JUMP_BACK         '108'

147	LOAD_GLOBAL       'WIFSIGNALED'
150	LOAD_FAST         'sts'
153	CALL_FUNCTION_1   None
156	JUMP_IF_FALSE     '173'

159	LOAD_GLOBAL       'WTERMSIG'
162	LOAD_FAST         'sts'
165	CALL_FUNCTION_1   None
168	UNARY_NEGATIVE    None
169	RETURN_VALUE      None
170	JUMP_BACK         '108'

173	LOAD_GLOBAL       'WIFEXITED'
176	LOAD_FAST         'sts'
179	CALL_FUNCTION_1   None
182	JUMP_IF_FALSE     '198'

185	LOAD_GLOBAL       'WEXITSTATUS'
188	LOAD_FAST         'sts'
191	CALL_FUNCTION_1   None
194	RETURN_VALUE      None
195	JUMP_BACK         '108'

198	LOAD_GLOBAL       'error'
201	LOAD_CONST        'Not stopped, signaled or exited???'
204	RAISE_VARARGS_2   None
207	JUMP_BACK         '108'
210	POP_BLOCK         None
211_0	COME_FROM         '83'
211_1	COME_FROM         '105'
211	LOAD_CONST        None
214	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 210


    def spawnv(mode, file, args):
        return _spawnvef(mode, file, args, None, execv)


    def spawnve(mode, file, args, env):
        return _spawnvef(mode, file, args, env, execve)


    def spawnvp(mode, file, args):
        return _spawnvef(mode, file, args, None, execvp)


    def spawnvpe(mode, file, args, env):
        return _spawnvef(mode, file, args, env, execvpe)


if _exists('spawnv'):

    def spawnl(mode, file, *args):
        return spawnv(mode, file, args)


    def spawnle(mode, file, *args):
        env = args[-1]
        return spawnve(mode, file, args[:-1], env)


    __all__.extend(['spawnv',
     'spawnve',
     'spawnl',
     'spawnle'])
if _exists('spawnvp'):

    def spawnlp(mode, file, *args):
        return spawnvp(mode, file, args)


    def spawnlpe(mode, file, *args):
        env = args[-1]
        return spawnvpe(mode, file, args[:-1], env)


    __all__.extend(['spawnvp',
     'spawnvpe',
     'spawnlp',
     'spawnlpe'])
if _exists('fork'):
    if not _exists('popen2'):

        def popen2(cmd, mode = 't', bufsize = -1):
            import popen2
            stdout, stdin = popen2.popen2(cmd, bufsize)
            return (stdin, stdout)


        __all__.append('popen2')
    if not _exists('popen3'):

        def popen3(cmd, mode = 't', bufsize = -1):
            import popen2
            stdout, stdin, stderr = popen2.popen3(cmd, bufsize)
            return (stdin, stdout, stderr)


        __all__.append('popen3')
    if not _exists('popen4'):

        def popen4(cmd, mode = 't', bufsize = -1):
            import popen2
            stdout, stdin = popen2.popen4(cmd, bufsize)
            return (stdin, stdout)


        __all__.append('popen4')
import copy_reg as _copy_reg

def _make_stat_result(tup, dict):
    return stat_result(tup, dict)


def _pickle_stat_result(sr):
    type, args = sr.__reduce__()
    return (_make_stat_result, args)


try:
    _copy_reg.pickle(stat_result, _pickle_stat_result, _make_stat_result)
except NameError:
    pass

def _make_statvfs_result(tup, dict):
    return statvfs_result(tup, dict)


def _pickle_statvfs_result(sr):
    type, args = sr.__reduce__()
    return (_make_statvfs_result, args)


try:
    _copy_reg.pickle(statvfs_result, _pickle_statvfs_result, _make_statvfs_result)
except NameError:
    pass

if not _exists('urandom'):
    _urandomfd = None

    def urandom(n):
        global _urandomfd
        if _urandomfd is None:
            try:
                _urandomfd = open('/dev/urandom', O_RDONLY)
            except:
                _urandomfd = NotImplementedError

        if _urandomfd is NotImplementedError:
            raise NotImplementedError('/dev/urandom (or equivalent) not found')
        bytes = ''
        while len(bytes) < n:
            bytes += read(_urandomfd, n - len(bytes))

        return bytes# decompiled 0 files: 0 okay, 1 failed, 0 verify failed
# 2013.08.22 22:13:15 Pacific Daylight Time

# Can't uncompyle C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\os.pyc
Traceback (most recent call last):
  File "C:\python27\lib\uncompyle2\__init__.py", line 206, in main
    uncompyle_file(infile, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 143, in uncompyle_file
    uncompyle(version, co, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 132, in uncompyle
    raise walk.ERROR
ParserError: --- This code section failed: ---

0	LOAD_GLOBAL       'fork'
3	CALL_FUNCTION_0   None
6	STORE_FAST        'pid'

9	LOAD_FAST         'pid'
12	JUMP_IF_TRUE      '86'

15	SETUP_EXCEPT      '66'

18	LOAD_FAST         'env'
21	LOAD_CONST        None
24	COMPARE_OP        'is'
27	JUMP_IF_FALSE     '46'

30	LOAD_FAST         'func'
33	LOAD_FAST         'file'
36	LOAD_FAST         'args'
39	CALL_FUNCTION_2   None
42	POP_TOP           None
43	JUMP_FORWARD      '62'

46	LOAD_FAST         'func'
49	LOAD_FAST         'file'
52	LOAD_FAST         'args'
55	LOAD_FAST         'env'
58	CALL_FUNCTION_3   None
61	POP_TOP           None
62_0	COME_FROM         '43'
62	POP_BLOCK         None
63	JUMP_ABSOLUTE     '211'
66_0	COME_FROM         '15'

66	POP_TOP           None
67	POP_TOP           None
68	POP_TOP           None

69	LOAD_GLOBAL       '_exit'
72	LOAD_CONST        127
75	CALL_FUNCTION_1   None
78	POP_TOP           None
79	JUMP_ABSOLUTE     '211'
82	END_FINALLY       None
83_0	COME_FROM         '82'
83	JUMP_FORWARD      '211'

86	LOAD_FAST         'mode'
89	LOAD_GLOBAL       'P_NOWAIT'
92	COMPARE_OP        '=='
95	JUMP_IF_FALSE     '105'

98	LOAD_FAST         'pid'
101	RETURN_VALUE      None
102	JUMP_FORWARD      '105'
105_0	COME_FROM         '102'

105	SETUP_LOOP        '211'

108	LOAD_GLOBAL       'waitpid'
111	LOAD_FAST         'pid'
114	LOAD_CONST        0
117	CALL_FUNCTION_2   None
120	UNPACK_SEQUENCE_2 None
123	STORE_FAST        'wpid'
126	STORE_FAST        'sts'

129	LOAD_GLOBAL       'WIFSTOPPED'
132	LOAD_FAST         'sts'
135	CALL_FUNCTION_1   None
138	JUMP_IF_FALSE     '147'

141	CONTINUE          '108'
144	JUMP_BACK         '108'

147	LOAD_GLOBAL       'WIFSIGNALED'
150	LOAD_FAST         'sts'
153	CALL_FUNCTION_1   None
156	JUMP_IF_FALSE     '173'

159	LOAD_GLOBAL       'WTERMSIG'
162	LOAD_FAST         'sts'
165	CALL_FUNCTION_1   None
168	UNARY_NEGATIVE    None
169	RETURN_VALUE      None
170	JUMP_BACK         '108'

173	LOAD_GLOBAL       'WIFEXITED'
176	LOAD_FAST         'sts'
179	CALL_FUNCTION_1   None
182	JUMP_IF_FALSE     '198'

185	LOAD_GLOBAL       'WEXITSTATUS'
188	LOAD_FAST         'sts'
191	CALL_FUNCTION_1   None
194	RETURN_VALUE      None
195	JUMP_BACK         '108'

198	LOAD_GLOBAL       'error'
201	LOAD_CONST        'Not stopped, signaled or exited???'
204	RAISE_VARARGS_2   None
207	JUMP_BACK         '108'
210	POP_BLOCK         None
211_0	COME_FROM         '83'
211_1	COME_FROM         '105'
211	LOAD_CONST        None
214	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 210

