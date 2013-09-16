# 2013.08.22 22:12:53 Pacific Daylight Time
# Embedded file name: calendar
import datetime
__all__ = ['error',
 'setfirstweekday',
 'firstweekday',
 'isleap',
 'leapdays',
 'weekday',
 'monthrange',
 'monthcalendar',
 'prmonth',
 'month',
 'prcal',
 'calendar',
 'timegm',
 'month_name',
 'month_abbr',
 'day_name',
 'day_abbr']
error = ValueError
January = 1
February = 2
mdays = [0,
 31,
 28,
 31,
 30,
 31,
 30,
 31,
 31,
 30,
 31,
 30,
 31]

class _localized_month():
    __module__ = __name__
    _months = [ datetime.date(2001, i + 1, 1).strftime for i in range(12) ]
    _months.insert(0, lambda x: '')

    def __init__(self, format):
        self.format = format

    def __getitem__(self, i):
        funcs = self._months[i]
        if isinstance(i, slice):
            return [ f(self.format) for f in funcs ]
        else:
            return funcs(self.format)

    def __len__(self):
        return 13


class _localized_day():
    __module__ = __name__
    _days = [ datetime.date(2001, 1, i + 1).strftime for i in range(7) ]

    def __init__(self, format):
        self.format = format

    def __getitem__(self, i):
        funcs = self._days[i]
        if isinstance(i, slice):
            return [ f(self.format) for f in funcs ]
        else:
            return funcs(self.format)

    def __len__(self):
        return 7


day_name = _localized_day('%A')
day_abbr = _localized_day('%a')
month_name = _localized_month('%B')
month_abbr = _localized_month('%b')
MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY = range(7)
_firstweekday = 0

def firstweekday():
    global _firstweekday
    return _firstweekday


def setfirstweekday(weekday):
    global _firstweekday
    if not MONDAY <= weekday <= SUNDAY:
        raise ValueError, 'bad weekday number; must be 0 (Monday) to 6 (Sunday)'
    _firstweekday = weekday


def isleap(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def leapdays(y1, y2):
    y1 -= 1
    y2 -= 1
    return y2 // 4 - y1 // 4 - (y2 // 100 - y1 // 100) + (y2 // 400 - y1 // 400)


def weekday(year, month, day):
    return datetime.date(year, month, day).weekday()


def monthrange(year, month):
    if not 1 <= month <= 12:
        raise ValueError, 'bad month number'
    day1 = weekday(year, month, 1)
    ndays = mdays[month] + (month == February and isleap(year))
    return (day1, ndays)


def monthcalendar(year, month):
    day1, ndays = monthrange(year, month)
    rows = []
    r7 = range(7)
    day = (_firstweekday - day1 + 6) % 7 - 5
    while day <= ndays:
        row = [0,
         0,
         0,
         0,
         0,
         0,
         0]
        for i in r7:
            if 1 <= day <= ndays:
                row[i] = day
            day = day + 1

        rows.append(row)

    return rows


def prweek(theweek, width):
    print week(theweek, width),


def week(theweek, width):
    days = []
    for day in theweek:
        if day == 0:
            s = ''
        else:
            s = '%2i' % day
        days.append(s.center(width))

    return ' '.join(days)


def weekheader(width):
    if width >= 9:
        names = day_name
    else:
        names = day_abbr
    days = []
    for i in range(_firstweekday, _firstweekday + 7):
        days.append(names[i % 7][:width].center(width))

    return ' '.join(days)


def prmonth(theyear, themonth, w = 0, l = 0):
    print month(theyear, themonth, w, l),


def month(theyear, themonth, w = 0, l = 0):
    w = max(2, w)
    l = max(1, l)
    s = ('%s %r' % (month_name[themonth], theyear)).center(7 * (w + 1) - 1).rstrip() + '\n' * l + weekheader(w).rstrip() + '\n' * l
    for aweek in monthcalendar(theyear, themonth):
        s = s + week(aweek, w).rstrip() + '\n' * l

    return s[:-l] + '\n'


_colwidth = 7 * 3 - 1
_spacing = 6

def format3c(a, b, c, colwidth = _colwidth, spacing = _spacing):
    print format3cstring(a, b, c, colwidth, spacing)


def format3cstring(a, b, c, colwidth = _colwidth, spacing = _spacing):
    return a.center(colwidth) + ' ' * spacing + b.center(colwidth) + ' ' * spacing + c.center(colwidth)


def prcal(year, w = 0, l = 0, c = _spacing):
    print calendar(year, w, l, c),


def calendar(year, w = 0, l = 0, c = _spacing):
    w = max(2, w)
    l = max(1, l)
    c = max(2, c)
    colwidth = (w + 1) * 7 - 1
    s = repr(year).center(colwidth * 3 + c * 2).rstrip() + '\n' * l
    header = weekheader(w)
    header = format3cstring(header, header, header, colwidth, c).rstrip()
    for q in range(January, January + 12, 3):
        s = s + '\n' * l + format3cstring(month_name[q], month_name[q + 1], month_name[q + 2], colwidth, c).rstrip() + '\n' * l + header + '\n' * l
        data = []
        height = 0
        for amonth in range(q, q + 3):
            cal = monthcalendar(year, amonth)
            if len(cal) > height:
                height = len(cal)
            data.append(cal)

        for i in range(height):
            weeks = []
            for cal in data:
                if i >= len(cal):
                    weeks.append('')
                else:
                    weeks.append(week(cal[i], w))

            s = s + format3cstring(weeks[0], weeks[1], weeks[2], colwidth, c).rstrip() + '\n' * l

    return s[:-l] + '\n'


EPOCH = 1970
_EPOCH_ORD = datetime.date(EPOCH, 1, 1).toordinal()

def timegm(tuple):
    year, month, day, hour, minute, second = tuple[:6]
    days = datetime.date(year, month, 1).toordinal() - _EPOCH_ORD + day - 1
    hours = days * 24 + hour
    minutes = hours * 60 + minute
    seconds = minutes * 60 + second
    return seconds
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\calendar.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:12:53 Pacific Daylight Time
