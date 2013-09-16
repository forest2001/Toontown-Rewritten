# 2013.08.22 22:14:56 Pacific Daylight Time
# Embedded file name: distutils.spawn
__revision__ = '$Id: spawn.py,v 1.1.1.1 2005/04/12 20:52:45 skyler Exp $'
import sys, os, string
from distutils.errors import *
from distutils import log

def spawn(cmd, search_path = 1, verbose = 0, dry_run = 0):
    if os.name == 'posix':
        _spawn_posix(cmd, search_path, dry_run=dry_run)
    elif os.name == 'nt':
        _spawn_nt(cmd, search_path, dry_run=dry_run)
    elif os.name == 'os2':
        _spawn_os2(cmd, search_path, dry_run=dry_run)
    else:
        raise DistutilsPlatformError, "don't know how to spawn programs on platform '%s'" % os.name


def _nt_quote_args(args):
    for i in range(len(args)):
        if string.find(args[i], ' ') != -1:
            args[i] = '"%s"' % args[i]

    return args


def _spawn_nt(cmd, search_path = 1, verbose = 0, dry_run = 0):
    executable = cmd[0]
    cmd = _nt_quote_args(cmd)
    if search_path:
        if not find_executable(executable):
            executable = executable
        log.info(string.join([executable] + cmd[1:], ' '))
        if not dry_run:
            try:
                rc = os.spawnv(os.P_WAIT, executable, cmd)
            except OSError as exc:
                raise DistutilsExecError, "command '%s' failed: %s" % (cmd[0], exc[-1])

            raise rc != 0 and DistutilsExecError, "command '%s' failed with exit status %d" % (cmd[0], rc)


def _spawn_os2(cmd, search_path = 1, verbose = 0, dry_run = 0):
    executable = cmd[0]
    if search_path:
        if not find_executable(executable):
            executable = executable
        log.info(string.join([executable] + cmd[1:], ' '))
        if not dry_run:
            try:
                rc = os.spawnv(os.P_WAIT, executable, cmd)
            except OSError as exc:
                raise DistutilsExecError, "command '%s' failed: %s" % (cmd[0], exc[-1])

            print rc != 0 and "command '%s' failed with exit status %d" % (cmd[0], rc)
            raise DistutilsExecError, "command '%s' failed with exit status %d" % (cmd[0], rc)


def _spawn_posix--- This code section failed: ---

0	LOAD_GLOBAL       'log'
3	LOAD_ATTR         'info'
6	LOAD_GLOBAL       'string'
9	LOAD_ATTR         'join'
12	LOAD_FAST         'cmd'
15	LOAD_CONST        ' '
18	CALL_FUNCTION_2   None
21	CALL_FUNCTION_1   None
24	POP_TOP           None

25	LOAD_FAST         'dry_run'
28	JUMP_IF_FALSE     '38'

31	LOAD_CONST        None
34	RETURN_VALUE      None
35	JUMP_FORWARD      '38'
38_0	COME_FROM         '35'

38	LOAD_FAST         'search_path'
41	JUMP_IF_FALSE     '53'
44	LOAD_GLOBAL       'os'
47	LOAD_ATTR         'execvp'
50_0	COME_FROM         '41'
50	JUMP_IF_TRUE      '59'
53	LOAD_GLOBAL       'os'
56	LOAD_ATTR         'execv'
59	STORE_FAST        'exec_fn'

62	LOAD_GLOBAL       'os'
65	LOAD_ATTR         'fork'
68	CALL_FUNCTION_0   None
71	STORE_FAST        'pid'

74	LOAD_FAST         'pid'
77	LOAD_CONST        0
80	COMPARE_OP        '=='
83	JUMP_IF_FALSE     '215'

86	SETUP_EXCEPT      '110'

89	LOAD_FAST         'exec_fn'
92	LOAD_FAST         'cmd'
95	LOAD_CONST        0
98	BINARY_SUBSCR     None
99	LOAD_FAST         'cmd'
102	CALL_FUNCTION_2   None
105	POP_TOP           None
106	POP_BLOCK         None
107	JUMP_FORWARD      '175'
110_0	COME_FROM         '86'

