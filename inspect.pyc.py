# 2013.08.22 22:13:07 Pacific Daylight Time
# Embedded file name: inspect
__author__ = 'Ka-Ping Yee <ping@lfw.org>'
__date__ = '1 Jan 2001'
import sys, os, types, string, re, dis, imp, tokenize, linecache

def ismodule(object):
    return isinstance(object, types.ModuleType)


def isclass(object):
    return isinstance(object, types.ClassType) or hasattr(object, '__bases__')


def ismethod(object):
    return isinstance(object, types.MethodType)


def ismethoddescriptor(object):
    return hasattr(object, '__get__') and not hasattr(object, '__set__') and not ismethod(object) and not isfunction(object) and not isclass(object)


def isdatadescriptor(object):
    return hasattr(object, '__set__') and hasattr(object, '__get__')


def isfunction(object):
    return isinstance(object, types.FunctionType)


def istraceback(object):
    return isinstance(object, types.TracebackType)


def isframe(object):
    return isinstance(object, types.FrameType)


def iscode(object):
    return isinstance(object, types.CodeType)


def isbuiltin(object):
    return isinstance(object, types.BuiltinFunctionType)


def isroutine(object):
    return isbuiltin(object) or isfunction(object) or ismethod(object) or ismethoddescriptor(object)


def getmembers(object, predicate = None):
    results = []
    for key in dir(object):
        value = getattr(object, key)
        if not predicate or predicate(value):
            results.append((key, value))

    results.sort()
    return results


def classify_class_attrs(cls):
    mro = getmro(cls)
    names = dir(cls)
    result = []
    for name in names:
        if name in cls.__dict__:
            obj = cls.__dict__[name]
        else:
            obj = getattr(cls, name)
        homecls = getattr(obj, '__objclass__', None)
        if homecls is None:
            for base in mro:
                if name in base.__dict__:
                    homecls = base
                    break

        if homecls is not None and name in homecls.__dict__:
            obj = homecls.__dict__[name]
        obj_via_getattr = getattr(cls, name)
        if isinstance(obj, staticmethod):
            kind = 'static method'
        elif isinstance(obj, classmethod):
            kind = 'class method'
        elif isinstance(obj, property):
            kind = 'property'
        elif ismethod(obj_via_getattr) or ismethoddescriptor(obj_via_getattr):
            kind = 'method'
        else:
            kind = 'data'
        result.append((name,
         kind,
         homecls,
         obj))

    return result


def _searchbases(cls, accum):
    if cls in accum:
        return
    accum.append(cls)
    for base in cls.__bases__:
        _searchbases(base, accum)


def getmro(cls):
    if hasattr(cls, '__mro__'):
        return cls.__mro__
    else:
        result = []
        _searchbases(cls, result)
        return tuple(result)


def indentsize(line):
    expline = string.expandtabs(line)
    return len(expline) - len(string.lstrip(expline))


def getdoc(object):
    try:
        doc = object.__doc__
    except AttributeError:
        return None

    if not isinstance(doc, types.StringTypes):
        return None
    try:
        lines = string.split(string.expandtabs(doc), '\n')
    except UnicodeError:
        return None
    else:
        margin = sys.maxint
        for line in lines[1:]:
            content = len(string.lstrip(line))
            if content:
                indent = len(line) - content
                margin = min(margin, indent)

        if lines:
            lines[0] = lines[0].lstrip()
        if margin < sys.maxint:
            for i in range(1, len(lines)):
                lines[i] = lines[i][margin:]

        while lines and not lines[-1]:
            lines.pop()

        while lines and not lines[0]:
            lines.pop(0)

        return string.join(lines, '\n')

    return None


def getfile(object):
    if ismodule(object):
        if hasattr(object, '__file__'):
            return object.__file__
        raise TypeError('arg is a built-in module')
    if isclass(object):
        object = sys.modules.get(object.__module__)
        if hasattr(object, '__file__'):
            return object.__file__
        raise TypeError('arg is a built-in class')
    if ismethod(object):
        object = object.im_func
    if isfunction(object):
        object = object.func_code
    if istraceback(object):
        object = object.tb_frame
    if isframe(object):
        object = object.f_code
    if iscode(object):
        return object.co_filename
    raise TypeError('arg is not a module, class, method, function, traceback, frame, or code object')


