from DNAVisGroup import DNAVisGroup
import re


def getVisGroups(root):
    visGroups = []
    r_getVisGroups(root, visGroups)
    return visGroups
def r_getVisGroups(root, list):
    for child in root.children:
        if isinstance(child, DNAVisGroup):
            list.append(child)
        r_getVisGroups(child, list)

def getChildrenOfType(root, type):
    list = []
    r_getChildrenOfType(root, type, list)
    return list
def r_getChildrenOfType(root, type, list):
    for child in root.children:
        if isinstance(child, type):
            list.append(child)
        r_getVisGroups(child, list)


INDEX_REGEX = re.compile('tb([0-9]+):')
def getBlockFromName(name):
    match = INDEX_REGEX.match(name)
    if not match:
        return None
    else:
        return int(match.group(1))
