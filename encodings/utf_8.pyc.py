# 2013.08.22 22:15:03 Pacific Daylight Time
# Embedded file name: encodings.utf_8
import codecs
encode = codecs.utf_8_encode

def decode(input, errors = 'strict'):
    return codecs.utf_8_decode(input, errors, True)


class StreamWriter(codecs.StreamWriter):
    __module__ = __name__
    encode = codecs.utf_8_encode


class StreamReader(codecs.StreamReader):
    __module__ = __name__
    decode = codecs.utf_8_decode


def getregentry():
    return (encode,
     decode,
     StreamReader,
     StreamWriter)
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\encodings\utf_8.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:15:03 Pacific Daylight Time
