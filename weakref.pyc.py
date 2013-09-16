# 2013.08.22 22:13:40 Pacific Daylight Time
# Embedded file name: weakref
import UserDict
from _weakref import getweakrefcount, getweakrefs, ref, proxy, CallableProxyType, ProxyType, ReferenceType
from exceptions import ReferenceError
ProxyTypes = (ProxyType, CallableProxyType)
__all__ = ['ref',
 'proxy',
 'getweakrefcount',
 'getweakrefs',
 'WeakKeyDictionary',
 'ReferenceType',
 'ProxyType',
 'CallableProxyType',
 'ProxyTypes',
 'WeakValueDictionary']

class WeakValueDictionary(UserDict.UserDict):
    __module__ = __name__

    def __init__(self, *args, **kw):
        UserDict.UserDict.__init__(self, *args, **kw)

        def remove(wr, selfref = ref(self)):
            self = selfref()
            if self is not None:
                del self.data[wr.key]
            return

        self._remove = remove

    def __getitem__(self, key):
        o = self.data[key]()
        if o is None:
            raise KeyError, key
        else:
            return o
        return

    def __contains__(self, key):
        try:
            o = self.data[key]()
        except KeyError:
            return False

        return o is not None

    def has_key(self, key):
        try:
            o = self.data[key]()
        except KeyError:
            return False

        return o is not None

    def __repr__(self):
        return '<WeakValueDictionary at %s>' % id(self)

    def __setitem__(self, key, value):
        self.data[key] = KeyedRef(value, self._remove, key)

    def copy(self):
        new = WeakValueDictionary()
        for key, wr in self.data.items():
            o = wr()
            if o is not None:
                new[key] = o

        return new

    def get(self, key, default = None):
        try:
            wr = self.data[key]
        except KeyError:
            return default
        else:
            o = wr()
            if o is None:
                return default
            else:
                return o

        return

    def items(self):
        L = []
        for key, wr in self.data.items():
            o = wr()
            if o is not None:
                L.append((key, o))

        return L

    def iteritems--- This code section failed: ---

0	SETUP_LOOP        '63'
3	LOAD_FAST         'self'
6	LOAD_ATTR         'data'
9	LOAD_ATTR         'itervalues'
12	CALL_FUNCTION_0   None
15	GET_ITER          None
16	FOR_ITER          '62'
19	STORE_FAST        'wr'

22	LOAD_FAST         'wr'
25	CALL_FUNCTION_0   None
28	STORE_FAST        'value'

31	LOAD_FAST         'value'
34	LOAD_CONST        None
37	COMPARE_OP        'is not'
40	JUMP_IF_FALSE     '59'

43	LOAD_FAST         'wr'
46	LOAD_ATTR         'key'
49	LOAD_FAST         'value'
52	BUILD_TUPLE_2     None
55	YIELD_VALUE       None
56	JUMP_BACK         '16'
59	JUMP_BACK         '16'
62	POP_BLOCK         None
63_0	COME_FROM         '0'
63	LOAD_CONST        None
66	RETURN_VALUE      None

Syntax error at or near `JUMP_BACK' token at offset 59

    def iterkeys(self):
        return self.data.iterkeys()

    def __iter__(self):
        return self.data.iterkeys()

    def itervalues--- This code section failed: ---

0	SETUP_LOOP        '54'
3	LOAD_FAST         'self'
6	LOAD_ATTR         'data'
9	LOAD_ATTR         'itervalues'
12	CALL_FUNCTION_0   None
15	GET_ITER          None
16	FOR_ITER          '53'
19	STORE_FAST        'wr'

22	LOAD_FAST         'wr'
25	CALL_FUNCTION_0   None
28	STORE_FAST        'obj'

31	LOAD_FAST         'obj'
34	LOAD_CONST        None
37	COMPARE_OP        'is not'
40	JUMP_IF_FALSE     '50'

43	LOAD_FAST         'obj'
46	YIELD_VALUE       None
47	JUMP_BACK         '16'
50	JUMP_BACK         '16'
53	POP_BLOCK         None
54_0	COME_FROM         '0'
54	LOAD_CONST        None
57	RETURN_VALUE      None

Syntax error at or near `JUMP_BACK' token at offset 50

    def popitem--- This code section failed: ---

0	SETUP_LOOP        '62'

