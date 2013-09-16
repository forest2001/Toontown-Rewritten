# 2013.08.22 22:13:32 Pacific Daylight Time
# Embedded file name: string
whitespace = ' \t\n\r\x0b\x0c'
lowercase = 'abcdefghijklmnopqrstuvwxyz'
uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
letters = lowercase + uppercase
ascii_lowercase = lowercase
ascii_uppercase = uppercase
ascii_letters = ascii_lowercase + ascii_uppercase
digits = '0123456789'
hexdigits = digits + 'abcdef' + 'ABCDEF'
octdigits = '01234567'
punctuation = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
printable = digits + letters + punctuation + whitespace
l = map(chr, xrange(256))
_idmap = str('').join(l)
del l

def capwords(s, sep = None):
    return sep or ' '.join([ x.capitalize() for x in s.split(sep) ])


_idmapL = None

def maketrans(fromstr, tostr):
    global _idmapL
    if len(fromstr) != len(tostr):
        raise ValueError, 'maketrans arguments must have same length'
    if not _idmapL:
        _idmapL = map(None, _idmap)
    L = _idmapL[:]
    fromstr = map(ord, fromstr)
    for i in range(len(fromstr)):
        L[fromstr[i]] = tostr[i]

    return ''.join(L)


import re as _re

class _multimap():
    __module__ = __name__

    def __init__(self, primary, secondary):
        self._primary = primary
        self._secondary = secondary

    def __getitem__(self, key):
        try:
            return self._primary[key]
        except KeyError:
            return self._secondary[key]


class _TemplateMetaclass(type):
    __module__ = __name__
    pattern = '\n    %(delim)s(?:\n      (?P<escaped>%(delim)s) |   # Escape sequence of two delimiters\n      (?P<named>%(id)s)      |   # delimiter and a Python identifier\n      {(?P<braced>%(id)s)}   |   # delimiter and a braced identifier\n      (?P<invalid>)              # Other ill-formed delimiter exprs\n    )\n    '

    def __init__(cls, name, bases, dct):
        super(_TemplateMetaclass, cls).__init__(name, bases, dct)
        if 'pattern' in dct:
            pattern = cls.pattern
        else:
            pattern = _TemplateMetaclass.pattern % {'delim': _re.escape(cls.delimiter),
             'id': cls.idpattern}
        cls.pattern = _re.compile(pattern, _re.IGNORECASE | _re.VERBOSE)


class Template():
    __module__ = __name__
    __metaclass__ = _TemplateMetaclass
    delimiter = '$'
    idpattern = '[_a-z][_a-z0-9]*'

    def __init__(self, template):
        self.template = template

    def _invalid(self, mo):
        i = mo.start('invalid')
        lines = self.template[:i].splitlines(True)
        if not lines:
            colno = 1
            lineno = 1
        else:
            colno = i - len(''.join(lines[:-1]))
            lineno = len(lines)
        raise ValueError('Invalid placeholder in string: line %d, col %d' % (lineno, colno))

    def substitute(self, *args, **kws):
        if len(args) > 1:
            raise TypeError('Too many positional arguments')
        if not args:
            mapping = kws
        elif kws:
            mapping = _multimap(kws, args[0])
        else:
            mapping = args[0]

        def convert(mo):
            if not mo.group('named'):
                named = mo.group('braced')
                if named is not None:
                    val = mapping[named]
                    return '%s' % val
                if mo.group('escaped') is not None:
                    return self.delimiter
                mo.group('invalid') is not None and self._invalid(mo)
            raise ValueError('Unrecognized named group in pattern', self.pattern)
            return

        return self.pattern.sub(convert, self.template)

    def safe_substitute(self, *args, **kws):
        if len(args) > 1:
            raise TypeError('Too many positional arguments')
        if not args:
            mapping = kws
        elif kws:
            mapping = _multimap(kws, args[0])
        else:
            mapping = args[0]

        def convert(mo):
            named = mo.group('named')
            if named is not None:
                try:
                    return '%s' % mapping[named]
                except KeyError:
                    return self.delimiter + named

            braced = mo.group('braced')
            if braced is not None:
                try:
                    return '%s' % mapping[braced]
                except KeyError:
                    return self.delimiter + '{' + braced + '}'

            if mo.group('escaped') is not None:
                return self.delimiter
            if mo.group('invalid') is not None:
                return self.delimiter
            raise ValueError('Unrecognized named group in pattern', self.pattern)
            return

        return self.pattern.sub(convert, self.template)


index_error = ValueError
atoi_error = ValueError
atof_error = ValueError
atol_error = ValueError

def lower(s):
    return s.lower()


def upper(s):
    return s.upper()


def swapcase(s):
    return s.swapcase()


def strip(s, chars = None):
    return s.strip(chars)


def lstrip(s, chars = None):
    return s.lstrip(chars)


def rstrip(s, chars = None):
    return s.rstrip(chars)


def split(s, sep = None, maxsplit = -1):
    return s.split(sep, maxsplit)


splitfields = split

def rsplit(s, sep = None, maxsplit = -1):
    return s.rsplit(sep, maxsplit)


def join(words, sep = ' '):
    return sep.join(words)


joinfields = join

def index(s, *args):
    return s.index(*args)


def rindex(s, *args):
    return s.rindex(*args)


def count(s, *args):
    return s.count(*args)


def find(s, *args):
    return s.find(*args)


def rfind(s, *args):
    return s.rfind(*args)


_float = float
_int = int
_long = long

def atof(s):
    return _float(s)


def atoi(s, base = 10):
    return _int(s, base)


def atol(s, base = 10):
    return _long(s, base)


def ljust(s, width, *args):
    return s.ljust(width, *args)


def rjust(s, width, *args):
    return s.rjust(width, *args)


def center(s, width, *args):
    return s.center(width, *args)


def zfill(x, width):
    if not isinstance(x, basestring):
        x = repr(x)
    return x.zfill(width)


def expandtabs(s, tabsize = 8):
    return s.expandtabs(tabsize)


def translate(s, table, deletions = ''):
    if deletions:
        return s.translate(table, deletions)
    else:
        return s.translate(table + s[:0])


def capitalize(s):
    return s.capitalize()


def replace(s, old, new, maxsplit = -1):
    return s.replace(old, new, maxsplit)


try:
    from strop import maketrans, lowercase, uppercase, whitespace
    letters = lowercase + uppercase
except ImportError:
    pass
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\string.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:13:32 Pacific Daylight Time
