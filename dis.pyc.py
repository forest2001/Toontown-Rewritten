# 2013.08.22 22:12:56 Pacific Daylight Time
# Embedded file name: dis
import sys
import types
from opcode import *
from opcode import __all__ as _opcodes_all
__all__ = ['dis',
 'disassemble',
 'distb',
 'disco'] + _opcodes_all
del _opcodes_all

def dis(x = None):
    if x is None:
        distb()
        return
    if type(x) is types.InstanceType:
        x = x.__class__
    if hasattr(x, 'im_func'):
        x = x.im_func
    if hasattr(x, 'func_code'):
        x = x.func_code
    if hasattr(x, '__dict__'):
        items = x.__dict__.items()
        items.sort()
        for name, x1 in items:
            if type(x1) in (types.MethodType,
             types.FunctionType,
             types.CodeType,
             types.ClassType):
                print 'Disassembly of %s:' % name
                try:
                    dis(x1)
                except TypeError as msg:
                    print 'Sorry:', msg

                print

    elif hasattr(x, 'co_code'):
        disassemble(x)
    elif isinstance(x, str):
        disassemble_string(x)
    else:
        raise TypeError, "don't know how to disassemble %s objects" % type(x).__name__
    return


def distb(tb = None):
    if tb is None:
        try:
            tb = sys.last_traceback
        except AttributeError:
            raise RuntimeError, 'no last traceback to disassemble'

        while tb.tb_next:
            tb = tb.tb_next

    disassemble(tb.tb_frame.f_code, tb.tb_lasti)
    return


def disassemble(co, lasti = -1):
    code = co.co_code
    labels = findlabels(code)
    linestarts = dict(findlinestarts(co))
    n = len(code)
    i = 0
    extended_arg = 0
    free = None
    while i < n:
        c = code[i]
        op = ord(c)
        if i in linestarts:
            if i > 0:
                print
            print '%3d' % linestarts[i],
        else:
            print '   ',
        if i == lasti:
            print '-->',
        else:
            print '   ',
        if i in labels:
            print '>>',
        else:
            print '  ',
        print repr(i).rjust(4),
        print opname[op].ljust(20),
        i = i + 1
        if op >= HAVE_ARGUMENT:
            oparg = ord(code[i]) + ord(code[i + 1]) * 256 + extended_arg
            extended_arg = 0
            i = i + 2
            if op == EXTENDED_ARG:
                extended_arg = oparg * 65536L
            print repr(oparg).rjust(5),
            if op in hasconst:
                print '(' + repr(co.co_consts[oparg]) + ')',
            elif op in hasname:
                print '(' + co.co_names[oparg] + ')',
            elif op in hasjrel:
                print '(to ' + repr(i + oparg) + ')',
            elif op in haslocal:
                print '(' + co.co_varnames[oparg] + ')',
            elif op in hascompare:
                print '(' + cmp_op[oparg] + ')',
            elif op in hasfree:
                if free is None:
                    free = co.co_cellvars + co.co_freevars
                print '(' + free[oparg] + ')',
        print

    return


def disassemble_string(code, lasti = -1, varnames = None, names = None, constants = None):
    labels = findlabels(code)
    n = len(code)
    i = 0
    while i < n:
        c = code[i]
        op = ord(c)
        if i == lasti:
            print '-->',
        else:
            print '   ',
        if i in labels:
            print '>>',
        else:
            print '  ',
        print repr(i).rjust(4),
        print opname[op].ljust(15),
        i = i + 1
        if op >= HAVE_ARGUMENT:
            oparg = ord(code[i]) + ord(code[i + 1]) * 256
            i = i + 2
            print repr(oparg).rjust(5),
            if op in hasconst:
                if constants:
                    print '(' + repr(constants[oparg]) + ')',
                else:
                    print '(%d)' % oparg,
            elif op in hasname:
                if names is not None:
                    print '(' + names[oparg] + ')',
                else:
                    print '(%d)' % oparg,
            elif op in hasjrel:
                print '(to ' + repr(i + oparg) + ')',
            elif op in haslocal:
                if varnames:
                    print '(' + varnames[oparg] + ')',
                else:
                    print '(%d)' % oparg,
            elif op in hascompare:
                print '(' + cmp_op[oparg] + ')',
        print

    return


disco = disassemble

