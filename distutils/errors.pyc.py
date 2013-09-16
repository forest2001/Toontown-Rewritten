# 2013.08.22 22:14:56 Pacific Daylight Time
# Embedded file name: distutils.errors
__revision__ = '$Id: errors.py,v 1.1.1.1 2005/04/12 20:52:45 skyler Exp $'

class DistutilsError(Exception):
    __module__ = __name__


class DistutilsModuleError(DistutilsError):
    __module__ = __name__


class DistutilsClassError(DistutilsError):
    __module__ = __name__


class DistutilsGetoptError(DistutilsError):
    __module__ = __name__


class DistutilsArgError(DistutilsError):
    __module__ = __name__


class DistutilsFileError(DistutilsError):
    __module__ = __name__


class DistutilsOptionError(DistutilsError):
    __module__ = __name__


class DistutilsSetupError(DistutilsError):
    __module__ = __name__


class DistutilsPlatformError(DistutilsError):
    __module__ = __name__


class DistutilsExecError(DistutilsError):
    __module__ = __name__


class DistutilsInternalError(DistutilsError):
    __module__ = __name__


class DistutilsTemplateError(DistutilsError):
    __module__ = __name__


class CCompilerError(Exception):
    __module__ = __name__


class PreprocessError(CCompilerError):
    __module__ = __name__


class CompileError(CCompilerError):
    __module__ = __name__


class LibError(CCompilerError):
    __module__ = __name__


class LinkError(CCompilerError):
    __module__ = __name__


class UnknownFileError(CCompilerError):
    __module__ = __name__
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\distutils\errors.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:14:56 Pacific Daylight Time
