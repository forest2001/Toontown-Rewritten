# 2013.08.22 22:12:57 Pacific Daylight Time
# Embedded file name: doctest
__docformat__ = 'reStructuredText en'
__all__ = ['register_optionflag',
 'DONT_ACCEPT_TRUE_FOR_1',
 'DONT_ACCEPT_BLANKLINE',
 'NORMALIZE_WHITESPACE',
 'ELLIPSIS',
 'IGNORE_EXCEPTION_DETAIL',
 'COMPARISON_FLAGS',
 'REPORT_UDIFF',
 'REPORT_CDIFF',
 'REPORT_NDIFF',
 'REPORT_ONLY_FIRST_FAILURE',
 'REPORTING_FLAGS',
 'is_private',
 'Example',
 'DocTest',
 'DocTestParser',
 'DocTestFinder',
 'DocTestRunner',
 'OutputChecker',
 'DocTestFailure',
 'UnexpectedException',
 'DebugRunner',
 'testmod',
 'testfile',
 'run_docstring_examples',
 'Tester',
 'DocTestSuite',
 'DocFileSuite',
 'set_unittest_reportflags',
 'script_from_examples',
 'testsource',
 'debug_src',
 'debug']
import __future__
import sys, traceback, inspect, linecache, os, re, types
import unittest, difflib, pdb, tempfile
import warnings
from StringIO import StringIO
warnings.filterwarnings('ignore', 'is_private', DeprecationWarning, __name__, 0)
OPTIONFLAGS_BY_NAME = {}

def register_optionflag(name):
    flag = 1 << len(OPTIONFLAGS_BY_NAME)
    OPTIONFLAGS_BY_NAME[name] = flag
    return flag


DONT_ACCEPT_TRUE_FOR_1 = register_optionflag('DONT_ACCEPT_TRUE_FOR_1')
DONT_ACCEPT_BLANKLINE = register_optionflag('DONT_ACCEPT_BLANKLINE')
NORMALIZE_WHITESPACE = register_optionflag('NORMALIZE_WHITESPACE')
ELLIPSIS = register_optionflag('ELLIPSIS')
IGNORE_EXCEPTION_DETAIL = register_optionflag('IGNORE_EXCEPTION_DETAIL')
COMPARISON_FLAGS = DONT_ACCEPT_TRUE_FOR_1 | DONT_ACCEPT_BLANKLINE | NORMALIZE_WHITESPACE | ELLIPSIS | IGNORE_EXCEPTION_DETAIL
REPORT_UDIFF = register_optionflag('REPORT_UDIFF')
REPORT_CDIFF = register_optionflag('REPORT_CDIFF')
REPORT_NDIFF = register_optionflag('REPORT_NDIFF')
REPORT_ONLY_FIRST_FAILURE = register_optionflag('REPORT_ONLY_FIRST_FAILURE')
REPORTING_FLAGS = REPORT_UDIFF | REPORT_CDIFF | REPORT_NDIFF | REPORT_ONLY_FIRST_FAILURE
BLANKLINE_MARKER = '<BLANKLINE>'
ELLIPSIS_MARKER = '...'

def is_private(prefix, base):
    warnings.warn("is_private is deprecated; it wasn't useful; examine DocTestFinder.find() lists instead", DeprecationWarning, stacklevel=2)
    return base[:1] == '_' and not base[:2] == '__' == base[-2:]


def _extract_future_flags(globs):
    flags = 0
    for fname in __future__.all_feature_names:
        feature = globs.get(fname, None)
        if feature is getattr(__future__, fname):
            flags |= feature.compiler_flag

    return flags


def _normalize_module(module, depth = 2):
    if inspect.ismodule(module):
        return module
    elif isinstance(module, (str, unicode)):
        return __import__(module, globals(), locals(), ['*'])
    elif module is None:
        return sys.modules[sys._getframe(depth).f_globals['__name__']]
    else:
        raise TypeError('Expected a module, string, or None')
    return


def _indent(s, indent = 4):
    return re.sub('(?m)^(?!$)', indent * ' ', s)


def _exception_traceback(exc_info):
    excout = StringIO()
    exc_type, exc_val, exc_tb = exc_info
    traceback.print_exception(exc_type, exc_val, exc_tb, file=excout)
    return excout.getvalue()


class _SpoofOut(StringIO):
    __module__ = __name__

    def getvalue(self):
        result = StringIO.getvalue(self)
        if result and not result.endswith('\n'):
            result += '\n'
        if hasattr(self, 'softspace'):
            del self.softspace
        return result

    def truncate(self, size = None):
        StringIO.truncate(self, size)
        if hasattr(self, 'softspace'):
            del self.softspace


def _ellipsis_match(want, got):
    if ELLIPSIS_MARKER not in want:
        return want == got
    ws = want.split(ELLIPSIS_MARKER)
    startpos, endpos = 0, len(got)
    w = ws[0]
    if w:
        if got.startswith(w):
            startpos = len(w)
            del ws[0]
        else:
            return False
    w = ws[-1]
    if w:
        if got.endswith(w):
            endpos -= len(w)
            del ws[-1]
        else:
            return False
    if startpos > endpos:
        return False
    for w in ws:
        startpos = got.find(w, startpos, endpos)
        if startpos < 0:
            return False
        startpos += len(w)

    return True


