# 2013.08.22 22:13:36 Pacific Daylight Time
# Embedded file name: types
import sys
NoneType = type(None)
TypeType = type
ObjectType = object
IntType = int
LongType = long
FloatType = float
BooleanType = bool
try:
    ComplexType = complex
except NameError:
    pass

StringType = str
try:
    UnicodeType = unicode
    StringTypes = (StringType, UnicodeType)
except NameError:
    StringTypes = (StringType,)

BufferType = buffer
TupleType = tuple
ListType = list
DictType = DictionaryType = dict

def _f():
    pass


FunctionType = type(_f)
LambdaType = type(lambda : None)
try:
    CodeType = type(_f.func_code)
except RuntimeError:
    pass

def _g--- This code section failed: ---

0	LOAD_CONST        1
3	YIELD_VALUE       None

Syntax error at or near `LOAD_CONST' token at offset 0


GeneratorType = type(_g())

class _C():
    __module__ = __name__

    def _m(self):
        pass


ClassType = type(_C)
UnboundMethodType = type(_C._m)
_x = _C()
InstanceType = type(_x)
MethodType = type(_x._m)
BuiltinFunctionType = type(len)
BuiltinMethodType = type([].append)
ModuleType = type(sys)
FileType = file
XRangeType = xrange
try:
    raise TypeError
except TypeError:
    try:
        tb = sys.exc_info()[2]
        TracebackType = type(tb)
        FrameType = type(tb.tb_frame)
    except AttributeError:
        pass

    tb = None
    del tb

SliceType = slice
EllipsisType = type(Ellipsis)
DictProxyType = type(TypeType.__dict__)
NotImplementedType = type(NotImplemented)
del sys
del _f
del _g
del _C
del _x# decompiled 0 files: 0 okay, 1 failed, 0 verify failed
# 2013.08.22 22:13:36 Pacific Daylight Time

# Can't uncompyle C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\types.pyc
Traceback (most recent call last):
  File "C:\python27\lib\uncompyle2\__init__.py", line 206, in main
    uncompyle_file(infile, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 143, in uncompyle_file
    uncompyle(version, co, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 132, in uncompyle
    raise walk.ERROR
ParserError: --- This code section failed: ---

0	LOAD_CONST        1
3	YIELD_VALUE       None

Syntax error at or near `LOAD_CONST' token at offset 0

