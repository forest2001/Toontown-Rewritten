# 2013.08.22 22:13:28 Pacific Daylight Time
# Embedded file name: socket
import _socket
from _socket import *
_have_ssl = False
try:
    import _ssl
    from _ssl import *
    _have_ssl = True
except ImportError:
    pass

import os, sys
try:
    from errno import EBADF
except ImportError:
    EBADF = 9

__all__ = ['getfqdn']
__all__.extend(os._get_exports_list(_socket))
if _have_ssl:
    __all__.extend(os._get_exports_list(_ssl))
_realsocket = socket
if _have_ssl:
    _realssl = ssl

    def ssl(sock, keyfile = None, certfile = None):
        if hasattr(sock, '_sock'):
            sock = sock._sock
        return _realssl(sock, keyfile, certfile)


if sys.platform.lower().startswith('win'):
    errorTab = {}
    errorTab[10004] = 'The operation was interrupted.'
    errorTab[10009] = 'A bad file handle was passed.'
    errorTab[10013] = 'Permission denied.'
    errorTab[10014] = 'A fault occurred on the network??'
    errorTab[10022] = 'An invalid operation was attempted.'
    errorTab[10035] = 'The socket operation would block'
    errorTab[10036] = 'A blocking operation is already in progress.'
    errorTab[10048] = 'The network address is in use.'
    errorTab[10054] = 'The connection has been reset.'
    errorTab[10058] = 'The network has been shut down.'
    errorTab[10060] = 'The operation timed out.'
    errorTab[10061] = 'Connection refused.'
    errorTab[10063] = 'The name is too long.'
    errorTab[10064] = 'The host is down.'
    errorTab[10065] = 'The host is unreachable.'
    __all__.append('errorTab')

def getfqdn(name = ''):
    name = name.strip()
    if not name or name == '0.0.0.0':
        name = gethostname()
    try:
        hostname, aliases, ipaddrs = gethostbyaddr(name)
    except error:
        pass
    else:
        aliases.insert(0, hostname)
        for name in aliases:
            if '.' in name:
                break
        else:
            name = hostname

    return name


_socketmethods = ('bind', 'connect', 'connect_ex', 'fileno', 'listen', 'getpeername', 'getsockname', 'getsockopt', 'setsockopt', 'sendall', 'setblocking', 'settimeout', 'gettimeout', 'shutdown')
if sys.platform == 'riscos':
    _socketmethods = _socketmethods + ('sleeptaskw',)

class _closedsocket(object):
    __module__ = __name__
    __slots__ = []

    def _dummy(*args):
        raise error(EBADF, 'Bad file descriptor')

    send = recv = sendto = recvfrom = __getattr__ = _dummy


class _socketobject(object):
    __module__ = __name__
    __doc__ = _realsocket.__doc__
    __slots__ = ['_sock',
     'send',
     'recv',
     'sendto',
     'recvfrom',
     '__weakref__']

    def __init__(self, family = AF_INET, type = SOCK_STREAM, proto = 0, _sock = None):
        if _sock is None:
            _sock = _realsocket(family, type, proto)
        self._sock = _sock
        self.send = self._sock.send
        self.recv = self._sock.recv
        self.sendto = self._sock.sendto
        self.recvfrom = self._sock.recvfrom
        return

    def close(self):
        self._sock = _closedsocket()
        self.send = self.recv = self.sendto = self.recvfrom = self._sock._dummy

    close.__doc__ = _realsocket.close.__doc__

    def accept(self):
        sock, addr = self._sock.accept()
        return (_socketobject(_sock=sock), addr)

    accept.__doc__ = _realsocket.accept.__doc__

    def dup(self):
        return _socketobject(_sock=self._sock)

    def makefile(self, mode = 'r', bufsize = -1):
        return _fileobject(self._sock, mode, bufsize)

    _s = 'def %s(self, *args): return self._sock.%s(*args)\n\n%s.__doc__ = _realsocket.%s.__doc__\n'
    for _m in _socketmethods:
        exec _s % (_m,
         _m,
         _m,
         _m)

    del _m
    del _s


socket = SocketType = _socketobject