def _comment_line(line):
    line = line.rstrip()
    if line:
        return '# ' + line
    else:
        return '#'


class _OutputRedirectingPdb(pdb.Pdb):
    __module__ = __name__

    def __init__(self, out):
        self.__out = out
        pdb.Pdb.__init__(self)

    def trace_dispatch(self, *args):
        save_stdout = sys.stdout
        sys.stdout = self.__out
        try:
            return pdb.Pdb.trace_dispatch(self, *args)
        finally:
            sys.stdout = save_stdout


def _module_relative_path(module, path):
    if not inspect.ismodule(module):
        raise TypeError, 'Expected a module: %r' % module
    if path.startswith('/'):
        raise ValueError, 'Module-relative files may not have absolute paths'
    if hasattr(module, '__file__'):
        basedir = os.path.split(module.__file__)[0]
    elif module.__name__ == '__main__':
        if len(sys.argv) > 0 and sys.argv[0] != '':
            basedir = os.path.split(sys.argv[0])[0]
        else:
            basedir = os.curdir
    else:
        raise ValueError("Can't resolve paths relative to the module " + module + ' (it has no __file__)')
    return os.path.join(basedir, *path.split('/'))


class Example():
    __module__ = __name__

    def __init__(self, source, want, exc_msg = None, lineno = 0, indent = 0, options = None):
        if not source.endswith('\n'):
            source += '\n'
        if want and not want.endswith('\n'):
            want += '\n'
        if exc_msg is not None and not exc_msg.endswith('\n'):
            exc_msg += '\n'
        self.source = source
        self.want = want
        self.lineno = lineno
        self.indent = indent
        if options is None:
            options = {}
        self.options = options
        self.exc_msg = exc_msg
        return


class DocTest():
    __module__ = __name__

    def __init__(self, examples, globs, name, filename, lineno, docstring):
        self.examples = examples
        self.docstring = docstring
        self.globs = globs.copy()
        self.name = name
        self.filename = filename
        self.lineno = lineno

    def __repr__(self):
        if len(self.examples) == 0:
            examples = 'no examples'
        elif len(self.examples) == 1:
            examples = '1 example'
        else:
            examples = '%d examples' % len(self.examples)
        return '<DocTest %s from %s:%s (%s)>' % (self.name,
         self.filename,
         self.lineno,
         examples)

    def __cmp__(self, other):
        if not isinstance(other, DocTest):
            return -1
        return cmp((self.name,
         self.filename,
         self.lineno,
         id(self)), (other.name,
         other.filename,
         other.lineno,
         id(other)))


