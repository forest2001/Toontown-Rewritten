# 2013.08.22 22:13:35 Pacific Daylight Time
# Embedded file name: traceback
import linecache
import sys
import types
__all__ = ['extract_stack',
 'extract_tb',
 'format_exception',
 'format_exception_only',
 'format_list',
 'format_stack',
 'format_tb',
 'print_exc',
 'format_exc',
 'print_exception',
 'print_last',
 'print_stack',
 'print_tb',
 'tb_lineno']

def _print(file, str = '', terminator = '\n'):
    file.write(str + terminator)


def print_list(extracted_list, file = None):
    if file is None:
        file = sys.stderr
    for filename, lineno, name, line in extracted_list:
        _print(file, '  File "%s", line %d, in %s' % (filename, lineno, name))
        if line:
            _print(file, '    %s' % line.strip())

    return


def format_list(extracted_list):
    list = []
    for filename, lineno, name, line in extracted_list:
        item = '  File "%s", line %d, in %s\n' % (filename, lineno, name)
        if line:
            item = item + '    %s\n' % line.strip()
        list.append(item)

    return list


def print_tb(tb, limit = None, file = None):
    if file is None:
        file = sys.stderr
    if limit is None:
        if hasattr(sys, 'tracebacklimit'):
            limit = sys.tracebacklimit
    n = 0
    while tb is not None and (limit is None or n < limit):
        f = tb.tb_frame
        lineno = tb.tb_lineno
        co = f.f_code
        filename = co.co_filename
        name = co.co_name
        _print(file, '  File "%s", line %d, in %s' % (filename, lineno, name))
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno)
        if line:
            _print(file, '    ' + line.strip())
        tb = tb.tb_next
        n = n + 1

    return


def format_tb(tb, limit = None):
    return format_list(extract_tb(tb, limit))


def extract_tb(tb, limit = None):
    if limit is None:
        if hasattr(sys, 'tracebacklimit'):
            limit = sys.tracebacklimit
    list = []
    n = 0
    while tb is not None and (limit is None or n < limit):
        f = tb.tb_frame
        lineno = tb.tb_lineno
        co = f.f_code
        filename = co.co_filename
        name = co.co_name
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno)
        if line:
            line = line.strip()
        else:
            line = None
        list.append((filename,
         lineno,
         name,
         line))
        tb = tb.tb_next
        n = n + 1

    return list


def print_exception(etype, value, tb, limit = None, file = None):
    if file is None:
        file = sys.stderr
    if tb:
        _print(file, 'Traceback (most recent call last):')
        print_tb(tb, limit, file)
    lines = format_exception_only(etype, value)
    for line in lines[:-1]:
        _print(file, line, ' ')

    _print(file, lines[-1], '')
    return


def format_exception(etype, value, tb, limit = None):
    if tb:
        list = ['Traceback (most recent call last):\n']
        list = list + format_tb(tb, limit)
    else:
        list = []
    list = list + format_exception_only(etype, value)
    return list


def format_exception_only(etype, value):
    list = []
    if type(etype) == types.ClassType:
        stype = etype.__name__
    else:
        stype = etype
    if value is None:
        list.append(str(stype) + '\n')
    else:
        if etype is SyntaxError:
            try:
                msg, (filename, lineno, offset, line) = value
            except:
                pass
            else:
                if not filename:
                    filename = '<string>'
                list.append('  File "%s", line %d\n' % (filename, lineno))
                if line is not None:
                    i = 0
                    while i < len(line) and line[i].isspace():
                        i = i + 1

                    list.append('    %s\n' % line.strip())
                    if offset is not None:
                        s = '    '
                        for c in line[i:offset - 1]:
                            if c.isspace():
                                s = s + c
                            else:
                                s = s + ' '

                        list.append('%s^\n' % s)
                    value = msg
        s = _some_str(value)
        if s:
            list.append('%s: %s\n' % (str(stype), s))
        else:
            list.append('%s\n' % str(stype))
    return list


def _some_str(value):
    try:
        return str(value)
    except:
        return '<unprintable %s object>' % type(value).__name__


def print_exc(limit = None, file = None):
    if file is None:
        file = sys.stderr
    try:
        etype, value, tb = sys.exc_info()
        print_exception(etype, value, tb, limit, file)
    finally:
        etype = value = tb = None

    return


def format_exc(limit = None):
    try:
        etype, value, tb = sys.exc_info()
        return ''.join(format_exception(etype, value, tb, limit))
    finally:
        etype = value = tb = None

    return


def print_last(limit = None, file = None):
    if file is None:
        file = sys.stderr
    print_exception(sys.last_type, sys.last_value, sys.last_traceback, limit, file)
    return


def print_stack(f = None, limit = None, file = None):
    if f is None:
        try:
            raise ZeroDivisionError
        except ZeroDivisionError:
            f = sys.exc_info()[2].tb_frame.f_back

    print_list(extract_stack(f, limit), file)
    return


def format_stack(f = None, limit = None):
    if f is None:
        try:
            raise ZeroDivisionError
        except ZeroDivisionError:
            f = sys.exc_info()[2].tb_frame.f_back

    return format_list(extract_stack(f, limit))


def extract_stack(f = None, limit = None):
    if f is None:
        try:
            raise ZeroDivisionError
        except ZeroDivisionError:
            f = sys.exc_info()[2].tb_frame.f_back

    if limit is None:
        if hasattr(sys, 'tracebacklimit'):
            limit = sys.tracebacklimit
    list = []
    n = 0
    while f is not None and (limit is None or n < limit):
        lineno = f.f_lineno
        co = f.f_code
        filename = co.co_filename
        name = co.co_name
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno)
        if line:
            line = line.strip()
        else:
            line = None
        list.append((filename,
         lineno,
         name,
         line))
        f = f.f_back
        n = n + 1

    list.reverse()
    return list


def tb_lineno(tb):
    return tb.tb_lineno
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\traceback.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:13:36 Pacific Daylight Time
