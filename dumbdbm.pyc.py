# 2013.08.22 22:12:59 Pacific Daylight Time
# Embedded file name: dumbdbm
import os as _os
import __builtin__
import UserDict
_open = __builtin__.open
_BLOCKSIZE = 512
error = IOError

class _Database(UserDict.DictMixin):
    __module__ = __name__
    _os = _os
    _open = _open

    def __init__(self, filebasename, mode):
        self._mode = mode
        self._dirfile = filebasename + _os.extsep + 'dir'
        self._datfile = filebasename + _os.extsep + 'dat'
        self._bakfile = filebasename + _os.extsep + 'bak'
        self._index = None
        try:
            f = _open(self._datfile, 'r')
        except IOError:
            f = _open(self._datfile, 'w', self._mode)

        f.close()
        self._update()
        return

    def _update(self):
        self._index = {}
        try:
            f = _open(self._dirfile)
        except IOError:
            pass
        else:
            for line in f:
                key, pos_and_siz_pair = eval(line)
                self._index[key] = pos_and_siz_pair

            f.close()

    def _commit(self):
        if self._index is None:
            return
        try:
            self._os.unlink(self._bakfile)
        except self._os.error:
            pass

        try:
            self._os.rename(self._dirfile, self._bakfile)
        except self._os.error:
            pass

        f = self._open(self._dirfile, 'w', self._mode)
        for key, pos_and_siz_pair in self._index.iteritems():
            f.write('%r, %r\n' % (key, pos_and_siz_pair))

        f.close()
        return

    sync = _commit

    def __getitem__(self, key):
        pos, siz = self._index[key]
        f = _open(self._datfile, 'rb')
        f.seek(pos)
        dat = f.read(siz)
        f.close()
        return dat

    def _addval(self, val):
        f = _open(self._datfile, 'rb+')
        f.seek(0, 2)
        pos = int(f.tell())
        npos = (pos + _BLOCKSIZE - 1) // _BLOCKSIZE * _BLOCKSIZE
        f.write('\x00' * (npos - pos))
        pos = npos
        f.write(val)
        f.close()
        return (pos, len(val))

    def _setval(self, pos, val):
        f = _open(self._datfile, 'rb+')
        f.seek(pos)
        f.write(val)
        f.close()
        return (pos, len(val))

    def _addkey(self, key, pos_and_siz_pair):
        self._index[key] = pos_and_siz_pair
        f = _open(self._dirfile, 'a', self._mode)
        f.write('%r, %r\n' % (key, pos_and_siz_pair))
        f.close()

    def __setitem__(self, key, val):
        if not type(key) == type('') == type(val):
            raise TypeError, 'keys and values must be strings'
        if key not in self._index:
            self._addkey(key, self._addval(val))
        else:
            pos, siz = self._index[key]
            oldblocks = (siz + _BLOCKSIZE - 1) // _BLOCKSIZE
            newblocks = (len(val) + _BLOCKSIZE - 1) // _BLOCKSIZE
            if newblocks <= oldblocks:
                self._index[key] = self._setval(pos, val)
            else:
                self._index[key] = self._addval(val)

    def __delitem__(self, key):
        del self._index[key]
        self._commit()

    def keys(self):
        return self._index.keys()

    def has_key(self, key):
        return key in self._index

    def __contains__(self, key):
        return key in self._index

    def iterkeys(self):
        return self._index.iterkeys()

    __iter__ = iterkeys

    def __len__(self):
        return len(self._index)

    def close(self):
        self._commit()
        self._index = self._datfile = self._dirfile = self._bakfile = None
        return

    __del__ = close


def open(file, flag = None, mode = 438):
    return _Database(file, mode)
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\dumbdbm.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:12:59 Pacific Daylight Time
