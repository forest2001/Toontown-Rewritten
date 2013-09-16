# 2013.08.22 22:13:43 Pacific Daylight Time
# Embedded file name: __future__
all_feature_names = ['nested_scopes', 'generators', 'division']
__all__ = ['all_feature_names'] + all_feature_names
CO_NESTED = 16
CO_GENERATOR_ALLOWED = 4096
CO_FUTURE_DIVISION = 8192

class _Feature():
    __module__ = __name__

    def __init__(self, optionalRelease, mandatoryRelease, compiler_flag):
        self.optional = optionalRelease
        self.mandatory = mandatoryRelease
        self.compiler_flag = compiler_flag

    def getOptionalRelease(self):
        return self.optional

    def getMandatoryRelease(self):
        return self.mandatory

    def __repr__(self):
        return '_Feature' + repr((self.optional, self.mandatory, self.compiler_flag))


nested_scopes = _Feature((2, 1, 0, 'beta', 1), (2, 2, 0, 'alpha', 0), CO_NESTED)
generators = _Feature((2, 2, 0, 'alpha', 1), (2, 3, 0, 'final', 0), CO_GENERATOR_ALLOWED)
division = _Feature((2, 2, 0, 'alpha', 2), (3, 0, 0, 'alpha', 0), CO_FUTURE_DIVISION)
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\__future__.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:13:43 Pacific Daylight Time
