# 2013.08.22 22:15:54 Pacific Daylight Time
# Embedded file name: pytz.tzinfo
from datetime import datetime, timedelta, tzinfo
from bisect import bisect_right
from sets import Set
import pytz
__all__ = []
_timedelta_cache = {}

def memorized_timedelta(seconds):
    try:
        return _timedelta_cache[seconds]
    except KeyError:
        delta = timedelta(seconds=seconds)
        _timedelta_cache[seconds] = delta
        return delta


_datetime_cache = {}

def memorized_datetime(*args):
    try:
        return _datetime_cache[args]
    except KeyError:
        dt = datetime(*args)
        _datetime_cache[args] = dt
        return dt


_ttinfo_cache = {}

def memorized_ttinfo(*args):
    try:
        return _ttinfo_cache[args]
    except KeyError:
        ttinfo = (memorized_timedelta(args[0]), memorized_timedelta(args[1]), args[2])
        _ttinfo_cache[args] = ttinfo
        return ttinfo


_notime = memorized_timedelta(0)

def _to_seconds(td):
    return td.seconds + td.days * 24 * 60 * 60


class BaseTzInfo(tzinfo):
    __module__ = __name__
    _utcoffset = None
    _tzname = None
    zone = None

    def __str__(self):
        return self.zone


class StaticTzInfo(BaseTzInfo):
    __module__ = __name__

    def fromutc(self, dt):
        return (dt + self._utcoffset).replace(tzinfo=self)

    def utcoffset(self, dt):
        return self._utcoffset

    def dst(self, dt):
        return _notime

    def tzname(self, dt):
        return self._tzname

    def localize(self, dt, is_dst = False):
        if dt.tzinfo is not None:
            raise ValueError, 'Not naive datetime (tzinfo is already set)'
        return dt.replace(tzinfo=self)

    def normalize(self, dt, is_dst = False):
        if dt.tzinfo is None:
            raise ValueError, 'Naive time - no tzinfo set'
        return dt.replace(tzinfo=self)

    def __repr__(self):
        return '<StaticTzInfo %r>' % (self.zone,)

    def __reduce__(self):
        return (pytz._p, (self.zone,))


class DstTzInfo(BaseTzInfo):
    __module__ = __name__
    _utc_transition_times = None
    _transition_info = None
    zone = None
    _tzinfos = None
    _dst = None

    def __init__(self, _inf = None, _tzinfos = None):
        if _inf:
            self._tzinfos = _tzinfos
            self._utcoffset, self._dst, self._tzname = _inf
        else:
            _tzinfos = {}
            self._tzinfos = _tzinfos
            self._utcoffset, self._dst, self._tzname = self._transition_info[0]
            _tzinfos[self._transition_info[0]] = self
            for inf in self._transition_info[1:]:
                if not _tzinfos.has_key(inf):
                    _tzinfos[inf] = self.__class__(inf, _tzinfos)

    def fromutc(self, dt):
        dt = dt.replace(tzinfo=None)
        idx = max(0, bisect_right(self._utc_transition_times, dt) - 1)
        inf = self._transition_info[idx]
        return (dt + inf[0]).replace(tzinfo=self._tzinfos[inf])

    def normalize(self, dt):
        if dt.tzinfo is None:
            raise ValueError, 'Naive time - no tzinfo set'
        offset = dt.tzinfo._utcoffset
        dt = dt.replace(tzinfo=None)
        dt = dt - offset
        return self.fromutc(dt)

    def localize(self, dt, is_dst = False):
        if dt.tzinfo is not None:
            raise ValueError, 'Not naive datetime (tzinfo is already set)'
        possible_loc_dt = Set()
        for tzinfo in self._tzinfos.values():
            loc_dt = tzinfo.normalize(dt.replace(tzinfo=tzinfo))
            if loc_dt.replace(tzinfo=None) == dt:
                possible_loc_dt.add(loc_dt)

        if len(possible_loc_dt) == 1:
            return possible_loc_dt.pop()
        if is_dst is None:
            raise AmbiguousTimeError(dt)
        filtered_possible_loc_dt = [ p for p in possible_loc_dt if bool(p.tzinfo._dst) == is_dst ]
        if len(filtered_possible_loc_dt) == 1:
            return filtered_possible_loc_dt[0]
        if len(filtered_possible_loc_dt) == 0:
            filtered_possible_loc_dt = list(possible_loc_dt)

        def mycmp(a, b):
            return cmp(a.replace(tzinfo=None) - a.tzinfo._utcoffset, b.replace(tzinfo=None) - b.tzinfo._utcoffset)

        filtered_possible_loc_dt.sort(mycmp)
        return filtered_possible_loc_dt[0]

    def utcoffset(self, dt):
        return self._utcoffset

    def dst(self, dt):
        return self._dst

    def tzname(self, dt):
        return self._tzname

    def __repr__(self):
        if self._dst:
            dst = 'DST'
        else:
            dst = 'STD'
        if self._utcoffset > _notime:
            return '<DstTzInfo %r %s+%s %s>' % (self.zone,
             self._tzname,
             self._utcoffset,
             dst)
        else:
            return '<DstTzInfo %r %s%s %s>' % (self.zone,
             self._tzname,
             self._utcoffset,
             dst)

    def __reduce__(self):
        return (pytz._p, (self.zone,
          _to_seconds(self._utcoffset),
          _to_seconds(self._dst),
          self._tzname))


class AmbiguousTimeError(Exception):
    __module__ = __name__


def unpickler(zone, utcoffset = None, dstoffset = None, tzname = None):
    tz = pytz.timezone(zone)
    if utcoffset is None:
        return tz
    utcoffset = memorized_timedelta(utcoffset)
    dstoffset = memorized_timedelta(dstoffset)
    try:
        return tz._tzinfos[utcoffset, dstoffset, tzname]
    except KeyError:
        pass

    for localized_tz in tz._tzinfos.values():
        if localized_tz._utcoffset == utcoffset and localized_tz._dst == dstoffset:
            return localized_tz

    inf = (utcoffset, dstoffset, tzname)
    tz._tzinfos[inf] = tz.__class__(inf, tz._tzinfos)
    return tz._tzinfos[inf]
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\pytz\tzinfo.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:15:55 Pacific Daylight Time
