# 2013.08.22 22:14:09 Pacific Daylight Time
# Embedded file name: direct.distributed.PyDatagram
from pandac.PandaModules import *

class PyDatagram(Datagram):
    __module__ = __name__
    FuncDict = {STInt8: (Datagram.addInt8, int),
     STInt16: (Datagram.addInt16, int),
     STInt32: (Datagram.addInt32, int),
     STInt64: (Datagram.addInt64, int),
     STUint8: (Datagram.addUint8, int),
     STUint16: (Datagram.addUint16, int),
     STUint32: (Datagram.addUint32, int),
     STUint64: (Datagram.addUint64, int),
     STFloat64: (Datagram.addFloat64, None),
     STString: (Datagram.addString, None),
     STBlob: (Datagram.addString, None),
     STBlob32: (Datagram.addString32, None)}
    addChannel = Datagram.addUint64

    def addServerHeader(self, channel, sender, code):
        self.addInt8(1)
        self.addChannel(channel)
        self.addChannel(sender)
        self.addUint16(code)

    def addOldServerHeader(self, channel, sender, code):
        self.addChannel(channel)
        self.addChannel(sender)
        self.addChannel('A')
        self.addUint16(code)

    def putArg(self, arg, subatomicType, divisor = 1):
        if divisor == 1:
            funcSpecs = self.FuncDict.get(subatomicType)
            if funcSpecs:
                addFunc, argFunc = funcSpecs
                if argFunc:
                    arg = argFunc(arg)
                addFunc(self, arg)
            elif subatomicType == STInt8array:
                self.addUint16(len(arg))
                for i in arg:
                    self.addInt8(int(i))

            elif subatomicType == STInt16array:
                self.addUint16(len(arg) << 1)
                for i in arg:
                    self.addInt16(int(i))

            elif subatomicType == STInt32array:
                self.addUint16(len(arg) << 2)
                for i in arg:
                    self.addInt32(int(i))

            elif subatomicType == STUint8array:
                self.addUint16(len(arg))
                for i in arg:
                    self.addUint8(int(i))

            elif subatomicType == STUint16array:
                self.addUint16(len(arg) << 1)
                for i in arg:
                    self.addUint16(int(i))

            elif subatomicType == STUint32array:
                self.addUint16(len(arg) << 2)
                for i in arg:
                    self.addUint32(int(i))

            elif subatomicType == STUint32uint8array:
                self.addUint16(len(arg) * 5)
                for i in arg:
                    self.addUint32(int(i[0]))
                    self.addUint8(int(i[1]))

            else:
                raise Exception('Error: No such type as: ' + str(subatomicType))
        else:
            funcSpecs = self.FuncDict.get(subatomicType)
            if funcSpecs:
                addFunc, argFunc = funcSpecs
                addFunc(self, int(round(arg * divisor)))
            elif subatomicType == STInt8array:
                self.addUint16(len(arg))
                for i in arg:
                    self.addInt8(int(round(i * divisor)))

            elif subatomicType == STInt16array:
                self.addUint16(len(arg) << 1)
                for i in arg:
                    self.addInt16(int(round(i * divisor)))

            elif subatomicType == STInt32array:
                self.addUint16(len(arg) << 2)
                for i in arg:
                    self.addInt32(int(round(i * divisor)))

            elif subatomicType == STUint8array:
                self.addUint16(len(arg))
                for i in arg:
                    self.addUint8(int(round(i * divisor)))

            elif subatomicType == STUint16array:
                self.addUint16(len(arg) << 1)
                for i in arg:
                    self.addUint16(int(round(i * divisor)))

            elif subatomicType == STUint32array:
                self.addUint16(len(arg) << 2)
                for i in arg:
                    self.addUint32(int(round(i * divisor)))

            elif subatomicType == STUint32uint8array:
                self.addUint16(len(arg) * 5)
                for i in arg:
                    self.addUint32(int(round(i[0] * divisor)))
                    self.addUint8(int(round(i[1] * divisor)))

            else:
                raise Exception('Error: type does not accept divisor: ' + str(subatomicType))
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\distributed\PyDatagram.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:14:09 Pacific Daylight Time