class DocTestParser():
    __module__ = __name__
    _EXAMPLE_RE = re.compile('\n        # Source consists of a PS1 line followed by zero or more PS2 lines.\n        (?P<source>\n            (?:^(?P<indent> [ ]*) >>>    .*)    # PS1 line\n            (?:\\n           [ ]*  \\.\\.\\. .*)*)  # PS2 lines\n        \\n?\n        # Want consists of any non-blank lines that do not start with PS1.\n        (?P<want> (?:(?![ ]*$)    # Not a blank line\n                     (?![ ]*>>>)  # Not a line starting with PS1\n                     .*$\\n?       # But any other line\n                  )*)\n        ', re.MULTILINE | re.VERBOSE)
    _EXCEPTION_RE = re.compile("\n        # Grab the traceback header.  Different versions of Python have\n        # said different things on the first traceback line.\n        ^(?P<hdr> Traceback\\ \\(\n            (?: most\\ recent\\ call\\ last\n            |   innermost\\ last\n            ) \\) :\n        )\n        \\s* $                # toss trailing whitespace on the header.\n        (?P<stack> .*?)      # don't blink: absorb stuff until...\n        ^ (?P<msg> \\w+ .*)   #     a line *starts* with alphanum.\n        ", re.VERBOSE | re.MULTILINE | re.DOTALL)
    _IS_BLANK_OR_COMMENT = re.compile('^[ ]*(#.*)?$').match

    def parse(self, string, name = '<string>'):
        string = string.expandtabs()
        min_indent = self._min_indent(string)
        if min_indent > 0:
            string = '\n'.join([ l[min_indent:] for l in string.split('\n') ])
        output = []
        charno, lineno = (0, 0)
        for m in self._EXAMPLE_RE.finditer(string):
            output.append(string[charno:m.start()])
            lineno += string.count('\n', charno, m.start())
            source, options, want, exc_msg = self._parse_example(m, name, lineno)
            if not self._IS_BLANK_OR_COMMENT(source):
                output.append(Example(source, want, exc_msg, lineno=lineno, indent=min_indent + len(m.group('indent')), options=options))
            lineno += string.count('\n', m.start(), m.end())
            charno = m.end()

        output.append(string[charno:])
        return output

    def get_doctest(self, string, globs, name, filename, lineno):
        return DocTest(self.get_examples(string, name), globs, name, filename, lineno, string)

    def get_examples(self, string, name = '<string>'):
        return [ x for x in self.parse(string, name) if isinstance(x, Example) ]

    def _parse_example(self, m, name, lineno):
        indent = len(m.group('indent'))
        source_lines = m.group('source').split('\n')
        self._check_prompt_blank(source_lines, indent, name, lineno)
        self._check_prefix(source_lines[1:], ' ' * indent + '.', name, lineno)
        source = '\n'.join([ sl[indent + 4:] for sl in source_lines ])
        want = m.group('want')
        want_lines = want.split('\n')
        if len(want_lines) > 1 and re.match(' *$', want_lines[-1]):
            del want_lines[-1]
        self._check_prefix(want_lines, ' ' * indent, name, lineno + len(source_lines))
        want = '\n'.join([ wl[indent:] for wl in want_lines ])
        m = self._EXCEPTION_RE.match(want)
        if m:
            exc_msg = m.group('msg')
        else:
            exc_msg = None
        options = self._find_options(source, name, lineno)
        return (source,
         options,
         want,
         exc_msg)

    _OPTION_DIRECTIVE_RE = re.compile('#\\s*doctest:\\s*([^\\n\\\'"]*)$', re.MULTILINE)

    def _find_options(self, source, name, lineno):
        options = {}
        for m in self._OPTION_DIRECTIVE_RE.finditer(source):
            option_strings = m.group(1).replace(',', ' ').split()
            for option in option_strings:
                if option[0] not in '+-' or option[1:] not in OPTIONFLAGS_BY_NAME:
                    raise ValueError('line %r of the doctest for %s has an invalid option: %r' % (lineno + 1, name, option))
                flag = OPTIONFLAGS_BY_NAME[option[1:]]
                options[flag] = option[0] == '+'

        if options and self._IS_BLANK_OR_COMMENT(source):
            raise ValueError('line %r of the doctest for %s has an option directive on a line with no example: %r' % (lineno, name, source))
        return options

    _INDENT_RE = re.compile('^([ ]*)(?=\\S)', re.MULTILINE)

    def _min_indent(self, s):
        indents = [ len(indent) for indent in self._INDENT_RE.findall(s) ]
        if len(indents) > 0:
            return min(indents)
        else:
            return 0

    def _check_prompt_blank(self, lines, indent, name, lineno):
        for i, line in enumerate(lines):
            if len(line) >= indent + 4 and line[indent + 3] != ' ':
                raise ValueError('line %r of the docstring for %s lacks blank after %s: %r' % (lineno + i + 1,
                 name,
                 line[indent:indent + 3],
                 line))

    def _check_prefix(self, lines, prefix, name, lineno):
        for i, line in enumerate(lines):
            if line and not line.startswith(prefix):
                raise ValueError('line %r of the docstring for %s has inconsistent leading whitespace: %r' % (lineno + i + 1, name, line))


