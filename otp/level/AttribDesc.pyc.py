# 2013.08.22 22:15:28 Pacific Daylight Time
# Embedded file name: otp.level.AttribDesc


class AttribDesc():
    __module__ = __name__

    def __init__(self, name, default, datatype = 'string', params = {}):
        self.name = name
        self.default = default
        self.datatype = datatype
        self.params = params

    def getName(self):
        return self.name

    def getDefaultValue(self):
        return self.default

    def getDatatype(self):
        return self.datatype

    def getParams(self):
        return self.params

    def __str__(self):
        return self.name

    def __repr__(self):
        return 'AttribDesc(%s, %s, %s, %s)' % (repr(self.name),
         repr(self.default),
         repr(self.datatype),
         repr(self.params))
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\otp\level\AttribDesc.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:15:28 Pacific Daylight Time
