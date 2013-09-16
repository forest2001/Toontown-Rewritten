# 2013.08.22 22:13:26 Pacific Daylight Time
# Embedded file name: sets
from __future__ import generators
try:
    from itertools import ifilter, ifilterfalse
except ImportError:

    def ifilter--- This code section failed: ---

0	LOAD_FAST         'predicate'
3	LOAD_CONST        None
6	COMPARE_OP        'is'
9	JUMP_IF_FALSE     '24'

12	LOAD_CONST        '<code_object predicate>'
15	MAKE_FUNCTION_0   None
18	STORE_FAST        'predicate'
21	JUMP_FORWARD      '24'
24_0	COME_FROM         '21'

24	SETUP_LOOP        '60'
27	LOAD_FAST         'iterable'
30	GET_ITER          None
31	FOR_ITER          '59'
34	STORE_FAST        'x'

37	LOAD_FAST         'predicate'
40	LOAD_FAST         'x'
43	CALL_FUNCTION_1   None
46	JUMP_IF_FALSE     '56'

49	LOAD_FAST         'x'
52	YIELD_VALUE       None
53	JUMP_BACK         '31'
56	JUMP_BACK         '31'
59	POP_BLOCK         None
60_0	COME_FROM         '24'
60	LOAD_CONST        None
63	RETURN_VALUE      None

Syntax error at or near `JUMP_BACK' token at offset 56


    def ifilterfalse--- This code section failed: ---

0	LOAD_FAST         'predicate'
3	LOAD_CONST        None
6	COMPARE_OP        'is'
9	JUMP_IF_FALSE     '24'

12	LOAD_CONST        '<code_object predicate>'
15	MAKE_FUNCTION_0   None
18	STORE_FAST        'predicate'
21	JUMP_FORWARD      '24'
24_0	COME_FROM         '21'

24	SETUP_LOOP        '60'
27	LOAD_FAST         'iterable'
30	GET_ITER          None
31	FOR_ITER          '59'
34	STORE_FAST        'x'

37	LOAD_FAST         'predicate'
40	LOAD_FAST         'x'
43	CALL_FUNCTION_1   None
46	JUMP_IF_TRUE      '56'

49	LOAD_FAST         'x'
52_0	COME_FROM         '46'
52	YIELD_VALUE       None
53	CONTINUE          '31'
56	JUMP_BACK         '31'
59	POP_BLOCK         None
60_0	COME_FROM         '24'
60	LOAD_CONST        None
63	RETURN_VALUE      None

Syntax error at or near `CONTINUE' token at offset 53


    try:
        (True, False)
    except NameError:
        True, False = (0 == 0, 0 != 0)

__all__ = ['BaseSet', 'Set', 'ImmutableSet']

