# 2013.08.22 22:13:19 Pacific Daylight Time
# Embedded file name: pydoc
__author__ = 'Ka-Ping Yee <ping@lfw.org>'
__date__ = '26 February 2001'
__version__ = '$Revision: 1.1.1.1 $'
__credits__ = 'Guido van Rossum, for an excellent programming language.\nTommy Burnette, the original creator of manpy.\nPaul Prescod, for all his work on onlinehelp.\nRichard Chamberlain, for the first implementation of textdoc.\n'
import sys, imp, os, re, types, inspect, __builtin__
from repr import Repr
from string import expandtabs, find, join, lower, split, strip, rfind, rstrip
from collections import deque

def pathdirs():
    dirs = []
    normdirs = []
    for dir in sys.path:
        dir = os.path.abspath(dir or '.')
        normdir = os.path.normcase(dir)
        if normdir not in normdirs and os.path.isdir(dir):
            dirs.append(dir)
            normdirs.append(normdir)

    return dirs


def getdoc(object):
    result = inspect.getdoc(object) or inspect.getcomments(object)
    return result and re.sub('^ *\n', '', rstrip(result)) or ''


def splitdoc(doc):
    lines = split(strip(doc), '\n')
    if len(lines) == 1:
        return (lines[0], '')
    elif len(lines) >= 2 and not rstrip(lines[1]):
        return (lines[0], join(lines[2:], '\n'))
    return ('', join(lines, '\n'))


def classname(object, modname):
    name = object.__name__
    if object.__module__ != modname:
        name = object.__module__ + '.' + name
    return name


def isdata(object):
    return inspect.ismodule(object) or inspect.isclass(object) or inspect.isroutine(object) or inspect.isframe(object) or inspect.istraceback(object) or not inspect.iscode(object)


def replace(text, *pairs):
    while pairs:
        text = join(split(text, pairs[0]), pairs[1])
        pairs = pairs[2:]

    return text


