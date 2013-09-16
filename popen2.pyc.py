# 2013.08.22 22:13:15 Pacific Daylight Time
# Embedded file name: popen2
import os
import sys
__all__ = ['popen2', 'popen3', 'popen4']
try:
    MAXFD = os.sysconf('SC_OPEN_MAX')
except (AttributeError, ValueError):
    MAXFD = 256

_active = []

def _cleanup():
    for inst in _active[:]:
        inst.poll()


class Popen3():
    __module__ = __name__
    sts = -1

    def __init__(self, cmd, capturestderr = False, bufsize = -1):
        _cleanup()
        p2cread, p2cwrite = os.pipe()
        c2pread, c2pwrite = os.pipe()
        if capturestderr:
            errout, errin = os.pipe()
        self.pid = os.fork()
        if self.pid == 0:
            os.dup2(p2cread, 0)
            os.dup2(c2pwrite, 1)
            if capturestderr:
                os.dup2(errin, 2)
            self._run_child(cmd)
        os.close(p2cread)
        self.tochild = os.fdopen(p2cwrite, 'w', bufsize)
        os.close(c2pwrite)
        self.fromchild = os.fdopen(c2pread, 'r', bufsize)
        if capturestderr:
            os.close(errin)
            self.childerr = os.fdopen(errout, 'r', bufsize)
        else:
            self.childerr = None
        _active.append(self)
        return

    def _run_child(self, cmd):
        if isinstance(cmd, basestring):
            cmd = ['/bin/sh', '-c', cmd]
        for i in range(3, MAXFD):
            try:
                os.close(i)
            except OSError:
                pass

        try:
            os.execvp(cmd[0], cmd)
        finally:
            os._exit(1)

    def poll(self):
        if self.sts < 0:
            try:
                pid, sts = os.waitpid(self.pid, os.WNOHANG)
                if pid == self.pid:
                    self.sts = sts
                    _active.remove(self)
            except os.error:
                pass

        return self.sts

    def wait(self):
        if self.sts < 0:
            pid, sts = os.waitpid(self.pid, 0)
            if pid == self.pid:
                self.sts = sts
                _active.remove(self)
        return self.sts


class Popen4(Popen3):
    __module__ = __name__
    childerr = None

    def __init__(self, cmd, bufsize = -1):
        _cleanup()
        p2cread, p2cwrite = os.pipe()
        c2pread, c2pwrite = os.pipe()
        self.pid = os.fork()
        if self.pid == 0:
            os.dup2(p2cread, 0)
            os.dup2(c2pwrite, 1)
            os.dup2(c2pwrite, 2)
            self._run_child(cmd)
        os.close(p2cread)
        self.tochild = os.fdopen(p2cwrite, 'w', bufsize)
        os.close(c2pwrite)
        self.fromchild = os.fdopen(c2pread, 'r', bufsize)
        _active.append(self)


if sys.platform[:3] == 'win' or sys.platform == 'os2emx':
    del Popen3
    del Popen4

    def popen2(cmd, bufsize = -1, mode = 't'):
        w, r = os.popen2(cmd, mode, bufsize)
        return (r, w)


    def popen3(cmd, bufsize = -1, mode = 't'):
        w, r, e = os.popen3(cmd, mode, bufsize)
        return (r, w, e)


    def popen4(cmd, bufsize = -1, mode = 't'):
        w, r = os.popen4(cmd, mode, bufsize)
        return (r, w)


else:

    def popen2(cmd, bufsize = -1, mode = 't'):
        inst = Popen3(cmd, False, bufsize)
        return (inst.fromchild, inst.tochild)


    def popen3(cmd, bufsize = -1, mode = 't'):
        inst = Popen3(cmd, True, bufsize)
        return (inst.fromchild, inst.tochild, inst.childerr)


    def popen4(cmd, bufsize = -1, mode = 't'):
        inst = Popen4(cmd, bufsize)
        return (inst.fromchild, inst.tochild)


    __all__.extend(['Popen3', 'Popen4'])

def _test():
    cmd = 'cat'
    teststr = 'ab cd\n'
    if os.name == 'nt':
        cmd = 'more'
    expected = teststr.strip()
    print 'testing popen2...'
    r, w = popen2(cmd)
    w.write(teststr)
    w.close()
    got = r.read()
    if got.strip() != expected:
        raise ValueError('wrote %r read %r' % (teststr, got))
    print 'testing popen3...'
    try:
        r, w, e = popen3([cmd])
    except:
        r, w, e = popen3(cmd)

    w.write(teststr)
    w.close()
    got = r.read()
    if got.strip() != expected:
        raise ValueError('wrote %r read %r' % (teststr, got))
    got = e.read()
    if got:
        raise ValueError('unexpected %r on stderr' % (got,))
    for inst in _active[:]:
        inst.wait()

    if _active:
        raise ValueError('_active not empty')
    print 'All OK'


if __name__ == '__main__':
    _test()
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\popen2.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:13:16 Pacific Daylight Time
