# 2013.08.22 22:13:12 Pacific Daylight Time
# Embedded file name: nturl2path


def url2pathname(url):
    import string, urllib
    if '|' not in url:
        if url[:4] == '////':
            url = url[2:]
        components = url.split('/')
        return urllib.unquote('\\'.join(components))
    comp = url.split('|')
    if len(comp) != 2 or comp[0][-1] not in string.ascii_letters:
        error = 'Bad URL: ' + url
        raise IOError, error
    drive = comp[0][-1].upper()
    components = comp[1].split('/')
    path = drive + ':'
    for comp in components:
        if comp:
            path = path + '\\' + urllib.unquote(comp)

    return path


def pathname2url(p):
    import urllib
    if ':' not in p:
        if p[:2] == '\\\\':
            p = '\\\\' + p
        components = p.split('\\')
        return urllib.quote('/'.join(components))
    comp = p.split(':')
    if len(comp) != 2 or len(comp[0]) > 1:
        error = 'Bad path: ' + p
        raise IOError, error
    drive = urllib.quote(comp[0].upper())
    components = comp[1].split('\\')
    path = '///' + drive + '|'
    for comp in components:
        if comp:
            path = path + '/' + urllib.quote(comp)

    return path
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\nturl2path.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:13:12 Pacific Daylight Time
