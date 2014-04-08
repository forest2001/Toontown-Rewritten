from DNAVisGroup import DNAVisGroup


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


def getBlock(name):
    block = name[name.find(':')-2:name.find(':')]
    if block[0] > '9' or block[0] < '0':
        block = block[1:]
    return block
