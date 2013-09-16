# 2013.08.22 22:14:40 Pacific Daylight Time
# Embedded file name: direct.showbase.PythonUtil
__all__ = ['enumerate',
 'unique',
 'indent',
 'nonRepeatingRandomList',
 'writeFsmTree',
 'StackTrace',
 'traceFunctionCall',
 'traceParentCall',
 'printThisCall',
 'tron',
 'trace',
 'troff',
 'getClassLineage',
 'pdir',
 '_pdir',
 '_is_variadic',
 '_has_keywordargs',
 '_varnames',
 '_getcode',
 'Signature',
 'doc',
 'adjust',
 'difference',
 'intersection',
 'union',
 'sameElements',
 'makeList',
 'makeTuple',
 'list2dict',
 'invertDict',
 'invertDictLossless',
 'uniqueElements',
 'disjoint',
 'contains',
 'replace',
 'reduceAngle',
 'fitSrcAngle2Dest',
 'fitDestAngle2Src',
 'closestDestAngle2',
 'closestDestAngle',
 'binaryRepr',
 'profileFunc',
 'profiled',
 'startProfile',
 'printProfile',
 'getSetterName',
 'getSetter',
 'Functor',
 'Stack',
 'Queue',
 'ParamObj',
 'POD',
 'bound',
 'clamp',
 'lerp',
 'clerp',
 'triglerp',
 'average',
 'addListsByValue',
 'boolEqual',
 'lineupPos',
 'formatElapsedSeconds',
 'solveQuadratic',
 'stackEntryInfo',
 'lineInfo',
 'callerInfo',
 'lineTag',
 'findPythonModule',
 'describeException',
 'mostDerivedLast',
 'clampScalar',
 'weightedChoice',
 'randFloat',
 'normalDistrib',
 'weightedRand',
 'randUint31',
 'randInt32',
 'randUint32',
 'SerialNumGen',
 'serialNum',
 'uniqueName',
 'Enum',
 'Singleton',
 'SingletonError',
 'printListEnum',
 'safeRepr',
 'fastRepr',
 'tagRepr',
 'tagWithCaller',
 'isDefaultValue',
 'set_trace',
 'pm',
 'ScratchPad',
 'Sync',
 'RefCounter',
 'itype',
 'getNumberedTypedString',
 'getNumberedTypedSortedString',
 'getNumberedTypedSortedStringWithReferrers',
 'getNumberedTypedSortedStringWithReferrersGen',
 'printNumberedTyped',
 'DelayedCall',
 'DelayedFunctor',
 'FrameDelayedCall',
 'SubframeCall',
 'ArgumentEater',
 'ClassTree',
 'getBase',
 'HotkeyBreaker',
 'logMethodCalls',
 'GoldenRatio',
 'GoldenRectangle',
 'pivotScalar',
 'rad90',
 'rad180',
 'rad270',
 'rad360',
 'nullGen',
 'loopGen',
 'makeFlywheelGen',
 'flywheel',
 'choice',
 'printStack',
 'printReverseStack',
 'listToIndex2item',
 'listToItem2index',
 'pandaBreak',
 'pandaTrace',
 'formatTimeCompact',
 'DestructiveScratchPad',
 'deeptype',
 'getProfileResultString',
 'StdoutCapture',
 'StdoutPassthrough',
 'Averager',
 'getRepository',
 'formatTimeExact',
 'startSuperLog',
 'endSuperLog',
 'typeName',
 'safeTypeName',
 'histogramDict',
 'unescapeHtmlString',
 'bpdb']
import types
import string
import re
import math
import operator
import inspect
import os
import sys
import random
import time
import new
import gc
import bisect
import traceback
import __builtin__
from StringIO import StringIO
import marshal
import ElementTree as ET
from HTMLParser import HTMLParser
import BpDb
import unicodedata
__report_indent = 3
from direct.directutil import Verify
import direct.extensions_native.extension_native_helpers
from libpandaexpress import ConfigVariableBool
ScalarTypes = (types.FloatType, types.IntType, types.LongType)
import __builtin__
if not hasattr(__builtin__, 'enumerate'):

    def enumerate(L):
        return zip(xrange(len(L)), L)


    __builtin__.enumerate = enumerate
else:
    enumerate = __builtin__.enumerate

class Functor():
    __module__ = __name__

    def __init__(self, function, *args, **kargs):
        self._function = function
        self._args = args
        self._kargs = kargs
        if hasattr(self._function, '__name__'):
            self.__name__ = self._function.__name__
        else:
            self.__name__ = str(itype(self._function))
        if hasattr(self._function, '__doc__'):
            self.__doc__ = self._function.__doc__
        else:
            self.__doc__ = self.__name__

    def destroy(self):
        del self._function
        del self._args
        del self._kargs
        del self.__name__
        del self.__doc__

    def _do__call__(self, *args, **kargs):
        _kargs = self._kargs.copy()
        _kargs.update(kargs)
        return self._function(*(self._args + args), **_kargs)

    def _exceptionLoggedCreationStack__call__(self, *args, **kargs):
        try:
            return self._do__call__(*args, **kargs)
        except Exception as e:
            print '-->Functor creation stack (%s): %s' % (self.__name__, self.getCreationStackTraceCompactStr())
            raise

    __call__ = _do__call__

    def __repr__(self):
        s = 'Functor(%s' % self._function.__name__
        for arg in self._args:
            try:
                argStr = repr(arg)
            except:
                argStr = 'bad repr: %s' % arg.__class__

            s += ', %s' % argStr

        for karg, value in self._kargs.items():
            s += ', %s=%s' % (karg, repr(value))

        s += ')'
        return s


class Stack():
    __module__ = __name__

    def __init__(self):
        self.__list = []

    def push(self, item):
        self.__list.append(item)

    def top(self):
        return self.__list[-1]

    def pop(self):
        return self.__list.pop()

    def clear(self):
        self.__list = []

    def isEmpty(self):
        return len(self.__list) == 0

    def __len__(self):
        return len(self.__list)


class Queue():
    __module__ = __name__

    def __init__(self):
        self.__list = []

    def push(self, item):
        self.__list.append(item)

    def top(self):
        return self.__list[0]

    def front(self):
        return self.__list[0]

    def back(self):
        return self.__list[-1]

    def pop(self):
        return self.__list.pop(0)

    def clear(self):
        self.__list = []

    def isEmpty(self):
        return len(self.__list) == 0

    def __len__(self):
        return len(self.__list)


def unique(L1, L2):
    L2 = dict([ (k, None) for k in L2 ])
    return [ item for item in L1 if item not in L2 ]


def indent(stream, numIndents, str):
    stream.write('    ' * numIndents + str)


def nonRepeatingRandomList(vals, max):
    random.seed(time.time())
    valueList = range(max)
    finalVals = []
    for i in range(vals):
        index = int(random.random() * len(valueList))
        finalVals.append(valueList[index])
        valueList.remove(valueList[index])

    return finalVals


def writeFsmTree(instance, indent = 0):
    if hasattr(instance, 'parentFSM'):
        writeFsmTree(instance.parentFSM, indent - 2)
    elif hasattr(instance, 'fsm'):
        name = ''
        if hasattr(instance.fsm, 'state'):
            name = instance.fsm.state.name
        print '%s: %s' % (instance.fsm.name, name)


class StackTrace():
    __module__ = __name__

    def __init__(self, label = '', start = 0, limit = None):
        self.label = label
        if limit is not None:
            self.trace = traceback.extract_stack(sys._getframe(1 + start), limit=limit)
        else:
            self.trace = traceback.extract_stack(sys._getframe(1 + start))
        return

    def compact(self):
        r = ''
        comma = ','
        for filename, lineNum, funcName, text in self.trace:
            r += '%s.%s:%s%s' % (filename[:filename.rfind('.py')][filename.rfind('\\') + 1:],
             funcName,
             lineNum,
             comma)

        if len(r):
            r = r[:-len(comma)]
        return r

    def reverseCompact(self):
        r = ''
        comma = ','
        for filename, lineNum, funcName, text in self.trace:
            r = '%s.%s:%s%s%s' % (filename[:filename.rfind('.py')][filename.rfind('\\') + 1:],
             funcName,
             lineNum,
             comma,
             r)

        if len(r):
            r = r[:-len(comma)]
        return r

    def __str__(self):
        r = 'Debug stack trace of %s (back %s frames):\n' % (self.label, len(self.trace))
        for i in traceback.format_list(self.trace):
            r += i

        r += '***** NOTE: This is not a crash. This is a debug stack trace. *****'
        return r


def printStack():
    print StackTrace(start=1).compact()
    return True


def printReverseStack():
    print StackTrace(start=1).reverseCompact()
    return True


def printVerboseStack():
    print StackTrace(start=1)
    return True


def traceFunctionCall(frame):
    f = frame
    co = f.f_code
    dict = f.f_locals
    n = co.co_argcount
    if co.co_flags & 4:
        n = n + 1
    if co.co_flags & 8:
        n = n + 1
    r = ''
    if 'self' in dict:
        r = '%s.' % (dict['self'].__class__.__name__,)
    r += '%s(' % (f.f_code.co_name,)
    comma = 0
    for i in range(n):
        name = co.co_varnames[i]
        if name == 'self':
            continue
        if comma:
            r += ', '
        else:
            comma = 1
        r += name
        r += '='
        if name in dict:
            v = safeRepr(dict[name])
            if len(v) > 2000:
                r += v[:2000] + '...'
            else:
                r += v
        else:
            r += '*** undefined ***'

    return r + ')'


def traceParentCall():
    return traceFunctionCall(sys._getframe(2))


def printThisCall():
    print traceFunctionCall(sys._getframe(1))
    return 1


def tron():
    sys.settrace(trace)


def trace(frame, event, arg):
    if event == 'line':
        pass
    elif event == 'call':
        print traceFunctionCall(sys._getframe(1))
    elif event == 'return':
        print 'returning'
    elif event == 'exception':
        print 'exception'
    return trace


def troff():
    sys.settrace(None)
    return


def getClassLineage(obj):
    if type(obj) == types.DictionaryType:
        return [obj]
    elif type(obj) == types.InstanceType:
        return [obj] + getClassLineage(obj.__class__)
    elif type(obj) == types.ClassType or type(obj) == types.TypeType:
        lineage = [obj]
        for c in obj.__bases__:
            lineage = lineage + getClassLineage(c)

        return lineage
    elif hasattr(obj, '__class__'):
        return [obj] + getClassLineage(obj.__class__)
    else:
        return []


def pdir(obj, str = None, width = None, fTruncate = 1, lineWidth = 75, wantPrivate = 0):
    uniqueLineage = []
    for l in getClassLineage(obj):
        if type(l) == types.ClassType:
            if l in uniqueLineage:
                break
        uniqueLineage.append(l)

    uniqueLineage.reverse()
    for obj in uniqueLineage:
        _pdir(obj, str, width, fTruncate, lineWidth, wantPrivate)
        print


def _pdir(obj, str = None, width = None, fTruncate = 1, lineWidth = 75, wantPrivate = 0):

    def printHeader(name):
        name = ' ' + name + ' '
        length = len(name)
        if length < 70:
            padBefore = int((70 - length) / 2.0)
            padAfter = max(0, 70 - length - padBefore)
            header = '*' * padBefore + name + '*' * padAfter
        print header
        print

    def printInstanceHeader(i, printHeader = printHeader):
        printHeader(i.__class__.__name__ + ' INSTANCE INFO')

    def printClassHeader(c, printHeader = printHeader):
        printHeader(c.__name__ + ' CLASS INFO')

    def printDictionaryHeader(d, printHeader = printHeader):
        printHeader('DICTIONARY INFO')

    if type(obj) == types.InstanceType:
        printInstanceHeader(obj)
    elif type(obj) == types.ClassType:
        printClassHeader(obj)
    elif type(obj) == types.DictionaryType:
        printDictionaryHeader(obj)
    if type(obj) == types.DictionaryType:
        dict = obj
    elif not hasattr(obj, '__dict__'):
        dict = {}
    else:
        dict = obj.__dict__
    if width:
        maxWidth = width
    else:
        maxWidth = 10
    keyWidth = 0
    aproposKeys = []
    privateKeys = []
    remainingKeys = []
    for key in dict.keys():
        if not width:
            keyWidth = len(key)
        if str:
            if re.search(str, key, re.I):
                aproposKeys.append(key)
                if not width and keyWidth > maxWidth:
                    maxWidth = keyWidth
        elif key[:1] == '_':
            if wantPrivate:
                privateKeys.append(key)
                if not width and keyWidth > maxWidth:
                    maxWidth = keyWidth
        else:
            remainingKeys.append(key)
            if not width and keyWidth > maxWidth:
                maxWidth = keyWidth

    if str:
        aproposKeys.sort()
    else:
        privateKeys.sort()
        remainingKeys.sort()
    if wantPrivate:
        keys = aproposKeys + privateKeys + remainingKeys
    else:
        keys = aproposKeys + remainingKeys
    format = '%-' + repr(maxWidth) + 's'
    for key in keys:
        value = dict[key]
        if callable(value):
            strvalue = repr(Signature(value))
        else:
            strvalue = repr(value)
        if fTruncate:
            strvalue = strvalue[:max(1, lineWidth - maxWidth)]
        print (format % key)[:maxWidth] + '\t' + strvalue


_POS_LIST = 4
_KEY_DICT = 8

def _is_variadic(function):
    return function.func_code.co_flags & _POS_LIST


def _has_keywordargs(function):
    return function.func_code.co_flags & _KEY_DICT


def _varnames(function):
    return function.func_code.co_varnames


