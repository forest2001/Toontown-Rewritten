# 2013.08.22 22:13:58 Pacific Daylight Time
# Embedded file name: direct.directutil.Verify
wantVerifyPdb = 0

def verify(assertion):
    if not assertion:
        print '\n\nverify failed:'
        import sys
        print '    File "%s", line %d' % (sys._getframe(1).f_code.co_filename, sys._getframe(1).f_lineno)
        if wantVerifyPdb:
            import pdb
            pdb.set_trace()
        raise AssertionError


if not hasattr(__builtins__, 'verify'):
    __builtins__['verify'] = verify
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\directutil\Verify.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:13:58 Pacific Daylight Time
