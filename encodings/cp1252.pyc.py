# 2013.08.22 22:15:03 Pacific Daylight Time
# Embedded file name: encodings.cp1252
import codecs

class Codec(codecs.Codec):
    __module__ = __name__

    def encode(self, input, errors = 'strict'):
        return codecs.charmap_encode(input, errors, encoding_map)

    def decode(self, input, errors = 'strict'):
        return codecs.charmap_decode(input, errors, decoding_map)


class StreamWriter(Codec, codecs.StreamWriter):
    __module__ = __name__


class StreamReader(Codec, codecs.StreamReader):
    __module__ = __name__


def getregentry():
    return (Codec().encode,
     Codec().decode,
     StreamReader,
     StreamWriter)


decoding_map = codecs.make_identity_dict(range(256))
decoding_map.update({128: 8364,
 129: None,
 130: 8218,
 131: 402,
 132: 8222,
 133: 8230,
 134: 8224,
 135: 8225,
 136: 710,
 137: 8240,
 138: 352,
 139: 8249,
 140: 338,
 141: None,
 142: 381,
 143: None,
 144: None,
 145: 8216,
 146: 8217,
 147: 8220,
 148: 8221,
 149: 8226,
 150: 8211,
 151: 8212,
 152: 732,
 153: 8482,
 154: 353,
 155: 8250,
 156: 339,
 157: None,
 158: 382,
 159: 376})
encoding_map = codecs.make_encoding_map(decoding_map)
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\encodings\cp1252.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:15:03 Pacific Daylight Time