def _getcode(f):

    def method_get(f):
        return (f.__name__, f.im_func)

    def function_get(f):
        return (f.__name__, f)

    def instance_get(f):
        if hasattr(f, '__call__'):
            method = f.__call__
            if type(method) == types.MethodType:
                func = method.im_func
            else:
                func = method
            return ('%s%s' % (f.__class__.__name__, '__call__'), func)
        else:
            s = 'Instance %s of class %s does not have a __call__ method' % (f, f.__class__.__name__)
            raise TypeError, s

    def class_get(f):
        if hasattr(f, '__init__'):
            return (f.__name__, f.__init__.im_func)
        else:
            return (f.__name__, lambda : None)

    codedict = {types.UnboundMethodType: method_get,
     types.MethodType: method_get,
     types.FunctionType: function_get,
     types.InstanceType: instance_get,
     types.ClassType: class_get}
    try:
        return codedict[type(f)](f)
    except KeyError:
        if hasattr(f, '__call__'):
            return (f.__name__, None)
        else:
            raise TypeError, 'object %s of type %s is not callable.' % (f, type(f))

    return None


class Signature():
    __module__ = __name__

    def __init__(self, func):
        self.type = type(func)
        self.name, self.func = _getcode(func)

    def ordinary_args(self):
        n = self.func.func_code.co_argcount
        return _varnames(self.func)[0:n]

    def special_args(self):
        n = self.func.func_code.co_argcount
        x = {}
        if _is_variadic(self.func):
            x['positional'] = _varnames(self.func)[n]
            if _has_keywordargs(self.func):
                x['keyword'] = _varnames(self.func)[n + 1]
        elif _has_keywordargs(self.func):
            x['keyword'] = _varnames(self.func)[n]
        return x

    def full_arglist(self):
        base = list(self.ordinary_args())
        x = self.special_args()
        if 'positional' in x:
            base.append(x['positional'])
        if 'keyword' in x:
            base.append(x['keyword'])
        return base

    def defaults(self):
        defargs = self.func.func_defaults
        args = self.ordinary_args()
        mapping = {}
        if defargs is not None:
            for i in range(-1, -(len(defargs) + 1), -1):
                mapping[args[i]] = defargs[i]

        return mapping

    def __repr__(self):
        if self.func:
            defaults = self.defaults()
            specials = self.special_args()
            l = []
            for arg in self.ordinary_args():
                if arg in defaults:
                    l.append(arg + '=' + str(defaults[arg]))
                else:
                    l.append(arg)

            if 'positional' in specials:
                l.append('*' + specials['positional'])
            if 'keyword' in specials:
                l.append('**' + specials['keyword'])
            return '%s(%s)' % (self.name, string.join(l, ', '))
        else:
            return '%s(?)' % self.name


def doc(obj):
    if isinstance(obj, types.MethodType) or isinstance(obj, types.FunctionType):
        print obj.__doc__


def adjust(command = None, dim = 1, parent = None, **kw):
    from direct.tkwidgets import Valuator
    if command:
        kw['command'] = lambda x: apply(command, x)
        if parent is None:
            kw['title'] = command.__name__
    kw['dim'] = dim
    if not parent:
        vg = apply(Valuator.ValuatorGroupPanel, (parent,), kw)
    else:
        vg = apply(Valuator.ValuatorGroup, (parent,), kw)
        vg.pack(expand=1, fill='x')
    return vg


def difference(a, b):
    if not a:
        return b
    if not b:
        return a
    d = []
    for i in a:
        if i not in b and i not in d:
            d.append(i)

    for i in b:
        if i not in a and i not in d:
            d.append(i)

    return d


def intersection(a, b):
    if not a:
        return []
    if not b:
        return []
    d = []
    for i in a:
        if i in b and i not in d:
            d.append(i)

    for i in b:
        if i in a and i not in d:
            d.append(i)

    return d


def union(a, b):
    c = a[:]
    for i in b:
        if i not in c:
            c.append(i)

    return c


def sameElements(a, b):
    if len(a) != len(b):
        return 0
    for elem in a:
        if elem not in b:
            return 0

    for elem in b:
        if elem not in a:
            return 0

    return 1


def makeList(x):
    if type(x) is types.ListType:
        return x
    elif type(x) is types.TupleType:
        return list(x)
    else:
        return [x]


def makeTuple(x):
    if type(x) is types.ListType:
        return tuple(x)
    elif type(x) is types.TupleType:
        return x
    else:
        return (x,)


def list2dict(L, value = None):
    return dict([ (k, value) for k in L ])


def listToIndex2item(L):
    d = {}
    for i, item in enumerate(L):
        d[i] = item

    return d


def listToItem2index(L):
    d = {}
    for i, item in enumerate(L):
        d[item] = i

    return d


def invertDict(D, lossy = False):
    n = {}
    for key, value in D.items():
        if not lossy and value in n:
            raise 'duplicate key in invertDict: %s' % value
        n[value] = key

    return n


def invertDictLossless(D):
    n = {}
    for key, value in D.items():
        n.setdefault(value, [])
        n[value].append(key)

    return n


def uniqueElements(L):
    return len(L) == len(list2dict(L))


def disjoint(L1, L2):
    used = dict([ (k, None) for k in L1 ])
    for k in L2:
        if k in used:
            return 0

    return 1


def contains(whole, sub):
    if whole == sub:
        return 1
    for elem in sub:
        if elem not in whole:
            return 0

    return 1


def replace(list, old, new, all = 0):
    if old not in list:
        return 0
    if not all:
        i = list.index(old)
        list[i] = new
        return 1
    else:
        numReplaced = 0
        for i in xrange(len(list)):
            if list[i] == old:
                numReplaced += 1
                list[i] = new

        return numReplaced


rad90 = math.pi / 2.0
rad180 = math.pi
rad270 = 1.5 * math.pi
rad360 = 2.0 * math.pi

def reduceAngle(deg):
    return (deg + 180.0) % 360.0 - 180.0


def fitSrcAngle2Dest(src, dest):
    return dest + reduceAngle(src - dest)


def fitDestAngle2Src(src, dest):
    return src + reduceAngle(dest - src)


def closestDestAngle2(src, dest):
    diff = src - dest
    if diff > 180:
        return dest - 360
    elif diff < -180:
        return dest + 360
    else:
        return dest


def closestDestAngle(src, dest):
    diff = src - dest
    if diff > 180:
        return src - (diff - 360)
    elif diff < -180:
        return src - (360 + diff)
    else:
        return dest


def binaryRepr(number, max_length = 32):
    shifts = map(operator.rshift, max_length * [number], range(max_length - 1, -1, -1))
    digits = map(operator.mod, shifts, max_length * [2])
    if not digits.count(1):
        return 0
    digits = digits[digits.index(1):]
    return string.join(map(repr, digits), '')


class StdoutCapture():
    __module__ = __name__

    def __init__(self):
        self._oldStdout = sys.stdout
        sys.stdout = self
        self._string = ''

    def destroy(self):
        sys.stdout = self._oldStdout
        del self._oldStdout

    def getString(self):
        return self._string

    def write(self, string):
        self._string = ''.join([self._string, string])


class StdoutPassthrough(StdoutCapture):
    __module__ = __name__

    def write(self, string):
        self._string = ''.join([self._string, string])
        self._oldStdout.write(string)


PyUtilProfileDefaultFilename = 'profiledata'
PyUtilProfileDefaultLines = 80
PyUtilProfileDefaultSorts = ['cumulative', 'time', 'calls']
_ProfileResultStr = ''

def getProfileResultString():
    global _ProfileResultStr
    return _ProfileResultStr


def profileFunc(callback, name, terse, log = True):
    global _ProfileResultStr
    if 'globalProfileFunc' in __builtin__.__dict__:
        base.notify.warning('PythonUtil.profileStart(%s): aborted, already profiling %s' % (name, __builtin__.globalProfileFunc))
        return
    __builtin__.globalProfileFunc = callback
    __builtin__.globalProfileResult = [None]
    prefix = '***** START PROFILE: %s *****' % name
    if log:
        print prefix
    startProfile(cmd='globalProfileResult[0]=globalProfileFunc()', callInfo=not terse, silent=not log)
    suffix = '***** END PROFILE: %s *****' % name
    if log:
        print suffix
    else:
        _ProfileResultStr = '%s\n%s\n%s' % (prefix, _ProfileResultStr, suffix)
    result = globalProfileResult[0]
    del __builtin__.__dict__['globalProfileFunc']
    del __builtin__.__dict__['globalProfileResult']
    return result


def profiled(category = None, terse = False):

    def profileDecorator(f):

        def _profiled(*args, **kArgs):
            global Functor
            name = '(%s) %s from %s' % (category, f.func_name, f.__module__)
            if category is None or ConfigVariableBool('want-profile-%s' % category, 0).getValue():
                return profileFunc(Functor(f, *args, **kArgs), name, terse)
            else:
                return f(*args, **kArgs)
            return

        _profiled.__doc__ = f.__doc__
        return _profiled

    return profileDecorator


movedOpenFuncs = []
movedDumpFuncs = []
movedLoadFuncs = []
profileFilenames = set()
profileFilenameList = Stack()
profileFilename2file = {}
profileFilename2marshalData = {}

def _profileOpen(filename, *args, **kArgs):
    if filename in profileFilenames:
        if filename not in profileFilename2file:
            file = StringIO()
            file._profFilename = filename
            profileFilename2file[filename] = file
        else:
            file = profileFilename2file[filename]
    else:
        file = movedOpenFuncs[-1](filename, *args, **kArgs)
    return file


def _profileMarshalDump(data, file):
    if isinstance(file, StringIO) and hasattr(file, '_profFilename'):
        if file._profFilename in profileFilenames:
            profileFilename2marshalData[file._profFilename] = data
            return None
    return movedDumpFuncs[-1](data, file)


def _profileMarshalLoad(file):
    if isinstance(file, StringIO) and hasattr(file, '_profFilename'):
        if file._profFilename in profileFilenames:
            return profileFilename2marshalData[file._profFilename]
    return movedLoadFuncs[-1](file)


def _installProfileCustomFuncs(filename):
    profileFilenames.add(filename)
    profileFilenameList.push(filename)
    movedOpenFuncs.append(__builtin__.open)
    __builtin__.open = _profileOpen
    movedDumpFuncs.append(marshal.dump)
    marshal.dump = _profileMarshalDump
    movedLoadFuncs.append(marshal.load)
    marshal.load = _profileMarshalLoad


def _getProfileResultFileInfo(filename):
    return (profileFilename2file.get(filename, None), profileFilename2marshalData.get(filename, None))


def _setProfileResultsFileInfo(filename, info):
    f, m = info
    if f:
        profileFilename2file[filename] = f
    if m:
        profileFilename2marshalData[filename] = m


def _clearProfileResultFileInfo(filename):
    profileFilename2file.pop(filename, None)
    profileFilename2marshalData.pop(filename, None)
    return


def _removeProfileCustomFuncs(filename):
    marshal.load = movedLoadFuncs.pop()
    marshal.dump = movedDumpFuncs.pop()
    __builtin__.open = movedOpenFuncs.pop()
    profileFilenames.remove(filename)
    profileFilenameList.pop()
    profileFilename2file.pop(filename, None)
    profileFilename2marshalData.pop(filename, None)
    return


def _profileWithoutGarbageLeak(cmd, filename):
    import profile
    Profile = profile.Profile
    statement = cmd
    sort = -1
    retVal = None
    prof = Profile()
    try:
        prof = prof.run(statement)
    except SystemExit:
        pass

    if filename is not None:
        prof.dump_stats(filename)
    else:
        retVal = prof.print_stats(sort)
    del prof.dispatcher
    return retVal


def startProfile(filename = PyUtilProfileDefaultFilename, lines = PyUtilProfileDefaultLines, sorts = PyUtilProfileDefaultSorts, silent = 0, callInfo = 1, useDisk = False, cmd = 'run()'):
    filename = '%s.%s%s' % (filename, randUint31(), randUint31())
    if not useDisk:
        _installProfileCustomFuncs(filename)
    _profileWithoutGarbageLeak(cmd, filename)
    if silent:
        extractProfile(filename, lines, sorts, callInfo)
    else:
        printProfile(filename, lines, sorts, callInfo)
    if not useDisk:
        _removeProfileCustomFuncs(filename)
    else:
        os.remove(filename)


def printProfile(filename = PyUtilProfileDefaultFilename, lines = PyUtilProfileDefaultLines, sorts = PyUtilProfileDefaultSorts, callInfo = 1):
    import pstats
    s = pstats.Stats(filename)
    s.strip_dirs()
    for sort in sorts:
        s.sort_stats(sort)
        s.print_stats(lines)
        if callInfo:
            s.print_callees(lines)
            s.print_callers(lines)


def extractProfile(*args, **kArgs):
    global _ProfileResultStr
    sc = StdoutCapture()
    printProfile(*args, **kArgs)
    _ProfileResultStr = sc.getString()
    sc.destroy()


def getSetterName(valueName, prefix = 'set'):
    return '%s%s%s' % (prefix, string.upper(valueName[0]), valueName[1:])


def getSetter(targetObj, valueName, prefix = 'set'):
    return getattr(targetObj, getSetterName(valueName, prefix))


def mostDerivedLast(classList):

    def compare(a, b):
        if issubclass(a, b):
            result = 1
        elif issubclass(b, a):
            result = -1
        else:
            result = 0
        return result

    classList.sort(compare)