class DocTestFinder():
    __module__ = __name__

    def __init__(self, verbose = False, parser = DocTestParser(), recurse = True, _namefilter = None, exclude_empty = True):
        self._parser = parser
        self._verbose = verbose
        self._recurse = recurse
        self._exclude_empty = exclude_empty
        self._namefilter = _namefilter

    def find(self, obj, name = None, module = None, globs = None, extraglobs = None):
        if name is None:
            name = getattr(obj, '__name__', None)
            if name is None:
                raise ValueError("DocTestFinder.find: name must be given when obj.__name__ doesn't exist: %r" % (type(obj),))
        if module is False:
            module = None
        elif module is None:
            module = inspect.getmodule(obj)
        try:
            if not inspect.getsourcefile(obj):
                file = inspect.getfile(obj)
                source_lines = linecache.getlines(file)
                source_lines = source_lines or None
        except TypeError:
            source_lines = None

        if globs is None:
            if module is None:
                globs = {}
            else:
                globs = module.__dict__.copy()
        else:
            globs = globs.copy()
        if extraglobs is not None:
            globs.update(extraglobs)
        tests = []
        self._find(tests, obj, name, module, source_lines, globs, {})
        return tests

    def _filter(self, obj, prefix, base):
        return self._namefilter is not None and self._namefilter(prefix, base)

    def _from_module(self, module, object):
        if module is None:
            return True
        elif inspect.isfunction(object):
            return module.__dict__ is object.func_globals
        elif inspect.isclass(object):
            return module.__name__ == object.__module__
        elif inspect.getmodule(object) is not None:
            return module is inspect.getmodule(object)
        elif hasattr(object, '__module__'):
            return module.__name__ == object.__module__
        elif isinstance(object, property):
            return True
        else:
            raise ValueError('object must be a class or function')
        return

    def _find(self, tests, obj, name, module, source_lines, globs, seen):
        if self._verbose:
            print 'Finding tests in %s' % name
        if id(obj) in seen:
            return
        seen[id(obj)] = 1
        test = self._get_test(obj, name, module, globs, source_lines)
        if test is not None:
            tests.append(test)
        if inspect.ismodule(obj) and self._recurse:
            for valname, val in obj.__dict__.items():
                if self._filter(val, name, valname):
                    continue
                valname = '%s.%s' % (name, valname)
                if (inspect.isfunction(val) or inspect.isclass(val)) and self._from_module(module, val):
                    self._find(tests, val, valname, module, source_lines, globs, seen)

        if inspect.ismodule(obj) and self._recurse:
            for valname, val in getattr(obj, '__test__', {}).items():
                if not isinstance(valname, basestring):
                    raise ValueError('DocTestFinder.find: __test__ keys must be strings: %r' % (type(valname),))
                if not inspect.isfunction(val):
                    raise inspect.isclass(val) or inspect.ismethod(val) or inspect.ismodule(val) or isinstance(val, basestring) or ValueError('DocTestFinder.find: __test__ values must be strings, functions, methods, classes, or modules: %r' % (type(val),))
                valname = '%s.__test__.%s' % (name, valname)
                self._find(tests, val, valname, module, source_lines, globs, seen)

        if inspect.isclass(obj) and self._recurse:
            for valname, val in obj.__dict__.items():
                if self._filter(val, name, valname):
                    continue
                if isinstance(val, staticmethod):
                    val = getattr(obj, valname)
                if isinstance(val, classmethod):
                    val = getattr(obj, valname).im_func
                if (inspect.isfunction(val) or inspect.isclass(val) or isinstance(val, property)) and self._from_module(module, val):
                    valname = '%s.%s' % (name, valname)
                    self._find(tests, val, valname, module, source_lines, globs, seen)

        return

    def _get_test(self, obj, name, module, globs, source_lines):
        if isinstance(obj, basestring):
            docstring = obj
        else:
            try:
                if obj.__doc__ is None:
                    docstring = ''
                else:
                    docstring = obj.__doc__
                    if not isinstance(docstring, basestring):
                        docstring = str(docstring)
            except (TypeError, AttributeError):
                docstring = ''

        lineno = self._find_lineno(obj, source_lines)
        if self._exclude_empty and not docstring:
            return
        if module is None:
            filename = None
        else:
            filename = getattr(module, '__file__', module.__name__)
            if filename[-4:] in ('.pyc', '.pyo'):
                filename = filename[:-1]
        return self._parser.get_doctest(docstring, globs, name, filename, lineno)

    def _find_lineno(self, obj, source_lines):
        lineno = None
        if inspect.ismodule(obj):
            lineno = 0
        if inspect.isclass(obj):
            if source_lines is None:
                return
            pat = re.compile('^\\s*class\\s*%s\\b' % getattr(obj, '__name__', '-'))
            for i, line in enumerate(source_lines):
                if pat.match(line):
                    lineno = i
                    break

        if inspect.ismethod(obj):
            obj = obj.im_func
        if inspect.isfunction(obj):
            obj = obj.func_code
        if inspect.istraceback(obj):
            obj = obj.tb_frame
        if inspect.isframe(obj):
            obj = obj.f_code
        if inspect.iscode(obj):
            lineno = getattr(obj, 'co_firstlineno', None) - 1
        if lineno is not None:
            if source_lines is None:
                return lineno + 1
            pat = re.compile('(^|.*:)\\s*\\w*("|\')')
            for lineno in range(lineno, len(source_lines)):
                if pat.match(source_lines[lineno]):
                    return lineno

        return