def getmoduleinfo(path):
    filename = os.path.basename(path)
    suffixes = map(lambda (suffix, mode, mtype): (-len(suffix),
     suffix,
     mode,
     mtype), imp.get_suffixes())
    suffixes.sort()
    for neglen, suffix, mode, mtype in suffixes:
        if filename[neglen:] == suffix:
            return (filename[:neglen],
             suffix,
             mode,
             mtype)


def getmodulename(path):
    info = getmoduleinfo(path)
    if info:
        return info[0]


def getsourcefile(object):
    filename = getfile(object)
    if string.lower(filename[-4:]) in ['.pyc', '.pyo']:
        filename = filename[:-4] + '.py'
    for suffix, mode, kind in imp.get_suffixes():
        if 'b' in mode and string.lower(filename[-len(suffix):]) == suffix:
            return None

    if os.path.exists(filename):
        return filename
    return None


def getabsfile(object):
    return os.path.normcase(os.path.abspath(getsourcefile(object) or getfile(object)))


modulesbyfile = {}

def getmodule(object):
    if ismodule(object):
        return object
    if hasattr(object, '__module__'):
        return sys.modules.get(object.__module__)
    try:
        file = getabsfile(object)
    except TypeError:
        return None

    if file in modulesbyfile:
        return sys.modules.get(modulesbyfile[file])
    for module in sys.modules.values():
        if hasattr(module, '__file__'):
            modulesbyfile[os.path.realpath(getabsfile(module))] = module.__name__

    if file in modulesbyfile:
        return sys.modules.get(modulesbyfile[file])
    main = sys.modules['__main__']
    if not hasattr(object, '__name__'):
        return None
    if hasattr(main, object.__name__):
        mainobject = getattr(main, object.__name__)
        if mainobject is object:
            return main
    builtin = sys.modules['__builtin__']
    if hasattr(builtin, object.__name__):
        builtinobject = getattr(builtin, object.__name__)
        if builtinobject is object:
            return builtin
    return None


def findsource(object):
    if not getsourcefile(object):
        file = getfile(object)
        lines = linecache.getlines(file)
        if not lines:
            raise IOError('could not get source code')
        if ismodule(object):
            return (lines, 0)
        if isclass(object):
            name = object.__name__
            pat = re.compile('^\\s*class\\s*' + name + '\\b')
            for i in range(len(lines)):
                if pat.match(lines[i]):
                    return (lines, i)
            else:
                raise IOError('could not find class definition')

        if ismethod(object):
            object = object.im_func
        if isfunction(object):
            object = object.func_code
        if istraceback(object):
            object = object.tb_frame
        if isframe(object):
            object = object.f_code
        if iscode(object):
            raise hasattr(object, 'co_firstlineno') or IOError('could not find function definition')
        lnum = object.co_firstlineno - 1
        pat = re.compile('^(\\s*def\\s)|(.*(?<!\\w)lambda(:|\\s))|^(\\s*@)')
        while lnum > 0:
            if pat.match(lines[lnum]):
                break
            lnum = lnum - 1

        return (lines, lnum)
    raise IOError('could not find code object')


def getcomments(object):
    try:
        lines, lnum = findsource(object)
    except (IOError, TypeError):
        return None

    if ismodule(object):
        start = 0
        if lines and lines[0][:2] == '#!':
            start = 1
        while start < len(lines) and string.strip(lines[start]) in ['', '#']:
            start = start + 1

        if start < len(lines) and lines[start][:1] == '#':
            comments = []
            end = start
            while end < len(lines) and lines[end][:1] == '#':
                comments.append(string.expandtabs(lines[end]))
                end = end + 1

            return string.join(comments, '')
    elif lnum > 0:
        indent = indentsize(lines[lnum])
        end = lnum - 1
        if end >= 0 and string.lstrip(lines[end])[:1] == '#' and indentsize(lines[end]) == indent:
            comments = [string.lstrip(string.expandtabs(lines[end]))]
            if end > 0:
                end = end - 1
                comment = string.lstrip(string.expandtabs(lines[end]))
                while comment[:1] == '#' and indentsize(lines[end]) == indent:
                    comments[:0] = [comment]
                    end = end - 1
                    if end < 0:
                        break
                    comment = string.lstrip(string.expandtabs(lines[end]))

            while comments and string.strip(comments[0]) == '#':
                comments[:1] = []

            while comments and string.strip(comments[-1]) == '#':
                comments[-1:] = []

            return string.join(comments, '')
    return None


