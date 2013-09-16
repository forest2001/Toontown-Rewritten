# 2013.08.22 22:13:58 Pacific Daylight Time
# Embedded file name: direct.directtools.DirectUtil
from DirectGlobals import *

def ROUND_TO(value, divisor):
    return round(value / float(divisor)) * divisor


def ROUND_INT(val):
    return int(round(val))


def CLAMP(val, minVal, maxVal):
    return min(max(val, minVal), maxVal)


def getTkColorString(color):

    def toHex(intVal):
        val = int(round(intVal))
        if val < 16:
            return '0' + hex(val)[2:]
        else:
            return hex(val)[2:]

    r = toHex(color[0])
    g = toHex(color[1])
    b = toHex(color[2])
    return '#' + r + g + b


def lerpBackgroundColor(r, g, b, duration):

    def lerpColor(state):
        dt = globalClock.getDt()
        state.time += dt
        sf = state.time / state.duration
        if sf >= 1.0:
            base.setBackgroundColor(state.ec[0], state.ec[1], state.ec[2])
            return Task.done
        else:
            r = sf * state.ec[0] + (1 - sf) * state.sc[0]
            g = sf * state.ec[1] + (1 - sf) * state.sc[1]
            b = sf * state.ec[2] + (1 - sf) * state.sc[2]
            base.setBackgroundColor(r, g, b)
            return Task.cont

    taskMgr.remove('lerpBackgroundColor')
    t = taskMgr.add(lerpColor, 'lerpBackgroundColor')
    t.time = 0.0
    t.duration = duration
    t.sc = base.getBackgroundColor()
    t.ec = VBase4(r, g, b, 1)


def useDirectRenderStyle(nodePath, priority = 0):
    nodePath.setLightOff(priority)
    nodePath.setRenderModeFilled()


def getFileData(filename, separator = ','):
    f = open(filename.toOsSpecific(), 'r')
    rawData = f.readlines()
    f.close()
    fileData = []
    for line in rawData:
        l = line.strip()
        if l:
            data = map(lambda s: s.strip(), l.split(separator))
            fileData.append(data)

    return fileData
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\directtools\DirectUtil.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:13:58 Pacific Daylight Time