class DocTestRunner():
    __module__ = __name__
    DIVIDER = '*' * 70

    def __init__(self, checker = None, verbose = None, optionflags = 0):
        if not checker:
            self._checker = OutputChecker()
            verbose = verbose is None and '-v' in sys.argv
        self._verbose = verbose
        self.optionflags = optionflags
        self.original_optionflags = optionflags
        self.tries = 0
        self.failures = 0
        self._name2ft = {}
        self._fakeout = _SpoofOut()
        return

    def report_start(self, out, test, example):
        if self._verbose:
            if example.want:
                out('Trying:\n' + _indent(example.source) + 'Expecting:\n' + _indent(example.want))
            else:
                out('Trying:\n' + _indent(example.source) + 'Expecting nothing\n')

    def report_success(self, out, test, example, got):
        if self._verbose:
            out('ok\n')

    def report_failure(self, out, test, example, got):
        out(self._failure_header(test, example) + self._checker.output_difference(example, got, self.optionflags))

    def report_unexpected_exception(self, out, test, example, exc_info):
        out(self._failure_header(test, example) + 'Exception raised:\n' + _indent(_exception_traceback(exc_info)))

    def _failure_header(self, test, example):
        out = [self.DIVIDER]
        if test.filename:
            if test.lineno is not None and example.lineno is not None:
                lineno = test.lineno + example.lineno + 1
            else:
                lineno = '?'
            out.append('File "%s", line %s, in %s' % (test.filename, lineno, test.name))
        else:
            out.append('Line %s, in %s' % (example.lineno + 1, test.name))
        out.append('Failed example:')
        source = example.source
        out.append(_indent(source))
        return '\n'.join(out)

    def __run(self, test, compileflags, out):
        failures = tries = 0
        original_optionflags = self.optionflags
        SUCCESS, FAILURE, BOOM = range(3)
        check = self._checker.check_output
        for examplenum, example in enumerate(test.examples):
            if self.optionflags & REPORT_ONLY_FIRST_FAILURE:
                quiet = failures > 0
                self.optionflags = original_optionflags
                if example.options:
                    for optionflag, val in example.options.items():
                        if val:
                            self.optionflags |= optionflag
                        else:
                            self.optionflags &= ~optionflag

                tries += 1
                if not quiet:
                    self.report_start(out, test, example)
                filename = '<doctest %s[%d]>' % (test.name, examplenum)
                try:
                    exec compile(example.source, filename, 'single', compileflags, 1) in test.globs
                    self.debugger.set_continue()
                    exception = None
                except KeyboardInterrupt:
                    raise
                except:
                    exception = sys.exc_info()
                    self.debugger.set_continue()

                got = self._fakeout.getvalue()
                self._fakeout.truncate(0)
                outcome = FAILURE
                if exception is None:
                    if check(example.want, got, self.optionflags):
                        outcome = SUCCESS
                else:
                    exc_info = sys.exc_info()
                    exc_msg = traceback.format_exception_only(*exc_info[:2])[-1]
                    if not quiet:
                        got += _exception_traceback(exc_info)
                    if example.exc_msg is None:
                        outcome = BOOM
                    elif check(example.exc_msg, exc_msg, self.optionflags):
                        outcome = SUCCESS
                    elif self.optionflags & IGNORE_EXCEPTION_DETAIL:
                        m1 = re.match('[^:]*:', example.exc_msg)
                        m2 = re.match('[^:]*:', exc_msg)
                        if m1 and m2 and check(m1.group(0), m2.group(0), self.optionflags):
                            outcome = SUCCESS
                if outcome is SUCCESS:
                    quiet or self.report_success(out, test, example, got)
            elif outcome is FAILURE:
                if not quiet:
                    self.report_failure(out, test, example, got)
                failures += 1
            elif outcome is BOOM:
                if not quiet:
                    self.report_unexpected_exception(out, test, example, exc_info)
                failures += 1

        self.optionflags = original_optionflags
        self.__record_outcome(test, failures, tries)
        return (failures, tries)

    def __record_outcome(self, test, f, t):
        f2, t2 = self._name2ft.get(test.name, (0, 0))
        self._name2ft[test.name] = (f + f2, t + t2)
        self.failures += f
        self.tries += t

    __LINECACHE_FILENAME_RE = re.compile('<doctest (?P<name>[\\w\\.]+)\\[(?P<examplenum>\\d+)\\]>$')

    def __patched_linecache_getlines(self, filename):
        m = self.__LINECACHE_FILENAME_RE.match(filename)
        if m and m.group('name') == self.test.name:
            example = self.test.examples[int(m.group('examplenum'))]
            return example.source.splitlines(True)
        else:
            return self.save_linecache_getlines(filename)

    def run(self, test, compileflags = None, out = None, clear_globs = True):
        self.test = test
        if compileflags is None:
            compileflags = _extract_future_flags(test.globs)
        save_stdout = sys.stdout
        if out is None:
            out = save_stdout.write
        sys.stdout = self._fakeout
        save_set_trace = pdb.set_trace
        self.debugger = _OutputRedirectingPdb(save_stdout)
        self.debugger.reset()
        pdb.set_trace = self.debugger.set_trace
        self.save_linecache_getlines = linecache.getlines
        linecache.getlines = self.__patched_linecache_getlines
        try:
            return self.__run(test, compileflags, out)
        finally:
            sys.stdout = save_stdout
            pdb.set_trace = save_set_trace
            linecache.getlines = self.save_linecache_getlines
            if clear_globs:
                test.globs.clear()

        return

    def summarize(self, verbose = None):
        if verbose is None:
            verbose = self._verbose
        notests = []
        passed = []
        failed = []
        totalt = totalf = 0
        for x in self._name2ft.items():
            name, (f, t) = x
            totalt += t
            totalf += f
            if t == 0:
                notests.append(name)
            elif f == 0:
                passed.append((name, t))
            else:
                failed.append(x)

        if verbose:
            if notests:
                print len(notests), 'items had no tests:'
                notests.sort()
                for thing in notests:
                    print '   ', thing

            if passed:
                print len(passed), 'items passed all tests:'
                passed.sort()
                for thing, count in passed:
                    print ' %3d tests in %s' % (count, thing)

        if failed:
            print self.DIVIDER
            print len(failed), 'items had failures:'
            failed.sort()
            for thing, (f, t) in failed:
                print ' %3d of %3d in %s' % (f, t, thing)

        if verbose:
            print totalt, 'tests in', len(self._name2ft), 'items.'
            print totalt - totalf, 'passed and', totalf, 'failed.'
        if totalf:
            print '***Test Failed***', totalf, 'failures.'
        elif verbose:
            print 'Test passed.'
        return (totalf, totalt)

    def merge(self, other):
        d = self._name2ft
        for name, (f, t) in other._name2ft.items():
            if name in d:
                print "*** DocTestRunner.merge: '" + name + "' in both testers; summing outcomes."
                f2, t2 = d[name]
                f = f + f2
                t = t + t2
            d[name] = (f, t)


