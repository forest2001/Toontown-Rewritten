# 2013.08.22 22:14:58 Pacific Daylight Time
# Embedded file name: email.Errors


class MessageError(Exception):
    __module__ = __name__


class MessageParseError(MessageError):
    __module__ = __name__


class HeaderParseError(MessageParseError):
    __module__ = __name__


class BoundaryError(MessageParseError):
    __module__ = __name__


class MultipartConversionError(MessageError, TypeError):
    __module__ = __name__


class MessageDefect():
    __module__ = __name__

    def __init__(self, line = None):
        self.line = line


class NoBoundaryInMultipartDefect(MessageDefect):
    __module__ = __name__


class StartBoundaryNotFoundDefect(MessageDefect):
    __module__ = __name__


class FirstHeaderLineIsContinuationDefect(MessageDefect):
    __module__ = __name__


class MisplacedEnvelopeHeaderDefect(MessageDefect):
    __module__ = __name__


class MalformedHeaderDefect(MessageDefect):
    __module__ = __name__


class MultipartInvariantViolationDefect(MessageDefect):
    __module__ = __name__
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\email\Errors.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:14:58 Pacific Daylight Time