3	LOAD_FAST         'self'
6	LOAD_ATTR         'data'
9	LOAD_ATTR         'popitem'
12	CALL_FUNCTION_0   None
15	UNPACK_SEQUENCE_2 None
18	STORE_FAST        'key'
21	STORE_FAST        'wr'

24	LOAD_FAST         'wr'
27	CALL_FUNCTION_0   None
30	STORE_FAST        'o'

33	LOAD_FAST         'o'
36	LOAD_CONST        None
39	COMPARE_OP        'is not'
42	JUMP_IF_FALSE     '58'

45	LOAD_FAST         'key'
48	LOAD_FAST         'o'
51	BUILD_TUPLE_2     None
54	RETURN_VALUE      None
55	JUMP_BACK         '3'
58	JUMP_BACK         '3'
61	POP_BLOCK         None
62_0	COME_FROM         '0'
62	LOAD_CONST        None
65	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 61

    def pop(self, key, *args):
        try:
            o = self.data.pop(key)()
        except KeyError:
            if args:
                return args[0]
            raise

        if o is None:
            raise KeyError, key
        else:
            return o
        return

    def setdefault(self, key, default = None):
        try:
            wr = self.data[key]
        except KeyError:
            self.data[key] = KeyedRef(default, self._remove, key)
            return default
        else:
            return wr()

    def update(self, dict = None, **kwargs):
        d = self.data
        if dict is not None:
            if not hasattr(dict, 'items'):
                dict = type({})(dict)
            for key, o in dict.items():
                d[key] = KeyedRef(o, self._remove, key)

        if len(kwargs):
            self.update(kwargs)
        return

    def values(self):
        L = []
        for wr in self.data.values():
            o = wr()
            if o is not None:
                L.append(o)

        return L


class KeyedRef(ref):
    __module__ = __name__
    __slots__ = ('key',)

    def __new__(type, ob, callback, key):
        self = ref.__new__(type, ob, callback)
        self.key = key
        return self

    def __init__(self, ob, callback, key):
        super(KeyedRef, self).__init__(ob, callback)


class WeakKeyDictionary(UserDict.UserDict):
    __module__ = __name__

    def __init__(self, dict = None):
        self.data = {}

        def remove(k, selfref = ref(self)):
            self = selfref()
            if self is not None:
                del self.data[k]
            return

        self._remove = remove
        if dict is not None:
            self.update(dict)
        return

    def __delitem__(self, key):
        del self.data[ref(key)]

    def __getitem__(self, key):
        return self.data[ref(key)]

    def __repr__(self):
        return '<WeakKeyDictionary at %s>' % id(self)

    def __setitem__(self, key, value):
        self.data[ref(key, self._remove)] = value

    def copy(self):
        new = WeakKeyDictionary()
        for key, value in self.data.items():
            o = key()
            if o is not None:
                new[o] = value

        return new

    def get(self, key, default = None):
        return self.data.get(ref(key), default)

    def has_key(self, key):
        try:
            wr = ref(key)
        except TypeError:
            return 0

        return wr in self.data

    def __contains__(self, key):
        try:
            wr = ref(key)
        except TypeError:
            return 0

        return wr in self.data

    def items(self):
        L = []
        for key, value in self.data.items():
            o = key()
            if o is not None:
                L.append((o, value))

        return L

    def iteritems--- This code section failed: ---

0	SETUP_LOOP        '66'
3	LOAD_FAST         'self'
6	LOAD_ATTR         'data'
9	LOAD_ATTR         'iteritems'
12	CALL_FUNCTION_0   None
15	GET_ITER          None
16	FOR_ITER          '65'
19	UNPACK_SEQUENCE_2 None
22	STORE_FAST        'wr'
25	STORE_FAST        'value'

28	LOAD_FAST         'wr'
31	CALL_FUNCTION_0   None
34	STORE_FAST        'key'

37	LOAD_FAST         'key'
40	LOAD_CONST        None
43	COMPARE_OP        'is not'
46	JUMP_IF_FALSE     '62'

49	LOAD_FAST         'key'
52	LOAD_FAST         'value'
55	BUILD_TUPLE_2     None
58	YIELD_VALUE       None
59	JUMP_BACK         '16'
62	JUMP_BACK         '16'
65	POP_BLOCK         None
66_0	COME_FROM         '0'
66	LOAD_CONST        None
69	RETURN_VALUE      None

