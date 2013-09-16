# 2013.08.22 22:15:01 Pacific Daylight Time
# Embedded file name: email.Utils
import os
import re
import time
import base64
import random
import socket
import warnings
from cStringIO import StringIO
from email._parseaddr import quote
from email._parseaddr import AddressList as _AddressList
from email._parseaddr import mktime_tz
from email._parseaddr import parsedate as _parsedate
from email._parseaddr import parsedate_tz as _parsedate_tz
from quopri import decodestring as _qdecode
from email.Encoders import _bencode, _qencode
COMMASPACE = ', '
EMPTYSTRING = ''
UEMPTYSTRING = u''
CRLF = '\r\n'
specialsre = re.compile('[][\\\\()<>@,:;".]')
escapesre = re.compile('[][\\\\()"]')

def _identity(s):
    return s


def _bdecode(s):
    if not s:
        return s
    value = base64.decodestring(s)
    if not s.endswith('\n') and value.endswith('\n'):
        return value[:-1]
    return value


def fix_eols(s):
    s = re.sub('(?<!\\r)\\n', CRLF, s)
    s = re.sub('\\r(?!\\n)', CRLF, s)
    return s


def formataddr(pair):
    name, address = pair
    if name:
        quotes = ''
        if specialsre.search(name):
            quotes = '"'
        name = escapesre.sub('\\\\\\g<0>', name)
        return '%s%s%s <%s>' % (quotes,
         name,
         quotes,
         address)
    return address


def getaddresses(fieldvalues):
    all = COMMASPACE.join(fieldvalues)
    a = _AddressList(all)
    return a.addresslist


ecre = re.compile('\n  =\\?                   # literal =?\n  (?P<charset>[^?]*?)   # non-greedy up to the next ? is the charset\n  \\?                    # literal ?\n  (?P<encoding>[qb])    # either a "q" or a "b", case insensitive\n  \\?                    # literal ?\n  (?P<atom>.*?)         # non-greedy up to the next ?= is the atom\n  \\?=                   # literal ?=\n  ', re.VERBOSE | re.IGNORECASE)

def formatdate(timeval = None, localtime = False, usegmt = False):
    if timeval is None:
        timeval = time.time()
    if localtime:
        now = time.localtime(timeval)
        if time.daylight and now[-1]:
            offset = time.altzone
        else:
            offset = time.timezone
        hours, minutes = divmod(abs(offset), 3600)
        if offset > 0:
            sign = '-'
        else:
            sign = '+'
        zone = '%s%02d%02d' % (sign, hours, minutes // 60)
    else:
        now = time.gmtime(timeval)
        if usegmt:
            zone = 'GMT'
        else:
            zone = '-0000'
    return '%s, %02d %s %04d %02d:%02d:%02d %s' % (['Mon',
      'Tue',
      'Wed',
      'Thu',
      'Fri',
      'Sat',
      'Sun'][now[6]],
     now[2],
     ['Jan',
      'Feb',
      'Mar',
      'Apr',
      'May',
      'Jun',
      'Jul',
      'Aug',
      'Sep',
      'Oct',
      'Nov',
      'Dec'][now[1] - 1],
     now[0],
     now[3],
     now[4],
     now[5],
     zone)


def make_msgid(idstring = None):
    timeval = time.time()
    utcdate = time.strftime('%Y%m%d%H%M%S', time.gmtime(timeval))
    pid = os.getpid()
    randint = random.randrange(100000)
    if idstring is None:
        idstring = ''
    else:
        idstring = '.' + idstring
    idhost = socket.getfqdn()
    msgid = '<%s.%s.%s%s@%s>' % (utcdate,
     pid,
     randint,
     idstring,
     idhost)
    return msgid


def parsedate(data):
    if not data:
        return None
    return _parsedate(data)


def parsedate_tz(data):
    if not data:
        return None
    return _parsedate_tz(data)


def parseaddr(addr):
    addrs = _AddressList(addr).addresslist
    if not addrs:
        return ('', '')
    return addrs[0]


def unquote(str):
    if len(str) > 1:
        if str.startswith('"') and str.endswith('"'):
            return str[1:-1].replace('\\\\', '\\').replace('\\"', '"')
        if str.startswith('<') and str.endswith('>'):
            return str[1:-1]
    return str


def decode_rfc2231(s):
    import urllib
    parts = s.split("'", 2)
    if len(parts) == 1:
        return (None, None, urllib.unquote(s))
    charset, language, s = parts
    return (charset, language, urllib.unquote(s))


def encode_rfc2231(s, charset = None, language = None):
    import urllib
    s = urllib.quote(s, safe='')
    if charset is None and language is None:
        return s
    if language is None:
        language = ''
    return "%s'%s'%s" % (charset, language, s)


rfc2231_continuation = re.compile('^(?P<name>\\w+)\\*((?P<num>[0-9]+)\\*?)?$')

def decode_params(params):
    new_params = []
    rfc2231_params = {}
    name, value = params[0]
    new_params.append((name, value))
    for name, value in params[1:]:
        value = unquote(value)
        mo = rfc2231_continuation.match(name)
        if mo:
            name, num = mo.group('name', 'num')
            if num is not None:
                num = int(num)
            rfc2231_param1 = rfc2231_params.setdefault(name, [])
            rfc2231_param1.append((num, value))
        else:
            new_params.append((name, '"%s"' % quote(value)))

    if rfc2231_params:
        for name, continuations in rfc2231_params.items():
            value = []
            continuations.sort()
            for num, continuation in continuations:
                value.append(continuation)

            charset, language, value = decode_rfc2231(EMPTYSTRING.join(value))
            new_params.append((name, (charset, language, '"%s"' % quote(value))))

    return new_params


def collapse_rfc2231_value(value, errors = 'replace', fallback_charset = 'us-ascii'):
    if isinstance(value, tuple):
        rawval = unquote(value[2])
        charset = value[0] or 'us-ascii'
        try:
            return unicode(rawval, charset, errors)
        except LookupError:
            return unicode(rawval, fallback_charset, errors)

    else:
        return unquote(value)
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\email\Utils.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:15:02 Pacific Daylight Time