class OutputChecker():
    __module__ = __name__

    def check_output(self, want, got, optionflags):
        if got == want:
            return True
        if not optionflags & DONT_ACCEPT_TRUE_FOR_1:
            if (got, want) == ('True\n', '1\n'):
                return True
            if (got, want) == ('False\n', '0\n'):
                return True
        if not optionflags & DONT_ACCEPT_BLANKLINE:
            want = re.sub('(?m)^%s\\s*?$' % re.escape(BLANKLINE_MARKER), '', want)
            got = re.sub('(?m)^\\s*?$', '', got)
            if got == want:
                return True
        if optionflags & NORMALIZE_WHITESPACE:
            got = ' '.join(got.split())
            want = ' '.join(want.split())
            if got == want:
                return True
        if optionflags & ELLIPSIS:
            if _ellipsis_match(want, got):
                return True
        return False

    def _do_a_fancy_diff(self, want, got, optionflags):
        if not optionflags & (REPORT_UDIFF | REPORT_CDIFF | REPORT_NDIFF):
            return False
        if optionflags & REPORT_NDIFF:
            return True
        return want.count('\n') > 2 and got.count('\n') > 2

    def output_difference(self, example, got, optionflags):
        want = example.want
        if not optionflags & DONT_ACCEPT_BLANKLINE:
            got = re.sub('(?m)^[ ]*(?=\n)', BLANKLINE_MARKER, got)
        if self._do_a_fancy_diff(want, got, optionflags):
            want_lines = want.splitlines(True)
            got_lines = got.splitlines(True)
            if optionflags & REPORT_UDIFF:
                diff = difflib.unified_diff(want_lines, got_lines, n=2)
                diff = list(diff)[2:]
                kind = 'unified diff with -expected +actual'
            elif optionflags & REPORT_CDIFF:
                diff = difflib.context_diff(want_lines, got_lines, n=2)
                diff = list(diff)[2:]
                kind = 'context diff with expected followed by actual'
            elif optionflags & REPORT_NDIFF:
                engine = difflib.Differ(charjunk=difflib.IS_CHARACTER_JUNK)
                diff = list(engine.compare(want_lines, got_lines))
                kind = 'ndiff with -expected +actual'
            diff = [ line.rstrip() + '\n' for line in diff ]
            return 'Differences (%s):\n' % kind + _indent(''.join(diff))
        if want and got:
            return 'Expected:\n%sGot:\n%s' % (_indent(want), _indent(got))
        elif want:
            return 'Expected:\n%sGot nothing\n' % _indent(want)
        elif got:
            return 'Expected nothing\nGot:\n%s' % _indent(got)
        else:
            return 'Expected nothing\nGot nothing\n'


class DocTestFailure(Exception):
    __module__ = __name__

    def __init__(self, test, example, got):
        self.test = test
        self.example = example
        self.got = got

    def __str__(self):
        return str(self.test)


class UnexpectedException(Exception):
    __module__ = __name__

    def __init__(self, test, example, exc_info):
        self.test = test
        self.example = example
        self.exc_info = exc_info

    def __str__(self):
        return str(self.test)


class DebugRunner(DocTestRunner):
    __module__ = __name__

    def run(self, test, compileflags = None, out = None, clear_globs = True):
        r = DocTestRunner.run(self, test, compileflags, out, False)
        if clear_globs:
            test.globs.clear()
        return r

    def report_unexpected_exception(self, out, test, example, exc_info):
        raise UnexpectedException(test, example, exc_info)

    def report_failure(self, out, test, example, got):
        raise DocTestFailure(test, example, got)


master = None

def testmod(m = None, name = None, globs = None, verbose = None, isprivate = None, report = True, optionflags = 0, extraglobs = None, raise_on_error = False, exclude_empty = False):
    global master
    if isprivate is not None:
        warnings.warn('the isprivate argument is deprecated; examine DocTestFinder.find() lists instead', DeprecationWarning)
    if m is None:
        m = sys.modules.get('__main__')
    if not inspect.ismodule(m):
        raise TypeError('testmod: module required; %r' % (m,))
    if name is None:
        name = m.__name__
    finder = DocTestFinder(_namefilter=isprivate, exclude_empty=exclude_empty)
    if raise_on_error:
        runner = DebugRunner(verbose=verbose, optionflags=optionflags)
    else:
        runner = DocTestRunner(verbose=verbose, optionflags=optionflags)
    for test in finder.find(m, name, globs=globs, extraglobs=extraglobs):
        runner.run(test)

    if report:
        runner.summarize()
    if master is None:
        master = runner
    else:
        master.merge(runner)
    return (runner.failures, runner.tries)


def testfile(filename, module_relative = True, name = None, package = None, globs = None, verbose = None, report = True, optionflags = 0, extraglobs = None, raise_on_error = False, parser = DocTestParser()):
    global master
    if package and not module_relative:
        raise ValueError('Package may only be specified for module-relative paths.')
    if module_relative:
        package = _normalize_module(package)
        filename = _module_relative_path(package, filename)
    if name is None:
        name = os.path.basename(filename)
    if globs is None:
        globs = {}
    else:
        globs = globs.copy()
    if extraglobs is not None:
        globs.update(extraglobs)
    if raise_on_error:
        runner = DebugRunner(verbose=verbose, optionflags=optionflags)
    else:
        runner = DocTestRunner(verbose=verbose, optionflags=optionflags)
    s = open(filename).read()
    test = parser.get_doctest(s, globs, name, filename, 0)
    runner.run(test)
    if report:
        runner.summarize()
    if master is None:
        master = runner
    else:
        master.merge(runner)
    return (runner.failures, runner.tries)