class ParamObj():
    __module__ = __name__

    class ParamSet():
        __module__ = __name__
        Params = {}

        def __init__(self, *args, **kwArgs):
            self.__class__._compileDefaultParams()
            if len(args) == 1 and len(kwArgs) == 0:
                obj = args[0]
                self.paramVals = {}
                for param in self.getParams():
                    self.paramVals[param] = getSetter(obj, param, 'get')()

            else:
                self.paramVals = dict(kwArgs)

        def getValue(self, param):
            if param in self.paramVals:
                return self.paramVals[param]
            return self._Params[param]

        def applyTo(self, obj):
            obj.lockParams()
            for param in self.getParams():
                getSetter(obj, param)(self.getValue(param))

            obj.unlockParams()

        def extractFrom(self, obj):
            obj.lockParams()
            for param in self.getParams():
                self.paramVals[param] = getSetter(obj, param, 'get')()

            obj.unlockParams()

        @classmethod
        def getParams(cls):
            cls._compileDefaultParams()
            return cls._Params.keys()

        @classmethod
        def getDefaultValue(cls, param):
            cls._compileDefaultParams()
            dv = cls._Params[param]
            if hasattr(dv, '__call__'):
                dv = dv()
            return dv

        @classmethod
        def _compileDefaultParams(cls):
            if '_Params' in cls.__dict__:
                return
            bases = list(cls.__bases__)
            mostDerivedLast(bases)
            cls._Params = {}
            for c in bases + [cls]:
                c._compileDefaultParams()
                if 'Params' in c.__dict__:
                    cls._Params.update(c.Params)

        def __repr__(self):
            argStr = ''
            for param in self.getParams():
                argStr += '%s=%s,' % (param, repr(self.getValue(param)))

            return '%s.%s(%s)' % (self.__class__.__module__, self.__class__.__name__, argStr)

    def __init__(self, *args, **kwArgs):
        params = None
        if len(args) == 1 and len(kwArgs) == 0:
            params = args[0]
        elif len(kwArgs) > 0:
            params = self.ParamSet(**kwArgs)
        self._paramLockRefCount = 0
        self._curParamStack = []
        self._priorValuesStack = []
        for param in self.ParamSet.getParams():
            setattr(self, param, self.ParamSet.getDefaultValue(param))
            setterName = getSetterName(param)
            getterName = getSetterName(param, 'get')
            if not hasattr(self, setterName):

                def defaultSetter(self, value, param = param):
                    setattr(self, param, value)

                self.__class__.__dict__[setterName] = defaultSetter
            if not hasattr(self, getterName):

                def defaultGetter(self, param = param, default = self.ParamSet.getDefaultValue(param)):
                    return getattr(self, param, default)

                self.__class__.__dict__[getterName] = defaultGetter
            origSetterName = '%s_ORIG' % (setterName,)
            if not hasattr(self, origSetterName):
                origSetterFunc = getattr(self.__class__, setterName)
                setattr(self.__class__, origSetterName, origSetterFunc)

                def setterStub(self, value, param = param, origSetterName = origSetterName):
                    if self._paramLockRefCount > 0:
                        priorValues = self._priorValuesStack[-1]
                        if param not in priorValues:
                            try:
                                priorValue = getSetter(self, param, 'get')()
                            except:
                                priorValue = None

                            priorValues[param] = priorValue
                        self._paramsSet[param] = None
                        getattr(self, origSetterName)(value)
                    else:
                        try:
                            priorValue = getSetter(self, param, 'get')()
                        except:
                            priorValue = None

                        self._priorValuesStack.append({param: priorValue})
                        getattr(self, origSetterName)(value)
                        applier = getattr(self, getSetterName(param, 'apply'), None)
                        if applier is not None:
                            self._curParamStack.append(param)
                            applier()
                            self._curParamStack.pop()
                        self._priorValuesStack.pop()
                        if hasattr(self, 'handleParamChange'):
                            self.handleParamChange((param,))
                    return

                setattr(self.__class__, setterName, setterStub)

        if params is not None:
            params.applyTo(self)
        return

    def destroy(self):
        pass

    def setDefaultParams(self):
        self.ParamSet().applyTo(self)

    def getCurrentParams(self):
        params = self.ParamSet()
        params.extractFrom(self)
        return params

    def lockParams(self):
        self._paramLockRefCount += 1
        if self._paramLockRefCount == 1:
            self._handleLockParams()

    def unlockParams(self):
        if self._paramLockRefCount > 0:
            self._paramLockRefCount -= 1
            if self._paramLockRefCount == 0:
                self._handleUnlockParams()

    def _handleLockParams(self):
        self._paramsSet = {}
        self._priorValuesStack.append({})

    def _handleUnlockParams(self):
        for param in self._paramsSet:
            applier = getattr(self, getSetterName(param, 'apply'), None)
            if applier is not None:
                self._curParamStack.append(param)
                applier()
                self._curParamStack.pop()

        self._priorValuesStack.pop()
        if hasattr(self, 'handleParamChange'):
            self.handleParamChange(tuple(self._paramsSet.keys()))
        del self._paramsSet
        return

    def paramsLocked(self):
        return self._paramLockRefCount > 0

    def getPriorValue(self):
        return self._priorValuesStack[-1][self._curParamStack[-1]]

    def __repr__(self):
        argStr = ''
        for param in self.ParamSet.getParams():
            try:
                value = getSetter(self, param, 'get')()
            except:
                value = '<unknown>'

            argStr += '%s=%s,' % (param, repr(value))

        return '%s(%s)' % (self.__class__.__name__, argStr)


class POD():
    __module__ = __name__
    DataSet = {}

    def __init__(self, **kwArgs):
        self.__class__._compileDefaultDataSet()
        for name in self.getDataNames():
            if name in kwArgs:
                getSetter(self, name)(kwArgs[name])
            else:
                getSetter(self, name)(self.getDefaultValue(name))

    def setDefaultValues(self):
        for name in self.getDataNames():
            getSetter(self, name)(self.getDefaultValue(name))

    def copyFrom(self, other, strict = False):
        for name in self.getDataNames():
            if hasattr(other, getSetterName(name, 'get')):
                setattr(self, name, getSetter(other, name, 'get')())
            elif strict:
                raise "object '%s' doesn't have value '%s'" % (other, name)
            else:
                setattr(self, name, self.getDefaultValue(name))

        return self

    def makeCopy(self):
        return self.__class__().copyFrom(self)

    def applyTo(self, obj):
        for name in self.getDataNames():
            getSetter(obj, name)(getSetter(self, name, 'get')())

    def getValue(self, name):
        return getSetter(self, name, 'get')()

    @classmethod
    def getDataNames(cls):
        cls._compileDefaultDataSet()
        return cls._DataSet.keys()

    @classmethod
    def getDefaultValue(cls, name):
        cls._compileDefaultDataSet()
        dv = cls._DataSet[name]
        if hasattr(dv, '__call__'):
            dv = dv()
        return dv

    @classmethod
    def _compileDefaultDataSet(cls):
        if '_DataSet' in cls.__dict__:
            return
        if 'DataSet' in cls.__dict__:
            for name in cls.DataSet:
                setterName = getSetterName(name)
                if not hasattr(cls, setterName):

                    def defaultSetter(self, value, name = name):
                        setattr(self, name, value)

                    cls.__dict__[setterName] = defaultSetter
                getterName = getSetterName(name, 'get')
                if not hasattr(cls, getterName):

                    def defaultGetter(self, name = name):
                        return getattr(self, name)

                    cls.__dict__[getterName] = defaultGetter

        cls._DataSet = {}
        bases = list(cls.__bases__)
        bases.reverse()
        for curBase in bases:
            if issubclass(curBase, POD):
                curBase._compileDefaultDataSet()
                cls._DataSet.update(curBase._DataSet)

        if 'DataSet' in cls.__dict__:
            cls._DataSet.update(cls.DataSet)

    def __repr__(self):
        argStr = ''
        for name in self.getDataNames():
            argStr += '%s=%s,' % (name, repr(getSetter(self, name, 'get')()))

        return '%s(%s)' % (self.__class__.__name__, argStr)


def bound(value, bound1, bound2):
    if bound1 > bound2:
        return min(max(value, bound2), bound1)
    else:
        return min(max(value, bound1), bound2)


clamp = bound

def lerp(v0, v1, t):
    return v0 + (v1 - v0) * t


def clerp(v0, v1, t):
    x = t * t
    return lerp(v0, v1, 3.0 * x - 2.0 * t * x)


def triglerp(v0, v1, t):
    x = lerp(-math.pi / 2, math.pi / 2, t)
    v = math.sin(x)
    return lerp(v0, v1, (v + 1.0) / 2.0)


def getShortestRotation(start, end):
    start, end = start % 360, end % 360
    if abs(end - start) > 180:
        if end < start:
            end += 360
        else:
            start += 360
    return (start, end)


def average(*args):
    val = 0.0
    for arg in args:
        val += arg

    return val / len(args)


class Averager():
    __module__ = __name__

    def __init__(self, name):
        self._name = name
        self.reset()

    def reset(self):
        self._total = 0.0
        self._count = 0

    def addValue(self, value):
        self._total += value
        self._count += 1

    def getAverage(self):
        return self._total / self._count

    def getCount(self):
        return self._count


def addListsByValue(a, b):
    c = []
    for x, y in zip(a, b):
        c.append(x + y)

    return c


def boolEqual(a, b):
    return a and b or a or not b


def lineupPos(i, num, spacing):
    pos = float(i) * spacing
    return pos - float(spacing) * (num - 1) / 2.0


def formatElapsedSeconds(seconds):
    sign = ''
    if seconds < 0:
        seconds = -seconds
        sign = '-'
    seconds = math.floor(seconds)
    hours = math.floor(seconds / (60 * 60))
    if hours > 36:
        days = math.floor((hours + 12) / 24)
        return '%s%d days' % (sign, days)
    seconds -= hours * (60 * 60)
    minutes = int(seconds / 60)
    seconds -= minutes * 60
    if hours != 0:
        return '%s%d:%02d:%02d' % (sign,
         hours,
         minutes,
         seconds)
    else:
        return '%s%d:%02d' % (sign, minutes, seconds)


def solveQuadratic(a, b, c):
    if a == 0.0:
        return None
    D = b * b - 4.0 * a * c
    if D < 0:
        return None
    elif D == 0:
        return -b / (2.0 * a)
    else:
        sqrtD = math.sqrt(D)
        twoA = 2.0 * a
        root1 = (-b - sqrtD) / twoA
        root2 = (-b + sqrtD) / twoA
        return [root1, root2]
    return None


def stackEntryInfo(depth = 0, baseFileName = 1):
    try:
        stack = None
        frame = None
        try:
            stack = inspect.stack()
            frame = stack[depth + 1]
            filename = frame[1]
            if baseFileName:
                filename = os.path.basename(filename)
            lineNum = frame[2]
            funcName = frame[3]
            result = (filename, lineNum, funcName)
        finally:
            del stack
            del frame

    except:
        result = (None, None, None)

    return result


def lineInfo(baseFileName = 1):
    return stackEntryInfo(1, baseFileName)


def callerInfo(baseFileName = 1, howFarBack = 0):
    return stackEntryInfo(2 + howFarBack, baseFileName)


def lineTag(baseFileName = 1, verbose = 0, separator = ':'):
    fileName, lineNum, funcName = callerInfo(baseFileName)
    if fileName is None:
        return ''
    if verbose:
        return 'File "%s", line %s, in %s' % (fileName, lineNum, funcName)
    else:
        return '%s%s%s%s%s' % (fileName,
         separator,
         lineNum,
         separator,
         funcName)
    return


def findPythonModule(module):
    filename = module + '.py'
    for dir in sys.path:
        pathname = os.path.join(dir, filename)
        if os.path.exists(pathname):
            return pathname

    return None


def describeException(backTrace = 4):

    def byteOffsetToLineno(code, byte):
        import array
        lnotab = array.array('B', code.co_lnotab)
        line = code.co_firstlineno
        for i in range(0, len(lnotab), 2):
            byte -= lnotab[i]
            if byte <= 0:
                return line
            line += lnotab[i + 1]

        return line

    infoArr = sys.exc_info()
    exception = infoArr[0]
    exceptionName = getattr(exception, '__name__', None)
    extraInfo = infoArr[1]
    trace = infoArr[2]
    stack = []
    while trace.tb_next:
        frame = trace.tb_frame
        module = frame.f_globals.get('__name__', None)
        lineno = byteOffsetToLineno(frame.f_code, frame.f_lasti)
        stack.append('%s:%s, ' % (module, lineno))
        trace = trace.tb_next

    frame = trace.tb_frame
    module = frame.f_globals.get('__name__', None)
    lineno = byteOffsetToLineno(frame.f_code, frame.f_lasti)
    stack.append('%s:%s, ' % (module, lineno))
    description = ''
    for i in range(len(stack) - 1, max(len(stack) - backTrace, 0) - 1, -1):
        description += stack[i]

    description += '%s: %s' % (exceptionName, extraInfo)
    return description


def clampScalar(value, a, b):
    if a < b:
        if value < a:
            return a
        elif value > b:
            return b
        else:
            return value
    elif value < b:
        return b
    elif value > a:
        return a
    else:
        return value


def pivotScalar(scalar, pivot):
    return pivot + (pivot - scalar)


def weightedChoice(choiceList, rng = random.random, sum = None):
    if sum is None:
        sum = 0.0
        for weight, item in choiceList:
            sum += weight

    rand = rng()
    accum = rand * sum
    for weight, item in choiceList:
        accum -= weight
        if accum <= 0.0:
            return item

    return item


def randFloat(a, b = 0.0, rng = random.random):
    return lerp(a, b, rng())


