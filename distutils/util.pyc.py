# 2013.08.22 22:14:57 Pacific Daylight Time
# Embedded file name: distutils.util
__revision__ = '$Id: util.py,v 1.1.1.1 2005/04/12 20:52:45 skyler Exp $'
import sys, os, string, re
from distutils.errors import DistutilsPlatformError
from distutils.dep_util import newer
from distutils.spawn import spawn
from distutils import log

def get_platform():
    if os.name != 'posix' or not hasattr(os, 'uname'):
        return sys.platform
    osname, host, release, version, machine = os.uname()
    osname = string.lower(osname)
    osname = string.replace(osname, '/', '')
    machine = string.replace(machine, ' ', '_')
    if osname[:5] == 'linux':
        return '%s-%s' % (osname, machine)
    elif osname[:5] == 'sunos':
        if release[0] >= '5':
            osname = 'solaris'
            release = '%d.%s' % (int(release[0]) - 3, release[2:])
    elif osname[:4] == 'irix':
        return '%s-%s' % (osname, release)
    elif osname[:3] == 'aix':
        return '%s-%s.%s' % (osname, version, release)
    elif osname[:6] == 'cygwin':
        osname = 'cygwin'
        rel_re = re.compile('[\\d.]+')
        m = rel_re.match(release)
        if m:
            release = m.group()
    return '%s-%s-%s' % (osname, release, machine)


def convert_path(pathname):
    if os.sep == '/':
        return pathname
    if not pathname:
        return pathname
    if pathname[0] == '/':
        raise ValueError, "path '%s' cannot be absolute" % pathname
    if pathname[-1] == '/':
        raise ValueError, "path '%s' cannot end with '/'" % pathname
    paths = string.split(pathname, '/')
    while '.' in paths:
        paths.remove('.')

    if not paths:
        return os.curdir
    return apply(os.path.join, paths)


def change_root(new_root, pathname):
    if os.name == 'posix':
        if not os.path.isabs(pathname):
            return os.path.join(new_root, pathname)
        else:
            return os.path.join(new_root, pathname[1:])
    elif os.name == 'nt':
        drive, path = os.path.splitdrive(pathname)
        if path[0] == '\\':
            path = path[1:]
        return os.path.join(new_root, path)
    elif os.name == 'os2':
        drive, path = os.path.splitdrive(pathname)
        if path[0] == os.sep:
            path = path[1:]
        return os.path.join(new_root, path)
    elif os.name == 'mac':
        if not os.path.isabs(pathname):
            return os.path.join(new_root, pathname)
        else:
            elements = string.split(pathname, ':', 1)
            pathname = ':' + elements[1]
            return os.path.join(new_root, pathname)
    else:
        raise DistutilsPlatformError, "nothing known about platform '%s'" % os.name


_environ_checked = 0

def check_environ():
    global _environ_checked
    if _environ_checked:
        return
    if os.name == 'posix' and not os.environ.has_key('HOME'):
        import pwd
        os.environ['HOME'] = pwd.getpwuid(os.getuid())[5]
    if not os.environ.has_key('PLAT'):
        os.environ['PLAT'] = get_platform()
    _environ_checked = 1


def subst_vars(s, local_vars):
    check_environ()

    def _subst(match, local_vars = local_vars):
        var_name = match.group(1)
        if local_vars.has_key(var_name):
            return str(local_vars[var_name])
        else:
            return os.environ[var_name]

    try:
        return re.sub('\\$([a-zA-Z_][a-zA-Z_0-9]*)', _subst, s)
    except KeyError as var:
        raise ValueError, "invalid variable '$%s'" % var


def grok_environment_error(exc, prefix = 'error: '):
    if hasattr(exc, 'filename') and hasattr(exc, 'strerror'):
        if exc.filename:
            error = prefix + '%s: %s' % (exc.filename, exc.strerror)
        else:
            error = prefix + '%s' % exc.strerror
    else:
        error = prefix + str(exc[-1])
    return error


_wordchars_re = _squote_re = _dquote_re = None

def _init_regex():
    global _dquote_re
    global _squote_re
    global _wordchars_re
    _wordchars_re = re.compile('[^\\\\\\\'\\"%s ]*' % string.whitespace)
    _squote_re = re.compile("'(?:[^'\\\\]|\\\\.)*'")
    _dquote_re = re.compile('"(?:[^"\\\\]|\\\\.)*"')