110	DUP_TOP           None
111	LOAD_GLOBAL       'OSError'
114	COMPARE_OP        'exception match'
117	JUMP_IF_FALSE     '174'
120	POP_TOP           None
121	STORE_FAST        'e'
124	POP_TOP           None

125	LOAD_GLOBAL       'sys'
128	LOAD_ATTR         'stderr'
131	LOAD_ATTR         'write'
134	LOAD_CONST        'unable to execute %s: %s\n'
137	LOAD_FAST         'cmd'
140	LOAD_CONST        0
143	BINARY_SUBSCR     None
144	LOAD_FAST         'e'
147	LOAD_ATTR         'strerror'
150	BUILD_TUPLE_2     None
153	BINARY_MODULO     None
154	CALL_FUNCTION_1   None
157	POP_TOP           None

158	LOAD_GLOBAL       'os'
161	LOAD_ATTR         '_exit'
164	LOAD_CONST        1
167	CALL_FUNCTION_1   None
170	POP_TOP           None
171	JUMP_FORWARD      '175'
174	END_FINALLY       None
175_0	COME_FROM         '107'
175_1	COME_FROM         '174'

175	LOAD_GLOBAL       'sys'
178	LOAD_ATTR         'stderr'
181	LOAD_ATTR         'write'
184	LOAD_CONST        'unable to execute %s for unknown reasons'
187	LOAD_FAST         'cmd'
190	LOAD_CONST        0
193	BINARY_SUBSCR     None
194	BINARY_MODULO     None
195	CALL_FUNCTION_1   None
198	POP_TOP           None

199	LOAD_GLOBAL       'os'
202	LOAD_ATTR         '_exit'
205	LOAD_CONST        1
208	CALL_FUNCTION_1   None
211	POP_TOP           None
212	JUMP_FORWARD      '501'

215	SETUP_LOOP        '501'

218	SETUP_EXCEPT      '249'

221	LOAD_GLOBAL       'os'
224	LOAD_ATTR         'waitpid'
227	LOAD_FAST         'pid'
230	LOAD_CONST        0
233	CALL_FUNCTION_2   None
236	UNPACK_SEQUENCE_2 None
239	STORE_FAST        'pid'
242	STORE_FAST        'status'
245	POP_BLOCK         None
246	JUMP_FORWARD      '328'
249_0	COME_FROM         '218'

249	DUP_TOP           None
250	LOAD_GLOBAL       'OSError'
253	COMPARE_OP        'exception match'
256	JUMP_IF_FALSE     '327'
259	POP_TOP           None
260	STORE_FAST        'exc'
263	POP_TOP           None

264	LOAD_CONST        None
267	IMPORT_NAME       'errno'
270	STORE_FAST        'errno'

273	LOAD_FAST         'exc'
276	LOAD_ATTR         'errno'
279	LOAD_FAST         'errno'
282	LOAD_ATTR         'EINTR'
285	COMPARE_OP        '=='
288	JUMP_IF_FALSE     '297'

291	CONTINUE          '218'
294	JUMP_FORWARD      '297'
297_0	COME_FROM         '294'

297	LOAD_GLOBAL       'DistutilsExecError'
300	LOAD_CONST        "command '%s' failed: %s"
303	LOAD_FAST         'cmd'
306	LOAD_CONST        0
309	BINARY_SUBSCR     None
310	LOAD_FAST         'exc'
313	LOAD_CONST        -1
316	BINARY_SUBSCR     None
317	BUILD_TUPLE_2     None
320	BINARY_MODULO     None
321	RAISE_VARARGS_2   None
324	JUMP_FORWARD      '328'
327	END_FINALLY       None
328_0	COME_FROM         '246'
328_1	COME_FROM         '327'

328	LOAD_GLOBAL       'os'
331	LOAD_ATTR         'WIFSIGNALED'
334	LOAD_FAST         'status'
337	CALL_FUNCTION_1   None
340	JUMP_IF_FALSE     '378'