def normalDistrib(a, b, gauss = random.gauss):
    while True:
        r = gauss((a + b) * 0.5, (b - a) / 6.0)
        if r >= a and r <= b:
            return r


def weightedRand(valDict, rng = random.random):
    selections = valDict.keys()
    weights = valDict.values()
    totalWeight = 0
    for weight in weights:
        totalWeight += weight

    randomWeight = rng() * totalWeight
    for i in range(len(weights)):
        totalWeight -= weights[i]
        if totalWeight <= randomWeight:
            return selections[i]

    return selections[-1]


def randUint31(rng = random.random):
    return int(rng() * 2147483647)


def randInt32(rng = random.random):
    i = int(rng() * 2147483647)
    if rng() < 0.5:
        i *= -1
    return i


def randUint32(rng = random.random):
    return long(rng() * 4294967295L)


class SerialNumGen():
    __module__ = __name__

    def __init__(self, start = None):
        if start is None:
            start = 0
        self.__counter = start - 1
        return

    def next(self):
        self.__counter += 1
        return self.__counter


class SerialMaskedGen(SerialNumGen):
    __module__ = __name__

    def __init__(self, mask, start = None):
        self._mask = mask
        SerialNumGen.__init__(self, start)

    def next(self):
        v = SerialNumGen.next(self)
        return v & self._mask


_serialGen = SerialNumGen()

def serialNum():
    global _serialGen
    return _serialGen.next()


def uniqueName(name):
    return '%s-%s' % (name, _serialGen.next())


class EnumIter():
    __module__ = __name__

    def __init__(self, enum):
        self._values = enum._stringTable.keys()
        self._index = 0

    def __iter__(self):
        return self

    def next(self):
        if self._index >= len(self._values):
            raise StopIteration
        self._index += 1
        return self._values[self._index - 1]


class Enum():
    __module__ = __name__

    def __init__(self, items, start = 0):
        if type(items) == types.StringType:
            items = items.split(',')
        self._stringTable = {}
        i = start
        for item in items:
            item = string.strip(item)
            if len(item) == 0:
                continue
            self.__dict__[item] = i
            self._stringTable[i] = item
            i += 1

    def __iter__(self):
        return EnumIter(self)

    def hasString(self, string):
        return string in set(self._stringTable.values())

    def fromString(self, string):
        if self.hasString(string):
            return self.__dict__[string]
        {}[string]

    def getString(self, value):
        return self._stringTable[value]

    def __contains__(self, value):
        return value in self._stringTable

    def __len__(self):
        return len(self._stringTable)

    def copyTo(self, obj):
        for name, value in self._stringTable:
            setattr(obj, name, value)


class Singleton(type):
    __module__ = __name__

    def __init__(cls, name, bases, dic):
        super(Singleton, cls).__init__(name, bases, dic)
        cls.instance = None
        return

    def __call__(cls, *args, **kw):
        if cls.instance is None:
            cls.instance = super(Singleton, cls).__call__(*args, **kw)
        return cls.instance


class SingletonError(ValueError):
    __module__ = __name__


def printListEnumGen--- This code section failed: ---

0	LOAD_CONST        0
3	STORE_FAST        'digits'

6	LOAD_GLOBAL       'len'
9	LOAD_FAST         'l'
12	CALL_FUNCTION_1   None
15	STORE_FAST        'n'

18	SETUP_LOOP        '57'
21	LOAD_FAST         'n'
24	LOAD_CONST        0
27	COMPARE_OP        '>'
30	JUMP_IF_FALSE     '56'

33	LOAD_FAST         'digits'
36	LOAD_CONST        1
39	INPLACE_ADD       None
40	STORE_FAST        'digits'

43	LOAD_FAST         'n'
46	LOAD_CONST        10
49	INPLACE_FLOOR_DIVIDE None
50	STORE_FAST        'n'
53	JUMP_BACK         '21'
56	POP_BLOCK         None
57_0	COME_FROM         '18'

57	LOAD_CONST        '%0'
60	LOAD_CONST        '%s'
63	LOAD_FAST         'digits'
66	BINARY_MODULO     None
67	BINARY_ADD        None
68	LOAD_CONST        'i:%s'
71	BINARY_ADD        None
72	STORE_FAST        'format'

75	SETUP_LOOP        '127'
78	LOAD_GLOBAL       'range'
81	LOAD_GLOBAL       'len'
84	LOAD_FAST         'l'
87	CALL_FUNCTION_1   None
90	CALL_FUNCTION_1   None
93	GET_ITER          None
94	FOR_ITER          '126'
97	STORE_FAST        'i'

100	LOAD_FAST         'format'
103	LOAD_FAST         'i'
106	LOAD_FAST         'l'
109	LOAD_FAST         'i'
112	BINARY_SUBSCR     None
113	BUILD_TUPLE_2     None
116	BINARY_MODULO     None
117	PRINT_ITEM        None
118	PRINT_NEWLINE_CONT None

119	LOAD_CONST        None
122	YIELD_VALUE       None
123	JUMP_BACK         '94'
126	POP_BLOCK         None
127_0	COME_FROM         '75'
127	LOAD_CONST        None
130	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 126


def printListEnum(l):
    for result in printListEnumGen(l):
        pass


dtoolSuperBase = None

def _getDtoolSuperBase():
    global dtoolSuperBase
    from pandac.PandaModules import PandaNode
    dtoolSuperBase = PandaNode('').__class__.__bases__[0].__bases__[0].__bases__[0]


safeReprNotify = None

def _getSafeReprNotify():
    global safeReprNotify
    from direct.directnotify.DirectNotifyGlobal import directNotify
    safeReprNotify = directNotify.newCategory('safeRepr')
    return safeReprNotify


def safeRepr(obj):
    if dtoolSuperBase is None:
        _getDtoolSuperBase()
    if safeReprNotify is None:
        _getSafeReprNotify()
    if isinstance(obj, dtoolSuperBase):
        safeReprNotify.info('calling repr on instance of %s.%s' % (obj.__class__.__module__, obj.__class__.__name__))
        sys.stdout.flush()
    try:
        return repr(obj)
    except:
        return '<** FAILED REPR OF %s instance at %s **>' % (obj.__class__.__name__, hex(id(obj)))

    return


def safeReprTypeOnFail(obj):
    if dtoolSuperBase is None:
        _getDtoolSuperBase()
    if safeReprNotify is None:
        _getSafeReprNotify()
    if isinstance(obj, dtoolSuperBase):
        return type(obj)
    try:
        return repr(obj)
    except:
        return '<** FAILED REPR OF %s instance at %s **>' % (obj.__class__.__name__, hex(id(obj)))

    return


def fastRepr(obj, maxLen = 200, strFactor = 10, _visitedIds = None):
    try:
        if _visitedIds is None:
            _visitedIds = set()
        if id(obj) in _visitedIds:
            return '<ALREADY-VISITED %s>' % itype(obj)
        if type(obj) in (types.TupleType, types.ListType):
            s = ''
            s += {types.TupleType: '(',
             types.ListType: '['}[type(obj)]
            if maxLen is not None and len(obj) > maxLen:
                o = obj[:maxLen]
                ellips = '...'
            else:
                o = obj
                ellips = ''
            _visitedIds.add(id(obj))
            for item in o:
                s += fastRepr(item, maxLen, _visitedIds=_visitedIds)
                s += ', '

            _visitedIds.remove(id(obj))
            s += ellips
            s += {types.TupleType: ')',
             types.ListType: ']'}[type(obj)]
            return s
        elif type(obj) is types.DictType:
            s = '{'
            if maxLen is not None and len(obj) > maxLen:
                o = obj.keys()[:maxLen]
                ellips = '...'
            else:
                o = obj.keys()
                ellips = ''
            _visitedIds.add(id(obj))
            for key in o:
                value = obj[key]
                s += '%s: %s, ' % (fastRepr(key, maxLen, _visitedIds=_visitedIds), fastRepr(value, maxLen, _visitedIds=_visitedIds))

            _visitedIds.remove(id(obj))
            s += ellips
            s += '}'
            return s
        elif type(obj) is types.StringType:
            if maxLen is not None:
                maxLen *= strFactor
            if maxLen is not None and len(obj) > maxLen:
                return safeRepr(obj[:maxLen])
            else:
                return safeRepr(obj)
        else:
            r = safeRepr(obj)
            maxLen *= strFactor
            if len(r) > maxLen:
                r = r[:maxLen]
            return r
    except:
        return '<** FAILED REPR OF %s **>' % obj.__class__.__name__

    return


baseLine = {}

def baseLineCheck():
    global baseLine
    import gc
    obj = gc.get_objects()
    baseLine = {}
    for i in obj:
        baseLine[str(itype(i))] = 0

    for i in obj:
        baseLine[str(itype(i))] += 1


def diffSinceBaseLine():
    import copy
    import gc
    obj = gc.get_objects()
    since = copy.deepcopy(baseLine)
    for i in obj:
        since.setdefault(str(itype(i)), 0)

    for i in obj:
        since[str(itype(i))] -= 1

    for i in since.keys():
        if not since[i]:
            del since[i]
        else:
            since[i] = abs(since[i])

    final = [ (since[x], x) for x in since ]
    final.sort()
    final.reverse()
    for i in final:
        print i

    final = []
    since = []


def _getr(slist, olist, seen):
    for e in slist:
        if id(e) in seen:
            continue
        seen[id(e)] = None
        olist.append(e)
        tl = gc.get_referents(e)
        if tl:
            _getr(tl, olist, seen)

    return


def get_all_objects():
    gcl = gc.get_objects()
    olist = []
    seen = {}
    seen[id(gcl)] = None
    seen[id(olist)] = None
    seen[id(seen)] = None
    _getr(gcl, olist, seen)
    return olist


def getIdList():
    baseList = get_all_objects()
    idList = {}
    for i in baseList:
        idList[id(i)] = i

    return idList


ftype = None

def getTree(obj):
    global ftype
    if not ftype:
        ftype = itype(sys._getframe())
    objId = id(obj)
    obj = None
    idList = getIdList()
    objList = [objId]
    objTree = {objId: {}}
    r_add_chain(objId, objList, objTree[objId], idList, 0)
    return convertTree(objTree, idList)


def convertTree(objTree, idList):
    newTree = {}
    for key in objTree.keys():
        obj = (idList[key],)
        newTree[obj] = {}
        r_convertTree(objTree[key], newTree[obj], idList)

    return newTree


def r_convertTree(oldTree, newTree, idList):
    for key in oldTree.keys():
        obj = idList.get(key)
        if not obj:
            continue
        obj = str(obj)[:100]
        newTree[obj] = {}
        r_convertTree(oldTree[key], newTree[obj], idList)


def pretty_print(tree):
    for name in tree.keys():
        print name
        r_pretty_print(tree[name], 0)


def r_pretty_print(tree, num):
    num += 1
    for name in tree.keys():
        print '  ' * num, name
        r_pretty_print(tree[name], num)


def r_add_chain(objId, objList, objTree, idList, num):
    num += 1
    obj = idList.get(objId)
    if not obj:
        return
    refList = gc.get_referrers(obj)
    for ref in refList:
        refId = id(ref)
        if ref == __builtins__:
            continue
        if ref == objList:
            continue
        if refId in objList:
            continue
        if ref == idList:
            continue
        if itype(ref) == ftype:
            continue
        if itype(ref) == itype(sys):
            continue
        objList.append(refId)
        objTree[refId] = {}

    refList = None
    for refId in objTree:
        r_add_chain(refId, objList, objTree[refId], idList, num)

    return


def tagRepr(obj, tag):

    def reprWithTag(oldRepr, tag, self):
        return oldRepr() + '::<TAG=' + tag + '>'

    oldRepr = getattr(obj, '__repr__', None)
    if oldRepr is None:

        def stringer(s):
            return s

        oldRepr = Functor(stringer, repr(obj))
        stringer = None
    obj.__repr__ = new.instancemethod(Functor(reprWithTag, oldRepr, tag), obj, obj.__class__)
    reprWithTag = None
    return obj


def tagWithCaller(obj):
    tagRepr(obj, str(callerInfo(howFarBack=1)))


def isDefaultValue(x):
    return x == type(x)()


def notNone(A, B):
    if A is None:
        return B
    return A


def appendStr(obj, st):

    def appendedStr(oldStr, st, self):
        return oldStr() + st

    oldStr = getattr(obj, '__str__', None)
    if oldStr is None:

        def stringer(s):
            return s

        oldStr = Functor(stringer, str(obj))
        stringer = None
    obj.__str__ = new.instancemethod(Functor(appendedStr, oldStr, st), obj, obj.__class__)
    appendedStr = None
    return obj


try:
    import pdb
    set_trace = pdb.set_trace

    def setTrace():
        set_trace()
        return True


    pm = pdb.pm
except:
    set_trace = None
    setTrace = None
    pm = None

class ScratchPad():
    __module__ = __name__

    def __init__(self, **kArgs):
        for key, value in kArgs.iteritems():
            setattr(self, key, value)

        self._keys = set(kArgs.keys())

    def add(self, **kArgs):
        for key, value in kArgs.iteritems():
            setattr(self, key, value)

        self._keys.update(kArgs.keys())

    def destroy(self):
        for key in self._keys:
            delattr(self, key)

    def __getitem__(self, itemName):
        return getattr(self, itemName)

    def get(self, itemName, default = None):
        return getattr(self, itemName, default)

    def __contains__(self, itemName):
        return itemName in self._keys


class DestructiveScratchPad(ScratchPad):
    __module__ = __name__

    def add(self, **kArgs):
        for key, value in kArgs.iteritems():
            if hasattr(self, key):
                getattr(self, key).destroy()
            setattr(self, key, value)

        self._keys.update(kArgs.keys())

    def destroy(self):
        for key in self._keys:
            getattr(self, key).destroy()

        ScratchPad.destroy(self)