def findlabels(code):
    labels = []
    n = len(code)
    i = 0
    while i < n:
        c = code[i]
        op = ord(c)
        i = i + 1
        if op >= HAVE_ARGUMENT:
            oparg = ord(code[i]) + ord(code[i + 1]) * 256
            i = i + 2
            label = -1
            if op in hasjrel:
                label = i + oparg
            elif op in hasjabs:
                label = oparg
            if label >= 0:
                if label not in labels:
                    labels.append(label)

    return labels


def findlinestarts--- This code section failed: ---

0	BUILD_LIST_0      None
3	LOAD_FAST         'code'
6	LOAD_ATTR         'co_lnotab'
9	LOAD_CONST        0
12	LOAD_CONST        None
15	LOAD_CONST        2
18	BUILD_SLICE_3     None
21	BINARY_SUBSCR     None
22	GET_ITER          None
23	FOR_ITER          '44'
26	STORE_FAST        'c'
29	LOAD_GLOBAL       'ord'
32	LOAD_FAST         'c'
35	CALL_FUNCTION_1   None
38	LIST_APPEND       None
41	JUMP_BACK         '23'
44	STORE_FAST        'byte_increments'

47	BUILD_LIST_0      None
50	LOAD_FAST         'code'
53	LOAD_ATTR         'co_lnotab'
56	LOAD_CONST        1
59	LOAD_CONST        None
62	LOAD_CONST        2
65	BUILD_SLICE_3     None
68	BINARY_SUBSCR     None
69	GET_ITER          None
70	FOR_ITER          '91'
73	STORE_FAST        'c'
76	LOAD_GLOBAL       'ord'
79	LOAD_FAST         'c'
82	CALL_FUNCTION_1   None
85	LIST_APPEND       None
88	JUMP_BACK         '70'
91	STORE_FAST        'line_increments'

94	LOAD_CONST        None
97	STORE_FAST        'lastlineno'

100	LOAD_FAST         'code'
103	LOAD_ATTR         'co_firstlineno'
106	STORE_FAST        'lineno'

109	LOAD_CONST        0
112	STORE_FAST        'addr'

115	SETUP_LOOP        '207'
118	LOAD_GLOBAL       'zip'
121	LOAD_FAST         'byte_increments'
124	LOAD_FAST         'line_increments'
127	CALL_FUNCTION_2   None
130	GET_ITER          None
131	FOR_ITER          '206'
134	UNPACK_SEQUENCE_2 None
137	STORE_FAST        'byte_incr'
140	STORE_FAST        'line_incr'

143	LOAD_FAST         'byte_incr'
146	JUMP_IF_FALSE     '193'

149	LOAD_FAST         'lineno'
152	LOAD_FAST         'lastlineno'
155	COMPARE_OP        '!='
158	JUMP_IF_FALSE     '180'

161	LOAD_FAST         'addr'
164	LOAD_FAST         'lineno'
167	BUILD_TUPLE_2     None
170	YIELD_VALUE       None

171	LOAD_FAST         'lineno'
174	STORE_FAST        'lastlineno'
177	JUMP_FORWARD      '180'
180_0	COME_FROM         '177'

180	LOAD_FAST         'addr'
183	LOAD_FAST         'byte_incr'
186	INPLACE_ADD       None
187	STORE_FAST        'addr'
190	JUMP_FORWARD      '193'
193_0	COME_FROM         '190'

193	LOAD_FAST         'lineno'
196	LOAD_FAST         'line_incr'
199	INPLACE_ADD       None
200	STORE_FAST        'lineno'
203	JUMP_BACK         '131'
206	POP_BLOCK         None
207_0	COME_FROM         '115'

207	LOAD_FAST         'lineno'
210	LOAD_FAST         'lastlineno'
213	COMPARE_OP        '!='
216	JUMP_IF_FALSE     '232'

219	LOAD_FAST         'addr'
222	LOAD_FAST         'lineno'
225	BUILD_TUPLE_2     None
228	YIELD_VALUE       None
229	JUMP_FORWARD      '232'
232_0	COME_FROM         '229'
232	LOAD_CONST        None
235	RETURN_VALUE      None

