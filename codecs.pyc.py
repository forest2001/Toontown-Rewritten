# 2013.08.22 22:12:54 Pacific Daylight Time
# Embedded file name: codecs
import __builtin__, sys
try:
    from _codecs import *
except ImportError as why:
    raise SystemError, 'Failed to load the builtin codecs: %s' % why

__all__ = ['register',
 'lookup',
 'open',
 'EncodedFile',
 'BOM',
 'BOM_BE',
 'BOM_LE',
 'BOM32_BE',
 'BOM32_LE',
 'BOM64_BE',
 'BOM64_LE',
 'BOM_UTF8',
 'BOM_UTF16',
 'BOM_UTF16_LE',
 'BOM_UTF16_BE',
 'BOM_UTF32',
 'BOM_UTF32_LE',
 'BOM_UTF32_BE',
 'strict_errors',
 'ignore_errors',
 'replace_errors',
 'xmlcharrefreplace_errors',
 'register_error',
 'lookup_error']
BOM_UTF8 = '\xef\xbb\xbf'
BOM_LE = BOM_UTF16_LE = '\xff\xfe'
BOM_BE = BOM_UTF16_BE = '\xfe\xff'
BOM_UTF32_LE = '\xff\xfe\x00\x00'
BOM_UTF32_BE = '\x00\x00\xfe\xff'
if sys.byteorder == 'little':
    BOM = BOM_UTF16 = BOM_UTF16_LE
    BOM_UTF32 = BOM_UTF32_LE
else:
    BOM = BOM_UTF16 = BOM_UTF16_BE
    BOM_UTF32 = BOM_UTF32_BE
BOM32_LE = BOM_UTF16_LE
BOM32_BE = BOM_UTF16_BE
BOM64_LE = BOM_UTF32_LE
BOM64_BE = BOM_UTF32_BE

class Codec():
    __module__ = __name__

    def encode(self, input, errors = 'strict'):
        raise NotImplementedError

    def decode(self, input, errors = 'strict'):
        raise NotImplementedError


class StreamWriter(Codec):
    __module__ = __name__

    def __init__(self, stream, errors = 'strict'):
        self.stream = stream
        self.errors = errors

    def write(self, object):
        data, consumed = self.encode(object, self.errors)
        self.stream.write(data)

    def writelines(self, list):
        self.write(''.join(list))

    def reset(self):
        pass

    def __getattr__(self, name, getattr = getattr):
        return getattr(self.stream, name)


class StreamReader(Codec):
    __module__ = __name__

    def __init__(self, stream, errors = 'strict'):
        self.stream = stream
        self.errors = errors
        self.bytebuffer = ''
        self.charbuffer = u''
        self.atcr = False

    def decode(self, input, errors = 'strict'):
        raise NotImplementedError

    def read(self, size = -1, chars = -1):
        while True:
            if chars < 0:
                if self.charbuffer:
                    break
            elif len(self.charbuffer) >= chars:
                break
            if size < 0:
                newdata = self.stream.read()
            else:
                newdata = self.stream.read(size)
            data = self.bytebuffer + newdata
            newchars, decodedbytes = self.decode(data, self.errors)
            self.bytebuffer = data[decodedbytes:]
            self.charbuffer += newchars
            if not newdata:
                break

        if chars < 0:
            result = self.charbuffer
            self.charbuffer = u''
        else:
            result = self.charbuffer[:chars]
            self.charbuffer = self.charbuffer[chars:]
        return result

    def readline(self, size = None, keepends = True):
        readsize = size or 72
        line = u''
        while True:
            data = self.read(readsize)
            if self.atcr and data.startswith(u'\n'):
                data = data[1:]
            if data:
                self.atcr = data.endswith(u'\r')
            line += data
            lines = line.splitlines(True)
            if lines:
                line0withend = lines[0]
                line0withoutend = lines[0].splitlines(False)[0]
                if line0withend != line0withoutend:
                    self.charbuffer = u''.join(lines[1:]) + self.charbuffer
                    if keepends:
                        line = line0withend
                    else:
                        line = line0withoutend
                    break
            if not data or size is not None:
                if line and not keepends:
                    line = line.splitlines(False)[0]
                break
            if readsize < 8000:
                readsize *= 2

        return line

    def readlines(self, sizehint = None, keepends = True):
        data = self.read()
        return data.splitlines(keepends)

    def reset(self):
        self.bytebuffer = ''
        self.charbuffer = u''
        self.atcr = False

    def seek(self, offset, whence = 0):
        self.reset()
        self.stream.seek(offset, whence)

    def next(self):
        line = self.readline()
        if line:
            return line
        raise StopIteration

    def __iter__(self):
        return self

    def __getattr__(self, name, getattr = getattr):
        return getattr(self.stream, name)