class Sync():
    __module__ = __name__
    _SeriesGen = SerialNumGen()

    def __init__(self, name, other = None):
        self._name = name
        if other is None:
            self._series = self._SeriesGen.next()
            self._value = 0
        else:
            self._series = other._series
            self._value = other._value
        return

    def invalidate(self):
        self._value = None
        return

    def change(self):
        self._value += 1

    def sync(self, other):
        if self._series != other._series or self._value != other._value:
            self._series = other._series
            self._value = other._value
            return True
        else:
            return False

    def isSynced(self, other):
        return self._series == other._series and self._value == other._value

    def __repr__(self):
        return '%s(%s)<family=%s,value=%s>' % (self.__class__.__name__,
         self._name,
         self._series,
         self._value)


class RefCounter():
    __module__ = __name__

    def __init__(self, byId = False):
        self._byId = byId
        self._refCounts = {}

    def _getKey(self, item):
        if self._byId:
            key = id(item)
        else:
            key = item

    def inc(self, item):
        key = self._getKey(item)
        self._refCounts.setdefault(key, 0)
        self._refCounts[key] += 1

    def dec(self, item):
        key = self._getKey(item)
        self._refCounts[key] -= 1
        result = False
        if self._refCounts[key] == 0:
            result = True
            del self._refCounts[key]
        return result


def itype(obj):
    t = type(obj)
    if t is types.InstanceType:
        return '%s of <class %s>>' % (repr(types.InstanceType)[:-1], str(obj.__class__))
    else:
        if dtoolSuperBase is None:
            _getDtoolSuperBase()
        if isinstance(obj, dtoolSuperBase):
            return '%s of %s>' % (repr(types.InstanceType)[:-1], str(obj.__class__))
        return t
    return


def deeptype(obj, maxLen = 100, _visitedIds = None):
    if _visitedIds is None:
        _visitedIds = set()
    if id(obj) in _visitedIds:
        return '<ALREADY-VISITED %s>' % itype(obj)
    t = type(obj)
    if t in (types.TupleType, types.ListType):
        s = ''
        s += {types.TupleType: '(',
         types.ListType: '['}[type(obj)]
        if maxLen is not None and len(obj) > maxLen:
            o = obj[:maxLen]
            ellips = '...'
        else:
            o = obj
            ellips = ''
        _visitedIds.add(id(obj))
        for item in o:
            s += deeptype(item, maxLen, _visitedIds=_visitedIds)
            s += ', '

        _visitedIds.remove(id(obj))
        s += ellips
        s += {types.TupleType: ')',
         types.ListType: ']'}[type(obj)]
        return s
    elif type(obj) is types.DictType:
        s = '{'
        if maxLen is not None and len(obj) > maxLen:
            o = obj.keys()[:maxLen]
            ellips = '...'
        else:
            o = obj.keys()
            ellips = ''
        _visitedIds.add(id(obj))
        for key in o:
            value = obj[key]
            s += '%s: %s, ' % (deeptype(key, maxLen, _visitedIds=_visitedIds), deeptype(value, maxLen, _visitedIds=_visitedIds))

        _visitedIds.remove(id(obj))
        s += ellips
        s += '}'
        return s
    else:
        return str(itype(obj))
    return


def getNumberedTypedString(items, maxLen = 5000, numPrefix = ''):
    digits = 0
    n = len(items)
    while n > 0:
        digits += 1
        n //= 10

    digits = digits
    format = numPrefix + '%0' + '%s' % digits + 'i:%s \t%s'
    first = True
    s = ''
    snip = '<SNIP>'
    for i in xrange(len(items)):
        if not first:
            s += '\n'
        first = False
        objStr = fastRepr(items[i])
        if len(objStr) > maxLen:
            objStr = '%s%s' % (objStr[:maxLen - len(snip)], snip)
        s += format % (i, itype(items[i]), objStr)

    return s


def getNumberedTypedSortedString(items, maxLen = 5000, numPrefix = ''):
    digits = 0
    n = len(items)
    while n > 0:
        digits += 1
        n //= 10

    digits = digits
    format = numPrefix + '%0' + '%s' % digits + 'i:%s \t%s'
    snip = '<SNIP>'
    strs = []
    for item in items:
        objStr = fastRepr(item)
        if len(objStr) > maxLen:
            objStr = '%s%s' % (objStr[:maxLen - len(snip)], snip)
        strs.append(objStr)

    first = True
    s = ''
    strs.sort()
    for i in xrange(len(strs)):
        if not first:
            s += '\n'
        first = False
        objStr = strs[i]
        s += format % (i, itype(items[i]), strs[i])

    return s


def getNumberedTypedSortedStringWithReferrersGen--- This code section failed: ---

0	LOAD_CONST        0
3	STORE_FAST        'digits'

6	LOAD_GLOBAL       'len'
9	LOAD_FAST         'items'
12	CALL_FUNCTION_1   None
15	STORE_FAST        'n'

18	SETUP_LOOP        '57'
21	LOAD_FAST         'n'
24	LOAD_CONST        0
27	COMPARE_OP        '>'
30	JUMP_IF_FALSE     '56'

33	LOAD_FAST         'digits'
36	LOAD_CONST        1
39	INPLACE_ADD       None
40	STORE_FAST        'digits'

43	LOAD_FAST         'n'
46	LOAD_CONST        10
49	INPLACE_FLOOR_DIVIDE None
50	STORE_FAST        'n'
53	JUMP_BACK         '21'
56	POP_BLOCK         None
57_0	COME_FROM         '18'

57	LOAD_FAST         'digits'
60	STORE_FAST        'digits'

63	LOAD_FAST         'numPrefix'
66	LOAD_CONST        '%0'
69	BINARY_ADD        None
70	LOAD_CONST        '%s'
73	LOAD_FAST         'digits'
76	BINARY_MODULO     None
77	BINARY_ADD        None
78	LOAD_CONST        'i:%s @ %s \t%s'
81	BINARY_ADD        None
82	STORE_FAST        'format'

85	LOAD_CONST        '<SNIP>'
88	STORE_FAST        'snip'

91	BUILD_LIST_0      None
94	STORE_FAST        'strs'

97	SETUP_LOOP        '133'
100	LOAD_FAST         'items'
103	GET_ITER          None
104	FOR_ITER          '132'
107	STORE_FAST        'item'

110	LOAD_FAST         'strs'
113	LOAD_ATTR         'append'
116	LOAD_GLOBAL       'fastRepr'
119	LOAD_FAST         'item'
122	CALL_FUNCTION_1   None
125	CALL_FUNCTION_1   None
128	POP_TOP           None
129	JUMP_BACK         '104'
132	POP_BLOCK         None
133_0	COME_FROM         '97'

133	LOAD_FAST         'strs'
136	LOAD_ATTR         'sort'
139	CALL_FUNCTION_0   None
142	POP_TOP           None

143	SETUP_LOOP        '367'
146	LOAD_GLOBAL       'xrange'
149	LOAD_GLOBAL       'len'
152	LOAD_FAST         'strs'
155	CALL_FUNCTION_1   None
158	CALL_FUNCTION_1   None
161	GET_ITER          None
162	FOR_ITER          '366'
165	STORE_FAST        'i'

168	LOAD_FAST         'items'
171	LOAD_FAST         'i'
174	BINARY_SUBSCR     None
175	STORE_FAST        'item'

178	LOAD_FAST         'strs'
181	LOAD_FAST         'i'
184	BINARY_SUBSCR     None
185	STORE_FAST        'objStr'

188	LOAD_FAST         'objStr'
191	LOAD_CONST        ', \tREFERRERS=['
194	INPLACE_ADD       None
195	STORE_FAST        'objStr'

198	LOAD_GLOBAL       'gc'
201	LOAD_ATTR         'get_referrers'
204	LOAD_FAST         'item'
207	CALL_FUNCTION_1   None
210	STORE_FAST        'referrers'

213	SETUP_LOOP        '262'
216	LOAD_FAST         'referrers'
219	GET_ITER          None
220	FOR_ITER          '261'
223	STORE_FAST        'ref'

226	LOAD_FAST         'objStr'
229	LOAD_CONST        '%s@%s, '
232	LOAD_GLOBAL       'itype'
235	LOAD_FAST         'ref'
238	CALL_FUNCTION_1   None
241	LOAD_GLOBAL       'id'
244	LOAD_FAST         'ref'
247	CALL_FUNCTION_1   None
250	BUILD_TUPLE_2     None
253	BINARY_MODULO     None
254	INPLACE_ADD       None
255	STORE_FAST        'objStr'
258	JUMP_BACK         '220'
261	POP_BLOCK         None
262_0	COME_FROM         '213'

262	LOAD_FAST         'objStr'
265	LOAD_CONST        ']'
268	INPLACE_ADD       None
269	STORE_FAST        'objStr'

272	LOAD_GLOBAL       'len'
275	LOAD_FAST         'objStr'
278	CALL_FUNCTION_1   None
281	LOAD_FAST         'maxLen'
284	COMPARE_OP        '>'
287	JUMP_IF_FALSE     '323'

290	LOAD_CONST        '%s%s'
293	LOAD_FAST         'objStr'
296	LOAD_FAST         'maxLen'
299	LOAD_GLOBAL       'len'
302	LOAD_FAST         'snip'
305	CALL_FUNCTION_1   None
308	BINARY_SUBTRACT   None
309	SLICE+2           None
310	LOAD_FAST         'snip'
313	BUILD_TUPLE_2     None
316	BINARY_MODULO     None
317	STORE_FAST        'objStr'
320	JUMP_FORWARD      '323'
323_0	COME_FROM         '320'

323	LOAD_FAST         'format'
326	LOAD_FAST         'i'
329	LOAD_GLOBAL       'itype'
332	LOAD_FAST         'items'
335	LOAD_FAST         'i'
338	BINARY_SUBSCR     None
339	CALL_FUNCTION_1   None
342	LOAD_GLOBAL       'id'
345	LOAD_FAST         'items'
348	LOAD_FAST         'i'
351	BINARY_SUBSCR     None
352	CALL_FUNCTION_1   None
355	LOAD_FAST         'objStr'
358	BUILD_TUPLE_4     None
361	BINARY_MODULO     None
362	YIELD_VALUE       None
363	JUMP_BACK         '162'
366	POP_BLOCK         None
367_0	COME_FROM         '143'

Syntax error at or near `POP_BLOCK' token at offset 366


def getNumberedTypedSortedStringWithReferrers(items, maxLen = 10000, numPrefix = ''):
    s = ''
    for line in getNumberedTypedSortedStringWithReferrersGen(items, maxLen, numPrefix):
        s += '%s\n' % line

    return s


def printNumberedTyped(items, maxLen = 5000):
    digits = 0
    n = len(items)
    while n > 0:
        digits += 1
        n //= 10

    digits = digits
    format = '%0' + '%s' % digits + 'i:%s \t%s'
    for i in xrange(len(items)):
        objStr = fastRepr(items[i])
        if len(objStr) > maxLen:
            snip = '<SNIP>'
            objStr = '%s%s' % (objStr[:maxLen - len(snip)], snip)
        print format % (i, itype(items[i]), objStr)


def printNumberedTypesGen--- This code section failed: ---

0	LOAD_CONST        0
3	STORE_FAST        'digits'

6	LOAD_GLOBAL       'len'
9	LOAD_FAST         'items'
12	CALL_FUNCTION_1   None
15	STORE_FAST        'n'

18	SETUP_LOOP        '57'
21	LOAD_FAST         'n'
24	LOAD_CONST        0
27	COMPARE_OP        '>'
30	JUMP_IF_FALSE     '56'

33	LOAD_FAST         'digits'
36	LOAD_CONST        1
39	INPLACE_ADD       None
40	STORE_FAST        'digits'

43	LOAD_FAST         'n'
46	LOAD_CONST        10
49	INPLACE_FLOOR_DIVIDE None
50	STORE_FAST        'n'
53	JUMP_BACK         '21'
56	POP_BLOCK         None
57_0	COME_FROM         '18'

57	LOAD_FAST         'digits'
60	STORE_FAST        'digits'

63	LOAD_CONST        '%0'
66	LOAD_CONST        '%s'
69	LOAD_FAST         'digits'
72	BINARY_MODULO     None
73	BINARY_ADD        None
74	LOAD_CONST        'i:%s'
77	BINARY_ADD        None
78	STORE_FAST        'format'

81	SETUP_LOOP        '139'
84	LOAD_GLOBAL       'xrange'
87	LOAD_GLOBAL       'len'
90	LOAD_FAST         'items'
93	CALL_FUNCTION_1   None
96	CALL_FUNCTION_1   None
99	GET_ITER          None
100	FOR_ITER          '138'
103	STORE_FAST        'i'

106	LOAD_FAST         'format'
109	LOAD_FAST         'i'
112	LOAD_GLOBAL       'itype'
115	LOAD_FAST         'items'
118	LOAD_FAST         'i'
121	BINARY_SUBSCR     None
122	CALL_FUNCTION_1   None
125	BUILD_TUPLE_2     None
128	BINARY_MODULO     None
129	PRINT_ITEM        None
130	PRINT_NEWLINE_CONT None

131	LOAD_CONST        None
134	YIELD_VALUE       None
135	JUMP_BACK         '100'
138	POP_BLOCK         None
139_0	COME_FROM         '81'
139	LOAD_CONST        None
142	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 138


def printNumberedTypes--- This code section failed: ---

0	SETUP_LOOP        '30'
3	LOAD_GLOBAL       'printNumberedTypesGen'
6	LOAD_FAST         'items'
9	LOAD_FAST         'maxLen'
12	CALL_FUNCTION_2   None
15	GET_ITER          None
16	FOR_ITER          '29'
19	STORE_FAST        'result'

22	LOAD_FAST         'result'
25	YIELD_VALUE       None
26	JUMP_BACK         '16'
29	POP_BLOCK         None
30_0	COME_FROM         '0'

Syntax error at or near `POP_BLOCK' token at offset 29