def cram(text, maxlen):
    if len(text) > maxlen:
        pre = max(0, (maxlen - 3) // 2)
        post = max(0, maxlen - 3 - pre)
        return text[:pre] + '...' + text[len(text) - post:]
    return text


_re_stripid = re.compile(' at 0x[0-9a-f]{6,16}(>+)$', re.IGNORECASE)

def stripid(text):
    if _re_stripid.search(repr(Exception)):
        return _re_stripid.sub('\\1', text)
    return text


def _is_some_method(obj):
    return inspect.ismethod(obj) or inspect.ismethoddescriptor(obj)


def allmethods(cl):
    methods = {}
    for key, value in inspect.getmembers(cl, _is_some_method):
        methods[key] = 1

    for base in cl.__bases__:
        methods.update(allmethods(base))

    for key in methods.keys():
        methods[key] = getattr(cl, key)

    return methods


def _split_list(s, predicate):
    yes = []
    no = []
    for x in s:
        if predicate(x):
            yes.append(x)
        else:
            no.append(x)

    return (yes, no)


def visiblename(name, all = None):
    if name in ['__builtins__',
     '__doc__',
     '__file__',
     '__path__',
     '__module__',
     '__name__']:
        return 0
    if name.startswith('__'):
        if name.endswith('__'):
            return 1
    if all is not None:
        return name in all
    else:
        return not name.startswith('_')
    return


def ispackage(path):
    if os.path.isdir(path):
        for ext in ['.py', '.pyc', '.pyo']:
            if os.path.isfile(os.path.join(path, '__init__' + ext)):
                return True

    return False


def synopsis(filename, cache = {}):
    mtime = os.stat(filename).st_mtime
    lastupdate, result = cache.get(filename, (0, None))
    if lastupdate < mtime:
        info = inspect.getmoduleinfo(filename)
        file = open(filename)
        if info and 'b' in info[2]:
            try:
                module = imp.load_module('__temp__', file, filename, info[1:])
            except:
                return

            result = split(module.__doc__ or '', '\n')[0]
            del sys.modules['__temp__']
        else:
            line = file.readline()
            while line[:1] == '#' or not strip(line):
                line = file.readline()
                if not line:
                    break

            line = strip(line)
            if line[:4] == 'r"""':
                line = line[1:]
            if line[:3] == '"""':
                line = line[3:]
                if line[-1:] == '\\':
                    line = line[:-1]
                while not strip(line):
                    line = file.readline()
                    if not line:
                        break

                result = strip(split(line, '"""')[0])
            else:
                result = None
        file.close()
        cache[filename] = (mtime, result)
    return result


class ErrorDuringImport(Exception):
    __module__ = __name__

    def __init__(self, filename, (exc, value, tb)):
        self.filename = filename
        self.exc = exc
        self.value = value
        self.tb = tb

    def __str__(self):
        exc = self.exc
        if type(exc) is types.ClassType:
            exc = exc.__name__
        return 'problem in %s - %s: %s' % (self.filename, exc, self.value)


def importfile(path):
    magic = imp.get_magic()
    file = open(path, 'r')
    if file.read(len(magic)) == magic:
        kind = imp.PY_COMPILED
    else:
        kind = imp.PY_SOURCE
    file.close()
    filename = os.path.basename(path)
    name, ext = os.path.splitext(filename)
    file = open(path, 'r')
    try:
        module = imp.load_module(name, file, path, (ext, 'r', kind))
    except:
        raise ErrorDuringImport(path, sys.exc_info())

    file.close()
    return module


def safeimport(path, forceload = 0, cache = {}):
    if forceload and path in sys.modules:
        if path not in sys.builtin_module_names:
            info = inspect.getmoduleinfo(sys.modules[path].__file__)
            if info[3] != imp.C_EXTENSION:
                cache[path] = sys.modules[path]
                del sys.modules[path]
    try:
        module = __import__(path)
    except:
        exc, value, tb = info = sys.exc_info()
        if path in sys.modules:
            raise ErrorDuringImport(sys.modules[path].__file__, info)
        elif exc is SyntaxError:
            raise ErrorDuringImport(value.filename, info)
        elif exc is ImportError and split(lower(str(value)))[:2] == ['no', 'module']:
            return None
        else:
            raise ErrorDuringImport(path, sys.exc_info())

    for part in split(path, '.')[1:]:
        try:
            module = getattr(module, part)
        except AttributeError:
            return None

    return module


class Doc():
    __module__ = __name__

    def document(self, object, name = None, *args):
        args = (object, name) + args
        try:
            if inspect.ismodule(object):
                return self.docmodule(*args)
            if inspect.isclass(object):
                return self.docclass(*args)
            if inspect.isroutine(object):
                return self.docroutine(*args)
        except AttributeError:
            pass

        if isinstance(object, property):
            return self.docproperty(*args)
        return self.docother(*args)

    def fail(self, object, name = None, *args):
        message = "don't know how to document object%s of type %s" % (name and (' ' + repr(name), type(object).__name__))
        raise TypeError, message

    docmodule = docclass = docroutine = docother = fail

    def getdocloc(self, object):
        try:
            file = inspect.getabsfile(object)
        except TypeError:
            file = '(built-in)'

        docloc = os.environ.get('PYTHONDOCS', 'http://www.python.org/doc/current/lib')
        basedir = os.path.join(sys.exec_prefix, 'lib', 'python' + sys.version[0:3])
        if isinstance(object, type(os)) and (object.__name__ in ('errno', 'exceptions', 'gc', 'imp', 'marshal', 'posix', 'signal', 'sys', 'thread', 'zipimport') or file.startswith(basedir) and not file.startswith(os.path.join(basedir, 'site-packages'))):
            htmlfile = 'module-%s.html' % object.__name__
            if docloc.startswith('http://'):
                docloc = '%s/%s' % (docloc.rstrip('/'), htmlfile)
            else:
                docloc = os.path.join(docloc, htmlfile)
        else:
            docloc = None
        return docloc


class HTMLRepr(Repr):
    __module__ = __name__

    def __init__(self):
        Repr.__init__(self)
        self.maxlist = self.maxtuple = 20
        self.maxdict = 10
        self.maxstring = self.maxother = 100

    def escape(self, text):
        return replace(text, '&', '&amp;', '<', '&lt;', '>', '&gt;')

    def repr(self, object):
        return Repr.repr(self, object)

    def repr1(self, x, level):
        if hasattr(type(x), '__name__'):
            methodname = 'repr_' + join(split(type(x).__name__), '_')
            if hasattr(self, methodname):
                return getattr(self, methodname)(x, level)
        return self.escape(cram(stripid(repr(x)), self.maxother))

    def repr_string(self, x, level):
        test = cram(x, self.maxstring)
        testrepr = repr(test)
        if '\\' in test and '\\' not in replace(testrepr, '\\\\', ''):
            return 'r' + testrepr[0] + self.escape(test) + testrepr[0]
        return re.sub('((\\\\[\\\\abfnrtv\\\'"]|\\\\[0-9]..|\\\\x..|\\\\u....)+)', '<font color="#c040c0">\\1</font>', self.escape(testrepr))

    repr_str = repr_string

    def repr_instance(self, x, level):
        try:
            return self.escape(cram(stripid(repr(x)), self.maxstring))
        except:
            return self.escape('<%s instance>' % x.__class__.__name__)

    repr_unicode = repr_string


class HTMLDoc(Doc):
    __module__ = __name__
    _repr_instance = HTMLRepr()
    repr = _repr_instance.repr
    escape = _repr_instance.escape

    def page(self, title, contents):
        return '\n<!doctype html PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">\n<html><head><title>Python: %s</title>\n</head><body bgcolor="#f0f0f8">\n%s\n</body></html>' % (title, contents)

    def heading(self, title, fgcol, bgcol, extras = ''):
        return '\n<table width="100%%" cellspacing=0 cellpadding=2 border=0 summary="heading">\n<tr bgcolor="%s">\n<td valign=bottom>&nbsp;<br>\n<font color="%s" face="helvetica, arial">&nbsp;<br>%s</font></td\n><td align=right valign=bottom\n><font color="%s" face="helvetica, arial">%s</font></td></tr></table>\n    ' % (bgcol,
         fgcol,
         title,
         fgcol,
         extras or '&nbsp;')

    def section(self, title, fgcol, bgcol, contents, width = 6, prelude = '', marginalia = None, gap = '&nbsp;'):
        if marginalia is None:
            marginalia = '<tt>' + '&nbsp;' * width + '</tt>'
        result = '<p>\n<table width="100%%" cellspacing=0 cellpadding=2 border=0 summary="section">\n<tr bgcolor="%s">\n<td colspan=3 valign=bottom>&nbsp;<br>\n<font color="%s" face="helvetica, arial">%s</font></td></tr>\n    ' % (bgcol, fgcol, title)
        if prelude:
            result = result + '\n<tr bgcolor="%s"><td rowspan=2>%s</td>\n<td colspan=2>%s</td></tr>\n<tr><td>%s</td>' % (bgcol,
             marginalia,
             prelude,
             gap)
        else:
            result = result + '\n<tr><td bgcolor="%s">%s</td><td>%s</td>' % (bgcol, marginalia, gap)
        return result + '\n<td width="100%%">%s</td></tr></table>' % contents

    def bigsection(self, title, *args):
        title = '<big><strong>%s</strong></big>' % title
        return self.section(title, *args)

    def preformat(self, text):
        text = self.escape(expandtabs(text))
        return replace(text, '\n\n', '\n \n', '\n\n', '\n \n', ' ', '&nbsp;', '\n', '<br>\n')

    def multicolumn(self, list, format, cols = 4):
        result = ''
        rows = (len(list) + cols - 1) / cols
        for col in range(cols):
            result = result + '<td width="%d%%" valign=top>' % (100 / cols)
            for i in range(rows * col, rows * col + rows):
                if i < len(list):
                    result = result + format(list[i]) + '<br>\n'

            result = result + '</td>'

        return '<table width="100%%" summary="list"><tr>%s</tr></table>' % result

    def grey(self, text):
        return '<font color="#909090">%s</font>' % text

    def namelink(self, name, *dicts):
        for dict in dicts:
            if name in dict:
                return '<a href="%s">%s</a>' % (dict[name], name)

        return name

    def classlink(self, object, modname):
        name, module = object.__name__, sys.modules.get(object.__module__)
        if hasattr(module, name) and getattr(module, name) is object:
            return '<a href="%s.html#%s">%s</a>' % (module.__name__, name, classname(object, modname))
        return classname(object, modname)

    def modulelink(self, object):
        return '<a href="%s.html">%s</a>' % (object.__name__, object.__name__)

    def modpkglink(self, (name, path, ispackage, shadowed)):
        if shadowed:
            return self.grey(name)
        if path:
            url = '%s.%s.html' % (path, name)
        else:
            url = '%s.html' % name
        if ispackage:
            text = '<strong>%s</strong>&nbsp;(package)' % name
        else:
            text = name
        return '<a href="%s">%s</a>' % (url, text)

    def markup(self, text, escape = None, funcs = {}, classes = {}, methods = {}):
        escape = escape or self.escape
        results = []
        here = 0
        pattern = re.compile('\\b((http|ftp)://\\S+[\\w/]|RFC[- ]?(\\d+)|PEP[- ]?(\\d+)|(self\\.)?(\\w+))')
        while True:
            match = pattern.search(text, here)
            if not match:
                break
            start, end = match.span()
            results.append(escape(text[here:start]))
            all, scheme, rfc, pep, selfdot, name = match.groups()
            if scheme:
                url = escape(all).replace('"', '&quot;')
                results.append('<a href="%s">%s</a>' % (url, url))
            elif rfc:
                url = 'http://www.rfc-editor.org/rfc/rfc%d.txt' % int(rfc)
                results.append('<a href="%s">%s</a>' % (url, escape(all)))
            elif pep:
                url = 'http://www.python.org/peps/pep-%04d.html' % int(pep)
                results.append('<a href="%s">%s</a>' % (url, escape(all)))
            elif text[end:end + 1] == '(':
                results.append(self.namelink(name, methods, funcs, classes))
            elif selfdot:
                results.append('self.<strong>%s</strong>' % name)
            else:
                results.append(self.namelink(name, classes))
            here = end

        results.append(escape(text[here:]))
        return join(results, '')

    def formattree(self, tree, modname, parent = None):
        result = ''
        for entry in tree:
            if type(entry) is type(()):
                c, bases = entry
                result = result + '<dt><font face="helvetica, arial">'
                result = result + self.classlink(c, modname)
                if bases and bases != (parent,):
                    parents = []
                    for base in bases:
                        parents.append(self.classlink(base, modname))

                    result = result + '(' + join(parents, ', ') + ')'
                result = result + '\n</font></dt>'
            elif type(entry) is type([]):
                result = result + '<dd>\n%s</dd>\n' % self.formattree(entry, modname, c)

        return '<dl>\n%s</dl>\n' % result

    def docmodule(self, object, name = None, mod = None, *ignored):
        name = object.__name__
        try:
            all = object.__all__
        except AttributeError:
            all = None

        parts = split(name, '.')
        links = []
        for i in range(len(parts) - 1):
            links.append('<a href="%s.html"><font color="#ffffff">%s</font></a>' % (join(parts[:i + 1], '.'), parts[i]))

        linkedname = join(links + parts[-1:], '.')
        head = '<big><big><strong>%s</strong></big></big>' % linkedname
        try:
            path = inspect.getabsfile(object)
            url = path
            if sys.platform == 'win32':
                import nturl2path
                url = nturl2path.pathname2url(path)
            filelink = '<a href="file:%s">%s</a>' % (url, path)
        except TypeError:
            filelink = '(built-in)'

        info = []
        if hasattr(object, '__version__'):
            version = str(object.__version__)
            if version[:11] == '$' + 'Revision: ' and version[-1:] == '$':
                version = strip(version[11:-1])
            info.append('version %s' % self.escape(version))
        if hasattr(object, '__date__'):
            info.append(self.escape(str(object.__date__)))
        if info:
            head = head + ' (%s)' % join(info, ', ')
        docloc = self.getdocloc(object)
        if docloc is not None:
            docloc = '<br><a href="%(docloc)s">Module Docs</a>' % locals()
        else:
            docloc = ''
        result = self.heading(head, '#ffffff', '#7799ee', '<a href=".">index</a><br>' + filelink + docloc)
        modules = inspect.getmembers(object, inspect.ismodule)
        classes, cdict = [], {}
        for key, value in inspect.getmembers(object, inspect.isclass):
            if not all is not None:
                if inspect.getmodule(value) or object is object:
                    visiblename(key, all) and classes.append((key, value))
                    cdict[key] = cdict[value] = '#' + key

        for key, value in classes:
            for base in value.__bases__:
                key, modname = base.__name__, base.__module__
                module = sys.modules.get(modname)
                if modname != name and module and hasattr(module, key):
                    if getattr(module, key) is base:
                        if key not in cdict:
                            cdict[key] = cdict[base] = modname + '.html#' + key

        funcs, fdict = [], {}
        for key, value in inspect.getmembers(object, inspect.isroutine):
            if all is not None or inspect.isbuiltin(value) or inspect.getmodule(value) is object:
                if visiblename(key, all):
                    funcs.append((key, value))
                    fdict[key] = '#-' + key
                    if inspect.isfunction(value):
                        fdict[value] = fdict[key]

        data = []
        for key, value in inspect.getmembers(object, isdata):
            if visiblename(key, all):
                data.append((key, value))

        doc = self.markup(getdoc(object), self.preformat, fdict, cdict)
        if doc:
            doc = '<tt>%s</tt>' % doc
            result = result + '<p>%s</p>\n' % doc
            if hasattr(object, '__path__'):
                modpkgs = []
                modnames = []
                for file in os.listdir(object.__path__[0]):
                    path = os.path.join(object.__path__[0], file)
                    modname = inspect.getmodulename(file)
                    if modname != '__init__':
                        if modname and modname not in modnames:
                            modpkgs.append((modname,
                             name,
                             0,
                             0))
                            modnames.append(modname)
                        elif ispackage(path):
                            modpkgs.append((file,
                             name,
                             1,
                             0))

                modpkgs.sort()
                contents = self.multicolumn(modpkgs, self.modpkglink)
                result = result + self.bigsection('Package Contents', '#ffffff', '#aa55cc', contents)
            elif modules:
                contents = self.multicolumn(modules, lambda (key, value), s = self: s.modulelink(value))
                result = result + self.bigsection('Modules', '#fffff', '#aa55cc', contents)
            if classes:
                classlist = map(lambda (key, value): value, classes)
                contents = [self.formattree(inspect.getclasstree(classlist, 1), name)]
                for key, value in classes:
                    contents.append(self.document(value, key, name, fdict, cdict))

                result = result + self.bigsection('Classes', '#ffffff', '#ee77aa', join(contents))
            if funcs:
                contents = []
                for key, value in funcs:
                    contents.append(self.document(value, key, name, fdict, cdict))

                result = result + self.bigsection('Functions', '#ffffff', '#eeaa77', join(contents))
            if data:
                contents = []
                for key, value in data:
                    contents.append(self.document(value, key))

                result = result + self.bigsection('Data', '#ffffff', '#55aa55', join(contents, '<br>\n'))
            if hasattr(object, '__author__'):
                contents = self.markup(str(object.__author__), self.preformat)
                result = result + self.bigsection('Author', '#ffffff', '#7799ee', contents)
            contents = hasattr(object, '__credits__') and self.markup(str(object.__credits__), self.preformat)
            result = result + self.bigsection('Credits', '#ffffff', '#7799ee', contents)
        return result

    def docclass(self, object, name = None, mod = None, funcs = {}, classes = {}, *ignored):
        realname = object.__name__
        if not name:
            name = realname
            bases = object.__bases__
            contents = []
            push = contents.append

            class HorizontalRule():
                __module__ = __name__

                def __init__(self):
                    self.needone = 0

                def maybe(self):
                    if self.needone:
                        push('<hr>\n')
                    self.needone = 1

            hr = HorizontalRule()
            mro = deque(inspect.getmro(object))
            if len(mro) > 2:
                hr.maybe()
                push('<dl><dt>Method resolution order:</dt>\n')
                for base in mro:
                    push('<dd>%s</dd>\n' % self.classlink(base, object.__module__))

                push('</dl>\n')

            def spill(msg, attrs, predicate):
                ok, attrs = _split_list(attrs, predicate)
                if ok:
                    hr.maybe()
                    push(msg)
                    for name, kind, homecls, value in ok:
                        push(self.document(getattr(object, name), name, mod, funcs, classes, mdict, object))
                        push('\n')

                return attrs

            def spillproperties(msg, attrs, predicate):
                ok, attrs = _split_list(attrs, predicate)
                if ok:
                    hr.maybe()
                    push(msg)
                    for name, kind, homecls, value in ok:
                        push(self._docproperty(name, value, mod))

                return attrs

            def spilldata(msg, attrs, predicate):
                ok, attrs = _split_list(attrs, predicate)
                if ok:
                    hr.maybe()
                    push(msg)
                    for name, kind, homecls, value in ok:
                        base = self.docother(getattr(object, name), name, mod)
                        if callable(value) or inspect.isdatadescriptor(value):
                            doc = getattr(value, '__doc__', None)
                        else:
                            doc = None
                        if doc is None:
                            push('<dl><dt>%s</dl>\n' % base)
                        else:
                            doc = self.markup(getdoc(value), self.preformat, funcs, classes, mdict)
                            doc = '<dd><tt>%s</tt>' % doc
                            push('<dl><dt>%s%s</dl>\n' % (base, doc))
                        push('\n')

                return attrs

            attrs = filter(lambda (name, kind, cls, value): visiblename(name), inspect.classify_class_attrs(object))
            mdict = {}
            for key, kind, homecls, value in attrs:
                mdict[key] = anchor = '#' + name + '-' + key
                value = getattr(object, key)
                try:
                    mdict[value] = anchor
                except TypeError:
                    pass

            while attrs:
                if mro:
                    thisclass = mro.popleft()
                else:
                    thisclass = attrs[0][2]
                attrs, inherited = _split_list(attrs, lambda t: t[2] is thisclass)
                if thisclass is __builtin__.object:
                    attrs = inherited
                    continue
                elif thisclass is object:
                    tag = 'defined here'
                else:
                    tag = 'inherited from %s' % self.classlink(thisclass, object.__module__)
                tag += ':<br>\n'
                attrs.sort(key=lambda t: t[0])
                attrs = spill('Methods %s' % tag, attrs, lambda t: t[1] == 'method')
                attrs = spill('Class methods %s' % tag, attrs, lambda t: t[1] == 'class method')
                attrs = spill('Static methods %s' % tag, attrs, lambda t: t[1] == 'static method')
                attrs = spillproperties('Properties %s' % tag, attrs, lambda t: t[1] == 'property')
                attrs = spilldata('Data and other attributes %s' % tag, attrs, lambda t: t[1] == 'data')
                attrs = inherited

            contents = ''.join(contents)
            if name == realname:
                title = '<a name="%s">class <strong>%s</strong></a>' % (name, realname)
            else:
                title = '<strong>%s</strong> = <a name="%s">class %s</a>' % (name, name, realname)
            parents = bases and []
            for base in bases:
                parents.append(self.classlink(base, object.__module__))

            title = title + '(%s)' % join(parents, ', ')
        doc = self.markup(getdoc(object), self.preformat, funcs, classes, mdict)
        doc = doc and '<tt>%s<br>&nbsp;</tt>' % doc
        return self.section(title, '#000000', '#ffc8d8', contents, 3, doc)

    def formatvalue(self, object):
        return self.grey('=' + self.repr(object))

    def docroutine(self, object, name = None, mod = None, funcs = {}, classes = {}, methods = {}, cl = None):
        realname = object.__name__
        if not name:
            name = realname
            if not (cl and cl.__name__):
                anchor = '' + '-' + name
                note = ''
                skipdocs = 0
                if inspect.ismethod(object):
                    imclass = object.im_class
                    if cl:
                        if imclass is not cl:
                            note = ' from ' + self.classlink(imclass, mod)
                    elif object.im_self:
                        note = ' method of %s instance' % self.classlink(object.im_self.__class__, mod)
                    else:
                        note = ' unbound %s method' % self.classlink(imclass, mod)
                    object = object.im_func
                if name == realname:
                    title = '<a name="%s"><strong>%s</strong></a>' % (anchor, realname)
                else:
                    if cl and realname in cl.__dict__ and cl.__dict__[realname] is object:
                        reallink = '<a href="#%s">%s</a>' % (cl.__name__ + '-' + realname, realname)
                        skipdocs = 1
                    else:
                        reallink = realname
                    title = '<a name="%s"><strong>%s</strong></a> = %s' % (anchor, name, reallink)
                if inspect.isfunction(object):
                    args, varargs, varkw, defaults = inspect.getargspec(object)
                    argspec = inspect.formatargspec(args, varargs, varkw, defaults, formatvalue=self.formatvalue)
                    title = realname == '<lambda>' and '<strong>%s</strong> <em>lambda</em> ' % name
                    argspec = argspec[1:-1]
            else:
                argspec = '(...)'
            decl = title + argspec + (note and self.grey('<font face="helvetica, arial">%s</font>' % note))
            return skipdocs and '<dl><dt>%s</dt></dl>\n' % decl
        else:
            doc = self.markup(getdoc(object), self.preformat, funcs, classes, methods)
            doc = doc and '<dd><tt>%s</tt></dd>' % doc
            return '<dl><dt>%s</dt>%s</dl>\n' % (decl, doc)

    def _docproperty(self, name, value, mod):
        results = []
        push = results.append
        if name:
            push('<dl><dt><strong>%s</strong></dt>\n' % name)
        if value.__doc__ is not None:
            doc = self.markup(getdoc(value), self.preformat)
            push('<dd><tt>%s</tt></dd>\n' % doc)
        for attr, tag in [('fget', '<em>get</em>'), ('fset', '<em>set</em>'), ('fdel', '<em>delete</em>')]:
            func = getattr(value, attr)
            if func is not None:
                base = self.document(func, tag, mod)
                push('<dd>%s</dd>\n' % base)

        push('</dl>\n')
        return ''.join(results)

    def docproperty(self, object, name = None, mod = None, cl = None):
        return self._docproperty(name, object, mod)

    def docother(self, object, name = None, mod = None, *ignored):
        lhs = name and '<strong>%s</strong> = ' % name or ''
        return lhs + self.repr(object)

    def index(self, dir, shadowed = None):
        modpkgs = []
        if shadowed is None:
            shadowed = {}
        seen = {}
        files = os.listdir(dir)

        def found(name, ispackage, modpkgs = modpkgs, shadowed = shadowed, seen = seen):
            if name not in seen:
                modpkgs.append((name,
                 '',
                 ispackage,
                 name in shadowed))
                seen[name] = 1
                shadowed[name] = 1

        for file in files:
            path = os.path.join(dir, file)
            if ispackage(path):
                found(file, 1)

        for file in files:
            path = os.path.join(dir, file)
            if os.path.isfile(path):
                modname = inspect.getmodulename(file)
                if modname:
                    found(modname, 0)

        modpkgs.sort()
        contents = self.multicolumn(modpkgs, self.modpkglink)
        return self.bigsection(dir, '#ffffff', '#ee77aa', contents)


class TextRepr(Repr):
    __module__ = __name__

    def __init__(self):
        Repr.__init__(self)
        self.maxlist = self.maxtuple = 20
        self.maxdict = 10
        self.maxstring = self.maxother = 100

    def repr1(self, x, level):
        if hasattr(type(x), '__name__'):
            methodname = 'repr_' + join(split(type(x).__name__), '_')
            if hasattr(self, methodname):
                return getattr(self, methodname)(x, level)
        return cram(stripid(repr(x)), self.maxother)

    def repr_string(self, x, level):
        test = cram(x, self.maxstring)
        testrepr = repr(test)
        if '\\' in test and '\\' not in replace(testrepr, '\\\\', ''):
            return 'r' + testrepr[0] + test + testrepr[0]
        return testrepr

    repr_str = repr_string

    def repr_instance(self, x, level):
        try:
            return cram(stripid(repr(x)), self.maxstring)
        except:
            return '<%s instance>' % x.__class__.__name__


class TextDoc(Doc):
    __module__ = __name__
    _repr_instance = TextRepr()
    repr = _repr_instance.repr

    def bold(self, text):
        return join(map(lambda ch: ch + '\x08' + ch, text), '')

    def indent(self, text, prefix = '    '):
        if not text:
            return ''
        lines = split(text, '\n')
        lines = map(lambda line, prefix = prefix: prefix + line, lines)
        if lines:
            lines[-1] = rstrip(lines[-1])
        return join(lines, '\n')

    def section(self, title, contents):
        return self.bold(title) + '\n' + rstrip(self.indent(contents)) + '\n\n'

    def formattree(self, tree, modname, parent = None, prefix = ''):
        result = ''
        for entry in tree:
            if type(entry) is type(()):
                c, bases = entry
                result = result + prefix + classname(c, modname)
                if bases and bases != (parent,):
                    parents = map(lambda c, m = modname: classname(c, m), bases)
                    result = result + '(%s)' % join(parents, ', ')
                result = result + '\n'
            elif type(entry) is type([]):
                result = result + self.formattree(entry, modname, c, prefix + '    ')

        return result

    def docmodule(self, object, name = None, mod = None):
        name = object.__name__
        synop, desc = splitdoc(getdoc(object))
        result = self.section('NAME', name + (synop and ' - ' + synop))
        try:
            all = object.__all__
        except AttributeError:
            all = None

        try:
            file = inspect.getabsfile(object)
        except TypeError:
            file = '(built-in)'

        result = result + self.section('FILE', file)
        docloc = self.getdocloc(object)
        if docloc is not None:
            result = result + self.section('MODULE DOCS', docloc)
        if desc:
            result = result + self.section('DESCRIPTION', desc)
        classes = []
        for key, value in inspect.getmembers(object, inspect.isclass):
            if not all is not None:
                if inspect.getmodule(value) or object is object:
                    visiblename(key, all) and classes.append((key, value))

        funcs = []
        for key, value in inspect.getmembers(object, inspect.isroutine):
            if all is not None or inspect.isbuiltin(value) or inspect.getmodule(value) is object:
                if visiblename(key, all):
                    funcs.append((key, value))

        data = []
        for key, value in inspect.getmembers(object, isdata):
            if visiblename(key, all):
                data.append((key, value))

        if hasattr(object, '__path__'):
            modpkgs = []
            for file in os.listdir(object.__path__[0]):
                path = os.path.join(object.__path__[0], file)
                modname = inspect.getmodulename(file)
                if modname != '__init__':
                    if modname and modname not in modpkgs:
                        modpkgs.append(modname)
                    elif ispackage(path):
                        modpkgs.append(file + ' (package)')

            modpkgs.sort()
            result = result + self.section('PACKAGE CONTENTS', join(modpkgs, '\n'))
        if classes:
            classlist = map(lambda (key, value): value, classes)
            contents = [self.formattree(inspect.getclasstree(classlist, 1), name)]
            for key, value in classes:
                contents.append(self.document(value, key, name))

            result = result + self.section('CLASSES', join(contents, '\n'))
        if funcs:
            contents = []
            for key, value in funcs:
                contents.append(self.document(value, key, name))

            result = result + self.section('FUNCTIONS', join(contents, '\n'))
        if data:
            contents = []
            for key, value in data:
                contents.append(self.docother(value, key, name, 70))

            result = result + self.section('DATA', join(contents, '\n'))
        if hasattr(object, '__version__'):
            version = str(object.__version__)
            if version[:11] == '$' + 'Revision: ' and version[-1:] == '$':
                version = strip(version[11:-1])
            result = result + self.section('VERSION', version)
        if hasattr(object, '__date__'):
            result = result + self.section('DATE', str(object.__date__))
        if hasattr(object, '__author__'):
            result = result + self.section('AUTHOR', str(object.__author__))
        if hasattr(object, '__credits__'):
            result = result + self.section('CREDITS', str(object.__credits__))
        return result

    def docclass(self, object, name = None, mod = None):
        realname = object.__name__
        if not name:
            name = realname
            bases = object.__bases__

            def makename(c, m = object.__module__):
                return classname(c, m)

            if name == realname:
                title = 'class ' + self.bold(realname)
            else:
                title = self.bold(name) + ' = class ' + realname
            if bases:
                parents = map(makename, bases)
                title = title + '(%s)' % join(parents, ', ')
            doc = getdoc(object)
            if not (doc and [doc + '\n']):
                contents = []
                push = contents.append
                mro = deque(inspect.getmro(object))
                len(mro) > 2 and push('Method resolution order:')
                for base in mro:
                    push('    ' + makename(base))

                push('')

            class HorizontalRule():
                __module__ = __name__

                def __init__(self):
                    self.needone = 0

                def maybe(self):
                    if self.needone:
                        push('-' * 70)
                    self.needone = 1

            hr = HorizontalRule()

            def spill(msg, attrs, predicate):
                ok, attrs = _split_list(attrs, predicate)
                if ok:
                    hr.maybe()
                    push(msg)
                    for name, kind, homecls, value in ok:
                        push(self.document(getattr(object, name), name, mod, object))

                return attrs

            def spillproperties(msg, attrs, predicate):
                ok, attrs = _split_list(attrs, predicate)
                if ok:
                    hr.maybe()
                    push(msg)
                    for name, kind, homecls, value in ok:
                        push(self._docproperty(name, value, mod))

                return attrs

            def spilldata(msg, attrs, predicate):
                ok, attrs = _split_list(attrs, predicate)
                if ok:
                    hr.maybe()
                    push(msg)
                    for name, kind, homecls, value in ok:
                        if callable(value) or inspect.isdatadescriptor(value):
                            doc = getdoc(value)
                        else:
                            doc = None
                        push(self.docother(getattr(object, name), name, mod, 70, doc) + '\n')

                return attrs

            attrs = filter(lambda (name, kind, cls, value): visiblename(name), inspect.classify_class_attrs(object))
            while attrs:
                if mro:
                    thisclass = mro.popleft()
                else:
                    thisclass = attrs[0][2]
                attrs, inherited = _split_list(attrs, lambda t: t[2] is thisclass)
                if thisclass is __builtin__.object:
                    attrs = inherited
                    continue
                elif thisclass is object:
                    tag = 'defined here'
                else:
                    tag = 'inherited from %s' % classname(thisclass, object.__module__)
                filter(lambda t: not t[0].startswith('_'), attrs)
                attrs.sort()
                attrs = spill('Methods %s:\n' % tag, attrs, lambda t: t[1] == 'method')
                attrs = spill('Class methods %s:\n' % tag, attrs, lambda t: t[1] == 'class method')
                attrs = spill('Static methods %s:\n' % tag, attrs, lambda t: t[1] == 'static method')
                attrs = spillproperties('Properties %s:\n' % tag, attrs, lambda t: t[1] == 'property')
                attrs = spilldata('Data and other attributes %s:\n' % tag, attrs, lambda t: t[1] == 'data')
                attrs = inherited

            contents = '\n'.join(contents)
            return contents or title + '\n'
        return title + '\n' + self.indent(rstrip(contents), ' |  ') + '\n'

    def formatvalue(self, object):
        return '=' + self.repr(object)

    def docroutine(self, object, name = None, mod = None, cl = None):
        realname = object.__name__
        if not name:
            name = realname
            note = ''
            skipdocs = 0
            if inspect.ismethod(object):
                imclass = object.im_class
                if cl:
                    if imclass is not cl:
                        note = ' from ' + classname(imclass, mod)
                elif object.im_self:
                    note = ' method of %s instance' % classname(object.im_self.__class__, mod)
                else:
                    note = ' unbound %s method' % classname(imclass, mod)
                object = object.im_func
            if name == realname:
                title = self.bold(realname)
            else:
                if cl and realname in cl.__dict__ and cl.__dict__[realname] is object:
                    skipdocs = 1
                title = self.bold(name) + ' = ' + realname
            if inspect.isfunction(object):
                args, varargs, varkw, defaults = inspect.getargspec(object)
                argspec = inspect.formatargspec(args, varargs, varkw, defaults, formatvalue=self.formatvalue)
                if realname == '<lambda>':
                    title = 'lambda'
                    argspec = argspec[1:-1]
            else:
                argspec = '(...)'
            decl = title + argspec + note
            return skipdocs and decl + '\n'
        else:
            doc = getdoc(object) or ''
            return decl + '\n' + (doc and rstrip(self.indent(doc)) + '\n')

    def _docproperty(self, name, value, mod):
        results = []
        push = results.append
        if name:
            push(name)
        need_blank_after_doc = 0
        if not getdoc(value):
            doc = ''
            doc and push(self.indent(doc))
            need_blank_after_doc = 1
        for attr, tag in [('fget', '<get>'), ('fset', '<set>'), ('fdel', '<delete>')]:
            func = getattr(value, attr)
            if func is not None:
                if need_blank_after_doc:
                    push('')
                    need_blank_after_doc = 0
                base = self.document(func, tag, mod)
                push(self.indent(base))

        return '\n'.join(results)

    def docproperty(self, object, name = None, mod = None, cl = None):
        return self._docproperty(name, object, mod)

    def docother(self, object, name = None, mod = None, maxlen = None, doc = None):
        repr = self.repr(object)
        if maxlen:
            if not (name and name + ' = '):
                line = '' + repr
                chop = maxlen - len(line)
                if chop < 0:
                    repr = repr[:chop] + '...'
            line = name and self.bold(name) + ' = ' or '' + repr
            doc is not None and line += '\n' + self.indent(str(doc))
        return line


def pager(text):
    global pager
    pager = getpager()
    pager(text)


def getpager():
    if type(sys.stdout) is not types.FileType:
        return plainpager
    if not sys.stdin.isatty() or not sys.stdout.isatty():
        return plainpager
    if os.environ.get('TERM') in ['dumb', 'emacs']:
        return plainpager
    if 'PAGER' in os.environ:
        if sys.platform == 'win32':
            return lambda text: tempfilepager(plain(text), os.environ['PAGER'])
        elif os.environ.get('TERM') in ['dumb', 'emacs']:
            return lambda text: pipepager(plain(text), os.environ['PAGER'])
        else:
            return lambda text: pipepager(text, os.environ['PAGER'])
    if sys.platform == 'win32' or sys.platform.startswith('os2'):
        return lambda text: tempfilepager(plain(text), 'more <')
    if hasattr(os, 'system') and os.system('(less) 2>/dev/null') == 0:
        return lambda text: pipepager(text, 'less')
    import tempfile
    fd, filename = tempfile.mkstemp()
    os.close(fd)
    try:
        if hasattr(os, 'system') and os.system('more %s' % filename) == 0:
            return lambda text: pipepager(text, 'more')
        else:
            return ttypager
    finally:
        os.unlink(filename)


def plain(text):
    return re.sub('.\x08', '', text)


def pipepager(text, cmd):
    pipe = os.popen(cmd, 'w')
    try:
        pipe.write(text)
        pipe.close()
    except IOError:
        pass


def tempfilepager(text, cmd):
    import tempfile
    filename = tempfile.mktemp()
    file = open(filename, 'w')
    file.write(text)
    file.close()
    try:
        os.system(cmd + ' ' + filename)
    finally:
        os.unlink(filename)


def ttypager(text):
    lines = split(plain(text), '\n')
    try:
        import tty
        fd = sys.stdin.fileno()
        old = tty.tcgetattr(fd)
        tty.setcbreak(fd)
        getchar = lambda : sys.stdin.read(1)
    except (ImportError, AttributeError):
        tty = None
        getchar = lambda : sys.stdin.readline()[:-1][:1]

    try:
        r = inc = os.environ.get('LINES', 25) - 1
        sys.stdout.write(join(lines[:inc], '\n') + '\n')
        while lines[r:]:
            sys.stdout.write('-- more --')
            sys.stdout.flush()
            c = getchar()
            if c in ['q', 'Q']:
                sys.stdout.write('\r          \r')
                break
            elif c in ['\r', '\n']:
                sys.stdout.write('\r          \r' + lines[r] + '\n')
                r = r + 1
                continue
            if c in ['b', 'B', '\x1b']:
                r = r - inc - inc
                if r < 0:
                    r = 0
            sys.stdout.write('\n' + join(lines[r:r + inc], '\n') + '\n')
            r = r + inc

    finally:
        if tty:
            tty.tcsetattr(fd, tty.TCSAFLUSH, old)

    return


def plainpager(text):
    sys.stdout.write(plain(text))


def describe(thing):
    if inspect.ismodule(thing):
        if thing.__name__ in sys.builtin_module_names:
            return 'built-in module ' + thing.__name__
        if hasattr(thing, '__path__'):
            return 'package ' + thing.__name__
        else:
            return 'module ' + thing.__name__
    if inspect.isbuiltin(thing):
        return 'built-in function ' + thing.__name__
    if inspect.isclass(thing):
        return 'class ' + thing.__name__
    if inspect.isfunction(thing):
        return 'function ' + thing.__name__
    if inspect.ismethod(thing):
        return 'method ' + thing.__name__
    if type(thing) is types.InstanceType:
        return 'instance of ' + thing.__class__.__name__
    return type(thing).__name__


def locate(path, forceload = 0):
    parts = [ part for part in split(path, '.') if part ]
    module, n = (None, 0)
    while n < len(parts):
        nextmodule = safeimport(join(parts[:n + 1], '.'), forceload)
        if nextmodule:
            module, n = nextmodule, n + 1
        else:
            break

    if module:
        object = module
        for part in parts[n:]:
            try:
                object = getattr(object, part)
            except AttributeError:
                return None

        return object
    elif hasattr(__builtin__, path):
        return getattr(__builtin__, path)
    return None


text = TextDoc()
html = HTMLDoc()

def resolve(thing, forceload = 0):
    if isinstance(thing, str):
        object = locate(thing, forceload)
        if not object:
            raise ImportError, 'no Python documentation found for %r' % thing
        return (object, thing)
    else:
        return (thing, getattr(thing, '__name__', None))
    return None


def doc(thing, title = 'Python Library Documentation: %s', forceload = 0):
    try:
        object, name = resolve(thing, forceload)
        desc = describe(object)
        module = inspect.getmodule(object)
        if name and '.' in name:
            desc += ' in ' + name[:name.rfind('.')]
        elif module and module is not object:
            desc += ' in module ' + module.__name__
        if not inspect.ismodule(object):
            object = inspect.isclass(object) or inspect.isroutine(object) or isinstance(object, property) or type(object)
            desc += ' object'
        pager(title % desc + '\n\n' + text.document(object, name))
    except (ImportError, ErrorDuringImport) as value:
        print value


def writedoc(thing, forceload = 0):
    try:
        object, name = resolve(thing, forceload)
        page = html.page(describe(object), html.document(object, name))
        file = open(name + '.html', 'w')
        file.write(page)
        file.close()
        print 'wrote', name + '.html'
    except (ImportError, ErrorDuringImport) as value:
        print value


def writedocs(dir, pkgpath = '', done = None):
    if done is None:
        done = {}
    for file in os.listdir(dir):
        path = os.path.join(dir, file)
        if ispackage(path):
            writedocs(path, pkgpath + file + '.', done)
        elif os.path.isfile(path):
            modname = inspect.getmodulename(path)
            if modname:
                if modname == '__init__':
                    modname = pkgpath[:-1]
                else:
                    modname = pkgpath + modname
                if modname not in done:
                    done[modname] = 1
                    writedoc(modname)

    return


class Helper():
    __module__ = __name__
    keywords = {'and': 'BOOLEAN',
     'assert': ('ref/assert', ''),
     'break': ('ref/break', 'while for'),
     'class': ('ref/class', 'CLASSES SPECIALMETHODS'),
     'continue': ('ref/continue', 'while for'),
     'def': ('ref/function', ''),
     'del': ('ref/del', 'BASICMETHODS'),
     'elif': 'if',
     'else': ('ref/if', 'while for'),
     'except': 'try',
     'exec': ('ref/exec', ''),
     'finally': 'try',
     'for': ('ref/for', 'break continue while'),
     'from': 'import',
     'global': ('ref/global', 'NAMESPACES'),
     'if': ('ref/if', 'TRUTHVALUE'),
     'import': ('ref/import', 'MODULES'),
     'in': ('ref/comparisons', 'SEQUENCEMETHODS2'),
     'is': 'COMPARISON',
     'lambda': ('ref/lambdas', 'FUNCTIONS'),
     'not': 'BOOLEAN',
     'or': 'BOOLEAN',
     'pass': ('ref/pass', ''),
     'print': ('ref/print', ''),
     'raise': ('ref/raise', 'EXCEPTIONS'),
     'return': ('ref/return', 'FUNCTIONS'),
     'try': ('ref/try', 'EXCEPTIONS'),
     'while': ('ref/while', 'break continue if TRUTHVALUE'),
     'yield': ('ref/yield', '')}
    topics = {'TYPES': ('ref/types', 'STRINGS UNICODE NUMBERS SEQUENCES MAPPINGS FUNCTIONS CLASSES MODULES FILES inspect'),
     'STRINGS': ('ref/strings', 'str UNICODE SEQUENCES STRINGMETHODS FORMATTING TYPES'),
     'STRINGMETHODS': ('lib/string-methods', 'STRINGS FORMATTING'),
     'FORMATTING': ('lib/typesseq-strings', 'OPERATORS'),
     'UNICODE': ('ref/strings', 'encodings unicode SEQUENCES STRINGMETHODS FORMATTING TYPES'),
     'NUMBERS': ('ref/numbers', 'INTEGER FLOAT COMPLEX TYPES'),
     'INTEGER': ('ref/integers', 'int range'),
     'FLOAT': ('ref/floating', 'float math'),
     'COMPLEX': ('ref/imaginary', 'complex cmath'),
     'SEQUENCES': ('lib/typesseq', 'STRINGMETHODS FORMATTING xrange LISTS'),
     'MAPPINGS': 'DICTIONARIES',
     'FUNCTIONS': ('lib/typesfunctions', 'def TYPES'),
     'METHODS': ('lib/typesmethods', 'class def CLASSES TYPES'),
     'CODEOBJECTS': ('lib/bltin-code-objects', 'compile FUNCTIONS TYPES'),
     'TYPEOBJECTS': ('lib/bltin-type-objects', 'types TYPES'),
     'FRAMEOBJECTS': 'TYPES',
     'TRACEBACKS': 'TYPES',
     'NONE': ('lib/bltin-null-object', ''),
     'ELLIPSIS': ('lib/bltin-ellipsis-object', 'SLICINGS'),
     'FILES': ('lib/bltin-file-objects', ''),
     'SPECIALATTRIBUTES': ('lib/specialattrs', ''),
     'CLASSES': ('ref/types', 'class SPECIALMETHODS PRIVATENAMES'),
     'MODULES': ('lib/typesmodules', 'import'),
     'PACKAGES': 'import',
     'EXPRESSIONS': ('ref/summary', 'lambda or and not in is BOOLEAN COMPARISON BITWISE SHIFTING BINARY FORMATTING POWER UNARY ATTRIBUTES SUBSCRIPTS SLICINGS CALLS TUPLES LISTS DICTIONARIES BACKQUOTES'),
     'OPERATORS': 'EXPRESSIONS',
     'PRECEDENCE': 'EXPRESSIONS',
     'OBJECTS': ('ref/objects', 'TYPES'),
     'SPECIALMETHODS': ('ref/specialnames', 'BASICMETHODS ATTRIBUTEMETHODS CALLABLEMETHODS SEQUENCEMETHODS1 MAPPINGMETHODS SEQUENCEMETHODS2 NUMBERMETHODS CLASSES'),
     'BASICMETHODS': ('ref/customization', 'cmp hash repr str SPECIALMETHODS'),
     'ATTRIBUTEMETHODS': ('ref/attribute-access', 'ATTRIBUTES SPECIALMETHODS'),
     'CALLABLEMETHODS': ('ref/callable-types', 'CALLS SPECIALMETHODS'),
     'SEQUENCEMETHODS1': ('ref/sequence-types', 'SEQUENCES SEQUENCEMETHODS2 SPECIALMETHODS'),
     'SEQUENCEMETHODS2': ('ref/sequence-methods', 'SEQUENCES SEQUENCEMETHODS1 SPECIALMETHODS'),
     'MAPPINGMETHODS': ('ref/sequence-types', 'MAPPINGS SPECIALMETHODS'),
     'NUMBERMETHODS': ('ref/numeric-types', 'NUMBERS AUGMENTEDASSIGNMENT SPECIALMETHODS'),
     'EXECUTION': ('ref/execmodel', 'NAMESPACES DYNAMICFEATURES EXCEPTIONS'),
     'NAMESPACES': ('ref/naming', 'global ASSIGNMENT DELETION DYNAMICFEATURES'),
     'DYNAMICFEATURES': ('ref/dynamic-features', ''),
     'SCOPING': 'NAMESPACES',
     'FRAMES': 'NAMESPACES',
     'EXCEPTIONS': ('ref/exceptions', 'try except finally raise'),
     'COERCIONS': ('ref/coercion-rules', 'CONVERSIONS'),
     'CONVERSIONS': ('ref/conversions', 'COERCIONS'),
     'IDENTIFIERS': ('ref/identifiers', 'keywords SPECIALIDENTIFIERS'),
     'SPECIALIDENTIFIERS': ('ref/id-classes', ''),
     'PRIVATENAMES': ('ref/atom-identifiers', ''),
     'LITERALS': ('ref/atom-literals', 'STRINGS BACKQUOTES NUMBERS TUPLELITERALS LISTLITERALS DICTIONARYLITERALS'),
     'TUPLES': 'SEQUENCES',
     'TUPLELITERALS': ('ref/exprlists', 'TUPLES LITERALS'),
     'LISTS': ('lib/typesseq-mutable', 'LISTLITERALS'),
     'LISTLITERALS': ('ref/lists', 'LISTS LITERALS'),
     'DICTIONARIES': ('lib/typesmapping', 'DICTIONARYLITERALS'),
     'DICTIONARYLITERALS': ('ref/dict', 'DICTIONARIES LITERALS'),
     'BACKQUOTES': ('ref/string-conversions', 'repr str STRINGS LITERALS'),
     'ATTRIBUTES': ('ref/attribute-references', 'getattr hasattr setattr ATTRIBUTEMETHODS'),
     'SUBSCRIPTS': ('ref/subscriptions', 'SEQUENCEMETHODS1'),
     'SLICINGS': ('ref/slicings', 'SEQUENCEMETHODS2'),
     'CALLS': ('ref/calls', 'EXPRESSIONS'),
     'POWER': ('ref/power', 'EXPRESSIONS'),
     'UNARY': ('ref/unary', 'EXPRESSIONS'),
     'BINARY': ('ref/binary', 'EXPRESSIONS'),
     'SHIFTING': ('ref/shifting', 'EXPRESSIONS'),
     'BITWISE': ('ref/bitwise', 'EXPRESSIONS'),
     'COMPARISON': ('ref/comparisons', 'EXPRESSIONS BASICMETHODS'),
     'BOOLEAN': ('ref/Booleans', 'EXPRESSIONS TRUTHVALUE'),
     'ASSERTION': 'assert',
     'ASSIGNMENT': ('ref/assignment', 'AUGMENTEDASSIGNMENT'),
     'AUGMENTEDASSIGNMENT': ('ref/augassign', 'NUMBERMETHODS'),
     'DELETION': 'del',
     'PRINTING': 'print',
     'RETURNING': 'return',
     'IMPORTING': 'import',
     'CONDITIONAL': 'if',
     'LOOPING': ('ref/compound', 'for while break continue'),
     'TRUTHVALUE': ('lib/truth', 'if while and or not BASICMETHODS'),
     'DEBUGGING': ('lib/module-pdb', 'pdb')}

    def __init__(self, input, output):
        self.input = input
        self.output = output
        self.docdir = None
        execdir = os.path.dirname(sys.executable)
        homedir = os.environ.get('PYTHONHOME')
        for dir in [os.environ.get('PYTHONDOCS'),
         homedir and os.path.join(homedir, 'doc'),
         os.path.join(execdir, 'doc'),
         '/usr/doc/python-docs-' + split(sys.version)[0],
         '/usr/doc/python-' + split(sys.version)[0],
         '/usr/doc/python-docs-' + sys.version[:3],
         '/usr/doc/python-' + sys.version[:3],
         os.path.join(sys.prefix, 'Resources/English.lproj/Documentation')]:
            if dir and os.path.isdir(os.path.join(dir, 'lib')):
                self.docdir = dir

        return

    def __repr__(self):
        if inspect.stack()[1][3] == '?':
            self()
            return ''
        return '<pydoc.Helper instance>'

    def __call__(self, request = None):
        if request is not None:
            self.help(request)
        else:
            self.intro()
            self.interact()
            self.output.write('\nYou are now leaving help and returning to the Python interpreter.\nIf you want to ask for help on a particular object directly from the\ninterpreter, you can type "help(object)".  Executing "help(\'string\')"\nhas the same effect as typing a particular string at the help> prompt.\n')
        return

    def interact(self):
        self.output.write('\n')
        while True:
            try:
                request = self.getline('help> ')
                if not request:
                    break
            except (KeyboardInterrupt, EOFError):
                break

            request = strip(replace(request, '"', '', "'", ''))
            if lower(request) in ['q', 'quit']:
                break
            self.help(request)

    def getline(self, prompt):
        if self.input is sys.stdin:
            return raw_input(prompt)
        else:
            self.output.write(prompt)
            self.output.flush()
            return self.input.readline()

    def help(self, request):
        if type(request) is type(''):
            if request == 'help':
                self.intro()
            elif request == 'keywords':
                self.listkeywords()
            elif request == 'topics':
                self.listtopics()
            elif request == 'modules':
                self.listmodules()
            elif request[:8] == 'modules ':
                self.listmodules(split(request)[1])
            elif request in self.keywords:
                self.showtopic(request)
            elif request in self.topics:
                self.showtopic(request)
            elif request:
                doc(request, 'Help on %s:')
        elif isinstance(request, Helper):
            self()
        else:
            doc(request, 'Help on %s:')
        self.output.write('\n')

    def intro(self):
        self.output.write('\nWelcome to Python %s!  This is the online help utility.\n\nIf this is your first time using Python, you should definitely check out\nthe tutorial on the Internet at http://www.python.org/doc/tut/.\n\nEnter the name of any module, keyword, or topic to get help on writing\nPython programs and using Python modules.  To quit this help utility and\nreturn to the interpreter, just type "quit".\n\nTo get a list of available modules, keywords, or topics, type "modules",\n"keywords", or "topics".  Each module also comes with a one-line summary\nof what it does; to list the modules whose summaries contain a given word\nsuch as "spam", type "modules spam".\n' % sys.version[:3])

    def list(self, items, columns = 4, width = 80):
        items = items[:]
        items.sort()
        colw = width / columns
        rows = (len(items) + columns - 1) / columns
        for row in range(rows):
            for col in range(columns):
                i = col * rows + row
                if i < len(items):
                    self.output.write(items[i])
                    if col < columns - 1:
                        self.output.write(' ' + ' ' * (colw - 1 - len(items[i])))

            self.output.write('\n')

    def listkeywords(self):
        self.output.write('\nHere is a list of the Python keywords.  Enter any keyword to get more help.\n\n')
        self.list(self.keywords.keys())

    def listtopics(self):
        self.output.write('\nHere is a list of available topics.  Enter any topic name to get more help.\n\n')
        self.list(self.topics.keys())

    def showtopic(self, topic):
        if not self.docdir:
            self.output.write('\nSorry, topic and keyword documentation is not available because the Python\nHTML documentation files could not be found.  If you have installed them,\nplease set the environment variable PYTHONDOCS to indicate their location.\n')
            return
        target = self.topics.get(topic, self.keywords.get(topic))
        if not target:
            self.output.write('no documentation found for %s\n' % repr(topic))
            return
        if type(target) is type(''):
            return self.showtopic(target)
        filename, xrefs = target
        filename = self.docdir + '/' + filename + '.html'
        try:
            file = open(filename)
        except:
            self.output.write('could not read docs from %s\n' % filename)
            return

        divpat = re.compile('<div[^>]*navigat.*?</div.*?>', re.I | re.S)
        addrpat = re.compile('<address.*?>.*?</address.*?>', re.I | re.S)
        document = re.sub(addrpat, '', re.sub(divpat, '', file.read()))
        file.close()
        import htmllib, formatter, StringIO
        buffer = StringIO.StringIO()
        parser = htmllib.HTMLParser(formatter.AbstractFormatter(formatter.DumbWriter(buffer)))
        parser.start_table = parser.do_p
        parser.end_table = lambda parser = parser: parser.do_p({})
        parser.start_tr = parser.do_br
        parser.start_td = parser.start_th = lambda a, b = buffer: b.write('\t')
        parser.feed(document)
        buffer = replace(buffer.getvalue(), '\xa0', ' ', '\n', '\n  ')
        pager('  ' + strip(buffer) + '\n')
        if xrefs:
            buffer = StringIO.StringIO()
            formatter.DumbWriter(buffer).send_flowing_data('Related help topics: ' + join(split(xrefs), ', ') + '\n')
            self.output.write('\n%s\n' % buffer.getvalue())

    def listmodules(self, key = ''):
        if key:
            self.output.write('\nHere is a list of matching modules.  Enter any module name to get more help.\n\n')
            apropos(key)
        else:
            self.output.write('\nPlease wait a moment while I gather a list of all available modules...\n\n')
            modules = {}

            def callback(path, modname, desc, modules = modules):
                if modname and modname[-9:] == '.__init__':
                    modname = modname[:-9] + ' (package)'
                if find(modname, '.') < 0:
                    modules[modname] = 1

            ModuleScanner().run(callback)
            self.list(modules.keys())
            self.output.write('\nEnter any module name to get more help.  Or, type "modules spam" to search\nfor modules whose descriptions contain the word "spam".\n')


help = Helper(sys.stdin, sys.stdout)

class Scanner():
    __module__ = __name__

    def __init__(self, roots, children, descendp):
        self.roots = roots[:]
        self.state = []
        self.children = children
        self.descendp = descendp

    def next(self):
        if not self.state:
            if not self.roots:
                return None
            root = self.roots.pop(0)
            self.state = [(root, self.children(root))]
        node, children = self.state[-1]
        if not children:
            self.state.pop()
            return self.next()
        child = children.pop(0)
        if self.descendp(child):
            self.state.append((child, self.children(child)))
        return child


class ModuleScanner(Scanner):
    __module__ = __name__

    def __init__(self):
        roots = map(lambda dir: (dir, ''), pathdirs())
        Scanner.__init__(self, roots, self.submodules, self.isnewpackage)
        self.inodes = map(lambda (dir, pkg): os.stat(dir).st_ino, roots)

    def submodules(self, (dir, package)):
        children = []
        for file in os.listdir(dir):
            path = os.path.join(dir, file)
            if ispackage(path):
                children.append((path, package + (package and '.') + file))
            else:
                children.append((path, package))

        children.sort()
        return children

    def isnewpackage(self, (dir, package)):
        if os.path.exists(dir):
            inode = os.stat(dir).st_ino
            os.path.islink(dir) and (inode in self.inodes or self.inodes.append(inode))
            return ispackage(dir)
        return False

    def run(self, callback, key = None, completer = None):
        if key:
            key = lower(key)
        self.quit = False
        seen = {}
        for modname in sys.builtin_module_names:
            if modname != '__main__':
                seen[modname] = 1
                if key is None:
                    callback(None, modname, '')
                else:
                    desc = split(__import__(modname).__doc__ or '', '\n')[0]
                    if find(lower(modname + ' - ' + desc), key) >= 0:
                        callback(None, modname, desc)

        while not self.quit:
            node = self.next()
            if not node:
                break
            path, package = node
            modname = inspect.getmodulename(path)
            modname = os.path.isfile(path) and modname and package + (package and '.') + modname
            if modname not in seen:
                seen[modname] = 1
                if key is None:
                    callback(path, modname, '')
                elif not synopsis(path):
                    desc = ''
                    if find(lower(modname + ' - ' + desc), key) >= 0:
                        callback(path, modname, desc)

        if completer:
            completer()
        return


def apropos(key):

    def callback(path, modname, desc):
        if modname[-9:] == '.__init__':
            modname = modname[:-9] + ' (package)'
        print modname, desc and '- ' + desc

    try:
        import warnings
    except ImportError:
        pass
    else:
        warnings.filterwarnings('ignore')

    ModuleScanner().run(callback, key)


def serve(port, callback = None, completer = None):
    import BaseHTTPServer, mimetools, select

    class Message(mimetools.Message):
        __module__ = __name__

        def __init__(self, fp, seekable = 1):
            Message = self.__class__
            Message.__bases__[0].__bases__[0].__init__(self, fp, seekable)
            self.encodingheader = self.getheader('content-transfer-encoding')
            self.typeheader = self.getheader('content-type')
            self.parsetype()
            self.parseplist()

    class DocHandler(BaseHTTPServer.BaseHTTPRequestHandler):
        __module__ = __name__

        def send_document(self, title, contents):
            try:
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()
                self.wfile.write(html.page(title, contents))
            except IOError:
                pass

        def do_GET(self):
            path = self.path
            if path[-5:] == '.html':
                path = path[:-5]
            if path[:1] == '/':
                path = path[1:]
            if path and path != '.':
                try:
                    obj = locate(path, forceload=1)
                except ErrorDuringImport as value:
                    self.send_document(path, html.escape(str(value)))
                    return

                if obj:
                    self.send_document(describe(obj), html.document(obj, path))
                else:
                    self.send_document(path, 'no Python documentation found for %s' % repr(path))
            else:
                heading = html.heading('<big><big><strong>Python: Index of Modules</strong></big></big>', '#ffffff', '#7799ee')

                def bltinlink(name):
                    return '<a href="%s.html">%s</a>' % (name, name)

                names = filter(lambda x: x != '__main__', sys.builtin_module_names)
                contents = html.multicolumn(names, bltinlink)
                indices = ['<p>' + html.bigsection('Built-in Modules', '#ffffff', '#ee77aa', contents)]
                seen = {}
                for dir in pathdirs():
                    indices.append(html.index(dir, seen))

                contents = heading + join(indices) + '<p align=right>\n<font color="#909090" face="helvetica, arial"><strong>\npydoc</strong> by Ka-Ping Yee &lt;ping@lfw.org&gt;</font>'
                self.send_document('Index of Modules', contents)

        def log_message(self, *args):
            pass

    class DocServer(BaseHTTPServer.HTTPServer):
        __module__ = __name__

        def __init__(self, port, callback):
            host = sys.platform == 'mac' and '127.0.0.1' or 'localhost'
            self.address = ('', port)
            self.url = 'http://%s:%d/' % (host, port)
            self.callback = callback
            self.base.__init__(self, self.address, self.handler)

        def serve_until_quit(self):
            import select
            self.quit = False
            while not self.quit:
                rd, wr, ex = select.select([self.socket.fileno()], [], [], 1)
                if rd:
                    self.handle_request()

        def server_activate(self):
            self.base.server_activate(self)
            if self.callback:
                self.callback(self)

    DocServer.base = BaseHTTPServer.HTTPServer
    DocServer.handler = DocHandler
    DocHandler.MessageClass = Message
    try:
        DocServer(port, callback).serve_until_quit()
    except (KeyboardInterrupt, select.error):
        pass
    finally:
        if completer:
            completer()


def gui():

    class GUI():
        __module__ = __name__

        def __init__(self, window, port = 7464):
            self.window = window
            self.server = None
            self.scanner = None
            import Tkinter
            self.server_frm = Tkinter.Frame(window)
            self.title_lbl = Tkinter.Label(self.server_frm, text='Starting server...\n ')
            self.open_btn = Tkinter.Button(self.server_frm, text='open browser', command=self.open, state='disabled')
            self.quit_btn = Tkinter.Button(self.server_frm, text='quit serving', command=self.quit, state='disabled')
            self.search_frm = Tkinter.Frame(window)
            self.search_lbl = Tkinter.Label(self.search_frm, text='Search for')
            self.search_ent = Tkinter.Entry(self.search_frm)
            self.search_ent.bind('<Return>', self.search)
            self.stop_btn = Tkinter.Button(self.search_frm, text='stop', pady=0, command=self.stop, state='disabled')
            if sys.platform == 'win32':
                self.stop_btn.pack(side='right')
            self.window.title('pydoc')
            self.window.protocol('WM_DELETE_WINDOW', self.quit)
            self.title_lbl.pack(side='top', fill='x')
            self.open_btn.pack(side='left', fill='x', expand=1)
            self.quit_btn.pack(side='right', fill='x', expand=1)
            self.server_frm.pack(side='top', fill='x')
            self.search_lbl.pack(side='left')
            self.search_ent.pack(side='right', fill='x', expand=1)
            self.search_frm.pack(side='top', fill='x')
            self.search_ent.focus_set()
            font = ('helvetica', sys.platform == 'win32' and 8 or 10)
            self.result_lst = Tkinter.Listbox(window, font=font, height=6)
            self.result_lst.bind('<Button-1>', self.select)
            self.result_lst.bind('<Double-Button-1>', self.goto)
            self.result_scr = Tkinter.Scrollbar(window, orient='vertical', command=self.result_lst.yview)
            self.result_lst.config(yscrollcommand=self.result_scr.set)
            self.result_frm = Tkinter.Frame(window)
            self.goto_btn = Tkinter.Button(self.result_frm, text='go to selected', command=self.goto)
            self.hide_btn = Tkinter.Button(self.result_frm, text='hide results', command=self.hide)
            self.goto_btn.pack(side='left', fill='x', expand=1)
            self.hide_btn.pack(side='right', fill='x', expand=1)
            self.window.update()
            self.minwidth = self.window.winfo_width()
            self.minheight = self.window.winfo_height()
            self.bigminheight = self.server_frm.winfo_reqheight() + self.search_frm.winfo_reqheight() + self.result_lst.winfo_reqheight() + self.result_frm.winfo_reqheight()
            self.bigwidth, self.bigheight = self.minwidth, self.bigminheight
            self.expanded = 0
            self.window.wm_geometry('%dx%d' % (self.minwidth, self.minheight))
            self.window.wm_minsize(self.minwidth, self.minheight)
            self.window.tk.willdispatch()
            import threading
            threading.Thread(target=serve, args=(port, self.ready, self.quit)).start()
            return

        def ready(self, server):
            self.server = server
            self.title_lbl.config(text='Python documentation server at\n' + server.url)
            self.open_btn.config(state='normal')
            self.quit_btn.config(state='normal')

        def open(self, event = None, url = None):
            url = url or self.server.url
            try:
                import webbrowser
                webbrowser.open(url)
            except ImportError:
                if sys.platform == 'win32':
                    os.system('start "%s"' % url)
                elif sys.platform == 'mac':
                    try:
                        import ic
                    except ImportError:
                        pass
                    else:
                        ic.launchurl(url)

                else:
                    rc = os.system('netscape -remote "openURL(%s)" &' % url)
                    if rc:
                        os.system('netscape "%s" &' % url)

        def quit(self, event = None):
            if self.server:
                self.server.quit = 1
            self.window.quit()

        def search(self, event = None):
            key = self.search_ent.get()
            self.stop_btn.pack(side='right')
            self.stop_btn.config(state='normal')
            self.search_lbl.config(text='Searching for "%s"...' % key)
            self.search_ent.forget()
            self.search_lbl.pack(side='left')
            self.result_lst.delete(0, 'end')
            self.goto_btn.config(state='disabled')
            self.expand()
            import threading
            if self.scanner:
                self.scanner.quit = 1
            self.scanner = ModuleScanner()
            threading.Thread(target=self.scanner.run, args=(self.update, key, self.done)).start()

        def update(self, path, modname, desc):
            if modname[-9:] == '.__init__':
                modname = modname[:-9] + ' (package)'
            self.result_lst.insert('end', modname + ' - ' + (desc or '(no description)'))

        def stop(self, event = None):
            if self.scanner:
                self.scanner.quit = 1
                self.scanner = None
            return

        def done(self):
            self.scanner = None
            self.search_lbl.config(text='Search for')
            self.search_lbl.pack(side='left')
            self.search_ent.pack(side='right', fill='x', expand=1)
            if sys.platform != 'win32':
                self.stop_btn.forget()
            self.stop_btn.config(state='disabled')
            return

        def select(self, event = None):
            self.goto_btn.config(state='normal')

        def goto(self, event = None):
            selection = self.result_lst.curselection()
            if selection:
                modname = split(self.result_lst.get(selection[0]))[0]
                self.open(url=self.server.url + modname + '.html')

        def collapse(self):
            if not self.expanded:
                return
            self.result_frm.forget()
            self.result_scr.forget()
            self.result_lst.forget()
            self.bigwidth = self.window.winfo_width()
            self.bigheight = self.window.winfo_height()
            self.window.wm_geometry('%dx%d' % (self.minwidth, self.minheight))
            self.window.wm_minsize(self.minwidth, self.minheight)
            self.expanded = 0

        def expand(self):
            if self.expanded:
                return
            self.result_frm.pack(side='bottom', fill='x')
            self.result_scr.pack(side='right', fill='y')
            self.result_lst.pack(side='top', fill='both', expand=1)
            self.window.wm_geometry('%dx%d' % (self.bigwidth, self.bigheight))
            self.window.wm_minsize(self.minwidth, self.bigminheight)
            self.expanded = 1

        def hide(self, event = None):
            self.stop()
            self.collapse()

    import Tkinter
    try:
        root = Tkinter.Tk()
        try:
            gui = GUI(root)
            root.mainloop()
        finally:
            root.destroy()

    except KeyboardInterrupt:
        pass


def ispath(x):
    return isinstance(x, str) and find(x, os.sep) >= 0


def cli():
    import getopt

    class BadUsage():
        __module__ = __name__

    scriptdir = os.path.dirname(sys.argv[0])
    if scriptdir in sys.path:
        sys.path.remove(scriptdir)
    sys.path.insert(0, '.')
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'gk:p:w')
        writing = 0
        for opt, val in opts:
            if opt == '-g':
                gui()
                return
            if opt == '-k':
                apropos(val)
                return
            if opt == '-p':
                try:
                    port = int(val)
                except ValueError:
                    raise BadUsage

                def ready(server):
                    print 'pydoc server ready at %s' % server.url

                def stopped():
                    print 'pydoc server stopped'

                serve(port, ready, stopped)
                return
            if opt == '-w':
                writing = 1

        if not args:
            raise BadUsage
        for arg in args:
            if ispath(arg) and not os.path.exists(arg):
                print 'file %r does not exist' % arg
                break
            try:
                if ispath(arg) and os.path.isfile(arg):
                    arg = importfile(arg)
                if writing:
                    if ispath(arg) and os.path.isdir(arg):
                        writedocs(arg)
                    else:
                        writedoc(arg)
                else:
                    help.help(arg)
            except ErrorDuringImport as value:
                print value

    except (getopt.error, BadUsage):
        cmd = os.path.basename(sys.argv[0])
        print "pydoc - the Python documentation tool\n\n%s <name> ...\n    Show text documentation on something.  <name> may be the name of a\n    Python keyword, topic, function, module, or package, or a dotted\n    reference to a class or function within a module or module in a\n    package.  If <name> contains a '%s', it is used as the path to a\n    Python source file to document. If name is 'keywords', 'topics',\n    or 'modules', a listing of these things is displayed.\n\n%s -k <keyword>\n    Search for a keyword in the synopsis lines of all available modules.\n\n%s -p <port>\n    Start an HTTP server on the given port on the local machine.\n\n%s -g\n    Pop up a graphical interface for finding and serving documentation.\n\n%s -w <name> ...\n    Write out the HTML documentation for a module to a file in the current\n    directory.  If <name> contains a '%s', it is treated as a filename; if\n    it names a directory, documentation is written for all the contents.\n" % (cmd,
         os.sep,
         cmd,
         cmd,
         cmd,
         cmd,
         os.sep)


if __name__ == '__main__':
    cli()
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\pydoc.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:13:23 Pacific Daylight Time
