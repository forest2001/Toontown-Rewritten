# 2013.08.22 22:15:51 Pacific Daylight Time
# Embedded file name: pandac.extension_native_helpers
__all__ = ['Dtool_ObjectToDict', 'Dtool_funcToMethod', 'Dtool_PreloadDLL']
import imp, sys, os
dll_suffix = ''
if sys.platform == 'win32':
    dll_ext = '.dll'
    dll_suffix = getattr(sys, 'dll_suffix', None)
    if dll_suffix is None:
        dll_suffix = ''
        if sys.executable.endswith('_d.exe'):
            dll_suffix = '_d'
elif sys.platform == 'darwin':
    try:
        from direct.extensions_native.extensions_darwin import dll_ext
    except ImportError:
        dll_ext = '.dylib'

else:
    dll_ext = '.so'
if sys.platform == 'win32':
    target = None
    filename = 'libpandaexpress%s%s' % (dll_suffix, dll_ext)
    for dir in sys.path + [sys.prefix]:
        lib = os.path.join(dir, filename)
        if os.path.exists(lib):
            target = dir

    if target == None:
        message = 'Cannot find %s' % filename
        raise ImportError, message
    path = os.environ['PATH']
    if not path.startswith(target + ';'):
        os.environ['PATH'] = target + ';' + path

def Dtool_PreloadDLL(module):
    if module in sys.modules:
        return
    target = None
    filename = module + dll_suffix + dll_ext
    for dir in sys.path + [sys.prefix]:
        lib = os.path.join(dir, filename)
        if os.path.exists(lib):
            target = dir
            break

    if target == None:
        message = 'DLL loader cannot find %s.' % module
        raise ImportError, message
    pathname = os.path.join(target, filename)
    imp.load_dynamic(module, pathname)
    return


Dtool_PreloadDLL('libpandaexpress')
from libpandaexpress import *

def Dtool_ObjectToDict(clas, name, obj):
    clas.DtoolClassDict[name] = obj


def Dtool_funcToMethod(func, clas, method_name = None):
    func.im_class = clas
    func.im_func = func
    func.im_self = None
    if not method_name:
        method_name = func.__name__
    clas.DtoolClassDict[method_name] = func
    return
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\pandac\extension_native_helpers.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:15:52 Pacific Daylight Time