class StreamReaderWriter():
    __module__ = __name__
    encoding = 'unknown'

    def __init__(self, stream, Reader, Writer, errors = 'strict'):
        self.stream = stream
        self.reader = Reader(stream, errors)
        self.writer = Writer(stream, errors)
        self.errors = errors

    def read(self, size = -1):
        return self.reader.read(size)

    def readline(self, size = None):
        return self.reader.readline(size)

    def readlines(self, sizehint = None):
        return self.reader.readlines(sizehint)

    def next(self):
        return self.reader.next()

    def __iter__(self):
        return self

    def write(self, data):
        return self.writer.write(data)

    def writelines(self, list):
        return self.writer.writelines(list)

    def reset(self):
        self.reader.reset()
        self.writer.reset()

    def __getattr__(self, name, getattr = getattr):
        return getattr(self.stream, name)


class StreamRecoder():
    __module__ = __name__
    data_encoding = 'unknown'
    file_encoding = 'unknown'

    def __init__(self, stream, encode, decode, Reader, Writer, errors = 'strict'):
        self.stream = stream
        self.encode = encode
        self.decode = decode
        self.reader = Reader(stream, errors)
        self.writer = Writer(stream, errors)
        self.errors = errors

    def read(self, size = -1):
        data = self.reader.read(size)
        data, bytesencoded = self.encode(data, self.errors)
        return data

    def readline(self, size = None):
        if size is None:
            data = self.reader.readline()
        else:
            data = self.reader.readline(size)
        data, bytesencoded = self.encode(data, self.errors)
        return data

    def readlines(self, sizehint = None):
        data = self.reader.read()
        data, bytesencoded = self.encode(data, self.errors)
        return data.splitlines(1)

    def next(self):
        return self.reader.next()

    def __iter__(self):
        return self

    def write(self, data):
        data, bytesdecoded = self.decode(data, self.errors)
        return self.writer.write(data)

    def writelines(self, list):
        data = ''.join(list)
        data, bytesdecoded = self.decode(data, self.errors)
        return self.writer.write(data)

    def reset(self):
        self.reader.reset()
        self.writer.reset()

    def __getattr__(self, name, getattr = getattr):
        return getattr(self.stream, name)


def open(filename, mode = 'rb', encoding = None, errors = 'strict', buffering = 1):
    if encoding is not None and 'b' not in mode:
        mode = mode + 'b'
    file = __builtin__.open(filename, mode, buffering)
    if encoding is None:
        return file
    e, d, sr, sw = lookup(encoding)
    srw = StreamReaderWriter(file, sr, sw, errors)
    srw.encoding = encoding
    return srw


def EncodedFile(file, data_encoding, file_encoding = None, errors = 'strict'):
    if file_encoding is None:
        file_encoding = data_encoding
    encode, decode = lookup(data_encoding)[:2]
    Reader, Writer = lookup(file_encoding)[2:]
    sr = StreamRecoder(file, encode, decode, Reader, Writer, errors)
    sr.data_encoding = data_encoding
    sr.file_encoding = file_encoding
    return sr


def getencoder(encoding):
    return lookup(encoding)[0]


def getdecoder(encoding):
    return lookup(encoding)[1]


def getreader(encoding):
    return lookup(encoding)[2]


def getwriter(encoding):
    return lookup(encoding)[3]


def make_identity_dict(rng):
    res = {}
    for i in rng:
        res[i] = i

    return res


def make_encoding_map(decoding_map):
    m = {}
    for k, v in decoding_map.items():
        if v not in m:
            m[v] = k
        else:
            m[v] = None

    return m


try:
    strict_errors = lookup_error('strict')
    ignore_errors = lookup_error('ignore')
    replace_errors = lookup_error('replace')
    xmlcharrefreplace_errors = lookup_error('xmlcharrefreplace')
    backslashreplace_errors = lookup_error('backslashreplace')
except LookupError:
    strict_errors = None
    ignore_errors = None
    replace_errors = None
    xmlcharrefreplace_errors = None
    backslashreplace_errors = None

_false = 0
if _false:
    import encodings
if __name__ == '__main__':
    sys.stdout = EncodedFile(sys.stdout, 'latin-1', 'utf-8')
    sys.stdin = EncodedFile(sys.stdin, 'utf-8', 'latin-1')
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\codecs.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:12:54 Pacific Daylight Time