def run_docstring_examples(f, globs, verbose = False, name = 'NoName', compileflags = None, optionflags = 0):
    finder = DocTestFinder(verbose=verbose, recurse=False)
    runner = DocTestRunner(verbose=verbose, optionflags=optionflags)
    for test in finder.find(f, name, globs=globs):
        runner.run(test, compileflags=compileflags)


class Tester():
    __module__ = __name__

    def __init__(self, mod = None, globs = None, verbose = None, isprivate = None, optionflags = 0):
        warnings.warn('class Tester is deprecated; use class doctest.DocTestRunner instead', DeprecationWarning, stacklevel=2)
        if mod is None and globs is None:
            raise TypeError('Tester.__init__: must specify mod or globs')
        if mod is not None and not inspect.ismodule(mod):
            raise TypeError('Tester.__init__: mod must be a module; %r' % (mod,))
        if globs is None:
            globs = mod.__dict__
        self.globs = globs
        self.verbose = verbose
        self.isprivate = isprivate
        self.optionflags = optionflags
        self.testfinder = DocTestFinder(_namefilter=isprivate)
        self.testrunner = DocTestRunner(verbose=verbose, optionflags=optionflags)
        return

    def runstring(self, s, name):
        test = DocTestParser().get_doctest(s, self.globs, name, None, None)
        if self.verbose:
            print 'Running string', name
        f, t = self.testrunner.run(test)
        if self.verbose:
            print f, 'of', t, 'examples failed in string', name
        return (f, t)

    def rundoc(self, object, name = None, module = None):
        f = t = 0
        tests = self.testfinder.find(object, name, module=module, globs=self.globs)
        for test in tests:
            f2, t2 = self.testrunner.run(test)
            f, t = f + f2, t + t2

        return (f, t)

    def rundict(self, d, name, module = None):
        import new
        m = new.module(name)
        m.__dict__.update(d)
        if module is None:
            module = False
        return self.rundoc(m, name, module)

    def run__test__(self, d, name):
        import new
        m = new.module(name)
        m.__test__ = d
        return self.rundoc(m, name)

    def summarize(self, verbose = None):
        return self.testrunner.summarize(verbose)

    def merge(self, other):
        self.testrunner.merge(other.testrunner)


_unittest_reportflags = 0

def set_unittest_reportflags(flags):
    global _unittest_reportflags
    if flags & REPORTING_FLAGS != flags:
        raise ValueError('Only reporting flags allowed', flags)
    old = _unittest_reportflags
    _unittest_reportflags = flags
    return old


class DocTestCase(unittest.TestCase):
    __module__ = __name__

    def __init__(self, test, optionflags = 0, setUp = None, tearDown = None, checker = None):
        unittest.TestCase.__init__(self)
        self._dt_optionflags = optionflags
        self._dt_checker = checker
        self._dt_test = test
        self._dt_setUp = setUp
        self._dt_tearDown = tearDown

    def setUp(self):
        test = self._dt_test
        if self._dt_setUp is not None:
            self._dt_setUp(test)
        return

    def tearDown(self):
        test = self._dt_test
        if self._dt_tearDown is not None:
            self._dt_tearDown(test)
        test.globs.clear()
        return

    def runTest(self):
        test = self._dt_test
        old = sys.stdout
        new = StringIO()
        optionflags = self._dt_optionflags
        if not optionflags & REPORTING_FLAGS:
            optionflags |= _unittest_reportflags
        runner = DocTestRunner(optionflags=optionflags, checker=self._dt_checker, verbose=False)
        try:
            runner.DIVIDER = '-' * 70
            failures, tries = runner.run(test, out=new.write, clear_globs=False)
        finally:
            sys.stdout = old

        if failures:
            raise self.failureException(self.format_failure(new.getvalue()))

    def format_failure(self, err):
        test = self._dt_test
        if test.lineno is None:
            lineno = 'unknown line number'
        else:
            lineno = '%s' % test.lineno
        lname = '.'.join(test.name.split('.')[-1:])
        return 'Failed doctest test for %s\n  File "%s", line %s, in %s\n\n%s' % (test.name,
         test.filename,
         lineno,
         lname,
         err)

    def debug(self):
        self.setUp()
        runner = DebugRunner(optionflags=self._dt_optionflags, checker=self._dt_checker, verbose=False)
        runner.run(self._dt_test)
        self.tearDown()

    def id(self):
        return self._dt_test.name

    def __repr__(self):
        name = self._dt_test.name.split('.')
        return '%s (%s)' % (name[-1], '.'.join(name[:-1]))

    __str__ = __repr__

    def shortDescription(self):
        return 'Doctest: ' + self._dt_test.name


