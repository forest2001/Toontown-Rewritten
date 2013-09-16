# 2013.08.22 22:13:39 Pacific Daylight Time
# Embedded file name: UserDict


class UserDict():
    __module__ = __name__

    def __init__(self, dict = None, **kwargs):
        self.data = {}
        if dict is not None:
            self.update(dict)
        if len(kwargs):
            self.update(kwargs)
        return

    def __repr__(self):
        return repr(self.data)

    def __cmp__(self, dict):
        if isinstance(dict, UserDict):
            return cmp(self.data, dict.data)
        else:
            return cmp(self.data, dict)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, item):
        self.data[key] = item

    def __delitem__(self, key):
        del self.data[key]

    def clear(self):
        self.data.clear()

    def copy(self):
        if self.__class__ is UserDict:
            return UserDict(self.data.copy())
        import copy
        data = self.data
        try:
            self.data = {}
            c = copy.copy(self)
        finally:
            self.data = data

        c.update(self)
        return c

    def keys(self):
        return self.data.keys()

    def items(self):
        return self.data.items()

    def iteritems(self):
        return self.data.iteritems()

    def iterkeys(self):
        return self.data.iterkeys()

    def itervalues(self):
        return self.data.itervalues()

    def values(self):
        return self.data.values()

    def has_key(self, key):
        return self.data.has_key(key)

    def update(self, dict = None, **kwargs):
        if dict is None:
            pass
        elif isinstance(dict, UserDict):
            self.data.update(dict.data)
        elif isinstance(dict, type({})) or not hasattr(dict, 'items'):
            self.data.update(dict)
        else:
            for k, v in dict.items():
                self[k] = v

        if len(kwargs):
            self.data.update(kwargs)
        return

    def get(self, key, failobj = None):
        if not self.has_key(key):
            return failobj
        return self[key]

    def setdefault(self, key, failobj = None):
        if not self.has_key(key):
            self[key] = failobj
        return self[key]

    def pop(self, key, *args):
        return self.data.pop(key, *args)

    def popitem(self):
        return self.data.popitem()

    def __contains__(self, key):
        return key in self.data

    def fromkeys(cls, iterable, value = None):
        d = cls()
        for key in iterable:
            d[key] = value

        return d

    fromkeys = classmethod(fromkeys)


class IterableUserDict(UserDict):
    __module__ = __name__

    def __iter__(self):
        return iter(self.data)


class DictMixin():
    __module__ = __name__

    def __iter__--- This code section failed: ---

0	SETUP_LOOP        '27'
3	LOAD_FAST         'self'
6	LOAD_ATTR         'keys'
9	CALL_FUNCTION_0   None
12	GET_ITER          None
13	FOR_ITER          '26'
16	STORE_FAST        'k'

19	LOAD_FAST         'k'
22	YIELD_VALUE       None
23	JUMP_BACK         '13'
26	POP_BLOCK         None
27_0	COME_FROM         '0'

Syntax error at or near `POP_BLOCK' token at offset 26

    def has_key(self, key):
        try:
            value = self[key]
        except KeyError:
            return False

        return True

    def __contains__(self, key):
        return self.has_key(key)

    def iteritems--- This code section failed: ---

0	SETUP_LOOP        '31'
3	LOAD_FAST         'self'
6	GET_ITER          None
7	FOR_ITER          '30'
10	STORE_FAST        'k'

13	LOAD_FAST         'k'
16	LOAD_FAST         'self'
19	LOAD_FAST         'k'
22	BINARY_SUBSCR     None
23	BUILD_TUPLE_2     None
26	YIELD_VALUE       None
27	JUMP_BACK         '7'
30	POP_BLOCK         None
31_0	COME_FROM         '0'

Syntax error at or near `POP_BLOCK' token at offset 30

    def iterkeys(self):
        return self.__iter__()

    def itervalues--- This code section failed: ---

0	SETUP_LOOP        '33'
3	LOAD_FAST         'self'
6	LOAD_ATTR         'iteritems'
9	CALL_FUNCTION_0   None
12	GET_ITER          None
13	FOR_ITER          '32'
16	UNPACK_SEQUENCE_2 None
19	STORE_FAST        '_'
22	STORE_FAST        'v'

25	LOAD_FAST         'v'
28	YIELD_VALUE       None
29	JUMP_BACK         '13'
32	POP_BLOCK         None
33_0	COME_FROM         '0'

Syntax error at or near `POP_BLOCK' token at offset 32

    def values(self):
        return [ v for _, v in self.iteritems() ]

    def items(self):
        return list(self.iteritems())

    def clear(self):
        for key in self.keys():
            del self[key]

    def setdefault(self, key, default = None):
        try:
            return self[key]
        except KeyError:
            self[key] = default

        return default

    def pop(self, key, *args):
        if len(args) > 1:
            raise TypeError, 'pop expected at most 2 arguments, got ' + repr(1 + len(args))
        try:
            value = self[key]
        except KeyError:
            if args:
                return args[0]
            raise

        del self[key]
        return value

    def popitem(self):
        try:
            k, v = self.iteritems().next()
        except StopIteration:
            raise KeyError, 'container is empty'

        del self[k]
        return (k, v)

    def update(self, other = None, **kwargs):
        if other is None:
            pass
        elif hasattr(other, 'iteritems'):
            for k, v in other.iteritems():
                self[k] = v

        elif hasattr(other, 'keys'):
            for k in other.keys():
                self[k] = other[k]

        else:
            for k, v in other:
                self[k] = v

        if kwargs:
            self.update(kwargs)
        return

    def get(self, key, default = None):
        try:
            return self[key]
        except KeyError:
            return default

    def __repr__(self):
        return repr(dict(self.iteritems()))

    def __cmp__(self, other):
        if other is None:
            return 1
        if isinstance(other, DictMixin):
            other = dict(other.iteritems())
        return cmp(dict(self.iteritems()), other)

    def __len__(self):
        return len(self.keys())# decompiled 0 files: 0 okay, 1 failed, 0 verify failed
# 2013.08.22 22:13:40 Pacific Daylight Time

# Can't uncompyle C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\UserDict.pyc
Traceback (most recent call last):
  File "C:\python27\lib\uncompyle2\__init__.py", line 206, in main
    uncompyle_file(infile, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 143, in uncompyle_file
    uncompyle(version, co, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 132, in uncompyle
    raise walk.ERROR
ParserError: --- This code section failed: ---

0	SETUP_LOOP        '33'
3	LOAD_FAST         'self'
6	LOAD_ATTR         'iteritems'
9	CALL_FUNCTION_0   None
12	GET_ITER          None
13	FOR_ITER          '32'
16	UNPACK_SEQUENCE_2 None
19	STORE_FAST        '_'
22	STORE_FAST        'v'

25	LOAD_FAST         'v'
28	YIELD_VALUE       None
29	JUMP_BACK         '13'
32	POP_BLOCK         None
33_0	COME_FROM         '0'

Syntax error at or near `POP_BLOCK' token at offset 32