Syntax error at or near `STORE_FAST' token at offset 174


def _test():
    if sys.argv[1:]:
        if sys.argv[2:]:
            sys.stderr.write('usage: python dis.py [-|file]\n')
            sys.exit(2)
        fn = sys.argv[1]
        if not fn or fn == '-':
            fn = None
    else:
        fn = None
    if fn is None:
        f = sys.stdin
    else:
        f = open(fn)
    source = f.read()
    if fn is not None:
        f.close()
    else:
        fn = '<stdin>'
    code = compile(source, fn, 'exec')
    dis(code)
    return


if __name__ == '__main__':
    _test()# decompiled 0 files: 0 okay, 1 failed, 0 verify failed
# 2013.08.22 22:12:57 Pacific Daylight Time

# Can't uncompyle C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\dis.pyc
Traceback (most recent call last):
  File "C:\python27\lib\uncompyle2\__init__.py", line 206, in main
    uncompyle_file(infile, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 143, in uncompyle_file
    uncompyle(version, co, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 132, in uncompyle
    raise walk.ERROR
ParserError: --- This code section failed: ---

0	BUILD_LIST_0      None
3	LOAD_FAST         'code'
6	LOAD_ATTR         'co_lnotab'
9	LOAD_CONST        0
12	LOAD_CONST        None
15	LOAD_CONST        2
18	BUILD_SLICE_3     None
21	BINARY_SUBSCR     None
22	GET_ITER          None
23	FOR_ITER          '44'
26	STORE_FAST        'c'
29	LOAD_GLOBAL       'ord'
32	LOAD_FAST         'c'
35	CALL_FUNCTION_1   None
38	LIST_APPEND       None
41	JUMP_BACK         '23'
44	STORE_FAST        'byte_increments'

47	BUILD_LIST_0      None
50	LOAD_FAST         'code'
53	LOAD_ATTR         'co_lnotab'
56	LOAD_CONST        1
59	LOAD_CONST        None
62	LOAD_CONST        2
65	BUILD_SLICE_3     None
68	BINARY_SUBSCR     None
69	GET_ITER          None
70	FOR_ITER          '91'
73	STORE_FAST        'c'
76	LOAD_GLOBAL       'ord'
79	LOAD_FAST         'c'
82	CALL_FUNCTION_1   None
85	LIST_APPEND       None
88	JUMP_BACK         '70'
91	STORE_FAST        'line_increments'

94	LOAD_CONST        None
97	STORE_FAST        'lastlineno'

100	LOAD_FAST         'code'
103	LOAD_ATTR         'co_firstlineno'
106	STORE_FAST        'lineno'

109	LOAD_CONST        0
112	STORE_FAST        'addr'

115	SETUP_LOOP        '207'
118	LOAD_GLOBAL       'zip'
121	LOAD_FAST         'byte_increments'
124	LOAD_FAST         'line_increments'
127	CALL_FUNCTION_2   None
130	GET_ITER          None
131	FOR_ITER          '206'
134	UNPACK_SEQUENCE_2 None
137	STORE_FAST        'byte_incr'
140	STORE_FAST        'line_incr'

143	LOAD_FAST         'byte_incr'
146	JUMP_IF_FALSE     '193'

149	LOAD_FAST         'lineno'
152	LOAD_FAST         'lastlineno'
155	COMPARE_OP        '!='
158	JUMP_IF_FALSE     '180'

161	LOAD_FAST         'addr'
164	LOAD_FAST         'lineno'
167	BUILD_TUPLE_2     None
170	YIELD_VALUE       None

171	LOAD_FAST         'lineno'
174	STORE_FAST        'lastlineno'
177	JUMP_FORWARD      '180'
180_0	COME_FROM         '177'

180	LOAD_FAST         'addr'
183	LOAD_FAST         'byte_incr'
186	INPLACE_ADD       None
187	STORE_FAST        'addr'
190	JUMP_FORWARD      '193'
193_0	COME_FROM         '190'

193	LOAD_FAST         'lineno'
196	LOAD_FAST         'line_incr'
199	INPLACE_ADD       None
200	STORE_FAST        'lineno'
203	JUMP_BACK         '131'
206	POP_BLOCK         None
207_0	COME_FROM         '115'

207	LOAD_FAST         'lineno'
210	LOAD_FAST         'lastlineno'
213	COMPARE_OP        '!='
216	JUMP_IF_FALSE     '232'

219	LOAD_FAST         'addr'
222	LOAD_FAST         'lineno'
225	BUILD_TUPLE_2     None
228	YIELD_VALUE       None
229	JUMP_FORWARD      '232'
232_0	COME_FROM         '229'
232	LOAD_CONST        None
235	RETURN_VALUE      None

Syntax error at or near `STORE_FAST' token at offset 174

