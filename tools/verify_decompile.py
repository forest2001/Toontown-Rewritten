#!/usr/bin/env python2

import imp
import sys
import marshal
import dis
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
    if hasattr(c1, 'force_optimize'): c1 = c1.force_optimize()
    if hasattr(c2, 'force_optimize'): c2 = c2.force_optimize()
    if c1.co_name != c2.co_name:
        print "co_name mismatch"
        print "Expected: ", c1.co_name
        print "Got: ", c2.co_name
    if c1.co_argcount != c2.co_argcount:
        print "co_argcount mismatch"
        print "Expected: ", c1.co_argcount
        print "Got: ", c2.co_argcount
    if c1.co_cellvars != c2.co_cellvars:
        print "co_cellvars mismatch"
        print "Expected: ", c1.co_cellvars
        print "Got: ", c2.co_cellvars
    if c1.co_code != c2.co_code:
        print "co_code mismatch, dumping dis1.dis and dis2.dis"
        oldstdout = sys.stdout
        f = open("dis1.dis", "w")
        sys.stdout = f
        dis.disco(c1)
        f.close()
        f = open("dis2.dis", "w")
        sys.stdout = f
        dis.disco(c2)
        f.close()
        sys.stdout = oldstdout
    if filter_code(c1.co_consts) != filter_code(c2.co_consts):
        print "filter_code(c1.co_consts) mismatch"
        print "Expected: ", filter_code(c1.co_consts)
        print "Got: ", filter_code(c2.co_consts)
    if c1.co_flags != c2.co_flags:
        print "co_flags mismatch"
        print "Expected: ", c1.co_flags
        print "Got: ", c2.co_flags
    if c1.co_freevars != c2.co_freevars:
        print "co_freevars mismatch"
        print "Expected: ", c1.co_freevars
        print "Got: ", c2.co_freevars
    if c1.co_names != c2.co_names:
        print "co_names mismatch"
        print "Expected: ", c1.co_names
        print "Got     : ", c2.co_names
    if c1.co_nlocals != c2.co_nlocals:
        print "co_nlocals mismatch"
        print "Expected: ", c1.co_nlocals
        print "Got: ", c2.co_nlocals
    if c1.co_varnames != c2.co_varnames:
        print "co_varnames mismatch"
        print "Expected: ", c1.co_varnames
        print "Got     : ", c2.co_varnames
    '''if c1.co_ != c2.co_:
        print "co_ mismatch"
        print "Expected: ", c1.co_
        print "Got: ", c2.co_'''
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