class DelayedCall():
    __module__ = __name__

    def __init__(self, func, name = None, delay = None):
        if name is None:
            name = 'anonymous'
        if delay is None:
            delay = 0.01
        self._func = func
        self._taskName = 'DelayedCallback-%s' % name
        self._delay = delay
        self._finished = False
        self._addDoLater()
        return

    def destroy(self):
        self._finished = True
        self._removeDoLater()

    def finish(self):
        if not self._finished:
            self._doCallback()
        self.destroy()

    def _addDoLater(self):
        taskMgr.doMethodLater(self._delay, self._doCallback, self._taskName)

    def _removeDoLater(self):
        taskMgr.remove(self._taskName)

    def _doCallback(self, task):
        self._finished = True
        func = self._func
        del self._func
        func()


class FrameDelayedCall():
    __module__ = __name__

    def __init__(self, name, callback, frames = None, cancelFunc = None):
        if frames is None:
            frames = 1
        self._name = name
        self._frames = frames
        self._callback = callback
        self._cancelFunc = cancelFunc
        self._taskName = uniqueName('%s-%s' % (self.__class__.__name__, self._name))
        self._finished = False
        self._startTask()
        return

    def destroy(self):
        self._finished = True
        self._stopTask()
        self._callback = None
        self._cancelFunc = None
        return

    def finish(self):
        if not self._finished:
            self._finished = True
            self._callback()
        self.destroy()

    def _startTask(self):
        taskMgr.add(self._frameTask, self._taskName)
        self._counter = 0

    def _stopTask(self):
        taskMgr.remove(self._taskName)

    def _frameTask(self, task):
        if self._cancelFunc and self._cancelFunc():
            self.destroy()
            return task.done
        self._counter += 1
        if self._counter >= self._frames:
            self.finish()
            return task.done
        return task.cont


class DelayedFunctor():
    __module__ = __name__

    def __init__(self, functor, name = None, delay = None):
        self._functor = functor
        self._name = name
        self.__name__ = self._name
        self._delay = delay

    def _callFunctor(self):
        cb = Functor(self._functor, *self._args, **self._kwArgs)
        del self._functor
        del self._name
        del self._delay
        del self._args
        del self._kwArgs
        del self._delayedCall
        del self.__name__
        cb()

    def __call__(self, *args, **kwArgs):
        self._args = args
        self._kwArgs = kwArgs
        self._delayedCall = DelayedCall(self._callFunctor, self._name, self._delay)


class SubframeCall():
    __module__ = __name__

    def __init__(self, functor, taskPriority, name = None):
        self._functor = functor
        self._name = name
        self._taskName = uniqueName('SubframeCall-%s' % self._name)
        taskMgr.add(self._doCallback, self._taskName, priority=taskPriority)

    def _doCallback(self, task):
        functor = self._functor
        del self._functor
        functor()
        del self._name
        self._taskName = None
        return task.done

    def cleanup(self):
        if self._taskName:
            taskMgr.remove(self._taskName)
            self._taskName = None
        return

    def isFinished(self):
        return self._taskName == None


class ArgumentEater():
    __module__ = __name__

    def __init__(self, numToEat, func):
        self._numToEat = numToEat
        self._func = func

    def destroy(self):
        del self._func

    def __call__(self, *args, **kwArgs):
        self._func(*args[self._numToEat:], **kwArgs)


class ClassTree():
    __module__ = __name__

    def __init__(self, instanceOrClass):
        if type(instanceOrClass) in (types.ClassType, types.TypeType):
            cls = instanceOrClass
        else:
            cls = instanceOrClass.__class__
        self._cls = cls
        self._bases = []
        for base in self._cls.__bases__:
            if base not in (types.ObjectType, types.TypeType):
                self._bases.append(ClassTree(base))

    def getAllClasses(self):
        classes = set()
        classes.add(self._cls)
        for base in self._bases:
            classes.update(base.getAllClasses())

        return classes

    def _getStr(self, indent = None, clsLeftAtIndent = None):
        if indent is None:
            indent = 0
            clsLeftAtIndent = [1]
        s = ''
        if indent > 1:
            for i in range(1, indent):
                if clsLeftAtIndent[i] > 0:
                    s += ' |'
                else:
                    s += '  '

        if indent > 0:
            s += ' +'
        s += self._cls.__name__
        clsLeftAtIndent[indent] -= 1
        if len(self._bases):
            newList = list(clsLeftAtIndent)
            newList.append(len(self._bases))
            bases = self._bases
            bases.sort(lambda x, y: len(x._bases) - len(y._bases))
            for base in bases:
                s += '\n%s' % base._getStr(indent + 1, newList)

        return s

    def __repr__(self):
        return self._getStr()


class PStatScope():
    __module__ = __name__
    collectors = {}

    def __init__(self, level = None):
        self.levels = []
        if level:
            self.levels.append(level)

    def copy(self, push = None):
        c = PStatScope()
        c.levels = self.levels[:]
        if push:
            c.push(push)
        return c

    def __repr__(self):
        return "PStatScope - '%s'" % (self,)

    def __str__(self):
        return ':'.join(self.levels)

    def push(self, level):
        self.levels.append(level.replace('_', ''))

    def pop(self):
        return self.levels.pop()

    def start(self, push = None):
        if push:
            self.push(push)
        self.getCollector().start()

    def stop(self, pop = False):
        self.getCollector().stop()
        if pop:
            self.pop()

    def getCollector(self):
        label = str(self)
        if label not in self.collectors:
            from pandac.PandaModules import PStatCollector
            self.collectors[label] = PStatCollector(label)
        return self.collectors[label]


def pstatcollect(scope, level = None):

    def decorator(f):
        return f

    try:
        if not __dev__:
            return (not config.GetBool('force-pstatcollect', 0) or not scope) and decorator

        def decorator(f):

            def wrap(*args, **kw):
                scope.start(push=level or f.__name__)
                val = f(*args, **kw)
                scope.stop(pop=True)
                return val

            return wrap

    except:
        pass

    return decorator


__report_indent = 0

def report(types = [], prefix = '', xform = None, notifyFunc = None, dConfigParam = []):

    def indent(str):
        global __report_indent
        return ' ' * __report_indent + str

    def decorator(f):
        return f

    try:
        if not __dev__:
            if not config.GetBool('force-reports', 0):
                return decorator
            dConfigParamList = []
            doPrint = False
            if not dConfigParam:
                doPrint = True
            else:
                if not isinstance(dConfigParam, (list, tuple)):
                    dConfigParams = (dConfigParam,)
                else:
                    dConfigParams = dConfigParam
                dConfigParamList = [ param for param in dConfigParams if config.GetBool('want-%s-report' % (param,), 0) ]
                doPrint = bool(dConfigParamList)
            if not doPrint:
                return decorator
            prefixes = prefix and set([prefix])
        else:
            prefixes = set()
        for param in dConfigParamList:
            prefix = config.GetString('prefix-%s-report' % (param,), '')
            if prefix:
                prefixes.add(prefix)

    except NameError as e:
        return decorator

    from direct.distributed.ClockDelta import globalClockDelta

    def decorator(f):

        def wrap(*args, **kwargs):
            global __report_indent
            if args:
                rArgs = [args[0].__class__.__name__ + ', ']
            else:
                rArgs = []
            if 'args' in types:
                rArgs += [ repr(x) + ', ' for x in args[1:] ] + [ x + ' = ' + '%s, ' % repr(y) for x, y in kwargs.items() ]
            if not rArgs:
                rArgs = '()'
            else:
                rArgs = '(' + reduce(str.__add__, rArgs)[:-2] + ')'
            outStr = '%s%s' % (f.func_name, rArgs)
            if prefixes:
                outStr = '%%s %s' % (outStr,)
            if 'module' in types:
                outStr = '%s {M:%s}' % (outStr, f.__module__.split('.')[-1])
            if 'frameCount' in types:
                outStr = '%-8d : %s' % (globalClock.getFrameCount(), outStr)
            if 'timeStamp' in types:
                outStr = '%-8.3f : %s' % (globalClock.getFrameTime(), outStr)
            if 'deltaStamp' in types:
                outStr = '%-8.2f : %s' % (globalClock.getRealTime() - globalClockDelta.delta, outStr)
            if 'avLocation' in types:
                outStr = '%s : %s' % (outStr, str(localAvatar.getLocation()))
            if xform:
                outStr = '%s : %s' % (outStr, xform(args[0]))
            if prefixes:
                for prefix in prefixes:
                    if notifyFunc:
                        notifyFunc(outStr % (prefix,))
                    else:
                        print indent(outStr % (prefix,))

            elif notifyFunc:
                notifyFunc(outStr)
            else:
                print indent(outStr)
            if 'interests' in types:
                base.cr.printInterestSets()
            if 'stackTrace' in types:
                print StackTrace()
            rVal = None
            try:
                __report_indent += 1
                rVal = f(*args, **kwargs)
            finally:
                __report_indent -= 1
                if rVal is not None:
                    print indent(' -> ' + repr(rVal))

            return rVal

        wrap.func_name = f.func_name
        wrap.func_dict = f.func_dict
        wrap.func_doc = f.func_doc
        wrap.__module__ = f.__module__
        return wrap

    return decorator


def getBase():
    try:
        return base
    except:
        return simbase


def getRepository():
    try:
        return base.cr
    except:
        return simbase.air


exceptionLoggedNotify = None

def exceptionLogged(append = True):
    try:
        null = not __dev__
    except:
        null = not __debug__

    if null:

        def nullDecorator(f):
            return f

        return nullDecorator

    def _decoratorFunc(f, append = append):
        global exceptionLoggedNotify
        if exceptionLoggedNotify is None:
            from direct.directnotify.DirectNotifyGlobal import directNotify
            exceptionLoggedNotify = directNotify.newCategory('ExceptionLogged')

        def _exceptionLogged(*args, **kArgs):
            try:
                return f(*args, **kArgs)
            except Exception as e:
                try:
                    s = '%s(' % f.func_name
                    for arg in args:
                        s += '%s, ' % arg

                    for key, value in kArgs.items():
                        s += '%s=%s, ' % (key, value)

                    if len(args) or len(kArgs):
                        s = s[:-2]
                    s += ')'
                    if append:
                        appendStr(e, '\n%s' % s)
                    else:
                        exceptionLoggedNotify.info(s)
                except:
                    exceptionLoggedNotify.info('%s: ERROR IN PRINTING' % f.func_name)

                raise

        _exceptionLogged.__doc__ = f.__doc__
        return _exceptionLogged

    return _decoratorFunc


def recordCreationStack(cls):
    if not hasattr(cls, '__init__'):
        raise "recordCreationStack: class '%s' must define __init__" % cls.__name__
    cls.__moved_init__ = cls.__init__

    def __recordCreationStack_init__(self, *args, **kArgs):
        self._creationStackTrace = StackTrace(start=1)
        return self.__moved_init__(*args, **kArgs)

    def getCreationStackTrace(self):
        return self._creationStackTrace

    def getCreationStackTraceCompactStr(self):
        return self._creationStackTrace.compact()

    def printCreationStackTrace(self):
        print self._creationStackTrace

    cls.__init__ = __recordCreationStack_init__
    cls.getCreationStackTrace = getCreationStackTrace
    cls.getCreationStackTraceCompactStr = getCreationStackTraceCompactStr
    cls.printCreationStackTrace = printCreationStackTrace
    return cls


def recordCreationStackStr(cls):
    if not hasattr(cls, '__init__'):
        raise "recordCreationStackStr: class '%s' must define __init__" % cls.__name__
    cls.__moved_init__ = cls.__init__

    def __recordCreationStackStr_init__(self, *args, **kArgs):
        self._creationStackTraceStrLst = StackTrace(start=1).compact().split(',')
        return self.__moved_init__(*args, **kArgs)

    def getCreationStackTraceCompactStr(self):
        return string.join(self._creationStackTraceStrLst, ',')

    def printCreationStackTrace(self):
        print string.join(self._creationStackTraceStrLst, ',')

    cls.__init__ = __recordCreationStackStr_init__
    cls.getCreationStackTraceCompactStr = getCreationStackTraceCompactStr
    cls.printCreationStackTrace = printCreationStackTrace
    return cls


def logMethodCalls(cls):
    if not hasattr(cls, 'notify'):
        raise "logMethodCalls: class '%s' must have a notify" % cls.__name__
    for name in dir(cls):
        method = getattr(cls, name)
        if hasattr(method, '__call__'):

            def getLoggedMethodCall(method):

                def __logMethodCall__(obj, *args, **kArgs):
                    s = '%s(' % method.__name__
                    for arg in args:
                        try:
                            argStr = repr(arg)
                        except:
                            argStr = 'bad repr: %s' % arg.__class__

                        s += '%s, ' % argStr

                    for karg, value in kArgs.items():
                        s += '%s=%s, ' % (karg, repr(value))

                    if len(args) or len(kArgs):
                        s = s[:-2]
                    s += ')'
                    obj.notify.info(s)
                    return method(obj, *args, **kArgs)

                return __logMethodCall__

            setattr(cls, name, getLoggedMethodCall(method))

    __logMethodCall__ = None
    return cls