class ListReader():
    __module__ = __name__

    def __init__(self, lines):
        self.lines = lines
        self.index = 0

    def readline(self):
        i = self.index
        if i < len(self.lines):
            self.index = i + 1
            return self.lines[i]
        else:
            return ''


class EndOfBlock(Exception):
    __module__ = __name__


class BlockFinder():
    __module__ = __name__

    def __init__(self):
        self.indent = 0
        self.islambda = False
        self.started = False
        self.passline = False
        self.last = 0

    def tokeneater(self, type, token, (srow, scol), (erow, ecol), line):
        if not self.started:
            if token in ('def', 'class', 'lambda'):
                if token == 'lambda':
                    self.islambda = True
                self.started = True
            self.passline = True
        elif type == tokenize.NEWLINE:
            self.passline = False
            self.last = srow
        elif self.passline:
            pass
        elif self.islambda:
            raise EndOfBlock, self.last
        elif type == tokenize.INDENT:
            self.indent = self.indent + 1
            self.passline = True
        elif type == tokenize.DEDENT:
            self.indent = self.indent - 1
            if self.indent == 0:
                raise EndOfBlock, self.last
        elif type == tokenize.NAME and scol == 0:
            raise EndOfBlock, self.last


def getblock(lines):
    try:
        tokenize.tokenize(ListReader(lines).readline, BlockFinder().tokeneater)
    except EndOfBlock as eob:
        return lines[:eob.args[0]]

    return lines[:1]


def getsourcelines(object):
    lines, lnum = findsource(object)
    if ismodule(object):
        return (lines, 0)
    else:
        return (getblock(lines[lnum:]), lnum + 1)


def getsource(object):
    lines, lnum = getsourcelines(object)
    return string.join(lines, '')


def walktree(classes, children, parent):
    results = []
    classes.sort(key=lambda c: (c.__module__, c.__name__))
    for c in classes:
        results.append((c, c.__bases__))
        if c in children:
            results.append(walktree(children[c], children, c))

    return results


def getclasstree(classes, unique = 0):
    children = {}
    roots = []
    for c in classes:
        if c.__bases__:
            for parent in c.__bases__:
                if parent not in children:
                    children[parent] = []
                children[parent].append(c)
                if unique and parent in classes:
                    break

        elif c not in roots:
            roots.append(c)

    for parent in children:
        if parent not in classes:
            roots.append(parent)

    return walktree(roots, children, None)


CO_OPTIMIZED, CO_NEWLOCALS, CO_VARARGS, CO_VARKEYWORDS = (1, 2, 4, 8)

def getargs(co):
    if not iscode(co):
        raise TypeError('arg is not a code object')
    code = co.co_code
    nargs = co.co_argcount
    names = co.co_varnames
    args = list(names[:nargs])
    step = 0
    for i in range(nargs):
        if args[i][:1] in ['', '.']:
            stack, remain, count = [], [], []
            while step < len(code):
                op = ord(code[step])
                step = step + 1
                if op >= dis.HAVE_ARGUMENT:
                    opname = dis.opname[op]
                    value = ord(code[step]) + ord(code[step + 1]) * 256
                    step = step + 2
                    if opname in ['UNPACK_TUPLE', 'UNPACK_SEQUENCE']:
                        remain.append(value)
                        count.append(value)
                    elif opname == 'STORE_FAST':
                        stack.append(names[value])
                        if not remain:
                            stack[0] = [stack[0]]
                            break
                        else:
                            remain[-1] = remain[-1] - 1
                            while remain[-1] == 0:
                                remain.pop()
                                size = count.pop()
                                stack[-size:] = [stack[-size:]]
                                if not remain:
                                    break
                                remain[-1] = remain[-1] - 1

                            if not remain:
                                break

            args[i] = stack[0]

    varargs = None
    if co.co_flags & CO_VARARGS:
        varargs = co.co_varnames[nargs]
        nargs = nargs + 1
    varkw = None
    if co.co_flags & CO_VARKEYWORDS:
        varkw = co.co_varnames[nargs]
    return (args, varargs, varkw)