343	LOAD_GLOBAL       'DistutilsExecError'
346	LOAD_CONST        "command '%s' terminated by signal %d"
349	LOAD_FAST         'cmd'
352	LOAD_CONST        0
355	BINARY_SUBSCR     None
356	LOAD_GLOBAL       'os'
359	LOAD_ATTR         'WTERMSIG'
362	LOAD_FAST         'status'
365	CALL_FUNCTION_1   None
368	BUILD_TUPLE_2     None
371	BINARY_MODULO     None
372	RAISE_VARARGS_2   None
375	JUMP_BACK         '218'

378	LOAD_GLOBAL       'os'
381	LOAD_ATTR         'WIFEXITED'
384	LOAD_FAST         'status'
387	CALL_FUNCTION_1   None
390	JUMP_IF_FALSE     '453'

393	LOAD_GLOBAL       'os'
396	LOAD_ATTR         'WEXITSTATUS'
399	LOAD_FAST         'status'
402	CALL_FUNCTION_1   None
405	STORE_FAST        'exit_status'

408	LOAD_FAST         'exit_status'
411	LOAD_CONST        0
414	COMPARE_OP        '=='
417	JUMP_IF_FALSE     '427'

420	LOAD_CONST        None
423	RETURN_VALUE      None
424	JUMP_ABSOLUTE     '497'

427	LOAD_GLOBAL       'DistutilsExecError'
430	LOAD_CONST        "command '%s' failed with exit status %d"
433	LOAD_FAST         'cmd'
436	LOAD_CONST        0
439	BINARY_SUBSCR     None
440	LOAD_FAST         'exit_status'
443	BUILD_TUPLE_2     None
446	BINARY_MODULO     None
447	RAISE_VARARGS_2   None
450	JUMP_BACK         '218'

453	LOAD_GLOBAL       'os'
456	LOAD_ATTR         'WIFSTOPPED'
459	LOAD_FAST         'status'
462	CALL_FUNCTION_1   None
465	JUMP_IF_FALSE     '474'

468	CONTINUE          '218'
471	JUMP_BACK         '218'

474	LOAD_GLOBAL       'DistutilsExecError'
477	LOAD_CONST        "unknown error executing '%s': termination status %d"
480	LOAD_FAST         'cmd'
483	LOAD_CONST        0
486	BINARY_SUBSCR     None
487	LOAD_FAST         'status'
490	BUILD_TUPLE_2     None
493	BINARY_MODULO     None
494	RAISE_VARARGS_2   None
497	JUMP_BACK         '218'
500	POP_BLOCK         None
501_0	COME_FROM         '212'
501_1	COME_FROM         '215'

