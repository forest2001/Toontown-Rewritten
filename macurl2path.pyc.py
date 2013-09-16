# 2013.08.22 22:13:09 Pacific Daylight Time
# Embedded file name: macurl2path
import urllib
import os
__all__ = ['url2pathname', 'pathname2url']

def url2pathname(pathname):
    tp = urllib.splittype(pathname)[0]
    if tp and tp != 'file':
        raise RuntimeError, 'Cannot convert non-local URL to pathname'
    if pathname[:3] == '///':
        pathname = pathname[2:]
    elif pathname[:2] == '//':
        raise RuntimeError, 'Cannot convert non-local URL to pathname'
    components = pathname.split('/')
    i = 0
    while i < len(components):
        if components[i] == '.':
            del components[i]
        elif components[i] == '..' and i > 0 and components[i - 1] not in ('', '..'):
            del components[i - 1:i + 1]
            i = i - 1
        elif components[i] == '' and i > 0 and components[i - 1] != '':
            del components[i]
        else:
            i = i + 1

    if not components[0]:
        rv = ':'.join(components[1:])
    else:
        i = 0
        while i < len(components) and components[i] == '..':
            components[i] = ''
            i = i + 1

        rv = ':' + ':'.join(components)
    return urllib.unquote(rv)


def pathname2url(pathname):
    if '/' in pathname:
        raise RuntimeError, 'Cannot convert pathname containing slashes'
    components = pathname.split(':')
    if components[0] == '':
        del components[0]
    if components[-1] == '':
        del components[-1]
    for i in range(len(components)):
        if components[i] == '':
            components[i] = '..'

    components = map(_pncomp2url, components)
    if os.path.isabs(pathname):
        return '/' + '/'.join(components)
    else:
        return '/'.join(components)


def _pncomp2url(component):
    component = urllib.quote(component[:31], safe='')
    return component


def test():
    for url in ['index.html',
     'bar/index.html',
     '/foo/bar/index.html',
     '/foo/bar/',
     '/']:
        print '%r -> %r' % (url, url2pathname(url))

    for path in ['drive:',
     'drive:dir:',
     'drive:dir:file',
     'drive:file',
     'file',
     ':file',
     ':dir:',
     ':dir:file']:
        print '%r -> %r' % (path, pathname2url(path))


if __name__ == '__main__':
    test()
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\macurl2path.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:13:10 Pacific Daylight Time
