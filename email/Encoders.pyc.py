# 2013.08.22 22:14:58 Pacific Daylight Time
# Embedded file name: email.Encoders
import base64
from quopri import encodestring as _encodestring

def _qencode(s):
    enc = _encodestring(s, quotetabs=True)
    return enc.replace(' ', '=20')


def _bencode(s):
    if not s:
        return s
    hasnewline = s[-1] == '\n'
    value = base64.encodestring(s)
    if not hasnewline and value[-1] == '\n':
        return value[:-1]
    return value


def encode_base64(msg):
    orig = msg.get_payload()
    encdata = _bencode(orig)
    msg.set_payload(encdata)
    msg['Content-Transfer-Encoding'] = 'base64'


def encode_quopri(msg):
    orig = msg.get_payload()
    encdata = _qencode(orig)
    msg.set_payload(encdata)
    msg['Content-Transfer-Encoding'] = 'quoted-printable'


def encode_7or8bit(msg):
    orig = msg.get_payload()
    if orig is None:
        msg['Content-Transfer-Encoding'] = '7bit'
        return
    try:
        orig.encode('ascii')
    except UnicodeError:
        charset = msg.get_charset()
        if charset:
            output_cset = charset.output_charset
            msg['Content-Transfer-Encoding'] = output_cset and output_cset.lower().startswith('iso-2202-') and '7bit'
        else:
            msg['Content-Transfer-Encoding'] = '8bit'
    else:
        msg['Content-Transfer-Encoding'] = '7bit'

    return


def encode_noop(msg):
    pass
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\email\Encoders.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:14:58 Pacific Daylight Time
