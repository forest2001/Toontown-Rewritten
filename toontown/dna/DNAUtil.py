from DNAVisGroup import DNAVisGroup


def getVisGroups(root):
    visGroups = []
    r_getVisGroups(root, visGroups)
    return visGroups
def r_getVisGroups(root, list):
    for child in root.children:
        if type(child) == DNAVisGroup:
            list.append(child)
        r_getVisGroups(child, list)