class _fileobject(object):
    __module__ = __name__
    default_bufsize = 8192
    name = '<socket>'
    __slots__ = ['mode',
     'bufsize',
     'softspace',
     '_sock',
     '_rbufsize',
     '_wbufsize',
     '_rbuf',
     '_wbuf']

    def __init__(self, sock, mode = 'rb', bufsize = -1):
        self._sock = sock
        self.mode = mode
        if bufsize < 0:
            bufsize = self.default_bufsize
        self.bufsize = bufsize
        self.softspace = False
        if bufsize == 0:
            self._rbufsize = 1
        elif bufsize == 1:
            self._rbufsize = self.default_bufsize
        else:
            self._rbufsize = bufsize
        self._wbufsize = bufsize
        self._rbuf = ''
        self._wbuf = []

    def _getclosed(self):
        return self._sock is None

    closed = property(_getclosed, doc='True if the file is closed')

    def close(self):
        try:
            if self._sock:
                self.flush()
        finally:
            self._sock = None

        return

    def __del__(self):
        try:
            self.close()
        except:
            pass

    def flush(self):
        if self._wbuf:
            buffer = ''.join(self._wbuf)
            self._wbuf = []
            self._sock.sendall(buffer)

    def fileno(self):
        return self._sock.fileno()

    def write(self, data):
        data = str(data)
        if not data:
            return
        self._wbuf.append(data)
        if self._wbufsize == 0 or self._wbufsize == 1 and '\n' in data or self._get_wbuf_len() >= self._wbufsize:
            self.flush()

    def writelines(self, list):
        self._wbuf.extend(filter(None, map(str, list)))
        if self._wbufsize <= 1 or self._get_wbuf_len() >= self._wbufsize:
            self.flush()
        return

    def _get_wbuf_len(self):
        buf_len = 0
        for x in self._wbuf:
            buf_len += len(x)

        return buf_len

    def read(self, size = -1):
        data = self._rbuf
        if size < 0:
            buffers = []
            if data:
                buffers.append(data)
            self._rbuf = ''
            if self._rbufsize <= 1:
                recv_size = self.default_bufsize
            else:
                recv_size = self._rbufsize
            while True:
                data = self._sock.recv(recv_size)
                if not data:
                    break
                buffers.append(data)

            return ''.join(buffers)
        else:
            buf_len = len(data)
            if buf_len >= size:
                self._rbuf = data[size:]
                return data[:size]
            buffers = []
            if data:
                buffers.append(data)
            self._rbuf = ''
            while True:
                left = size - buf_len
                recv_size = max(self._rbufsize, left)
                data = self._sock.recv(recv_size)
                if not data:
                    break
                buffers.append(data)
                n = len(data)
                if n >= left:
                    self._rbuf = data[left:]
                    buffers[-1] = data[:left]
                    break
                buf_len += n

            return ''.join(buffers)

    def readline(self, size = -1):
        data = self._rbuf
        if size < 0:
            if self._rbufsize <= 1:
                buffers = []
                recv = self._sock.recv
                while data != '\n':
                    data = recv(1)
                    if not data:
                        break
                    buffers.append(data)

                return ''.join(buffers)
            nl = data.find('\n')
            if nl >= 0:
                nl += 1
                self._rbuf = data[nl:]
                return data[:nl]
            buffers = []
            if data:
                buffers.append(data)
            self._rbuf = ''
            while True:
                data = self._sock.recv(self._rbufsize)
                if not data:
                    break
                buffers.append(data)
                nl = data.find('\n')
                if nl >= 0:
                    nl += 1
                    self._rbuf = data[nl:]
                    buffers[-1] = data[:nl]
                    break

            return ''.join(buffers)
        else:
            nl = data.find('\n', 0, size)
            if nl >= 0:
                nl += 1
                self._rbuf = data[nl:]
                return data[:nl]
            buf_len = len(data)
            if buf_len >= size:
                self._rbuf = data[size:]
                return data[:size]
            buffers = []
            if data:
                buffers.append(data)
            self._rbuf = ''
            while True:
                data = self._sock.recv(self._rbufsize)
                if not data:
                    break
                buffers.append(data)
                left = size - buf_len
                nl = data.find('\n', 0, left)
                if nl >= 0:
                    nl += 1
                    self._rbuf = data[nl:]
                    buffers[-1] = data[:nl]
                    break
                n = len(data)
                if n >= left:
                    self._rbuf = data[left:]
                    buffers[-1] = data[:left]
                    break
                buf_len += n

            return ''.join(buffers)

    def readlines(self, sizehint = 0):
        total = 0
        list = []
        while True:
            line = self.readline()
            if not line:
                break
            list.append(line)
            total += len(line)
            if sizehint and total >= sizehint:
                break

        return list

    def __iter__(self):
        return self

    def next(self):
        line = self.readline()
        if not line:
            raise StopIteration
        return line
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\socket.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:13:29 Pacific Daylight Time
