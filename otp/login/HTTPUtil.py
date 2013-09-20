# 2013.08.22 22:15:36 Pacific Daylight Time
# Embedded file name: otp.login.HTTPUtil
from pandac.PandaModules import *

class HTTPUtilException(Exception):
    __module__ = __name__

    def __init__(self, what):
        Exception.__init__(self, what)


class ConnectionError(HTTPUtilException):
    __module__ = __name__

    def __init__(self, what, statusCode):
        HTTPUtilException.__init__(self, what)
        self.statusCode = statusCode


class UnexpectedResponse(HTTPUtilException):
    __module__ = __name__

    def __init__(self, what):
        HTTPUtilException.__init__(self, what)


def getHTTPResponse(url, http, body = ''):
    if body:
        hd = http.postForm(url, body)
    else:
        hd = http.getDocument(url)
    if not hd.isValid():
        raise ConnectionError('Unable to reach %s' % url.cStr(), hd.getStatusCode())
    stream = hd.openReadBody()
    sr = StreamReader(stream, 1)
    response = sr.readlines()
    for i in xrange(len(response)):
        if response[i][-1] == '\n':
            response[i] = response[i][:-1]

    return response
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\otp\login\HTTPUtil.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:15:36 Pacific Daylight Time
