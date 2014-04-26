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
        r_getVisGroups(child, list)

def getVisGroups(root):
    return getChildrenOfType(DNAVisGroup)


INDEX_REGEX = re.compile('tb([0-9]+):')
def getBlockFromName(name):
    match = INDEX_REGEX.match(name)
    if not match:
        return None
    else:
        return int(match.group(1))
