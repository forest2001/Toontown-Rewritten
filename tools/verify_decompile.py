#!/usr/bin/env python2

import imp
import sys
import marshal
from types import *

def filter_code(to_filter):
    if type(to_filter) == ListType:
        return filter(filter_code, to_filter)
    elif type(to_filter) == DictType:
        ret = {}
        for k,v in to_filter.items():
            k = filter_code(k)
            v = filter_code(v)
            ret[k] = v
        return ret
    elif type(to_filter) == TupleType:
        return tuple(filter(filter_code, list(to_filter)))
    elif type(to_filter) == CodeType:
        return None
    else:
        return to_filter

def find_code(to_search):
    if type(to_search) == ListType:
        for x in to_search:
            for y in find_code(x):
                yield y
    elif type(to_search) == DictType:
        for k,v in to_search.items():
            for y in find_code(k):
                yield y
            for y in find_code(v):
                yield y
    elif type(to_search) == TupleType:
        for y in find_code(list(to_search)):
            yield y
    elif type(to_search) == CodeType:
        yield to_search

def compare_code(c1, c2):
    return (c1.co_name == c2.co_name and
            c1.co_argcount == c2.co_argcount and
            c1.co_cellvars == c2.co_cellvars and
            c1.co_code == c2.co_code and
            filter_code(c1.co_consts) == filter_code(c2.co_consts) and
            c1.co_flags == c2.co_flags and
            c1.co_freevars == c2.co_freevars and
            c1.co_names == c2.co_names and
            c1.co_nlocals == c2.co_nlocals and
            c1.co_varnames == c2.co_varnames)

def recurse(indent, orig, reimpl):
    sys.stdout.write('%s%s... ' % (indent, orig.co_name))
    if reimpl is None:
        sys.stdout.write('Missing\n')
        return False

    if not compare_code(orig, reimpl):
        sys.stdout.write('Mismatch\n')
        return False

    sys.stdout.write('OK\n')

    match = True
    for o,r in zip(find_code(orig.co_consts),find_code(reimpl.co_consts)):
        if not recurse(indent + ' '*4, o, r):
            match = False

    return match

def main(argv):
    if len(argv) < 3:
        print('Usage: %s bytecode.pyc sourcecode.py' % argv[0])
        return

    bytecode = open(argv[1], 'rb')
    sourcecode = open(argv[2], 'r')

    if bytecode.read(4) != imp.get_magic():
        print('Bytecode file does not match this version of Python!')
        return
    bytecode.read(4) # Discard timestamp

    orig = marshal.load(bytecode)
    reimpl = compile(sourcecode.read().replace('\r\n','\n'), argv[2], 'exec')

    sys.exit(not recurse('', orig, reimpl))

if __name__ == '__main__':
    main(sys.argv)