GoldenRatio = (1.0 + math.sqrt(5.0)) / 2.0

class GoldenRectangle():
    __module__ = __name__

    @staticmethod
    def getLongerEdge(shorter):
        return shorter * GoldenRatio

    @staticmethod
    def getShorterEdge(longer):
        return longer / GoldenRatio


class HotkeyBreaker():
    __module__ = __name__

    def __init__(self, breakKeys = []):
        from direct.showbase.DirectObject import DirectObject
        self.do = DirectObject()
        self.breakKeys = {}
        if not isinstance(breakKeys, (list, tuple)):
            breakKeys = (breakKeys,)
        for key in breakKeys:
            self.addBreakKey(key)

    def addBreakKey(self, breakKey):
        if __dev__:
            self.do.accept(breakKey, self.breakFunc, extraArgs=[breakKey])

    def removeBreakKey(self, breakKey):
        if __dev__:
            self.do.ignore(breakKey)

    def breakFunc(self, breakKey):
        if __dev__:
            self.breakKeys[breakKey] = True

    def setBreakPt(self, breakKey = None, persistent = False):
        if __dev__:
            if not breakKey:
                import pdb
                pdb.set_trace()
                return True
            elif self.breakKeys.get(breakKey, False):
                if not persistent:
                    self.breakKeys.pop(breakKey)
                import pdb
                pdb.set_trace()
                return True
        return True

    def clearBreakPt(self, breakKey):
        if __dev__:
            return bool(self.breakKeys.pop(breakKey, None))
        return None


def nullGen--- This code section failed: ---

0	LOAD_GLOBAL       'False'
3	JUMP_IF_FALSE     '13'

6	LOAD_CONST        None
9	YIELD_VALUE       None
10	JUMP_FORWARD      '13'
13_0	COME_FROM         '10'
13	LOAD_CONST        None
16	RETURN_VALUE      None

Syntax error at or near `COME_FROM' token at offset 13_0


def loopGen(l):

    def _gen--- This code section failed: ---

0	SETUP_LOOP        '34'
3	LOAD_GLOBAL       'True'
6	JUMP_IF_FALSE     '33'

9	SETUP_LOOP        '30'
12	LOAD_FAST         'l'
15	GET_ITER          None
16	FOR_ITER          '29'
19	STORE_FAST        'item'

22	LOAD_FAST         'item'
25	YIELD_VALUE       None
26	JUMP_BACK         '16'
29	POP_BLOCK         None
30_0	COME_FROM         '9'
30	JUMP_BACK         '3'
33	POP_BLOCK         None
34_0	COME_FROM         '0'

Syntax error at or near `POP_BLOCK' token at offset 29

    gen = _gen(l)
    _gen = None
    return gen


def makeFlywheelGen--- This code section failed: ---

0	LOAD_CONST        '<code_object flywheel>'
3	MAKE_FUNCTION_0   None
6	STORE_FAST        'flywheel'

9	LOAD_FAST         'countList'
12	LOAD_CONST        None
15	COMPARE_OP        'is'
18	JUMP_IF_FALSE     '70'

21	BUILD_LIST_0      None
24	STORE_FAST        'countList'

27	SETUP_LOOP        '70'
30	LOAD_FAST         'objects'
33	GET_ITER          None
34	FOR_ITER          '66'
37	STORE_FAST        'object'

40	LOAD_CONST        None
43	YIELD_VALUE       None

44	LOAD_FAST         'countList'
47	LOAD_ATTR         'append'
50	LOAD_FAST         'countFunc'
53	LOAD_FAST         'object'
56	CALL_FUNCTION_1   None
59	CALL_FUNCTION_1   None
62	POP_TOP           None
63	JUMP_BACK         '34'
66	POP_BLOCK         None
67_0	COME_FROM         '27'
67	JUMP_FORWARD      '70'
70_0	COME_FROM         '67'

70	LOAD_FAST         'scale'
73	LOAD_CONST        None
76	COMPARE_OP        'is not'
79	JUMP_IF_FALSE     '170'

82	SETUP_LOOP        '170'
85	LOAD_GLOBAL       'xrange'
88	LOAD_GLOBAL       'len'
91	LOAD_FAST         'countList'
94	CALL_FUNCTION_1   None
97	CALL_FUNCTION_1   None
100	GET_ITER          None
101	FOR_ITER          '166'
104	STORE_FAST        'i'

107	LOAD_CONST        None
110	YIELD_VALUE       None

111	LOAD_FAST         'countList'
114	LOAD_FAST         'i'
117	BINARY_SUBSCR     None
118	LOAD_CONST        0
121	COMPARE_OP        '>'
124	JUMP_IF_FALSE     '163'

127	LOAD_GLOBAL       'max'
130	LOAD_CONST        1
133	LOAD_GLOBAL       'int'
136	LOAD_FAST         'countList'
139	LOAD_FAST         'i'
142	BINARY_SUBSCR     None
143	LOAD_FAST         'scale'
146	BINARY_MULTIPLY   None
147	CALL_FUNCTION_1   None
150	CALL_FUNCTION_2   None
153	LOAD_FAST         'countList'
156	LOAD_FAST         'i'
159	STORE_SUBSCR      None
160	JUMP_BACK         '101'
163	JUMP_BACK         '101'
166	POP_BLOCK         None
167_0	COME_FROM         '82'
167	JUMP_FORWARD      '170'
170_0	COME_FROM         '167'

170	BUILD_MAP         None
173	STORE_FAST        'index2objectAndCount'

176	SETUP_LOOP        '233'
179	LOAD_GLOBAL       'xrange'
182	LOAD_GLOBAL       'len'
185	LOAD_FAST         'countList'
188	CALL_FUNCTION_1   None
191	CALL_FUNCTION_1   None
194	GET_ITER          None
195	FOR_ITER          '232'
198	STORE_FAST        'i'

201	LOAD_CONST        None
204	YIELD_VALUE       None

205	LOAD_FAST         'objects'
208	LOAD_FAST         'i'
211	BINARY_SUBSCR     None
212	LOAD_FAST         'countList'
215	LOAD_FAST         'i'
218	BINARY_SUBSCR     None
219	BUILD_LIST_2      None
222	LOAD_FAST         'index2objectAndCount'
225	LOAD_FAST         'i'
228	STORE_SUBSCR      None
229	JUMP_BACK         '195'
232	POP_BLOCK         None
233_0	COME_FROM         '176'

233	LOAD_FAST         'flywheel'
236	LOAD_FAST         'index2objectAndCount'
239	CALL_FUNCTION_1   None
242	YIELD_VALUE       None
243	LOAD_CONST        None
246	RETURN_VALUE      None