Syntax error at or near `JUMP_BACK' token at offset 62

    def iterkeys--- This code section failed: ---

0	SETUP_LOOP        '54'
3	LOAD_FAST         'self'
6	LOAD_ATTR         'data'
9	LOAD_ATTR         'iterkeys'
12	CALL_FUNCTION_0   None
15	GET_ITER          None
16	FOR_ITER          '53'
19	STORE_FAST        'wr'

22	LOAD_FAST         'wr'
25	CALL_FUNCTION_0   None
28	STORE_FAST        'obj'

31	LOAD_FAST         'obj'
34	LOAD_CONST        None
37	COMPARE_OP        'is not'
40	JUMP_IF_FALSE     '50'

43	LOAD_FAST         'obj'
46	YIELD_VALUE       None
47	JUMP_BACK         '16'
50	JUMP_BACK         '16'
53	POP_BLOCK         None
54_0	COME_FROM         '0'
54	LOAD_CONST        None
57	RETURN_VALUE      None

Syntax error at or near `JUMP_BACK' token at offset 50

    def __iter__(self):
        return self.iterkeys()

    def itervalues(self):
        return self.data.itervalues()

    def keys(self):
        L = []
        for wr in self.data.keys():
            o = wr()
            if o is not None:
                L.append(o)

        return L

    def popitem--- This code section failed: ---

0	SETUP_LOOP        '62'

3	LOAD_FAST         'self'
6	LOAD_ATTR         'data'
9	LOAD_ATTR         'popitem'
12	CALL_FUNCTION_0   None
15	UNPACK_SEQUENCE_2 None
18	STORE_FAST        'key'
21	STORE_FAST        'value'

24	LOAD_FAST         'key'
27	CALL_FUNCTION_0   None
30	STORE_FAST        'o'

33	LOAD_FAST         'o'
36	LOAD_CONST        None
39	COMPARE_OP        'is not'
42	JUMP_IF_FALSE     '58'

45	LOAD_FAST         'o'
48	LOAD_FAST         'value'
51	BUILD_TUPLE_2     None
54	RETURN_VALUE      None
55	JUMP_BACK         '3'
58	JUMP_BACK         '3'
61	POP_BLOCK         None
62_0	COME_FROM         '0'
62	LOAD_CONST        None
65	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 61

    def pop(self, key, *args):
        return self.data.pop(ref(key), *args)

    def setdefault(self, key, default = None):
        return self.data.setdefault(ref(key, self._remove), default)

    def update(self, dict = None, **kwargs):
        d = self.data
        if dict is not None:
            if not hasattr(dict, 'items'):
                dict = type({})(dict)
            for key, value in dict.items():
                d[ref(key, self._remove)] = value

        if len(kwargs):
            self.update(kwargs)
        return# decompiled 0 files: 0 okay, 1 failed, 0 verify failed
# 2013.08.22 22:13:41 Pacific Daylight Time

# Can't uncompyle C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\weakref.pyc
Traceback (most recent call last):
  File "C:\python27\lib\uncompyle2\__init__.py", line 206, in main
    uncompyle_file(infile, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 143, in uncompyle_file
    uncompyle(version, co, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 132, in uncompyle
    raise walk.ERROR
ParserError: --- This code section failed: ---

0	SETUP_LOOP        '62'

3	LOAD_FAST         'self'
6	LOAD_ATTR         'data'
9	LOAD_ATTR         'popitem'
12	CALL_FUNCTION_0   None
15	UNPACK_SEQUENCE_2 None
18	STORE_FAST        'key'
21	STORE_FAST        'value'

24	LOAD_FAST         'key'
27	CALL_FUNCTION_0   None
30	STORE_FAST        'o'

33	LOAD_FAST         'o'
36	LOAD_CONST        None
39	COMPARE_OP        'is not'
42	JUMP_IF_FALSE     '58'

45	LOAD_FAST         'o'
48	LOAD_FAST         'value'
51	BUILD_TUPLE_2     None
54	RETURN_VALUE      None
55	JUMP_BACK         '3'
58	JUMP_BACK         '3'
61	POP_BLOCK         None
62_0	COME_FROM         '0'
62	LOAD_CONST        None
65	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 61

