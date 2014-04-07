class DNAElement:
    TAG = '*'
    PARENTS = []

    def __init__(self):
        self.parent = None
        self.children = []

    def reparentTo(self, parent):
        if self.parent:
            self.parent.children.remove(self)

        self.parent = parent

        if parent:
            self.parent.children.append(self)

    def handleText(self, chars):
        pass

    def findChildren(self, type):
        return [child for child in self.children if isinstance(child, type)]