Syntax error at or near `POP_TOP' token at offset 62


def flywheel(*args, **kArgs):
    for flywheel in makeFlywheelGen(*args, **kArgs):
        pass

    return flywheel


def quickProfile(name = 'unnamed'):
    import pstats

    def profileDecorator(f):
        if not config.GetBool('use-profiler', 0):
            return f

        def _profiled(*args, **kArgs):
            if not config.GetBool('profile-debug', 0):
                st = globalClock.getRealTime()
                f(*args, **kArgs)
                s = globalClock.getRealTime() - st
                print 'Function %s.%s took %s seconds' % (f.__module__, f.__name__, s)
            else:
                import profile as prof, pstats
                if not hasattr(base, 'stats'):
                    base.stats = {}
                if not base.stats.get(name):
                    base.stats[name] = []
                prof.runctx('f(*args, **kArgs)', {'f': f,
                 'args': args,
                 'kArgs': kArgs}, None, 't.prof')
                s = pstats.Stats('t.prof')
                s.strip_dirs()
                s.sort_stats('cumulative')
                base.stats[name].append(s)
            return

        _profiled.__doc__ = f.__doc__
        return _profiled

    return profileDecorator


def getTotalAnnounceTime():
    td = 0
    for objs in base.stats.values():
        for stat in objs:
            td += getAnnounceGenerateTime(stat)

    return td


def getAnnounceGenerateTime(stat):
    val = 0
    stats = stat.stats
    for i in stats.keys():
        if i[2] == 'announceGenerate':
            newVal = stats[i][3]
            if newVal > val:
                val = newVal

    return val


def choice(condition, ifTrue, ifFalse):
    if condition:
        return ifTrue
    else:
        return ifFalse


class MiniLog():
    __module__ = __name__

    def __init__(self, name):
        self.indent = 1
        self.name = name
        self.lines = []

    def __str__(self):
        return '%s\nMiniLog: %s\n%s\n%s\n%s' % ('*' * 50,
         self.name,
         '-' * 50,
         '\n'.join(self.lines),
         '*' * 50)

    def enterFunction(self, funcName, *args, **kw):
        rArgs = [ repr(x) + ', ' for x in args ] + [ x + ' = ' + '%s, ' % repr(y) for x, y in kw.items() ]
        if not rArgs:
            rArgs = '()'
        else:
            rArgs = '(' + reduce(str.__add__, rArgs)[:-2] + ')'
        line = '%s%s' % (funcName, rArgs)
        self.appendFunctionCall(line)
        self.indent += 1
        return line

    def exitFunction(self):
        self.indent -= 1
        return self.indent

    def appendFunctionCall(self, line):
        self.lines.append(' ' * (self.indent * 2) + line)
        return line

    def appendLine(self, line):
        self.lines.append(' ' * (self.indent * 2) + '<< ' + line + ' >>')
        return line

    def flush(self):
        outStr = str(self)
        self.indent = 0
        self.lines = []
        return outStr


class MiniLogSentry():
    __module__ = __name__

    def __init__(self, log, funcName, *args, **kw):
        self.log = log
        if self.log:
            self.log.enterFunction(funcName, *args, **kw)

    def __del__(self):
        if self.log:
            self.log.exitFunction()
        del self.log


def logBlock(id, msg):
    print '<< LOGBLOCK(%03d)' % id
    print str(msg)
    print '/LOGBLOCK(%03d) >>' % id


class HierarchyException(Exception):
    __module__ = __name__
    JOSWILSO = 0

    def __init__(self, owner, description):
        self.owner = owner
        self.desc = description

    def __str__(self):
        return '(%s): %s' % (self.owner, self.desc)

    def __repr__(self):
        return 'HierarchyException(%s)' % (self.owner,)


def recordFunctorCreationStacks():
    global Functor
    from pandac.PandaModules import getConfigShowbase
    config = getConfigShowbase()
    if __dev__ and config.GetBool('record-functor-creation-stacks', 0):
        if not hasattr(Functor, '_functorCreationStacksRecorded'):
            Functor = recordCreationStackStr(Functor)
            Functor._functorCreationStacksRecorded = True
            Functor.__call__ = Functor._exceptionLoggedCreationStack__call__


def formatTimeCompact(seconds):
    result = ''
    a = int(seconds)
    seconds = a % 60
    a //= 60
    if a > 0:
        minutes = a % 60
        a //= 60
        if a > 0:
            hours = a % 24
            a //= 24
            if a > 0:
                days = a
                result += '%sd' % days
            result += '%sh' % hours
        result += '%sm' % minutes
    result += '%ss' % seconds
    return result


def formatTimeExact(seconds):
    result = ''
    a = int(seconds)
    seconds = a % 60
    a //= 60
    if a > 0:
        minutes = a % 60
        a //= 60
        if a > 0:
            hours = a % 24
            a //= 24
            if a > 0:
                days = a
                result += '%sd' % days
            if hours or minutes or seconds:
                result += '%sh' % hours
        if minutes or seconds:
            result += '%sm' % minutes
    if seconds or result == '':
        result += '%ss' % seconds
    return result


class AlphabetCounter():
    __module__ = __name__

    def __init__(self):
        self._curCounter = ['A']

    def next(self):
        result = ''.join([ c for c in self._curCounter ])
        index = -1
        while True:
            curChar = self._curCounter[index]
            if curChar is 'Z':
                nextChar = 'A'
                carry = True
            else:
                nextChar = chr(ord(self._curCounter[index]) + 1)
                carry = False
            self._curCounter[index] = nextChar
            if carry:
                if -index == len(self._curCounter):
                    self._curCounter = ['A'] + self._curCounter
                    break
                else:
                    index -= 1
                carry = False
            else:
                break

        return result


globalPdb = None
traceCalled = False

def setupPdb():
    global globalPdb
    import pdb

    class pandaPdb(pdb.Pdb):
        __module__ = __name__

        def stop_here(self, frame):
            global traceCalled
            if traceCalled:
                result = pdb.Pdb.stop_here(self, frame)
                if result == True:
                    traceCalled = False
                return result
            if frame is self.stopframe:
                return True
            return False

    globalPdb = pandaPdb()
    globalPdb.reset()
    sys.settrace(globalPdb.trace_dispatch)


def pandaTrace():
    global traceCalled
    if __dev__:
        if not globalPdb:
            setupPdb()
        globalPdb.set_trace(sys._getframe().f_back)
        traceCalled = True


packageMap = {'toontown': '$TOONTOWN',
 'direct': '$DIRECT',
 'otp': '$OTP',
 'pirates': '$PIRATES'}

def pandaBreak(dotpath, linenum, temporary = 0, cond = None):
    if __dev__:
        from pandac.PandaModules import Filename
        if not globalPdb:
            setupPdb()
        dirs = dotpath.split('.')
        root = Filename.expandFrom(packageMap[dirs[0]]).toOsSpecific()
        filename = root + '\\src'
        for d in dirs[1:]:
            filename = '%s\\%s' % (filename, d)

        print filename
        globalPdb.set_break(filename + '.py', linenum, temporary, cond)


class Default():
    __module__ = __name__


superLogFile = None

def startSuperLog(customFunction = None):
    global superLogFile
    if not superLogFile:
        superLogFile = open('c:\\temp\\superLog.txt', 'w')

        def trace_dispatch(a, b, c):
            if b == 'call' and a.f_code.co_name != '?' and a.f_code.co_name.find('safeRepr') < 0:
                vars = dict(a.f_locals)
                if 'self' in vars:
                    del vars['self']
                if '__builtins__' in vars:
                    del vars['__builtins__']
                for i in vars:
                    vars[i] = safeReprTypeOnFail(vars[i])

                if customFunction:
                    superLogFile.write('before = %s\n' % customFunction())
                superLogFile.write('%s(%s):%s:%s\n' % (a.f_code.co_filename.split('\\')[-1],
                 a.f_code.co_firstlineno,
                 a.f_code.co_name,
                 vars))
                if customFunction:
                    superLogFile.write('after = %s\n' % customFunction())
                return trace_dispatch

        sys.settrace(trace_dispatch)


def endSuperLog():
    global superLogFile
    if superLogFile:
        sys.settrace(None)
        superLogFile.close()
        superLogFile = None
    return


def isInteger(n):
    return type(n) in (types.IntType, types.LongType)


def configIsToday(configName):
    today = time.localtime()
    confStr = config.GetString(configName, '')
    for format in ('%m/%d/%Y', '%m-%d-%Y', '%m.%d.%Y'):
        try:
            confDate = time.strptime(confStr, format)
        except ValueError:
            pass
        else:
            if confDate.tm_year == today.tm_year and confDate.tm_mon == today.tm_mon and confDate.tm_mday == today.tm_mday:
                return True

    return False


def typeName(o):
    if hasattr(o, '__class__'):
        return o.__class__.__name__
    else:
        return o.__name__


def safeTypeName(o):
    try:
        return typeName(o)
    except:
        pass

    try:
        return type(o)
    except:
        pass

    return '<failed safeTypeName()>'


def histogramDict(l):
    d = {}
    for e in l:
        d.setdefault(e, 0)
        d[e] += 1

    return d


def unescapeHtmlString(s):
    result = ''
    i = 0
    while i < len(s):
        char = s[i]
        if char == '+':
            char = ' '
        elif char == '%':
            if i < len(s) - 2:
                num = eval('0x' + s[i + 1:i + 3])
                char = chr(num)
                i += 2
        i += 1
        result += char

    return result


class HTMLStringToElements(HTMLParser):
    __module__ = __name__

    def __init__(self, str, *a, **kw):
        self._elements = []
        self._elementStack = Stack()
        HTMLParser.__init__(self, *a, **kw)
        self.feed(str)
        self.close()

    def getElements(self):
        return self._elements

    def _handleNewElement(self, element):
        if len(self._elementStack):
            self._elementStack.top().append(element)
        else:
            self._elements.append(element)
        self._elementStack.push(element)

    def handle_starttag(self, tag, attrs):
        kwArgs = {}
        for name, value in attrs:
            kwArgs[name] = value

        el = ET.Element(tag, **kwArgs)
        self._handleNewElement(el)

    def handle_data(self, data):
        if len(self._elementStack):
            self._elementStack.top().text = data

    def handle_endtag(self, tag):
        top = self._elementStack.top()
        if len(top.getchildren()) == 0:
            if top.tag == 'script' and top.get('type') == 'text/javascript':
                if top.text == None:
                    top.text = '// force tag closer'
            else:
                self.handle_comment('force tag closer')
                self._elementStack.pop()
        self._elementStack.pop()
        return

    def handle_comment(self, data):
        comment = ET.Comment(data)
        self._handleNewElement(comment)


def str2elements(str):
    return HTMLStringToElements(str).getElements()


def repeatableRepr(obj):
    if type(obj) is types.DictType:
        keys = obj.keys()
        keys.sort()
        s = '{'
        for i in xrange(len(keys)):
            key = keys[i]
            s += repeatableRepr(key)
            s += ': '
            s += repeatableRepr(obj[key])
            if i < len(keys) - 1:
                s += ', '

        s += '}'
        return s
    elif type(obj) is type(set()):
        l = []
        for item in obj:
            l.append(item)

        l.sort()
        return repeatableRepr(l)
    return repr(obj)


bpdb = BpDb.BpDb()

def bpdbGetEnabled():
    enabled = True
    try:
        enabled = __dev__
        enabled = ConfigVariableBool('force-breakpoints', enabled).getValue()
    finally:
        return enabled


bpdb.setEnabledCallback(bpdbGetEnabled)
bpdb.setConfigCallback(lambda cfg: ConfigVariableBool('want-bp-%s' % (cfg.lower(),), 0).getValue())

def u2ascii(s):
    if type(s) is types.UnicodeType:
        return unicodedata.normalize('NFKD', s).encode('ascii', 'backslashreplace')
    else:
        return str(s)


def unicodeUtf8(s):
    if type(s) is types.UnicodeType:
        return s
    else:
        return unicode(str(s), 'utf-8')


def encodedUtf8(s):
    return unicodeUtf8(s).encode('utf-8')


class PriorityCallbacks():
    __module__ = __name__
    TokenGen = SerialNumGen()

    @classmethod
    def GetToken(cls):
        return 'pc-%s' % cls.TokenGen.next()

    def __init__(self):
        self._callbacks = []
        self._token2item = {}

    def clear(self):
        while self._callbacks:
            self._callbacks.pop()

        self._token2item = {}

    def add(self, callback, priority = None):
        if priority is None:
            priority = 0
        item = (priority, callback)
        bisect.insort(self._callbacks, item)
        token = self.GetToken()
        self._token2item[token] = item
        return token

    def remove(self, token):
        item = self._token2item[token]
        self._callbacks.pop(bisect.bisect_left(self._callbacks, item))

    def __contains__(self, token):
        return token in self._token2item

    def __call__(self):
        callbacks = self._callbacks[:]
        for priority, callback in callbacks:
            callback()


def quantize(value, divisor):
    return float(int(value * int(divisor))) / int(divisor)


def quantizeVec(vec, divisor):
    vec[0] = quantize(vec[0], divisor)
    vec[1] = quantize(vec[1], divisor)
    vec[2] = quantize(vec[2], divisor)


def isClient():
    if hasattr(__builtin__, 'simbase') and not hasattr(__builtin__, 'base'):
        return False
    return True


import __builtin__
__builtin__.Functor = Functor
__builtin__.Stack = Stack
__builtin__.Queue = Queue
__builtin__.Enum = Enum
__builtin__.SerialNumGen = SerialNumGen
__builtin__.SerialMaskedGen = SerialMaskedGen
__builtin__.ScratchPad = ScratchPad
__builtin__.DestructiveScratchPad = DestructiveScratchPad
__builtin__.uniqueName = uniqueName
__builtin__.serialNum = serialNum
__builtin__.profiled = profiled
__builtin__.set_trace = set_trace
__builtin__.setTrace = setTrace
__builtin__.pm = pm
__builtin__.itype = itype
__builtin__.exceptionLogged = exceptionLogged
__builtin__.appendStr = appendStr
__builtin__.bound = bound
__builtin__.clamp = clamp
__builtin__.lerp = lerp
__builtin__.clerp = clerp
__builtin__.triglerp = triglerp
__builtin__.notNone = notNone
__builtin__.clampScalar = clampScalar
__builtin__.makeList = makeList
__builtin__.makeTuple = makeTuple
__builtin__.printStack = printStack
__builtin__.printReverseStack = printReverseStack
__builtin__.printVerboseStack = printVerboseStack
__builtin__.DelayedCall = DelayedCall
__builtin__.DelayedFunctor = DelayedFunctor
__builtin__.FrameDelayedCall = FrameDelayedCall
__builtin__.SubframeCall = SubframeCall
__builtin__.ArgumentEater = ArgumentEater
__builtin__.ClassTree = ClassTree
__builtin__.invertDict = invertDict
__builtin__.invertDictLossless = invertDictLossless
__builtin__.getBase = getBase
__builtin__.getRepository = getRepository
__builtin__.safeRepr = safeRepr
__builtin__.fastRepr = fastRepr
__builtin__.nullGen = nullGen
__builtin__.flywheel = flywheel
__builtin__.loopGen = loopGen
__builtin__.StackTrace = StackTrace
__builtin__.choice = choice
__builtin__.report = report
__builtin__.pstatcollect = pstatcollect
__builtin__.MiniLog = MiniLog
__builtin__.MiniLogSentry = MiniLogSentry
__builtin__.logBlock = logBlock
__builtin__.HierarchyException = HierarchyException
__builtin__.pdir = pdir
__builtin__.deeptype = deeptype
__builtin__.Default = Default
__builtin__.isInteger = isInteger
__builtin__.configIsToday = configIsToday
__builtin__.typeName = typeName
__builtin__.safeTypeName = safeTypeName
__builtin__.histogramDict = histogramDict
__builtin__.repeatableRepr = repeatableRepr
__builtin__.bpdb = bpdb
__builtin__.u2ascii = u2ascii
__builtin__.unicodeUtf8 = unicodeUtf8
__builtin__.encodedUtf8 = encodedUtf8
__builtin__.isClient = isClient# decompiled 0 files: 0 okay, 1 failed, 0 verify failed
# 2013.08.22 22:14:45 Pacific Daylight Time

# Can't uncompyle C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\showbase\PythonUtil.pyc
Traceback (most recent call last):
  File "C:\python27\lib\uncompyle2\__init__.py", line 206, in main
    uncompyle_file(infile, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 143, in uncompyle_file
    uncompyle(version, co, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 132, in uncompyle
    raise walk.ERROR
ParserError: --- This code section failed: ---

0	LOAD_CONST        '<code_object flywheel>'
3	MAKE_FUNCTION_0   None
6	STORE_FAST        'flywheel'

9	LOAD_FAST         'countList'
12	LOAD_CONST        None
15	COMPARE_OP        'is'
18	JUMP_IF_FALSE     '70'

21	BUILD_LIST_0      None
24	STORE_FAST        'countList'

27	SETUP_LOOP        '70'
30	LOAD_FAST         'objects'
33	GET_ITER          None
34	FOR_ITER          '66'
37	STORE_FAST        'object'

40	LOAD_CONST        None
43	YIELD_VALUE       None

44	LOAD_FAST         'countList'
47	LOAD_ATTR         'append'
50	LOAD_FAST         'countFunc'
53	LOAD_FAST         'object'
56	CALL_FUNCTION_1   None
59	CALL_FUNCTION_1   None
62	POP_TOP           None
63	JUMP_BACK         '34'
66	POP_BLOCK         None
67_0	COME_FROM         '27'
67	JUMP_FORWARD      '70'
70_0	COME_FROM         '67'

70	LOAD_FAST         'scale'
73	LOAD_CONST        None
76	COMPARE_OP        'is not'
79	JUMP_IF_FALSE     '170'

82	SETUP_LOOP        '170'
85	LOAD_GLOBAL       'xrange'
88	LOAD_GLOBAL       'len'
91	LOAD_FAST         'countList'
94	CALL_FUNCTION_1   None
97	CALL_FUNCTION_1   None
100	GET_ITER          None
101	FOR_ITER          '166'
104	STORE_FAST        'i'

107	LOAD_CONST        None
110	YIELD_VALUE       None

111	LOAD_FAST         'countList'
114	LOAD_FAST         'i'
117	BINARY_SUBSCR     None
118	LOAD_CONST        0
121	COMPARE_OP        '>'
124	JUMP_IF_FALSE     '163'

127	LOAD_GLOBAL       'max'
130	LOAD_CONST        1
133	LOAD_GLOBAL       'int'
136	LOAD_FAST         'countList'
139	LOAD_FAST         'i'
142	BINARY_SUBSCR     None
143	LOAD_FAST         'scale'
146	BINARY_MULTIPLY   None
147	CALL_FUNCTION_1   None
150	CALL_FUNCTION_2   None
153	LOAD_FAST         'countList'
156	LOAD_FAST         'i'
159	STORE_SUBSCR      None
160	JUMP_BACK         '101'
163	JUMP_BACK         '101'
166	POP_BLOCK         None
167_0	COME_FROM         '82'
167	JUMP_FORWARD      '170'
170_0	COME_FROM         '167'

170	BUILD_MAP         None
173	STORE_FAST        'index2objectAndCount'

176	SETUP_LOOP        '233'
179	LOAD_GLOBAL       'xrange'
182	LOAD_GLOBAL       'len'
185	LOAD_FAST         'countList'
188	CALL_FUNCTION_1   None
191	CALL_FUNCTION_1   None
194	GET_ITER          None
195	FOR_ITER          '232'
198	STORE_FAST        'i'

201	LOAD_CONST        None
204	YIELD_VALUE       None

205	LOAD_FAST         'objects'
208	LOAD_FAST         'i'
211	BINARY_SUBSCR     None
212	LOAD_FAST         'countList'
215	LOAD_FAST         'i'
218	BINARY_SUBSCR     None
219	BUILD_LIST_2      None
222	LOAD_FAST         'index2objectAndCount'
225	LOAD_FAST         'i'
228	STORE_SUBSCR      None
229	JUMP_BACK         '195'
232	POP_BLOCK         None
233_0	COME_FROM         '176'

233	LOAD_FAST         'flywheel'
236	LOAD_FAST         'index2objectAndCount'
239	CALL_FUNCTION_1   None
242	YIELD_VALUE       None
243	LOAD_CONST        None
246	RETURN_VALUE      None

Syntax error at or near `POP_TOP' token at offset 62