def split_quoted(s):
    if _wordchars_re is None:
        _init_regex()
    s = string.strip(s)
    words = []
    pos = 0
    while s:
        m = _wordchars_re.match(s, pos)
        end = m.end()
        if end == len(s):
            words.append(s[:end])
            break
        if s[end] in string.whitespace:
            words.append(s[:end])
            s = string.lstrip(s[end:])
            pos = 0
        elif s[end] == '\\':
            s = s[:end] + s[end + 1:]
            pos = end + 1
        else:
            if s[end] == "'":
                m = _squote_re.match(s, end)
            elif s[end] == '"':
                m = _dquote_re.match(s, end)
            else:
                raise RuntimeError, "this can't happen (bad char '%c')" % s[end]
            if m is None:
                raise ValueError, 'bad string (mismatched %s quotes?)' % s[end]
            beg, end = m.span()
            s = s[:beg] + s[beg + 1:end - 1] + s[end:]
            pos = m.end() - 2
        if pos >= len(s):
            words.append(s)
            break

    return words


def execute(func, args, msg = None, verbose = 0, dry_run = 0):
    if msg is None:
        msg = '%s%r' % (func.__name__, args)
        if msg[-2:] == ',)':
            msg = msg[0:-2] + ')'
    log.info(msg)
    if not dry_run:
        apply(func, args)
    return


def strtobool(val):
    val = string.lower(val)
    if val in ('y', 'yes', 't', 'true', 'on', '1'):
        return 1
    elif val in ('n', 'no', 'f', 'false', 'off', '0'):
        return 0
    else:
        raise ValueError, 'invalid truth value %r' % (val,)


def byte_compile(py_files, optimize = 0, force = 0, prefix = None, base_dir = None, verbose = 1, dry_run = 0, direct = None):
    if direct is None:
        if __debug__:
            direct = optimize == 0
        if not direct:
            try:
                from tempfile import mkstemp
                script_fd, script_name = mkstemp('.py')
            except ImportError:
                from tempfile import mktemp
                script_fd, script_name = None, mktemp('.py')

            log.info("writing byte-compilation script '%s'", script_name)
            if not dry_run:
                if script_fd is not None:
                    script = os.fdopen(script_fd, 'w')
                else:
                    script = open(script_name, 'w')
                script.write('from distutils.util import byte_compile\nfiles = [\n')
                script.write(string.join(map(repr, py_files), ',\n') + ']\n')
                script.write('\nbyte_compile(files, optimize=%r, force=%r,\n             prefix=%r, base_dir=%r,\n             verbose=%r, dry_run=0,\n             direct=1)\n' % (optimize,
                 force,
                 prefix,
                 base_dir,
                 verbose))
                script.close()
            cmd = [sys.executable, script_name]
            optimize == 1 and cmd.insert(1, '-O')
        elif optimize == 2:
            cmd.insert(1, '-OO')
        spawn(cmd, dry_run=dry_run)
        execute(os.remove, (script_name,), 'removing %s' % script_name, dry_run=dry_run)
    else:
        from py_compile import compile
        for file in py_files:
            if file[-3:] != '.py':
                continue
            cfile = file + (__debug__ and 'c' or 'o')
            dfile = file
            if prefix:
                if file[:len(prefix)] != prefix:
                    raise ValueError, "invalid prefix: filename %r doesn't start with %r" % (file, prefix)
                dfile = dfile[len(prefix):]
            if base_dir:
                dfile = os.path.join(base_dir, dfile)
            cfile_base = os.path.basename(cfile)
            if direct:
                if force or newer(file, cfile):
                    log.info('byte-compiling %s to %s', file, cfile_base)
                    if not dry_run:
                        compile(file, cfile, dfile)
                else:
                    log.debug('skipping byte-compilation of %s to %s', file, cfile_base)

    return


def rfc822_escape(header):
    lines = string.split(header, '\n')
    lines = map(string.strip, lines)
    header = string.join(lines, '\n' + 8 * ' ')
    return header
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\distutils\util.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:14:57 Pacific Daylight Time