class BaseSet(object):
    __module__ = __name__
    __slots__ = ['_data']

    def __init__(self):
        if self.__class__ is BaseSet:
            raise TypeError, 'BaseSet is an abstract class.  Use Set or ImmutableSet.'

    def __len__(self):
        return len(self._data)

    def __repr__(self):
        return self._repr()

    __str__ = __repr__

    def _repr(self, sorted = False):
        elements = self._data.keys()
        if sorted:
            elements.sort()
        return '%s(%r)' % (self.__class__.__name__, elements)

    def __iter__(self):
        return self._data.iterkeys()

    def __cmp__(self, other):
        raise TypeError, "can't compare sets using cmp()"

    def __eq__(self, other):
        if isinstance(other, BaseSet):
            return self._data == other._data
        else:
            return False

    def __ne__(self, other):
        if isinstance(other, BaseSet):
            return self._data != other._data
        else:
            return True

    def copy(self):
        result = self.__class__()
        result._data.update(self._data)
        return result

    __copy__ = copy

    def __deepcopy__(self, memo):
        from copy import deepcopy
        result = self.__class__()
        memo[id(self)] = result
        data = result._data
        value = True
        for elt in self:
            data[deepcopy(elt, memo)] = value

        return result

    def __or__(self, other):
        if not isinstance(other, BaseSet):
            return NotImplemented
        return self.union(other)

    def union(self, other):
        result = self.__class__(self)
        result._update(other)
        return result

    def __and__(self, other):
        if not isinstance(other, BaseSet):
            return NotImplemented
        return self.intersection(other)

    def intersection(self, other):
        if not isinstance(other, BaseSet):
            other = Set(other)
        if len(self) <= len(other):
            little, big = self, other
        else:
            little, big = other, self
        common = ifilter(big._data.has_key, little)
        return self.__class__(common)

    def __xor__(self, other):
        if not isinstance(other, BaseSet):
            return NotImplemented
        return self.symmetric_difference(other)

    def symmetric_difference(self, other):
        result = self.__class__()
        data = result._data
        value = True
        selfdata = self._data
        try:
            otherdata = other._data
        except AttributeError:
            otherdata = Set(other)._data

        for elt in ifilterfalse(otherdata.has_key, selfdata):
            data[elt] = value

        for elt in ifilterfalse(selfdata.has_key, otherdata):
            data[elt] = value

        return result

    def __sub__(self, other):
        if not isinstance(other, BaseSet):
            return NotImplemented
        return self.difference(other)

    def difference(self, other):
        result = self.__class__()
        data = result._data
        try:
            otherdata = other._data
        except AttributeError:
            otherdata = Set(other)._data

        value = True
        for elt in ifilterfalse(otherdata.has_key, self):
            data[elt] = value

        return result

    def __contains__(self, element):
        try:
            return element in self._data
        except TypeError:
            transform = getattr(element, '__as_temporarily_immutable__', None)
            if transform is None:
                raise
            return transform() in self._data

        return

    def issubset(self, other):
        self._binary_sanity_check(other)
        if len(self) > len(other):
            return False
        for elt in ifilterfalse(other._data.has_key, self):
            return False

        return True

    def issuperset(self, other):
        self._binary_sanity_check(other)
        if len(self) < len(other):
            return False
        for elt in ifilterfalse(self._data.has_key, other):
            return False

        return True

    __le__ = issubset
    __ge__ = issuperset

    def __lt__(self, other):
        self._binary_sanity_check(other)
        return len(self) < len(other) and self.issubset(other)

    def __gt__(self, other):
        self._binary_sanity_check(other)
        return len(self) > len(other) and self.issuperset(other)

    def _binary_sanity_check(self, other):
        if not isinstance(other, BaseSet):
            raise TypeError, 'Binary operation only permitted between sets'

    def _compute_hash(self):
        result = 0
        for elt in self:
            result ^= hash(elt)

        return result

    def _update(self, iterable):
        data = self._data
        if isinstance(iterable, BaseSet):
            data.update(iterable._data)
            return
        value = True
        if type(iterable) in (list, tuple, xrange):
            it = iter(iterable)
            while True:
                try:
                    for element in it:
                        data[element] = value

                    return
                except TypeError:
                    transform = getattr(element, '__as_immutable__', None)
                    if transform is None:
                        raise
                    data[transform()] = value

        else:
            for element in iterable:
                try:
                    data[element] = value
                except TypeError:
                    transform = getattr(element, '__as_immutable__', None)
                    if transform is None:
                        raise
                    data[transform()] = value

        return


class ImmutableSet(BaseSet):
    __module__ = __name__
    __slots__ = ['_hashcode']

    def __init__(self, iterable = None):
        self._hashcode = None
        self._data = {}
        if iterable is not None:
            self._update(iterable)
        return

    def __hash__(self):
        if self._hashcode is None:
            self._hashcode = self._compute_hash()
        return self._hashcode

    def __getstate__(self):
        return (self._data, self._hashcode)

    def __setstate__(self, state):
        self._data, self._hashcode = state


