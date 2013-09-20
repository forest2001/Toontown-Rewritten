# 2013.08.22 22:15:34 Pacific Daylight Time
# Embedded file name: otp.level.LevelUtil
import string
import LevelConstants

def getZoneNum2Node(levelModel, logFunc = lambda str: str):

    def findNumberedNodes(baseString, model, caseInsens = 1):
        srch = '**/%s*' % baseString
        if caseInsens:
            srch += ';+i'
        potentialNodes = model.findAllMatches(srch)
        num2node = {}
        for potentialNode in potentialNodes:
            name = potentialNode.getName()
            logFunc('potential match for %s: %s' % (baseString, name))
            name = name[len(baseString):]
            numDigits = 0
            while numDigits < len(name):
                if name[numDigits] not in string.digits:
                    break
                numDigits += 1

            if numDigits == 0:
                continue
            num = int(name[:numDigits])
            if num == LevelConstants.UberZoneEntId:
                logFunc('warning: cannot use UberZone zoneNum (%s). ignoring %s' % (LevelConstants.UberZoneEntId, potentialNode))
                continue
            if num < LevelConstants.MinZoneNum or num > LevelConstants.MaxZoneNum:
                logFunc('warning: zone %s is out of range. ignoring %s' % (num, potentialNode))
                continue
            if num in num2node:
                logFunc('warning: zone %s already assigned to %s. ignoring %s' % (num, num2node[num], potentialNode))
                continue
            num2node[num] = potentialNode

        return num2node

    zoneNum2node = findNumberedNodes('zone', levelModel)
    zoneNum2node[LevelConstants.UberZoneEntId] = levelModel
    return zoneNum2node
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\otp\level\LevelUtil.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:15:34 Pacific Daylight Time
