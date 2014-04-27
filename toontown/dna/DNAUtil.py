from DNAVisGroup import DNAVisGroup
import re


def getChildrenOfType(root, type):
    list = []
    r_getChildrenOfType(root, type, list)
    return list

def r_getChildrenOfType(root, type, list):
    for child in root.children:
        if isinstance(child, type):
            list.append(child)
        r_getChildrenOfType(child, type, list)

def getVisGroups(root):
    return getChildrenOfType(root, DNAVisGroup)


INDEX_REGEX = re.compile('([a-z][a-z])([0-9]+):')
def getBuildingClassFromName(name):
    match = INDEX_REGEX.match(name)
    if not match:
        return None
    else:
        return match.group(1)

def getBlockFromName(name):
    match = INDEX_REGEX.match(name)
    if not match:
        return None
    else:
        return int(match.group(2))
