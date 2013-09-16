# 2013.08.22 22:13:29 Pacific Daylight Time
# Embedded file name: SocketServer
__version__ = '0.4'
import socket
import sys
import os
__all__ = ['TCPServer',
 'UDPServer',
 'ForkingUDPServer',
 'ForkingTCPServer',
 'ThreadingUDPServer',
 'ThreadingTCPServer',
 'BaseRequestHandler',
 'StreamRequestHandler',
 'DatagramRequestHandler',
 'ThreadingMixIn',
 'ForkingMixIn']
if hasattr(socket, 'AF_UNIX'):
    __all__.extend(['UnixStreamServer',
     'UnixDatagramServer',
     'ThreadingUnixStreamServer',
     'ThreadingUnixDatagramServer'])

class BaseServer():
    __module__ = __name__

    def __init__(self, server_address, RequestHandlerClass):
        self.server_address = server_address
        self.RequestHandlerClass = RequestHandlerClass

    def server_activate(self):
        pass

    def serve_forever--- This code section failed: ---

0	SETUP_LOOP        '17'

3	LOAD_FAST         'self'
6	LOAD_ATTR         'handle_request'
9	CALL_FUNCTION_0   None
12	POP_TOP           None
13	JUMP_BACK         '3'
16	POP_BLOCK         None
17_0	COME_FROM         '0'

Syntax error at or near `POP_BLOCK' token at offset 16

    def handle_request(self):
        try:
            request, client_address = self.get_request()
        except socket.error:
            return

        if self.verify_request(request, client_address):
            try:
                self.process_request(request, client_address)
            except:
                self.handle_error(request, client_address)
                self.close_request(request)

    def verify_request(self, request, client_address):
        return True

    def process_request(self, request, client_address):
        self.finish_request(request, client_address)
        self.close_request(request)

    def server_close(self):
        pass

    def finish_request(self, request, client_address):
        self.RequestHandlerClass(request, client_address, self)

    def close_request(self, request):
        pass

    def handle_error(self, request, client_address):
        print '-' * 40
        print 'Exception happened during processing of request from',
        print client_address
        import traceback
        traceback.print_exc()
        print '-' * 40


class TCPServer(BaseServer):
    __module__ = __name__
    address_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM
    request_queue_size = 5
    allow_reuse_address = False

    def __init__(self, server_address, RequestHandlerClass):
        BaseServer.__init__(self, server_address, RequestHandlerClass)
        self.socket = socket.socket(self.address_family, self.socket_type)
        self.server_bind()
        self.server_activate()

    def server_bind(self):
        if self.allow_reuse_address:
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.server_address)

    def server_activate(self):
        self.socket.listen(self.request_queue_size)

    def server_close(self):
        self.socket.close()

    def fileno(self):
        return self.socket.fileno()

    def get_request(self):
        return self.socket.accept()

    def close_request(self, request):
        request.close()


class UDPServer(TCPServer):
    __module__ = __name__
    allow_reuse_address = False
    socket_type = socket.SOCK_DGRAM
    max_packet_size = 8192

    def get_request(self):
        data, client_addr = self.socket.recvfrom(self.max_packet_size)
        return ((data, self.socket), client_addr)

    def server_activate(self):
        pass

    def close_request(self, request):
        pass


class ForkingMixIn():
    __module__ = __name__
    active_children = None
    max_children = 40

    def collect_children(self):
        while self.active_children:
            if len(self.active_children) < self.max_children:
                options = os.WNOHANG
            else:
                options = 0
            try:
                pid, status = os.waitpid(0, options)
            except os.error:
                pid = None

            if not pid:
                break
            self.active_children.remove(pid)

        return

    def process_request(self, request, client_address):
        self.collect_children()
        pid = os.fork()
        if pid:
            if self.active_children is None:
                self.active_children = []
            self.active_children.append(pid)
            self.close_request(request)
            return
        else:
            try:
                self.finish_request(request, client_address)
                os._exit(0)
            except:
                try:
                    self.handle_error(request, client_address)
                finally:
                    os._exit(1)

        return


class ThreadingMixIn():
    __module__ = __name__
    daemon_threads = False

    def process_request_thread(self, request, client_address):
        try:
            self.finish_request(request, client_address)
            self.close_request(request)
        except:
            self.handle_error(request, client_address)
            self.close_request(request)

    def process_request(self, request, client_address):
        import threading
        t = threading.Thread(target=self.process_request_thread, args=(request, client_address))
        if self.daemon_threads:
            t.setDaemon(1)
        t.start()


class ForkingUDPServer(ForkingMixIn, UDPServer):
    __module__ = __name__


class ForkingTCPServer(ForkingMixIn, TCPServer):
    __module__ = __name__


class ThreadingUDPServer(ThreadingMixIn, UDPServer):
    __module__ = __name__


class ThreadingTCPServer(ThreadingMixIn, TCPServer):
    __module__ = __name__


if hasattr(socket, 'AF_UNIX'):

    class UnixStreamServer(TCPServer):
        __module__ = __name__
        address_family = socket.AF_UNIX


    class UnixDatagramServer(UDPServer):
        __module__ = __name__
        address_family = socket.AF_UNIX


    class ThreadingUnixStreamServer(ThreadingMixIn, UnixStreamServer):
        __module__ = __name__


    class ThreadingUnixDatagramServer(ThreadingMixIn, UnixDatagramServer):
        __module__ = __name__


class BaseRequestHandler():
    __module__ = __name__

    def __init__(self, request, client_address, server):
        self.request = request
        self.client_address = client_address
        self.server = server
        try:
            self.setup()
            self.handle()
            self.finish()
        finally:
            sys.exc_traceback = None

        return

    def setup(self):
        pass

    def handle(self):
        pass

    def finish(self):
        pass


class StreamRequestHandler(BaseRequestHandler):
    __module__ = __name__
    rbufsize = -1
    wbufsize = 0

    def setup(self):
        self.connection = self.request
        self.rfile = self.connection.makefile('rb', self.rbufsize)
        self.wfile = self.connection.makefile('wb', self.wbufsize)

    def finish(self):
        if not self.wfile.closed:
            self.wfile.flush()
        self.wfile.close()
        self.rfile.close()


class DatagramRequestHandler(BaseRequestHandler):
    __module__ = __name__

    def setup(self):
        import StringIO
        self.packet, self.socket = self.request
        self.rfile = StringIO.StringIO(self.packet)
        self.wfile = StringIO.StringIO()

    def finish(self):
        self.socket.sendto(self.wfile.getvalue(), self.client_address)# decompiled 0 files: 0 okay, 1 failed, 0 verify failed
# 2013.08.22 22:13:29 Pacific Daylight Time

# Can't uncompyle C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\SocketServer.pyc
Traceback (most recent call last):
  File "C:\python27\lib\uncompyle2\__init__.py", line 206, in main
    uncompyle_file(infile, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 143, in uncompyle_file
    uncompyle(version, co, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 132, in uncompyle
    raise walk.ERROR
ParserError: --- This code section failed: ---

0	SETUP_LOOP        '17'

3	LOAD_FAST         'self'
6	LOAD_ATTR         'handle_request'
9	CALL_FUNCTION_0   None
12	POP_TOP           None
13	JUMP_BACK         '3'
16	POP_BLOCK         None
17_0	COME_FROM         '0'

Syntax error at or near `POP_BLOCK' token at offset 16