def DocTestSuite(module = None, globs = None, extraglobs = None, test_finder = None, **options):
    if test_finder is None:
        test_finder = DocTestFinder()
    module = _normalize_module(module)
    tests = test_finder.find(module, globs=globs, extraglobs=extraglobs)
    if globs is None:
        globs = module.__dict__
    if not tests:
        raise ValueError(module, 'has no tests')
    tests.sort()
    suite = unittest.TestSuite()
    for test in tests:
        if len(test.examples) == 0:
            continue
        if not test.filename:
            filename = module.__file__
            if filename[-4:] in ('.pyc', '.pyo'):
                filename = filename[:-1]
            test.filename = filename
        suite.addTest(DocTestCase(test, **options))

    return suite


class DocFileCase(DocTestCase):
    __module__ = __name__

    def id(self):
        return '_'.join(self._dt_test.name.split('.'))

    def __repr__(self):
        return self._dt_test.filename

    __str__ = __repr__

    def format_failure(self, err):
        return 'Failed doctest test for %s\n  File "%s", line 0\n\n%s' % (self._dt_test.name, self._dt_test.filename, err)


def DocFileTest(path, module_relative = True, package = None, globs = None, parser = DocTestParser(), **options):
    if globs is None:
        globs = {}
    if package and not module_relative:
        raise ValueError('Package may only be specified for module-relative paths.')
    if module_relative:
        package = _normalize_module(package)
        path = _module_relative_path(package, path)
    name = os.path.basename(path)
    doc = open(path).read()
    test = parser.get_doctest(doc, globs, name, path, 0)
    return DocFileCase(test, **options)


def DocFileSuite(*paths, **kw):
    suite = unittest.TestSuite()
    if kw.get('module_relative', True):
        kw['package'] = _normalize_module(kw.get('package'))
    for path in paths:
        suite.addTest(DocFileTest(path, **kw))

    return suite


def script_from_examples(s):
    output = []
    for piece in DocTestParser().parse(s):
        if isinstance(piece, Example):
            output.append(piece.source[:-1])
            want = piece.want
            if want:
                output.append('# Expected:')
                output += [ '## ' + l for l in want.split('\n')[:-1] ]
        else:
            output += [ _comment_line(l) for l in piece.split('\n')[:-1] ]

    while output and output[-1] == '#':
        output.pop()

    while output and output[0] == '#':
        output.pop(0)

    return '\n'.join(output)


def testsource(module, name):
    module = _normalize_module(module)
    tests = DocTestFinder().find(module)
    test = [ t for t in tests if t.name == name ]
    if not test:
        raise ValueError(name, 'not found in tests')
    test = test[0]
    testsrc = script_from_examples(test.docstring)
    return testsrc


def debug_src(src, pm = False, globs = None):
    testsrc = script_from_examples(src)
    debug_script(testsrc, pm, globs)


def debug_script(src, pm = False, globs = None):
    import pdb
    srcfilename = tempfile.mktemp('.py', 'doctestdebug')
    f = open(srcfilename, 'w')
    f.write(src)
    f.close()
    try:
        if globs:
            globs = globs.copy()
        else:
            globs = {}
        if pm:
            try:
                execfile(srcfilename, globs, globs)
            except:
                print sys.exc_info()[1]
                pdb.post_mortem(sys.exc_info()[2])

        else:
            pdb.run('execfile(%r)' % srcfilename, globs, globs)
    finally:
        os.remove(srcfilename)


def debug(module, name, pm = False):
    module = _normalize_module(module)
    testsrc = testsource(module, name)
    debug_script(testsrc, pm, module.__dict__)


class _TestClass():
    __module__ = __name__

    def __init__(self, val):
        self.val = val

    def square(self):
        self.val = self.val ** 2
        return self

    def get(self):
        return self.val


__test__ = {'_TestClass': _TestClass,
 'string': '\n                      Example of a string object, searched as-is.\n                      >>> x = 1; y = 2\n                      >>> x + y, x * y\n                      (3, 2)\n                      ',
 'bool-int equivalence': '\n                                    In 2.2, boolean expressions displayed\n                                    0 or 1.  By default, we still accept\n                                    them.  This can be disabled by passing\n                                    DONT_ACCEPT_TRUE_FOR_1 to the new\n                                    optionflags argument.\n                                    >>> 4 == 4\n                                    1\n                                    >>> 4 == 4\n                                    True\n                                    >>> 4 > 4\n                                    0\n                                    >>> 4 > 4\n                                    False\n                                    ',
 'blank lines': "\n                Blank lines can be marked with <BLANKLINE>:\n                    >>> print 'foo\\n\\nbar\\n'\n                    foo\n                    <BLANKLINE>\n                    bar\n                    <BLANKLINE>\n            ",
 'ellipsis': "\n                If the ellipsis flag is used, then '...' can be used to\n                elide substrings in the desired output:\n                    >>> print range(1000) #doctest: +ELLIPSIS\n                    [0, 1, 2, ..., 999]\n            ",
 'whitespace normalization': '\n                If the whitespace normalization flag is used, then\n                differences in whitespace are ignored.\n                    >>> print range(30) #doctest: +NORMALIZE_WHITESPACE\n                    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14,\n                     15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26,\n                     27, 28, 29]\n            '}

def _test():
    r = unittest.TextTestRunner()
    r.run(DocTestSuite())


if __name__ == '__main__':
    _test()
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\doctest.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:12:59 Pacific Daylight Time