class Set(BaseSet):
    __module__ = __name__
    __slots__ = []

    def __init__(self, iterable = None):
        self._data = {}
        if iterable is not None:
            self._update(iterable)
        return

    def __getstate__(self):
        return (self._data,)

    def __setstate__(self, data):
        self._data, = data

    def __hash__(self):
        raise TypeError, "Can't hash a Set, only an ImmutableSet."

    def __ior__(self, other):
        self._binary_sanity_check(other)
        self._data.update(other._data)
        return self

    def union_update(self, other):
        self._update(other)

    def __iand__(self, other):
        self._binary_sanity_check(other)
        self._data = (self & other)._data
        return self

    def intersection_update(self, other):
        if isinstance(other, BaseSet):
            self &= other
        else:
            self._data = self.intersection(other)._data

    def __ixor__(self, other):
        self._binary_sanity_check(other)
        self.symmetric_difference_update(other)
        return self

    def symmetric_difference_update(self, other):
        data = self._data
        value = True
        if not isinstance(other, BaseSet):
            other = Set(other)
        for elt in other:
            if elt in data:
                del data[elt]
            else:
                data[elt] = value

    def __isub__(self, other):
        self._binary_sanity_check(other)
        self.difference_update(other)
        return self

    def difference_update(self, other):
        data = self._data
        if not isinstance(other, BaseSet):
            other = Set(other)
        for elt in ifilter(data.has_key, other):
            del data[elt]

    def update(self, iterable):
        self._update(iterable)

    def clear(self):
        self._data.clear()

    def add(self, element):
        try:
            self._data[element] = True
        except TypeError:
            transform = getattr(element, '__as_immutable__', None)
            if transform is None:
                raise
            self._data[transform()] = True

        return

    def remove(self, element):
        try:
            del self._data[element]
        except TypeError:
            transform = getattr(element, '__as_temporarily_immutable__', None)
            if transform is None:
                raise
            del self._data[transform()]

        return

    def discard(self, element):
        try:
            self.remove(element)
        except KeyError:
            pass

    def pop(self):
        return self._data.popitem()[0]

    def __as_immutable__(self):
        return ImmutableSet(self)

    def __as_temporarily_immutable__(self):
        return _TemporarilyImmutableSet(self)


class _TemporarilyImmutableSet(BaseSet):
    __module__ = __name__

    def __init__(self, set):
        self._set = set
        self._data = set._data

    def __hash__(self):
        return self._set._compute_hash()# decompiled 0 files: 0 okay, 1 failed, 0 verify failed
# 2013.08.22 22:13:27 Pacific Daylight Time

# Can't uncompyle C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\sets.pyc
Traceback (most recent call last):
  File "C:\python27\lib\uncompyle2\__init__.py", line 206, in main
    uncompyle_file(infile, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 143, in uncompyle_file
    uncompyle(version, co, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 132, in uncompyle
    raise walk.ERROR
ParserError: --- This code section failed: ---

0	LOAD_FAST         'predicate'
3	LOAD_CONST        None
6	COMPARE_OP        'is'
9	JUMP_IF_FALSE     '24'

12	LOAD_CONST        '<code_object predicate>'
15	MAKE_FUNCTION_0   None
18	STORE_FAST        'predicate'
21	JUMP_FORWARD      '24'
24_0	COME_FROM         '21'

24	SETUP_LOOP        '60'
27	LOAD_FAST         'iterable'
30	GET_ITER          None
31	FOR_ITER          '59'
34	STORE_FAST        'x'

37	LOAD_FAST         'predicate'
40	LOAD_FAST         'x'
43	CALL_FUNCTION_1   None
46	JUMP_IF_TRUE      '56'

49	LOAD_FAST         'x'
52_0	COME_FROM         '46'
52	YIELD_VALUE       None
53	CONTINUE          '31'
56	JUMP_BACK         '31'
59	POP_BLOCK         None
60_0	COME_FROM         '24'
60	LOAD_CONST        None
63	RETURN_VALUE      None

Syntax error at or near `CONTINUE' token at offset 53