Syntax error at or near `POP_BLOCK' token at offset 500


def find_executable(executable, path = None):
    if path is None:
        path = os.environ['PATH']
   
# Can't uncompyle C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\distutils\spawn.pyc
Traceback (most recent call last):
  File "C:\python27\lib\uncompyle2\__init__.py", line 206, in main
    uncompyle_file(infile, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 143, in uncompyle_file
    uncompyle(version, co, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 132, in uncompyle
    raise walk.ERROR
ParserError: --- This code section failed: ---

0	LOAD_GLOBAL       'log'
3	LOAD_ATTR         'info'
6	LOAD_GLOBAL       'string'
9	LOAD_ATTR         'join'
12	LOAD_FAST         'cmd'
15	LOAD_CONST        ' '
18	CALL_FUNCTION_2   None
21	CALL_FUNCTION_1   None
24	POP_TOP           None

25	LOAD_FAST         'dry_run'
28	JUMP_IF_FALSE     '38'

31	LOAD_CONST        None
34	RETURN_VALUE      None
35	JUMP_FORWARD      '38'
38_0	COME_FROM         '35'

38	LOAD_FAST         'search_path'
41	JUMP_IF_FALSE     '53'
44	LOAD_GLOBAL       'os'
47	LOAD_ATTR         'execvp'
50_0	COME_FROM         '41'
50	JUMP_IF_TRUE      '59'
53	LOAD_GLOBAL       'os'
56	LOAD_ATTR         'execv'
59	STORE_FAST        'exec_fn'

62	LOAD_GLOBAL       'os'
65	LOAD_ATTR         'fork'
68	CALL_FUNCTION_0   None
71	STORE_FAST        'pid'

74	LOAD_FAST         'pid'
77	LOAD_CONST        0
80	COMPARE_OP        '=='
83	JUMP_IF_FALSE     '215'

86	SETUP_EXCEPT      '110'

89	LOAD_FAST         'exec_fn'
92	LOAD_FAST         'cmd'
95	LOAD_CONST        0
98	BINARY_SUBSCR     None
99	LOAD_FAST         'cmd'
102	CALL_FUNCTION_2   None
105	POP_TOP           None
106	POP_BLOCK         None
107	JUMP_FORWARD      '175'
110_0	COME_FROM         '86'

110	DUP_TOP           None
111	LOAD_GLOBAL       'OSError'
114	COMPARE_OP        'exception match'
117	JUMP_IF_FALSE     '174'
120	POP_TOP           None
121	STORE_FAST        'e'
124	POP_TOP           None

125	LOAD_GLOBAL       'sys'
128	LOAD_ATTR         'stderr'
131	LOAD_ATTR         'write'
134	LOAD_CONST        'unable to execute %s: %s\n'
137	LOAD_FAST         'cmd'
140	LOAD_CONST        0
143	BINARY_SUBSCR     None
144	LOAD_FAST         'e'
147	LOAD_ATTR         'strerror'
150	BUILD_TUPLE_2     None
153	BINARY_MODULO     None
154	CALL_FUNCTION_1   None
157	POP_TOP           None

158	LOAD_GLOBAL       'os'
161	LOAD_ATTR         '_exit'
164	LOAD_CONST        1
167	CALL_FUNCTION_1   None
170	POP_TOP           None
171	JUMP_FORWARD      '175'
174	END_FINALLY       None
175_0	COME_FROM         '107'
175_1	COME_FROM         '174'

175	LOAD_GLOBAL       'sys'
178	LOAD_ATTR         'stderr'
181	LOAD_ATTR         'write'
184	LOAD_CONST        'unable to execute %s for unknown reasons'
187	LOAD_FAST         'cmd'
190	LOAD_CONST        0
193	BINARY_SUBSCR     None
194	BINARY_MODULO     None
195	CALL_FUNCTION_1   None
198	POP_TOP           None

199	LOAD_GLOBAL       'os'
202	LOAD_ATTR         '_exit'
205	LOAD_CONST        1
208	CALL_FUNCTION_1   None
211	POP_TOP           None
212	JUMP_FORWARD      '501'

215	SETUP_LOOP        '501'

218	SETUP_EXCEPT      '249'

221	LOAD_GLOBAL       'os'
224	LOAD_ATTR         'waitpid'
227	LOAD_FAST         'pid'
230	LOAD_CONST        0
233	CALL_FUNCTION_2   None
236	UNPACK_SEQUENCE_2 None
239	STORE_FAST        'pid'
242	STORE_FAST        'status'
245	POP_BLOCK         None
246	JUMP_FORWARD      '328'
249_0	COME_FROM         '218'

249	DUP_TOP           None
250	LOAD_GLOBAL       'OSError'
253	COMPARE_OP        'exception match'
256	JUMP_IF_FALSE     '327'
259	POP_TOP           None
260	STORE_FAST        'exc'
263	POP_TOP           None

264	LOAD_CONST        None
267	IMPORT_NAME       'errno'
270	STORE_FAST        'errno'

273	LOAD_FAST         'exc'
276	LOAD_ATTR         'errno'
279	LOAD_FAST         'errno'
282	LOAD_ATTR         'EINTR'
285	COMPARE_OP        '=='
288	JUMP_IF_FALSE     '297'

291	CONTINUE          '218'
294	JUMP_FORWARD      '297'
297_0	COME_FROM         '294'

297	LOAD_GLOBAL       'DistutilsExecError'
300	LOAD_CONST        "command '%s' failed: %s"
303	LOAD_FAST         'cmd'
306	LOAD paths = string.split(path, os.pathsep)
    base, ext = os.path.splitext(executable)
    if (sys.platform == 'win32' or os.name == 'os2') and ext != '.exe':
        executable = executable + '.exe'
    if not os.path.isfile(executable):
        for p in paths:
            f = os.path.join(p, executable)
            if os.path.isfile(f):
                return f

        return
    else:
        return executable
    return# decompiled 0 files: 0 okay, 1 failed, 0 verify failed
# 2013.08.22 22:14:57 Pacific Daylight Time
_CONST        0
309	BINARY_SUBSCR     None
310	LOAD_FAST         'exc'
313	LOAD_CONST        -1
316	BINARY_SUBSCR     None
317	BUILD_TUPLE_2     None
320	BINARY_MODULO     None
321	RAISE_VARARGS_2   None
324	JUMP_FORWARD      '328'
327	END_FINALLY       None
328_0	COME_FROM         '246'
328_1	COME_FROM         '327'

328	LOAD_GLOBAL       'os'
331	LOAD_ATTR         'WIFSIGNALED'
334	LOAD_FAST         'status'
337	CALL_FUNCTION_1   None
340	JUMP_IF_FALSE     '378'

343	LOAD_GLOBAL       'DistutilsExecError'
346	LOAD_CONST        "command '%s' terminated by signal %d"
349	LOAD_FAST         'cmd'
352	LOAD_CONST        0
355	BINARY_SUBSCR     None
356	LOAD_GLOBAL       'os'
359	LOAD_ATTR         'WTERMSIG'
362	LOAD_FAST         'status'
365	CALL_FUNCTION_1   None
368	BUILD_TUPLE_2     None
371	BINARY_MODULO     None
372	RAISE_VARARGS_2   None
375	JUMP_BACK         '218'

378	LOAD_GLOBAL       'os'
381	LOAD_ATTR         'WIFEXITED'
384	LOAD_FAST         'status'
387	CALL_FUNCTION_1   None
390	JUMP_IF_FALSE     '453'

393	LOAD_GLOBAL       'os'
396	LOAD_ATTR         'WEXITSTATUS'
399	LOAD_FAST         'status'
402	CALL_FUNCTION_1   None
405	STORE_FAST        'exit_status'

408	LOAD_FAST         'exit_status'
411	LOAD_CONST        0
414	COMPARE_OP        '=='
417	JUMP_IF_FALSE     '427'

420	LOAD_CONST        None
423	RETURN_VALUE      None
424	JUMP_ABSOLUTE     '497'

427	LOAD_GLOBAL       'DistutilsExecError'
430	LOAD_CONST        "command '%s' failed with exit status %d"
433	LOAD_FAST         'cmd'
436	LOAD_CONST        0
439	BINARY_SUBSCR     None
440	LOAD_FAST         'exit_status'
443	BUILD_TUPLE_2     None
446	BINARY_MODULO     None
447	RAISE_VARARGS_2   None
450	JUMP_BACK         '218'

453	LOAD_GLOBAL       'os'
456	LOAD_ATTR         'WIFSTOPPED'
459	LOAD_FAST         'status'
462	CALL_FUNCTION_1   None
465	JUMP_IF_FALSE     '474'

468	CONTINUE          '218'
471	JUMP_BACK         '218'

474	LOAD_GLOBAL       'DistutilsExecError'
477	LOAD_CONST        "unknown error executing '%s': termination status %d"
480	LOAD_FAST         'cmd'
483	LOAD_CONST        0
486	BINARY_SUBSCR     None
487	LOAD_FAST         'status'
490	BUILD_TUPLE_2     None
493	BINARY_MODULO     None
494	RAISE_VARARGS_2   None
497	JUMP_BACK         '218'
500	POP_BLOCK         None
501_0	COME_FROM         '212'
501_1	COME_FROM         '215'

Syntax error at or near `POP_BLOCK' token at offset 500