def getargspec(func):
    if ismethod(func):
        func = func.im_func
    if not isfunction(func):
        raise TypeError('arg is not a Python function')
    args, varargs, varkw = getargs(func.func_code)
    return (args,
     varargs,
     varkw,
     func.func_defaults)


def getargvalues(frame):
    args, varargs, varkw = getargs(frame.f_code)
    return (args,
     varargs,
     varkw,
     frame.f_locals)


def joinseq(seq):
    if len(seq) == 1:
        return '(' + seq[0] + ',)'
    else:
        return '(' + string.join(seq, ', ') + ')'


def strseq(object, convert, join = joinseq):
    if type(object) in [types.ListType, types.TupleType]:
        return join(map(lambda o, c = convert, j = join: strseq(o, c, j), object))
    else:
        return convert(object)


def formatargspec(args, varargs = None, varkw = None, defaults = None, formatarg = str, formatvarargs = lambda name: '*' + name, formatvarkw = lambda name: '**' + name, formatvalue = lambda value: '=' + repr(value), join = joinseq):
    specs = []
    if defaults:
        firstdefault = len(args) - len(defaults)
    for i in range(len(args)):
        spec = strseq(args[i], formatarg, join)
        if defaults and i >= firstdefault:
            spec = spec + formatvalue(defaults[i - firstdefault])
        specs.append(spec)

    if varargs is not None:
        specs.append(formatvarargs(varargs))
    if varkw is not None:
        specs.append(formatvarkw(varkw))
    return '(' + string.join(specs, ', ') + ')'


def formatargvalues(args, varargs, varkw, locals, formatarg = str, formatvarargs = lambda name: '*' + name, formatvarkw = lambda name: '**' + name, formatvalue = lambda value: '=' + repr(value), join = joinseq):

    def convert(name, locals = locals, formatarg = formatarg, formatvalue = formatvalue):
        return formatarg(name) + formatvalue(locals[name])

    specs = []
    for i in range(len(args)):
        specs.append(strseq(args[i], convert, join))

    if varargs:
        specs.append(formatvarargs(varargs) + formatvalue(locals[varargs]))
    if varkw:
        specs.append(formatvarkw(varkw) + formatvalue(locals[varkw]))
    return '(' + string.join(specs, ', ') + ')'


def getframeinfo(frame, context = 1):
    if istraceback(frame):
        lineno = frame.tb_lineno
        frame = frame.tb_frame
    else:
        lineno = frame.f_lineno
    if not isframe(frame):
        raise TypeError('arg is not a frame or traceback object')
    if not getsourcefile(frame):
        filename = getfile(frame)
        start = context > 0 and lineno - 1 - context // 2
        try:
            lines, lnum = findsource(frame)
        except IOError:
            lines = index = None
        else:
            start = max(start, 1)
            start = max(0, min(start, len(lines) - context))
            lines = lines[start:start + context]
            index = lineno - 1 - start

    else:
        lines = index = None
    return (filename,
     lineno,
     frame.f_code.co_name,
     lines,
     index)


def getlineno(frame):
    return frame.f_lineno


def getouterframes(frame, context = 1):
    framelist = []
    while frame:
        framelist.append((frame,) + getframeinfo(frame, context))
        frame = frame.f_back

    return framelist


def getinnerframes(tb, context = 1):
    framelist = []
    while tb:
        framelist.append((tb.tb_frame,) + getframeinfo(tb, context))
        tb = tb.tb_next

    return framelist


currentframe = sys._getframe

def stack(context = 1):
    return getouterframes(sys._getframe(1), context)


def trace(context = 1):
    return getinnerframes(sys.exc_info()[2], context)
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\inspect.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:13:08 Pacific Daylight Time
