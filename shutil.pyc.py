# 2013.08.22 22:13:27 Pacific Daylight Time
# Embedded file name: shutil
import os
import sys
import stat
import exceptions
from os.path import abspath
__all__ = ['copyfileobj',
 'copyfile',
 'copymode',
 'copystat',
 'copy',
 'copy2',
 'copytree',
 'move',
 'rmtree',
 'Error']

class Error(exceptions.EnvironmentError):
    __module__ = __name__


def copyfileobj--- This code section failed: ---

0	SETUP_LOOP        '45'

3	LOAD_FAST         'fsrc'
6	LOAD_ATTR         'read'
9	LOAD_FAST         'length'
12	CALL_FUNCTION_1   None
15	STORE_FAST        'buf'

18	LOAD_FAST         'buf'
21	JUMP_IF_TRUE      '28'

24	BREAK_LOOP        None
25	JUMP_FORWARD      '28'
28_0	COME_FROM         '25'

28	LOAD_FAST         'fdst'
31	LOAD_ATTR         'write'
34	LOAD_FAST         'buf'
37	CALL_FUNCTION_1   None
40	POP_TOP           None
41	JUMP_BACK         '3'
44	POP_BLOCK         None
45_0	COME_FROM         '0'

Syntax error at or near `POP_BLOCK' token at offset 44


def _samefile(src, dst):
    if hasattr(os.path, 'samefile'):
        try:
            return os.path.samefile(src, dst)
        except OSError:
            return False

    return os.path.normcase(os.path.abspath(src)) == os.path.normcase(os.path.abspath(dst))


def copyfile(src, dst):
    if _samefile(src, dst):
        raise Error, '`%s` and `%s` are the same file' % (src, dst)
    fsrc = None
    fdst = None
    try:
        fsrc = open(src, 'rb')
        fdst = open(dst, 'wb')
        copyfileobj(fsrc, fdst)
    finally:
        if fdst:
            fdst.close()
        if fsrc:
            fsrc.close()

    return


def copymode(src, dst):
    if hasattr(os, 'chmod'):
        st = os.stat(src)
        mode = stat.S_IMODE(st.st_mode)
        os.chmod(dst, mode)


def copystat(src, dst):
    st = os.stat(src)
    mode = stat.S_IMODE(st.st_mode)
    if hasattr(os, 'utime'):
        os.utime(dst, (st.st_atime, st.st_mtime))
    if hasattr(os, 'chmod'):
        os.chmod(dst, mode)


def copy(src, dst):
    if os.path.isdir(dst):
        dst = os.path.join(dst, os.path.basename(src))
    copyfile(src, dst)
    copymode(src, dst)


def copy2(src, dst):
    if os.path.isdir(dst):
        dst = os.path.join(dst, os.path.basename(src))
    copyfile(src, dst)
    copystat(src, dst)


def copytree(src, dst, symlinks = False):
    names = os.listdir(src)
    os.mkdir(dst)
    errors = []
    for name in names:
        srcname = os.path.join(src, name)
        dstname = os.path.join(dst, name)
        try:
            if symlinks and os.path.islink(srcname):
                linkto = os.readlink(srcname)
                os.symlink(linkto, dstname)
            elif os.path.isdir(srcname):
                copytree(srcname, dstname, symlinks)
            else:
                copy2(srcname, dstname)
        except (IOError, os.error) as why:
            errors.append((srcname, dstname, why))

    if errors:
        raise Error, errors


def rmtree(path, ignore_errors = False, onerror = None):
    if ignore_errors:

        def onerror(*args):
            pass

    elif onerror is None:

        def onerror(*args):
            raise

    names = []
    try:
        names = os.listdir(path)
    except os.error as err:
        onerror(os.listdir, path, sys.exc_info())

    for name in names:
        fullname = os.path.join(path, name)
        try:
            mode = os.lstat(fullname).st_mode
        except os.error:
            mode = 0

        if stat.S_ISDIR(mode):
            rmtree(fullname, ignore_errors, onerror)
        else:
            try:
                os.remove(fullname)
            except os.error as err:
                onerror(os.remove, fullname, sys.exc_info())

    try:
        os.rmdir(path)
    except os.error:
        onerror(os.rmdir, path, sys.exc_info())

    return


def move(src, dst):
    try:
        os.rename(src, dst)
    except OSError:
        if os.path.isdir(src):
            if destinsrc(src, dst):
                raise Error, "Cannot move a directory '%s' into itself '%s'." % (src, dst)
            copytree(src, dst, symlinks=True)
            rmtree(src)
        else:
            copy2(src, dst)
            os.unlink(src)


def destinsrc(src, dst):
    return abspath(dst).startswith(abspath(src))# decompiled 0 files: 0 okay, 1 failed, 0 verify failed
# 2013.08.22 22:13:28 Pacific Daylight Time

# Can't uncompyle C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\shutil.pyc
Traceback (most recent call last):
  File "C:\python27\lib\uncompyle2\__init__.py", line 206, in main
    uncompyle_file(infile, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 143, in uncompyle_file
    uncompyle(version, co, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 132, in uncompyle
    raise walk.ERROR
ParserError: --- This code section failed: ---

0	SETUP_LOOP        '45'

3	LOAD_FAST         'fsrc'
6	LOAD_ATTR         'read'
9	LOAD_FAST         'length'
12	CALL_FUNCTION_1   None
15	STORE_FAST        'buf'

18	LOAD_FAST         'buf'
21	JUMP_IF_TRUE      '28'

24	BREAK_LOOP        None
25	JUMP_FORWARD      '28'
28_0	COME_FROM         '25'

28	LOAD_FAST         'fdst'
31	LOAD_ATTR         'write'
34	LOAD_FAST         'buf'
37	CALL_FUNCTION_1   None
40	POP_TOP           None
41	JUMP_BACK         '3'
44	POP_BLOCK         None
45_0	COME_FROM         '0'

Syntax error at or near `POP_BLOCK' token at offset 44

